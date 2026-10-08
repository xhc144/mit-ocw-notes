#!/usr/bin/env python3
"""Package only Chinese compilation inputs, build dependencies and attribution."""
from pathlib import Path
import hashlib,json,zipfile

def main():
    project=Path(__file__).resolve().parents[1]
    relative_files=[Path(x) for x in [
        'main.tex','LICENSE.md','SOURCE-README.txt',
        'tools/build.sh','tools/bootstrap_tex.py',
        'vendor/math-latex-typesetting/SOURCE.json',
        'vendor/math-latex-typesetting/requirements.txt',
        'vendor/math-latex-typesetting/templates/wangzhe_baiti_style.tex',
    ]]
    for folder,suffix in [('chapters','.tex'),('frontmatter','.tex'),
                          ('vendor/math-latex-typesetting/scripts','.py')]:
        relative_files.extend(path.relative_to(project) for path in (project/folder).glob('*'+suffix))
    files=[]
    for rel in relative_files:
        path=project/rel
        assert path.is_file() and not path.is_symlink(),rel
        files.append((path,'real-analysis/'+rel.as_posix()))
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
            'members':records,'member_count':len(records),'fonts_distributed':False,
            'english_originals_distributed':False,'qa_or_build_cache_distributed':False,
            'scope':'Chinese compilation inputs, validator/runtime setup tools and attribution only',
            'all_members_verified':True}
    (project/'qa/package-manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='members'},ensure_ascii=False))

if __name__=='__main__':main()
