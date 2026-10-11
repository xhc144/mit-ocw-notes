#!/usr/bin/env python3
"""Restore and validate only the already frozen official OCW objects."""
from pathlib import Path
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
import json,hashlib
import fitz
ROOT=Path(__file__).resolve().parents[3]
MAN=ROOT/'manifests/introductory-mechanics-sources.json'
m=json.loads(MAN.read_text())
def restore(a):
    p=ROOT/a['local_path']
    data=p.read_bytes() if p.exists() else urlopen(a['url'],timeout=90).read()
    if hashlib.sha256(data).hexdigest()!=a['sha256']:
        raise RuntimeError('Frozen source changed: '+a['local_path'])
    p.parent.mkdir(parents=True,exist_ok=True)
    if not p.exists():p.write_bytes(data)
    if p.suffix=='.pdf':
        assert data.startswith(b'%PDF')
        d=fitz.open(stream=data,filetype='pdf');assert len(d)==a['pages']
        tx='\n\f\n'.join(page.get_text() for page in d)
        assert hashlib.sha256(tx.encode()).hexdigest()==a['text_sha256']
        p.with_suffix('.txt').write_text(tx)
    return a['local_path']
with ThreadPoolExecutor(max_workers=4) as ex:
    restored=list(ex.map(restore,m['pages']+m['assets']))
print(f"Verified {len(m['pages'])} metadata pages, {len(m['assets'])} PDF files, {sum(a['pages'] for a in m['assets'])} source pages")
