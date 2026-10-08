# Recitation 原题库存与源答案审校

审核日期：2026-10-08。独立委派 Sol 审稿。仅审原题库存与源数学；尚未审新增中文题解和成书。

实际通读24份PDF的全部56页（题卷24页，答案32页）；文本提取符号丢失处已看原页，12张全部页序联系图均已实际查看，另放大复核rec3、11、12、13的关键页。来源文件SHA-256及各页序绑定于 `rec-inventory.json`。仓库及/workspace内未发现AGENTS.md。已读vendor数学讲义SKILL、writing-and-proof、research-and-sources及review-gates。

## 冻结计数

按原卷最末级数字题号计叶项；整题没有细号便计一个叶项。同一编号内的“计算、判断、解释、作图”列为作答义务，不拆出虚构题号。共44大题/84印刷叶项，其中rec6 3.4仅阅读看图，数学解答叶项为83。原卷无(a)(b)字母子问。rec2两个4.3保留为first/second。官方无rec10，不列为下载缺项。

|Recitation|大题|印刷叶项|数学叶项|题卷PDF页数|答案PDF页数|
|---|---:|---:|---:|---:|---:|
|1|4|10|10|2|2|
|2|4|13|13|2|2|
|3|3|7|7|2|4|
|4|4|8|8|2|3|
|5|2|2|2|2|2|
|6|3|9|8|2|3|
|7|4|5|5|2|2|
|8|4|9|9|2|2|
|9|4|4|4|2|3|
|11|2|6|6|2|3|
|12|5|5|5|2|2|
|13|5|6|6|2|4|

## 每叶项定位与全部作答义务

H=handout、S=solutions，页码均指PDF文件页序，从1开始，不将MIT尾页算作题目。各卷H全部题目均在p1，H p2均为官方来源/条款页。完整路径由各卷文件名与JSON给出。

### Recitation 1

文件：`mit18_04s18_recit1-handout.pdf` / `mit18_04s18_recit1-solutions.pdf`。

|原叶号（必要时区分位置）|H页|全部作答义务|S定位与状态|独立核对结果/补全目标|
|---|---:|---|---|---|
|1.1|1|判断 e^{log z}=z；判断 log(e^z)=z|p1；第一问直接核算；第二问转指 problem set 2；partial|前式 z≠0 时成立；多值 log(e^z)={z+2πik}，主值须检查虚部区间|
|1.2|1|由一个 log z 值给出全部其他值|p1；Ans under 1.2；direct|w+2πik，k∈Z|
|2.1|1|计算 z1=2e^{iπ/3} 的所有对数；给出主值|p1；Ans under 2.1；direct|log2+iπ/3+2πik；主值 k=0|
|2.2|1|计算 z2=3+4i 的所有对数；给出主值|p1；Ans under 2.2 未单列主值；partial|log5+i arctan(4/3)+2πik；主值 k=0|
|3.1|1|判断 z^a 的单值或多值性；解释原因|p1；Ans under 3.1；needs_qualification|一般随对数分支改变，但 a∈Z 时单值；z≠0|
|3.2|1|判断 a∈Z、z≠0 时 z^a 的单值性|p1；Ans under 3.2；direct|单值，因为 e^{2πika}=1|
|3.3|1|a 为实数时，比较全部 a 次幂的共同性质|p1；Ans under 3.3；direct|同模 \|z\|^a|
|3.4|1|a 为纯虚数时，比较全部 a 次幂的共同性质|p1；Ans under 3.4；direct|各值的比为正实数，故主辐角相同|
|4.1|1|计算 z1^{z2} 的所有值|p1；Ans under 4.1；direct|e^{3log2−4π/3}e^{i(4log2+π)}e^{−8πk}，k∈Z|
|4.2|1|计算 z1^{1/4}；数清不同值；在复平面画出全部值|p1；Ans under 4.2 给出四值但未画图；partial|2^{1/4}e^{i(π/12+kπ/2)}，k=0,1,2,3；须画四点|

### Recitation 2

文件：`mit18_04s18_recit2-handout.pdf` / `mit18_04s18_recit2-solutions.pdf`。

