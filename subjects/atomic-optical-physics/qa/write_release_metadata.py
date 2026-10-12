"""Create scoped provenance and coverage records; no original source PDFs are released."""
from pathlib import Path
import json,collections,re
SUBJECTS=Path(__file__).resolve().parents[2]
CONFIG={
 'atomic-optical-physics':{
 'title':'原子分子与光物理','instructors':{'8-421':['Wolfgang Ketterle'],'8-422':['Wolfgang Ketterle'],'6-974':['Franz X. Kärtner'],'6-453':['Jeffrey H. Shapiro']},
 'assessments':[
 {'course':'8.421','kind':'homework','hosted_term':'Spring 2014','document_term':'Spring 2012','counts':[3,3,3,2,3,3,3,3,2,2],'chapter':'15–16'},
 {'course':'8.422','kind':'homework','hosted_term':'Spring 2013','document_term':'Spring 2013; files 1 and 3 also bear 2011 dates','counts':[3,3,4,2,2,3,3,2,3,3],'chapter':'17–18'},
 {'course':'8.421','kind':'midterm','years':[2008,2010,2012,2014],'counts':[5,3,5,4],'chapter':'19'}],
 'count':72,'complete':72,'partial':[],
 'course_scope':{'8.421 Spring 2014':'Core thematic reconstruction, all three calendar blocks; all 27 self-contained original assignment problem numbers and 17 published midterm problem numbers. No verbatim transcript claim.','8.422 Spring 2013':'Core thematic reconstruction of 21 calendar sessions / 28 transcript segments; all 28 original assignment problem numbers. No exams in the syllabus.','6.974 Spring 2006':'Selected laser, gain, cavity and linewidth background only. Downloaded files are not whole-course translated coverage.','6.453 Fall 2016':'Selected quantized optical states, correlations and detection only. Communication lectures and assessment bank not translated.'},
 'limits':['Third-party book figures and literary quotations are excluded.','AMO Wiki and textbook-only reading links are not republished.','Semester papers and laboratory research projects were not performed.','Original transcripts marked INAUDIBLE do not justify fabricated instructor words.','Underspecified angular geometry, density, linewidth convention and distribution are answered conditionally; no unique experimental number is fabricated.'],
 'corrections':['8.422 HW2 P3: general LOCC does not preserve Schmidt rank; a fixed Schmidt-amplitude threshold is not monotone.','8.422 HW3 P1: two-arm loss visibility depends on both transmissions, not only their angular difference.','8.422 HW4 P1: stated Yurke state and number difference yield 1/n, not the printed sqrt(2)/n.','8.422 HW6 P3: one fixed finite environment is not an exponential Markov channel without a reset/scaling limit.','8.422 HW7 P1: short-time expansion also requires small detuning*time and decay*time.'],
 'theory_chapters':list(range(1,15)),
 },
 'quantum-information':{
 'title':'量子信息与量子计算','instructors':{'18-435':['Peter W. Shor'],'mas-865':['Isaac Chuang','Peter Shor']},
 'assessments':[
 {'course':'18.435J / 2.111','kind':'main homework','original_problem_numbers':{'HW1':[1,2,3],'HW2':[1,2,3,4,6,7],'HW3':[1,2,3,5,6,7],'HW4':[1,2,3,4,5],'HW5':[1,2,3,4,5]},'chapter':'14','withdrawn':['HW2.5']},
 {'course':'MAS.865J / 6.443J / 8.371J / 18.409','kind':'problem set','counts':[4,4,3,4],'chapter':'15–16'},
 {'course':'18.435J / 2.111J / ESD.79','kind':'additional problem set','original_problem_numbers':{'PS1':[1,2,3],'PS2':[1,2,3,4,5,6],'PS3':[1,2,3,4,5],'PS4':[1,2,3,4,5,6,8],'PS5':[1,2,3,4],'PS6':[1,3,4],'PS7':[1,2,3,4,5],'PS8':[1,2,3],'PS9':[1,2,3,4,5,6],'PS10':[1,2,3,4]},'document_year_note':'PS3,4,7,8,9 print Fall 2004; other extra sets have no printed year. Hosted on 2003 OCW.','chapter':'17'},
 {'course':'18.435J','kind':'quiz','counts':[3,4],'chapter':'17','solution_status':['Quiz 1 official solution retrieved','Quiz 2: editor answers; separate official solution not retrieved']}],
 'count':93,'complete':92,'partial':[{'id':'18.435J HW4.5','reason':'The downloaded figure does not yield a legible unique edge set. The official solutions4 PDF explicitly defers this extra-credit solution. A clearly identified three-CNOT alternative is given, not a proof of that specific figure.'}],
 'course_scope':{'18.435J / 2.111 Fall 2003':'Core algorithm, circuit, noise and QEC themes; available main and extra self-contained assessment files. Only part of the original lecture notes is publicly available.','MAS.865J Spring 2006':'20 theoretical lecture topics reconstructed thematically; lecture 18 alternative notes count as the same session. All 15 published PS problem numbers, with original subquestions. Last six calendar entries are project meetings/presentations.','8.370x Spring 2018':'OCW syllabus/about and Open Learning Library public about access checked only; no locally recovered full assessment bank or whole-course transcript claim.','8.371x Spring 2018':'OCW syllabus/about entry checked only; not merged with MAS.865J 2006 8.371J merely because of the number.'},
 'limits':['Commercial Nielsen–Chuang textbook-only problem references are not transcribed or solved as recovered original statements.','Book passages directly reproduced inside HW1 are excluded.','HW2.5 is withdrawn by the author.','Research projects, global minimum graph/estimator proofs and a device-specific rigorous threshold were not completed.','General HSW, full decoupling, full adiabatic equivalence, non-Abelian algorithms and majorization theorem proofs are cited advanced results; the Chinese volume derives the stated elementary models rather than claiming full reproof.','Finite numeric checks are not a proof for all inputs or all decoders.'],
 'book_refs':['2.29','2.30','2.31','2.32','2.59','2.60','2.61','5.20','10.27','4.26','5.6'],
 'corrections':['MAS PS1: use squared fidelity consistently, fix Steane Fourier support and check matrix indices.','MAS PS2: ZIZ is harmless for both indicated Clifford implementations, contradicting a claim in the original problem.','MAS PS3: real gates cannot densely generate all complex unitaries on a fixed Hilbert space; computational universality via an extra rebit is distinguished.','MAS PS4: normalize Bayesian posteriors over labels; nondegenerate posterior width scales as t^(-1/2), not t^(-1).','MAS PS4: all LOCC does not preserve Schmidt rank.','Additional PS5.4: F2 tensor F3 is not related to F6 by the same input/output permutation; diagonal entries give a counterexample.','Old encoded PDF text needed visual verification: extra PS2 uses Y/X, AC Bell+ with B+, and a bra+ contraction; PS8 has the same negative X rotation on both sides.'],
 'theory_chapters':list(range(1,14)),
 }}
