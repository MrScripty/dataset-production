#!/usr/bin/env python3
"""Typeset the exact Pandoc AST with no browser or network dependency."""
import html,json,re,subprocess,textwrap
from pathlib import Path
from reportlab import rl_config
rl_config.invariant=1
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate,Frame,PageTemplate,Paragraph,Spacer,PageBreak,LongTable,TableStyle,Image,Preformatted,KeepTogether
from reportlab.platypus.tableofcontents import TableOfContents
from PIL import Image as PILImage
ROOT=Path(__file__).resolve().parents[1];BOOK=ROOT/'docs/book'
WIDTH,HEIGHT=595.276,841.890;LEFT=RIGHT=TOP=BOTTOM=50;CONTENT=WIDTH-LEFT-RIGHT
for name,file in [('Sans','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Italic','DejaVuSans-Oblique.ttf'),('Mono','DejaVuSansMono.ttf')]:
 pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
pdfmetrics.registerFontFamily('Sans',normal='Sans',bold='Bold',italic='Italic',boldItalic='Bold')
INK=colors.HexColor('#172b33');TEAL=colors.HexColor('#076b62')
styles={
 'body':ParagraphStyle('Body',fontName='Sans',fontSize=10.2,leading=14.8,textColor=INK,spaceAfter=7,allowWidows=0,allowOrphans=0,splitLongWords=1),
 'title':ParagraphStyle('Title',fontName='Bold',fontSize=35,leading=41,textColor=INK,spaceAfter=24),
 'h1':ParagraphStyle('Chapter',fontName='Bold',fontSize=23,leading=29,textColor=INK,spaceAfter=17,keepWithNext=True),
 'h2':ParagraphStyle('Section',fontName='Bold',fontSize=13.5,leading=18.2,textColor=INK,spaceBefore=12,spaceAfter=7,keepWithNext=True),
 'h3':ParagraphStyle('Subsection',fontName='Bold',fontSize=11.2,leading=15.2,textColor=INK,spaceBefore=9,spaceAfter=6,keepWithNext=True),
 'code':ParagraphStyle('Code',fontName='Mono',fontSize=8.2,leading=11.4,textColor=INK,backColor=colors.HexColor('#f0f4f2'),borderPadding=8,spaceBefore=7,spaceAfter=10),
 'table':ParagraphStyle('Cell',fontName='Sans',fontSize=8.4,leading=11.6,textColor=INK,splitLongWords=1),
 'th':ParagraphStyle('TableHeader',fontName='Bold',fontSize=8.5,leading=11.7,textColor=INK,splitLongWords=1),
 'caption':ParagraphStyle('Caption',fontName='Sans',fontSize=9,leading=12.5,textColor=colors.HexColor('#526168'),spaceAfter=12),
 'toc':ParagraphStyle('Contents',fontName='Sans',fontSize=9.5,leading=14.7,textColor=INK,spaceAfter=4)}

def plain(inlines):
 out=[]
 for x in inlines:
  t,c=x['t'],x.get('c')
  if t=='Str':out.append(c)
  elif t in ('Space','SoftBreak','LineBreak'):out.append(' ')
  elif t=='Code':out.append(c[1])
  elif t in ('Strong','Emph','Underline','Strikeout','Superscript','Subscript','SmallCaps'):out.append(plain(c))
  elif t in ('Link','Image','Span','Cite'):out.append(plain(c[1]))
  elif t=='Quoted':out.append('“'+plain(c[1])+'”')
  elif t=='Math':out.append(c[1])
 return ''.join(out)

