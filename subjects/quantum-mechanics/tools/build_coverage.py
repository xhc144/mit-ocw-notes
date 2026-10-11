#!/usr/bin/env python3
"""Generate honest chapter/source and assessment coverage; preserve source metadata."""
import json,re,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[3]
SUB=ROOT/'subjects/quantum-mechanics'
mp=ROOT/'manifests/quantum-mechanics-sources.json'
m=json.loads(mp.read_text())
for r in m['resources']:
    p=r.get('text_path')
    if p and (ROOT/p).is_file():
        t=(ROOT/p).read_text()
        contributors=[]
        for name in ('Sarah Geller','Andrew Turner'):
            if re.search(name+r'.{0,90}transcribed|transcribed.{0,90}'+name,t,re.S):contributors.append(name)
        if contributors:
            r['author']='Barton Zwiebach (lecture notes); '+', '.join(contributors)+' (first LaTeX transcription)'
            r['contributors']=contributors
            r['attribution']='MIT OpenCourseWare; Barton Zwiebach; '+', '.join(contributors)
        else:r['contributors']=[]
mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
mapping=[('8.04',[1,2,3,4]),('8.04',[5,6]),('8.04',[5,6]),('8.04',[7,8,9]),('8.04',[10,11]),('8.04',[16,17]),('8.04',[7,'14_15']),('8.05',[4,5,6]),('8.05',[2,7]),('8.05',[9,10]),('8.04',[22]),('8.05',[8]),('8.06',[1]),('8.06',[1,2]),('8.06',[6]),('8.06',[3,7])]
def match(c,n):
    pattern={'8.04':f'LecNotes{n}.pdf','8.05':f'Chap_{n:02}.pdf','8.06':f'ch{n}.pdf'}[c] if isinstance(n,int) else f'LecNotes{n}.pdf'
    return next(r for r in m['resources'] if r['course']==c and r.get('path','').endswith(pattern))
chapters=[]
for i,(course,nums) in enumerate(mapping,1):
    p=SUB/f'chapters/ch{i:02}.tex';title=re.search(r'\\originalchapter\{([^}]+)\}',p.read_text())[1]
    rs=[match(course,n) for n in nums]
    chapters.append({'number':i,'title':title,'file':str(p.relative_to(ROOT)),'status':'written_independent_review_completed','source_resources':[r['resource_page_url'] for r in rs],
       'scope':'Selected foundational concepts and derivations; not a complete translation of all listed source pages.',
       'original_additions':True})
selected={'MIT8_04S16_ps1_2016.pdf':('chapters/assessment-ps1.tex',7),'MIT8_04S16_Test1_Fall2015.pdf':('chapters/assessment-test1.tex',5),'MIT8_05F13_ps6.pdf':('chapters/assessment-ps6.tex',6),'MIT8_06S18ps1.pdf':('chapters/assessment-advanced-ps1.tex',5)}
assess=[]
for r in m['resources']:
    if r['category'] not in ['assignments','exams'] or 'duplicate_of' in r:continue
    name=pathlib.Path(r.get('path',r.get('download_path_not_distributed'))).name[33:]
    sel=selected.get(name)
    status='full_chinese_statement_and_independent_solution' if sel else ('withheld_rights_or_textbook_dependency' if not r.get('retained_in_repository') else ('formula_sheet_archived' if 'Formula Sheet' in r['title'] else 'original_archived_chinese_solution_pending'))
    assess.append({'course':r['course'],'title':r['title'],'hosting_term':r['term'],'document_term':r['document_term'],'source_url':r['url'],'resource_url':r['resource_page_url'],'sha256':r['sha256'],'retained_original':r['retained_in_repository'],'status':status,'chinese_file':'subjects/quantum-mechanics/'+sel[0] if sel else None,'question_count':sel[1] if sel else None,'all_subparts_in_selected_document':bool(sel),'solution_author':'AI independent' if sel else None,'official_solution_received':False})
