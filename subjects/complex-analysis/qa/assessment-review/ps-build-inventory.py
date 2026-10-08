import json,re,hashlib
from pathlib import Path
ROOT=Path('/workspace/mit-ocw-notes')
OUT=ROOT/'subjects/complex-analysis/qa/assessment-review'
BASE=ROOT/'sources/complex-analysis/18.04-spring-2018/assessments'
# Every row was read from its question PDF. Text below is a normalized inventory,
# not a replacement transcription. Conjugates were resolved visually.
DATA={
1:'''1|a,b,c.i,c.ii,d|z1=1+i,z2=1+3i：求乘积、商（直角形式）及主支z1^z2（极形式）;;求i^i全部值、指出主支值并讨论实性;;z=1+i√3，求z^8直角形式;;求z全部四次根;;原图|z|=2.5、辐角70°，复制图并加入五次根
2|a,b,c|证明共轭(exp z)=exp(bar z);;证明单位模z的逆等于bar z;;(x+iy)/(x−iy)=a+ib，证明a²+b²=1
3|a,b|画z=exp(t(1+i))、t全实数的曲线;;画z²映射下顶点0,1,i的三角域像
4|_|z_k=exp(2πi/n)，证明1+z_k+…+z_k^(n−1)=0
5|a.i,a.ii,a.iii,b.i,b.ii,b.iii|exp z：画竖直线像;;exp z：同图画水平线像;;证明这两类像在交点正交;;z²：复做竖直线像;;z²：复做水平线像;;z²：复做正交验证
6|_|求Arg((z−1)/(z+2))=±π/2全部点，并排除Arg未定义点''',
2:'''1|a,b|证明cos z整且导数−sin z;;给cot z解析域及导数
2|a,b|P=∏(z−r_j)，证明P'/P=Σ1/(z−r_j);;计算((az+b)/(cz+d))'并解释ad−bc=0
3|_|解释任一log分支为何不能总有log(exp z)=z
4|a,b|原点中心圆盘上f全纯，证明overline(f(bar z))全纯;;证明f(bar z)除f常数外不全纯
5|_|证明|z|²仅在0复可微
6|_|用主支log给出sqrt(z²−1)解析区域''',
3:'''1|a,b.i,b.ii,c|逆时针圆|z−2|=1上积分1/z;;用复积分基本定理证明简单闭曲线上积分z²为0;;实虚两部分写成Mdx+Ndy并各用Green定理;;单位圆上积分1/z写成实虚两部分平面积分
2|a,b.i,b.ii|直接定义算单位圆积分bar z，并比较积分z;;积分bar z²：0到1+i直线;;积分bar z²：0到1再到1+i折线
3|a,b|圆|z+4|=1积分1/(z+4)，Cauchy定理是否推出0及原因;;参数化计算该积分并核对前问
4|_|从0到1+i路径积分z^9+cos z−exp z，给直角形式并说明依据
5|a,b|上半单位圆1→−1积分z^(1/3)，主辐角分支;;复做π≤arg z<3π分支
6|_|用复积分基本定理证明1/z在穿孔平面无原函数
7|_|判定Re(∫f dz)=∫Re(f)dz，证明或反例
8|i,ii,iii,iv|穿孔平面是否单连通;;去非负实轴平面是否单连通;;圆内是否单连通;;圆外是否单连通''',
4:'''1|a,b,c,d|Cauchy公式算|z|=4积分[sin(πz²)+cos(πz²)]/[(z−1)(z−2)];;|z−i|=1积分z²/(z²+1);;|z|=2积分bar z/(z²−1)，注意非解析分子;;0≤θ≤π,r=1−0.1cos100θ波浪路径积分z²
2|a,b|直接积分证明z^n的Cauchy函数值公式及一阶导数公式;;|z|=a积分(c0+c1z+c2z²+c3z³)z^(−n)，n=0,1,…
3|a,b,c.i,c.ii||z|=2积分|z|exp z/z²;;全实轴积分1/[(x²+1)(x²+4)]，按图证明大半圆贡献消失;;以Cauchy公式分离0,1算积分1/[z²(z−1)³]=0;;扩大圆至R并估计趋0证明同一积分为0
4|_|曲线及内部全纯f在边界恒0，证明内部恒0
5|i,ii|γ过1+i，f=(1/2πi)∫cos w/(w−z)dw，求外侧趋1+i极限;;求内侧趋1+i极限
6|a,b|由Cauchy公式证明圆周平均值公式;;证明带exp(−inθ)权的一般导数平均值公式
7|a,b,c,d,e||z|=2积分z/(z²+35)为何0;;cos z/(z²−6z+10)为何0;;exp(−z)(2z+1)为何0;;主支log(z+3)为何0;;sec(z/2)为何0
8|_|证明0至π积分exp(cosθ)cos(sinθ)=π
9|a,b|A单连通，证明∫f'/(z−z0)=∫f/(z−z0)²;;去掉A单连通假设仍证明等式
10|_|整函数f满足f(z)/z→0，证明常数，题面附可去点提示
11|a,b,c,d,e,f|单位圆积分cos z/z;;单位圆积分sin z/z;;|z|=2积分z²/(z−1);;单位圆积分exp z/z²;;|z|=2积分(z²−1)/(z²+1);;|z|=2积分1/(z²+z+1)''',
5:'''1|a,b.i,b.ii|u=x³−3xy²+2x，验证调和;;用C-R方程积分求调和共轭;;识别f'=u_x−iu_y为z函数再积分求共轭
2|a,b|u=x/r²，证调和并找共轭v使u+iv解析;;u=(x²−y²)/r⁴，同问
3|_|速度场((x²−y²)/r⁴,2xy/r⁴)，证无散无旋并求复势
4|a,b|0<arg z<π/4楔内找非零调和ψ边界0;;以ψ等高线作流线，给无散无旋速度场
5|a,b,c|Φ=Az³,A>0，求势、流函数、速度;;画流线及速度场;;给可解释为壁面楔流的楔角
6|_|无散无旋场(u,v)，证明u调和
7|a,b,c,Challenge|单位圆盘边界T=sin²θ，求中心温度;;求最大温度;;求最小温度;;求整个圆盘内T(x,y)
8|a,b|Σ(n≥1)z^(−n)用比值判敛;;原点中心大圆上积分此f''',
6:'''1|a,b,c,d|判Σ[(1+2i)/(1−i)]^n;;判Σi^n;;判Σ[(1−i)/(1+2i)]^n;;判Σn!/10^n
2|a,b|Σz^(3n)/2^n收敛半径;;1+3(z−1)+3(z−1)²+(z−1)³收敛半径
3|a,b|Σa_nz^n半径R，求Σa_nz^(2n)半径;;求Σ(n≥1)n^(−n)a_nz^n半径
4|a,b|构造C去1上全纯、0简单零点、1本性奇点的f;;m阶零点f的f'/f有简单极点且留数m
5|a,b,c,d,e|1/(2cos z−2+z²)²在0极点阶数;;(z²+1)/(2z cos z)在0留数;;exp z/[z(z+1)³]全部孤立奇点及留数;;1/(1−z)无穷远留数;;cos z/[∫0^z f(w)dw]在0留数，f解析f(0)=1
6|a,b|z³exp(1/z)主部及留数;;(1−cosh z)/z³主部及留数
7|a,b|主支(1+z)^a在0的Taylor展开;;主支sqrt z能否在0<|z|有Laurent展开
8|a,b,c|1/(4−z²)在1 Taylor及半径;;1<|z−1|<R1 Laurent及R1;;|z−1|>3 Laurent
9|a,b,c||z|=3积分exp(iz)/[z²(z−2)(z+5i)];;单位圆积分exp(1/z)sin(1/z);;解释Cauchy公式是留数定理特例
10|a,b,c,d|πcot(πz)全奇点极点阶及留数;;正方形顶点±(N+1/2)±i(N+1/2)上积分πcot(πz)/z²;;用给定|cotπz|<2证明积分趋0;;计算Σ(n≥1)1/n²
Fun 1|_|用Σz^n/n²、Σz^n/n、Σz^n说明圆周上全、部分、无点收敛三种情况
Fun 2|a,b,c|(1+z)f'=2f,f(0)=1，求闭式;;直接由微分方程求幂级数系数;;对比闭式Taylor验证系数
Fun 3|_|证明第10题方形边上|cotπz|<2（竖边<1、横边<2）
Fun 4|_|证明Σn²a_nz^n与Σa_nz^n收敛半径相同''',
7:'''1|a,b,c|0至2π积分8/(5+2cosθ);;0至2π积分1/(3+2cosθ)²;;0至2π积分sin²θ/(a+bcosθ)，a>|b|>0
2|a,b,c|全实轴积分1/(x²+2x+2);;全实轴积分x²/[(x²+1)(x²+4)];;按图2π/3扇形证明0至∞积分1/(x³+1)=2π√3/9
3|a,b|全实轴积分cos2x/(x²+1);;全实轴积分cos2x/(x²+1)²
4|a,b|PV全实轴积分exp(3ix)/(x−2i);;推导PV积分cos x/(x−w)在Im w正负两种公式
5|a,b|PV积分exp(ix)/[(x−1)(x−2)]=πi(exp2i−expi);;证明0至∞积分sin²x/x²=π/2
6|_|0至∞积分sqrt x/(x²+1)
7|a,b|f为(−1,1)指示函数，计算Fourier变换;;用凹陷路径验证Fourier逆（必须处理端点）
Fun.1|a,b|Gaussian半轴积分exp(−x²)exp(2iωx)，用矩形求实部;;利用对称求Gaussian全Fourier变换
Fun.2|_|0至2π积分cos^(2n)θ，n=1,2,…
Fun.3|_|算PV全实轴积分x²/(x²+1)²，并比较普通广义积分''',
8:'''1|a,b,c,d,e|exp z像：0<y<π带;;x<y<x+2π斜带;;x>0,0<y<π半带;;1<x<2,0<y<π矩形;;x>0右半平面
2|a,b,c|右半平面到单位圆盘的分式线性映射，0→−1;;非恒等分式线性映射至多两不动点;;圆S外点z1关于S有唯一对称点z2（先证明直线）
3|a,b,c,d|右半平面边界u(0,y)=y/(1+y²)，验证旋转α的矩阵;;找右半平面至圆盘映射令边界φ=sinθ/2;;证明φ(w)=Im w/2;;拉回求u
4|a,b|z+1/z把|z|=a,a≠1映到指定椭圆;;求|z|=1像
5|a,b,c|上半平面边界实轴(−1,1)为0、其余1，求调和函数;;圆盘右侧−π/4<θ<π/4边界0、其余1（原分段与图冲突，须说明）;;π/4无穷楔两边0<r<1边值0、r>1边值1，求调和函数''',
9:'''1|a,b,c|匀速流加2i涡，复势、流函数、流线（手绘或Matlab/Mathematica）;;Milne-Thomson圆定理绕|z|=1圆柱，复势、流函数、流线;;解释两流无穷远匀速
2|a,b,c|z⁵−2z把|z|=3绕0几圈;;把|z|=1绕0几圈;;把|z|=3绕−2几圈
3|a,b|z³+9z+30在|z|<2无根;;z⁶+4z²−1在|z|<1恰两根
4|_|f闭圆盘邻域全纯且边界|f|<1，证明f−z内部恰一零点
5|a,b|G=(s+1)/[(s−1)(s−2)],k=4，解析判闭环稳定性;;画kG沿虚轴Nyquist曲线，算绕−1次数并对应前問（可用给定MIT小程序）
6|a,b,c,d|用软件等轴比例画(z+1/z)/2像：|z|=3/2;;|z+1/2|=3/2;;|exp(iπ/4)z+1/2|=3/2;;|z|=1'''
}

