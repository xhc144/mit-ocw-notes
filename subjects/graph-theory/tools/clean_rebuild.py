#!/usr/bin/env python3
"""Extract the final ZIP into a fresh directory and compare every rebuilt page."""
import hashlib,json,os,re,subprocess,tempfile,zipfile
from pathlib import Path
import fitz

ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    package=ROOT/'dist/source.zip'
    temporary=Path(tempfile.mkdtemp(prefix='graph-clean-rebuild-'))
    with zipfile.ZipFile(package) as z:
        for name in z.namelist():
            p=Path(name)
            assert not p.is_absolute() and '..' not in p.parts
            assert name.startswith('graph-theory/')
        z.extractall(temporary)
    book=temporary/'graph-theory'
    assert not (book/'dist/main.pdf').exists() and not (book/'build').exists()
    subprocess.run(['bash','build.sh'],cwd=book,env=os.environ.copy(),check=True)
    original=fitz.open(ROOT/'dist/main.pdf');rebuilt=fitz.open(book/'dist/main.pdf')
    assert len(original)==len(rebuilt)
    rows=[]
    for n,(a,b) in enumerate(zip(original,rebuilt),1):
        text=a.get_text()==b.get_text()
        size=a.rect==b.rect
        pixels=a.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).samples==b.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).samples
        assert text and size and pixels,n
        rows.append({'page':n,'same_native_text':text,'same_size':size,'same_72dpi_pixels':pixels})
    assert original.get_toc()==rebuilt.get_toc()
    def links(page):
        return [(x['kind'],x.get('page'),x.get('uri'),x.get('nameddest'),tuple(x['from'])) for x in page.get_links()]
    assert all(links(a)==links(b) for a,b in zip(original,rebuilt))
    log=(book/'build/main.log').read_text(errors='replace')
    bad=re.findall(r'^!|Overfull|Missing character|Undefined control sequence|There were undefined references',log,re.M)
    assert not bad,bad
    result={'status':'passed','package':'dist/source.zip','package_sha256':sha(package),
        'clean_extract_dir':str(book),'compile_command':'inherited TeX/font runtime environment; bash build.sh',
        'compile_passes':3,'initial_output_pdf_present':False,'independent_repository_inputs_required':False,
        'source_originals_required':False,'original_pdf_sha256':sha(ROOT/'dist/main.pdf'),
        'clean_rebuilt_pdf_sha256':sha(book/'dist/main.pdf'),
        'pdf_bytes_identical':sha(ROOT/'dist/main.pdf')==sha(book/'dist/main.pdf'),
        'pages':rows,'page_count':len(rows),'bookmarks_identical':True,'link_annotations_identical':True,
        'final_log_errors_or_overfull':len(bad),'fonts_in_zip':False,
        'limits_zh':'全新目录实际重编；文本、尺寸、72dpi像素及书签一致。PDF元数据/ID可导致字节不同，外部TeX和字体运行时另需安装。'}
    (ROOT/'qa/clean-rebuild.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(f'PASS: {len(rows)} clean rebuilt pages, text/size/pixels/bookmarks equal; PDF byte equal={result["pdf_bytes_identical"]}')
if __name__=='__main__':main()
