#!/usr/bin/env python3
"""Assemble the principles-first source. No network or publication side effects."""
import hashlib
import json
from pathlib import Path
import re
import shutil
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / 'editions/principles'
CONFIG = EDITION / 'edition.json'
SOURCE_URL = '../source/'


def section(path, heading, anchor):
    source = path.read_text(encoding='utf-8')
    match = re.match(r'^# [^\n]+\n', source)
    if not match:
        raise ValueError(f'Missing first-level title: {path}')
    content = source[match.end():].strip()
    # Source modules may retain their own meaningful subheadings, never h1.
    if re.search(r'^# ', content, re.M):
        raise ValueError(f'Nested first-level heading: {path}')
    def link(match):
        target = match[1]
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or target.startswith('#') or target.startswith('figures/'):
            return match[0]
        local = (path.parent / parsed.path).resolve()
        relative = local.relative_to(ROOT)
        if not local.exists():
            raise ValueError(f'Missing source link {target} in {path}')
        return '](' + SOURCE_URL + relative.as_posix() + (('#' + parsed.fragment) if parsed.fragment else '') + ')'
    content = re.sub(r'\]\(([^)]+)\)', link, content)
    return f'# {heading} {{#{anchor}}}\n\n[Back to contents](#contents)\n\n{content}\n'


