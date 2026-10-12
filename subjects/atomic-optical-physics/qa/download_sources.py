import requests, pathlib, bs4, json, concurrent.futures, urllib.parse, xml.etree.ElementTree as ET,hashlib,re
BASE=pathlib.Path('/workspace/mit-ocw-notes/subjects')
COURSES=[('atomic-optical-physics','8-421-atomic-and-optical-physics-i-spring-2014'),('atomic-optical-physics','8-422-atomic-and-optical-physics-ii-spring-2013'),('atomic-optical-physics','6-974-fundamentals-of-photonics-quantum-electronics-spring-2006'),('atomic-optical-physics','6-453-quantum-optical-communication-fall-2016'),('quantum-information','mas-865j-quantum-information-science-spring-2006'),('quantum-information','18-435j-quantum-computation-fall-2003')]
def fetch(u):
 r=requests.get(u,timeout=45);r.raise_for_status();return r
jobs=[]
for sub,slug in COURSES:
 root=BASE/sub/'sources'/slug;root.mkdir(parents=True,exist_ok=True)
 u='https://ocw.mit.edu/courses/'+slug+'/'
 sf=root/'sitemap.xml.xml'
 if not sf.exists():sf.write_bytes(fetch(u+'sitemap.xml').content)
 for e in ET.fromstring(sf.read_bytes()).iter():
  if e.tag.endswith('loc') and '/resources/' in e.text:jobs.append((sub,slug,e.text))
def one(j):
 sub,slug,u=j;root=BASE/sub/'sources'/slug
 try:
  r=fetch(u);s=bs4.BeautifulSoup(r.text,'html.parser');main=s.find('main') or s
  links={urllib.parse.urljoin(u,a['href']) for a in s.find_all('a',href=True) if re.search(r'\.(pdf|txt|srt)(\?|$)',a['href'],re.I)}
  title=s.title.get_text(' ',strip=True) if s.title else u
  fs=[]
  for link in sorted(links):
   name=urllib.parse.unquote(link.split('/')[-1]);f=root/name
   if not f.exists():f.write_bytes(fetch(link).content)
   info={'url':link,'local':str(f.relative_to(BASE/sub)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size}
   if f.suffix=='.pdf':
    import fitz
    doc=fitz.open(f);info['pages']=len(doc);f.with_suffix('.extracted.txt').write_text('\n\n'.join(p.get_text() for p in doc))
   fs.append(info)
  return {'course':slug,'resource_page':u,'title':title,'files':fs,'status':'retrieved'}
 except Exception as e:return {'course':slug,'resource_page':u,'status':'failed','error':str(e)}
rs=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 for i,r in enumerate(ex.map(one,jobs)):
  rs.append(r)
  if i%30==0:print('resources',i+1,'/',len(jobs),flush=True)
for sub in ['atomic-optical-physics','quantum-information']:
 out=[r for r in rs if any(r['course']==slug and sub==s for s,slug in COURSES)]
 (BASE/sub/'sources'/'retrieval-manifest.json').write_text(json.dumps({'retrieved_on':'2026-10-12','default_license':'CC BY-NC-SA 4.0; per-item exceptions require review','resources':out},ensure_ascii=False,indent=2))
 print(sub,len(out),sum(len(r.get('files',[])) for r in out),'files',flush=True)