def inline(inlines):
 out=[]
 for x in inlines:
  t,c=x['t'],x.get('c')
  if t=='Str':out.append(html.escape(c))
  elif t in ('Space','SoftBreak'):out.append(' ')
  elif t=='LineBreak':out.append('<br/>')
  elif t=='Code':out.append('<font name="Mono">'+html.escape(c[1])+'</font>')
  elif t=='Strong':out.append('<b>'+inline(c)+'</b>')
  elif t=='Emph':out.append('<i>'+inline(c)+'</i>')
  elif t=='Link':
   target=c[2][0]
   if target.startswith('../source/'):target='https://mrscripty.github.io/dataset-production/source/'+target[len('../source/'):]
   out.append('<link href="'+html.escape(target,quote=True)+'" color="#076b62">'+inline(c[1])+'</link>')
  elif t in ('Image','Span','Cite'):out.append(inline(c[1]))
  elif t=='Quoted':out.append('“'+inline(c[1])+'”')
  elif t in ('Underline','Strikeout','SmallCaps'):out.append(inline(c))
  elif t=='Superscript':out.append('<super>'+inline(c)+'</super>')
  elif t=='Subscript':out.append('<sub>'+inline(c)+'</sub>')
  elif t=='Math':out.append(html.escape(c[1]))
  elif t=='Note':out.append(' [Note: '+' '.join(plain(b['c']) for b in c if b['t'] in ('Plain','Para'))+']')
  elif t=='RawInline':out.append(html.escape(re.sub('<[^>]+>','',c[1])))
 return ''.join(out)

