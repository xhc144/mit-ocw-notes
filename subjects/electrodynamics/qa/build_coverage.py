#!/usr/bin/env python3
"""Create an explicit coverage record; do not infer completion from downloads."""
import json,hashlib,re
from pathlib import Path
root=Path(__file__).resolve().parents[1];repo=root.parents[1]
source=json.loads((repo/'manifests/electrodynamics-sources.json').read_text())
hw={1:['1','3','5','6','7'],2:['1','2','3','4','5','7'],3:['2','3','4'],4:['2','3'],5:['2','4','5(c)'],6:['4','6'],7:['3','7'],8:['5'],9:['8'],10:['3','7']}
missing={1:['Griffiths 1.2, 1.6, 1.12, 1.13(a)'],2:['Griffiths 2.48'],3:['Griffiths 3.8, 3.15'],4:['Griffiths 3.15, 3.20, 3.22, 3.41'],5:['Griffiths 3.22, 3.45, 3.42(a)-(b)'],6:['Griffiths 4.2, 4.16, 4.32; Jackson 4.10'],7:['Griffiths 5.3, 5.8, 5.24, 5.58, 5.43; 5(d) depends on unspecified Q'],8:['Griffiths 5.58, 5.37, 5.49, 6.5, 6.17, 6.25'],9:['Griffiths 7.8, 7.20, 7.42, 7.49, 7.58, 7.59, 8.1'],10:['Griffiths 8.4, 8.6, 9.10, 9.12, 9.13']}
entries=[]
for n,probs in hw.items():
 entries.append({'course':'8.07 Fall 2012','assessment':f'Problem Set {n}','source_id':f'mit8_07f12_pset{n:02d}','translated_solved_items':probs,'chapter':'12-assignments-a' if n<=5 else '13-assignments-b','solution_identity':'AI independent; no official solutions retrieved','missing_or_incomplete_statements':missing[n]})
for title,n,ch,identity in [('Quiz 1',4,'14-quiz1','Official solutions translated with added explanation and erratum'),('Quiz 2',5,'15-quiz2','Official solutions translated with added explanation and coefficient erratum'),('Final',5,'16-final','AI independent; no official solutions retrieved')]:
 entries.append({'course':'8.07 Fall 2012','assessment':title,'translated_solved_items':list(range(1,n+1)),'chapter':ch,'solution_identity':identity,'all_retrieved_exam_questions_and_subparts':True})
entries.append({'course':'8.311 Spring 2004','assessment':'Final','translated_solved_items':[1,2,3],'chapter':'17-advanced-assessments','solution_identity':'Official solutions translated, with Gaussian-to-SI conversion and explanatory additions','all_retrieved_exam_questions_and_subparts':True})
chapters=[]
for p in sorted((root/'chapters').glob('*.tex')):
 s=p.read_text();title=re.search(r'\\originalchapter\{([^}]+)',s).group(1)
 chapters.append({'path':str(p.relative_to(repo)),'title':title,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'assessment_units':s.count('\\begin{exercise}')})
record={'schema_version':1,'date':'2026-10-11','release_scope':'本科电动力学中文重编第一版, 含已取得自含题面的解答; 进阶理论为选讲','source_pdf_archived':sum(f['archive_allowed'] for f in source['files']),'source_pages_archived':sum(f['pages'] for f in source['files'] if f['archive_allowed']),'source_pdf_withheld':[{k:f[k] for k in ['id','url','pages','sha256','third_party_exception']} for f in source['files'] if not f['archive_allowed']],'chapters':chapters,'assessments':entries,'solved_assessment_units':sum(len(e['translated_solved_items']) for e in entries),'advanced_assignments':{'downloaded':12,'official_solution_files_downloaded':12,'translated':0,'status':'原件和官方解答已归档; 尚未逐题中文重编'},'proof_boundaries':['Kramers–Kronig 引用关系, 非零起点完整复分析证明','Liènard 总功率引用, 未完成相对论角积分推导','协变理论仅入口; Noether、辐射反作用、同步辐射不称完整展开'],'review_evidence':['qa/source-review.md','qa/theory-review.md','qa/assessment-review.md','qa/revision-review.md'],'license':'CC BY-NC-SA 4.0 for Chinese reworking; retain MIT OCW individual attribution and exceptions'}
assert record['solved_assessment_units']==44
(root/'coverage.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
lines=['# 中文覆盖清单','',record['release_scope']+'。下载状态与中文写作状态分别记录。','',f"实际归档 {record['source_pdf_archived']} 份原件、{record['source_pages_archived']} 页；中文稿17章，考核44项（本科作业27项、Quiz9题、本科期末5题、进阶期末3题）。",'','| 来源 | 已写题目 | 身份 | 尚缺的题面 |','|---|---|---|---|']
for e in entries:
 lines.append('| '+e['course']+' '+e['assessment']+' | '+', '.join(map(str,e['translated_solved_items']))+' | '+e['solution_identity']+' | '+'; '.join(e.get('missing_or_incomplete_statements',[]))+' |')
lines+=['','研究生12套作业题面与官方解答已归档，逐题中文重编为0套。理论选讲不等同于完整8.311。8.312未定位到可核验官方原件。','', '第15讲原件含明确YouTube许可例外，第17讲含商业教材扫描页，整件暂不打包；可自行重述的数学内容不使用这些第三方图片。','', '证明边界：']+['- '+v for v in record['proof_boundaries']]
(root/'coverage.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'archived':record['source_pdf_archived'],'pages':record['source_pages_archived'],'assessment_units':record['solved_assessment_units']}))
