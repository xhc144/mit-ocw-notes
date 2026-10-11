#!/usr/bin/env python3
"""Make a deterministic source archive with a complete member hash manifest."""
import argparse,hashlib,json,pathlib,stat,zipfile
SUBJECT=pathlib.Path(__file__).resolve().parents[1]
ROOT=SUBJECT.parents[1]
EXCLUDE_QA={'release.json','source-zip-rebuild.json','upload-manifest.json','upload-receipt.json'}
def sha(data):return hashlib.sha256(data).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=pathlib.Path,default=SUBJECT/'thermal-statistical-physics-source.zip');a=ap.parse_args()
    candidates=list(SUBJECT.rglob('*'))+list((ROOT/'sources/thermal-statistical-physics').rglob('*'))+[ROOT/'manifests/thermal-statistical-physics-sources.json']
    members={}
    for p in sorted(set(candidates)):
        if not p.is_file():continue
        if p.is_symlink():raise RuntimeError(f'Symlink rejected: {p}')
        rel=p.relative_to(ROOT)
        if 'build' in rel.parts or '__pycache__' in rel.parts:continue
        if p.suffix in {'.zip','.pyc','.aux','.log','.out','.toc','.fls'}:continue
        if p==SUBJECT/'thermal-statistical-physics-zh.pdf':continue
        if p.parent==SUBJECT/'qa' and p.name in EXCLUDE_QA:continue
        members[str(rel)]=p.read_bytes()
    record={'schema_version':1,'subject':'thermal-statistical-physics','files':[{'path':k,'sha256':sha(v),'bytes':len(v)}for k,v in members.items()],
            'excluded':'Generated PDF, ZIP, build outputs and final ZIP/publication receipts; no fonts or credentials bundled.'}
    members['SOURCE-ZIP-MANIFEST.json']=(json.dumps(record,ensure_ascii=False,indent=2)+'\n').encode()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(a.out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in sorted(members.items()):
            info=zipfile.ZipInfo(name,date_time=(2026,10,11,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=(stat.S_IFREG|0o644)<<16
            z.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    print(json.dumps({'zip':str(a.out),'sha256':sha(a.out.read_bytes()),'members':len(members),'bytes':a.out.stat().st_size}))
if __name__=='__main__':main()
