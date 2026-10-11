#!/usr/bin/env python3
"""Assemble an unpublished review edition without modifying the delivered book."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'editions/next/manifest.json'


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
    used, outputs = [], []
    for item in config['chapters']:
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
        outputs.append((title, '\n\n'.join(parts)))
    if sorted(used) != sorted(chapters):
        raise ValueError('each retained substantive chapter must occur exactly once in this initial assembly')
    front = '# Dataset Production\n\n## From a first release to reliable practical datasets\n\n'
    front += f'Author: {config["author"]}\n\nInitial next-edition draft | {config["date"]}\n\n'
    front += ('Build and audit a small supplied release first, then use the same contracts across optional text, tabular, image, audio, reasoning and physical-data projects. No specialist hardware is required for the opening. Model fitting and inference remain in the separate training companion.\n\n'
              'New chapters were researched on 11 October 2026. Retained research and companion observations keep their original 2 October 2026 evidence boundary. Published experiments, illustrative calculations, executed fixture checks and proposed research are distinct. This review draft does not replace the delivered website/PDF.\n\n'
              '## Contents\n\n')
    guide = (ROOT / 'editions/next/progression.md').read_text()
    guide = guide.replace('# Beginner to practical application', '# Reader paths and data acquisition', 1)
    guide = guide.replace('\nAuthor: Puma\n', '\n', 1)
    front = front.replace('## Contents\n\n', guide + '\n\n## Contents\n\n')
    front += '\n'.join(f'- {i} {title}' for i, (title, _) in enumerate(outputs, 1))
    front += '\n- Retained appendices and reference ledger\n- Next edition research register\n\n'
    manuscript = front + '\n\n'.join(f'# {i} {title}\n\n{body}' for i, (title, body) in enumerate(outputs, 1))
    manuscript += '\n\n' + '\n\n'.join(extras) + '\n\n'
    register = (ROOT / 'editions/next/research-register.md').read_text()
    manuscript += register.replace('# Research register for the next edition', '# Next edition research register', 1)
    manuscript = re.sub(r'(!\[[^\]]*\]\(figures/[^)]+)\.png\)', r'\1.svg)', manuscript)
    metadata = {'author': config['author'], 'status': config['status'], 'base_commit': config['base_commit'],
                'chapters': len(outputs), 'retained_chapters': sorted(used),
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
    style = 'body{max-width:76ch;margin:3rem auto;padding:0 1.5rem;font:18px/1.65 system-ui;color:#202020}h1{margin-top:3rem;line-height:1.2}h2{line-height:1.3}img{max-width:100%;height:auto}table{display:block;overflow-x:auto;border-collapse:collapse;font-size:.85em}th,td{border:1px solid #ddd;padding:.5em;text-align:left}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f4f4f4;padding:1rem}a{color:#1257a4}code{overflow-wrap:anywhere}'
    page = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Dataset Production next edition review</title><style>' + style + '</style></head><body>' + rendered + '</body></html>\n'
    (output / 'index.html').write_text(page)
    print(json.dumps(metadata, indent=2))


if __name__ == '__main__':
    main()
