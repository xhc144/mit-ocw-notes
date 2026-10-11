#!/usr/bin/env python3
"""Record acquired statements, solved subparts and source theory separately."""
import json,hashlib,re
from pathlib import Path
root=Path(__file__).resolve().parents[1];repo=root.parents[1]
source=json.loads((repo/'manifests/electrodynamics-sources.json').read_text())
hw={1:[1,3,5,6,7],2:[1,2,3,4,5,7],3:[2,3,4],4:[2,3],5:[2,4],6:[4,6],7:[3,7],8:[5],9:[8],10:[3,7]}
counts=[7,7,5,6,5,6,7,7,8,7];grad_counts=[5,7,5,6,6,6,5,7,6,5,3,5]
entries=[];undergrad=[]
for n,total in enumerate(counts,1):
 for q in range(1,total+1):
  full=q in hw[n];partial=n==5 and q==5
  undergrad.append({'set':n,'problem':q,'source_id':f'mit8_07f12_pset{n:02d}','status':'中文题面及解答' if full else '仅(c)中文题面及解答' if partial else '缺完整教材题面或所依赖条件','translated_subparts':'all acquired self-contained subparts' if full else ['c'] if partial else [],'solution_identity':'AI independent; no official homework solution retrieved','chapter':12 if n<=5 else 13,'missing_statement':not(full or partial)})
for n,qs in hw.items():
 entries.append({'course':'8.07 Fall 2012','assessment':f'Problem Set {n}','translated_solved_items':qs+(['5(c)'] if n==5 else []),'chapter':12 if n<=5 else 13,'solution_identity':'AI independent','complete_numbered_groups':len(qs),'partial_groups':1 if n==5 else 0})
for title,n,ch,identity in [('Quiz 1',4,14,'Official solutions translated with explanations and erratum'),('Quiz 2',5,15,'Official solutions translated with explanations and coefficient erratum'),('Final',5,16,'AI independent; no official solution retrieved')]:
 entries.append({'course':'8.07 Fall 2012','assessment':title,'translated_solved_items':list(range(1,n+1)),'chapter':ch,'solution_identity':identity,'all_retrieved_subparts':True})
entries.append({'course':'8.311 Spring 2004','assessment':'Final','translated_solved_items':[1,2,3],'chapter':17,'solution_identity':'Official solutions translated with SI conversion and additions','all_retrieved_subparts':True})
graduate=[]
for n,total in enumerate(grad_counts,1):
 entries.append({'course':'8.311 Spring 2004','assessment':f'Problem Set {n}','translated_solved_items':list(range(1,total+1)),'chapter':17+n,'solution_identity':'AI independent derivation; compared with official results where available','matching_official_solution_retrieved':n!=7,'all_acquired_subparts_written':True,'unavailable_comparison':'PS11 Q3 textbook Figure 34.4 not acquired' if n==11 else None})
 for q in range(1,total+1):
  graduate.append({'set':n,'problem':q,'chapter':17+n,'status':'中文题面、推导和解答已写','solution_identity':'AI independent, not MIT official Chinese','limitation':'教材Figure34.4未取得；已自绘角型，未作实图比对' if(n,q)==(11,3) else None})
topics=[
([1,12],'矢量微分、积分定理、分量记号'),([1,12],'转动矩阵、指标变换、正交与Levi-Civita'),
([1,2,12],'场方程积分形式、点源分布、内边界'),([2,12,18],'导体表面压力、电容矩阵、场能'),
([3,12,20,23],'镜像、唯一性、矩形分离变量'),([3,12,23],'球坐标径向/角向方程、边界投影'),
([3],'圆孔球壳内外势、面荷跳跃和Legendre积分'),([3,4,12],'STF、多极展开、球谐表示和低阶去迹'),
([3,4,12],'Legendre与球谐、Y31/Yll归一和P4'),([6,19],'电流矩、磁矩二分之一、偶极势及场'),
([5,6,13,19],'極化/磁化体面源、退磁场、磁化球柱'),([11],'负ε/μ频带、相位与能流、反向切伦科夫'),
([11],'超材料反向辐射的相位与能流解释、保留作者署名'),([9,20,21,22],'相量、平均能流、偏振、Fresnel与趋肤'),
([7,27],'规范、推迟格林解、LW根雅可比及完整求导'),([10,27,28,29],'电磁偶极、三阶场、辐射角分布和功率'),
([7,9,10,16],'波、势及辐射复习内容由自写推导整合')]
advanced={'wave_guides':([9,23],'TE/TM纵场、横场重建、导体边界、截止及TEM'),'field_osc':([11,23,24],'横势模态、归一、场L/H、带源作用量与库仑项消元、一般受迫模态因果卷积、等能与正交'),'power_spec':([10,29],'正频单边角谱、速度软因子、有限τ与sinc截止'),'charge_mov':([11,29],'场振子共振、Frank–Tamm、碰撞软谱及红外入口')}
theory=[]
for f in source['files']:
 if f['kind']=='lecture-notes':
  ch,t=topics[int(f['id'].split('_ln')[-1])-1] if f['id'].startswith('mit8_07') else advanced[f['id']]
  theory.append({'source_id':f['id'],'title':f['title'],'url':f['url'],'pages':f['pages'],'source_archived':f['archive_allowed'],'chapters':ch,'written_topics':t,'status':'核心主题中文重编与推导','boundary':'研究型实验/设计幻灯片与第三方图片未逐页复制' if f['id'] in ['mit8_07f12_ln12','mit8_07f12_ln13'] else '原件有第三方例外，数学自写；整件不打包' if not f['archive_allowed'] else '按主题重编，非逐页逐字翻译'})
