"""Extract this book's clean ZIP into a fresh directory and compare its rebuild."""
from pathlib import Path, PurePosixPath
import hashlib, json, os, subprocess, tempfile, zipfile
import fitz

def sha_bytes(raw): return hashlib.sha256(raw).hexdigest()
def main():
    root=Path(__file__).resolve().parents[1]
    package=root/'functional-analysis-source.zip'
    fresh=Path(tempfile.mkdtemp(prefix='functional-clean-rebuild-',dir='/tmp'))
    with zipfile.ZipFile(package) as archive:
        assert archive.testzip() is None
        for member in archive.infolist():
            p=PurePosixPath(member.filename)
            assert not p.is_absolute() and '..' not in p.parts
            assert p.parts[0]=='functional-analysis'
            assert p.suffix.lower() not in {'.pdf','.otf','.ttf','.png','.zip','.pyc'}
        archive.extractall(fresh)
        for member in archive.namelist():
            rel=PurePosixPath(member).relative_to('functional-analysis')
            assert (fresh/member).read_bytes()==(root/str(rel)).read_bytes(),rel
        count=len(archive.infolist())
    project=fresh/'functional-analysis'
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
    run=subprocess.run(['python',str(project/'vendor/math-latex-typesetting/scripts/validate.py'),
                        str(project/'main.tex'),'--out','build'],env=env,
                       capture_output=True,text=True,timeout=600)
    (fresh/'rebuild.log').write_text(run.stdout+run.stderr)
    if run.returncode: raise RuntimeError('Clean rebuild failed; see '+str(fresh/'rebuild.log'))
    a=fitz.open(root/'functional-analysis.pdf');b=fitz.open(project/'build/main.pdf')
    assert len(a)==len(b)
    assert a.get_toc()==b.get_toc()
    pages=[]
    for index,(pa,pb) in enumerate(zip(a,b),1):
        ta=pa.get_text();tb=pb.get_text();assert ta==tb,('text',index)
        def links(page):
            return [{k:str(v) if isinstance(v,(fitz.Point,fitz.Rect)) else v
                     for k,v in link.items() if k not in {'xref','id'}}
                    for link in page.get_links()]
        assert links(pa)==links(pb),('links',index)
        ha=sha_bytes(pa.get_pixmap(dpi=110,alpha=False).samples)
        hb=sha_bytes(pb.get_pixmap(dpi=110,alpha=False).samples)
        assert ha==hb,('raster',index)
        pages.append({'page':index,'text_sha256':sha_bytes(ta.encode()),
                      'raster_110dpi_sha256':ha,'text_pixels_and_links_identical':True})
    record={'zip_sha256':sha_bytes(package.read_bytes()),'clean_directory':str(fresh),
            'extracted_files':count,'all_extracted_members_match_current_sources':True,
            'rebuild_automated_status':'PASS','pages':len(a),
            'reference_pdf_sha256':sha_bytes((root/'functional-analysis.pdf').read_bytes()),
            'rebuilt_pdf_sha256':sha_bytes((project/'build/main.pdf').read_bytes()),
            'all_page_text_pixels_links_identical':True,'outlines_identical':True,
            'font_runtime_external':'Use the documented TeX/CTeX/Fandol/CM Unicode dependencies; fonts are not in the ZIP.',
            'page_evidence':pages}
    (root/'qa/zip-rebuild.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k!='page_evidence'},ensure_ascii=False))
if __name__=='__main__':main()
