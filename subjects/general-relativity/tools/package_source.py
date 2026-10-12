#!/usr/bin/env python3
"""Package the frozen source classes, excluding build caches, fonts and credentials."""
import hashlib,json,pathlib,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    files=[ROOT/x for x in ['main.tex','course-info.tex','BUILDING.md','README.md','SOURCES.md','LICENSE-NOTICE.md']]
    files.extend(sorted((ROOT/'chapters').glob('*.tex')))
    files.extend(sorted((ROOT/'tools').glob('*.py')))
    for folder in ['vendor','sources']:
        files.extend(p for p in sorted((ROOT/folder).rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix not in {'.pyc','.otf','.ttf','.woff','.woff2','.aux','.log','.out','.toc','.fls'})
    excluded_qa={'source-zip.json','zip-rebuild.json','release-manifest.json','publication-verification.json'}
    files.extend(p for p in sorted((ROOT/'qa').glob('*.json')) if p.name not in excluded_qa)
    assert len(files)==len(set(files))
    record={str(p.relative_to(ROOT)):sha(p) for p in files}
    dest=ROOT/'dist/general-relativity-source.zip';dest.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:
            info=zipfile.ZipInfo(str(p.relative_to(ROOT)),date_time=(2026,10,12,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,p.read_bytes())
        info=zipfile.ZipInfo('SOURCE-MANIFEST.json',date_time=(2026,10,12,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    out={'archive':str(dest.relative_to(ROOT)),'archive_sha256':sha(dest),'inputs':record,'file_count':len(files)+1,'fonts_bundled':False,'original_ocw_sources_bundled':True,'original_sources_as_body':False}
    (ROOT/'qa/source-zip.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(dest)
if __name__=='__main__':main()
