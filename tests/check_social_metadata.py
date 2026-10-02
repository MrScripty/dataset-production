#!/usr/bin/env python3
"""Validate static cover-sharing tags and unchanged source dimensions."""
from html.parser import HTMLParser
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
BASE='https://mrscripty.github.io/dataset-production/'
IMAGE=BASE+'assets/book-cover.webp'
class Head(HTMLParser):
    def __init__(self):super().__init__();self.meta={};self.canonical=[];self.in_head=False
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='head':self.in_head=True
        if not self.in_head:return
        if tag=='meta':
            key=attrs.get('property',attrs.get('name',''))
            self.meta.setdefault(key,[]).append(attrs.get('content'))
        if tag=='link' and attrs.get('rel')=='canonical':self.canonical.append(attrs['href'])
    def handle_endtag(self,tag):
        if tag=='head':self.in_head=False
width,height=Image.open(ROOT/'docs/assets/book-cover.webp').size
assert (width,height)==(500,646)
for path,canonical in [('index.html',''),('book/index.html','book/'),('about.html','about.html')]:
    p=Head();p.feed((ROOT/'docs'/path).read_text())
    assert p.canonical==[BASE+canonical]
    for k in ['og:title','og:type','og:url','og:description','og:image','og:image:type','og:image:width','og:image:height','og:image:alt','twitter:card','twitter:image','twitter:title','twitter:description','twitter:image:alt']:
        assert len(p.meta.get(k,[]))==1,(path,k,'missing or duplicate')
    for k in ['og:image','og:image:secure_url','twitter:image']:assert p.meta[k]==[IMAGE]
    assert p.meta['og:url']==[BASE+canonical]
    assert p.meta['og:image:width']==[str(width)] and p.meta['og:image:height']==[str(height)]
    assert p.meta['og:image:type']==['image/webp']
    assert p.meta['og:title']==p.meta['twitter:title'] and p.meta['og:description']==p.meta['twitter:description']
    assert p.meta['og:image:alt']==p.meta['twitter:image:alt']
    assert p.meta['twitter:card']==['summary_large_image']
print('Passed: static cover metadata on homepage, reader (including chapter anchors), and about page')
