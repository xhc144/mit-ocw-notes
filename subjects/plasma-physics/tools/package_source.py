#!/usr/bin/env python3
"""Package editable inputs and evidence, excluding originals and build caches."""
import hashlib,json,pathlib,shutil,zipfile

ROOT=pathlib.Path(__file__).resolve().parents[1]
POST_PACKAGE={'clean-zip-build.json','delivery-verification.json','publish-manifest.json'}

def selected_files():
    files=[ROOT/name for name in ('main.tex','course-info.tex','README.md','BUILDING.md','LICENSE.md','source-manifest.json')]
    for directory in ('chapters','tools','figures','vendor','qa'):
        for p in (ROOT/directory).rglob('*'):
            if not p.is_file() or p.is_symlink() or '__pycache__' in p.parts or '.qa' in p.parts:
                continue
            if directory=='qa' and (p.suffix not in ('.json','.md','.csv') or p.name in POST_PACKAGE):
                continue
            if p.suffix=='.pyc':
                continue
            files.append(p)
    return sorted(set(files))

def main():
    out=ROOT/'dist';out.mkdir(exist_ok=True)
    pdf=ROOT/'qa/typesetting/main.pdf'
    review=json.loads((ROOT/'qa/final-visual-review.json').read_text())
    actual=hashlib.sha256(pdf.read_bytes()).hexdigest()
    if review.get('pdf_actual_sha256',review.get('pdf',{}).get('sha256'))!=actual or review.get('status')!='PASS':
        raise RuntimeError('The exact PDF must have a completed final visual review before packaging.')
    shutil.copy2(pdf,out/'plasma-physics-zh.pdf')
    archive=out/'plasma-physics-source.zip'
    files=selected_files()
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:
            entry=zipfile.ZipInfo('plasma-physics/'+str(p.relative_to(ROOT)),date_time=(2026,10,12,0,0,0))
            entry.compress_type=zipfile.ZIP_DEFLATED;entry.external_attr=0o644<<16
            z.writestr(entry,p.read_bytes())
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:raise RuntimeError('ZIP CRC failure')
    print(json.dumps({'files':len(files),'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}))

if __name__=='__main__':main()
