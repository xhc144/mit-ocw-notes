#!/usr/bin/env python3
"""Package a clean, checksummed editable book plus unchanged official originals."""
import argparse, hashlib, json, zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--originals', type=Path, default=root.parents[1] / 'sources/ordinary-differential-equations')
parser.add_argument('--output', type=Path, default=root / 'ordinary-differential-equations-source.zip')
args = parser.parse_args()
excluded_dirs = {'build', '.runtime', '__pycache__', '.git', 'source-visual'}
excluded_suffixes = {'.pyc', '.zip', '.aux', '.log', '.toc', '.out', '.fls', '.fdb_latexmk', '.gz'}
excluded_names = {'ordinary-differential-equations.pdf', 'elegantbook-original-adapter.cls',
    'zip-rebuild.json', 'artifact-checksums.json', 'source-investigation.json',
    'investigate_sources.py', 'finalize_sources.py'}
members = []
for base, prefix in [(root, ''), (args.originals, 'originals/')]:
    for path in sorted(base.rglob('*')):
        relative = path.relative_to(base)
        if any(x in excluded_dirs for x in relative.parts) or path.name in excluded_names or path.suffix in excluded_suffixes:
            continue
        if path.is_symlink():
            raise SystemExit(f'Symlink not packaged: {path}')
        if path.is_file():
            members.append((prefix + relative.as_posix(), path.read_bytes()))
inventory = [{'path': n, 'bytes': len(d), 'sha256': hashlib.sha256(d).hexdigest()} for n,d in members]
members.append(('ZIP-CONTENTS.json', (json.dumps({'format':1,'members':inventory},ensure_ascii=False,indent=2)+'\n').encode()))
with zipfile.ZipFile(args.output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for name, data in members:
        info = zipfile.ZipInfo(name, date_time=(2026,10,8,0,0,0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, data)
print(json.dumps({'members':len(members),'bytes':args.output.stat().st_size,'sha256':hashlib.sha256(args.output.read_bytes()).hexdigest()}))
