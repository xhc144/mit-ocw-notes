#!/usr/bin/env python3
"""Verify archived sources if present; a standalone book ZIP needs no originals."""
import hashlib, json
from pathlib import Path
import fitz

root=Path(__file__).resolve().parents[1]
data=json.loads((root/'source-manifest.json').read_text())
assert data['selection_frozen'] and data['selected_count']==34
source=root.parents[1]/'sources/graph-theory'
if not source.is_dir():
    print('Standalone book: 34 source metadata records preserved; originals are external references, not build dependencies.')
else:
    for x in data['selected_resources']:
        p=source/x['path']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256'], x['id']
        assert len(fitz.open(p))==x['pages'] and x['archive_allowed'], x['id']
    assert not any('18225' in p.name for p in (source/'originals').iterdir())
    print('Verified all 34 original hashes and 1062 physical pages; held author book is not archived.')
