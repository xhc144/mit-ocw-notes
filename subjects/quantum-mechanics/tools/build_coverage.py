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
mapping=[('8.04',[1,2,3,4]),('8.04',[5,6]),('8.04',[5,6]),('8.04',[7,8,9]),('8.04',[10,11]),('8.04',[16,17]),('8.04',[7,'14_15']),('8.05',[4,5,6]),('8.05',[2,7]),('8.05',[9,10]),('8.04',[22]),('8.05',[8]),('8.06',[1]),('8.06',[1,2]),('8.06',[6]),('8.06',[3,7]),('independent',[])]
def match(c,n):
    pattern={'8.04':f'LecNotes{n}.pdf','8.05':f'Chap_{n:02}.pdf','8.06':f'ch{n}.pdf'}[c] if isinstance(n,int) else f'LecNotes{n}.pdf'
    return next(r for r in m['resources'] if r['course']==c and r.get('path','').endswith(pattern))
chapters=[]
for i,(course,nums) in enumerate(mapping,1):
    p=SUB/f'chapters/ch{i:02}.tex';title=re.search(r'\\originalchapter\{([^}]+)\}',p.read_text())[1]
    rs=[match(course,n) for n in nums]
    chapters.append({'number':i,'title':title,'file':str(p.relative_to(ROOT)),'status':'written_independent_review_completed','source_resources':[r['resource_page_url'] for r in rs],
       'scope':('Independent support chapter, not a translation of unavailable 8.06 chapter 5.' if not rs else 'Concepts and derivations organized by prerequisites; not a complete page-by-page translation.'),
       'original_additions':True})
selected={'MIT8_04S16_ps1_2016.pdf': ('chapters/assessment-ps1.tex', 7), 'MIT8_04S16_Test1_Fall2015.pdf': ('chapters/assessment-test1.tex', 5), 'MIT8_05F13_ps6.pdf': ('chapters/assessment-ps6.tex', 6), 'MIT8_06S18ps1.pdf': ('chapters/assessment-advanced-ps1.tex', 5), 'MIT8_04S16_ps2_2016.pdf': ('chapters/assessment-804-ps2.tex', 5), 'MIT8_04S16_ps4_2016.pdf': ('chapters/assessment-804-ps4.tex', 7), 'MIT8_04S16_ps5_2016.pdf': ('chapters/assessment-804-ps5.tex', 8), 'MIT8_04S16_ps9_2016.pdf': ('chapters/assessment-804-ps9.tex', 6), 'MIT8_04S16_Test2_Fall2015.pdf': ('chapters/assessment-804-test2.tex', 5), 'MIT8_04S16_FinalTest_2015.pdf': ('chapters/assessment-804-final2015.tex', 6), 'MIT8_05F13_ps7.pdf': ('chapters/assessment-805-ps7.tex', 7), 'MIT8_05F13_ps9.pdf': ('chapters/assessment-805-ps9.tex', 6), 'MIT8_05F13_test_2011.pdf': ('chapters/assessment-805-test2011.tex', 5), 'MIT8_05F13_test_2012v4.pdf': ('chapters/assessment-805-test2012.tex', 5), 'MIT8_05F13_test_2013_v3.pdf': ('chapters/assessment-805-test2013.tex', 5), 'MIT8_05F13_final_2011.pdf': ('chapters/assessment-805-final2011.tex', 7), 'MIT8_05F13_final_2012.pdf': ('chapters/assessment-805-final2012.tex', 6), 'MIT8_05F13_final_2013.pdf': ('chapters/assessment-805-final2013.tex', 6), 'MIT8_06S18ps5.pdf': ('chapters/assessment-806-ps5.tex', 5)}
for f,n in selected.values():
    assert (SUB/f).is_file(), f
assess=[]
for r in m['resources']:
    if r['category'] not in ['assignments','exams'] or 'duplicate_of' in r:continue
    name=pathlib.Path(r.get('path',r.get('download_path_not_distributed'))).name[33:]
    sel=selected.get(name)
    status='full_chinese_statement_and_independent_solution' if sel else ('conservative_hold_or_incomplete_textbook_statement' if not r.get('retained_in_repository') else ('formula_sheet_archived' if 'Formula Sheet' in r['title'] else 'original_archived_chinese_solution_pending'))
    assess.append({'course':r['course'],'title':r['title'],'hosting_term':r['term'],'document_term':r['document_term'],'source_url':r['url'],'resource_url':r['resource_page_url'],'sha256':r['sha256'],'retained_original':r['retained_in_repository'],'status':status,'chinese_file':'subjects/quantum-mechanics/'+sel[0] if sel else None,'question_count':sel[1] if sel else None,'all_subparts_in_selected_document':bool(sel),'solution_author':'AI independent' if sel else None,'official_solution_received':False})