def assemble():
    config = json.loads(CONFIG.read_text())
    core = sorted((EDITION / 'core').glob('[0-9][0-9]-*.md'))
    if [int(p.name[:2]) for p in core] != list(range(1, 16)):
        raise ValueError('Exactly chapters 01–15 required')
    sections, nav = [], []
    for number, path in enumerate(core, 1):
        title = path.read_text().splitlines()[0][2:]
        title = re.sub(r'^\d+\s+', '', title)
        anchor = 'chapter-' + config['chapter_ids'][number - 1]
        part = next(item for item in config['parts'] if item['first'] == number) if number in (1, 5, 9, 13) else None
        if part:
            index = config['parts'].index(part) + 1
            sections.append(f'# Part {index}: {part["title"]} {{#part-{index}}}\n\nChapters {part["first"]}–{part["last"]}.\n')
            nav.append(f'- [Part {index}: {part["title"]}](#part-{index})')
        sections.append(section(path, f'{number} {title}', anchor))
        nav.append(f'  - [{number} {title}](#{anchor})')
    tracks = sorted((EDITION / 'tracks').glob('*.md'))
    modality = [p for p in tracks if not p.name.startswith('advanced')]
    if len(modality) != 6:
        raise ValueError(f'Exactly six modality tracks required, found {len(modality)}')
    sections.append('# Optional tracks {#optional-tracks}\n\nChoose a track after chapter 8. Carry its small example through chapters 9–15; the track does not replace independence, audit or recovery checks. Complete one controlled improvement and study the other approaches conceptually.\n')
    nav.append('- [Optional tracks](#optional-tracks)')
    for path in tracks:
        title = path.read_text().splitlines()[0][2:]
        anchor = 'track-' + path.stem
        sections.append(section(path, title, anchor))
        nav.append(f'  - [{title}](#{anchor})')
    case_paths = sorted((EDITION / 'cases').glob('[0-9][0-9]-*.md'))
    if (EDITION / 'cases/evidence-ledger.md').exists():
        case_paths.append(EDITION / 'cases/evidence-ledger.md')
    for path in case_paths:
        title = path.read_text().splitlines()[0][2:]
        anchor = 'case-' + path.stem
        sections.append(section(path, title, anchor))
        nav.append(f'- [{title}](#{anchor})')
    retained = (ROOT / 'editions/research-2026-10-02/manuscript.md').read_text()
    for text in re.split(r'(?m)(?=^# )', retained):
        if text.startswith('# Appendix '):
            heading, content = text.split('\n', 1)
            letter = re.match(r'# Appendix ([A-D]) ', heading)[1]
            anchor = 'appendix-' + letter.lower()
            historical = ('Retained companion/source contract from the 2 October 2026 research edition. These observations remain pinned to the revisions cited below; they are not fresh runtime tests. The supported educational text consumer in chapter 14 is separate from the numeric companion.\n\n' if letter == 'A' else 'Retained reference worksheet from the 2 October 2026 research edition; use the current chapter evidence gates when filling it.\n\n')
            sections.append(heading + ' {#' + anchor + '}\n\n[Back to contents](#contents)\n\n' + historical + content.strip() + '\n')
            nav.append(f'- [{heading[2:]}](#{anchor})')
        elif text.startswith('# References '):
            sections.append(text.split('\n', 1)[0] + ' {#references-and-evidence-notes}\n\n[Back to contents](#contents)\n\nHistorical bibliography retained for migrated material. Repository and companion observations below keep their original dates and revisions. New case evidence is pinned in the case ledgers; newer methods link directly to primary sources at the relevant lesson. No cited experiment was rerun unless explicitly marked executed fixture.\n\n' + text.split('\n', 1)[1].strip() + '\n')
            nav.append('- [References and evidence notes](#references-and-evidence-notes)')
    front = '''# Dataset Production {#book-title}

## From one useful release to trustworthy evidence

Author: Puma

Principles-first edition | 13 October 2026

A dataset is a set of choices about what counts, what values mean and what evidence supports using them. This book teaches those reasons before workflows. Start with a small release you can inspect. Then protect independence, test one improvement and deliver bytes another person can interpret and recover.

The core assumes basic reading and arithmetic. No GPU, sensors, paid service, account or external dataset download is required. Code is optional until you choose the supplied CPU labs. Six optional tracks let the same principles travel across representations.

### How to learn

Observe and explain; calculate or classify on paper; optionally run a supplied CPU exercise; change one thing; defend a release decision. Read the worked answer after trying. An acceptance check identifies what evidence is missing, rather than rewarding a plausible explanation alone.

The four part assessments build one capstone: a bounded claim and contract, source and rights, lineage and split rationale, audit, controlled improvement, tested consumer and demonstrated recovery. Missing evidence means revise. Leakage, unsupported rights or compatibility, and misleading evaluation block acceptance.

### What the evidence labels mean

- Authored illustration: invented records or arithmetic for explanation, not observed population performance
- Executed fixture: reproducible CPU output from the supplied code, within its tiny teaching scope
- Independently reviewed reference: only when a named review protocol and independent reference evidence exist; the supplied gold file is separately authored, not this category
- Published result: the cited authors' experiment, not reproduced here
- Source-inspected receipt: a pinned project artifact read for this edition, not a fresh runtime reproduction
- Proposed or unrun work: an experiment, integration or validation still needing execution

The observation unit, denominator, revision and limits belong beside a result. A checksum proves identity of bytes. It does not prove labels, generalization, physics or permission.

### Companion boundary

Training Your Own Models stays a separate companion for fitting implementations, architectures and neural training. This book ends at a tested data and consumer contract. The educational text adapter supports its specifically named consumer; numeric companion examples generate their own inputs. There is no automatic text-to-numeric compatibility.

### Rights and privacy

The supplied records and tiny grids are fictional teaching fixtures, with no real participant data. No distribution license has been selected for this repository or book. Public visibility is not a reuse license. External sources retain their own terms. Do not put private messages into a fixture and assume quarantine sanitizes them.

## Contents {#contents}

'''
    manuscript = front + '\n'.join(nav) + '\n\n' + '\n\n'.join(sections)
    manuscript = re.sub(r'(!\[[^\]]*\]\(figures/[^)]+)\.png\)', r'\1.svg)', manuscript)
    metadata = {**config, 'manuscript_sha256': hashlib.sha256(manuscript.encode()).hexdigest(), 'modules': [p.relative_to(ROOT).as_posix() for p in core + tracks + case_paths]}
    return manuscript, metadata


def main():
    manuscript, metadata = assemble()
    (ROOT / 'docs/book/manuscript.md').write_text(manuscript, encoding='utf-8')
    (EDITION / 'assembly.json').write_text(json.dumps(metadata, indent=2) + '\n')
    # Mirror only explicitly linked public source, so local/PDF review does not
    # depend on an unpublished or moving repository branch.
    for relative in sorted(set(re.findall(r'\]\(\.\./source/([^)#]+)', manuscript))):
        source = ROOT / relative
        target = ROOT / 'docs/source' / relative
        if source.is_dir():
            shutil.copytree(source, target, dirs_exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    print(json.dumps({'chapters': metadata['chapters'], 'tracks': metadata['tracks'], 'source_sha256': metadata['manuscript_sha256']}))


if __name__ == '__main__':
    main()