|原叶号（必要时区分位置）|H页|全部作答义务|S定位与状态|独立核对结果/补全目标|
|---|---:|---|---|---|
|1.1|1|用复导数定义证明共轭函数不可复微|p1；Ans under 1.1 回指下一问；direct|增量商为 conjugate(h)/h，实与纯虚方向为1、−1|
|1.2|1|求 z→0 时 conjugate(z)/z 的所有可达极限值|p1；Ans under 1.2；needs_qualification|整体极限不存在；沿路径可得任一单位圆点 e^{−2iθ}|
|2.1|1|写出 cos z 的实虚部；写出 sin z 的实虚部|p1；Ans under 2.1；direct|cos z=cos x cosh y−i sin x sinh y；sin z=sin x cosh y+i cos x sinh y|
|2.2|1|把两函数实虚部限制在实轴；限制在虚轴|p1；Ans under 2.2 回指2.1；direct|cos x、sin x；cos(iy)=cosh y，sin(iy)=i sinh y|
|2.3|1|判断 cos z、sin z 是否有界|p1；Ans under 2.3；direct|在 C 上均无界|
|2.4|1|判断 cos²z+sin²z=1 是否成立|p1；Ans under 2.4；direct|对全部复数成立|
|3.1|1|证明 e^z 连续|p1；Ans under 3.1；direct|实虚部 e^x cos y、e^x sin y 连续|
|3.2|1|由前问证明 cos z、sin z 连续|p1；Ans under 3.2；direct|指数函数线性组合连续|
|3.3|1|判断共轭函数连续性；解释与Q1是否矛盾|p1；Ans under 3.3；direct|连续；连续不推出复可微|
|4.1|1|为 e^z、z²、cos z、sin z 分别写 u+iv|p1；末段回指 notes 和 problem set 2；reference_only|除三角式外：e^x(cos y+i sin y)，z²=x²−y²+2ixy|
|4.2|1|对四函数各求 ux、uy、vx、vy；检验CR|p1；末段回指 notes 和 problem set 2；reference_only|四函数全满足CR，须把16个偏导写全|
|4.3-first|1|分别给出四函数的复导数|p1；第一个印刷4.3；末段回指 notes；reference_only|e^z、2z、−sin z、cos z|
|4.3-second|1|对共轭函数重复前面实虚部分解、偏导与CR检验；解释与Q1是否一致|p1；第二个印刷4.3；末段说CR不满足；partial|u=x,v=−y；ux=1,uy=0,vx=0,vy=−1；不满足CR，处处无复导数|

### Recitation 3

文件：`mit18_04s18_recit3-handout.pdf` / `mit18_04s18_recit3-solutions.pdf`。

|原叶号（必要时区分位置）|H页|全部作答义务|S定位与状态|独立核对结果/补全目标|
|---|---:|---|---|---|
|1|1|在 u,v∈C² 条件下证明全纯函数的导函数全纯|p1；Ans under Q1；direct|f′=ux+i vx；混合偏导可交换，导函数满足CR|
|2.1|1|证明 ∫conjugate(z)dz 不路径无关；说明为何不违反基本定理|p1；Ans under 2.1 只算圆周积分；partial|正向单位圆积分2πi；共轭函数无全纯原函数|
|2.2|1|对全部整数 n 计算正向单位圆 ∫z^n dz；说明与基本定理一致|p1；Ans under 2.2；direct|n=−1 时2πi，其余0；n≠−1 的显式原函数|
|2.3|1|判断圆盘不含0时Q2.2答案是否改变|p1；Ans under 2.3；direct|全部0；圆盘邻域有 log 分支|
|3.1|1|求0<x<π竖条内水平线、垂直线的像；判断 cos 的单射性|p1,2；Ans under 3.1 在p1，附图在p2；partial_with_error|非退化水平线为半椭圆；垂直线为单支双曲线；y=0 为线段、x=π/2 为虚轴；cos在竖条内单射|
|3.2|1|加入 x=0,y≥0 与 x=π,y>0 后求值域；判断单射性|p3；Ans under 3.2 错称entire complex plane；error|值域 C\{−1}，仍单射；−1只能对应π+2πk，不在原域|
|3.3|1|给出上述反余弦单值选取的割线|p3；Ans under 3.3；needs_qualification|解析分支用 C\((−∞,−1]∪[1,∞))；边界单值选取在外侧实射线上跳跃，±1是分支点|

### Recitation 4

文件：`mit18_04s18_recit4-handout.pdf` / `mit18_04s18_recit4-solutions.pdf`。