out={'schema_version':1,'date':'2026-10-11','edition':'First substantive Chinese installment; further source and assessment expansion pending','chinese_core_chapters':chapters,'assessments':assess,'fully_solved_assessment_documents':4,'fully_solved_main_questions':23,
'pending_topics':['8.04 complete shooting method, node theorem, delta potentials, resonance and Levinson theorem','8.05 complete time pictures, tensor products and angular-momentum coupling exercises','8.06 full relativistic/Darwin fine-structure derivation, charged particles, complete Airy connection proof, scattering detail and identical-particle applications','Remaining retained assignments, tests and final exams listed individually above'],
'unavailable_or_withheld_sources':m['known_gaps'],'independent_solution_notice':'All Chinese assessment solutions are AI independent; no official solutions obtained for selected courses.'}
(SUB/'coverage.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
def esc(s):return s.replace('&',r'\&').replace('_',r'\_').replace('%',r'\%')
rows=[]
for c in chapters:
    labels=[]
    for url in c['source_resources']:
        r=next(r for r in m['resources'] if r['resource_page_url']==url)
        labels.append(r'\href{'+url+'}{'+r['course']+' '+esc(pathlib.Path(r['path']).name[33:].replace('MIT8_04S16_','').replace('MIT8_05F13_','').replace('MIT8_06S18','').replace('.pdf',''))+'}')
    rows.append(f"{c['number']} & {esc(c['title'])} & "+'; '.join(labels)+r'\\')
text=r'''\originalchapter{来源对应与覆盖边界}
本册正文为按先修顺序的中文重编, 不是逐页全文翻译. 下表给主要来源, 独立补充的证明和算例也在相应章内展开. 第15章含时微扰的基本公式为独立推导, 没有复制被暂缓打包的8.06第4章中的教材改编例题. 三门课程教师均为Barton Zwiebach. 8.04原讲义另署首版LaTeX转录者Sarah Geller、Andrew Turner; 第1、2、5、6、11、12、16、19讲署Geller, 第3、7、8、9、10、13、18讲署Turner, 第4、14--15、20--21、22讲署二人. 第17讲未另署转录者, 不代填姓名. 本册署名保留这些贡献者, 新增中文说明与题解为AI独立整理.
\begin{longtable}{p{.05\textwidth}p{.38\textwidth}p{.47\textwidth}}
\toprule 章 & 内容 & 原件资源页链接\\\midrule\endhead
'''+ '\n'.join(rows)+r'''
\bottomrule\end{longtable}
\originalsection{考核覆盖}
四份选定材料共23道大题的所有小问, 已在第17--20章转述并解答. 本次选定课程页面没有取得官方解答, 全部解答为AI独立计算. 未完成中文化的原件仍提供原始链接与实际PDF; 不能把原件归档当作中文解答完成. 下表逐份列出作业与测试状态, 历史试卷年份按题面和网页分别记录. 公式表只作为原件归档, 不计为已解答试卷.
\begin{longtable}{p{.10\textwidth}p{.47\textwidth}p{.33\textwidth}}
\toprule 课程 & 文件资源页 & 中文处理状态\\\midrule\endhead
'''
for a in assess:
    status={'full_chinese_statement_and_independent_solution':'所有小问中文题面及独立解答','withheld_rights_or_textbook_dependency':'教材依赖或第三方例外, 暂缓打包','formula_sheet_archived':'公式表原件已归档','original_archived_chinese_solution_pending':'原件已归档; 中文题解待补'}[a['status']]
    label=a['title'].replace(' (PDF)','')
    text+=a['course']+' & '+r'\href{'+a['resource_url']+'}{'+esc(label)+'} & '+status+r'\\'+'\n'
text+=r'''\bottomrule\end{longtable}
\originalsection{尚待扩充与许可}
8.04的完整打靶法、节点定理、$\delta$势、共振和Levinson定理; 8.05更完整的动力学表象与角动量合成; 8.06完整精细结构、带电粒子、Airy连接式证明、散射及全同粒子应用, 均仍需扩充. 当前WKB连接式注明引用标准结果, 没有宣称已完整证明特殊函数渐近式. 同样, 尚未逐份中文解答的考试不能列为完成.

8.06 Spring 2018第5章原件缺失, 两次考试明确不向OCW公开, 课纲述末周不计分作业也未在作业页提供. 没有补造题面. 默认许可证不自动覆盖引用的商业教材; 整份混合文件保守暂缓打包, URL、页数、SHA256及理由仍记录在来源清单. 其中的数学或物理事实可以独立推导, 本册不复制该类题面或外站图片.

课程入口: \href{https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/}{8.04 Spring 2016}, \href{https://ocw.mit.edu/courses/8-05-quantum-physics-ii-fall-2013/}{8.05 Fall 2013}, \href{https://ocw.mit.edu/courses/8-06-quantum-physics-iii-spring-2018/}{8.06 Spring 2018}. 每课页面的Syllabus、Calendar、Lecture Notes、Assignments和公开Exams栏目有本地检索快照. 逐文件清单保留直接PDF网址、标题、教师、实际题面年份、页数、字节数、SHA256和第三方例外.

原件及本中文改编按\href{https://creativecommons.org/licenses/by-nc-sa/4.0/}{CC BY-NC-SA 4.0}署名、非商业、相同方式共享; 另参\href{https://ocw.mit.edu/pages/privacy-and-terms-of-use/}{MIT OCW使用条款}. 本册没有MIT官方中文或官方认可的含义.
'''
(SUB/'chapters/source-map.tex').write_text(text)
print('Updated contributors, chapter/source coverage, assessment statuses, and source-map.tex')
