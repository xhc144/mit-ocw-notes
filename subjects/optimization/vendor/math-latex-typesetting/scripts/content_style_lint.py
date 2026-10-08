#!/usr/bin/env python3
"""Layout-only lint: no prose blacklist, theorem-depth quota or AI detector."""
from __future__ import annotations
import argparse
from dataclasses import dataclass,asdict
import json
from pathlib import Path
import re
import unicodedata
from tex_scan import document_body,commands,inline_math,environment_spans,environment_errors,plain_text
from tex_project import expand_project

@dataclass
class Finding:
    level:str
    kind:str
    line:int
    detail:str

NUMBERED={'theorem','lemma','proposition','corollary','definition','example','exercise'}

def title_width(s: str) -> float:
    return sum(1 if unicodedata.east_asian_width(c) in 'WF' else .5 for c in s if not c.isspace())

def lint(text: str,title_soft_limit: float=20) -> tuple[list[Finding],dict]:
    body,offset=document_body(text); findings=[]
    def add(kind,detail,pos=0,level='WARNING'):
        findings.append(Finding(level,kind,text.count('\n',0,offset+pos)+1,detail))
    headings=list(commands(body,('originalchapter','originalsection','chapter','section','subsection','subsubsection','paragraph','subparagraph')))
    for name,title,pos,_ in headings:
        readable=plain_text(title).strip()
        if not readable: add('empty-title','标题为空，请补实际标题或移除此空标题。',pos,'ERROR')
        if name not in {'originalchapter','originalsection'}:
            add('heading-style','该标题不使用默认章/节宏；核对是否为授权扩展，而非临时换样式。',pos)
        if title_width(readable)>title_soft_limit:
            add('title-length-review','标题较长，仅需检查清晰度与换行；不能删必要限定或伪造缩写。',pos)
    for m in re.finditer(r'\\begin\s*\{(?:example|exercise)\}\s*\[',body):
        add('problem-title','默认题目环境不显示可选题名。核对原题/用户要求；不要静默丢失内容。',m.start(),'ERROR')
    for m in re.finditer(r'\\original(?:example|solution)\b',body):
        add('legacy-environment','已废止的题目宏，改用对应固定环境以避免手工编号。',m.start(),'ERROR')
    for m in re.finditer(r'\\textbf\s*\{\s*(?:引理|定理|证明|解答|例题|习题)(?:\s|\d|[:：}])',body):
        add('manual-label-review','可能在手打数学标签；引用或讲解标签本身时无需删除。',m.start())
    for m in re.finditer(r'\\begin\s*\{(?:tcolorbox|mdframed)\}',body):
        add('decorative-box','固定版式不使用装饰框，证毕符号和 minipage 不在此列。',m.start(),'ERROR')
    for m in re.finditer(r'\$\$|\\begin\s*\{eqnarray\*?\}',body):
        add('legacy-display','建议使用 amsmath 显示环境，检查现有间距和编号。',m.start())
    for m in re.finditer(r'\\(?:resizebox|scalebox)\b',body):
        add('scale-review','检查被缩放的是图表还是正文公式；合法图形缩放无需返工。',m.start())
    try: spans=inline_math(body)
    except ValueError as exc: add('math-delimiter',str(exc),0,'ERROR'); spans=[]
    for sp in spans:
        if re.search(r'\\(?:displaystyle|dfrac)\b|\\begin\s*\{(?:aligned|cases|[pbBvV]?matrix)\}',sp.content):
            add('inline-height-review','此行内式可能撑高行距，结合实际页面判断是否改为行间。',sp.start)
    for pos,message in environment_errors(body): add('environment-balance',message,pos,'ERROR')
    first=body.find('\\originalchapter')
    envs=list(environment_spans(body,NUMBERED|{'proof','solution'}))
    for name,start,cs,ce,_ in envs:
        inner=body[cs:ce]
        if name in NUMBERED and (first<0 or start<first):
            add('chapter-number-review','带章编号的环境出现在默认首章之前；检查实际计数器，不推测内容是否该删。',start)
        if name in {'proof','solution'}:
            if not re.sub(r'\\label\s*\{[^}]*\}|\s','',inner):
                add('empty-proof','空 proof/solution 会输出证毕符号；由内容作者补齐或移除空环境。',start,'ERROR')
            if re.search(r'\\qed\b|\\hfill\s*(?:\$|\\\().*?\\(?:square|Box)\b',inner,re.S):
                add('manual-qed-review','可能与自动证毕符号重复；检查语境和最终页面。',start)
            if re.search(r'(?:\\\]|\\end\s*\{(?:equation\*?|align\*?|gather\*?|multline\*?|enumerate|itemize)\})\s*$',inner) and '\\qedhere' not in inner:
                add('qed-placement-review','证明以公式/列表结束；查看 QED 是否正常，不自动要求增加收尾文字。',start)
        if name in {'example','exercise'} and re.search(r'\\begin\s*\{solution\}',inner):
            add('solution-in-question','题面与解答环境嵌套，需区分呈现边界，不删解答内容。',start,'ERROR')
    return findings,{'heading_count':len(headings),'inline_math_count':len(spans),
        'proof_count':sum(e[0]=='proof' for e in envs),'solution_count':sum(e[0]=='solution' for e in envs),
        'content_depth_assessed':False}

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('file',type=Path); ap.add_argument('--json',action='store_true')
    a=ap.parse_args()
    try:
        project=expand_project(a.file); found,metrics=lint(project.text)
        rows=[]
        for f in found:
            row=asdict(f); row['file'],row['line']=project.location(f.line); rows.append(row)
    except (OSError,ValueError) as exc: print('INPUT ERROR:',exc); return 2
    if a.json: print(json.dumps({'metrics':metrics,'findings':rows},ensure_ascii=False,indent=2))
    else:
        for f in rows: print(f"{f['level']} {f['file']}:{f['line']} {f['kind']}: {f['detail']}")
        if not rows: print('No listed layout problems found; content was not evaluated.')
    return int(any(f.level=='ERROR' for f in found))

if __name__=='__main__': raise SystemExit(main())
