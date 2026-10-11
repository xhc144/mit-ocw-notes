#!/usr/bin/env python3
"""Freeze selected official OCW resource URLs, then verify PDFs locally.
Original downloads are quarantined until object-specific rights review.
"""
import urllib.request,re,html,json,pathlib,hashlib,concurrent.futures,fitz
ROOT=pathlib.Path(__file__).resolve().parents[3]
OUT=ROOT/'sources/thermal-statistical-physics'
MAN=ROOT/'manifests/thermal-statistical-physics-sources.json'
BASE='https://ocw.mit.edu'
COURSES={
'8.044':{'slug':'8-044-statistical-physics-i-spring-2013','instructor':'Thomas Greytak','term':'Spring 2013','level':'Undergraduate','selected':'All 22 current-course lectures, all 11 current-course problem sets and solutions, two practice exams and three 2013 exams and solutions. Historical 2003/2004 exam bank is not selected.'},
'8.333':{'slug':'8-333-statistical-mechanics-i-statistical-mechanics-of-particles-fall-2013','instructor':'Mehran Kardar','term':'Fall 2013','level':'Graduate','selected':'Lecture notes 15–22 (cumulant/cluster/virial expansion, condensation, critical point, density matrix, quantum ensembles) and complete problem set 5. Other lectures, problem sets and review-exam banks are not selected.'}}
def get(url):return urllib.request.urlopen(url,timeout=60).read()
def sha(b):return hashlib.sha256(b).hexdigest()
def txt(d):
 s=re.sub(r'<(script|style)\b.*?</\1>','',d,flags=re.S)
 return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s)))
def discover():
 resources={};pages=[]
 for cid,c in COURSES.items():
  base=BASE+'/courses/'+c['slug']+'/'
  names=['syllabus','calendar','readings-notes-slides','assignments','exams'] if cid=='8.044' else ['syllabus','calendar','lecture-notes','assignments','exams']
  for name in names:
   u=base+'pages/'+name+'/';raw=get(u);d=raw.decode()
   path=OUT/'pages'/f'{cid}-{name}.html';path.write_bytes(raw)
   path.with_suffix('.txt').write_text(txt(d),encoding='utf8')
   pages.append({'course':cid,'url':u,'path':str(path.relative_to(ROOT)),'sha256':sha(raw)})
   if name in ['syllabus','calendar'] or (cid=='8.333' and name=='exams'):continue
   for a in re.findall(r'<a\b.*?</a>',d,re.S):
    m=re.search(r'href="([^"]+/resources/[^"]+)"',a)
    if not m:continue
    u=BASE+m.group(1);rid=u.rstrip('/').split('/')[-1];title=txt(a).strip()
    if cid=='8.044' and not rid.startswith('mit8_044s13_'):continue
    if cid=='8.333' and rid not in [f'lecture-{i}' for i in range(15,23)]+['problem-set-5']:continue
    if u in resources:continue
    rd=get(u);rh=rd.decode();pdfs=re.findall(r'(?:href|data-href)="([^"]+\.pdf)"',rh)
    pdfs=list(dict.fromkeys(pdfs))
    if not pdfs:raise RuntimeError('No PDF: '+u)
    pu=pdfs[0];pu=pu if pu.startswith('http') else BASE+pu
    (OUT/'pages'/f'{cid}-{rid}.html').write_bytes(rd)
    resources[u]={'id':rid,'course':cid,'title':title,'resource_url':u,'pdf_url':pu,'selection_status':'frozen','rights_status':'pending_object_review'}
 manifest={'schema_version':1,'frozen_on':'2026-10-11','subject':'thermal-statistical-physics','repository':'xhc144/mit-ocw-notes','courses':COURSES,'pages':pages,'resources':list(resources.values()),'license':'CC BY-NC-SA 4.0 unless specifically marked otherwise; object-specific review before redistribution','scope_status':'frozen_before_pdf_download','historical_assessments_selected':False}
 MAN.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 print('FROZEN',len(resources),'PDF resources')
def download():
 m=json.loads(MAN.read_text());q=pathlib.Path('/tmp/thermal-source-quarantine');q.mkdir(exist_ok=True)
 def one(r):
  b=get(r['pdf_url']);p=q/(r['course']+'-'+r['id']+'.pdf');p.write_bytes(b)
  if not b.startswith(b'%PDF'):raise RuntimeError('not PDF '+r['id'])
  d=fitz.open(p);t='\n'.join(f'\n=== PDF PAGE {i+1} ===\n'+page.get_text() for i,page in enumerate(d))
  p.with_suffix('.txt').write_text(t)
  return {**r,'download_sha256':sha(b),'bytes':len(b),'pdf_pages':len(d),'quarantine_path':str(p),'rights_markers':[(i+1,re.findall(r'.{0,60}(?:rights reserved|copyright|courtesy|©).{0,80}',page.get_text(),re.I)) for i,page in enumerate(d) if re.search(r'rights reserved|copyright|courtesy|©',page.get_text(),re.I)]}
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:m['resources']=list(ex.map(one,m['resources']))
 m['download_verification']='All selected bytes are valid, parseable PDFs; per-file SHA256 recorded. Redistribution pending object review.'
 MAN.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
 print('DOWNLOADED',len(m['resources']),'files',sum(r['pdf_pages'] for r in m['resources']),'pages')
if __name__=='__main__':
 import sys
 {'freeze':discover,'download':download}[sys.argv[1]]()
