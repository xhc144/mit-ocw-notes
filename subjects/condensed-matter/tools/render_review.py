#!/usr/bin/env python3
"""Render every physical page. Inspection flags are set only after human/model viewing."""
import argparse,hashlib,json,re,pathlib
import fitz
from PIL import Image,ImageDraw
root=pathlib.Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
pdf=root/'build/main.pdf';d=fitz.open(pdf);names=d.resolve_names();links=[];bad=[];pages=[]
for i,p in enumerate(d):
 for l in p.get_links():
  if l['kind'] in (fitz.LINK_GOTO,fitz.LINK_NAMED):
   page=l.get('page',names.get(l.get('nameddest',''),{}).get('page',-1));links.append({'from':i+1,'target':page+1,'name':l.get('nameddest')})
   if not 0<=page<len(d):bad.append(links[-1])
 q=a.out/f'page-{i+1:03d}.png';p.get_pixmap(matrix=fitz.Matrix(1.45,1.45),alpha=False).save(q)
 pages.append({'physical_page':i+1,'image':str(q),'sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'inspected':False})
for j in range(0,len(d),4):
 ims=[Image.open(a.out/f'page-{i+1:03d}.png') for i in range(j,min(j+4,len(d)))];w,h=ims[0].size
 sheet=Image.new('RGB',(2*w,2*(h+22)),(218,218,218));dr=ImageDraw.Draw(sheet)
 for k,im in enumerate(ims):x=k%2*w;y=k//2*(h+22);dr.text((x+10,y+4),f'physical page {j+k+1}',fill='black');sheet.paste(im,(x,y+22))
 sheet.save(a.out/f'sheet-{j//4+1:02d}.png')
s=(root/'main.tex').read_text();locked=re.search(r'% WZ-LOCKED-CLASS-BEGIN.*?% WZ-LOCKED-CLASS-END',s,re.S).group();prev=(root.parent/'thermal-statistical-physics/main.tex').read_text();gold=re.search(r'% WZ-LOCKED-CLASS-BEGIN.*?% WZ-LOCKED-CLASS-END',prev,re.S).group()
qa={'pages':len(d),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'locked_template_sha256':hashlib.sha256(locked.encode()).hexdigest(),'template_exact_match':locked==gold,'internal_links':len(links),'bad_links':bad,'outlines':len(d.get_toc()),'bad_outlines':[x for x in d.get_toc() if not 1<=x[2]<=len(d)],'named_destinations':len(names),'rendered_pages':pages,'inspection_method':'Four-page contact sheets at 1.45 pixels per PDF point; original detail; flags await viewing.'}
(root/'qa/render-and-links.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n');print({k:v for k,v in qa.items() if k!='rendered_pages'})