|原叶号（必要时区分位置）|H页|全部作答义务|S定位与状态|独立核对结果/补全目标|
|---|---:|---|---|---|
|1.1|1|对正向上半圆盘边界用Cauchy公式算 ∫dz/(1+z²)²|p1；Ans below 1.3: Example 4.11；reference_only|R>1，闭轮廓积分π/2；被称作semicircle但包含直径|
|1.2|1|分离直径和半圆弧；用积分三角不等式估计弧积分|p1；Ans below 1.3: Example 4.11；reference_only|弧积分模≤πR/(R²−1)²|
|1.3|1|给出直径积分估计；令R→∞求实积分|p1；Ans below 1.3: Example 4.11；reference_only|\|∫_{−R}^R dx/(1+x²)²−π/2\|≤πR/(R²−1)²，极限π/2|
|2.1|1|用导数积分公式与三角不等式证明Cauchy估计|p1；Ans under 2.1: Theorem 4.15；reference_only|\|f^{(n)}(z0)\|≤n! MR/R^n|
|2.2|1|以n=1及整函数有界推出Liouville结论|p1；Ans under 2.2: Theorem 4.16；reference_only|对每一点令R→∞得f′=0，f常数|
|3.1|1|无根假设下证明1/P整且有界；用Liouville导出矛盾|p1；Ans below 3.2: notes 4.7.2；reference_only|n≥1；大圆外\|P\|→∞，圆内用连续非零的最小模|
|3.2|1|迭代第一根分解，证明恰有n根，计重数|p1；Ans below 3.2: notes 4.7.2；reference_only|除以每个线性因子，归纳降低次数|
|4|1|从Cauchy公式证明圆周均值性质|p2；Ans continued on p2: Theorem 4.18；reference_only|f(z0)=(1/2π)∫_0^{2π}f(z0+Re^{iθ})dθ|

### Recitation 5

文件：`mit18_04s18_recit5-handout.pdf` / `mit18_04s18_recit5-solutions.pdf`。

|原叶号（必要时区分位置）|H页|全部作答义务|S定位与状态|独立核对结果/补全目标|
|---|---:|---|---|---|
|1|1|由四条给定边温求方形板上的全局最高、最低温度|p1；Ans under Q1；direct|最大200位于(1,1)，最小0位于(0,0)；要求内域调和且闭板连续|
|2|1|证明u=sin x cosh y调和；求调和共轭|p1；Ans under Q2 求f=sin z但未显式写v；partial|v=cos x sinh y+C|

### Recitation 6

文件：`mit18_04s18_recit6-handout.pdf` / `mit18_04s18_recit6-solutions.pdf`。

|原叶号（必要时区分位置）|H页|全部作答义务|S定位与状态|独立核对结果/补全目标|
|---|---:|---|---|---|
|1.1|1|用边界B与u表达闭圆盘A上的最大值|p1；Ans under 1.1；direct|max_B u；需连续到边界|
|1.2|1|用边界B与u表达闭圆盘A上的最小值|p1；Ans under 1.2；direct|min_B u|
|1.3|1|用半径2的边界值表达u(0,0)|p1；Ans under 1.3；direct|(1/2π)∫_0^{2π}u(2cosθ,2sinθ)dθ|
|2.1|1|在目标域A单连通时证明u∘Φ调和|p1；Ans under 2.1；direct|u=Re f，u∘Φ=Re(f∘Φ)|
|2.2|1|判断能否去掉A单连通假设；证明判断|p1；Ans under 2.2；direct|能；Δ(u∘Φ)=\|Φ′\|²(Δu)∘Φ=0|
|3.1|1|求双源Φ=log(z−1)+log(z+1)的速度场|p2；Ans under 3.1 写φ及梯度但未展开速度分量；partial|F=(Re[2z/(z²−1)],−Im[2z/(z²−1)])；z≠±1|
|3.2|1|证明在y轴上流动沿y轴|p2；Ans under 3.2；direct|φx(0,y)=0，y轴为流线（去除停滞点）|
|3.3|1|求停滞点|p2；Ans under 3.3；direct|仅z=0；±1是源点不属速度定义域|
|3.4|1|阅读Topic6，查看双源流线并延伸讨论|p2；题目重述；无独立Ans；reading_instruction|须保留阅读任务；可自绘 Im log(z²−1)=常数的流线，不要求软件|

### Recitation 7

文件：`mit18_04s18_recit7-handout.pdf` / `mit18_04s18_recit7-solutions.pdf`。

