#!/usr/bin/env python3
"""Package a clean, checksummed editable book with unchanged original OCW PDFs."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--originals', type=Path, default=root.parents[1] / 'sources/complex-analysis')
parser.add_argument('--output', type=Path, default=root / 'complex-analysis-source.zip')
args = parser.parse_args()
excluded_dirs = {'build', '.runtime', '__pycache__', '.git'}
excluded_suffixes = {'.pyc', '.zip', '.png', '.aux', '.log', '.toc', '.out', '.fls', '.fdb_latexmk', '.synctex.gz'}
excluded_names = {'complex-analysis.pdf', 'elegantbook-original-adapter.cls', 'zip-rebuild.json', 'artifact-checksums.json', 'remote-verification.json', 'publication-manifest.json'}
members = []
for base, prefix in [(root, ''), (args.originals, 'originals/')]:
    for path in sorted(base.rglob('*')):
        relative = path.relative_to(base)
        if any(x in excluded_dirs for x in relative.parts) or path.name in excluded_names or path.suffix in excluded_suffixes:
            continue
        if path.is_symlink():
            raise SystemExit(f'Symlink not packaged: {path}')
        if path.is_file():
            data = path.read_bytes()
            members.append((prefix + relative.as_posix(), data))
inventory = [{'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for name, data in members]
with zipfile.ZipFile(args.output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for name, data in members:
        info = zipfile.ZipInfo(name, date_time=(2026,10,8,0,0,0))
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, data)
    archive.writestr('ZIP-CONTENTS.json', json.dumps({'format': 1, 'members': inventory}, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'zip': str(args.output), 'members': len(members)+1, 'bytes': args.output.stat().st_size, 'sha256': hashlib.sha256(args.output.read_bytes()).hexdigest()}))
