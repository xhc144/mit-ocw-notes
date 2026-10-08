#!/usr/bin/env python3
"""Acquire the explicitly selected MIT OCW PDFs; no off-host redirects."""
import urllib.request,urllib.parse,json,re,hashlib,concurrent.futures
from pathlib import Path
from html.parser import HTMLParser
import fitz
ROOT=Path(__file__).resolve().parents[3]/'sources/graph-theory'
if (ROOT/'source-manifest.json').exists() and json.loads((ROOT/'source-manifest.json').read_text()).get('selection_frozen'):
 raise SystemExit('Source selection is frozen; verify_sources.py checks it without rewriting the archive.')
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  if tag=='a':self.links.append(dict(attrs).get('href',''))
def get(u):
 with urllib.request.urlopen(u,timeout=45) as r:
  if urllib.parse.urlparse(r.url).hostname!='ocw.mit.edu':raise ValueError('off-host redirect')
  return r.read(),r.url
SELECT={'18315':{f'lec{i:02d}' for i in [1,*range(3,13),*range(19,26),27]},'18433':{'l123','l78','l9'},'18212':{f'mit18_212s19_lec{i}' for i in [22,23,*range(26,33)]},'18217':{'mit18_217f19_ch2','mit18_217f19_ch4'},'6042':{'mit6_042js15_textbook.pdf'}}
AUTHORS={'18315':['Igor Pak (lecturer)','Amanda Redlich (notes)'],'18433':['Santosh Vempala'],'18212':['Alexander Postnikov (lecturer)','Andrew Lin (notes)'],'18217':['Yufei Zhao (lecturer/editor)','MIT 18.217 Fall 2019 class students (notes)'],'6042':['Eric Lehman','F. Thomson Leighton','Albert R. Meyer']}
YEAR={'18315':2005,'18433':2003,'18212':2019,'18217':2019,'6042':2015}
def one(item):
 k,u=item;slug=u.rstrip('/').split('/')[-1]
 if not u.endswith('.pdf'):
  b,_=get(u);(ROOT/'pages'/f'{k}-{slug}.html').write_bytes(b);p=Links();p.feed(b.decode());ps=list(dict.fromkeys(urllib.parse.urljoin(u,x) for x in p.links if x.endswith('.pdf')))
  if len(ps)!=1:raise ValueError((u,ps))
  pdf=ps[0]
 else:pdf=u
 b,final=get(pdf);name=f'{k}-{slug.removesuffix(".pdf")}.pdf'; path=ROOT/'originals'/name;path.write_bytes(b)
 d=fitz.open(stream=b,filetype='pdf');txt='\n\f\n'.join(p.get_text() for p in d);(ROOT/'text'/name.replace('.pdf','.txt')).write_text(txt)
 flags=[]
 for i,p in enumerate(d):
  for line in p.get_text().splitlines():
   if re.search(r'copyright|rights reserved|permission|creative commons|CC BY|©|courtesy|removed',line,re.I):flags.append({'pdf_page':i+1,'text':line})
 return {'id':f'{k}-{slug.removesuffix(".pdf")}','course':k,'year':YEAR[k],'authors':AUTHORS[k],'resource_url':u,'url':pdf,'final_url':final,'path':f'originals/{name}','pages':len(d),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'pdf_metadata':d.metadata,'rights_flags':flags,'license':'MIT OCW default CC BY-NC-SA 4.0; individual notices prevail','archive_allowed':None,'license_review':'pending','downloaded_on':'2026-10-08'}
items=[]
for k,wanted in SELECT.items():
 ls=json.loads((ROOT/'pages'/f'{k}-links.json').read_text());sel=[u for u in ls if u.rstrip('/').split('/')[-1] in wanted]
 if len(sel)!=len(wanted):raise ValueError((k,wanted,sel))
 items.extend((k,u) for u in sel)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:out=list(pool.map(one,items))
(ROOT/'source-manifest.json').write_text(json.dumps({'version':1,'selected_resources':out,'selection_frozen':False},ensure_ascii=False,indent=2)+'\n')
for x in out:print(x['id'],x['pages'],x['rights_flags'])
