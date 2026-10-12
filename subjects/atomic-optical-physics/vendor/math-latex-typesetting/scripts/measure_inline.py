#!/usr/bin/env python3
"""Optional physical-width diagnostic. Unmeasurable is NOT incorrect."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from build_utils import build
from tex_project import expand_project
from tex_scan import document_body,inline_math,mask_noncode

MEASURE_MACRO=r'''
\newsavebox{\WZmeasurebox}
\newlength{\WZmeasureheight}
\DeclareRobustCommand{\WZmeasureinline}[2]{%
  \begingroup
  \sbox{\WZmeasurebox}{#2}%
  \WZmeasureheight=\ht\WZmeasurebox\advance\WZmeasureheight by\dp\WZmeasurebox
  \typeout{WZMEASURE|#1|\the\wd\WZmeasurebox|\the\WZmeasureheight|\the\linewidth|\the\baselineskip}%
  \endgroup#2%
}
'''

def instrument(text: str) -> tuple[str,list[dict]]:
    body,offset=document_body(text); spans=inline_math(body); rows=[]
    for i,sp in enumerate(spans,1):
        row={'id':i,'line':text.count('\n',0,offset+sp.start)+1,'source':sp.content.strip(),
             'start':offset+sp.start,'end':offset+sp.end}
        if re.search(r'\\(?:label|tag|write|refstepcounter|stepcounter|addtocounter|footnote|index|glossary)\b',sp.content):
            row['skipped']='Potential side effect; inspect the original formula without double evaluation.'
        rows.append(row)
    result=text
    for row in reversed(rows):
        if row.get('skipped'): continue
        result=result[:row['start']]+'\\WZmeasureinline{'+str(row['id'])+'}{'+text[row['start']:row['end']]+'}'+result[row['end']:]
    m=re.search(r'\\begin\s*\{document\}',mask_noncode(result))
    if not m: raise ValueError('Measurement needs a full document, not a fragment.')
    result=result[:m.start()]+MEASURE_MACRO+'\n'+result[m.start():]
    return result,rows

def measure(tex: Path,limit: float=.50,timeout: int=120) -> dict:
    if not 0<limit<=1: raise ValueError('Diagnostic ratio must be in (0,1].')
    project=expand_project(tex); instrumented,rows=instrument(project.text)
    warnings=[]; data={}
    if any(not x.get('skipped') for x in rows):
        try:
            result=build(tex,replacement=instrumented,passes=2,timeout=timeout)
            pattern=r'WZMEASURE\|(\d+)\|([\d.]+)pt\|([\d.]+)pt\|([\d.]+)pt\|([\d.]+)pt'
            for m in re.finditer(pattern,result['log']):
                i=int(m.group(1)); w,h,width,baseline=map(float,m.groups()[1:])
                value={'width_pt':w,'height_pt':h,'linewidth_pt':width,'baseline_pt':baseline,
                       'width_ratio':w/width if width else None}
                if i not in data or (value['width_ratio'] or 0)>(data[i]['width_ratio'] or 0): data[i]=value
        except (OSError,ValueError,RuntimeError) as exc:
            warnings.append('Diagnostic build unavailable; original build remains authoritative: '+str(exc)[-1000:])
    output=[]
    for row in rows:
        record={k:v for k,v in row.items() if k not in {'start','end'}}
        record['file'],record['line']=project.location(row['line'])
        where=f"{record['file']}:{record['line']}"
        if row['id'] in data:
            record.update(data[row['id']]); record['status']='measured'
            if record['width_ratio'] is None: warnings.append(where+': local line width could not be measured.')
            elif record['width_ratio']>limit:
                warnings.append(f"{where}: natural formula width is {record['width_ratio']:.1%} of local line width; review actual wrapping, not an automatic error.")
            if record['baseline_pt'] and record['height_pt']>1.5*record['baseline_pt']:
                warnings.append(where+': possible line-height expansion; inspect the page.')
        else:
            record['status']='unmeasured'
            record.setdefault('skipped','No execution record: unused branch/macro or unsupported instrumentation.')
            warnings.append(where+': '+record['skipped'])
        output.append(record)
    return {'status':'complete' if len(data)==len(rows) else 'partial','measured':len(data),
            'total_static_spans':len(rows),'issues':[],'warnings':warnings,'formulas':output,
            'limitation':'Ordinary static spans only; macro-generated formula coverage is not certified.'}

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('file',type=Path); ap.add_argument('--json',action='store_true')
    ap.add_argument('--report',type=Path); ap.add_argument('--timeout',type=int,default=120); a=ap.parse_args()
    try: r=measure(a.file,timeout=a.timeout)
    except (OSError,ValueError) as exc: print('INPUT ERROR:',exc); return 2
    payload=json.dumps(r,ensure_ascii=False,indent=2); print(payload)
    if a.report: a.report.parent.mkdir(parents=True,exist_ok=True); a.report.write_text(payload+'\n',encoding='utf-8')
    return 0
if __name__=='__main__': raise SystemExit(main())
