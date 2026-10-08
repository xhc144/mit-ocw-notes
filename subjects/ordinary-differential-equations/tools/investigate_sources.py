#!/usr/bin/env python3
import urllib.request,re,html,json,hashlib,concurrent.futures
from pathlib import Path
from urllib.parse import urljoin
import fitz
ROOT=Path(__file__).resolve().parents[3]; S=ROOT/'sources/ordinary-differential-equations'; Q=ROOT/'subjects/ordinary-differential-equations/review'; S.mkdir(exist_ok=True); Q.mkdir(exist_ok=True)
HOST='https://ocw.mit.edu'; courses=['18-03-differential-equations-spring-2010','12-006j-nonlinear-dynamics-chaos-fall-2022']
def get(u):
 with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=50) as r:
  if not r.url.startswith(HOST+'/'): raise ValueError('Nonofficial redirect')
  return r.read()
def links(h):
 return [(urljoin(HOST,u),html.unescape(re.sub('<.*?>','',t)).strip()) for u,t in re.findall(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>',h.decode(),re.S)]
res={}
for c in courses:
 for p in (['lecture-notes','readings'] if c==courses[0] else ['lecture-notes']):
  u=f'{HOST}/courses/{c}/pages/{p}/'; h=get(u); (S/(c+'-'+p+'.html')).write_bytes(h)
  for v,t in links(h):
   if '/resources/' in v: res[v]=(c,t,p)
  if p=='readings':
   for v,t in links(h):
    if '18.03 Supplementary Notes' in t or '18.03 Notes and Exercises' in t:
     h2=get(v); (S/('index-'+v.rstrip('/').split('/')[-1]+'.html')).write_bytes(h2)
     for v2,t2 in links(h2):
      if '/resources/' in v2: res[v2]=(c,t2,t)
def one(kv):
 u,(c,t,idx)=kv; h=get(u); slug=u.rstrip('/').split('/')[-1]
 pdfs=list(dict.fromkeys(v for v,l in links(h) if '.pdf' in v and v.startswith(HOST+'/')))
 if not pdfs: return {'resource_url':u,'error':'no pdf'}
 v=pdfs[0]; data=get(v); d=fitz.open(stream=data,filetype='pdf'); text='\n'.join(p.get_text() for p in d)
 title=re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"',h.decode())
 hits=[line.strip() for line in text.splitlines() if re.search(r'copyright|©|courtesy|permission|all rights|not.*creative|excluded|strogatz|pearson|prentice|wiley|norton|houghton|cambridge',line,re.I)]
 folder=S/c; folder.mkdir(exist_ok=True); (folder/(slug+'.txt')).write_text(text)
 (folder/(slug+'.resource.html')).write_bytes(h)
 entry={'id':slug,'course':c,'course_year':2010 if c==courses[0] else 2022,'course_instructors':['Haynes Miller','Arthur Mattuck'] if c==courses[0] else ['Daniel Rothman'],'listed_label':t,'index':idx,'resource_url':u,'url':v,'pages':len(d),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'metadata':d.metadata,'rights_review_lines':hits,'description':html.unescape(title.group(1)) if title else '', 'archive_allowed':False,'license':'MIT OCW default CC BY-NC-SA 4.0; individual rights review pending','temporary_original':'/tmp/ode-source-review/'+slug+'.pdf'}
 tmp=Path(entry['temporary_original']);tmp.parent.mkdir(exist_ok=True);tmp.write_bytes(data)
 return entry
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 entries=list(ex.map(one,res.items()))
(Q/'source-investigation.json').write_text(json.dumps({'checked_on':'2026-10-08','sources':entries},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'files':len(entries),'pages':sum(e.get('pages',0) for e in entries),'rights_flags':[{k:e[k] for k in ['id','pages','rights_review_lines']} for e in entries if e.get('rights_review_lines')]},ensure_ascii=False,indent=2))
