"""Freeze MIT OCW assessments; linked notebooks are for local review only, not redistribution."""
import hashlib,json,subprocess,urllib.request
from pathlib import Path
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[3]
DEST=ROOT/'sources/18.335j-spring-2019/assessments'
DEST.mkdir(parents=True,exist_ok=True)
BASE='https://ocw.mit.edu'
rows=[]
def fetch(url):
 with urllib.request.urlopen(url,timeout=45) as r:return r.read()
def resource(pair):
 title,rel=pair;url=urljoin(BASE,rel);slug=rel.rstrip('/').split('/')[-1]
 raw=fetch(url);s=BeautifulSoup(raw,'html.parser')
 pdfs=list(dict.fromkeys(urljoin(BASE,a['href']) for a in s.find_all('a',href=True) if a['href'].split('?')[0].endswith('.pdf')))
 if len(pdfs)!=1:raise ValueError((slug,pdfs))
 data=fetch(pdfs[0]);path=DEST/(slug+'.pdf');path.write_bytes(data)
 subprocess.run(['pdftotext','-layout',str(path),str(path.with_suffix('.txt'))],check=True)
 year=slug.split('exam')[-1].replace('sol','') if 'exam' in slug else '19'
 term=(('Spring ' if year in ['15','19'] else 'Fall ')+'20'+year) if 'exam' in slug else 'Spring 2019'
 info=subprocess.run(['pdfinfo',str(path)],check=True,capture_output=True,text=True).stdout
 pages=int(next(line.split(':')[1].strip() for line in info.splitlines() if line.startswith('Pages:')))
 return {'id':slug,'title':title,'resource_url':url,'source_url':pdfs[0],'local_path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'pages':pages,'original_term':term,'license':'MIT OCW CC BY-NC-SA 4.0; retain original notices','rights_review':'preserve original MIT footer; no excluded third-party notice found in extracted text; source-specific review required','public_upload_status':'eligible_authorized_public_noncommercial_CC_BY_NC_SA_4_0_preserve_notices','retrieved_at_utc':'2026-10-08'}
pairs=[]
for n in ['resource-index','week-9']:
 s=BeautifulSoup((ROOT/'sources/18.335j-spring-2019/html'/f'{n}.html').read_text(),'html.parser')
 for a in s.find_all('a',href=True):
  href=a['href']
  if '/resources/mit18_335js19_' in href and ('pset' in href or 'exam' in href):pairs.append((a.get_text(' ',strip=True),href))
pairs=list({rel:(title,rel) for title,rel in pairs}.values())
with ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(resource,pairs))
for name in ['pset1','pset1sol']:
 url=f'https://raw.githubusercontent.com/mitmath/18335/spring19/psets/{name}.ipynb';data=fetch(url);path=DEST/(name+'.ipynb');path.write_bytes(data)
 rows.append({'id':name+'-notebook','source_url':url,'local_path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'license':'External course repository without root license: original notebook link only', 'public_upload_status':'hold_link_only','retrieved_at_utc':'2026-10-08'})
(DEST/'.gitignore').write_text('pset1.ipynb\npset1sol.ipynb\n')
(DEST/'source-manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print(json.dumps([{'id':r['id'],'bytes':r['bytes']} for r in rows],indent=2))
