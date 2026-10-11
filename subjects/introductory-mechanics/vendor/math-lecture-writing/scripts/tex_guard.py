#!/usr/bin/env python3
"""Static risk reduction for reachable TeX sources; NOT an OS sandbox."""
from __future__ import annotations
import argparse
from dataclasses import dataclass, asdict
import json
from pathlib import Path
import re
from tex_scan import mask_noncode
from tex_project import ProjectError, expand_project, local_code_files, safe_path

@dataclass
class Finding:
    severity: str
    file: str
    line: int
    rule: str
    excerpt: str

RULES = [
    ('critical','shell execution',r'\\(?:write\s*18|ShellEscape|directlua|latelua)\b'),
    ('high','raw file I/O',r'\\(?:openout|openin|read|write)\b'),
    ('high','pipe input',r'\\input\s*\{?\s*["\']?\|'),
    ('medium','dynamic category codes require review',r'\\catcode\b'),
]

def scan_text(text: str,file: str,root: Path) -> list[Finding]:
    clean=mask_noncode(text); found=[]
    def add(severity: str,rule: str,m):
        found.append(Finding(severity,file,clean.count('\n',0,m.start())+1,rule,m.group(0)[:180]))
    for severity,rule,pattern in RULES:
        for m in re.finditer(pattern,clean,re.S): add(severity,rule,m)
    for m in re.finditer(r'\\(?:usepackage|RequirePackage)(?:\s*\[[^]]*\])?\s*\{([^}]+)\}',clean):
        if {'minted','pythontex','gnuplottex'} & {x.strip() for x in m.group(1).split(',')}:
            add('high','package may execute external processes',m)
    for m in re.finditer(r'\\(?:input|include|includegraphics|bibliography|addbibresource|lstinputlisting)\*?(?:\s*\[[^]]*\])?\s*\{([^}]+)\}',clean,re.S):
        target=m.group(1)
        if '\\' in target or '#' in target:
            add('medium','dynamic path requires explicit review',m); continue
        for name in target.split(','):
            try: safe_path(root,name,exists=False)
            except ProjectError: add('high','path outside project or invalid',m)
    return found

def scan_file(path: Path,root: Path) -> list[Finding]:
    if path.stat().st_size>4*1024*1024:
        return [Finding('high',str(path),1,'source exceeds 4 MiB','')]
    return scan_text(path.read_text(encoding='utf-8-sig'),path.relative_to(root).as_posix(),root)

def scan_project(main: Path) -> list[Finding]:
    project=expand_project(main)
    return [f for p in local_code_files(project) for f in scan_file(p,project.root)]

def scan_tree(root: Path) -> list[Finding]:
    """Explicit whole-folder audit only; ordinary compilation uses scan_project."""
    found=[]
    for p in root.rglob('*'):
        if any(x in {'.git','build','.build','.qa','__pycache__'} for x in p.relative_to(root).parts): continue
        if p.is_file() and p.suffix.lower() in {'.tex','.sty','.cls','.ltx'}:
            if p.is_symlink(): found.append(Finding('high',str(p),1,'symlink',''))
            else: found.extend(scan_file(p,root))
    return found

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('path',type=Path); ap.add_argument('--json',action='store_true')
    a=ap.parse_args()
    try:
        if not a.path.exists(): raise ValueError('Input path does not exist')
        found=scan_tree(a.path.resolve()) if a.path.is_dir() else scan_project(a.path.resolve())
    except (OSError,ValueError) as exc:
        print('INPUT ERROR:',exc); return 2
    if a.json: print(json.dumps([asdict(x) for x in found],ensure_ascii=False,indent=2))
    else:
        for x in found: print(f'{x.severity.upper()} {x.file}:{x.line} {x.rule}')
        if not found: print('No guarded constructs found; not a safety certification.')
    return int(any(x.severity in {'high','critical'} for x in found))

if __name__=='__main__': raise SystemExit(main())
