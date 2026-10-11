#!/usr/bin/env python3
"""Freeze and collect a precisely selected OCW course layer, never whole-course ZIPs."""
import concurrent.futures,hashlib,json,pathlib,re,urllib.request,urllib.parse
from html.parser import HTMLParser
import fitz
ROOT=pathlib.Path(__file__).resolve().parents[3]
DEST=ROOT/'sources/introductory-electromagnetism'
MF=ROOT/'manifests/introductory-electromagnetism-sources.json'
SLUG='8-02-physics-ii-electricity-and-magnetism-spring-2007'
BASE='https://ocw.mit.edu'
COURSE=BASE+'/courses/'+SLUG+'/'
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.a=None;self.links=[];self.parts=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
  if t=='a':self.a=[dict(a).get('href',''),'']
  if t in ('p','tr','li','h1','h2','h3'):self.parts.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
  if t=='a' and self.a:self.links.append(self.a);self.a=None
 def handle_data(self,d):
  if self.a:self.a[1]+=d
  if not self.skip:self.parts.append(d)
def get(url):
 if urllib.parse.urlparse(url).hostname!='ocw.mit.edu':raise ValueError('Non OCW hostname')
 with urllib.request.urlopen(url,timeout=45) as r:
  if urllib.parse.urlparse(r.url).hostname!='ocw.mit.edu':raise ValueError('External redirect')
  return r.read(),r.url
def parse(url):
 b,u=get(url);p=Parser();p.feed(b.decode());return p,b
def sha(b):return hashlib.sha256(b).hexdigest()
pages=[];resources=[]
for section in ['syllabus','class-topics','readings','problem-solving']:
 url=COURSE+'pages/'+section+'/'
 p,b=parse(url);out=DEST/'metadata'/f'{section}.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b)
 out.with_suffix('.txt').write_text(re.sub(r'\n\s*\n+','\n\n',''.join(p.parts)))
 pages.append(dict(url=url,path=str(out.relative_to(ROOT)),sha256=sha(b)))
 for href,title in p.links:
  ident=href.rstrip('/').split('/')[-1]
  if '/resources/' not in href or not re.fullmatch(r'summary_w\d+d\d|solving\d+',ident):continue
  if any(x['id']==ident for x in resources):continue
  resources.append(dict(id=ident,kind='lecture-summary' if ident.startswith('summary') else 'friday-problem-solving',resource_url=urllib.parse.urljoin(BASE,href),status='frozen_selected'))
manifest=dict(schema_version=1,subject='introductory-electromagnetism',frozen_on='2026-10-11',selection='All 36 session summaries and all 11 Friday problem-solving PDFs linked on the selected 8.02 Spring 2007 pages. Textbook chapters, Monday/Wednesday group worksheets, slides, experiments and MasteringPhysics are not selected or downloaded in this batch.',courses=[dict(code='8.02',title='Physics II: Electricity and Magnetism',term='Spring 2007',url=COURSE,instructors=['Physics Department Faculty, Lecturers, and Technical Staff'],material_authors=['Peter Dourmashkin','Eric Hudson','Sen-Ben Liao'],role='main')],prerequisites=['8.01 classical mechanics','single-variable calculus; elementary vectors, introduced locally'],onward_course=dict(code='8.022',term='Fall 2004',instructor='Gabriella Sciolla',url=BASE+'/courses/8-022-physics-ii-electricity-and-magnetism-fall-2004/',role='metadata reviewed; no PDF selected; deeper first-year alternative'),missing_assessments='8.02 syllabus explicitly states that weekly written homework is not available to OCW users. Exam summaries are information/review, not obtained exam questions.',pages=pages,resources=resources)
MF.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(DEST/'selection-frozen.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('FROZEN',len(resources),flush=True)
def download(item):
 p,b=parse(item['resource_url']);urls=list(dict.fromkeys(urllib.parse.urljoin(BASE,h) for h,t in p.links if urllib.parse.urlparse(h).path.endswith('.pdf')))
 if len(urls)!=1:raise ValueError((item['id'],urls))
 data,final=get(urls[0])
 if not data.startswith(b'%PDF-'):raise ValueError('PDF magic')
 doc=fitz.open(stream=data,filetype='pdf');txt='\n'.join(p.get_text() for p in doc)
 if not len(doc) or doc.is_encrypted:raise ValueError('Empty/encrypted PDF')
 out=DEST/'8.02-spring2007'/f"{item['id']}.pdf";out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data);out.with_suffix('.txt').write_text(txt)
 item.update(url=urls[0],final_url=final,path=str(out.relative_to(ROOT)),text_path=str(out.with_suffix('.txt').relative_to(ROOT)),sha256=sha(data),bytes=len(data),pages=len(doc),status='downloaded_verified',license='CC BY-NC-SA 4.0 unless an object bears an explicit exception',attribution='MIT OpenCourseWare; MIT 8.02 course staff; Peter Dourmashkin, Eric Hudson, Sen-Ben Liao',rights_review='pending',archive_allowed=False)
 return item
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:manifest['resources']=list(ex.map(download,resources))
MF.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('VERIFIED',len(resources),'PDFs',sum(x['pages'] for x in resources),'pages')
