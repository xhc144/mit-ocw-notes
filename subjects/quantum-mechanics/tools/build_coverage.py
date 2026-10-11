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

# Per-document available MIT questions. Number-only external references remain explicit.
addition_specs={
 '804':{3:([1,2,3,4,5,6],[]),6:([1,3,4,5,6],[2]),7:([1,3,4,6],[2,5]),8:([1,2,3,4,5],[]),10:([1,2,3,4,5,6,7],[])},
 '805':{1:([1,2,3,4,5,6],[7]),2:([1,2,3,4,5,6],[]),3:([1,2,3,4,5,6],[]),4:([1,2,3,4,5,7],[6]),5:([1,2,3,4,5,6,8,9],[7]),8:([1,2,3,4,5,6],[]),10:([1,2,3,5],[4]),11:([1,2,3,4,5,6,'practice1','practice2','practice3','practice4','practice5','practice6'],[])},
 '806':{2:([1,2,3,4,5],[]),3:([1,2,3,4,5],[]),4:([1,2,3,4,6],[5]),6:([1,2,3],[4,5]),7:([1,2,3,4,5,6,7],[]),8:([1,2,3,4,5,6],[]),9:([1,2,3],[])}
}
added={}
for course,sets in addition_specs.items():
    for ps,(usable,omitted)in sets.items():
        name=(f'MIT8_04S16_ps{ps}_2016.pdf'if course=='804'else f'MIT8_05F13_ps{ps}.pdf'if course=='805'else f'MIT8_06S18ps{ps}.pdf')
        f=f'chapters/assessment-{course}-ps{ps}.tex'
        selected[name]=(f,len(usable))
        added[name]={'usable_questions':usable,'number_only_external_references':omitted,'all_subparts_of_usable_questions':True,'role_notes':[]}
added['MIT8_05F13_ps10.pdf']['role_notes']=['Question 3 contains all seven exercises from MIT Chapter 9; counted once as a main question.']
added['MIT8_05F13_ps11.pdf']['role_notes']=['Six regular and six practice main questions; practice originally not for submission.']
added['MIT8_06S18ps9.pdf']['role_notes']=['Practice problem set.']
added['MIT8_06S18ps3.pdf']['role_notes']=['Q1 expressly credited to Griffiths with modifications; independently rewritten Chinese mathematics, not labelled MIT original.']
for course,ps in [('804',8),('806',7)]:
    name=f'MIT8_04S16_ps{ps}_2016.pdf'if course=='804'else f'MIT8_06S18ps{ps}.pdf'
    added[name]['role_notes'].append('Referenced commercial book figure/data not supplied; own generic model/figure explicitly labelled, no invented missing statement.')
for i,(name,rs)in enumerate([
 ('spectrum-variational-support.tex',[match('8.05',1)]),
 ('time-dependent-support.tex',[match('8.06',4)])],18):
    f=SUB/'chapters'/name
    chapters.append({'number':i,'title':re.search(r'\\originalchapter\{([^}]+)\}',f.read_text())[1],
      'file':str(f.relative_to(ROOT)),'status':'written_independent_review_completed',
      'source_resources':[r['resource_page_url']for r in rs],'scope':'Omitted derivations and examples integrated as a supplement; no page-by-page translation claim.','original_additions':True})
