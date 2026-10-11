#!/usr/bin/env python3
"""Render all pages with hashes; deliberately does not claim human visual approval."""
import argparse,hashlib,json,pathlib
import fitz
from PIL import Image,ImageDraw
ap=argparse.ArgumentParser();ap.add_argument('pdf',type=pathlib.Path);ap.add_argument('--out',type=pathlib.Path,default=pathlib.Path('/tmp/thermal-render'));a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
d=fitz.open(a.pdf);pages=[];contacts=[];batch=[]
for i,p in enumerate(d,1):
 path=a.out/f'page-{i:03d}.png';p.get_pixmap(dpi=130,alpha=False).save(path)
 pages.append({'page':i,'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'width':p.rect.width,'height':p.rect.height})
 im=Image.open(path).convert('RGB');im.thumbnail((1020,1320));batch.append((i,im.copy()))
 if len(batch)==2 or i==len(d):
  sheet=Image.new('RGB',(2080,1370),'white');draw=ImageDraw.Draw(sheet)
  for j,(n,im)in enumerate(batch):sheet.paste(im,(j*1040+10,30));draw.text((j*1040+10,5),f'PDF physical page {n}',fill='black')
  dst=a.out/f'contact-{len(contacts)+1:02d}.png';sheet.save(dst);contacts.append(str(dst));batch=[]
record={'pdf_sha256':hashlib.sha256(a.pdf.read_bytes()).hexdigest(),'pages':len(d),'dpi':130,'page_records':pages,'contacts':contacts,'visual_review':'not performed by renderer'}
(a.out/'render.json').write_text(json.dumps(record,indent=2)+'\n');print(a.out/'render.json')
