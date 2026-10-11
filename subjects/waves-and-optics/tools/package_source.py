#!/usr/bin/env python3
"""Build a deterministic, network-free manuscript ZIP from explicit source classes."""
import hashlib,json,pathlib,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
    files=[ROOT/'main.tex',ROOT/'course-info.tex',ROOT/'BUILDING.md',ROOT/'LICENSE-NOTICE.md',*sorted((ROOT/'chapters').glob('*.tex')),*sorted((ROOT/'tools').glob('*.py'))]
    files+=[p for p in sorted((ROOT/'vendor').rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix not in {'.pyc','.pdf'}]
    record={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    archive=ROOT/'waves-and-optics-source.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:
            info=zipfile.ZipInfo(str(p.relative_to(ROOT)),date_time=(2026,10,11,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,p.read_bytes())
        z.writestr(zipfile.ZipInfo('SOURCE-MANIFEST.json',date_time=(2026,10,11,0,0,0)),json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    out={'archive':archive.name,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'inputs':record,'file_count':len(files)+1,'fonts_bundled':False,'original_pdf_bundled':False}
    (ROOT/'qa/source-zip.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(archive)
if __name__=='__main__':main()
