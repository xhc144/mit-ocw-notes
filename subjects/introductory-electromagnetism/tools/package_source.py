#!/usr/bin/env python3
"""Create one deterministic source ZIP; original PDFs and fonts stay outside it."""
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

root = Path(__file__).resolve().parents[1]
target = root / 'introductory-electromagnetism-zh-source.zip'
files = [root / name for name in (
    'main.tex', 'course-info.tex', 'source-map.tex', 'BUILDING.txt',
    'LICENSE.md', 'build.sh', 'coverage.json')]
for directory in ('chapters', 'figures', 'vendor', 'tools'):
    files += [p for p in (root / directory).rglob('*')
              if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc']
for path in (root / 'qa').glob('*'):
    if path.is_file() and path.suffix in ('.json', '.md', '.txt') and path.name not in (
            'rebuild.json', 'remote-verification.json', 'release.json', 'handoff.md'):
        files.append(path)

def put(archive, name, data, executable=False):
    entry = ZipInfo('introductory-electromagnetism/' + name, (2026, 10, 11, 0, 0, 0))
    entry.compress_type = ZIP_DEFLATED
    entry.external_attr = (0o100755 if executable else 0o100644) << 16
    archive.writestr(entry, data)

with ZipFile(target, 'w') as archive:
    for path in sorted(set(files)):
        put(archive, path.relative_to(root).as_posix(), path.read_bytes(), path.name == 'build.sh')
    manifest = root.parents[1] / 'manifests' / 'introductory-electromagnetism-sources.json'
    if manifest.is_file():
        put(archive, 'source-manifest.json', manifest.read_bytes())
with ZipFile(target) as archive:
    assert archive.testzip() is None
    print(json.dumps({'zip': str(target), 'entries': len(archive.namelist()),
                      'uncompressed_bytes': sum(x.file_size for x in archive.infolist())}))
