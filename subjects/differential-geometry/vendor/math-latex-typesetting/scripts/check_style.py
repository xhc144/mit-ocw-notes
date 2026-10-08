#!/usr/bin/env python3
"""Compare the authorized template and detect direct style overrides."""
from __future__ import annotations
import argparse
from pathlib import Path
import re
from tex_scan import mask_noncode
from tex_project import expand_project
START,END='% WZ-LOCKED-CLASS-BEGIN','% WZ-LOCKED-CLASS-END'
ROOT=Path(__file__).resolve().parents[1]
PROTECTED='theorem|lemma|proposition|corollary|definition|example|exercise|proof|solution|remark'

def locked(s: str) -> str:
    if s.count(START)!=1 or s.count(END)!=1 or s.index(START)>s.index(END):
        raise ValueError('锁定区标记必须各出现一次且次序正确')
    return s.split(START,1)[1].split(END,1)[0].replace('\r\n','\n')

def check(text: str,golden: str|None=None) -> list[str]:
    golden=golden if golden is not None else (ROOT/'templates/wangzhe_baiti_style.tex').read_text(encoding='utf-8-sig')
    errors=[]
    try:
        if locked(text)!=locked(golden): errors.append('固定类与所选授权模板不一致；不能修改字体/环境/间距来伪造通过。')
    except ValueError as exc: return [str(exc)]
    outside=mask_noncode(text.split(START,1)[0]+text.split(END,1)[1])
    if not re.search(r'\\documentclass\s*\{elegantbook-original-adapter\}',outside): errors.append('主文档没有使用所选固定适配类。')
    patterns=[
        (r'\\(?:newenvironment|renewenvironment|NewDocumentEnvironment|RenewDocumentEnvironment)\s*\{(?:'+PROTECTED+r')\}', '内容区重复定义固定数学环境。'),
        (r'\\newtheorem\*?\s*\{(?:'+PROTECTED+r')\}', '内容区重复注册固定数学环境。'),
        (r'\\(?:geometry|newgeometry|setstretch|linespread|setmainfont|setsansfont|setmonofont|setCJKmainfont|setCJKsansfont|setCJKmonofont|setCJKfamilyfont)\b','内容区覆盖固定页面、行距或字体。'),
        (r'\\(?:usepackage|RequirePackage)(?:\s*\[[^]]*\])?\s*\{[^}]*\b(?:tcolorbox|mdframed|titlesec|ntheorem)\b','加载冲突的样式宏包。'),
        (r'\\hypersetup\s*\{[^}]*(?:linkcolor|urlcolor|citecolor)','覆盖固定链接颜色。'),
        (r'\\(?:renewcommand|def|let)\s*\{?\\(?:proof|endproof|qed|qedsymbol|originalchapter|originalsection)\b','覆盖固定证明/章节/QED 命令。'),
        (r'\\setlength\s*\{\\(?:parskip|parindent|textwidth|textheight|baselineskip|abovedisplayskip|belowdisplayskip)\}','内容区改变固定长度。'),
        (r'\\(?:hbadness|vbadness|hfuzz|vfuzz)\s*(?:=|\d)','内容区更改告警阈值，可能隐藏实际布局问题。')]
    for pattern,message in patterns:
        if re.search(pattern,outside,re.S): errors.append(message)
    return errors

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('file',type=Path); ap.add_argument('--template',type=Path)
    a=ap.parse_args()
    try: result=check(expand_project(a.file).text,a.template.read_text(encoding='utf-8-sig') if a.template else None)
    except (OSError,ValueError) as exc: print('INPUT ERROR:',exc); return 2
    for x in result: print('ERROR:',x)
    if not result: print('Template checks passed; semantic and visual review remain separate.')
    return int(bool(result))
if __name__=='__main__': raise SystemExit(main())
