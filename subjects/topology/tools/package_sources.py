#!/usr/bin/env python3
"""Package only the Chinese book's actual compile dependencies and attribution."""
from pathlib import Path
import hashlib,json,zipfile,sys,re

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'topology-source.zip'
sys.path.insert(0,str(ROOT/'vendor/math-latex-typesetting/scripts'))
from tex_project import expand_project, safe_path
from tex_scan import mask_noncode

def main():
    project=expand_project(ROOT/'main.tex')
    members=[(p,p.relative_to(ROOT).as_posix()) for p in project.files]
    # This book's figures are native TikZ. Include any future literal image dependency,
    # but never select an archive directory merely because it exists.
    for m in re.finditer(r'\\includegraphics(?:\s*\[[^]]*\])?\s*\{([^}]+)\}',mask_noncode(project.text)):
        p=safe_path(ROOT,m.group(1))
        members.append((p,p.relative_to(ROOT).as_posix()))
    members.extend([(ROOT/'source-README.md','README.md'),(ROOT/'LICENSE.md','LICENSE.md'),
                    (ROOT/'source-provenance.md','source-provenance.md'),
                    (ROOT/'sources/licenses/CC-BY-NC-SA-4.0.txt','licenses/CC-BY-NC-SA-4.0.txt')])
    members=sorted(dict((archive_path,(p,archive_path)) for p,archive_path in members).values(),key=lambda x:x[1])
    records=[]
    with zipfile.ZipFile(OUTPUT,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p,relative in members:
            payload=p.read_bytes()
            info=zipfile.ZipInfo('topology/'+relative,(2026,1,1,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16
            z.writestr(info,payload)
            records.append({'path':relative,'source_path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(payload).hexdigest(),'bytes':len(payload)})
    with zipfile.ZipFile(OUTPUT) as z:
        assert z.testzip() is None
        for row in records:
            assert hashlib.sha256(z.read('topology/'+row['path'])).hexdigest()==row['sha256']
    result={'archive':OUTPUT.name,'sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest(), 'bytes':OUTPUT.stat().st_size,'members':records,'fonts_bundled':False,
            'scope':'Chinese compile dependencies, license and attribution only; no English originals, source snapshots, review archive or finished PDF',
            'compile_tex_files':[p.relative_to(ROOT).as_posix() for p in project.files]}
    (ROOT/'release-source-manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='members'},ensure_ascii=False))

if __name__=='__main__':
    main()
