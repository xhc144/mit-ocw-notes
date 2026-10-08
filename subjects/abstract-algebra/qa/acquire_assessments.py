from pathlib import Path
import urllib.request,re,html,json,hashlib,fitz
root=Path(__file__).resolve().parents[3];out=root/'sources/abstract-algebra'
def get(u,p):
 d=urllib.request.urlopen(u,timeout=90).read();p.write_bytes(d);return d
def links(b):return [(html.unescape(u),html.unescape(re.sub('<[^>]+>','',t))) for u,t in re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>',b.decode(),re.S)]
records=[]
for kind,n in [('assignments',11),('exams',3)]:
 u=f'https://ocw.mit.edu/courses/18-703-modern-algebra-spring-2013/pages/{kind}/';b=get(u,out/'html'/f'{kind}.html');ls=[]
 for href,title in links(b):
  if '/resources/' in href and href not in [a[0] for a in ls]:ls.append((href,title))
 assert len(ls)==n,(kind,len(ls))
 for i,(href,title) in enumerate(ls,1):
  res='https://ocw.mit.edu'+href if href.startswith('/') else href;key=('hw' if kind=='assignments' else 'practice')+f'{i:02}'
  b=get(res,out/'html'/f'{key}.html');url=[u for u,t in links(b) if u.endswith('.pdf')][0];url='https://ocw.mit.edu'+url if url.startswith('/') else url
  p=out/'pdf'/f'{key}.pdf';d=get(url,p);doc=fitz.open(p);s='\n\f\n'.join(pg.get_text() for pg in doc);(out/'text'/f'{key}.txt').write_text(s)
  records.append(dict(id=key,title=title,course='18.703 Spring 2013',resource_url=res,url=url,path=str(p.relative_to(root)),pages=len(doc),bytes=len(d),sha256=hashlib.sha256(d).hexdigest(),official_solutions=False))
  print(key,len(doc),s[:100].replace('\n',' '),flush=True)
(out/'assessment-manifest.json').write_text(json.dumps({'access_date':'2026-10-08','files':records,'official_solutions':'None linked on assignments or exams pages; exams are practice only'},ensure_ascii=False,indent=2))
