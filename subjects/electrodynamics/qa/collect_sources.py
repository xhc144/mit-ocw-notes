#!/usr/bin/env python3
"""Fetch actual OCW resource PDFs, preserve metadata, and quarantine before rights review."""
import urllib.request, urllib.parse, re, json, hashlib, html, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import fitz
ROOT=Path(__file__).resolve().parents[3]
CACHE=Path('/tmp/electrodynamics-candidates'); CACHE.mkdir(exist_ok=True)
BASE='https://ocw.mit.edu'
COURSES=[('8-07-fall-2012','8-07-electromagnetism-ii-fall-2012','Fall 2012',['Alan Guth','Min Chen']),('8-311-spring-2004','8-311-electromagnetic-theory-spring-2004','Spring 2004',['Robert L. Jaffe'])]
def get(u):
 with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'MIT-OCW-archive/1.0'}),timeout=45) as r:
  assert urllib.parse.urlparse(r.url).hostname=='ocw.mit.edu'
  return r.read(),r.url,r.headers.get('Content-Type')
def clean(s): return html.unescape(re.sub('<[^>]+>',' ',s)).strip()
entries=[]; pages=[]
for cid,slug,term,authors in COURSES:
 for sec in ['','pages/syllabus/','pages/calendar/','pages/lecture-notes/','pages/assignments/','pages/exams/']:
  u=f'{BASE}/courses/{slug}/{sec}'
  try: b,fu,ct=get(u)
  except Exception as e: pages.append({'course_id':cid,'url':u,'status':'unavailable','reason':str(e)}); continue
  s=b.decode(); (CACHE/f'{cid}-{sec.replace("/","_") or "home"}.html').write_bytes(b)
  main=s[s.find('course-content-section'):]; main=main[:main.find('</main>')]
  pages.append({'course_id':cid,'url':u,'title':clean(re.search(r'<title>(.*?)</title>',s,re.S)[1]),'text':clean(main),'status':'retrieved','sha256':hashlib.sha256(b).hexdigest()})
  for href,title in re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>',main,re.S):
   if '/resources/' not in href: continue
   ru=urllib.parse.urljoin(BASE,href)
   if any(e['resource_url']==ru for e in entries): continue
   author=authors
   if cid=='8-07-fall-2012':
    m=re.search(r'_ln(\d+)/',ru)
    if m: author=['Min Chen'] if int(m[1]) in [12,17] else ['Hongsheng Chen','Min Chen'] if int(m[1])==13 else ['Alan Guth']
   entries.append({'id':ru.rstrip('/').split('/')[-1],'course_id':cid,'course_url':f'{BASE}/courses/{slug}/','semester':term,'title':clean(title),'authors':author,'index_url':u,'resource_url':ru,'kind':sec.split('/')[-2] if sec else 'home','license_default':'CC BY-NC-SA 4.0, except identified third-party material','license_url':'https://ocw.mit.edu/pages/privacy-and-terms-of-use/'})
def fetch(e):
 b,fu,ct=get(e['resource_url']); s=b.decode()
 urls=re.findall(r'(?:href|content)="([^"]+\.pdf(?:\?[^"]*)?)"',s)
 if not urls: return {**e,'status':'no-pdf-link'}
 u=urllib.parse.urljoin(BASE,html.unescape(urls[0])); b,fu,ct=get(u)
 assert b.startswith(b'%PDF-'),u
 p=CACHE/(e['id']+'.pdf'); p.write_bytes(b)
 d=fitz.open(p); assert not d.is_encrypted and len(d)>0
 txt='\n'.join(f'=== PDF page {i+1} ===\n'+page.get_text() for i,page in enumerate(d))
 (CACHE/(e['id']+'.txt')).write_text(txt)
 return {**e,'url':u,'final_url':fu,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'pages':len(d),'pdf_valid':True,'status':'quarantined-for-rights-review','local_candidate':str(p),'exception_markers':[x for x in txt.splitlines() if re.search(r'excluded|permission|copyright|all rights|©|Griffiths|Jackson',x,re.I)]}
with ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(fetch,entries))
(CACHE/'collection.json').write_text(json.dumps({'courses':COURSES,'pages':pages,'files':results},ensure_ascii=False,indent=2)+'\n')
for e in results: print(e['course_id'],e['id'],e.get('pages'),e.get('bytes'),e['title'],e.get('exception_markers',[]))
print('actual_pdf_count',sum(e.get('pdf_valid',False) for e in results))
