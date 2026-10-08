"""Create a deterministic source ZIP with no compiled files, fonts or held source prose."""
from pathlib import Path
import hashlib, json, zipfile
ROOT=Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    files=[ROOT/'main.tex',ROOT/'course-info.tex',ROOT/'backmatter.tex',ROOT/'build.sh',ROOT/'README.md',ROOT/'LICENSE.md',ROOT/'ASSESSMENTS.md',ROOT/'assessment-coverage.json',ROOT/'sources/assessment-resources.json',ROOT/'source-metadata.json',ROOT/'coverage.json',ROOT/'COVERAGE.md']
    for folder,patterns in [('chapters',['*.tex']),('assessments',['*.tex']),('tools',['*.py']),('data',['*.json','*.csv']),('review',['*-audit.json','*-numerical.json','*-computations.json','*-reader.json','coverage-check.json','inventory-freeze.json','visual-pages-*.json','visual-review-v2.json'])]:
        for pattern in patterns: files.extend((ROOT/folder).glob(pattern))
    # Cell values are the actual source of spreadsheet-only questions. They are data, not Excel executable code.
    files.extend((ROOT/'sources/15.053/assessments').glob('*.cells.json'))
    files=sorted(set(files)); missing=[str(f.relative_to(ROOT)) for f in files if not f.is_file()]
    if missing: raise SystemExit('Missing required source files: '+repr(missing))
    zpath=ROOT/'dist/source.zip'; zpath.parent.mkdir(exist_ok=True)
    entries=[]
    with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:
            name=p.relative_to(ROOT).as_posix()
            zi=zipfile.ZipInfo(name,date_time=(2026,10,8,0,0,0)); zi.external_attr=(0o755 if name=='build.sh' else 0o644)<<16
            zi.compress_type=zipfile.ZIP_DEFLATED; z.writestr(zi,p.read_bytes());entries.append({'path':name,'sha256':sha(p),'bytes':p.stat().st_size})
    report={'zip':'dist/source.zip','sha256':sha(zpath),'files':entries,'excluded':['original source PDFs','held external book prose','fonts','generated cls','build and render caches','aux/toc/log','Git metadata','credentials']}
    (ROOT/'review/source-package.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps({'zip_sha256':report['sha256'],'entries':len(entries),'bytes':zpath.stat().st_size}))
if __name__=='__main__':main()
