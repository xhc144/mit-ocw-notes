#!/usr/bin/env python3
"""One bounded XeLaTeX build implementation shared by both skills.

Build in a fresh directory, follow real inputs, wait for reference convergence,
record file hashes, and never silently substitute fonts. Not a full sandbox.
"""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from tex_guard import scan_project, scan_text
from tex_project import expand_project

SOURCE_EXTENSIONS={'.tex','.sty','.cls','.clo','.def','.cfg','.ltx','.bib','.bst','.png','.jpg','.jpeg','.pdf','.eps','.svg','.csv','.dat','.txt','.pgf','.tikz'}
SKIP={'.git','build','safe-build','.build','.qa','__pycache__','node_modules','.venv','source-materials'}
RERUN=re.compile(r'Label\(s\) may have changed|Rerun to get|rerunfilecheck Warning: File .*has changed',re.I)

def sha256(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def write_json(p: Path,data: dict) -> None:
    p.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.record-',suffix='.json',dir=p.parent)
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f: json.dump(data,f,ensure_ascii=False,indent=2); f.write('\n')
        os.replace(tmp,p)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def copy_project(source: Path,destination: Path,exclude: tuple[Path,...]=()) -> dict[str,str]:
    before={}
    for p in source.rglob('*'):
        rel=p.relative_to(source)
        if any(part in SKIP for part in rel.parts) or any(p==x or p.is_relative_to(x) for x in exclude): continue
        if p.is_symlink(): continue  # referenced symlinks are rejected by the resolver
        if not p.is_file() or p.suffix.lower() not in SOURCE_EXTENSIONS: continue
        if p.stat().st_size>50*1024*1024: continue  # unused large source material is not a build dependency
        q=destination/rel; q.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(p,q); before[rel.as_posix()]=sha256(p)
    return before

def build(tex: Path,out: Path|None=None,replacement: str|None=None,passes: int=2,
          timeout: int=120,max_passes: int=5) -> dict:
    tex=tex.resolve(); project=tex.parent
    if not tex.is_file() or tex.suffix.lower()!='.tex': raise ValueError('Expected an existing .tex file')
    if timeout<1 or passes<1 or max_passes<max(2,passes): raise ValueError('Invalid timeout/pass limits')
    out=out.resolve() if out is not None else None
    if out is not None: out.mkdir(parents=True,exist_ok=True)
    record={'schema_version':1,'status':'failed','source':tex.name,'inputs':[],
            'started_at':datetime.now(timezone.utc).isoformat(),'passes':0,
            'pdf':{'path':os.path.relpath(out/(tex.stem+'.pdf'),project).replace(os.sep,'/') if out else '', 'sha256':''},
            'mathematical_verification':False,'visual_review':'not_performed'}
    transcripts=[]
    try:
        if shutil.which('xelatex') is None: raise RuntimeError('XeLaTeX is missing; no font or engine substitution was made.')
        proj=expand_project(tex)
        findings=scan_project(tex)
        if replacement is not None: findings+=scan_text(replacement,'diagnostic-copy',project)
        record['guard_warnings']=[f'{x.file}:{x.line} {x.rule}' for x in findings if x.severity=='medium']
        blocked=[x for x in findings if x.severity in {'high','critical'}]
        if blocked: raise RuntimeError('TeX guard blocked: '+'; '.join(f'{x.file}:{x.line} {x.rule}' for x in blocked))
        with tempfile.TemporaryDirectory(prefix='math-tex-') as directory:
            work=Path(directory)
            excludes=() if out is None or out==project else (out,)
            before=copy_project(project,work,excludes)
            # Never copy a prior generated PDF into its own build.
            old_pdf=work/(tex.stem+'.pdf')
            if old_pdf.exists(): old_pdf.unlink()
            local=work/tex.name
            if not local.exists(): raise RuntimeError('Main source was not staged (path/size policy).')
            for p in proj.files:
                if p.relative_to(project).as_posix() not in before: raise RuntimeError('A referenced source could not be staged: '+str(p))
            if replacement is not None: local.write_text(replacement,encoding='utf-8')
            env=os.environ.copy(); env.update(openin_any='p',openout_any='p',shell_escape='f',TEXMFOUTPUT=str(work))
            previous=None; converged=False
            for i in range(1,max_passes+1):
                proc=subprocess.run(['xelatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error',
                    '-file-line-error','-recorder','./'+local.name],cwd=work,env=env,stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,errors='replace',check=False,timeout=timeout,shell=False)
                transcripts.append(f'PASS {i}\n'+proc.stdout); record['passes']=i
                if proc.returncode: raise RuntimeError(f'XeLaTeX pass {i} failed:\n'+proc.stdout[-4000:])
                log=local.with_suffix('.log').read_text(encoding='utf-8',errors='replace')
                current={ext:sha256(work/(tex.stem+ext)) for ext in ('.aux','.toc','.out','.lof','.lot') if (work/(tex.stem+ext)).exists()}
                if i>=max(2,passes) and current==previous and not RERUN.search(log): converged=True; break
                previous=current
            if not converged: raise RuntimeError('References did not converge within the configured pass limit; final files were not published.')
            pdf=local.with_suffix('.pdf')
            if not pdf.is_file() or pdf.read_bytes()[:5]!=b'%PDF-': raise RuntimeError('No valid PDF header produced')
            fls=local.with_suffix('.fls')
            if not fls.exists(): raise RuntimeError('Missing TeX recorder (.fls)')
            used={tex.name}; generated=[]
            for line in fls.read_text(encoding='utf-8',errors='replace').splitlines():
                if not line.startswith('INPUT '): continue
                q=Path(line[6:]); q=(work/q).resolve() if not q.is_absolute() else q.resolve()
                if not q.is_relative_to(work): continue  # TeX system installation is not bundled
                rel=q.relative_to(work).as_posix()
                if rel in before: used.add(rel)
                elif q.is_file() and q.suffix.lower() in {'.cls','.sty','.tex'}: generated.append(rel)
            for rel in used:
                p=project/rel
                if not p.is_file() or sha256(p)!=before[rel]: raise RuntimeError('Source changed during compilation: '+rel)
            record.update(status='built',converged=True,inputs=[{'path':r,'sha256':before[r]} for r in sorted(used)],
                generated_inputs=sorted(set(generated)),finished_at=datetime.now(timezone.utc).isoformat())
            record['pdf']['sha256']=sha256(pdf)
            result={'log':log,'stdout':'\n'.join(transcripts),'record':record}
            if out is not None:
                for ext in ('.pdf','.log'): shutil.copy2(local.with_suffix(ext),out/(tex.stem+ext))
                result.update(pdf=str(out/(tex.stem+'.pdf')),build_record=str(out/(tex.stem+'.build.json')))
            return result
    except (OSError,ValueError,RuntimeError,subprocess.TimeoutExpired) as exc:
        record['status']='failed'
        record['error']=str(exc)
        if isinstance(exc, subprocess.TimeoutExpired):
            raise RuntimeError(f'XeLaTeX exceeded the per-pass timeout ({timeout}s); no new PDF was published.') from exc
        raise
    finally:
        if out is not None:
            (out/(tex.stem+'.compile.txt')).write_text('\n'.join(transcripts),encoding='utf-8')
            write_json(out/(tex.stem+'.build.json'),record)