def source_blocks(n,sol):
 p=BASE/f'mit18_04_s18_pset{n:02d}{"_sol" if sol else ""}.txt'
 t=p.read_text(); markers=list(re.finditer(r'\[PDF PAGE (\d+)\]',t)); heads=list(re.finditer(r'^Problem ((?:Fun\.? ?)?\d+)\.',t,re.M)); result={}
 def pg(pos): return max(int(m.group(1)) for m in markers if m.start()<=pos)
 for i,m in enumerate(heads):
  end=heads[i+1].start() if i+1<len(heads) else t.index('MIT OpenCourseWare')
  text=t[m.start():end].strip()
  # Ignore next-page header when it is the only text before the next problem.
  pages=[pg(m.start())]
  for page in markers:
   if m.end()<page.start()<end:
    next_marker=next((x.start() for x in markers if x.start()>page.start()),end)
    rest=t[page.end():min(end,next_marker)]
    rest=re.sub(r'^\s*\d*\s*18\.04 Problem Set \d+, Spring 2018(?: Solutions)?\s*','',rest)
    rest=re.sub(r'Problems below here are not assigned\..*', '',rest,flags=re.S)
    if rest.strip(): pages.append(int(page.group(1)))
  key=m.group(1).replace('Fun.','Fun ').replace('  ',' ')
  result[key]={'pages':sorted(set(pages)),'text':text,'locator':m.group(0)}
 return result
