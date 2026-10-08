import pathlib,json,re,html,hashlib,datetime
ROOT=pathlib.Path('/workspace/mit-ocw-notes');R=ROOT/'sources/graph-theory/assessments/6042'
def load(n):return json.loads((R/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def plain(s):return html.unescape(re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',s))).strip()
# Top-level answer labels, checked against the actual task text, not figure panels or references.
parts={
'cp1':'abcd,abc,abc,-,-','cp2':'-,-,-,-','cp3':'-,-,-,-,-','cp4':'-,abc,abc,-','cp5':'-,abcde,-,-,abcdefg','cp6':'ab,abcdefg,abc,-','cp7':'-,-,abcde,-,abcd','cp8':'-,ab,-,-','cp9':'abc,abc,abcd,-','cp10':'ab,ab,abcdef,abc','cp11':'ab,-,ab,abcd','cp12':'ab,ab,abc,abcd','cp13':'-,abcde,ab','cp14':'-,abc,-,abc','cp15':'abc,ab,abcd','cp16':'abc,ab,abcd,ab','cp17':'abcde,abcd,abc,abcdef','cp18':'abcdefgh,abcd,abcd,ab','cp19':'abcd,abc,-,abcdefghij,ab','cp20':'abc,ab,abc,abc','cp21':'abcd,-,-,ab','cp22':'ab,abcde,-,-','cp23':'ab,abcd,-,abcd,-','cp24':'abc,ab,-,-,-','cp25':'ab,ab,ab,abcde','cp26':'abcd,abcd,abcdefghijklmno,abc,ab','cp27':'abcd,abc,-,ab,-','cp28':'ab,abc,-,-,-,abc','cp29':'abcde,-,-,-','cp30':'abcde,abc,abcd,abcd','cp31':'-,-,abc,ab,ab','cp32':'abcd,abc,-,abcdefghij,ab','cp33':'abc,abcd,abcdef,abcdefg,abc','cp34':'abcd,abc,-,-,-,ab','cp35':'abcdefg,-,ab',
'ps1':'-,-,abcd,abcde','ps2':'abc,-,abcdefgh','ps3':'-,-,abcd','ps4':'-,-,abcdef','ps5':'-,ab,abcd','ps6':'-,ab,abc','ps7':'abcd,ab,-,ab','ps8':'-,ab,abc','ps9':'-,-,-','ps10':'abc,abcd,ab','ps11':'abc,-,abcde','ps12':'abc,abcd,abc',
'midterm1':'-,-,abcd,abcde,-','midterm2':'-,ab,-,abcde,-,abc','midterm3':'abc,ab,ab,-,abcdefg,ab','finalexam':'-,-,abcde,ab,abcd,-,abcde,abcdef,ab,-,abcd,abc'}
topics={
'cp1':['勾股定理证明','错误代数证明','错误证明辨析','算术几何均值证明','突击测验悖论'],
'cp2':['反证法不等式','根号无理性','无理数幂分类','构造无理数有理幂'],
'cp3':['良序原理邮票填空','平方和良序证明','四次方无整数解','二进制金额','邮票可表示性'],
'cp4':['命题逻辑分配律','文件系统可满足性','数字加法电路','自然语言条件句'],
'cp5':['量词及数域','二进制串逻辑','邮件关系量词','量词反模型','逻辑密码故事'],
'cp6':['集合运算与逻辑','集合论公式','序偶编码','子集取走游戏'],
'cp7':['逆关系性质','笛卡尔积基数','函数与像集基数','映射规则','单射满射双射'],
'cp8':['数列不等式归纳','L形铺砖','邮票归纳','素数整除归纳谬误'],
'cp9':['乘法状态机','十五数码不变量','车流状态机','网格二邻居感染过程'],
'cp10':['递归函数及导数','括号匹配递归','递归集合','满二叉树叶数与规模'],
'cp11':['无穷集合加点','可数性与满射','有理数可数性','停机问题'],
'cp12':['扩展Euclid','素因子gcd/lcm','二进制gcd','整除与gcd性质'],
'cp13':['模算术余数','中国剩余定理','整数多项式同余'],
'cp14':['Euler定理余数','模逆与Euler函数','素数幂Euler函数','十三次方模十'],
'cp15':['RSA计算','Euler函数与因子分解','RSA解密正确性'],
'cp16':['闭游走奇偶与有向圈','有向距离等号与最短路','de Bruijn串与Euler游走','竞赛图Hamilton路径'],
'cp17':['课程先修DAG排程','加权DAG两处理器排程','极端并行排程界','DAG覆盖边与传递约简'],
'cp18':['一般关系分类','幂集偏序链与反链','子序列与偏序链反链','等价关系与函数核'],
'cp19':['二部图平均度与人数','握手引理及奇度连通分支','图同构枚举','同构不变量','有向图同构与邻居像'],
'cp20':['寄存器分配与图染色','连通性错误归纳','三染色逻辑门构件','超立方体点连通度'],
'cp21':['网格Kruskal/Prim/并行MST','树与唯一路径','最小权边必入MST','宽度一与森林'],
'cp22':['稳定匹配与唯一性算法','稳定匹配算法不变量判定','由不变量证明稳定性','医院容量稳定匹配'],
'cp23':['酒水混合','沙漠远征调度','积分估计','借贷几何级数','几何和扰动法'],
'cp24':['渐近关系分类','渐近关系作为偏序','大O伪证明','渐近断言','阶乘对数增长'],
'cp25':['一般双射计数','最大叶Prüfer编码与Cayley公式','隔板法双射','关系/函数/双射计数'],
'cp26':['分组计数','书籍/整数计数','BOOKKEEPER排列','二项式系数','轮舞与分组计数'],
'cp27':['一般鸽巢原理','密码容斥','格点路径容斥计数','重复数字整除','幂三鸽巢'],
'cp28':['四门Monty Hall','组件故障概率','二次抛币','可数并集上界','概率规则','二胜系列概率'],
'cp29':['疾病贝叶斯','三囚犯概率','不完整牌组','首次出现HTT/HHT'],
'cp30':['大学选择条件概率','三币独立性','随机图二步游走与三角形','独立事件性质'],
'cp31':['猜数游戏策略','指标独立性','均匀变量最大值分布','二项分布','生育停止变量'],
'cp32':['二部图平均度与人数（重复CP19）','握手引理及奇度连通分支（重复CP19）','图同构枚举（重复CP19）','同构不变量（重复CP19）','有向图同构与邻居像（重复CP19）'],
'cp33':['Markov牛群温度','赌博期望方差','随机返还帽子','随机边赋色的单色三角形','期望及方差极值'],
'cp34':['抽样置信度','生日碰撞','弱大数收敛率','置信度发表偏差','测速统计','两两独立抽样定理'],
'cp35':['有限图随机游走平稳性和收敛','双随机转移与均匀平稳分布','对称Google图的度数平稳分布'],
'ps1':['无理性','良序原理不等式','命题逻辑','超前进位电路'],
'ps2':['集合论公式','De Morgan集合律','二进制串递归和逻辑'],
'ps3':['Fibonacci闭式','拆堆游戏归纳','复合函数单满射'],
'ps4':['格点机器人算术不变量','唯一标号满二叉树叶数','实区间/平面基数'],
'ps5':['二进制扩展gcd','素数模自逆/Wilson','Euler函数乘法性'],
'ps6':['RSA危险消息','有向路径与闭游走/圈','竞赛图王者定理'],
'ps7':['一般传递关系','等价关系交并','四图同构比较','两端图与错误归纳'],
'ps8':['不同权值MST唯一性','无三角形四色图','稳定匹配的非极端解与指数多解'],
'ps9':['立方和','阶乘渐近','幂和渐近'],
'ps10':['骰子计数','字母/团队计数','多项式模素数'],
'ps11':['矩阵单色矩形鸽巢','抽牌策略','两张牌条件概率'],
'ps12':['均匀变量独立性','合并血样期望','随机布尔可满足性'],
'midterm1':['无理性','四次方良序反证','谓词逻辑','整数函数单滿射','团队人数归纳'],
'midterm2':['递归有理函数','水桶状态机','无穷集合基数','gcd/lcm与素数幂','同余','Euler函数'],
'midterm3':['DAG排程','一般偏序与等价关系','多条路径与圈','树的染色计数','不等人数稳定匹配','级数积分判别'],
'finalexam':['概率逻辑','树的宽度一','数论真假','DAG并行排程极端界','度序列与连通性','大O不可比','扑克计数','条件概率','随机图度二顶点期望','抛币方差求和','Markov/Chebyshev赌博','随机游走平稳分布反例']}
selected={'ps4':[2],'ps6':[2,3],'ps7':[3,4],'ps8':[1,2,3],'cp10':[4],'cp16':[1,2,3,4],'cp17':[1,2,3,4],'cp18':[3],'cp19':[1,2,3,4,5],'cp20':[1,2,3,4],'cp21':[1,2,3,4],'cp22':[1,2,3,4],'cp25':[2],'cp30':[3],'cp32':[1,2,3,4,5],'cp33':[4],'cp35':[1,2,3],'midterm3':[1,3,4,5],'finalexam':[2,4,5,9,12]}
bridges={'cp9':[4],'cp27':[3],'ps11':[1]}
fs=[];ver={x['filename']:x for x in load('oll-public-pdf-verification.json')}
for f in load('pdf-file-metadata.json'):
 code=f['filename'].replace('MIT6_042JS15_','')[:-4];text=(R/'text'/(f['filename'][:-4]+'.txt')).read_text();headings=list(re.finditer(r'(?:^|\n)Problem\s+(\d+)(?=\.|\s*\()',text));labels=parts[code].split(',');assert len(headings)==len(labels)==len(topics[code]),code
 f.update({'local_path':str((R/'originals'/f['filename']).relative_to(ROOT)),'text_path':str((R/'text'/(f['filename'][:-4]+'.txt')).relative_to(ROOT)),'official_public_pdf_url':ver[f['filename']]['url'],'byte_equal_to_legacy_and_oll':ver[f['filename']]['byte_equal_to_legacy_zip'],'course_year':2015,'pdf_metadata_author':f['pdf_metadata'].get('author'),'copyright_authors':['Albert R. Meyer'] if code=='cp27' else ['Eric Lehman','F. Tom Leighton','Albert R. Meyer'],'header_instructors':['Albert R. Meyer','Adam Chlipala'],'copyright_year':2015,'license':'CC BY-SA 3.0' if code=='cp27' else 'CC BY-NC-SA 3.0','license_url':'https://creativecommons.org/licenses/by-sa/3.0/' if code=='cp27' else 'https://creativecommons.org/licenses/by-nc-sa/3.0/','license_evidence':'PDF first-page footer; specific PDF license governs over general course HTML 4.0 footer','official_solution_status':'explicitly withheld from general public in corresponding official legacy ZIP index; no solution file in either official ZIP or current OLL assessment units','main_question_count':len(headings),'questions':[]})
 for j,m in enumerate(headings):
  n=int(m[1]);seg=text[m.start():headings[j+1].start() if j+1<len(headings) else len(text)];lab=[] if labels[j]=='-' else list(labels[j]);page=int(re.findall(r'=== PAGE (\d+) ===',text[:m.start()])[-1]);scope='graph-theory' if n in selected.get(code,[]) else ('boundary-candidate' if n in bridges.get(code,[]) else 'excluded');q={'id':str(n),'physical_start_page':page,'topic_zh':topics[code][j],'explicit_top_level_subquestion_labels':lab,'top_level_answer_unit_count':len(lab) or 1,'scope':scope,'scope_reason':'题干直接研究图、树、图上的匹配/算法/染色、DAG链反链或随机图/图随机游走' if scope=='graph-theory' else ('可用图模型重述，但主体是一般不变量/格点路径计数/矩阵鸽巢；冻结范围时单独决定，默认不自动并入' if scope=='boundary-candidate' else '题干主体为逻辑、一般关系、数论、一般计数、集合或一般概率，未因箭头、函数图像或概率树而并入'),'stem_excerpt':re.sub(r'\s+',' ',seg)[:240],'has_figure':bool(re.search(r'Figure|pictured|graph in|graphs pictured',seg)),'difficulty_status':'未作竞赛量化分级；题型、先修与高工作量项另见 difficulty_gaps'}
  if code=='cp17' and n==4:q['nested_subquestions']={'f':['i','ii','iii']};q['leaf_answer_unit_count']=8
  if code=='cp32':q['content_duplicate_of']='MIT6_042JS15_cp19.pdf Problem '+str(n)
  if code=='cp10' and n==2:q['nested_unlabelled_proof_blanks_in_b']=5
  if code=='cp3' and n==1:q['unlabelled_proof_blanks']=6
  if code=='cp5' and n==1:q['unlabelled_formula_cases']=5;q['domains_per_formula']=5
  if code=='cp7' and n==1:q['table_fill_in_rows']=4
  if code=='cp28' and n==5:q['unlabelled_named_rules_to_prove']=5
  f['questions'].append(q)
 f['explicit_top_level_subquestion_count']=sum(len(q['explicit_top_level_subquestion_labels']) for q in f['questions']);f['top_level_answer_unit_count']=sum(q['top_level_answer_unit_count'] for q in f['questions']);fs.append(f)
fs.sort(key=lambda f:('MIT6_042JS15_'+f['filename'],))
# Public course timetable is a session sequence; dates are not invented.
s=(R/'pages/legacy-contents-readings-index.htm').read_text();progress=[]
for tr in re.findall(r'<tr\b[^>]*>(.*?)</tr>',s,re.S):
 tds=[plain(x) for x in re.findall(r'<t[dh]\b[^>]*>(.*?)</t[dh]>',tr,re.S)]
 if len(tds)==3 and tds[0].isdigit():progress.append({'session':int(tds[0]),'topic':tds[1],'textbook_reading':tds[2].replace(' (PDF)','')})
assert len(progress)==35
online=load('online-feedback-index.json');graph_online=[x for x in online if x['scope']=='graph-theory']
issues=[
{'source':'MIT6_042JS15_cp33.pdf Problem4(f,g)','type':'implicit_hypothesis','detail':'含sqrt(mu log mu)与1/log mu的有限n不等式须限定mu>1（本均匀三色模型n≥5）；极限n→∞不受影响。'},
{'source':'online Graph Coloring II; CP21 Problem2','type':'empty_graph_convention','detail':'无边图的色数1需非空；空图按本册约定色数0。树的唯一路径刻画须图非空，避免空图上全称断言真却不为树。'},
{'source':'all extracted PDF text; extraction-warnings.json','type':'text_extraction_limit','detail':'数学符号字体编码多处提取为D/C或控制字符；CP11/33/4/6有MuPDF zlib读取警告，CP33为所选范围。正式中文题干与公式须对照原PDF而非仅复制text，已实际打开CP33页2。'},
{'source':'MIT6_042JS15_cp32.pdf','type':'content_duplicate_and_index_mismatch','detail':'官方Session32阅读索引标Expectation，但其PDF题干、日期和页眉重复CP19（Week8 Wed），不同文件SHA不得计作新题；按内容去重。'},
{'source':'MIT6_042JS15_ps7.pdf Problem4; online Extreme Graphs','type':'terminology','detail':'原文line graph按其局部定义指路径图，不是通常的线图L(G)。中文译路径图，并说明原文局部用词。'},
{'source':'online Adjacency Matrix Q1','type':'official_feedback_mathematical_error','detail':'A²非零计数长度2游走而非必须无重复顶点的路径；i=j时有回走是反例。原解释另把i到j和j到i误写成同一方向。编者须独立纠正。'},
{'source':'online Extreme Graphs Q1 explanation','type':'official_feedback_arithmetic_typo','detail':'总度44即22边；K7为21边，添新顶点及一条边可达44，官方“两条边”会达46。'},
{'source':'online Chromatic Number Q2','type':'official_answer_convention_error','detail':'若n是轮图总顶点数且n≥4为偶数，则圈长n−1为奇数，色数4；官方答案3与题干相冲突。若改称偶数个轮圈顶点则3正确。'},
{'source':'online Graph Algorithm Q1 explanation','type':'official_feedback_definition_error','detail':'固定顶点集V时初始标记边集为空一般是森林而非树；“vacuously tree”不可沿用。'},
{'source':'online Multiple Choice (minimum-spanning-trees) Q1 explanation','type':'official_feedback_overstatement','detail':'不同边权是MST唯一性的充分条件，不是必要条件；“only true when distinct”不应沿用，任何树本身即使边权相同也有唯一MST。'},
{'source':'online Bipartite equivalence relation Q1','type':'terminology','detail':'本题实际问女孩到男孩匹配映射是全定义单射；“equivalence relation”是原文误用，不应译成等价关系结论。'},
{'source':'online Mating Ritual Q1','type':'terminology','detail':'确定的严格偏好与固定提议方给同一个提议方最优结果，不能把unique stable matchings理解为所有稳定匹配唯一。'},
{'source':'MIT6_042JS15_ps8.pdf Problem3(c)','type':'implicit_hypothesis','detail':'按n/2分组的原构造要求n为偶数；需说明偶数情形及奇数时取floor(n/2)组配上一个固定伴侣，n=1时原2^(n/2)下界不成立；若对奇数n≥3保留原2^(n/2)下界则另核构造，不能悄然声称原分组适用所有n。'},
{'source':'MIT6_042JS15_cp16.pdf Problem2','type':'distance_domain','detail':'最短路距离等号刻画应明确dist(u,v)有限；不可把∞=∞+有限视为存在最短路的证明。'},
{'source':'MIT6_042JS15_cp35.pdf Problem3','type':'random_walk_definition','detail':'1/outdeg(v)模型要求所有顶点outdeg>0且总弧数e>0；汇点需事先约定转移规则。'},
{'source':'MIT6_042JS15_cp27.pdf','type':'license_difference','detail':'该文件版权仅Albert R. Meyer，CC BY-SA3.0；其余50评测PDF均为三作者CC BY-NC-SA3.0，不可统一改标课程HTML4.0。'},
]
# Content deduplication proven by exact problem text after stripping course footer and page-break metadata.
a19=(R/'text/MIT6_042JS15_cp19.txt').read_text();a32=(R/'text/MIT6_042JS15_cp32.txt').read_text()
def norm_body(t):
 t=t[t.find('Problem 1.'):];t=re.sub(r'=== PAGE \d+ ===','',t);t=t.replace('\nFigure 1\nGraphs with several isomorphisms\n','\n');t=t.split('MIT OpenCourseWare')[0];return re.sub(r'\s+','',t)
assert norm_body(a19)==norm_body(a32)
body_sha=hashlib.sha256(norm_body(a19).encode()).hexdigest()
visual=[]
for p in sorted((R/'review-images').glob('*.png')):visual.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'actually_opened_with_view_image':True,'purpose':'题干/图形对象核查；不是完整193页视觉验收'})
# Hash-bind every saved evidence file, excluding this generator and the final manifest itself.
evidence=[]
for p in sorted(R.rglob('*')):
 if p.is_file() and p.name not in ['evidence-file-manifest.json']:evidence.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)})