chapters=[]
for p in sorted((root/'chapters').glob('*.tex')):
 s=p.read_text();title=re.search(r'\\originalchapter\{([^}]+)',s).group(1)
 chapters.append({'path':str(p.relative_to(repo)),'title':title,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'assessment_units':s.count('\\begin{exercise}')})
record={'schema_version':2,'date':'2026-10-11','release_scope':'电动力学中文重编扩充版；本科主线、取得自含题面的考核及8.311十二套作业合订','source_pdf_archived':sum(f['archive_allowed'] for f in source['files']),'source_pages_archived':sum(f['pages'] for f in source['files'] if f['archive_allowed']),'source_pdf_withheld':[{k:f[k] for k in ['id','url','pages','sha256','third_party_exception']} for f in source['files'] if not f['archive_allowed']],'chapters':chapters,'theory_source_topic_map':theory,'assessments':entries,'undergraduate_homework_all_numbered_groups':undergrad,'graduate_homework_all_numbered_groups':graduate,'solved_assessment_units':sum(len(e['translated_solved_items']) for e in entries),'counts':{'undergraduate_numbered_homework_groups':65,'undergraduate_complete_groups':26,'undergraduate_partial_groups':1,'undergraduate_missing_whole_statements_or_conditions':38,'quiz_questions':9,'undergraduate_final_questions':5,'advanced_final_questions':3,'graduate_homework_sets_written':12,'graduate_homework_groups_written':66},'advanced_assignments':{'downloaded':12,'official_solution_filename_count':12,'matching_sets_with_official_solution':11,'translated':12,'solved_numbered_groups':66,'mismatch':'solution7.pdf contains PS8, not PS7','solution_identity':'AI independent with official comparison, not official Chinese translation'},'proof_boundaries':['8.311全课历不等于四份补充笔记；Noether、完整协变作用量、辐射反作用与同步辐射全套理论未建立','KK基本复分析定理与相对论Liénard总功率为明示工具，后续和规则及应用已推导','8.312尚未找到可核官方原件','天线教材Fig.34.4缺失，保留实图比对边界'],'review_evidence':['qa/field-oscillator-closure-review.md','qa/revision-second-review.md','qa/graduate-review-1-3.md','qa/graduate-review-4-6.md','qa/graduate-review-7-9.md','qa/graduate-review-10-12.md'],'license':'CC BY-NC-SA 4.0; individual MIT OCW attribution and third-party exceptions retained'}
assert sum(grad_counts)==66 and len(undergrad)==65 and record['solved_assessment_units']==110 and sum(c['assessment_units'] for c in chapters)==110
(root/'coverage.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
lines=['# 中文覆盖与未取得项目','','当前29章、110个考核题解单元：本科作业26道完整一级题、1道仅(c)，Quiz9题、本科期末5题；研究生期末3题及十二套作业66道一级题。110不是110道全子问完整原题，缺失仍按下表保留。','','61份原件474页已校验归档。12个命名的研究生官方解答文件仅匹配11套，solution7实为PS8；PS7独立解答。研究生题解均标AI独立推导，官方缺解与勘误在题旁说明。','','## 理论逐文件、逐主题对应','','| 原件 | 已写章 | 核心主题 | 边界 |','|---|---|---|---|']
for e in theory:lines.append('| '+e['source_id']+' | '+','.join(map(str,e['chapters']))+' | '+e['written_topics']+' | '+e['boundary']+' |')
lines+=['','## 本科作业全部编号（包括延后/重复引用）','','| 原题 | 中文状态 | 对应章 |','|---|---|---|']
for e in undergrad:lines.append(f"| PS{e['set']} Q{e['problem']} | {e['status']} | {e['chapter'] if not e['missing_statement'] else '—'} |")
lines+=['','## 研究生十二套全部一级题','','| 原作业 | 已写题号 | 对应章 | 限制 |','|---|---|---|---|']
for n,count in enumerate(grad_counts,1):lines.append(f"| PS{n} | "+', '.join(map(str,range(1,count+1)))+f" | {17+n} | "+('未取得匹配官方解，全部独算' if n==7 else 'Q3已自绘；缺教材Fig.34.4，无法实图比对' if n==11 else '模型条件与原题/官方解勘误在题旁说明')+' |')
lines+=['','## 尚未取得或未完整证明','','- 本科38道编号组缺完整商业教材题面或依赖条件；PS5 Q5只有(c)，(a)(b)保留缺失。PS7 Q5追加(d)依赖未取得的参数Q。题号不是取得教材或复制许可。','- 第15讲有明确YouTube例外，第17讲含商业教材扫描页，整件不打包。8.312未找到可核官方原件。','- 已取得的理论核心主题均有中文计算位置；研究型超材料幻灯片不逐页译写，第三方实验图不复制。','- 8.311全课历中的Noether、完整协变作用量、辐射反作用、同步辐射不能由四份补充笔记冒称全课完成。','- 天线教材Fig.34.4未随题面提供，已有自绘角型但不能声称完成实图比对。','- 数学/物理独立审查、编译、结构链接与实际视觉证据分开，另见qa/release.json。']
(root/'coverage.md').write_text('\n'.join(lines)+'\n')
print(json.dumps(record['counts'],ensure_ascii=False))
