#!/usr/bin/env python3
"""Project-aware typesetting checks. Automatic checks never certify content quality."""
from __future__ import annotations
import argparse
from dataclasses import asdict
from pathlib import Path
import json
from build_utils import build,write_json,sha256
from tex_project import expand_project
from check_style import check
from content_style_lint import lint
from log_audit import audit as audit_log
from validation_policy import load_policy,annotate_warnings

def validate(tex: Path,out: Path,template: Path|None=None,policy_path: Path|None=None,
             measure_inline: bool=False,timeout: int=120) -> dict:
    tex=tex.resolve(); out=out.resolve(); out.mkdir(parents=True,exist_ok=True)
    report={'schema_version':2,'source':str(tex),'automated_status':'FAIL',
            'mathematical_verification':False,'pedagogy_assessed':False,'visual_review':'not_performed',
            'errors':[],'warnings':[],'stages':{}}
    try:
        policy=load_policy(policy_path); report['policy']=policy
        p=expand_project(tex)
        report['sources']=[{'path':x.relative_to(p.root).as_posix(),'sha256':sha256(x)} for x in p.files]
        style=check(p.text,template.read_text(encoding='utf-8-sig') if template else None)
        found,metrics=lint(p.text,policy['title_soft_limit']); rows=[]
        for f in found:
            row=asdict(f); row['file'],row['line']=p.location(f.line); rows.append(row)
        report['warnings']+=annotate_warnings(rows,policy,p.root)
        report['layout_source']={'findings':rows,'metrics':metrics,'style_errors':style}
        report['errors']+=style+[f"{x['file']}:{x['line']} {x['kind']}: {x['detail']}" for x in rows if x['level']=='ERROR']
        report['warnings']+=[f"{x['file']}:{x['line']} {x['kind']}: {x['detail']}" for x in rows if x['level']=='WARNING']
        report['stages']['source']='failed' if report['errors'] else 'passed'
        if report['errors']: return report
        built=build(tex,out,timeout=timeout)
        report['stages']['compile']='passed'; report['build_record']=str(Path(built['build_record']).relative_to(p.root)) if Path(built['build_record']).is_relative_to(p.root) else built['build_record']
        report['pdf_path']=built['pdf']; report['passes']=built['record']['passes']
        report['warnings']+=built['record'].get('guard_warnings',[])
        report['log']=audit_log(built['log'],policy['overflow_tolerance_pt'])
        from wangzhe_pdf_audit import audit as audit_pdf
        report['pdf']=audit_pdf(Path(built['pdf']),tuple(policy['page_size']))
        for stage in ('log','pdf'):
            report['errors'] += [stage+': '+x for x in report[stage]['issues']]
            report['warnings'] += [stage+': '+x for x in report[stage]['warnings']]
            report['stages'][stage]='failed' if report[stage]['issues'] else 'passed'
        if measure_inline:
            from measure_inline import measure
            report['inline']=measure(tex,limit=policy['inline_warning_ratio'],timeout=timeout)
            report['warnings']+=report['inline']['warnings']; report['stages']['inline_diagnostic']=report['inline']['status']
        else: report['stages']['inline_diagnostic']='not_requested; log and page review remain required'
        from pdf_artifacts import render_pdf
        rendered=render_pdf(Path(built['pdf']),root=p.root)
        report['render_record']=str(rendered.relative_to(p.root)) if rendered.is_relative_to(p.root) else str(rendered)
        report['stages']['render']='generated_not_inspected'
        report['automated_status']='PASS' if not report['errors'] else 'FAIL'
    except (OSError,ValueError,RuntimeError,ImportError) as exc:
        report['errors'].append(str(exc)); report['failure_type']=type(exc).__name__
    finally:
        write_json(out/'validation_report.json',report)
    return report

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('file',type=Path); ap.add_argument('--out',type=Path,default=Path('build'))
    ap.add_argument('--template',type=Path); ap.add_argument('--policy',type=Path); ap.add_argument('--measure-inline',action='store_true')
    ap.add_argument('--timeout',type=int,default=120); a=ap.parse_args()
    out=a.out if a.out.is_absolute() else a.file.resolve().parent/a.out
    report=validate(a.file,out,a.template,a.policy,a.measure_inline,a.timeout)
    for x in report['errors']: print('ERROR:',x)
    for x in report['warnings']: print('REVIEW:',x)
    print('AUTOMATED '+report['automated_status']+'; mathematical/teaching quality not assessed; visual review not performed.')
    if report.get('pdf_path'): print('PDF:',report['pdf_path'])
    print('REPORT:',out/'validation_report.json')
    return 0 if report['automated_status']=='PASS' else (2 if report.get('failure_type') in {'FileNotFoundError','ProjectError','ImportError','ModuleNotFoundError'} else 1)

if __name__=='__main__': raise SystemExit(main())