|原叶号（必要时区分位置）|H页|全部作答义务|S定位与状态|独立核对结果/补全目标|
|---|---:|---|---|---|
|1|1|在0<\|z\|<1展开 (z+1)/(z³(z²+1)) 的Laurent级数|p1；Ans under Q1: Example 7.22；reference_only|Σ_{k≥0}(−1)^k(z^{2k−3}+z^{2k−2})|
|2.1|1|在0<\|z\|<1展开1/[z(z−1)]|p1；Ans below 2.2: Example 7.23；reference_only|−Σ_{k≥0}z^{k−1}|
|2.2|1|在1<\|z\|<∞展开1/[z(z−1)]|p1；Ans below 2.2: Example 7.23；reference_only|Σ_{k≥0}z^{−k−2}|
|3|1|已知单位圆盘内某实线段上f=5，求f(i/2)；把线段改为x−3i/4后再判断|p1；Ans under Q3 仅论证原线段的0聚点；partial|两种均为5；第二种聚点为−3i/4而不是0|
|4|1|用幂级数解f′=f+2、f(0)=0|p1；Ans under Q4: Example 7.24；reference_only|f(z)=2(e^z−1)=2Σ_{n≥1}z^n/n!|

### Recitation 8

文件：`mit18_04s18_recit8-handout.pdf` / `mit18_04s18_recit8-solutions.pdf`。

|原叶号（必要时区分位置）|H页|全部作答义务|S定位与状态|独立核对结果/补全目标|
|---|---:|---|---|---|
|1.1|1|证明g在z0单零点则1/g为单极点|p1；Ans below 1.3: Section8 p5 Property5；reference_only|g=(z−z0)h，h(z0)≠0|
|1.2|1|证明Res(1/g,z0)=1/g′(z0)|p1；Ans below 1.3: Section8 p5 Property5；reference_only|由h(z0)=g′(z0)得到|
|1.3|1|求1/sin z全部极点；证明单极点；算留数|p1；Ans below 1.3: Example8.11；reference_only|z=kπ，单极点，留数(−1)^k|
|2.1|1|证明p/q的单极点留数公式（p(z0)≠0、q单零点）|p1；Ans below 2.2: Example8.13；reference_only|Res=p(z0)/q′(z0)|
|2.2|1|求cot z全部极点；证明单极点；算留数|p1；Ans below 2.2: Section8.4.3；reference_only|z=kπ，单极点，留数1|
|3|1|利用sin、cos的Taylor级数求cot在0的Laurent前几项|p1；Ans under Q3: Example8.17；reference_only|cot z=1/z−z/3−z³/45−2z⁵/945+…，0<\|z\|<π|
|4.1|1|用扩展Cauchy定理证明一个内部孤立奇点的留数公式|p1；只重述题，无Ans；missing|内部须属解析域；挖小圆后等值，积分=2πi Res|
|4.2|1|用扩展Cauchy定理证明两个内部孤立奇点的公式|p1；只重述题，无Ans；missing|挖两个小圆，积分为两留数之和乘2πi|
|4.3|1|推广到有限多个内部孤立奇点，证明留数定理|p1；只重述题，无Ans；missing|闭内部包含在A，挖有限多个小圆；内部留数和|

### Recitation 9

文件：`mit18_04s18_recit9-handout.pdf` / `mit18_04s18_recit9-solutions.pdf`。

|原叶号（必要时区分位置）|H页|全部作答义务|S定位与状态|独立核对结果/补全目标|
|---|---:|---|---|---|
|1|1|求∫_R dx/(1+x⁴)|p1；Ans under Q1: Example9.4；reference_only|π/√2|
|2|1|求∫_0^{2π}dθ/(2−sinθ)|p1；Ans under Q2；direct|2π/√3|
|3|1|求∫_0^{2π}sin^{2n}θ dθ|p1,2；Ans begins p1, ends p2；direct|n∈Z≥0；2π(2n)!/[2^{2n}(n!)²]|
|4|1|求∫_1^∞dx/[x√(x²−1)]|p2；Ans under Q4: Example9.8；reference_only|π/2；实轴取正平方根|

### Recitation 11

文件：`mit18_04s18_recit11-handout.pdf` / `mit18_04s18_recit11-solutions.pdf`。

