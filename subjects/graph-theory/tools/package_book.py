#!/usr/bin/env python3
"""Package explicit Chinese book dependencies without sources, fonts or cache."""
import hashlib,json,zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FILES=['main.tex','build.sh','README.md','LICENSE.md','source-manifest.json',
       *[f'chapters/ch{n:02}.tex' for n in range(1,18)],'chapters/source-map.tex',
       'tools/bootstrap_tex.py','tools/verify_sources.py','tools/audit_pdf.py',
       'tools/matrix-electric-check.py','tools/spectral-extremal-check.py','tools/ramsey-poset-check.py',
       'qa/style-baseline.tex','qa/classical-review.md','qa/polynomial-algorithm-review.md',
       'qa/matrix-electric-review.md','qa/spectral-extremal-review.md','qa/ramsey-poset-review.md',
       'qa/spectral-extremal-computations.json','qa/ramsey-poset-computations.json',
       'qa/visual-pages-01-20.json','qa/visual-pages-21-40.json','qa/visual-pages-41-56.json',
       'qa/QUALITY.json','qa/final-checks.json','qa/typesetting/main.build.json',
       'qa/typesetting/main.render.json','qa/typesetting/validation_report.json']
for p in sorted((ROOT/'vendor/math-latex-typesetting').rglob('*')):
    if p.is_file() and '__pycache__' not in p.parts:
        FILES.append(p.relative_to(ROOT).as_posix())
FILES.append('tools/package_book.py')
assert len(FILES)==len(set(FILES))
(ROOT/'dist').mkdir(exist_ok=True)
records=[]
with zipfile.ZipFile(ROOT/'dist/source.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
    for name in FILES:
        path=ROOT/name
        assert path.is_file() and not path.is_symlink(),name
        raw=path.read_bytes();entry=zipfile.ZipInfo('graph-theory/'+name,(2026,10,8,0,0,0))
        entry.compress_type=zipfile.ZIP_DEFLATED;entry.external_attr=(0o100755 if name.endswith('.sh') else 0o100644)<<16
        archive.writestr(entry,raw)
        records.append({'member':entry.filename,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
out={'package':'dist/source.zip','sha256':hashlib.sha256((ROOT/'dist/source.zip').read_bytes()).hexdigest(),
     'member_count':len(records),'members':records,'original_english_pdfs_included':False,
     'fonts_build_cache_rendered_pages_included':False,'compile_dependencies':'All LaTeX inputs and fixed class are included; TeX/font runtime dependencies external.'}
(ROOT/'qa/package-manifest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(f'Created source.zip with {len(records)} members, SHA256 {out["sha256"]}')
