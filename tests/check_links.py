#!/usr/bin/env python3
"""Check every static asset, local link, book citation and embedded lab link."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re
ROOT=Path(__file__).resolve().parents[1]/'docs'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  for k in ['href','src']:
   if k in a:self.links.append(a[k])
pages={}
for f in ROOT.rglob('*.html'):
 p=Page();p.feed(f.read_text());pages[f.resolve()]=p
 assert len(p.ids)==len(set(p.ids)),f'Duplicate HTML IDs in {f}'
routes={'home','geometry','splits','review','lineage','release','tuldok'}
checked=0
for f,p in pages.items():
 links=p.links[:]
 if f==ROOT.resolve()/'index.html':links+=re.findall(r'href="([^"$]+)',(ROOT/'app.js').read_text())
 for url in links:
  u=urlsplit(url)
  if u.scheme or u.netloc:continue
  target=(f.parent/unquote(u.path)).resolve() if u.path else f
  if target.is_dir():target=target/'index.html'
  assert target.exists(),f'Missing local file {url} from {f}'
  if u.fragment and target in pages:
   assert u.fragment in pages[target].ids or (target==ROOT.resolve()/'index.html' and u.fragment in routes),f'Missing local anchor {url} from {f}'
  checked+=1
print(f'Passed: {checked} local references across {len(pages)} HTML pages, including lab and citation links')