class BookDoc(BaseDocTemplate):
 def __init__(self,target):
  super().__init__(str(target),pagesize=(WIDTH,HEIGHT),leftMargin=LEFT,rightMargin=RIGHT,topMargin=TOP,bottomMargin=BOTTOM,title='Dataset Production',author='Puma',subject='Principles-first edition: 15 core chapters and six optional tracks',pageCompression=1)
  frame=Frame(LEFT,BOTTOM,CONTENT,HEIGHT-TOP-BOTTOM,id='body',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
  self.addPageTemplates(PageTemplate(id='book',frames=[frame],onPage=self.decorate))
 def decorate(self,canvas,doc):
  canvas.saveState();canvas.setFont('Sans',7.5);canvas.setFillColor(colors.HexColor('#526168'))
  if doc.page>1:canvas.drawString(LEFT,HEIGHT-27,'DATASET PRODUCTION · PUMA')
  canvas.drawString(LEFT,25,'Principles-first edition | 13 October 2026');canvas.drawRightString(WIDTH-RIGHT,25,str(doc.page));canvas.restoreState()
 def afterFlowable(self,f):
  if getattr(f,'_bookmark',None):
   self.canv.bookmarkPage(f._bookmark)
   if getattr(f,'_toc',False):
    self.canv.addOutlineEntry(f._plain,f._bookmark,level=0,closed=False);self.notify('TOCEntry',(0,f._plain,self.page,f._bookmark))
  if getattr(f,'_reference',None):self.canv.bookmarkPage(f._reference)

def image(x):
 target=x['c'][2][0];file=(BOOK/target).with_suffix('.png') if target.endswith('.svg') else BOOK/target
 if not file.is_file():raise ValueError('Missing raster companion '+str(file))
 w,h=PILImage.open(file).size;s=min(CONTENT/w,390/h);return Image(str(file),width=w*s,height=h*s)

def story_from(blocks):
 first=True;in_refs=False;skip_toc=False
 def convert(blocks,indent=0):
  nonlocal first,in_refs,skip_toc
  out=[]
  for b in blocks:
   t,c=b['t'],b.get('c')
   if t=='Header':
    level,attrs,words=c;title=plain(words);ident=attrs[0]
    if ident=='contents':
     out.extend([PageBreak(),Paragraph('Contents',styles['h1'])]);toc=TableOfContents();toc.levelStyles=[styles['toc']];toc.dotsMinLevel=0;out.extend([toc,Spacer(1,12)]);skip_toc=True;continue
    if level==1:
     skip_toc=False
     if not first and out and not isinstance(out[-1],PageBreak):out.append(PageBreak())
     if first:out.append(Spacer(1,48))
     p=Paragraph(inline(words),styles['title'] if first else styles['h1']);p._bookmark=ident;p._toc=not first;p._plain=title;out.append(p);first=False;in_refs=ident=='references-and-evidence-notes'
    else:
     p=Paragraph(inline(words),styles['h2'] if level==2 else styles['h3']);p._bookmark=ident;out.append(p)
   elif skip_toc and t in ('BulletList','OrderedList'):continue
   elif t in ('Para','Plain'):
    if c and c[0]['t']=='Image':out.append(image(c[0]));continue
    txt=inline(c)
    if not in_refs:
     def citation(group):
      return re.sub(r'[RTB]\d+',lambda m:'<link href="#reference-'+m[0].lower()+'" color="#076b62">'+m[0]+'</link>',group[0])
     txt=re.sub(r'\[(?:[RTB]\d+)(?:\s*(?:,|[-–])\s*[RTB]\d+)*\]',citation,txt)
    if txt.startswith('<link href="#contents"'):continue
    style=ParagraphStyle('Indented',parent=styles['body'],leftIndent=indent) if indent else styles['body'];p=Paragraph(txt,style)
    if in_refs:
     m=re.match(r'^\[([RTB]\d+)\]',plain(c))
     if m:p._reference='reference-'+m[1].lower()
    out.append(p)
   elif t=='CodeBlock':
    lines=[]
    for line in c[1].splitlines():lines.extend(textwrap.wrap(line,width=94,expand_tabs=False,replace_whitespace=False,drop_whitespace=False,break_long_words=True,break_on_hyphens=False) or [''])
    group=[Preformatted('\n'.join(lines),styles['code'])]
    if out and isinstance(out[-1],Paragraph) and len(out[-1].getPlainText())<150:
     group.insert(0,out.pop())
     if out and isinstance(out[-1],Paragraph) and out[-1].style.name in ('Section','Subsection'):
      group.insert(0,out.pop())
    out.append(KeepTogether(group))
   elif t in ('BulletList','OrderedList'):
    items=c if t=='BulletList' else c[1];start=1 if t=='BulletList' else c[0][0]
    for index,items_blocks in enumerate(items,start):
     child=convert(items_blocks,indent+14)
     if child and isinstance(child[0],Paragraph):
      child[0].bulletText='•' if t=='BulletList' else str(index)+'.';child[0].style=ParagraphStyle('Bullet',parent=child[0].style,bulletIndent=indent,firstLineIndent=0,leftIndent=indent+14)
     out.extend(child)
   elif t=='Table':
    _,caption,spec,head,bodies,foot=c;rows=[]
    def cells(row,style):return [Paragraph(' '.join(inline(x['c']) for x in cell[4] if x['t'] in ('Plain','Para')),style) for cell in row[1]]
    for row in head[1]:rows.append(cells(row,styles['th']))
    repeats=len(rows)
    for body in bodies:
     for row in body[2]+body[3]:rows.append(cells(row,styles['table']))
    if not rows:continue
    n=len(spec)
    if any(len(row)!=n for row in rows):raise ValueError('Spanning table cell unsupported')
    weights=[x[1].get('c',1/n) for x in spec];widths=[CONTENT*x/sum(weights) for x in weights]
    table=LongTable(rows,colWidths=widths,repeatRows=repeats,hAlign='LEFT',spaceBefore=8,spaceAfter=11)
    table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#c4cfce')),('BACKGROUND',(0,0),(-1,repeats-1),colors.HexColor('#e1eee8')),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));out.append(table)
   elif t=='Figure':
    attrs,caption,parts=c;items=[]
    for part in parts:
     if part['t'] in ('Plain','Para'):
      for x in part['c']:
       if x['t']=='Image':items.append(image(x))
    text=' '.join(plain(x['c']) for x in caption[1] if x['t'] in ('Plain','Para'))
    if text:items.append(Paragraph(html.escape(text),styles['caption']))
    out.append(KeepTogether(items))
   elif t in ('BlockQuote','Div'):out.extend(convert(c if t=='BlockQuote' else c[1],indent+12))
   elif t=='HorizontalRule':out.append(Spacer(1,12))
   elif t=='Null':continue
   else:raise ValueError('Unsupported PDF block '+t)
  return out
 return convert(blocks)

def render(target):
 source=(BOOK/'manuscript.md').read_text();ast=json.loads(subprocess.run(['pandoc','-f','markdown','-t','json'],input=source,text=True,capture_output=True,check=True).stdout)
 doc=BookDoc(target);doc.multiBuild(story_from(ast['blocks']))
 import fitz
 pdf=fitz.open(target);pages=len(pdf)
 for page in pdf:
  if not page.get_text().strip():raise ValueError('Empty PDF page')
 pdf.close();return pages
if __name__=='__main__':print(render(ROOT/'docs/downloads/dataset-production.pdf'))
