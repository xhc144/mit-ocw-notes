#!/usr/bin/env python3
"""Create an explicit, clean, reproducible source ZIP; excludes runtime fonts."""
from pathlib import Path
import hashlib,json,zipfile

def main():
    project=Path(__file__).resolve().parents[1]
    original=project.parents[1]/'sources/real-analysis'
    if not original.is_dir():original=project/'sources-original'
    excluded_dirs={'build','__pycache__','.git','sources-original'}
    excluded_suffixes={'.aux','.log','.out','.toc','.pyc','.synctex.gz','.zip'}
    files=[]
    for path in project.rglob('*'):
        rel=path.relative_to(project)
        if path.is_file() and not (set(rel.parts)&excluded_dirs) and path.suffix not in excluded_suffixes:
            if path.name in {'real-analysis.pdf','elegantbook-original-adapter.cls','package-manifest.json','remote-verification.json','upload-receipt.json','clean-rebuild.json','final-checks.json','upload-manifest.json','final-verification-receipt.json'}:continue
            files.append((path,'real-analysis/'+rel.as_posix()))
    for path in original.rglob('*'):
        if path.is_file():files.append((path,'real-analysis/sources-original/'+path.relative_to(original).as_posix()))
    files.sort(key=lambda x:x[1])
    records=[{'path':name,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()} for path,name in files]
    archive=project/'real-analysis-source.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zip:
        for path,name in files:
            info=zipfile.ZipInfo(name,date_time=(2026,10,8,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16
            zip.writestr(info,path.read_bytes())
    with zipfile.ZipFile(archive) as zip:
        for item in records:
            raw=zip.read(item['path'])
            assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256']
    result={'archive':archive.name,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
            'members':records,'member_count':len(records),'fonts_distributed':False,'all_members_verified':True}
    (project/'qa/package-manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='members'},ensure_ascii=False))

if __name__=='__main__':main()
