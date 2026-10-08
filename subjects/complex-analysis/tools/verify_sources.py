#!/usr/bin/env python3
"""Verify every archived source PDF against the recorded bytes, hash and page count."""
import argparse
import hashlib
import json
from pathlib import Path
import fitz

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--originals', type=Path)
parser.add_argument('--out', type=Path)
args = parser.parse_args()
originals = args.originals or (root / 'originals' if (root / 'originals').is_dir() else root.parents[1] / 'sources/complex-analysis')
manifest = json.loads((root / 'source-manifest.json').read_text())
entries = []
for record in manifest['files']:
    path = originals / record['file']
    data = path.read_bytes()
    with fitz.open(path) as pdf:
        pages = len(pdf)
    actual = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'pages': pages}
    if any(actual[k] != record[k] for k in actual):
        raise SystemExit(f'Source mismatch: {record["file"]}')
    entries.append({'file': record['file'], **actual})
result = {'status': 'PASS', 'files': len(entries), 'pages': sum(x['pages'] for x in entries), 'verified': entries}
if args.out:
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'files': result['files'], 'pages': result['pages']}))