|原叶号（必要时区分位置）|H页|全部作答义务|S定位与状态|独立核对结果/补全目标|
|---|---:|---|---|---|
|1.1|1|构造y>x tanα半平面到单位圆盘的LFT|p1；Ans under 1.1；needs_qualification|令β=arctan(tanα)∈(−π/2,π/2)，再用(e^{−iβ}z−i)/(e^{−iβ}z+i)；原旋转α需cosα>0|
|1.2|1|构造0<y<π条带到上半平面的共形双射|p1；Ans under 1.2；direct|e^z|
|1.3|1|构造上半单位圆盘到上半平面的共形双射|p1；Ans under 1.3；direct|T(z)=−i(z−1)/(z+1)到第一象限，再平方|
|1.4|1|构造0<y<π,x<0无限井到上半平面的共形双射|p1；Ans under 1.4 误回指2.3，应1.3；direct_with_typo|e^z到上半圆盘，再接1.3；Wπ的条件须保留x<0|
|2.1|1|求点z1在实轴的反射|p1；Ans under 2.1；direct|conjugate(z1)|
|2.2|1|由LFT—直线反射—逆LFT定义求单位圆反射|p1,2；Ans begins p1, finishes p2；direct|1/conjugate(z2)；球面上0与∞互换|

### Recitation 12

文件：`mit18_04s18_recit12-handout.pdf` / `mit18_04s18_recit12-solutions.pdf`。

|原叶号（必要时区分位置）|H页|全部作答义务|S定位与状态|独立核对结果/补全目标|
|---|---:|---|---|---|
|1|1|用Rouché证明z⁵+3z+1的5根全在\|z\|<2|p1；Ans under Q1: Example11.7；reference_only|\|z⁵\|=32>7≥\|3z+1\||
|2|1|用Rouché证明z+3+2e^z在左半平面恰有一零点|p1；Ans under Q2: Example11.8；reference_only|左半圆边界：虚轴\|z+3\|≥3>2；左弧R>5时\|z+3\|≥R−3>2；每个左侧零点\|z\|<5|
|3|1|用Rouché另证n次首一多项式恰有n根（计重数）|p1；Ans under Q3: Theorem after Example11.8；reference_only|大圆上首项严格压过低次项|
|4|1|证明H=G/(1+G)的极点数与G极点数及Ind(G∘γ,−1)关系|p1；Ans under Q4；direct_needs_domain|G极点在H处可去；H极点恰是1+G零点同阶；非正向Jordan曲线须以绕数加权并要求闭内部属亚纯域|
|5|1|对源点0与墙y=±1确定镜像源数量；给出复势|p1；Ans under Q5 末式指标和收敛均错误；error|所有±2ni，n≥1；配对正则化 Φ=log z+Σ_{n≥1}log(1+z²/(4n²))=Log[(2/π)sinh(πz/2)]（局部选支）|

### Recitation 13

文件：`mit18_04s18_recit13-handout.pdf` / `mit18_04s18_recit13-solutions.pdf`。

|原叶号（必要时区分位置）|H页|全部作答义务|S定位与状态|独立核对结果/补全目标|
|---|---:|---|---|---|
|1|1|求L(sinωt;s)，ω∈R|p1；Ans under Q1 多出收敛域询问；direct|ω/(s²+ω²)，Re s>0；ω=0的零函数另处理|
|2|1|证明一阶导数的Laplace公式；再证明二阶导数公式并用f′指数型条件|p1；Ans under Q2；direct_needs_regular|sF−f(0)；s²F−sf(0)−f′(0)；须给可分部积分的正则性|
|3|1|证明L(tf)=−dF/ds；据此求所有n≥0的L(t^n)|p1,2；Ans begins p1, polynomial transforms p2；direct_needs_justification|n!/s^{n+1}；用半平面紧集上的t e^{−δt}控制说明换微分与积分|
|4.1|1|解释常函数1与阶跃函数为何有相同单边Laplace变换|p2；Ans under 4.1；direct|t=0的未指定值任意；负半轴不参与积分|
|4.2|1|解释e^{at}只在t=2改为0为何不改变Laplace变换|p2；Ans under 4.2；direct|单点修改积分不变，Re s>Re a|
|5|1|用Laplace与部分分式解x″+8x′+7x=e^{−2t}、x(0)=0、x′(0)=1|p2,3；Ans begins p2, ends p3，末行误写X；direct_with_typo|x(t)=e^{−t}/3−e^{−2t}/5−2e^{−7t}/15；代入初值与ODE均满足|

## 重合核对

