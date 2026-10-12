from pathlib import Path
import fitz,subprocess,concurrent.futures,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'qa/ocr/theory-revision';OUT.mkdir(parents=True,exist_ok=True)
ps=list((ROOT/'sources').rglob('*lecture*.pdf'))+list((ROOT/'sources').rglob('*qc_lec*.pdf'))
def one(p):
 target=p.with_suffix('.ocr.txt')
 if target.exists():return {'file':p.name,'status':'existing'}
 d=fitz.open(p);pieces=[]
 for i,pg in enumerate(d):
  img=OUT/(p.stem+f'-{i+1:02}.png');pg.get_pixmap(matrix=fitz.Matrix(2.2,2.2)).save(img)
  z=subprocess.run(['tesseract',str(img),'stdout','-l','eng','--psm','3'],capture_output=True,text=True,check=True);pieces.append(f'\nSOURCE PAGE {i+1}\n'+z.stdout)
 target.write_text(''.join(pieces));print('OCR',p.name,len(d),'pages',flush=True);return {'file':p.name,'pages':len(d),'status':'ocr produced; formulas still require source visual verification'}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(one,ps))
(OUT/'ocr-jobs.json').write_text(json.dumps(rows,indent=2))
