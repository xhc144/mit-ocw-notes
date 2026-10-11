#!/usr/bin/env python3
"""Download only actual OCW PDF links discovered from the three frozen course pages.
No course ZIP, embedded media, commercial textbook, or external-host download.
"""
import concurrent.futures,hashlib,json,re,pathlib,urllib.request,urllib.parse
from html.parser import HTMLParser
import fitz
ROOT=pathlib.Path(__file__).resolve().parents[3]
BASE='https://ocw.mit.edu'
COURSES=[('8.04','8-04-quantum-physics-i-spring-2016','Spring 2016'),('8.05','8-05-quantum-physics-ii-fall-2013','Fall 2013'),('8.06','8-06-quantum-physics-iii-spring-2018','Spring 2018')]
class Parser(HTMLParser):
 def __init__(self): super().__init__();self.links=[];self.a=None;self.skip=0;self.text=[]
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
  if t=='a':self.a=[dict(a).get('href',''),'']
  if t in ['p','div','tr','li','h1','h2','h3','h4']:self.text.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
  if t=='a' and self.a:self.links.append(self.a);self.a=None
 def handle_data(self,d):
  if self.a:self.a[1]+=d
  if not self.skip:self.text.append(d)
def get(u):
 if urllib.parse.urlparse(u).hostname!='ocw.mit.edu':raise ValueError('non-OCW URL')
 with urllib.request.urlopen(u,timeout=60) as r:
  if urllib.parse.urlparse(r.url).hostname!='ocw.mit.edu':raise ValueError('non-OCW redirect')
  return r.read(),r.url,r.headers.get('Content-Type')
def parsed(u):
 b,final,typ=get(u);p=Parser();p.feed(b.decode());return p,b
items=[];pages=[]
for code,slug,term in COURSES:
 folder=ROOT/'sources/quantum-mechanics'/slug;folder.mkdir(parents=True,exist_ok=True)
 for section in ['syllabus','calendar','lecture-notes','assignments','exams']:
  u=f'{BASE}/courses/{slug}/pages/{section}/'
  try:p,b=parsed(u)
  except Exception as e:
   pages.append(dict(course=code,section=section,url=u,status='unavailable',error=str(e)));continue
  path=folder/(section+'.html');path.write_bytes(b)
  tx=folder/(section+'.txt');tx.write_text(re.sub(r'\n\s*\n+', '\n\n',''.join(p.text)),encoding='utf-8')
  pages.append(dict(course=code,section=section,url=u,path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(b).hexdigest(),status='downloaded',title=section))
  for href,title in p.links:
   if '/resources/' not in href:continue
   ru=urllib.parse.urljoin(BASE,href)
   if any(x['resource_page_url']==ru for x in items):continue
   items.append(dict(course=code,course_slug=slug,term=term,instructor='Barton Zwiebach',author='Barton Zwiebach / MIT course staff; document-specific credit requires text review',category=section,title=title.strip(),resource_page_url=ru,course_url=f'{BASE}/courses/{slug}/',license='CC BY-NC-SA 4.0, except identified third-party content',license_url='https://creativecommons.org/licenses/by-nc-sa/4.0/',attribution='MIT OpenCourseWare; Barton Zwiebach and credited course staff',status='discovered'))
def download(it):
 try:
  p,_=parsed(it['resource_page_url'])
  urls=list(dict.fromkeys(urllib.parse.urljoin(BASE,h) for h,t in p.links if urllib.parse.urlparse(h).path.lower().endswith('.pdf')))
  if len(urls)!=1:raise ValueError(f'expected one PDF link, found {len(urls)}')
  u=urls[0];b,final,typ=get(u)
  if not b.startswith(b'%PDF-'):raise ValueError('not PDF magic')
  d=fitz.open(stream=b,filetype='pdf');text='\n'.join(p.get_text() for p in d)
  if d.is_encrypted or not len(d):raise ValueError('encrypted or empty PDF')
  name=pathlib.PurePosixPath(urllib.parse.urlparse(u).path).name
  path=ROOT/'sources/quantum-mechanics'/it['course_slug']/'pdf'/name;path.parent.mkdir(exist_ok=True);path.write_bytes(b)
  txt=path.with_suffix('.txt');txt.write_text(text)
  it.update(url=u,final_url=final,path=str(path.relative_to(ROOT)),text_path=str(txt.relative_to(ROOT)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),pages=len(d),mime=typ,downloaded_on='2026-10-11',status='downloaded_verified',archive_allowed=False,license_review='pending',pdf_verification=dict(magic=True,all_pages_open=True,text_characters=len(text)))
  return it
 except Exception as e:it.update(status='download_failed',error=str(e));return it
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:items=list(pool.map(download,items))
# Deduplicate aliases by actual byte hash, retaining all resource-page provenance.
seen={}
for it in items:
 if it.get('sha256') in seen:it['duplicate_of']=seen[it['sha256']]
 elif it.get('sha256'):seen[it['sha256']]=it['path']
manifest=dict(schema_version=1,subject='quantum-mechanics',retrieved_on='2026-10-11',collection_scope='Official PDF lecture notes, assignments, exams and formula sheets linked from the three selected OCW courses. Course webpage links are metadata, not downloaded PDFs.',courses=[dict(code=c,slug=s,term=t,instructor='Barton Zwiebach',url=f'{BASE}/courses/{s}/') for c,s,t in COURSES],pages=pages,resources=items)
out=ROOT/'manifests/quantum-mechanics-sources.json';out.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(resources=len(items),verified=sum(i['status']=='downloaded_verified' for i in items),unique_pdfs=len(seen),pages=sum(i.get('pages',0) for i in items if 'duplicate_of' not in i),failures=[i for i in items if i['status']!='downloaded_verified']),ensure_ascii=False))
