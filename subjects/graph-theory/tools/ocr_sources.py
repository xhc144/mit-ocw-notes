import os,fitz,subprocess,concurrent.futures,re,json
from pathlib import Path
r=Path('/workspace/mit-ocw-notes/sources/graph-theory');temp=Path('/tmp/graph-source-review');temp.mkdir(exist_ok=True)
manifest=json.loads((r/'source-manifest.json').read_text());jobs=[]
if manifest.get('selection_frozen'):
 raise SystemExit('Source selection is frozen; OCR cannot silently rewrite reviewed source metadata.')
for x in manifest['selected_resources']:
 if x['course'] in ['18315','18433']:
  d=fitz.open(r/x['path'])
  for i,p in enumerate(d):
   dest=temp/f'{x["id"]}-p{i+1:02d}.png';p.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(dest);jobs.append((x['id'],i,dest))
def ocr(job):
 k,i,p=job;res=subprocess.run(['tesseract',str(p),'stdout','--psm','6'],capture_output=True,text=True,check=True,timeout=60,env={**os.environ,"OMP_THREAD_LIMIT":"1"});return k,i,res.stdout
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:out=list(pool.map(ocr,jobs))
for x in manifest['selected_resources']:
 if x['course'] in ['18315','18433']:
  rows=sorted((i,t) for k,i,t in out if k==x['id']);(r/'text'/f'{x["id"]}.txt').write_text('\n\f\n'.join(t for i,t in rows));x['text_extraction']='Tesseract OCR; scanned manuscript or broken font encoding; mathematical reading uses original images'
  x['rights_flags']=[{'pdf_page':i+1,'text':line} for i,t in rows for line in t.splitlines() if re.search(r'copyright|rights reserved|permission|creative commons|©|courtesy',line,re.I)]
(manifest_path:=r/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('OCR pages',len(jobs)); print('Rights hits',[(x['id'],x['rights_flags']) for x in manifest['selected_resources'] if x['rights_flags'] and x['course'] in ['18315','18433']])
