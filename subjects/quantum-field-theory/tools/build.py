#!/usr/bin/env python3
"""Build the self-contained Chinese manuscript in an isolated directory."""
import argparse,hashlib,json,os,pathlib,re,shutil,subprocess,tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=pathlib.Path,default=ROOT/'build');a=ap.parse_args()
    out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
    inputs=[ROOT/'main.tex',ROOT/'course-info.tex',*sorted((ROOT/'chapters').glob('*.tex'))]
    initial={str(p.relative_to(ROOT)):sha(p) for p in inputs}
    with tempfile.TemporaryDirectory(prefix='qft-tex-') as td:
        work=pathlib.Path(td)
        for p in inputs:
            q=work/p.relative_to(ROOT);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
        env=os.environ.copy();env.update(openin_any='p',openout_any='p',shell_escape='f',TEXMFOUTPUT=str(work))
        env.setdefault('XDG_CACHE_HOME','/tmp/qft-font-cache')
        env.setdefault('SOURCE_DATE_EPOCH','1791763200')
        env.setdefault('FORCE_SOURCE_DATE','1')
        previous=None;converged=False
        for passes in range(1,6):
            cp=subprocess.run(['xelatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder','main.tex'],cwd=work,env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=120)
            if cp.returncode:
                (out/'failed-build.log').write_text(cp.stdout)
                raise RuntimeError(cp.stdout[-4000:])
            current={x:sha(work/('main'+x))for x in ['.aux','.toc','.out']if(work/('main'+x)).exists()}
            log=(work/'main.log').read_text()
            if passes>=2 and current==previous and not re.search(r'Rerun to get|Label\(s\) may have changed|has changed\.\s*Rerun',log):converged=True;break
            previous=current
        if not converged:raise RuntimeError('References did not converge within five passes.')
        if initial!={str(p.relative_to(ROOT)):sha(p)for p in inputs}:raise RuntimeError('Source changed during build.')
        shutil.copy2(work/'main.log',out/'main.log')
        if re.search(r'Overfull \\[hv]box|Missing character:|LaTeX Font Warning:',log):raise RuntimeError('Layout or font error; inspect main.log before publishing.')
        for ext in ['.pdf','.log']:shutil.copy2(work/('main'+ext),out/('main'+ext))
        (out/'standalone-build.json').write_text(json.dumps({'source_sha256':initial,'passes':passes,'pdf_sha256':sha(out/'main.pdf'),'engine':'XeLaTeX; no shell escape','visual_review':'not_performed_by_builder'},ensure_ascii=False,indent=2)+'\n')
    print(out/'main.pdf')
if __name__=='__main__':main()
