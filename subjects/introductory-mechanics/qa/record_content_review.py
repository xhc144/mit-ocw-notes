from pathlib import Path
import json,hashlib
ROOT=Path('/workspace/mit-ocw-notes');QA=ROOT/'subjects/introductory-mechanics/qa';CH=ROOT/'subjects/introductory-mechanics/chapters'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
j=json.loads((QA/'assessment-manuscript-review.json').read_text());inv=json.loads((QA/'assessment-inventory.json').read_text())
for name in j['read_complete_tex']:j['read_complete_tex'][name]=sha(CH/name)
for r in j['primary_problem_reviews']:
 r['manuscript_sha256']=sha(ROOT/r['manuscript_file']);r['review_status']='read_no_blocking_formula_found'
 if r['id']=='sc-ps2-4':r['note']='已复读修正：上2/下1，F拉上2向左，F=µg(m1+3m2)，全部小问完整。最终图另核。'
 if r['id']=='sc-ps6-1':r['note']='已复读修正：分量(跨河,下游)=(0.5,1.0)，原图θ=63.4°；互余26.6°单列说明。'
 if r['id']=='sc-ps8-5':r['note']='已复读图源码：K=E−U、负U与E均有箭头，势阱/力/转向速度正确。最终图另核；U/K在±0.45对称取等势高度。'
for r in j['advanced_problem_reviews']:r['manuscript_sha256']=sha(CH/'advanced-ps.tex')
notes={
 'exam1':[
 '四力式全部保留；(i)(ii)不成立。(b)原图左移/逆时针已恢复、接触滑速−V+ΩR<0→摩擦右；官方取消评分说明保留。',
 '轻轮F=2T；无滑共同a=F/(M1+M2)；滑动a1=F/(2M1)−µg、a2=F/(2M2)+µM1g/M2；阈值2µM1g(M1+M2)/(M2−M1)，阈值以上a1>a2；FBD视觉待查。',
 '归一λ0=Mπ/(2L)；自由端T(L)=0；T(z)=Mg(1+cosπz/L)/2，边界及方向正确。',
 '净摩擦是径向与切向合成；αmax=µg/r，ts=[((µg/r)²−α²)/α⁴]^(1/4)，需0<α≤αmax。',
 '壳层定理→ω²=4πGρ/3；准确T/量纲尺度=√(3π)，显式加速度已补。非均匀密度结论有包围质量更大条件；bonus质量/Schwarzschild数量级与牛顿风险推论边界分开。'],
 'exam2':[
 'm→右、2m静止，四末态完整；弹性仅(-v/3,2v/3)；三冲量第三最大；漏沙v不变、复合盘d/10、落粘土只水平动量守恒。',
 '已与原图核：m初向下/2m初右，2m末下；小球U=(2v,v)，√5v、atan(1/2)，ΔK=+2mv²。',
 'v²=2gR(1−cosθ)，接触N≥0，离球cosθ=2/3；顶点严格静止的扰动极限已交代。',
 '恒推力起动、耗半燃料时最高v、燃尽后制动距离；燃烧行程M0vex(1−ln2)/(2γ)−µgtb²/2独立积分成立；µ=0非有限距离单列。',
 '原F=−Amv²vhat保留；圆轨U,K,E；ΔE=−2πAGMm、Δr=−4πAr²、vr=−2A√(GMr)；弱阻力Ar≪1及恒星表面截止。'],
 'exam3':[
 '快速选择与全部备选保留；驱动轮上坡摩擦与自由前轮区别、陀螺进动向下、绕柱仅能量守恒；等冲量质心同速，典型非零末转动时偏心施力更大动能。',
 '原竖直杆、球自右撞上容器保留；LP=Mvd/2、I=3Md²/2→ω=v/(3d)逆时针；损Mv²/6、180°临界√(12gd)。',
 '枢轴功0、ω²=3g sinθ/d、θddot=3g cosθ/(2d)；杆给支点Fx=9Mg sinθcosθ/4、Fy=−Mg(1+9sin²θ)/4；符号及时间积分正确。',
 'I轮=3MR²、a=g/6、v²=gh/3；触地后重端松绳、轮/轻板速度连续的官方模型明确，总高度5h/3。',
 '原自旋向量−ωs(cosα rhat+sinα zhat)，Ω=ωsb/R向上。完整CM方程与Ldot给g tanα=RΩ²+(b/2)Ωωs−(5b/4)Ω²sinα；一阶L各分量核对成立，官方快自旋额外近似明示。'],
 'final':[
 '两行星速度/角动量比、Chasles全部四项、滑冰机械/总能量区别、G量纲保留；(e)只能定g垂轴向上，官方选斜右上；(f)原照片保留、官方总ω较陡右上及前翻说明正确，图待最终视觉。',
 '两个静摩擦运动条件与下行a=(2g/7)(1−2sinα−2µcosα)正确；轻块触地前有效。',
 'Mdotv=γu−Av²，耗尽v=vb/(1+Avbt/MR)；90°锥弹性反射纵向冲量mv，A=NmπR²，无误加2。',
 '原M盘右移且逆时针，2M盘静止下方；VC=v0/3，IC=25MR²/6，ωf=(3Rω0−8v0)/(25R)；一般能耗及官方不转特例19Mv0²/9区分正确。',
 'Δp向+y、点在+x侧、ΔL向+z、右端上升；小冲量α、细杆Ω向上正确；bonus tanαc=L/(2R)为几何阈值，官方Δpc≈MRLωs/(4r)超出小冲量适用范围的估算明确，不虚称一般精确冲量阈值已求。',
 '保持力−Mω²r0 rhat；释放r=r0 coshωt；离心/Coriolis与真实杆横向力2Mωrdot一致。',
 '原−Ar³rhat；Ueff=Ar⁴/4+L²/(2mr²)，唯一极小无真正拐点；L=0可过原点例外保留；vc=r0²√(A/m)，ωr=√(6Ar0²/m)，Tr/Torb=1/√6。']}
