#!/usr/bin/env python3
"""Verify build/render bindings against actual files, never reviewer sincerity."""
from __future__ import annotations
import json
from pathlib import Path,PureWindowsPath
import re
from build_utils import sha256

def safe_file(root: Path,relative: object) -> Path:
    if not isinstance(relative,str) or not relative.strip() or '\x00' in relative:
        raise ValueError('Expected a nonempty project-relative path')
    raw=relative.replace('\\','/')
    if Path(raw).is_absolute() or PureWindowsPath(raw).drive: raise ValueError('Absolute/drive paths are not allowed in records')
    p=(root/raw).resolve()
    if not p.is_relative_to(root.resolve()) or not p.is_file() or not p.stat().st_size:
        raise ValueError('Missing, empty, or outside-project file: '+relative)
    return p

def bound(root: Path,entry: object) -> Path:
    if not isinstance(entry,dict): raise ValueError('File binding must be an object')
    p=safe_file(root,entry.get('path'))
    h=entry.get('sha256')
    if not isinstance(h,str) or not re.fullmatch('[0-9a-f]{64}',h) or sha256(p)!=h:
        raise ValueError('Missing/stale SHA-256: '+str(entry.get('path')))
    return p

def read_record(path: Path) -> dict:
    if path.stat().st_size>10_000_000: raise ValueError('Record exceeds 10 MB')
    value=json.loads(path.read_text(encoding='utf-8-sig'))
    if not isinstance(value,dict): raise ValueError('Record must be a JSON object')
    return value

def verify_records(root: Path,build_ref: str|None,render_ref: str|None,
                   require_render: bool=True) -> dict:
    errors=[]; warnings=[]; statuses={'build':'not_provided','render':'not_provided'}; pdf=None; page_count=None
    if build_ref:
        try:
            record=read_record(safe_file(root,build_ref))
            if record.get('status')!='built': raise ValueError('Latest build is not successful')
            pdf=bound(root,record.get('pdf'))
            import fitz
            with fitz.open(pdf) as doc:
                if doc.needs_pass or len(doc)==0: raise ValueError('Unreadable/encrypted/empty PDF')
                page_count=len(doc)
            inputs=record.get('inputs')
            if not isinstance(inputs,list) or not inputs: raise ValueError('No actual build inputs bound')
            paths=[bound(root,x) for x in inputs]
            if len(paths)!=len(set(paths)): raise ValueError('Duplicate build input binding')
            source=record.get('source')
            if source and safe_file(root,source) not in paths: raise ValueError('Main source missing from build inputs')
            statuses['build']='verified'
        except (OSError,ValueError,TypeError,RuntimeError,ImportError) as exc:
            errors.append('build: '+str(exc)); statuses['build']='failed'
    else: warnings.append('No build record: compilation has not been verified.')
    if render_ref:
        try:
            record=read_record(safe_file(root,render_ref)); rendered_pdf=bound(root,record.get('pdf'))
            if pdf is not None and rendered_pdf!=pdf: raise ValueError('Rendered PDF differs from the build PDF')
            import fitz
            with fitz.open(rendered_pdf) as doc:
                if doc.needs_pass or not len(doc): raise ValueError('Unreadable/encrypted/empty rendered PDF')
                actual_count=len(doc)
            if 'page_count' in record and (type(record['page_count']) is not int or record['page_count']!=actual_count):
                raise ValueError('Declared render page count differs from actual PDF')
            pages=record.get('pages')
            if not isinstance(pages,list) or len(pages)!=actual_count:
                raise ValueError(f'Render coverage incomplete: actual PDF has {actual_count} pages')
            numbers=[]; paths=[]
            from PIL import Image
            for item in pages:
                if not isinstance(item,dict) or type(item.get('page')) is not int: raise ValueError('Invalid page record')
                numbers.append(item['page']); image=bound(root,item); paths.append(image)
                with Image.open(image) as im: im.verify()
            if sorted(numbers)!=list(range(1,actual_count+1)): raise ValueError('Missing/duplicate/invalid page numbers')
            if len(paths)!=len(set(paths)): raise ValueError('Same rendered file reused for multiple pages')
            statuses['render']='verified_files_only'
        except (OSError,ValueError,TypeError,RuntimeError,ImportError) as exc:
            errors.append('render: '+str(exc)); statuses['render']='failed'
    elif require_render: errors.append('render: record missing; final pages not verified')
    else: warnings.append('No render record: final page rendering has not been verified.')
    return {'errors':errors,'warnings':warnings,'statuses':statuses,'page_count':page_count,
            'mathematical_verification':False,'visual_inspection_verified':False}