原ch01–14共38个exercise环境逐一读取，其完整题面、文件、行号在JSON。没有把理论章节中的例题混算为这38题。

|原卷叶项|现有自设题|关系|说明|
|---|---|---|---|
|rec01-q4.2|ch01-exercise-1|same_method|四次根的数目与几何位置，底数不同，无同题全文重合|
|rec02-q2.1|ch01-exercise-2|partial|复正弦实虚部分解；自设题另求矩形上最大模|
|rec02-q2.3|ch01-exercise-2|related|全平面无界与紧矩形上的最大模并非同问|
|rec02-q4.2|ch02-exercise-1|same_method|CR与复可微判别；函数不同|
|rec03-q2.2|ch03-exercise-1|partial_exact|n=−1的单位圆积分是自设题的第二部分|
|rec04-q1.3|ch07-exercise-1|special_case|自设Fourier型积分取a=1,t=0便是原卷实积分；原卷另指定Cauchy公式路线|
|rec04-q2.1|ch04-exercise-2|special_case|自设题是R=1,z0=0,n=1,MR≤1的导数估计|
|rec04-q2.2|ch04-exercise-1|same_method|Liouville用于Re f有上界，自设题有指数辅助函数|
|rec04-q2.2|ch04-exercise-3|same_method|Liouville加远处趋零，非同一命题|
|rec06-q2.2|ch09-exercise-3|equivalent_core|调和复合不变及Δ复合公式是同一核心证明；原卷Q2.1另要单连通共轭路线|
|rec07-q3|ch05-exercise-2|same_method|恒等定理；常值线段与cos在实轴/整数的比较不同|
|rec08-q1.3|ch06-exercise-1|same_method|奇点分类与留数，具体函数不同|
|rec08-q2.1|ch06-exercise-2|same_method|留数求法，自设题为二阶极点|
|rec11-q1.3|ch11-exercise-3|same_method|象限/扇形幂映射后接Cayley变换；域不同|
|rec11-q2.2|ch11-exercise-2|same_method|圆反射的平移缩放推广，自设圆心半径不同|
|rec12-q1|ch08-exercise-1|same_method|Rouché，多项式、圆半径及数根结果不同|
|rec12-q4|ch08-exercise-3|same_method|辐角原理与零极点数，无同题|
|rec13-q1|ch12-exercise-2|partial_exact|sin t变换是自设题ω=1的基础步骤；自设另有延迟|
|rec13-q3|ch12-exercise-2|partial|自设t sin t为乘t微分公式应用；原卷求一般f与所有t^n|
|rec13-q5|ch12-exercise-1|same_method|Laplace解初值ODE，阶数和强迫项不同|

其中rec6 Q2.2与ch09第3题的核心证明等价，rec3 Q2.2的n=−1与ch03第1题的单位圆部分完全重合；其余为特殊化、部分任务或方法关联。不能据此删掉原卷叶项。38题中未列出的题未发现与原卷的具体作答任务重合，主题相同不自动等于重复题。

Recitations内部关联：

- rec02-q2.1, rec02-q4.1, rec03-q3.1：复sin/cos实虚部公式在CR与映射问题中复用，不删题。
- rec04-q4, rec06-q1.3：解析函数均值与调和函数圆心均值；对象不同但同一均值机制。
- rec04-q2.2, rec04-q3.1, rec12-q3：代数基本定理两个独立路线：Liouville与Rouché；不能合并。
- rec01-q3.4, rec03-q3.3, rec06-q3.1, rec12-q5：对数多值与分支只属主题关联，题目数据不同。
- rec03-q2.2, rec08-q4.1：单项幂积分是一般留数公式的基础计算，非重复完整题。
- rec08-q1.2, rec08-q2.1：后式是前式的解析分子推广，原卷分别要求证明。
- rec11-q1.2, rec11-q1.4：同用e^z，后式域限制后再接半圆盘映射，非重复。
- rec13-q2, rec13-q5：导数变换公式用于ODE，前者证明、后者应用。

## 作图、软件、来源和个人信息

