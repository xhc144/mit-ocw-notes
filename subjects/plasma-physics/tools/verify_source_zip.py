#!/usr/bin/env python3
"""Actually rebuild a fresh ZIP extraction and compare every PDF page."""
import argparse,hashlib,json,os,pathlib,subprocess,sys,tempfile,zipfile
import fitz

ROOT=pathlib.Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--zip',type=pathlib.Path,default=ROOT/'dist/plasma-physics-source.zip')
    ap.add_argument('--pdf',type=pathlib.Path,default=ROOT/'dist/plasma-physics-zh.pdf')
    ap.add_argument('--out',type=pathlib.Path,default=ROOT/'qa/clean-zip-build.json')
    a=ap.parse_args()
    with tempfile.TemporaryDirectory(prefix='plasma-clean-zip-') as td:
        clean=pathlib.Path(td)
        with zipfile.ZipFile(a.zip) as z:
            if z.testzip() is not None:raise RuntimeError('ZIP CRC failure')
            names=z.namelist()
            for name in names:
                p=pathlib.PurePosixPath(name)
                if p.is_absolute() or '..' in p.parts or p.parts[0]!='plasma-physics':
                    raise RuntimeError('Unexpected archive path')
            z.extractall(clean)
        source=clean/'plasma-physics';build=clean/'rebuilt'
        cp=subprocess.run([sys.executable,str(source/'tools/build.py'),'--out',str(build)],cwd=source,env=os.environ.copy(),capture_output=True,text=True,timeout=600)
        if cp.returncode:raise RuntimeError(cp.stdout[-2000:]+cp.stderr[-2000:])
        left=fitz.open(a.pdf);right=fitz.open(build/'main.pdf')
        if len(left)!=len(right):raise RuntimeError('Page count differs')
        matrix=fitz.Matrix(130/72,130/72)
        differences=[]
        for i in range(len(left)):
            if left[i].get_text()!=right[i].get_text():differences.append({'page':i+1,'kind':'text'})
            lp=left[i].get_pixmap(matrix=matrix,alpha=False);rp=right[i].get_pixmap(matrix=matrix,alpha=False)
            if (lp.width,lp.height,lp.samples)!=(rp.width,rp.height,rp.samples):
                differences.append({'page':i+1,'kind':'render'})
        if differences:raise RuntimeError(json.dumps(differences))
        record={'status':'PASS','physical_pages':len(left),'pdf_sha256':sha(a.pdf),'clean_rebuilt_pdf_sha256':sha(build/'main.pdf'),'source_zip_sha256':sha(a.zip),'zip_files':len(names),'all_page_text_equal':True,'all_page_renders_equal_at_dpi':130,'byte_identical_rebuild':sha(a.pdf)==sha(build/'main.pdf'),'actual_build_in_fresh_extraction':True,'builder_record':json.loads((build/'standalone-build.json').read_text()),'limitation':'PDF timestamps and trailer IDs may differ. Every page text and 130dpi raster byte matched; neither comparison substitutes for independent mathematical review.'}
        a.out.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({k:v for k,v in record.items() if k!='builder_record'},ensure_ascii=False))

if __name__=='__main__':main()