manifest=json.loads((ROOT/'sources/complex-analysis/assessment-manifest.json').read_text())
files={Path(f['file']).name:f for f in manifest['files']}
sets=[]
for n,rows in DATA.items():
 q=source_blocks(n,False);s=source_blocks(n,True);problems=[]
 for row in rows.splitlines():
  number,paths,tasks=row.split('|',2); paths=paths.split(',');tasks=tasks.split(';;');assert len(paths)==len(tasks),(n,number)
  norm=number.replace('Fun.','Fun ')
  qb=q[norm];sb=s[norm]
  qpdf=f'mit18_04_s18_pset{n:02d}.pdf';spdf=f'mit18_04_s18_pset{n:02d}_sol.pdf'
  leaves=[]
  for part,task in zip(paths,tasks):
   loc=number if part=='_' else number+'.'+part
   leaves.append({'id':f'PS{n}.{loc}','original_part':None if part=='_' else part,'requirements':task,'question':{'file':str((BASE/qpdf).relative_to(ROOT)),'pdf_pages':qb['pages'],'locator':qb['locator']+('' if part=='_' else ' '+part)},'official_solution':{'file':str((BASE/spdf).relative_to(ROOT)),'pdf_pages':sb['pages'],'locator':sb['locator']+('' if part=='_' else ' '+part),'coverage':'present; completeness and correctness exceptions listed separately'},'figure_required':False,'software_requested':False,'external_book_reference':None,'chapter_overlap':[],'cross_ps_overlap':[]})
  tree={}
  for p in paths:
   node=tree
   for bit in p.split('.'):
    node=node.setdefault(bit,{})
  problems.append({'original_number':number,'id':f'PS{n}.{number}','optional':number.startswith('Fun') or (n==1 and number=='6') or (n==4 and int(number)>=8),'has_subparts':paths!=['_'],'part_tree':tree if paths!=['_'] else {},'leaf_count':len(leaves),'leaves':leaves,'source_question_block':{'file':str((BASE/qpdf).relative_to(ROOT)),'pdf_pages':qb['pages'],'locator':qb['locator']},'source_solution_block':{'file':str((BASE/spdf).relative_to(ROOT)),'pdf_pages':sb['pages'],'locator':sb['locator']}})
 sets.append({'problem_set':n,'question_pdf':files[qpdf],'official_solution_pdf':files[spdf],'paper_title':f'18.04 Problem Set {n}, Spring 2018','major_count':len(problems),'with_subparts_count':sum(p['has_subparts'] for p in problems),'without_subparts_count':sum(not p['has_subparts'] for p in problems),'leaf_count':sum(p['leaf_count'] for p in problems),'problems':problems})
