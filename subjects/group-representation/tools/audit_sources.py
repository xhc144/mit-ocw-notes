import urllib.request, pathlib, fitz, hashlib, re, json, html
from concurrent.futures import ThreadPoolExecutor
root=pathlib.Path(__file__).resolve().parents[3]; s=root/'sources/group-representation';qa=root/'subjects/group-representation/qa'
base='https://ocw.mit.edu/courses/18-712-introduction-to-representation-theory-fall-2010/'
def get(url):
 with urllib.request.urlopen(url,timeout=60) as response:
  if not response.url.startswith('https://ocw.mit.edu/'):raise RuntimeError('unexpected redirect')
  return response.read()
for name,url in [('lecture-notes',base+'pages/lecture-notes/'),('syllabus',base+'pages/syllabus/'),('terms','https://ocw.mit.edu/pages/privacy-and-terms-of-use/')]:
 (s/'html'/f'{name}.html').write_bytes(get(url))
page=(s/'html/lecture-notes.html').read_text();links=[]
for href,txt in re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>',page,re.S):
 if 'PDF' in txt and href.startswith('/courses/'):
  u='https://ocw.mit.edu'+html.unescape(href); resource=get(u).decode(); pdfs=re.findall(r'href="([^"?]+\.pdf)"',resource)
  if pdfs:
   p=pdfs[0]; links.append({'resource_page':u,'pdf_url':'https://ocw.mit.edu'+p if p.startswith('/') else p})
old=base+'24d8b3fa2ce48e48ee6c2d8d5e3562f6_MIT18_712F10_replect.pdf'
if not any(x['pdf_url']==old for x in links): links.insert(0,{'resource_page':base+'pages/lecture-notes/','pdf_url':old})
(qa/'duplicate-audit').mkdir(exist_ok=True)
def download(x):
 data=get(x['pdf_url']);d=fitz.open(stream=data,filetype='pdf');name=x['pdf_url'].rsplit('/',1)[1]
 text='\n'.join(p.get_text() for p in d);x.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),pages=len(d),filename=name,rights_lines=[line for line in text.splitlines() if re.search(r'copyright|license|permission|reserved|©|creativecommons|terms of use',line,re.I)])
 if x['pdf_url']==old:
  (s/'pdf'/name).write_bytes(data);(s/'text/old-lecture-notes.txt').write_text(text);x['archive_path']=f'sources/group-representation/pdf/{name}'
 else:
  (qa/'duplicate-audit'/name).write_bytes(data);x['status']='duplicate audit only, not archived in release'
 return x
with ThreadPoolExecutor(max_workers=4) as pool:audit=list(pool.map(download,links))
(s/'source-audit-draft.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
print(json.dumps(audit,ensure_ascii=False,indent=2))
