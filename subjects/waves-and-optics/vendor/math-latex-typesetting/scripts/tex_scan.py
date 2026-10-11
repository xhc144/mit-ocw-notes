#!/usr/bin/env python3
"""Offset-preserving scanner for ordinary LaTeX, not a TeX interpreter."""
from __future__ import annotations
from dataclasses import dataclass
import re

VERBATIM = {'verbatim','verbatim*','Verbatim','Verbatim*','lstlisting','minted','comment'}
DISPLAY = {'equation','equation*','align','align*','alignat','alignat*','gather','gather*',
           'multline','multline*','flalign','flalign*','eqnarray','eqnarray*','displaymath'}

def escaped(s: str, i: int) -> bool:
    n=0; i-=1
    while i >= 0 and s[i]=='\\': n+=1; i-=1
    return bool(n%2)

def read_group(s: str, start: int, left: str='{', right: str='}') -> tuple[str,int]:
    while start<len(s) and s[start].isspace(): start+=1
    if start>=len(s) or s[start]!=left: raise ValueError(f'Expected {left} at character {start}')
    depth=1; i=start+1
    while i<len(s):
        if not escaped(s,i):
            if s[i]==left: depth+=1
            elif s[i]==right:
                depth-=1
                if depth==0: return s[start+1:i],i+1
        i+=1
    raise ValueError(f'Unclosed group at character {start}')

def _blank(out: list[str], start: int, end: int) -> None:
    for i in range(start,end):
        if out[i] not in '\r\n': out[i]=' '

def mask_noncode(s: str, literals: bool=True) -> str:
    """Mask comments AND literal examples, retaining exact offsets and line numbers.

    Verbatim is recognized before interpreting percent signs. This matters for
    a literal `%` followed by a real command on the same source line.
    """
    out=list(s); i=0
    while i<len(s):
        if s[i]=='%' and not escaped(s,i):
            end=s.find('\n',i); end=len(s) if end<0 else end
            _blank(out,i,end); i=end; continue
        if s[i]=='\\' and not escaped(s,i):
            m=re.match(r'\\verb\*?([^A-Za-z\s])',s[i:])
            if m:
                end=s.find(m.group(1),i+m.end())
                end=len(s) if end<0 else end+1
                if literals: _blank(out,i,end)
                i=end; continue
            m=re.match(r'\\begin\s*\{([^}]+)\}',s[i:])
            if m and m.group(1) in VERBATIM:
                close=re.search(r'\\end\s*\{'+re.escape(m.group(1))+r'\}',s[i+m.end():])
                end=len(s) if close is None else i+m.end()+close.end()
                if literals: _blank(out,i,end)
                i=end; continue
            if literals:
                m=re.match(r'\\string\s*(?:\\[A-Za-z@]+|\\.|.)',s[i:],re.S)
                if m: _blank(out,i,i+m.end()); i+=m.end(); continue
                m=re.match(r'\\detokenize\b',s[i:])
                if m:
                    try: _,end=read_group(s,i+m.end())
                    except ValueError: end=i+m.end()
                    _blank(out,i,end); i=end; continue
        i+=1
    return ''.join(out)

def strip_comments(s: str) -> str:
    return mask_noncode(s,literals=False)

def document_body(s: str) -> tuple[str,int]:
    clean=mask_noncode(s)
    m=re.search(r'\\begin\s*\{document\}',clean)
    if not m: return clean,0
    stop=re.search(r'\\end\s*\{document\}',clean[m.end():])
    end=m.end()+stop.start() if stop else len(clean)
    return clean[m.end():end],m.end()

def commands(s: str,names: tuple[str,...]):
    for m in re.finditer(r'\\('+'|'.join(re.escape(n) for n in names)+r')\b(\*)?',s):
        if escaped(s,m.start()): continue
        pos=m.end()
        while pos<len(s) and s[pos].isspace(): pos+=1
        if pos<len(s) and s[pos]=='[':
            _,pos=read_group(s,pos,'[',']')
        try: content,end=read_group(s,pos)
        except ValueError: continue
        yield m.group(1),content,m.start(),end

@dataclass
class InlineMath:
    start:int
    end:int
    content:str
    raw:str

def inline_math(s: str) -> list[InlineMath]:
    clean=mask_noncode(s); found=[]; i=0
    def closing(token: str,start: int) -> int:
        j=clean.find(token,start)
        while j>=0 and escaped(clean,j): j=clean.find(token,j+len(token))
        return j
    while i<len(clean):
        if clean[i]=='\\' and not escaped(clean,i):
            m=re.match(r'\\begin\s*\{([^}]+)\}',clean[i:])
            if m and m.group(1) in DISPLAY:
                end=re.search(r'\\end\s*\{'+re.escape(m.group(1))+r'\}',clean[i+m.end():])
                if not end: raise ValueError(f'Unclosed display environment at character {i}')
                i=i+m.end()+end.end(); continue
            if clean.startswith('\\[',i):
                j=closing('\\]',i+2)
                if j<0: raise ValueError(f'Unclosed display math at character {i}')
                i=j+2; continue
            if clean.startswith('\\(',i):
                j=closing('\\)',i+2)
                if j<0: raise ValueError(f'Unclosed inline math at character {i}')
                found.append(InlineMath(i,j+2,clean[i+2:j],s[i:j+2])); i=j+2; continue
        if clean[i]=='$' and not escaped(clean,i):
            delim='$$' if clean.startswith('$$',i) else '$'; j=closing(delim,i+len(delim))
            if j<0: raise ValueError(f'Unclosed math delimiter at character {i}')
            if delim=='$': found.append(InlineMath(i,j+1,clean[i+1:j],s[i:j+1]))
            i=j+len(delim); continue
        i+=1
    return found

def environment_spans(s: str,selected: set[str]):
    stack=[]
    for m in re.finditer(r'\\(begin|end)\s*\{([^}]+)\}',mask_noncode(s)):
        name=m.group(2)
        if m.group(1)=='begin': stack.append((name,m.start(),m.end()))
        elif stack and stack[-1][0]==name:
            _,start,cs=stack.pop()
            if name in selected: yield name,start,cs,m.start(),m.end()

def environment_errors(s: str) -> list[tuple[int,str]]:
    stack=[]; errors=[]
    for m in re.finditer(r'\\(begin|end)\s*\{([^}]+)\}',mask_noncode(s)):
        name=m.group(2)
        if name=='filecontents*': continue  # source-generating wrapper; TeX diagnoses it
        if m.group(1)=='begin': stack.append((name,m.start()))
        elif not stack: errors.append((m.start(),f'Unexpected end of {name}'))
        elif stack[-1][0]!=name: errors.append((m.start(),f'Expected end of {stack[-1][0]}, got {name}'))
        else: stack.pop()
    errors.extend((pos,f'Unclosed environment {name}') for name,pos in stack)
    return errors

def plain_text(s: str) -> str:
    s=re.sub(r'\\(?:url|href)\s*\{[^{}]*\}',' ',s)
    s=re.sub(r'\\[A-Za-z@]+\*?',' ',s)
    return re.sub(r'[{}$~]','',s)