lookup={leaf['id']:leaf for S in sets for P in S['problems'] for leaf in P['leaves']}
for id in ['PS1.1.d','PS3.5.a','PS3.5.b','PS4.3.b','PS7.2.c','PS8.5.b','PS8.5.c']:
 lookup[id]['figure_required']=True
for id in ['PS1.3.a','PS1.3.b','PS1.5.a.i','PS1.5.a.ii','PS1.5.b.i','PS1.5.b.ii','PS5.5.b','PS9.1.a','PS9.1.b','PS9.5.b','PS9.6.a','PS9.6.b','PS9.6.c','PS9.6.d']:
 lookup[id]['figure_required']=True
for id in ['PS9.1.a','PS9.1.b','PS9.5.b','PS9.6.a','PS9.6.b','PS9.6.c','PS9.6.d']:
 lookup[id]['software_requested']=True
# Exact or containment relations, not vague shared-topic matches.
overlap={'PS2.5':[('ch02.tex',1,'exact subproblem: |z|² differentiability')],'PS5.1.a':[('ch02.tex',2,'same u; preliminary harmonicity')],'PS5.1.b.i':[('ch02.tex',2,'exact task: same u, conjugate')],'PS5.1.b.ii':[('ch02.tex',2,'exact task: same u, second method required by source')],'PS7.3.b':[('ch07.tex',1,'contained specialization a=1,t=2')],'PS8.2.c':[('ch11.tex',2,'general statement vs numeric specialization')],'PS3.6':[('ch03.tex',1,'unit-circle integral supplies obstruction; not exact question')]}
for id,items in overlap.items():
 lookup[id]['chapter_overlap']=[{'chapter':f'subjects/complex-analysis/chapters/{f}','exercise':i,'relation':r} for f,i,r in items]
groups=[(['PS1.3.a','PS8.1.b'],'same logarithmic spiral exp((1+i)t), curve vs slit-plane mapping'),(['PS1.5.a.i','PS1.5.a.ii','PS8.1.a','PS8.1.c','PS8.1.d','PS8.1.e'],'same exponential coordinate grid, different region tasks'),(['PS8.4.a','PS9.6.a'],'same Joukowsky circle calculation; PS9 uses factor 1/2 and a=3/2'),(['PS8.4.b','PS9.6.d'],'same Joukowsky unit circle, scaled by 1/2'),(['PS8.2.a','PS8.3.b'],'PS8.3 reuses same half-plane/disk transform')]
for ids,relation in groups:
 for id in ids:lookup[id]['cross_ps_overlap'].append({'ids':[x for x in ids if x!=id],'relation':relation})
