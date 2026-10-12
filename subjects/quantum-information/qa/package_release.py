"""Package only reviewed source inputs and actually rebuild the ZIP in a clean directory."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys,tempfile,zipfile
import fitz

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pdftext(p):
 d=fitz.open(p);return len(d),hashlib.sha256(''.join(pg.get_text() for pg in d).encode()).hexdigest()
p=argparse.ArgumentParser();p.add_argument('subject',type=Path);p.add_argument('--zip',type=Path);args=p.parse_args();r=args.subject.resolve();slug=r.name
canonical=r/'dist'/f'{slug}-zh.pdf';archive=args.zip.resolve() if args.zip else r/'dist'/f'{slug}-source.zip'
if not args.zip:
 fixed=['.gitignore','main.tex','course-info.tex','README.md','LICENSE.md','SOURCES.md','source-inventory.json','coverage-frozen.json','coverage.json','LECTURE-COVERAGE.md','lecture-coverage.json']
 files=[r/x for x in fixed]
 for name in ['chapters','figures','vendor']:files.extend(x for x in (r/name).rglob('*') if x.is_file() and '__pycache__' not in x.parts)
 files.extend(x for x in (r/'qa').glob('*') if x.is_file() and x.suffix in ['.json','.py','.md'] and x.name not in ['clean-rebuild.json','source-package-manifest.json','remote-verification.json'])
 assert all(x.is_file() and x.is_relative_to(r) for x in files)
 entries=[{'path':str(x.relative_to(r)),'bytes':x.stat().st_size,'sha256':sha(x)} for x in sorted(set(files))]
 manifest={'schema_version':1,'entries':entries,'exclusions':['downloaded original sources','OCR/screenshots','render caches','font files','compiler artifacts','release PDF and ZIP'],'note':'The manifest excludes its own hash to avoid a circular digest.'}
 (r/'qa/source-package-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');files.append(r/'qa/source-package-manifest.json')
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for x in sorted(set(files)):z.write(x,x.relative_to(r))
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 names=z.namelist();assert 'main.tex' in names
 assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names)
 work=Path(tempfile.mkdtemp(prefix='ocw-source-rebuild-',dir='/tmp'));z.extractall(work)
 pkg=json.loads((work/'qa/source-package-manifest.json').read_text())
 for e in pkg['entries']:assert sha(work/e['path'])==e['sha256'],e['path']
cmd=[sys.executable,'vendor/math-latex-typesetting/scripts/validate.py','main.tex','--out','build']
proc=subprocess.run(cmd,cwd=work,text=True,capture_output=True,timeout=300)
(work/'clean-build-output.txt').write_text(proc.stdout+'\n'+proc.stderr)
assert proc.returncode==0,(work,proc.stdout[-1500:],proc.stderr[-1000:])
a=pdftext(canonical);b=pdftext(work/'build/main.pdf');assert a==b,(a,b)
original=json.loads((r/'qa/all-pages-render-record.json').read_text());clean=json.loads((work/'build/main.render.json').read_text());assert [x['sha256'] for x in original['pages']]==[x['sha256'] for x in clean['pages']]
report={'schema_version':1,'status':'passed','zip_file':archive.name,'zip_sha256':sha(archive),'zip_crc':'passed','input_manifest_entries_verified':len(pkg['entries']),'clean_directory':str(work),'command':cmd,'compiler_returncode':proc.returncode,'canonical_pdf_sha256':sha(canonical),'canonical_pages':a[0],'clean_pdf_pages':b[0],'canonical_and_clean_extracted_text_sha256':a[1],'all_page_render_hashes_identical':True,'clean_pdf_sha256':sha(work/'build/main.pdf'),'font_dependencies':'TeX Live ctex, xeCJK, Fandol and CMU provisioned externally; fonts not distributed','automated_validation_report':'qa/automated-validation-report.json','visual_record':'qa/visual-audit.json','mathematical_review_scope':'qa/README.md; finite numeric cases and explicit proof limitations only'}
if not args.zip:(r/'qa/clean-rebuild.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