j['exam_problem_reviews']=[]
for a in inv['assessments']:
 if a['id'] not in notes:continue
 for p,note in zip(a['problems'],notes[a['id']]):
  j['exam_problem_reviews'].append({'id':a['id']+'-'+str(p['number']),'source_requests':p['subquestions'],'manuscript_file':'subjects/introductory-mechanics/chapters/exams.tex','manuscript_sha256':sha(CH/'exams.tex'),'review_status':'all published requests and options retained; independently checked mathematics with declared qualifications','note':note})
j['read_complete_tex']['exams.tex']=sha(CH/'exams.tex')
j['project_review']['numerics_status']='independently verified using mpmath elliptic integrals and SciPy DOP853, plus recalculated E/L from published CSV; see independent-numerical-review.json'
j['project_review']['numerical_source_sha256']=sha(ROOT/'subjects/introductory-mechanics/tools/numerics.py')
j['formula_sheet_review']={'status':'all 4 independent sheet content pages high-resolution visually read; merged formulas checked; e2 work-energy typo explicitly corrected','manuscript_sha256':sha(CH/'exams.tex'),'evidence':['qa/e1equations-p2.png','qa/e2equations-p2.png','qa/e3equations-p2.png','qa/e3equations-p3.png']}
j['status']='complete TeX content/math review of primary62/121, advanced13/34, exams22/80 and85reference objects; final PDF figures/display pending'
j['unreviewed']=['Final compiled PDF visual pages and newly added final vector/FBD renderings; raw source example solutions not all read word-for-word']
j['counts']={'primary_main':62,'primary_requests':121,'advanced_main':13,'advanced_requests':34,'exam_main':22,'exam_requests':80,'reference_only':85}
(QA/'assessment-manuscript-review.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
current={'status':'all 14 theory manuscripts read; substantive coverage map completed; no remaining major mathematical finding in read TeX; final PDF visual check pending','hashes':{p.name:sha(p) for p in sorted(CH.glob('ch*.tex'))},'read_limits':'The source narrative readpack is not a claim to have individually recalculated all original examples or read all PDF pages. The whole current Chinese theory and all reproduced assessment solutions were read. Thermal appendix14A remains explicitly cross-subject.'}
(QA/'theory-final-content-review.json').write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n')
print(j['status'])