# Source pages at subpart precision when a major straddles pages.
qpages={'PS7.3.a':[1],'PS7.3.b':[1],'PS1.2.a':[1],'PS1.2.b':[1],'PS1.2.c':[2],'PS4.3.a':[1],'PS4.3.b':[2],'PS4.3.c.i':[2],'PS4.3.c.ii':[2],**{f'PS4.7.{x}':[3] for x in 'abcde'},'PS6.5.e':[2],**{f'PS6.5.{x}':[1] for x in 'abcd'},'PS6.10.a':[2],'PS6.10.b':[2],'PS6.10.c':[3],'PS6.10.d':[3],'PS7.Fun.1.a':[2,3],'PS7.Fun.1.b':[3],'PS8.3.a':[1],'PS8.3.b':[1,2],'PS8.3.c':[2],'PS8.3.d':[2],'PS8.5.a':[2],'PS8.5.b':[2],'PS8.5.c':[2,3],'PS9.5.a':[1],'PS9.5.b':[1,2]}
for id,pages in qpages.items():lookup[id]['question']['pdf_pages']=pages
# Solution locators retain original major block page ranges, which are honest searchable evidence.
counts={'major_total':sum(S['major_count'] for S in sets),'with_subparts':sum(S['with_subparts_count'] for S in sets),'without_subparts':sum(S['without_subparts_count'] for S in sets),'leaf_total':sum(S['leaf_count'] for S in sets),'assigned_major_total':sum(not P['optional'] for S in sets for P in S['problems']),'optional_major_total':sum(P['optional'] for S in sets for P in S['problems']),'assigned_leaf_total':sum(P['leaf_count'] for S in sets for P in S['problems'] if not P['optional']),'optional_leaf_total':sum(P['leaf_count'] for S in sets for P in S['problems'] if P['optional'])}
obj={'schema_version':1,'reviewer':'independent delegated Sol source/inventory review','review_date':'2026-10-08','scope':'MIT OCW 18.04 Spring 2018 Problem Sets 1–9 with official solutions, including all optional exercises','counting_convention':['Count every original Problem n, Problem Fun n, Problem Fun.n as one major, preserving original labels.','Count deepest explicit numbered/lettered terminal parts as leaves; a problem with no labeled parts is one leaf, even when it requests several computations or comparisons.','PS1.5(b) explicitly says repeat (a), so its three inherited (i),(ii),(iii) tasks are counted separately.','PS5.7 Challenge is one additional named leaf within Problem 7. It is included despite having no allocated points.','PS6 Fun1 three unnumbered series, PS4.2a two unnumbered formula proofs and PS7 Fun3 computation/comparison remain compound requirements within one leaf.','Do not omit zero-point, Fun, Challenge, figure or software tasks. Counts are structural leaves, not all unnumbered verbs.'],'counts':counts,'question_pages_semantics':'1-based physical PDF page order; source original locator preserved. Leaf ranges may encompass the original major when no finer split is needed.','source_transcription_boundary':'requirements are normalized inventory descriptions from actual PDF/text reading; original PDF is authoritative. This JSON is not a verbatim question transcription. Conjugate symbols resolved from rendered pages.','attribution':{'institution':'Massachusetts Institute of Technology','author':'Jeremy Orloff','course':'18.04 Complex Variables with Applications, Spring 2018','source_directory_url':'https://ocw.mit.edu/courses/18-04-complex-variables-with-applications-spring-2018/pages/problem-sets-and-solutions/','license':'CC BY-NC-SA 4.0 under MIT OCW default terms, subject to any separate notices','metadata_evidence':'sources/complex-analysis/18.04-spring-2018/assessment-html/problem-sets-and-solutions.html, instructor and CC footer'},'rights_review':{'all_18_pdfs_text_read':True,'separate_third_party_restriction_found':False,'personal_student_information_found':False,'external_book_exercise_reference_found':False,'notes':'Calendars, generic submit-to-Jerry instruction, official instructor/app URL and software names are course context. No student answers, student names/IDs or grades. Visual review is explicitly limited to listed rendered pages; no claim of all-page visual review.'},'sets':sets,'source_review_file':'subjects/complex-analysis/qa/assessment-review/ps-source-review.md'}
assert counts['major_total']==74 and counts['leaf_total']==179
(OUT/'ps-inventory.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(counts,ensure_ascii=False));print([(S['problem_set'],S['major_count'],S['with_subparts_count'],S['without_subparts_count'],S['leaf_count']) for S in sets])
