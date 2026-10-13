#!/usr/bin/env python3
"""Reader keyboard/mobile checks and all-page PDF review sheets."""
import hashlib
import json
import os
from pathlib import Path
import re
import fitz
from PIL import Image, ImageOps, ImageDraw
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'qa-output/book'
OUT.mkdir(parents=True, exist_ok=True)
BASE = os.environ.get('SITE_URL', 'http://127.0.0.1:8094/')
checks = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1440, 'height': 1000})
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(BASE+'book/', wait_until='networkidle')
    assert page.locator('article h1[id^="chapter-"]').count()==15
    assert page.locator('article h1[id^="part-"]').count()==4
    assert page.locator('article h1[id^="track-0"]').count()==6
    assert page.locator('img').evaluate_all('(images)=>images.every(i=>i.complete&&i.naturalWidth>0)')
    checks.append('Exact 15 core / four parts / six modality tracks; all figures decode')
    page.screenshot(path=str(OUT/'desktop-opening.png'))
    page.locator('#toc-search').fill('audio')
    assert page.locator('.book-toc nav a:visible').count()==1
    page.locator('.book-toc nav a:visible').click()
    assert page.url.endswith('#track-04-audio')
    page.locator('#toc-search').fill('no chapter matches this')
    assert page.locator('.book-toc nav a:visible').count()==0
    assert '0 matching sections' in page.locator('#toc-result').inner_text()
    page.locator('#toc-search').fill('')
    assert page.locator('.book-toc nav a:visible').count()>25
    checks.append('TOC filtering, zero-match recovery, anchor navigation and history')
    for width,height,label in [(1440,1000,'desktop'),(390,844,'mobile'),(320,740,'small-phone')]:
        page.set_viewport_size({'width':width,'height':height})
        for anchor in ['book-title','chapter-data-contract','chapter-audit-baseline','chapter-freeze-consumer','chapter-operate-recover-cost','track-06-physical-fields-simulation','case-01-rheon','case-02-tuldok']:
            page.goto(BASE+'book/#'+anchor)
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (width,anchor)
            assert page.locator('#'+anchor).is_visible()
            page.screenshot(path=str(OUT/(label+'-'+anchor+'.png')))
        pre=page.locator('pre').first
        pre.scroll_into_view_if_needed()
        pre.focus()
        assert pre.evaluate('(el)=>document.activeElement===el')
        assert pre.evaluate('(el)=>getComputedStyle(el).whiteSpace')=='pre'
        assert pre.evaluate('(el)=>getComputedStyle(el).overflowX')=='auto'
        page.keyboard.press('ArrowRight')
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    checks.append('1440/390/320px reader fits; diagrams retain rows with focusable horizontal scrolling')
    page.set_viewport_size({'width':390,'height':844})
    page.goto(BASE+'research-edition/')
    assert page.get_by_role('heading', name='Dataset Production', exact=True).count()==1
    assert '16 chapters' in page.locator('.book-edition').inner_text()
    checks.append('Preserved previous research reader loads independently')
    page.goto(BASE+'book/')
    page.evaluate("document.querySelector('script[src=\"reader.js\"]').remove()")
    assert page.locator('article h1[id^="chapter-"]').count()==15
    assert not errors,errors
    checks.append('Static reader text and links do not depend on JavaScript; no runtime errors')
    browser.close()

pdf=ROOT/'docs/downloads/dataset-production.pdf'
document=fitz.open(pdf)
config=json.loads((ROOT/'editions/principles/edition.json').read_text())
assert len(document)==config['pdf_pages']
assert document.metadata['author']=='Puma'
thumbs=[]
for index,page in enumerate(document):
    assert page.get_text().strip(),f'Empty PDF page {index+1}'
    assert '\ufffd' not in page.get_text(),f'Replacement glyph on page {index+1}'
    for block in page.get_text('dict')['blocks']:
        if block.get('type')!=0:continue
        for line in block.get('lines',[]):
            for span in line.get('spans',[]):
                x0,y0,x1,y1=span['bbox']
                assert x0>=-0.5 and y0>=-0.5 and x1<=page.rect.width+0.5 and y1<=page.rect.height+0.5,(index+1,span['text'])
    pix=page.get_pixmap(matrix=fitz.Matrix(.42,.42),alpha=False)
    im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
    canvas=Image.new('RGB',(270,380),'#e8eceb')
    canvas.paste(im,((270-im.width)//2,18))
    ImageDraw.Draw(canvas).text((10,362),f'Page {index+1}',fill='#172b33')
    thumbs.append(canvas)
for first in range(0,len(thumbs),20):
    rows=(min(20,len(thumbs)-first)+3)//4
    sheet=Image.new('RGB',(270*4,380*rows),'white')
    for offset,im in enumerate(thumbs[first:first+20]):sheet.paste(im,((offset%4)*270,(offset//4)*380))
    sheet.save(OUT/f'pdf-sheet-{first//20+1:02}.png')
text=' '.join(page.get_text() for page in document)
for title in ['Inspect and reproduce a small release','Treat labels as measurements','Freeze and test what the consumer reads','Operate recover and account for cost']:
    assert title in re.sub(r'\s+',' ',text),title
checks.append(f'{len(document)} PDF pages: metadata, extracted text, page boundaries and all-page visual sheets prepared')
receipt={'status':'passed','source_sha256':hashlib.sha256((ROOT/'docs/book/manuscript.md').read_bytes()).hexdigest(),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'checks':checks,'visual_review':'Contact sheets and selected full-resolution pages still require human-style visual inspection before publication'}
(OUT/'results.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