- rec1 4.2明确要求在复平面画出全部四次根。源答案只有四值，缺图；中文题解必须补图或足够明确的坐标/标注图示。
- rec3 S p2提供cos映射前后网格图，已实际查看；不复制受限外部图片，按公式自绘可得到相同数学信息。
- rec6 3.4是查看Topic6流线和讨论的阅读任务；须保留任务，不能伪造为官方无此子问。
- 12份题卷均无指定软件计算、编程、MATLAB或数值实验任务。
- 24份PDF末页均为MIT OCW、课程名、Spring2018及引用/条款URL；未见额外的逐图受限标识。PDF未直接印CC版本，保留官方/仓库中的CC许可来源，不能把末页条款URL冒写为具体授权文本。
- 全部24份页首是公开学术署名Vishesh Jain；保留作者与2018年份。未发现学生姓名、学号、邮箱、成绩、个人批注或填卷信息。

## 审查边界

只写rec-*审核记录，未改源PDF或正文。参照讲义的例题/定理编号按答案PDF如实记录；本次没有重新读取所有被引用的官方讲义段落，因此reference_only表示本答案PDF并非自足，而非已验证对应讲义内容。独立计算、逐页读图和新增中文正文审查分别记录；后者尚待后续任务。


## 需要明确修正或补齐的原答案

**rec1（H/S p1）。** 1.1第二等式在多值意义下只表示z是log(e^z)的一值，不能把多值集合等于单值z；主对数时有虚部取值限制。1.2和3.1–3.4采用复对数定义应明确z≠0；3.1源泛称“multivalued”，整数a例外已在3.2给出。2.2源没再单列主值。4.2官方未附所要求的根图，需补四点图，模2^{1/4}、角π/12+kπ/2。

**rec2（H/S p1）。** 1.2的全局极限不存在，原“can attain”是沿不同趋近路径可得的极限或聚点，不是存在一个取多个值的普通极限。4.1–4.3的四函数运算仅转指讲义，应展开实虚部、16个偏导、CR及复导数。第二个4.3要求对共轭函数重复全部上述检验；不能只给“无导数”一行。不能将重复印号私改为官方4.4而不说明。

**rec3（S p1–3）。** 3.1取z=x0+iy的像为(cos x0 cosh y,−sin x0 sinh y)。x0=π/2时是整条虚轴，非除以cos²x0得到的双曲线；其余垂直线只走双曲线的一支。水平线y=y0，x∈(0,π)，y0≠0时只走椭圆的一个开半边；y0=0时是(−1,1)实线段。cos z=cos w给z=±w+2πk，可直接排除条带内不同点，完成源未写出的单射证明。3.2照H p1原条件添加x=0,y≥0与x=π,y>0；前者补[1,∞)，后者补(−∞,−1)，所以准确像为C\{−1}。−1的所有原像是π+2πk，均未加入。源S p3“entire complex plane”错误；不得暗改y>0为y≥0再照抄结论。3.3要区分解析分支的开割域和割线边界的单值选取：±1是分支点，在±1处不能声称存在解析逆。

**rec4（H p1，S p1–2）。** 1.1的“semicircle C”从1.2可知是包含直径的闭边界，方向正向、R>1应明示；只取半圆弧不能直接用Cauchy积分公式。若R=1经过极点，积分未定义；R<1不包i，积分为0。3.1的代数基本定理路线须n≥1；非零常数多项式没有根，不适用无根反证。所有八叶在本答案PDF只有讲义参考编号，不是自足解答。

**rec5（H/S p1）。** 四边给定值在角点相容；在板内调和、连续到闭板的条件下最大200、最小0正确。不能把边界表达100(x²+y²)擅当内部温度，因为其Laplacian为400。Q2源找到了sin z，却未明确写出v=cos x sinh y+C；中文须给共轭及常数自由度。

**rec6（H p1，S p1–2）。** “调和函数在闭盘A”应用最大最小值原理应读为内调和且闭盘连续，或闭盘邻域调和。Q2.2源链式偏导计算与结论正确，允许全纯映射有临界点，不需另加单射或Φ′≠0。Q3的两个log相加不作为任意主值下的严格等式；局部可调常数2πik，速度场是全局有理函数。在z≠±1处F=(Re(2z/(z²−1)),−Im(2z/(z²−1)))；沿y轴其第二分量2y/(1+y²)，0是唯一停滞点。3.4只有查看Topic6流线的阅读指令，不伪造额外算题，也不能漏原号。

**rec7（H/S p1）。** Q3源只用聚点0处理实轴线段，漏第二条平移线段；第二情形聚点−3i/4仍在单位圆盘内，恒等定理仍得f≡5。Q1、Q2和Q4均为参考讲义的短答案，新增中文解答需写具体展开及收敛环域。

