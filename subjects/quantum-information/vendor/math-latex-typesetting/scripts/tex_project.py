#!/usr/bin/env python3
"""Resolve ordinary static TeX inputs, with source locations and bounded paths."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath
import re
from tex_scan import mask_noncode, read_group, escaped

class ProjectError(ValueError): pass

@dataclass
class Project:
    root: Path
    main: Path
    text: str
    files: list[Path]
    origins: list[tuple[str,int]]
    def location(self,line: int) -> tuple[str,int]:
        if not self.origins: return self.main.name,line
        return self.origins[min(max(line-1,0),len(self.origins)-1)]

def safe_path(root: Path,raw: str,exists: bool=True) -> Path:
    raw=raw.strip().strip('"')
    if not raw or '\x00' in raw or Path(raw).is_absolute() or PureWindowsPath(raw).drive or raw.startswith(('~','|')):
        raise ProjectError('Invalid/non-project path: '+repr(raw))
    if re.search(r'[#$%{}]',raw) or '\\' in raw:
        raise ProjectError('Dynamic/ambiguous TeX path; use a literal relative path with /: '+raw)
    candidate=root/raw
    for parent in (candidate,*candidate.parents):
        if parent==root.parent: break
        if parent.is_symlink(): raise ProjectError('Symlink in referenced path: '+raw)
    result=candidate.resolve()
    if not result.is_relative_to(root.resolve()): raise ProjectError('Path escapes project: '+raw)
    if exists and not result.is_file(): raise ProjectError('Missing input file: '+raw)
    return result

def input_commands(text: str):
    clean=mask_noncode(text)
    for m in re.finditer(r'\\(input|include)\b',clean):
        if escaped(clean,m.start()): continue
        pos=m.end()
        while pos<len(clean) and clean[pos].isspace(): pos+=1
        if pos<len(clean) and clean[pos]=='{':
            raw,end=read_group(clean,pos)
        else:
            word=re.match(r'[^\s%]+',clean[pos:])
            if not word: raise ProjectError('Missing input filename')
            raw=word.group(); end=pos+word.end()
        yield m.group(1),raw,m.start(),end

def expand_project(main: Path,max_depth: int=64) -> Project:
    main=main.resolve(); root=main.parent
    if not main.is_file(): raise ProjectError('Main TeX file does not exist: '+str(main))
    files=[]; total=0
    def expand(path: Path,stack: tuple[Path,...]) -> tuple[str,list[tuple[str,int]]]:
        nonlocal total
        if path in stack: raise ProjectError('Circular input: '+' -> '.join(p.name for p in stack+(path,)))
        if len(stack)>=max_depth: raise ProjectError('Input nesting limit exceeded')
        if path.stat().st_size>4*1024*1024: raise ProjectError('Source file exceeds 4 MiB: '+str(path))
        raw=path.read_text(encoding='utf-8-sig'); total+=len(raw)
        if total>20*1024*1024: raise ProjectError('Expanded source exceeds 20 MiB')
        if path not in files: files.append(path)
        clean=mask_noncode(raw)
        if re.search(r'\\(?:includeonly|import|subimport|subfile)\b',clean):
            raise ProjectError('Partial/dynamic project command needs explicit review; use ordinary input/include for full-project checks: '+str(path))
        chunks=[]; origins=[]; cursor=0
        def append_chunk(value: str,start: int):
            if not value: return
            chunks.append(value)
            first=raw.count('\n',0,start)+1
            origins.extend((path.relative_to(root).as_posix(),first+i) for i,_ in enumerate(value.splitlines(keepends=True)))
        for kind,target,start,end in input_commands(raw):
            # Newlines delimit expansion chunks and make line provenance unambiguous.
            head=raw[cursor:start]
            if head and not head.endswith('\n'): head+='\n'
            append_chunk(head,cursor)
            p=safe_path(root,target,exists=False)
            if not p.suffix: p=p.with_suffix('.tex')
            if not p.is_file(): raise ProjectError(f'{path.name}:{raw.count(chr(10),0,start)+1}: Missing input {target}')
            p=safe_path(root,p.relative_to(root).as_posix())
            content,locs=expand(p,stack+(path,))
            if kind=='include':
                append_chunk('\\clearpage\n',start)
            chunks.append(content if content.endswith('\n') else content+'\n'); origins.extend(locs)
            if kind=='include': append_chunk('\\clearpage\n',start)
            cursor=end
        append_chunk(raw[cursor:],cursor)
        return ''.join(chunks),origins
    text,origins=expand(main,())
    return Project(root,main,text,files,origins)

def local_code_files(project: Project) -> list[Path]:
    """Follow literal local class/package names as well as project TeX inputs."""
    result=list(project.files); i=0
    while i<len(result):
        p=result[i]; i+=1
        clean=mask_noncode(p.read_text(encoding='utf-8-sig'))
        for m in re.finditer(r'\\(documentclass|LoadClass|usepackage|RequirePackage)(?:\s*\[[^]]*\])?\s*\{([^}]+)\}',clean):
            ext='.cls' if m.group(1) in {'documentclass','LoadClass'} else '.sty'
            for name in m.group(2).split(','):
                q=safe_path(project.root,name.strip()+ext,exists=False)
                if q.exists() and q not in result: result.append(q)
        # A local style may also input ordinary TeX files.
        if p not in project.files:
            for _,target,_,_ in input_commands(clean):
                q=safe_path(project.root,target,exists=False)
                if not q.suffix: q=q.with_suffix('.tex')
                if q.exists() and q not in result: result.append(q)
    return result
