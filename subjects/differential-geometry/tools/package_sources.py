#!/usr/bin/env python3
"""Package only explicit editable source/skill dependencies, never build caches or fonts."""
from pathlib import Path
import hashlib, json, zipfile
ROOT=Path(__file__).resolve().parents[1]
files=[ROOT/'main.tex',ROOT/'build.sh',ROOT/'README.md',ROOT/'LICENSE.md',ROOT/'source-manifest.json',ROOT/'assignment-inventory.json']
files+=sorted((ROOT/'chapters').glob('*.tex'))
files+=sorted((ROOT/'tools').glob('*.py'))
for pkg in ['math-latex-typesetting','math-lecture-writing']:
 p=ROOT/'vendor'/pkg
 files += [p/'SKILL.md',p/'SOURCE.json',p/'requirements.txt']
 for directory in ['scripts','references','templates']:
  if (p/directory).is_dir():
   files += sorted(f for f in (p/directory).rglob('*') if f.is_file() and f.suffix in ['.py','.md','.json','.tex'])
files=sorted(set(files),key=lambda p:p.relative_to(ROOT).as_posix())
for p in files:
 if not p.is_file() or p.is_symlink():raise SystemExit(f'Missing/unsafe: {p}')
entries=[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
manifest={'schema_version':1,'source_files':entries,'no_fonts_or_build_artifacts':True}
(ROOT/'release-source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(ROOT/'differential-geometry-source.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files+[ROOT/'release-source-manifest.json']:
  rel=p.relative_to(ROOT).as_posix();info=zipfile.ZipInfo('differential-geometry/'+rel,date_time=(2026,10,8,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=(0o100644<<16);z.writestr(info,p.read_bytes())
print(json.dumps({'zip':'differential-geometry-source.zip','members':len(files)+1,'sha256':hashlib.sha256((ROOT/'differential-geometry-source.zip').read_bytes()).hexdigest()}))
