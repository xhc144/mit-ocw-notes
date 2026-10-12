"""Compile this source bundle with XeLaTeX, in an isolated temporary directory."""
from pathlib import Path
import argparse,hashlib,json,os,re,shutil,subprocess,tempfile
ap=argparse.ArgumentParser();ap.add_argument('--output',default='build');args=ap.parse_args()
root=Path(__file__).resolve().parents[1];out=root/args.output;out.mkdir(parents=True,exist_ok=True)
main=(root/'main.tex').read_text();template=(root/'sources/approved-template.tex').read_text()
def locked(s):return s[s.index('% WZ-LOCKED-CLASS-BEGIN'):s.index('% WZ-LOCKED-CLASS-END')]
if locked(main)!=locked(template):raise SystemExit('Approved template locked class mismatch')
if shutil.which('xelatex') is None:raise SystemExit('XeLaTeX is required')
included=[root/name for name in re.findall(r'\\input\{([^}]+)\}',main)]
inputs=list(dict.fromkeys([root/'main.tex']+included+list((root/'qa').glob('*.csv'))))
env=os.environ.copy();env.update(openin_any='p',openout_any='p',shell_escape='f',SOURCE_DATE_EPOCH='1791763200',FORCE_SOURCE_DATE='1')
logs=[]
with tempfile.TemporaryDirectory(prefix='mit-physics-clean-build-') as td:
 work=Path(td)
 for p in inputs:
  target=work/p.relative_to(root);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
 for n in range(3):
  result=subprocess.run(['xelatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder','main.tex'],cwd=work,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=900)
  logs.append(result.stdout)
  if result.returncode:
   (out/'compile-failed.txt').write_text(result.stdout);raise SystemExit('XeLaTeX failed; inspect compile-failed.txt')
 log=(work/'main.log').read_text(errors='replace')
 if any(x in log for x in ['Missing character:','There were undefined references','LaTeX Error:','Undefined control sequence']):raise SystemExit('Compilation log contains unresolved errors')
 for name in ['main.pdf','main.log','main.toc','main.out','main.fls']:shutil.copy2(work/name,out/name)
 (out/'compile.txt').write_text('\n'.join(logs))
record={'engine':'XeLaTeX','passes':3,'no_shell_escape':True,'inputs':{p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},'pdf_sha256':hashlib.sha256((out/'main.pdf').read_bytes()).hexdigest()}
(out/'build-record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2));print(json.dumps(record,ensure_ascii=False,indent=2))
