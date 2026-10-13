#!/usr/bin/env python3
"""Render the reviewed edition; --release also emits the exact PDF/source bundle."""
import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import zipfile
from social_metadata import inject
from build_next_edition import link_citations, make_pre_scrollable

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'docs/book'
CONFIG = ROOT / 'editions/principles/edition.json'


def render():
    config = json.loads(CONFIG.read_text())
    source = (BOOK / 'manuscript.md').read_text()
    body = subprocess.run(['pandoc', '-f', 'markdown', '-t', 'html5', '--wrap=none'], input=source, text=True, capture_output=True, check=True).stdout
    body = make_pre_scrollable(link_citations(body))
    headings = re.findall(r'<h1 id="([^"]+)">(.*?)</h1>', body)
    nav = ''.join(f'<a href="#{identity}">{title}</a>' for identity, title in headings)
    pdf_pages = config.get('pdf_pages')
    pages = f'{pdf_pages}-page PDF' if pdf_pages else 'Complete PDF'
    edition = f'{config["label"]} · {config["edition"]}'
    description = f'{config["chapters"]} core chapters · {config["tracks"]} optional tracks · {config["appendices"]} appendices'
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="A principles-first learning path from one small release to trustworthy evidence, controlled improvement and reliable delivery."><title>Dataset Production by Puma — Principles-first fieldbook</title><link rel="stylesheet" href="../style.css"><link rel="icon" href="../assets/icon.svg"></head><body><a class="skip-link" href="#book-content">Skip to book text</a><header class="site-header"><a class="brand" href="../"><span class="brand-icon" aria-hidden="true">▦</span><span>Dataset<span class="brand-second">Production</span></span></a><nav aria-label="Main navigation"><a href="./" aria-current="page">Read the book</a><a href="../#geometry">Open the labs</a><a href="../#tuldok">Tuldok concept</a></nav><a class="header-meta" href="../downloads/dataset-production.pdf">PDF ↓</a></header><div class="book-layout"><aside class="book-toc" aria-label="Book contents"><p>{html.escape(edition)}</p><label class="field" for="toc-search">Find a chapter</label><input id="toc-search" type="search" placeholder="Filter chapter titles…"><nav>{nav}</nav><p id="toc-result" aria-live="polite"></p><a href="manuscript.md" download>Download Markdown ↓</a><a href="../downloads/dataset-production-source.zip">Download source + exercises ↓</a><a href="../research-edition/">Previous research edition</a></aside><article class="book-body" id="book-content"><div class="book-edition">{html.escape(edition)}<br>{description} · {pages}<br>Authored examples, executed CPU fixtures, published results and source-inspected receipts have separate evidence boundaries.</div>{body}</article></div><footer class="site-footer"><div>▦ Dataset Production · Puma</div><p>{html.escape(edition)}</p><a href="../about.html">Evidence, privacy & reuse</a></footer><script src="reader.js"></script></body></html>'''
    (BOOK / 'index.html').write_text(inject(page, 'book/'))
    metadata = {**config, 'source_sha256': hashlib.sha256(source.encode()).hexdigest(), 'headings': [{'id': identity, 'title': re.sub('<[^>]+>', '', title)} for identity, title in headings]}
    (ROOT / 'docs/book-metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
    return source, body, metadata


def release(source, body):
    from render_pdf import render as render_pdf
    downloads = ROOT / 'docs/downloads'
    downloads.mkdir(exist_ok=True)
    pdf = downloads / 'dataset-production.pdf'
    pages = render_pdf(pdf)
    config = json.loads(CONFIG.read_text())
    config['pdf_pages'] = pages
    CONFIG.write_text(json.dumps(config, indent=2) + '\n')
    render()
    # Package only public, reader-facing source and runnable educational inputs.
    package = downloads / 'dataset-production-source.zip'
    include = [BOOK / 'manuscript.md'] + sorted((BOOK / 'figures').glob('*.svg'))
    include += [p for folder in (ROOT / 'editions', ROOT / 'examples') for p in sorted(folder.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc']
    include += [ROOT / 'scripts/build_book.py', ROOT / 'scripts/build_principles_edition.py', ROOT / 'scripts/build_next_edition.py', ROOT / 'scripts/social_metadata.py', ROOT / 'editions/research-2026-10-02/manuscript.md']
    include += [p for folder in (ROOT / 'scripts', ROOT / 'tests') for p in sorted(folder.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc']
    include += [p for p in sorted((ROOT / '.github/workflows').glob('*.yml')) if p.is_file()]
    include += [ROOT / 'README.md', ROOT / 'package.json']
    include += [p for p in sorted((ROOT / 'docs').rglob('*')) if p.is_file() and 'downloads' not in p.parts]
    include += sorted((ROOT / 'docs/downloads').glob('dataset-production-research-2026-10-02*'))
    include = sorted(set(include))
    bundle_files = {p.relative_to(ROOT).as_posix(): p.read_bytes() for p in include}
    bundle_files['README.txt'] = b'Dataset Production, Puma. Principles-first edition, 13 October 2026. The manuscript is docs/book/manuscript.md. Examples need Python 3.10+ and standard library. Book build dependencies are documented in editions/principles/README.md. No distribution license has been selected. Fixture outputs are descriptive, not generalization claims.\n'
    hashes = {name: hashlib.sha256(content).hexdigest() for name, content in bundle_files.items()}
    bundle_files['file-hashes.json'] = (json.dumps(hashes, indent=2, sort_keys=True) + '\n').encode()
    with zipfile.ZipFile(package, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(bundle_files.items()):
            item = zipfile.ZipInfo(name, date_time=(2026, 10, 13, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o644 << 16
            archive.writestr(item, content)
    checksums = {'edition': config['edition'], 'manuscript_sha256': hashlib.sha256(source.encode()).hexdigest(), 'pdf_pages': pages, 'files': {p.name: {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in (pdf, package)}}
    (downloads / 'checksums.json').write_text(json.dumps(checksums, indent=2) + '\n')
    print(json.dumps(checksums, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release', action='store_true')
    args = parser.parse_args()
    source, body, metadata = render()
    if args.release:
        release(source, body)
    else:
        print(f'Rendered {len(metadata["headings"])} sections; source SHA-256 {metadata["source_sha256"]}')


if __name__ == '__main__':
    main()