chapters[7]['source_resources'].append(match('8.05',3)['resource_page_url'])
chapters[7]['supplement_file']='subjects/quantum-mechanics/chapters/linear-algebra-support.tex'
assess=[]
for r in m['resources']:
    if r['category']not in ('assignments','exams')or'duplicate_of'in r:continue
    name=pathlib.Path(r['path']).name[33:];sel=selected.get(name);info=added.get(name,{})
    status='all_available_questions_chinese_statement_and_AI_solution'if sel else 'formula_sheet_archived'
    a={'course':r['course'],'title':r['title'],'hosting_term':r['term'],'document_term':r['document_term'],
       'source_url':r['url'],'resource_url':r['resource_page_url'],'sha256':r['sha256'],'retained_original':r['retained_in_repository'],
       'status':status,'chinese_file':'subjects/quantum-mechanics/'+sel[0]if sel else None,'question_count':sel[1]if sel else 0,
       'all_subparts_of_usable_questions':bool(sel),'all_subparts_in_selected_document':bool(sel)and not info.get('number_only_external_references'),
       'solution_author':'AI independent'if sel else None,'official_solution_received':False,**info}
    if sel and name not in added:a['usable_questions']=list(range(1,sel[1]+1));a['number_only_external_references']=[]
    if sel:
        f=SUB/sel[0];assert f.is_file()
        # Prior audited chapters sometimes group adjacent original questions.
        if name in added:
            actual=len(re.findall(r'\\begin\{exercise\}',f.read_text()));assert actual==sel[1],(name,actual,sel[1])
    assess.append(a)
boundaries=['Course concepts organized by prerequisites; not a page-by-page translation.',
 '10 number-only commercial-book questions in the 20 additions have no complete MIT statement and are not invented.',
 '8.06 Chapter 5, exams and syllabus last-week problem set not supplied by OCW.',
 'No official assessment solutions received. All Chinese solutions are AI independent.',
 'Relativistic field theory, radiative corrections and full many-body theory outside this selection.']
out={'schema_version':2,'date':'2026-10-11','edition':'Completed 23-source restoration additions',
 'chinese_core_chapters':chapters,'assessments':assess,
 'assessment_documents_with_all_usable_questions_solved':len(selected),
 'fully_solved_assessment_documents':sum(a['all_subparts_in_selected_document']for a in assess),
 'fully_solved_main_questions':sum(s[1]for s in selected.values()),
 'addition_assessment_documents':len(added),'addition_main_questions':sum(len(a['usable_questions'])for a in added.values()),
 'number_only_omitted_questions':sum(len(a['number_only_external_references'])for a in added.values()),
 'all_subparts_of_usable_questions_completed':True,'coverage_boundaries':boundaries,
 'unavailable_or_withheld_sources':m['known_gaps'],
 'source_review_reports':['qa/additions-804-independent.md','qa/additions-805-early-independent.md','qa/additions-805-late-independent.md','qa/additions-806-independent.md']}
