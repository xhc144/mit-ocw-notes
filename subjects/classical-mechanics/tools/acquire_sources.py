#!/usr/bin/env python3
"""Fetch actual OCW resources, validate bytes and record immutable provenance."""
import urllib.request,urllib.parse,concurrent.futures,hashlib,json,re
from pathlib import Path
from html.parser import HTMLParser
import fitz
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'sources/classical-mechanics'
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.text=[]
 def handle_starttag(self,t,a):
  if t=='a':self.links.append(dict(a).get('href',''))
 def handle_data(self,d):self.text.append(d)
def fetch(u):
 with urllib.request.urlopen(u,timeout=60) as r:return r.read(),r.headers.get('Content-Type','')
def resource(item):
 slug,kind,u=item
 data,_=fetch(u);html=data.decode();p=Links();p.feed(html)
 target=BASE/slug/'resource-pages';target.mkdir(parents=True,exist_ok=True);rid=u.rstrip('/').split('/')[-1];(target/(rid+'.html')).write_bytes(data)
 title=re.search(r'<title>(.*?)</title>',html,re.S).group(1).split(' | ')[0]
 files=list(dict.fromkeys(urllib.parse.urljoin(u,x) for x in p.links if re.search(r'\.(pdf|nb)$',x,re.I)))
 out=[]
 for url in files:
  name=url.split('/')[-1];content,ctype=fetch(url);dest=BASE/slug/('pdf' if name.lower().endswith('.pdf') else 'notebooks')/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(content)
  entry={'course':slug,'kind':kind,'title':title,'resource_url':u,'url':url,'path':str(dest.relative_to(ROOT)),'bytes':len(content),'sha256':hashlib.sha256(content).hexdigest(),'content_type':ctype,'semester':'Fall 2014' if slug.startswith('8-09') else 'January IAP 2017','instructor':'Iain Stewart' if slug.startswith('8-09') else 'Matthew Evans','author':'Iain Stewart' if slug.startswith('8-09') else ('Students who took the course; individual authors to be checked in each PDF' if kind=='lecture-notes' else 'MIT 8.223 course staff; individual author not stated on OCW resource page'),'license':'CC BY-NC-SA 4.0 unless otherwise indicated; per-file inspection required','license_url':'https://ocw.mit.edu/pages/privacy-and-terms-of-use/','third_party_review':'pending','redistribute':False}
  if name.lower().endswith('.pdf'):
   assert content.startswith(b'%PDF-'),url
   doc=fitz.open(stream=content,filetype='pdf');assert not doc.is_encrypted
   entry['pages']=len(doc);entry['pdf_validated']=True
   text='\n'.join(x.get_text() for x in doc);(dest.with_suffix('.txt')).write_text(text)
   entry['pdf_metadata']=doc.metadata
  out.append(entry)
 return out
if __name__=='__main__':
 jobs=[]
 for directory in BASE.iterdir():
  if not directory.is_dir():continue
  for kind in ['lecture-notes','assignments','projects']:
   page=directory/'context'/f'{kind}.html'
   if not page.exists():continue
   p=Links();p.feed(page.read_text())
   jobs.extend((directory.name,kind,urllib.parse.urljoin('https://ocw.mit.edu',u)) for u in dict.fromkeys(p.links) if '/resources/' in u)
 entries=[]
 with concurrent.futures.ThreadPoolExecutor(4) as pool:
  for result in pool.map(resource,jobs):entries.extend(result)
 manifest={'schema_version':1,'retrieved_at':'2026-10-11','courses':[{'id':s,'url':f'https://ocw.mit.edu/courses/{s}/'} for s in sorted(set(x['course'] for x in entries))],'resources':entries,'note':'Actual files fetched; redistribution requires completion of third-party review.'}
 (ROOT/'manifests/classical-mechanics-sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'files':len(entries),'pdfs':sum('pages'in x for x in entries),'pages':sum(x.get('pages',0) for x in entries)},ensure_ascii=False))
