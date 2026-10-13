#!/usr/bin/env python3
"""Filesystem-only PDF integrity, geometry and all-page visual review sheets."""
import hashlib,json,re
from pathlib import Path
import fitz
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'qa-output/pdf';OUT.mkdir(parents=True,exist_ok=True)
pdf=ROOT/'docs/downloads/dataset-production.pdf';document=fitz.open(pdf)
config=json.loads((ROOT/'editions/principles/edition.json').read_text())
assert len(document)==config['pdf_pages'];assert document.metadata['author']=='Puma'
thumbs=[];links=0;text=[]
for index,page in enumerate(document):
 content=page.get_text();assert content.strip(),index+1;assert '\ufffd' not in content,index+1;text.append(content)
 for block in page.get_text('dict')['blocks']:
  if block.get('type')!=0:continue
  for line in block.get('lines',[]):
   for span in line.get('spans',[]):
    x0,y0,x1,y1=span['bbox'];assert x0>=-.5 and y0>=-.5 and x1<=page.rect.width+.5 and y1<=page.rect.height+.5,(index+1,span['text'],span['bbox'])
 for link in page.get_links():
  links+=1;uri=link.get('uri','');assert not uri.startswith('file:'),(index+1,uri);assert '/workspace/' not in uri,(index+1,uri)
 pix=page.get_pixmap(matrix=fitz.Matrix(.42,.42),alpha=False);im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
 canvas=Image.new('RGB',(270,380),'#e8eceb');canvas.paste(im,((270-im.width)//2,18));ImageDraw.Draw(canvas).text((10,362),f'Page {index+1}',fill='#172b33');thumbs.append(canvas)
for first in range(0,len(thumbs),20):
 rows=(min(20,len(thumbs)-first)+3)//4;sheet=Image.new('RGB',(1080,380*rows),'white')
 for offset,im in enumerate(thumbs[first:first+20]):sheet.paste(im,((offset%4)*270,(offset//4)*380))
 sheet.save(OUT/f'contact-{first//20+1:02}.png')
whole=re.sub(r'\s+',' ',' '.join(text))
for title in ['Inspect and reproduce a small release','Treat labels as measurements','Freeze and test what the consumer reads','Operate recover and account for cost','Case evidence ledger']:
 assert title in whole,title
assert links>150,links
receipt={'status':'structural checks passed; visual inspection required','pages':len(document),'links':links,'manuscript_sha256':hashlib.sha256((ROOT/'docs/book/manuscript.md').read_bytes()).hexdigest(),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'contact_sheets':len(list(OUT.glob('contact-*.png'))),'checks':['all pages contain text','no replacement glyphs','all text bounds inside page','Puma author metadata','no private file URI/workspace links','all core and case headings present','internal/external links emitted']}
(OUT/'results.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