**rec8（H/S p1）。** Q4.1、4.2、4.3在S中仅重述题面，沒有Ans；这三叶属于真实源缺答。三个挖小圆证明须分别出现，而非仅说“即留数定理”。题面仅说C在A中，不足以保证内部属于A：若C围住A的一个洞，函数在洞中根本未给定。应明确C及其闭内部包含在A，或给一般零同调版本条件。内部孤立奇点有限性由闭内部紧致、奇点无内聚点及曲线避开奇点获得，不能直接对无穷多个圈求和。其余六叶参考讲义，需独立展开。

**rec9（H p1，S p1–2）。** 四个结果分别π/√2、2π/√3、2π(2n)!/[2^{2n}(n!)²]、π/2。Q3参数n∈Z≥0在题面未写，源二项式及高阶极点推导依赖此假设，中文要明示；n=0亦适用。Q4积分x>1，根号正，x=1可积奇性；不能取任意复分支。Q1和Q4答案只引用例题。

**rec11（H p1，S p1–2）。** 1.1的tanα须有定义，原向右旋α得到上半平面的说明还要求cosα>0。因Im(e^{−iα}z)=cosα(y−x tanα)，cosα<0时映到下半平面。可取β=arctan(tanα)修复所有tanα存在的参数；不能无条件照抄原旋转。1.3公式−i(z−1)/(z+1)及平方正确，应验证象限、双射和内部非零导数。1.4准确条件0<y<π,x<0，使用e^z映到上半圆盘；原答案回指“2.3”不存在，应为1.3。2.2反射是1/conjugate z，不是1/z；0、∞在球面上互换。

**rec12（H/S p1）。** Q2左半平面零点数不能只在虚轴比模而声称Rouché适用无界域：需正向左半圆轮廓（R>5），虚轴|z+3|≥3>2，左弧|z+3|≥R−3>2≥|2e^z|，并把全部可能零点包住（零点满足|z+3|=2e^{Re z}<2，故|z|<5）。Q4符号P、Z若代表普通内部极点/零点数，应限定正向Jordan曲线且闭内部属于亚纯域；一般闭曲线需定义按绕数加权的数目。G的极点在H处可去，1+G的零点在H处成为同阶极点，源核心论证正确。

Q5源叙述“每个±2ni处一个源”正确，但末式第一和n≥1的log(z+2ni)给负侧源，第二和n≤−1的log(z−2ni)又给相同负侧源，遗漏正侧；即使把第二下标改正，两侧未经正则化的log和仍发散。正确配对势可取

Φ(z)=Log z+Σ_{n≥1}Log(1+z²/(4n²))，

在避开源点的局部选支并先固定常数；项为O_K(n^{−2})而局部一致收敛，速度对应

Φ′(z)=1/z+Σ_{n≥1}2z/(z²+4n²)=(π/2)coth(πz/2)。

可用sinh乘积得Φ=Log[(2/π)sinh(πz/2)]（差局部常数），但若使用该乘积需有支持；也可直接对配对速度用相邻镜像成对消去法验证墙法向速度0。闭式验证：z=x±i时coth(πx/2±iπ/2)=tanh(πx/2)为实，F_y=−Im Φ′=0。无限个镜像源、求和正则化、墙为流线这三项义务都要说明。

**rec13（H p1，S p1–3）。** Q1在S多一句收敛域询问，H没有这一句，可作为解答条件补充而不冒作原题新子问。ω≠0时原Laplace积分绝对收敛域Re s>0；ω=0是零函数，可定义全s的变换0，形式0/s²在s=0需移除。Q2应明确f局部C¹（或局部绝对连续及适当条件），二阶式另需f′可分部积分。仅f具有指数型不自动给f′指数型；如果将Laplace限定为绝对收敛，必须另检查导数的可积性，不能偷换定义。Q3源直接换微分与积分未解释，须在Re s>a的紧集用t e^{−δt}可积上界支持；幂函数变换用n归纳可避免“and so on”跳步。4.1未给t=0的阶跃值不影响积分，可任取。Q5部分分式系数、初值、微分方程均正确，S p3末行把时域解写为X而不是x，是记号笔误。独立代入：x(0)=1/3−1/5−2/15=0；x′(0)=−1/3+2/5+14/15=1；仅−e^{−2t}/5项贡献(4−16+7)(−1/5)e^{−2t}=e^{−2t}。
