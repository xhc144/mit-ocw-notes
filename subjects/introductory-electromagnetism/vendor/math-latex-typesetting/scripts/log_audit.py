#!/usr/bin/env python3
"""Read the FINAL log; distinguish hard failures from layout review hints."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path

def audit(log: str,overflow_tolerance_pt: float=.5) -> dict:
    issues=[]; warnings=[]
    for m in re.finditer(r'Overfull \\[hv]box \(([\d.]+)pt (?:too wide|too high)\)[^\n]*',log):
        (issues if float(m.group(1))>overflow_tolerance_pt else warnings).append(m.group(0))
    for pattern in [r'Missing character:[^\n]*',r'(?:LaTeX|Package [^\n]+) Warning:[^\n]*undefined[^\n]*',
                    r'LaTeX Warning: There were undefined references[^\n]*',r'LaTeX Warning: Label [^\n]*multiply defined[^\n]*',
                    r'LaTeX Warning: There were multiply-defined labels[^\n]*',r'^! [^\n]+',r'Cannot patch proof[^\n]*']:
        issues.extend(m.group(0) for m in re.finditer(pattern,log,re.M))
    for pattern in [r'Underfull \\[hv]box[^\n]*',r'LaTeX Font Warning:[^\n]*',r'Package fontspec Warning:[^\n]*',
                    r'Label\(s\) may have changed[^\n]*',r'Package rerunfilecheck Warning:[^\n]*',r'Package hyperref Warning:[^\n]*']:
        warnings.extend(m.group(0) for m in re.finditer(pattern,log))
    return {'issues':list(dict.fromkeys(issues)),'warnings':list(dict.fromkeys(warnings))}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('log',type=Path); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
    try: r=audit(a.log.read_text(encoding='utf-8',errors='replace'))
    except OSError as exc: print('INPUT ERROR:',exc); return 2
    print(json.dumps(r,ensure_ascii=False,indent=2)); return int(bool(r['issues']))
if __name__=='__main__': raise SystemExit(main())