(SUB/'coverage.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
for r in m['resources']:
    if'duplicate_of'in r:continue
    name=pathlib.Path(r['path']).name[33:]
    if name in added:r['chinese_addition_coverage']=added[name]|{'file':'subjects/quantum-mechanics/'+selected[name][0],'solution_role':'AI independent'}
for n,f in [('MIT8_05F13_Chap_01.pdf','spectrum-variational-support.tex'),('MIT8_05F13_Chap_03.pdf','linear-algebra-support.tex'),('MIT8_06S18ch4.pdf','time-dependent-support.tex')]:
    r=next(r for r in m['resources']if r.get('path','').endswith(n))
    r['chinese_addition_coverage']={'file':'subjects/quantum-mechanics/chapters/'+f,'role':'Independent Chinese explanations of all source sections, combined with previously written theory.'}
mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
def esc(s):return s.replace('&',r'\&').replace('_',r'\_').replace('%',r'\%')
text=r'''\originalchapter{来源对应与覆盖边界}
本册按先修顺序中文重编, 不是逐页全文翻译. 原17理论章和19考核篇保留, 新增两理论章、在第8章接入Chapter 3线代补充, 并纳入20份作业的115道可用大题. 全册现有19理论章、39考核篇, 共227道大题. 8.05作业10第3题内部七个MIT讲义练习逐个解答, 计数仍为一大题; 作业11正式与练习各六题, 共12题.

三课教师Barton Zwiebach. 8.04原讲义另署首版LaTeX转录者Sarah Geller、Andrew Turner, 原件和清单保留各人贡献, 中文新增解释与题解为AI独立整理. 改编或Inspired信用照实保留, 不称全部题目均为MIT原创. 官方课程页面未提供本册所选题目的官方解答.
\begin{longtable}{p{.05\textwidth}p{.38\textwidth}p{.47\textwidth}}
\toprule 章 & 内容 & 原件资源页链接\\\midrule\endhead
'''
for c in chapters:
    labels=[]
    for url in c['source_resources']:
        r=next(r for r in m['resources']if r['resource_page_url']==url)
        name=pathlib.Path(r['path']).name[33:].replace('MIT8_04S16_','').replace('MIT8_05F13_','').replace('MIT8_06S18','').replace('.pdf','')
        labels.append(r'\href{'+url+'}{'+r['course']+' '+esc(name)+'}')
    text+=f"{c['number']} & {esc(c['title'])} & "+('; '.join(labels)if labels else '独立推导')+r'\\'+'\n'
text+=r'''\bottomrule\end{longtable}
\originalsection{逐份作业与考试覆盖}
39份文档中所有可用题面的小问均中文重述和独立解答. 少数文档还有仅给商业书题号的对象, 下表明确列出, 不补造题面. 两张公式表只归档, 不计解答考核. 数值图全部自绘, 题面所引未附商业图片没有复制或假称已见.
\begin{longtable}{p{.08\textwidth}p{.40\textwidth}p{.42\textwidth}}
\toprule 课程 & 原件资源页 & 可用题及处理\\\midrule\endhead
'''
for a in assess:
    if a['question_count']:
        status='完整可用题已解: '+','.join(str(q).replace('practice','练习')for q in a['usable_questions'])
        if a['number_only_external_references']:status+='; 仅书号未编: '+','.join(map(str,a['number_only_external_references']))
    else:status='公式表归档'
    text+=a['course']+' & '+r'\href{'+a['resource_url']+'}{'+esc(a['title'].replace(' (PDF)',''))+'} & '+status+r'\\'+'\n'
text+=r'''\bottomrule\end{longtable}
\originalsection{许可与实际缺失边界}
23份先前因商业书名、题号或改编信用而整份暂缓的OCW原件已逐件核对资源页并全部恢复, 当前78份唯一PDF、874页. \href{https://mitocw.zendesk.com/hc/en-us/articles/4414756181403-How-is-all-rights-reserved-content-different-from-the-rest-of-OCW-content}{OCW官方FAQ}解释未标例外内容及Used with permission的默认CC适用, 明确All rights reserved例外另论. 本次没有找到这23份资源的逐件相反声明. 商业教材本身没有打包, 仅书名、题号或参考表不意味着已取得外书题面或表格; 本册只处理MIT实际给出的完整任务和自写推导. 历史恢复、引用信用及具体逐题角色见覆盖清单和独审记录.

8.06第5章原件、考试及课纲末周作业未提供, 不编造. 部分进阶物理输入（低能Dirac项、非终止超几何增长等）仍在原章明确注明; 新增Runge--Lenz练习现给出长算符恒等式的有序推导. 本册没有场论、辐射修正或完整多体论.

课程入口: \href{https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/}{8.04 Spring 2016}, \href{https://ocw.mit.edu/courses/8-05-quantum-physics-ii-fall-2013/}{8.05 Fall 2013}, \href{https://ocw.mit.edu/courses/8-06-quantum-physics-iii-spring-2018/}{8.06 Spring 2018}. 逐文件清单保存资源页、直接PDF网址、题面年份、页数、字节数、SHA256、许可与贡献者.

原件及中文改编按\href{https://creativecommons.org/licenses/by-nc-sa/4.0/}{CC BY-NC-SA 4.0}署名、非商业、相同方式共享, 另参\href{https://ocw.mit.edu/pages/privacy-and-terms-of-use/}{MIT OCW使用条款}. 本册为非官方中文整理.
'''
(SUB/'chapters/source-map.tex').write_text(text)
print('Updated 39 assessments / 227 main questions / 23-source coverage.')
