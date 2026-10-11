#!/usr/bin/env python3
"""Build a reproducible editable-source ZIP and verify every compiled input."""
from pathlib import Path
import hashlib,json,zipfile

ROOT=Path(__file__).resolve().parents[1]

def sha(data):return hashlib.sha256(data).hexdigest()

def main():
    build=json.loads((ROOT/'qa/build/main.build.json').read_text())
    files=[]
    for p in ROOT.rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(ROOT)
        if any(x in {'__pycache__','build','render','subjects'} for x in rel.parts):continue
        if p.suffix not in {'.tex','.csv','.py','.md','.json','.txt'}:continue
        if rel.as_posix() in {'qa/source-zip-manifest.json','qa/publication-receipt.json'}:continue
        files.append(p)
    files=sorted(files,key=lambda p:p.relative_to(ROOT).as_posix())
    contents={p.relative_to(ROOT).as_posix():p.read_bytes() for p in files}
    checks=[]
    for row in build['inputs']:
        assert row['path'] in contents,row['path']
        assert sha(contents[row['path']])==row['sha256'],row['path']
        checks.append(row)
    rows=[{'path':name,'bytes':len(data),'sha256':sha(data)} for name,data in contents.items()]
    manifest={'edition':'expanded','files':rows,'compiled_inputs':checks,
       'scope':'Editable Chinese LaTeX/TikZ/CSV/scripts and QA text; no original English PDF, font files or source notebook. Publication status in ZIP is a frozen precommit snapshot.'}
    contents['SOURCE-MANIFEST.json']=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()
    archive=ROOT/'classical-mechanics-source.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in sorted(contents.items()):
            info=zipfile.ZipInfo('classical-mechanics/'+name,date_time=(2026,10,11,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            z.writestr(info,data)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for name,data in contents.items():assert z.read('classical-mechanics/'+name)==data
    report={'archive':archive.name,'sha256':sha(archive.read_bytes()),'bytes':archive.stat().st_size,
       'entries':len(contents),'crc_test':'PASS','all_archive_member_bytes_match_source':True,
       'compiled_inputs_match_archive':len(checks),'manifest_in_archive':'classical-mechanics/SOURCE-MANIFEST.json','files':rows}
    (ROOT/'qa/source-zip-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['archive','sha256','bytes','entries','compiled_inputs_match_archive']}))

if __name__=='__main__':main()
