#!/usr/bin/env python3
"""Render every real PDF page and bind the result; viewing is a separate action."""
from __future__ import annotations
import os
from pathlib import Path
import tempfile
from build_utils import sha256, write_json

def render_pdf(pdf: Path,root: Path|None=None,dpi: int=130) -> Path:
    import fitz
    from PIL import Image, ImageDraw
    pdf=pdf.resolve(); root=(root or pdf.parent).resolve()
    if not pdf.is_file(): raise ValueError('Missing PDF')
    if not 72<=dpi<=300: raise ValueError('Render DPI must be between 72 and 300')
    before=sha256(pdf); qa=pdf.parent/'.qa'; qa.mkdir(exist_ok=True)
    dest=Path(tempfile.mkdtemp(prefix=pdf.stem+'-',dir=qa)); pages=[]; contacts=[]
    def rel(p): return os.path.relpath(p,root).replace(os.sep,'/')
    with fitz.open(pdf) as doc:
        if doc.needs_pass or len(doc)==0: raise ValueError('Encrypted or empty PDF')
        thumbnails=[]
        for i,page in enumerate(doc,1):
            path=dest/f'page-{i:04d}.png'
            pix=page.get_pixmap(dpi=dpi,alpha=False); pix.save(path)
            pages.append({'page':i,'path':rel(path),'sha256':sha256(path)})
            with Image.open(path) as im:
                thumb=im.convert('RGB'); thumb.thumbnail((340,460)); thumbnails.append((i,thumb.copy()))
            if len(thumbnails)==12 or i==len(doc):
                cols=min(3,len(thumbnails)); rows=(len(thumbnails)+cols-1)//cols
                sheet=Image.new('RGB',(cols*360,rows*500),'white'); draw=ImageDraw.Draw(sheet)
                for j,(n,image) in enumerate(thumbnails):
                    x=(j%cols)*360+10; y=(j//cols)*500+25
                    sheet.paste(image,(x,y)); draw.text((x,y-18),f'Page {n}',fill='black')
                contact=dest/f'contact-{len(contacts)+1:03d}.png'; sheet.save(contact)
                contacts.append(rel(contact)); thumbnails=[]
        count=len(doc)
    if sha256(pdf)!=before: raise ValueError('PDF changed while rendering')
    record={'schema_version':1,'pdf':{'path':rel(pdf),'sha256':before},'page_count':count,'dpi':dpi,
            'inspected':False,'pages':pages,'contacts':contacts,
            'limitation':'Rendered files exist; no claim that any page has been visually inspected.'}
    target=pdf.with_suffix('.render.json'); write_json(target,record); return target
