#!/usr/bin/env python3
"""Static sharing metadata for crawlers, without changing page bodies."""
from html import escape
from pathlib import Path
import re
BASE='https://mrscripty.github.io/dataset-production/'
IMAGE=BASE+'assets/book-cover.webp'
TITLE='Dataset Production by Puma'
DESCRIPTION='An 80-page fieldbook on building reliable training data, with interactive examples and proposed Tuldok workspaces.'
ALT='Dataset Production book cover by Puma, showing photographs, sound waveforms, and botanical annotation in a warm study.'
START='<!-- book-sharing-metadata:start -->'
END='<!-- book-sharing-metadata:end -->'
def metadata(relative_path=''):
    url=BASE+relative_path
    tags=[('og:type','website'),('og:site_name','Dataset Production'),('og:title',TITLE),('og:description',DESCRIPTION),('og:url',url),('og:image',IMAGE),('og:image:secure_url',IMAGE),('og:image:type','image/webp'),('og:image:width','500'),('og:image:height','646'),('og:image:alt',ALT)]
    output=[START,f'<link rel="canonical" href="{escape(url,quote=True)}">']
    output += [f'<meta property="{key}" content="{escape(value,quote=True)}">' for key,value in tags]
    twitter=[('twitter:card','summary_large_image'),('twitter:title',TITLE),('twitter:description',DESCRIPTION),('twitter:image',IMAGE),('twitter:image:alt',ALT)]
    output += [f'<meta name="{key}" content="{escape(value,quote=True)}">' for key,value in twitter]
    return '\n'.join(output+[END])
def inject(page,relative_path=''):
    page=re.sub(re.escape(START)+r'.*?'+re.escape(END)+r'\n?', '', page,flags=re.S)
    assert '</head>' in page
    return page.replace('</head>',metadata(relative_path)+'\n</head>',1)
if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]/'docs'
    for path,canonical in [('index.html',''),('book/index.html','book/'),('about.html','about.html')]:
        file=root/path;file.write_text(inject(file.read_text(),canonical))
        print(f'Updated sharing metadata: {path}')