(R/'evidence-file-manifest.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
selectedqs=[(f,q) for f in fs for q in f['questions'] if q['scope']=='graph-theory'];uniq=[(f,q) for f,q in selectedqs if not q.get('content_duplicate_of')]
course_url='https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/'
report={
'schema_version':1,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'独立模型资料审查，非人类专家；当前任务仅清单研究，无中文解答或主PDF编辑',
'write_scope':['sources/graph-theory/assessments/6042/','subjects/graph-theory/qa/assessments-inventory-6042.json'],
'course_metadata':{'official_title':'Mathematics for Computer Science','course_numbers':['6.042J','18.062J'],'term':'Spring 2015','level':'Undergraduate','instructors':['Albert R. Meyer','Adam Chlipala'],'official_course_url':course_url,'syllabus_url':course_url+'pages/syllabus/','readings_url':course_url+'pages/readings/','weekly_meetings':{'sessions_per_week':3,'hours_per_session':1.5,'hours_per_week':4.5,'format':'flipped class; 6–8人团队问题解决，课前阅读与在线反馈题'},'prerequisites':{'course':'18.01 Single Variable Calculus','topics':['数列与级数','极限','一元函数微分与积分']},'overview':['数学基础：定义、证明、集合、函数、关系','离散结构：数论、图、状态机、计数','离散概率'],'objectives':['使用离散数学描述算法/系统中的数据和结构','辨析严谨论证与错误证明，建立归纳证明','用组合和分析方法研究计算过程','计算概率及期望并进行团队问题解决'],'reading_book':{'title':'Mathematics for Computer Science','authors':['Eric Lehman','F. Tom Leighton','Albert R. Meyer'],'course_edition_year':2015,'evidence':'官方Readings页链接整本教材及逐课章节；评测PDF版权页确认三作者。不是外推商业书目。'},'session_progress_and_readings':progress,'calendar_policy':'只抄官方35课序列及阅读范围，不生成课程日历日期；PDF印刷题期/截止日期作为文件内元数据可查，不外推补齐。','assessment_weight_percent':{'class_participation':25,'online_feedback':5,'problem_sets':15,'three_midterms':30,'final_exam':25},'exam_details':{'midterms':{'count':3,'minutes_each':80,'weight_percent_each':10,'cribsheet':'one two-sided sheet'},'final':{'count':1,'minutes':180,'weight_percent':25,'cribsheet':'two two-sided sheets'}},'grading_notes':['最低1次作业及最低3次课堂参与不计总评','在线反馈与课堂问题主要按参与计分','每份作业设计在至多3小时完成'],'evidence_files':['pages/ocw-course-home.html','pages/ocw-syllabus.html','pages/ocw-readings.html','pages/oll-about.html','pages/legacy-contents-index.htm','pages/legacy-contents-syllabus-index.htm','pages/legacy-contents-readings-index.htm'],'republication':{'platform':'MIT Open Learning Library','run':'OCW+6.042J+2T2019','about_url':'https://openlearninglibrary.mit.edu/courses/course-v1:OCW+6.042J+2T2019/about','outline_url':'https://openlearninglibrary.mit.edu/courses/course-v1:OCW+6.042J+2T2019/course/','year':2019,'caution':'课程运行重发布年2019不是评测编写年；本清单51个PDF文件逐个核字节等同2015课程旧ZIP。课程其他slides有S16文件，不混入本评测年份。'}},
'resource_counts':{'problem_set_pdfs':12,'in_class_question_pdfs':35,'midterm_pdfs':3,'final_exam_pdfs':1,'assessment_pdf_files':len(fs),'assessment_pdf_pages':sum(f['pages'] for f in fs),'assessment_pdf_numbered_questions':sum(f['main_question_count'] for f in fs),'assessment_pdf_explicit_top_level_subquestions':sum(f['explicit_top_level_subquestion_count'] for f in fs),'assessment_pdf_top_level_answer_units':sum(f['top_level_answer_unit_count'] for f in fs),'standalone_quiz_pdfs_found':0,'practice_exam_pdfs_found':0,'official_pdf_solution_files_found':0,'online_feedback_html_pages':len(online),'online_Q_response_units':sum(x['question_count'] for x in online),'online_public_answer_marker_units':sum(x['public_answer_question_count'] for x in online),'online_public_explanation_blocks':sum(x['public_explanation_count'] for x in online),'selected_graph_pdf_question_occurrences':len(selectedqs),'selected_graph_pdf_questions_after_cp32_content_dedup':len(uniq),'selected_graph_online_html_pages':len(graph_online),'selected_graph_online_Q_response_units':sum(x['question_count'] for x in graph_online)},
'counting_method':'PDF主问题依原Problem n编号，a,b等实际作答小问手工核对，图(a)–(d)、引用小问、示例编号不算作答小问。无字母标签问题按1个顶层回答单元；明示的无标签填空/表格与已识别嵌套另列，故顶层回答单元不冒充全部微型判断数。HTML每个self_assessment页算一测验页，每个Qn_div算一回答单元，多选选项不另算问题，S块可能共用解释。',
'archive_checks':{'modern':{k:v for k,v in load('modern-download-zip-index.json').items() if k!='entries'},'modern_entry_count':len(load('modern-download-zip-index.json')['entries']),'modern_pdf_count':sum(e['name'].endswith('.pdf') for e in load('modern-download-zip-index.json')['entries']),'legacy':{k:v for k,v in load('legacy-download-zip-index.json').items() if k!='entries'},'legacy_entry_count':len(load('legacy-download-zip-index.json')['entries']),'legacy_pdf_count':sum(e['name'].endswith('.pdf') for e in load('legacy-download-zip-index.json')['entries']),'zip_storage_policy':'两份ZIP仅保存在/tmp；仓库保存ZIP完整条目索引、所需评测PDF与HTML证据','assessment_pdf_direct_url_checks':'51个当前公开OLL直链均实际GET成功，SHA逐个等于旧ZIP对应PDF','solution_search_scope':'两ZIP全部1941/385条目＋旧版三个评测分类HTML＋OLL课程资源索引195 PDF链接＋OLL12作业/4考试单元；未把受限、登录后或机构邮件申请的答案称为公开可得'},
'official_solution_status':{'pdf_assessments':'三个旧ZIP分类索引都明确solutions not available to general public；可由认可机构教师/学生按个案联系Meyer，但本任务未联系或取用受限答案。两公开ZIP及OLL单元均无这些PDF官方答案。','online_feedback':'171个公开HTML含376个官方答案标记与232块解释，区别于未公开的作业/课堂PDF/考试答案；有答案不代表有完整证明，且若干标记/解释有数学或术语错误。','evidence':['legacy-metadata/assignments/index.htm','legacy-metadata/in-class-questions/index.htm','legacy-metadata/exams/index.htm','online-feedback-index.json'],'practice_exams':'本2015公开包/当前OLL索引无独立Practice Exam资源；仅报告本课程核查范围，不宣称MIT所有课程均无。'},
'pdf_files':fs,
'online_feedback_inventory':{'path':'sources/graph-theory/assessments/6042/online-feedback-index.json','sha256':sha(R/'online-feedback-index.json'),'contains':'171项，每项原ZIP位置、HTML与题干文本路径、SHA、Q编号、答案标记与公开解释、题图依赖、范围理由及许可；全文原HTML保存供冻结后逐题编写','selected_graph_pages':[{'title':x['title'],'local_path':x['local_path'],'sha256':x['sha256'],'Q_ids':x['question_ids'],'public_answers':x['public_answer_question_count'],'public_explanation_blocks':x['public_explanation_count']} for x in graph_online]},
'content_deduplication':[{'files':['MIT6_042JS15_cp19.pdf','MIT6_042JS15_cp32.pdf'],'duplicate_question_pairs':[[str(i),str(i)] for i in range(1,6)],'comparison':'从Problem1起去除分页标识、空白、末尾OCW引文，以及CP32独有的Figure1说明文字后题干全文逐字相等；原文件SHA不同','normalized_body_sha256':body_sha,'recommendation':'只编一次并保留两个官方索引映射；不得计为10道新题。'}, {'sources':['CP21 Problem4(b)','Final Problem2'],'comparison':'Final树宽度一结论包含在CP21(4b)，后者额外要求推出森林等价；不能丢掉额外任务','recommendation':'内容去重时用一个完整解答覆盖两来源，考试编号仍在来源映射登记。'}, {'sources':['CP35 Problem1(a-f)','online Random Walks / Random Walks(cont.)'],'comparison':'三个相同转移图、平稳分布与收敛问题重合；在线节点单项回答比PDF问题拆分更细','recommendation':'冻结时逐个Q建立对照，可合并完整图题；CP35(g)与后续独立证明不能因图相同而删除。'}],
'source_issues_and_editorial_corrections':issues,
'difficulty_gaps':{'status':'未进行Putnam/IMC/CMC量化评级；这是资料清单，不冒称已解答难度审定','course_level':'本科离散数学；包括反馈识别题、完整归纳/交换论证、构造与算法运行、偏序调度极端构造、随机图方差及Markov链分析','higher_workload_candidates':['PS8 Problem2:需完整无三角形四色图论证','CP16 Problem3:de Bruijn/Euler图建模及一般化','CP17 Problem3:固定高度DAG的最少/最多处理器极端构造','CP17 Problem4:传递约简唯一性且含有向圈反例','CP20 Problem3:3染色逻辑构件逐项核图','CP33 Problem4:三角形共享边的联合概率、两两独立和方差','CP35 Problem1/3:平稳分布、周期性、多闭类与有向/无向模型区分'],'missing_public_solutions':'所有51个PDF需要编者独立写解答并再交叉审查；在线33图论解释块不足以代替全部75回答单元的完整中文解答'},
'license_and_attribution_summary':{'pdfs':'50×CC BY-NC-SA3.0（三作者）；CP27×CC BY-SA3.0（Albert R.Meyer）','online_html':'课程HTML明确CC BY-NC-SA4.0；未发现已选在线图题额外第三方限制标注，个人题作者未单列，按课程作者与MIT OCW来源归属，不杜撰','source_figures':'PDF图形按该PDF明确许可处理，HTML题图保存真实ZIP依赖；成册应原生TikZ重绘，禁止嵌整张英文页面','not_inferred':'许可取源页/文件标记，不把PDF metadata修改年2016或OLL运行年2019替代2015课程版权年；题干与官方答案不同可得性。'},
'actual_visual_source_checks':visual,
'evidence_manifest':{'path':'sources/graph-theory/assessments/6042/evidence-file-manifest.json','sha256':sha(R/'evidence-file-manifest.json'),'files':len(evidence)},
'remaining_work':['parent冻结统一来源和选题清单','按冻结清单合并跨PDF/HTML重题且保留完整来源编号','独立编写中文完整解答并交叉审核官方瑕疵与条件','本任务没有修改主PDF、章节、旧数学/视觉QA或其他学科']}
qa=ROOT/'subjects/graph-theory/qa/assessments-inventory-6042.json';qa.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report['resource_counts'],ensure_ascii=False));print('QA',sha(qa));print('evidence',len(evidence))
