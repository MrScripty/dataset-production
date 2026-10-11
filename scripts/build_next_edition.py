#!/usr/bin/env python3
"""Assemble an unpublished review edition without modifying the delivered book."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'editions/next/manifest.json'
CITATION_GROUP = re.compile(r'\[(?:[RTB]\d+)(?:\s*(?:,|[-–])\s*[RTB]\d+)*\]')
CITATION_ID = re.compile(r'[RTB]\d+')


class CitationLinker(HTMLParser):
    """Link known citation IDs in text, preserving markers and existing markup."""
    SKIP = {'a', 'code', 'pre', 'strong', 'script', 'style'}

    def __init__(self, references):
        super().__init__(convert_charrefs=False)
        self.references, self.parts, self.skipped = references, [], []

    def handle_starttag(self, tag, attrs):
        self.parts.append(self.get_starttag_text())
        if tag in self.SKIP:
            self.skipped.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.parts.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        self.parts.append(f'</{tag}>')
        if tag in self.SKIP and self.skipped and self.skipped[-1] == tag:
            self.skipped.pop()

    def handle_data(self, data):
        def group(match):
            return CITATION_ID.sub(lambda item: (
                f'<a class="citation" href="#reference-{item[0].lower()}">{item[0]}</a>'
                if item[0] in self.references else item[0]), match[0])
        self.parts.append(data if self.skipped else CITATION_GROUP.sub(group, data))

    def handle_entityref(self, name):
        self.parts.append('&' + name + ';')

    def handle_charref(self, name):
        self.parts.append('&#' + name + ';')

    def handle_comment(self, data):
        self.parts.append('<!--' + data + '-->')

    def handle_decl(self, decl):
        self.parts.append('<!' + decl + '>')


class PreformattedScroller(CitationLinker):
    """Keep preformatted text intact while making overflow keyboard reachable."""
    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        if tag == 'pre':
            existing = dict(attrs)
            additions = {'tabindex': '0', 'role': 'region',
                         'aria-label': 'Code or text diagram; scroll horizontally when needed'}
            extra = ''.join(f' {key}="{value}"' for key, value in additions.items()
                            if key not in existing)
            self.parts[-1] = self.parts[-1][:-1] + extra + '>'

    def handle_data(self, data):
        self.parts.append(data)


def make_pre_scrollable(rendered):
    parser = PreformattedScroller(set())
    parser.feed(rendered)
    parser.close()
    return ''.join(parser.parts)


class ReferenceAnchorer(CitationLinker):
    """Recognize entry paragraphs only inside the actual reference section."""
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
            'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self):
        super().__init__(set())
        self.stack, self.in_references, self.paragraph_start = [], False, False
        self.candidate = None

    def handle_starttag(self, tag, attrs):
        # An entry label must start as direct text in its leading strong element.
        if self.candidate is not None:
            self.candidate = None
        attributes = dict(attrs)
        if tag == 'h1' and not self.skipped:
            self.in_references = attributes.get('id') == 'references-and-evidence-notes'
        if tag == 'p':
            self.paragraph_start = True
        elif self.stack and self.stack[-1] == 'p':
            if tag == 'strong' and self.in_references and self.paragraph_start and not self.skipped:
                self.candidate = (len(self.parts), attributes.get('id'))
            self.paragraph_start = False
        super().handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag == 'strong':
            self.candidate = None
        super().handle_endtag(tag)
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_entityref(self, name):
        self.candidate, self.paragraph_start = None, False
        super().handle_entityref(name)

    def handle_charref(self, name):
        self.candidate, self.paragraph_start = None, False
        super().handle_charref(name)

    def handle_data(self, data):
        if self.candidate is not None:
            index, existing_id = self.candidate
            self.candidate = None
            match = re.match(r'^\[([RTB]\d+)\]', data)
            if match:
                label, anchor = match[1], 'reference-' + match[1].lower()
                if label in self.references:
                    raise ValueError('duplicate bibliography label would create an ambiguous citation link')
                if existing_id is not None and existing_id != anchor:
                    raise ValueError('reference entry already has a conflicting anchor')
                self.references.add(label)
                if existing_id is None:
                    self.parts[index] = self.parts[index][:-1] + f' id="{anchor}">'
        if self.stack and self.stack[-1] == 'p' and data.strip():
            self.paragraph_start = False
        self.parts.append(data)


def link_citations(rendered):
    """Only real entry paragraphs in the reference section create destinations."""
    anchorer = ReferenceAnchorer()
    anchorer.feed(rendered)
    anchorer.close()
    parser = CitationLinker(anchorer.references)
    parser.feed(''.join(anchorer.parts))
    parser.close()
    return ''.join(parser.parts)


def read_sections(source):
    chunks = re.split(r'(?m)(?=^# )', source)
    chapters, extras = {}, []
    for chunk in chunks:
        match = re.match(r'# (\d+) (.+)\n', chunk)
        if match:
            number = int(match[1])
            if number in chapters:
                raise ValueError(f'duplicate existing chapter {number}')
            chapters[number] = (match[2], chunk[match.end():].strip())
        elif chunk.startswith('# Appendix ') or chunk.startswith('# References '):
            extras.append(chunk.strip())
    return chapters, extras


def assemble():
    config = json.loads(MANIFEST.read_text())
    source = (ROOT / config['retained_source']).read_text()
    chapters, extras = read_sections(source)
    used, outputs, chapter_ids = [], [], set()
    for item in config['chapters']:
        identity = item['id']
        if not re.fullmatch(r'[a-z][a-z0-9-]*', identity) or identity in chapter_ids:
            raise ValueError('chapter IDs must be unique stable lowercase slugs')
        chapter_ids.add(identity)
        parts = []
        title = item.get('title')
        for segment in item['segments']:
            if 'existing_chapter' in segment:
                number = segment['existing_chapter']
                old_title, content = chapters[number]
                used.append(number)
                title = title or old_title
                parts.append(content)
            else:
                path = ROOT / segment['path']
                content = path.read_text()
                match = re.match(r'# (.+)\n', content)
                if not match:
                    raise ValueError(f'missing chapter title: {path}')
                title = title or match[1]
                # Resolve source-relative prose links to the review branch. Figures
                # inherited from the delivered edition are copied separately below.
                content = content[match.end():].strip()
                def resolve(match):
                    target = match[1]
                    if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                        return match[0]
                    resolved = (path.parent / target).resolve()
                    relative = resolved.relative_to(ROOT)
                    if not resolved.exists():
                        raise ValueError(f'broken local link in {path}: {target}')
                    return '](' + config['review_source_url'] + '/' + relative.as_posix() + ')'
                content = re.sub(r'\]\(([^)]+)\)', resolve, content)
                parts.append(content)
        outputs.append((title, '\n\n'.join(parts), 'chapter-' + identity))
    if sorted(used) != sorted(chapters):
        raise ValueError('each retained substantive chapter must occur exactly once in this initial assembly')
    front = '# Dataset Production {#book-title}\n\n## From a first release to reliable practical datasets\n\n'
    front += f'Author: {config["author"]}\n\nInitial next-edition draft | {config["date"]}\n\n'
    front += ('Build and audit a small supplied release first, then use the same contracts across optional text, tabular, image, audio, reasoning and physical-data projects. No specialist hardware is required for the opening. Model fitting and inference remain in the separate training companion.\n\n'
              'New chapters were researched on 11 October 2026. Retained research and companion observations keep their original 2 October 2026 evidence boundary. Published experiments, illustrative calculations, executed fixture checks and proposed research are distinct. This review draft does not replace the delivered website/PDF.\n\n'
              '## Contents {#contents}\n\n')
    guide = (ROOT / 'editions/next/progression.md').read_text()
    guide = guide.replace('# Beginner to practical application', '# Reader paths and data acquisition {#reader-paths}', 1)
    guide = guide.replace('\nAuthor: Puma\n', '\n', 1)
    front = front.replace('## Contents {#contents}\n\n', guide + '\n\n## Contents {#contents}\n\n')
    front += '- [Reader paths and data acquisition](#reader-paths)\n'
    front += '\n'.join(f'- [{i} {title}](#{anchor})' for i, (title, _, anchor) in enumerate(outputs, 1))
    anchored_extras = []
    for extra in extras:
        heading, content = extra.split('\n', 1)
        appendix = re.match(r'# Appendix ([A-D]) ', heading)
        anchor = 'appendix-' + appendix[1].lower() if appendix else 'references-and-evidence-notes'
        front += f'\n- [{heading[2:]}](#{anchor})'
        anchored_extras.append(heading + ' {#' + anchor + '}\n\n[Back to contents](#contents)\n' + content)
    front += '\n- [Next edition research register](#next-edition-research-register)\n\n'
    manuscript = front + '\n\n'.join(
        f'# {i} {title} {{#{anchor}}}\n\n[Back to contents](#contents)\n\n{body}'
        for i, (title, body, anchor) in enumerate(outputs, 1))
    manuscript += '\n\n' + '\n\n'.join(anchored_extras) + '\n\n'
    register = (ROOT / 'editions/next/research-register.md').read_text()
    manuscript += register.replace('# Research register for the next edition',
                                   '# Next edition research register {#next-edition-research-register}\n\n[Back to contents](#contents)', 1)
    manuscript = re.sub(r'(!\[[^\]]*\]\(figures/[^)]+)\.png\)', r'\1.svg)', manuscript)
    metadata = {'author': config['author'], 'status': config['status'], 'base_commit': config['base_commit'],
                'chapters': len(outputs), 'chapter_anchors': [anchor for _, _, anchor in outputs],
                'retained_chapters': sorted(used),
                'retained_source_sha256': hashlib.sha256(source.encode()).hexdigest(),
                'manuscript_sha256': hashlib.sha256(manuscript.encode()).hexdigest()}
    return manuscript, metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    output = args.out.resolve()
    # The review builder must never be a disguised deployment path.
    if output == ROOT or (ROOT / 'docs') == output or (ROOT / 'docs') in output.parents:
        parser.error('review output must be outside the published docs tree and repository root')
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        parser.error('choose an empty output directory')
    manuscript, metadata = assemble()
    rendered = subprocess.run(['pandoc', '-f', 'markdown', '-t', 'html5', '--wrap=none'],
                              input=manuscript, text=True, capture_output=True, check=True).stdout
    rendered = make_pre_scrollable(link_citations(rendered))
    output.mkdir(parents=True, exist_ok=True)
    figures = output / 'figures'
    figures.mkdir()
    for name in re.findall(r'!\[[^\]]*\]\(figures/([^)]*)\)', manuscript):
        source = ROOT / 'docs/book/figures' / name
        if not source.is_file():
            raise ValueError(f'missing figure: {source}')
        shutil.copyfile(source, figures / name)
    (output / 'manuscript.md').write_text(manuscript)
    (output / 'metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
    style = 'body{max-width:76ch;margin:3rem auto;padding:0 1.5rem;font:18px/1.65 system-ui;color:#202020;overflow-wrap:anywhere}h1{margin-top:3rem;line-height:1.2}h2{line-height:1.3}img{max-width:100%;height:auto}table{display:block;overflow-x:auto;border-collapse:collapse;font-size:.85em}th,td{border:1px solid #ddd;padding:.5em;text-align:left}pre{max-width:100%;box-sizing:border-box;overflow-x:auto;white-space:pre;overflow-wrap:normal;word-break:normal;background:#f4f4f4;padding:1rem}pre:focus-visible{outline:2px solid #1257a4;outline-offset:2px}a{color:#1257a4;overflow-wrap:anywhere}code{overflow-wrap:anywhere}pre code{white-space:inherit;overflow-wrap:normal;word-break:normal}'
    page = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Dataset Production next edition review</title><style>' + style + '</style></head><body>' + rendered + '</body></html>\n'
    (output / 'index.html').write_text(page)
    print(json.dumps(metadata, indent=2))


if __name__ == '__main__':
    main()
