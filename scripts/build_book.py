#!/usr/bin/env python3
"""Render the reviewed Markdown edition. Requires Pandoc; no browser runtime dependency."""
import hashlib, html, json, re, subprocess
from pathlib import Path
from social_metadata import inject
ROOT=Path(__file__).resolve().parents[1]
BOOK=ROOT/'docs/book'
source=(BOOK/'manuscript.md').read_text()
source=source.replace('](figures/',' ](figures/') if False else source
# Published diagrams are original SVGs from the delivered book source bundle.
source=re.sub(r'(!\[[^\]]*\]\(figures/[^)]+)\.png\)',r'\1.svg)',source)
body=subprocess.run(['pandoc','-f','markdown','-t','html5','--wrap=none'],input=source,text=True,capture_output=True,check=True).stdout
# Stable semantic anchors survive a chapter number changing between editions.
body=re.sub(r'id="\d+-([^"\n]+)"',r'id="\1"',body)
headings=re.findall(r'<h1 id="([^"]+)">(.*?)</h1>',body)
for ref in re.findall(r'<strong>\[([RTB]\d+)\]',body):
 body=body.replace(f'<strong>[{ref}]',f'<strong id="reference-{ref.lower()}">[{ref}]')
# Link inline source labels without modifying source headings, attributes, or code.
parts=re.split(r'(<[^>]+>)',body)
inside_link=inside_strong=inside_code=0
for i,p in enumerate(parts):
 if p.startswith('<'):
  if re.match(r'<a\b',p):inside_link+=1
  if p=='</a>':inside_link=max(0,inside_link-1)
  if p.startswith('<strong'):inside_strong+=1
  if p=='</strong>':inside_strong=max(0,inside_strong-1)
  if p.startswith('<code'):inside_code+=1
  if p=='</code>':inside_code=max(0,inside_code-1)
 elif not(inside_link or inside_strong or inside_code):
  parts[i]=re.sub(r'\[([RTB]\d+)\]',lambda m:f'<a class="citation" href="#reference-{m[1].lower()}">[{m[1]}]</a>',p)
body=''.join(parts)
nav=''.join(f'<a href="#{i}">{title}</a>' for i,title in headings)
title=re.sub('<[^>]+>','',headings[0][1])
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Read the complete research fieldbook on dataset production, training contracts, and proposed Tuldok workspaces."><title>{html.escape(title)} — Fieldbook</title><link rel="stylesheet" href="../style.css"><link rel="icon" href="../assets/icon.svg" type="image/svg+xml"></head><body><a class="skip-link" href="#book-content">Skip to book</a><header class="site-header"><a class="brand" href="../"><span class="brand-icon" aria-hidden="true">▦</span><span>Dataset<span class="brand-second">Production</span></span></a><nav aria-label="Main navigation"><a href="./" aria-current="page">Read the book</a><a href="../#geometry">Open the labs</a><a href="../#tuldok">Tuldok concept</a></nav><a class="header-meta" href="../downloads/dataset-production.pdf">PDF ↓</a></header><div class="book-layout"><aside class="book-toc" aria-label="Book contents"><p>Research edition · 02 Oct 2026</p><label class="field" for="toc-search">Find a chapter</label><input id="toc-search" type="search" placeholder="Filter chapter titles…"><nav>{nav}</nav><p id="toc-result" aria-live="polite"></p><a href="manuscript.md" download>Download Markdown ↓</a><a href="../downloads/dataset-production-source.zip">Download source + diagrams ↓</a></aside><article class="book-body" id="book-content"><div class="book-edition">Revised delivered research edition · 16 chapters + 4 appendices · 80-page PDF<br>Repository observations are pinned to the commits cited. Interface concepts are proposals. Experiments and trainer compatibility have not been runtime-validated by this book.</div>{body}</article></div><footer class="site-footer"><div>▦ Dataset Production</div><p>Research edition · 2 October 2026</p><a href="../about.html">Evidence, privacy & reuse</a></footer><script src="reader.js"></script></body></html>'''
(BOOK/'index.html').write_text(inject(page,'book/'))
(ROOT/'docs/book-metadata.json').write_text(json.dumps({'title':title,'edition':'2026-10-02','chapters':16,'pdf_pages':80,'source_sha256':hashlib.sha256((BOOK/'manuscript.md').read_bytes()).hexdigest(),'headings':[{'id':i,'title':re.sub('<[^>]+>','',t)} for i,t in headings]},indent=2)+'\n')
print(f'Rendered {len(headings)} top-level sections; source SHA-256 {hashlib.sha256(source.encode()).hexdigest()}')
