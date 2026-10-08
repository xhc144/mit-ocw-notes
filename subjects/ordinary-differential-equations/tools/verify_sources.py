#!/usr/bin/env python3
"""Verify all archived original PDF bytes, hashes and page counts, in repo or ZIP."""
import argparse, hashlib, json
from pathlib import Path
import fitz

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--originals', type=Path)
parser.add_argument('--out', type=Path)
args = parser.parse_args()
originals = args.originals or (root / 'originals' if (root / 'originals').is_dir()
    else root.parents[1] / 'sources/ordinary-differential-equations')
manifest = json.loads((root / 'source-manifest.json').read_text())
entries = []
for record in manifest['sources']:
    relative = Path(record.get('path', '')).relative_to('sources/ordinary-differential-equations') if record['archive_allowed'] else None
    if relative is None:
        withheld = originals / record['course'] / (record['id'] + '.pdf')
        if withheld.exists():
            raise SystemExit(f'Withheld source unexpectedly present: {withheld}')
        continue
    path = originals / relative
    data = path.read_bytes()
    with fitz.open(path) as pdf:
        pages = len(pdf)
    actual = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'pages': pages}
    if any(actual[k] != record[k] for k in actual):
        raise SystemExit(f'Source mismatch: {relative}')
    entries.append({'file': relative.as_posix(), **actual})
actual_paths = {p.relative_to(originals).as_posix() for p in originals.rglob('*.pdf')}
if actual_paths != {e['file'] for e in entries}:
    raise SystemExit('Unexpected or missing original PDF')
result = {'status': 'PASS', 'files': len(entries), 'pages': sum(x['pages'] for x in entries), 'verified': entries}
if args.out:
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: result[k] for k in ('status','files','pages')}))
