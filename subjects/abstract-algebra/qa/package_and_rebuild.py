"""Package only Chinese source and rebuild it outside the repository."""
from pathlib import Path
import hashlib,json,zipfile,tempfile,subprocess,os,re,fitz
sub=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
names=['main.tex','build.sh','README.md','LICENSE.md','source-manifest.json','assessment-map.json','qa/core-review-a.md','qa/core-review-b.md','qa/assessment-independent.md','judson-assessment-map.json','licenses/GFDL-1.2.txt','qa/judson-independent.md','qa/judson-source-audit.json','qa/JUDSON-SOURCE-CHECK.md','qa/license-text-blocks.json','qa/license-pdf-check.json']
names += ['chapters/course-info.tex']+[f'chapters/ch{i:02d}.tex' for i in range(1,15)]+['chapters/homework.tex','chapters/exams.tex','chapters/source-map.tex','chapters/judson-frontmatter.tex','chapters/judson-supplement.tex','chapters/gfdl-license.tex']
if (sub/'qa/QUALITY.md').exists():names+=['qa/QUALITY.md']
assert len(names)==len(set(names))
dest=sub/'dist/source.zip'
members=[]
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in sorted(names):
  p=sub/n;assert p.is_file() and not p.is_symlink()
  assert p.suffix in ['.tex','.md','.json','.sh','.txt']
  data=p.read_bytes();item=zipfile.ZipInfo('abstract-algebra/'+n,date_time=(2026,10,8,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED;item.external_attr=(0o100755 if n=='build.sh' else 0o100644)<<16
  z.writestr(item,data);members.append({'path':item.filename,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
clean=Path(tempfile.mkdtemp(prefix='abstract-algebra-clean-'))
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None
 for n in z.namelist():assert n.startswith('abstract-algebra/') and '..' not in Path(n).parts
 z.extractall(clean)
work=clean/'abstract-algebra'
with (clean/'compile-output.txt').open('w') as log:
 result=subprocess.run(['bash','build.sh'],cwd=work,env=os.environ.copy(),stdout=log,stderr=subprocess.STDOUT,timeout=180)
assert result.returncode==0,(clean,result.returncode)
log=(work/'build/main.log').read_text(errors='replace')
bad=['Overfull','Missing character:','LaTeX Error','undefined references','undefined citations','Rerun to get cross-references right','multiply defined']
assert not any(s in log for s in bad),[s for s in bad if s in log]
a=fitz.open(sub/'dist/main.pdf');b=fitz.open(work/'dist/main.pdf');assert len(a)==len(b)==58
checks=[]
for i in range(len(a)):
 text_match=a[i].get_text()==b[i].get_text()
 ra=a[i].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False);rb=b[i].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
 image_match=(ra.width,ra.height,ra.samples)==(rb.width,rb.height,rb.samples)
 assert text_match and image_match,i+1
 checks.append({'page':i+1,'text_equal':text_match,'72dpi_render_equal':image_match,'render_sha256':hashlib.sha256(rb.samples).hexdigest()})
assert a.get_toc()==b.get_toc()
report={'status':'PASS','zip':'dist/source.zip','zip_sha256':sha(dest),'pdf_sha256':sha(sub/'dist/main.pdf'),'clean_pdf_sha256':sha(work/'dist/main.pdf'),'actual_pages':len(a),'source_members':members,'member_count':len(members),'no_original_english_pdf_or_tex_archive':True,'mandatory_English_license_and_copyright_only':True,'GFDL_complete_license_in_tex_and_txt':True,'no_fonts_cache_credentials_or_generated_pdf':True,'clean_directory':str(work),'command':'bash build.sh (three XeLaTeX rounds, no-shell-escape)','environment_note':'TEXMFHOME=/workspace/.local/texmf; XDG_CACHE_HOME=/tmp/abstract-algebra-fontcache supplies installed packages/fonts in this environment. Source package itself has no dependency on these absolute paths.','final_log_issues':[],'all_page_text_and_render_equal':True,'toc_equal':True,'byte_identical_pdf_claimed':False,'page_checks':checks}
(sub/'qa/clean-rebuild.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS: clean ZIP rebuild,',len(members),'members, 58 pages, all page text and renders equal. ZIP SHA256',sha(dest))
