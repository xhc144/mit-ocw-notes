#!/usr/bin/env python3
"""Create a reproducible editable source ZIP; exclude fonts, builds and Git data."""
from pathlib import Path
import hashlib,json,zipfile

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'topology-source.zip'
DIRECTORIES={'chapters','sources','research','review','tools','vendor'}
ROOT_FILES={'main.tex','frontmatter.tex','references.tex','README.md','PROGRESS.md','LICENSE.md','.gitignore','build-toolchain.md','topology.pdf'}

def main():
    members=[]
    for p in sorted(ROOT.rglob('*')):
        relative=p.relative_to(ROOT)
        if not p.is_file() or not (relative.parts[0] in DIRECTORIES or relative.as_posix() in ROOT_FILES):
            continue
        if '__pycache__' in relative.parts or p.suffix.lower() in {'.pyc','.otf','.ttf','.ttc','.woff','.woff2'}:
            continue
        if p.is_symlink():
            raise SystemExit(f'Refusing symlink: {relative}')
        members.append((p,relative.as_posix()))
    records=[]
    with zipfile.ZipFile(OUTPUT,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p,relative in members:
            payload=p.read_bytes()
            info=zipfile.ZipInfo('topology/'+relative,(2026,1,1,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=(0o100755 if relative.endswith('build.sh') else 0o100644)<<16
            z.writestr(info,payload)
            records.append({'path':relative,'sha256':hashlib.sha256(payload).hexdigest(),'bytes':len(payload)})
    with zipfile.ZipFile(OUTPUT) as z:
        assert z.testzip() is None
        for row in records:
            assert hashlib.sha256(z.read('topology/'+row['path'])).hexdigest()==row['sha256']
    result={'archive':OUTPUT.name,'sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest(), 'bytes':OUTPUT.stat().st_size,'members':records,'fonts_bundled':False}
    (ROOT/'release-source-manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='members'},ensure_ascii=False))

if __name__=='__main__':
    main()
