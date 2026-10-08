from pathlib import Path
import json,hashlib
R=Path('/workspace/mit-ocw-notes');O=R/'subjects/complex-analysis/qa/assessment-review';inv=json.loads((O/'ps-inventory.json').read_text())
# Filled only after actual continuous reading and independent mathematical checking.
CHECKS={
1:['乘除与主支幂指数、i^i全对数支、z^8和四根以及70度图五根复算','共轭指数与单位模逆元证明；商排除原点条件','z²三角形像抛物线系数与双向区域覆盖；exp(t(1+i))原曲线参数','根的几何和因子分解；n=1反例与n≥2条件','exp像圆/射线；z²两类抛物线及退化半轴；非零交点切向量正交','纯虚商等价式、完整圆逆向验证及1、−2排除'],
2:['cos指数导数与修正C-R；cot全部复零点及导数','乘积对数导数含重根；分式线性零行列式的c=0/c≠0分类','指数非单射及Log复合主条带和割线','双共轭全纯与单输入共轭的C-R符号，圆盘对称及常数结论','|z|²在0全方向极限，非零点实/虚方向差商','主支复合精确割线、D/E/G三支区别、z<−1符号及T/U延拓'],
3:['Cauchy条件、z²原函数及Green两实部旋度、1/z正确径向切向形式','bar z与bar z²两路径参数积分独立复算','圆心奇点阻止Cauchy；逆时针参数积分2πi','原函数端点+1、(1+i)^10=32i、sin/exp直角形式','上半圆1→−1主支立方根与换支因子；端点跳跃不改变积分','非零单位圆周期积分排全球单值原函数','明确反例左0右(1+i)/2；正确Re积分式','绕数障碍与割平面凸条带同胚、圆盘收缩、外域绕数'],
5:['给定u的Laplace零与两条共轭路线、积分常数实部条件','穿孔域1/z与1/z²两共轭、偏导正确','1/z²速度、−1/z复势及C-R无散无旋','z⁴楔映射/调和ψ/速度正确；图中方向箭头已按F左下修复并复核','Az³实/虚部、速度方向及六楔π/3；绘图级数极坐标构造正确','二阶混合偏导证明，无需全局势','中心均值1/2，闭盘极值与开盘sup/inf，温度(1−x²+y²)/2','几何级数判敛边界、圆周一致收敛交换积分及Cauchy替代'],
6:['四级数模/比值判据','稀疏幂级数半径2^(1/3)、有限多项式∞','sqrt R包含边界情形；n^(−n)权正半径∞及R=0的通用根式',"显式本性函数简单零点；f'/f零点分解留数m",'8阶极点首系数1/144；1/2；第三阶留数−5/(2e)；无穷远1；原函数分母留数1','两主部完整负幂及1/24、−1/2留数','广义二项式系数；主支sqrt无完整环域Laurent及绕数矛盾','z−1三层几何展开、分母负幂、两距离1/3','两圆内留数独立复算，0处(−12+5i)/100；本性乘积留数1；Cauchy特殊情形','cot整数简单留数1；0三阶−π²/3；正确方形周长与Σ=π²/6','边界全点、部分点、无点收敛；几何和界+Dirichlet','微分方程闭式、幂级数递推、两法系数对照','竖边|1−t|/(1+t)<1及横边q估计<2','n^(2/n)→1双向半径，含0/∞']
}
CHECKS[7]=['三角积分z替换；两二阶留数与一般a,b内外根判定及2π(a−Δ)/b²','两实有理积分留数/大弧界；2π/3扇形斜边相位与唯一极点','cos2x指数替换、πe^(−2)与3πe^(−2)/2及绝对收敛界','上/下矩形指数衰减和顺逆时针方向；复w分解两指数所得分段式','两实简单极点上凹口半留数与正号；sin²/x²先复化再取实部','sqrt钥匙孔两岸符号、两本支留数及大小弧界','Fourierω=0补值、J(a)凹口两方向、跳跃点1/2及对称PV说明','Gaussian矩形四边指数符号/右边界；缩放与偶性含负/零频率','二项式唯独k=n给留数；2πi因子修正','绝对收敛确保PV=广义积分；二阶留数−i/4独立复算']
CHECKS[4]=['Cauchy4πi、−π、bar z沿圆替换残和0、波浪路径端点−.486及漏1/3校订','不用待证公式的缩圆/二项式直算两公式；多项式四系数筛选','|z|exp z沿圆替换；全实轴π/6大弧界/绝对收敛；两个局部圈及2!、扩大圆独立第二法','任意内部点Cauchy公式，闭区域开邻域解释','外Cauchy零、内cos z连续趋cos(1+i)，正/负方向区别','圆周参数微分相消、一般n阶权与r幂','逐项核对两分母外极点、整函数、主log割线及sec全部复奇点','单位圆exp z/z值和虚部；2π−θ对称严格化半区间','单连通内外两种Cauchy；有洞时g单值作g导数全球闭路周期零','可去g(0)=f′(0)完整定义/最大模矛盾；独立移心Cauchy估计全域常数','六积分Cauchy函数值/导数，两个分式有限根及留数/部分分式相消']
CHECKS[8]=['exp像按r=e^x、模2π辐角逐域核对；斜带螺线唯一原像','Cayley两向不等式/逆式；不动点含∞的分类；圆反射唯一及中心↔∞','旋转矩阵、虚轴变换边值、选择调和解及增长无约束非唯一性、拉回y/((x+1)²+y²)','Joukowsky整圈椭圆覆盖、a>0及a<1走向、a=1往返实段','上半平面两个Arg的边值三段；原题冲突声明；corrected k=1+√2逆式/三点/Im正/u(0)=3/4；楔z⁴两边r<1对应']
CHECKS[9]=['涡位2i、复势/ψ和速度符号；圆定理bar U/z镜像、导数与单位圆ψ=0、远场按速度；45条流线9486点及18箭头独立数值核对','三圈Rouché界与绕目标−2对应f+2，0处次数5/1/5','两不等式12>8与3>1、实正负根确保两个不同根','Rouché总重数1及简单根结论','闭环极点(−1±i sqrt23)/2；Nyquist实虚部、向上虚轴顺时针闭合P−Z=2及t参数箭头','四圆参数、椭圆13/12和5/12、b的z=1临界尖点、c的旋转参数、d实段往返；Matlab四问axis equal']
records=[]
for S in inv['sets']:
 n=S['problem_set']
 if n not in CHECKS:continue
 f=R/f'subjects/complex-analysis/chapters/assessments/ps{n:02d}.tex';t=f.read_text();notes=CHECKS[n];assert len(notes)==S['major_count'];assert f.read_bytes()==(O/f'ps-reviewed-{n:02d}.tex').read_bytes(), 'Body differs from actually reviewed snapshot; diff and review before regenerating hashes'
 records.append({'problem_set':n,'file':str(f.relative_to(R)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'actual_continuous_read':True,'major_count':S['major_count'],'leaf_count':S['leaf_count'],'status':'mathematics_and_coverage_pass','scope_limit':'source code mathematics and task coverage; final compiled PDF visual/layout inspection not included','major_checks':[{'id':P['id'],'leaf_ids':[L['id'] for L in P['leaves']],'checked':note} for P,note in zip(S['problems'],notes)]})
obj={'reviewer':'independent delegated Sol source/inventory reviewer; not an author of ps01–09.tex','date':'2026-10-08','inventory_file':'subjects/complex-analysis/qa/assessment-review/ps-inventory.json','read_leaf_count':sum(x['leaf_count'] for x in records),'total_leaf_count':179,'records':records,'resolved':['PS5.4b arrow fix rechecked: (.9,.64)→(.844,.448), parallel to true left/down velocity.'],'outstanding':['Final PDF visual and layout review is separate.']}
v=O/'ps-final-visual.json'
if v.exists():
 visual=json.loads(v.read_text())
 if visual.get('status')=='PASS':
  obj['outstanding']=[]
  obj['final_visual_review']=str(v.relative_to(R))
  obj['final_pdf_sha256']=visual['final_pdf_sha256']
(O/'ps-text-review.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('Read leaves:',obj['read_leaf_count'],'Mathematics pass leaves:',sum(x['leaf_count'] for x in records if x['status']=='mathematics_and_coverage_pass'))