out={'schema_version':1,'date':'2026-10-11','edition':'Expanded continuous Chinese study book; all nineteen retained full-statement assessment documents solved','chinese_core_chapters':chapters,'assessments':assess,'fully_solved_assessment_documents':len(selected),'fully_solved_main_questions':sum(x[1] for x in selected.values()),
'coverage_boundaries':['Selected course sequence organized conceptually; no claim to translate every lecture page.','Unpublished 8.06 exams and conservative source holds are not invented.','Airy contour deformation, nonterminating hypergeometric growth, low-energy Dirac effective terms and Runge–Lenz long commutator identities are explicitly cited mathematical/physical inputs; subsequent calculations are derived.','Relativistic quantum field theory, radiative corrections and all many-body theory are outside this introductory-to-advanced selection.'],
'unavailable_or_withheld_sources':m['known_gaps'],'independent_solution_notice':'All Chinese assessment solutions are AI independent; no official solutions obtained for selected courses.'}
(SUB/'coverage.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
def esc(s):return s.replace('&',r'\&').replace('_',r'\_').replace('%',r'\%')
rows=[]
for c in chapters:
    labels=[]
    for url in c['source_resources']:
        r=next(r for r in m['resources'] if r['resource_page_url']==url)
        labels.append(r'\href{'+url+'}{'+r['course']+' '+esc(pathlib.Path(r['path']).name[33:].replace('MIT8_04S16_','').replace('MIT8_05F13_','').replace('MIT8_06S18','').replace('.pdf',''))+'}')
    rows.append(f"{c['number']} & {esc(c['title'])} & "+('; '.join(labels) if labels else '独立推导; 未冒称缺失原件翻译')+r'\\')
text=r'''\originalchapter{来源对应与覆盖边界}
本册正文为按先修顺序的中文重编, 不是逐页全文翻译. 下表给主要来源, 独立补充的证明和算例也在相应章内展开. 第15章含时微扰的基本公式为独立推导, 没有复制被暂缓打包的8.06第4章中的教材改编例题. 三门课程教师均为Barton Zwiebach. 8.04原讲义另署首版LaTeX转录者Sarah Geller、Andrew Turner; 第1、2、5、6、11、12、16、19讲署Geller, 第3、7、8、9、10、13、18讲署Turner, 第4、14--15、20--21、22讲署二人. 第17讲未另署转录者, 不代填姓名. 本册署名保留这些贡献者, 新增中文说明与题解为AI独立整理.
\begin{longtable}{p{.05\textwidth}p{.38\textwidth}p{.47\textwidth}}
\toprule 章 & 内容 & 原件资源页链接\\\midrule\endhead
'''+ '\n'.join(rows)+r'''
\bottomrule\end{longtable}
\originalsection{考核覆盖}
19份保留的完整题面考核共112道大题, 所有小问已在考核篇转述并独立解答. 本次选定课程页面没有取得官方解答, 全部解答为AI独立计算. 两张公式表作为原件提供, 不计入已解答试卷; 暂缓打包的混合文件只记录URL和校验事实, 不补造缺失的教材题面. 下表逐份列出作业与测试状态, 历史试卷年份按题面和网页分别记录. 公式表只作为原件归档, 不计为已解答试卷.
\begin{longtable}{p{.10\textwidth}p{.47\textwidth}p{.33\textwidth}}
\toprule 课程 & 文件资源页 & 中文处理状态\\\midrule\endhead
'''
for a in assess:
    status={'full_chinese_statement_and_independent_solution':'所有小问中文题面及独立解答','conservative_hold_or_incomplete_textbook_statement':'教材依赖或改编待核, 保守暂缓打包','formula_sheet_archived':'公式表原件已归档','original_archived_chinese_solution_pending':'原件已归档; 中文题解待补'}[a['status']]
    label=a['title'].replace(' (PDF)','')
    text+=a['course']+' & '+r'\href{'+a['resource_url']+'}{'+esc(label)+'} & '+status+r'\\'+'\n'
text+=r'''\bottomrule\end{longtable}
\originalsection{覆盖边界与许可}
正文已经补入打靶与节点排序、$\delta$势、相干与压缩、三种动力学表象、角动量合成、精细结构三项、含时跃迁与Berry相位、Airy连接推导、带电粒子、散射和全同粒子应用. 本册仍是按概念组织的选定课程学习册, 不是每页原讲义的全文翻译. 复路径变形、非终止超几何级数的增长结论、低能Dirac有效项及Runge--Lenz长算符恒等式明确作为进阶输入, 不假称已在本册从零证明. 没有包含场论、辐射修正或完整多体理论.

8.06 Spring 2018第5章原件缺失, 两次考试明确不向OCW公开, 课纲述末周不计分作业也未在作业页提供. 没有补造题面. 默认许可证不自动覆盖商业教材; 对题面依赖和明确改编信用未充分确认的混合文件, 整份保守暂缓打包. 引用、书目或改编信用本身不等于已证实的版权排除, 逐项记录区分观察事实、权利不确定性与当前打包决定. URL、页数和SHA256仍记录在清单. 其中的数学物理事实可独立推导, 本册不复制该类题面或外站图片.

课程入口: \href{https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/}{8.04 Spring 2016}, \href{https://ocw.mit.edu/courses/8-05-quantum-physics-ii-fall-2013/}{8.05 Fall 2013}, \href{https://ocw.mit.edu/courses/8-06-quantum-physics-iii-spring-2018/}{8.06 Spring 2018}. 每课页面的Syllabus、Calendar、Lecture Notes、Assignments和公开Exams栏目有本地检索快照. 逐文件清单保留直接PDF网址、标题、教师、实际题面年份、页数、字节数、SHA256、明确权利声明与保守暂缓理由.

原件及本中文改编按\href{https://creativecommons.org/licenses/by-nc-sa/4.0/}{CC BY-NC-SA 4.0}署名、非商业、相同方式共享; 另参\href{https://ocw.mit.edu/pages/privacy-and-terms-of-use/}{MIT OCW使用条款}. 本册没有MIT官方中文或官方认可的含义.
'''
(SUB/'chapters/source-map.tex').write_text(text)
print('Updated contributors, chapter/source coverage, assessment statuses, and source-map.tex')