SCRIBES={1:'Kayla Jacobs',2:'Jennifer Novosad',3:'Saikat Guha',4:'Kayla Jacobs',5:'Igor Sylvester (some originals: Sylvestor)',6:'Danial Lashkari',7:'Salman Abolfathe',8:'Kayla Jacobs',9:'Kayla Jacobs',10:'Edward Platt',11:'Isaac Kim',12:'Kayla Jacobs',13:'Igor Sylvester (some originals: Sylvestor)',14:'Stephen Jordan',15:'Saikat Guha',16:'Kayla Jacobs',17:'Igor Sylvester (some originals: Sylvestor)',18:'Jennifer Novosad',19:'Kayla Jacobs',20:'Edward Platt'}
for slug,c in CONFIG.items():
 root=SUBJECTS/slug;d=json.loads((root/'source-inventory.json').read_text());stats={}
 for f in d['files']:
  q=stats.setdefault(f['course'],{'files_unique_by_sha256':0,'pdfs_unique_by_sha256':0,'downloaded_pdf_pages_sum':0,'note':'File hash deduplication does not remove content overlap in combined/chapter files or alternate lecture versions; these are not delivered Chinese page counts.'});q['files_unique_by_sha256']+=1;q['pdfs_unique_by_sha256']+=f['local'].endswith('.pdf');q['downloaded_pdf_pages_sum']+=f.get('pages',0)
  f['course_instructors']=next((v for k,v in c['instructors'].items() if f['course'].startswith(k)),[])
  f['license_basis']={'default':'CC BY-NC-SA 4.0','terms':'https://ocw.mit.edu/pages/privacy-and-terms-of-use/','exceptions':'Book/literary excerpts and third-party figures are not reused. No original downloaded PDF is included in this release. The default does not override item-specific third-party rights.'}
  if f['course'].startswith('mas-865'):
   m=re.search(r'lecture_?(\d+)',f['local'])
   if m:f['student_scribe']=SCRIBES[int(m.group(1))]
 d['retrieved_files_summary']=stats;d['bibliographic_metadata_added_on']='2026-10-12';(root/'source-inventory.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 cov={'schema_version':1,'frozen_target':'coverage-frozen.json','counting_unit':'One original numbered MIT problem, irrespective of merged Chinese exercise environments. Subparts do not add to the count. Withdrawn and unavailable book-only statements do not count.','original_problem_numbers':c['count'],'answer_provided_problem_numbers':c['complete'],'partial_problem_numbers':c['partial'],'assessment_groups':c['assessments'],'course_scope':c['course_scope'],'theory_chapters':c['theory_chapters'],'limitations':c['limits'],'source_corrections_or_qualifications':c['corrections'],'download_inventory':stats,'solution_authorship':'Editor-derived answers unless explicitly described as reconstructed with an actual official solution; corrections are identified in the body.','independent_agent_review':False}
 if 'book_refs'in c:cov['unavailable_book_problem_references']={'book':'Nielsen and Chuang, Quantum Computation and Quantum Information','distinct_numbers':c['book_refs'],'count':len(c['book_refs'])}
 if slug=='quantum-information':cov['MAS_lecture_scribes']={str(k):v for k,v in SCRIBES.items()}
 (root/'coverage.json').write_text(json.dumps(cov,ensure_ascii=False,indent=2)+'\n')
 license='''# 许可与署名

本卷根据 MIT OpenCourseWare 的公开课程材料翻译、按主题重编，并补写中文推导与解答。MIT 与原作者保留原作权利；本项目不表示 MIT、授课教师或学生笔记者认可。

适用 OCW 默认许可的改编内容和本项目新增的中文说明、解答及自绘图以 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 发布：署名、非商业使用、相同方式共享。许可全文：[Legal Code](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode)。使用条款：[MIT OCW Privacy and Terms](https://ocw.mit.edu/pages/privacy-and-terms-of-use/)。

这项默认许可不覆盖逐件标注的第三方例外。出版包没有收录下载的英文原 PDF、商业教材、第三方教材插图、文学引文或外部字体文件；教材题号只保留定位。数学事实的独立推导不意味着取得原书题面的复制许可。

逐文件出处、作者角色、下载版本、URL、SHA-256 与页数在 `source-inventory.json`；实际改编层级与未覆盖项在 `coverage.json` 和 `SOURCES.md`。软件与模板沿用各自文件中的许可说明，不能把本卷内容许可解释为替换它们的原许可。

项目编者所作修改：中文翻译、物理与计算主题重排、TeX 公式重录、推导及条件补写、官方排印错误复核、自绘 TikZ 图和数值矢量图。自行补写答案不标成 MIT 官方答案。

原作者与课程：
'''
 for course,scope in c['course_scope'].items():
  matching=[f for f in d['files'] if course.split()[0].replace('.','-').lower() in f['course']]
  teachers=sorted({a for f in matching for a in f['course_instructors']});license+=f'\n- {course}：'+(', '.join(teachers) if teachers else '课程网页列出的原作者；见来源表')+'。'
 if slug=='quantum-information':license+='\n\nMAS.865J 学生笔记署名：'+', '.join(sorted(set(SCRIBES.values())))+'。逐讲对应保留在账本。'
 (root/'LICENSE.md').write_text(license+'\n')
 lines=[f'# {c["title"]}来源与覆盖','', '冻结清单先于正文写作建立；此表另记实际完成层级。下载成功、目录存在和中文主题覆盖分别计数。下载的原件只用于本地核对，正式发布包不重新分发。', '', '| 官方课程 | 实际公开文件（SHA 去重） | 中文层级 |','|---|---:|---|']
 for course,scope in c['course_scope'].items():
  # Explicit corresponding slugs, rather than conflating course aliases.
  key=next((k for k in stats if course.startswith(k.split('-')[0]+'.'+k.split('-')[1])),None)
  if course.startswith('MAS'):key=next((k for k in stats if k.startswith('mas-865')),None)
  count=stats[key]['pdfs_unique_by_sha256'] if key else '课程入口核查'
  url='https://ocw.mit.edu/courses/'+key+'/' if key else ('https://ocw.mit.edu/courses/8-370x-quantum-information-science-i-spring-2018/' if '8.370x'in course else 'https://ocw.mit.edu/courses/8-371x-quantum-information-science-ii-spring-2018/')
  lines.append(f'| [{course}]({url}) | {count} | {scope} |')
 lines+=['','题数以原题大编号计；多道基础题在排版中合并到一个 `exercise`，不把排版环境数量冒充原题数。',f'本卷登记 **{c["count"]}** 个原题号；**{c["complete"]}** 个给出所述条件下的答案。']
 for p in c['partial']:lines.append(f'- 部分完成 {p["id"]}：{p["reason"]}')
 lines+=['','版本与考核分组：','']
 for a in c['assessments']:lines.append('- '+json.dumps(a,ensure_ascii=False))
 lines+=['','未覆盖及边界：','']+['- '+x for x in c['limits']]
 if 'book_refs'in c:lines+=['','未取得可再出版题面的商业教材定位：'+', '.join(c['book_refs'])+'；共11个不同编号。']
 lines+=['','校正与条件限定：','']+['- '+x for x in c['corrections']]
 lines+=['','完整来源索引：','', '| 文件/原作者角色 | 官方资源页 | 文件链接 | SHA-256 | 原页数 |','|---|---|---|---|---:|']
 for f in d['files']:
  if not f['local'].endswith('.pdf'):continue
  author=', '.join(f['course_instructors'])+('; scribe: '+f['student_scribe'] if 'student_scribe'in f else '')
  lines.append(f'| {Path(f["local"]).name} / {author} | [官方资源]({f["resource_pages"][-1]}) | [原文件]({f["url"]}) | `{f["sha256"]}` | {f.get("pages", "")} |')
 (root/'SOURCES.md').write_text('\n'.join(lines)+'\n')
 print(slug,'coverage records written; PDF source entries',sum(f['local'].endswith('.pdf') for f in d['files']))
