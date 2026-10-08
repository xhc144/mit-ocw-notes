# 18.152 Fall 2011：独立来源与考题范围审查

日期：2026-10-08。审查者未编写正文/题解；审查范围是原始来源、题面覆盖、缺项、重复与原卷条件。没有把未审的中文答案标作通过。

## 核定清单与计数

官方 [Assignments](https://ocw.mit.edu/courses/18-152-introduction-to-partial-differential-equations-fall-2011/pages/assignments/) 公布11份作业、1份Bonus；[Exams](https://ocw.mit.edu/courses/18-152-introduction-to-partial-differential-equations-fall-2011/pages/exams/) 公布期中卷、期中官方解答、期末卷。没有公开作业/Bonus/期末答案，也没有其它quizzes/practice exams链接。15考核PDF共78页；18讲义PDF共136页。33原件实际页数及SHA-256均与现有清单相符。

11作业含51罗马编号条目：39完整公开大题、11商业书仅题号、1阅读任务。加Bonus1、期中5、期末7，共52完整公开大题。

叶条目口径：有字母小问逐个计，无字母分问每罗马题计1；内部连续要求必须全部完成。作业75、Bonus10、期中9、期末20，共114条。Bonus标号a,b,c,d,e,f,f,g,h,i，第二个f不得吞掉，消歧为f₁、f₂。三条真正重复小问复用证明后有111独立叶条目。Salsa未知小问不估算。

| 原文件 | 完整公开原题号 | 叶条目数 | 官方答案 |
|---|---|---:|---|
| PS1 | I,II,III,IV | 4 | 未公开 |
| PS2 | III,IV,V | 3 | 未公开 |
| PS3 | I,II,V,VI | 4 | 未公开 |
| PS4 | VI | 1 | 未公开 |
| PS5 | I,II,III | 3 | 未公开 |
| PS6 | I,II,III | 7 | 未公开 |
| PS7 | I,II,III,IV,V | 7 | 未公开 |
| PS8 | I,II | 7 | 未公开 |
| PS9 | I,II,III,IV,V,VI | 13 | 未公开 |
| PS10 | I,II,III,IV | 13 | 未公开 |
| PS11 | I,II,III,IV | 13 | 未公开 |
| Bonus | I | 10 | 未公开 |
| Midterm | I,II,III,IV,V | 9 | 有，I–V |
| Final | I,II,III,IV,V,VI,VII | 20 | 未公开 |

## 完整公开题目与分问索引

全部题号属于MIT 18.152 Fall 2011，Jared Speck。下列页码是原PDF页序。只有期中有官方答案，其余答案必须标作AI独立编写并复核。

### PS1-I　Green 第二恒等式

原件 `mit18_152f11_problemset_1.pdf`，PDF第1页。

- 由散度定理对 u∇v−v∇u 证明恒等式。

需处理：C01。

### PS1-II　振荡对数函数的 L² 可积性

原件 `mit18_152f11_problemset_1.pdf`，PDF第1页。

- 0<ε<1/2；原分子为 sin(x)ln(x²+1)，分母为 |x|^(1−ε)，控制0与±∞。

### PS1-III　实内积空间中的基本不等式

原件 `mit18_152f11_problemset_1.pdf`，PDF第1,2页。

- 二次型最小值证明 Cauchy–Schwarz。
- 证明三角不等式。

### PS1-IV　L² 内积与积分泛函

原件 `mit18_152f11_problemset_1.pdf`，PDF第2页。

- 验证内积三性质。
- 推出积分 Cauchy–Schwarz。
- 取 PS1-II 的 ε=1/4 估计指定积分。

需处理：C02。

### PS2-III　不相容角点热解的 L² 初值

原件 `mit18_152f11_problemset_2.pdf`，PDF第1页。

- 给定正弦级数在 t↓0 于 L²(0,1) 收敛到 x。

需处理：C03。

### PS2-IV　区间热流的能量衰减

原件 `mit18_152f11_problemset_2.pdf`，PDF第1,2页。

- 初始范数 √(ℓ/30)。
- 能量导数。
- C⁰ 估计。
- Poincaré 型估计。
- 能量微分不等式。
- 指数衰减。

需处理：E01, C04。

### PS2-V　一维热核自相似推导

原件 `mit18_152f11_problemset_2.pdf`，PDF第2页。

- 自相似代换推 ODE。
- 对称性/衰减定积分常数。
- 求 Gaussian。
- 总质量归一。

需处理：C05。

### PS3-I　热解的反射对称性

原件 `mit18_152f11_problemset_3.pdf`，PDF第1页。

- 比较 u(t,x) 与 u(t,1−x) 并用唯一性。

需处理：C04。

### PS3-II　热解的非负性与指数上界

原件 `mit18_152f11_problemset_3.pdf`，PDF第1页。

- 闭域连续性强制边界常数为0。
- 证明非负。
- 讨论所有可行 α,β，而非只一组充分条件。
- 一致趋于0的极限应为 t→∞。

需处理：E02, C06。

### PS3-V　一般线性方程的 Duhamel 原理

原件 `mit18_152f11_problemset_3.pdf`，PDF第1,2页。

- 用解族的积分检查非齐次方程与零初值。

需处理：E03, C07。

### PS3-VI　非齐次热方程表示式

原件 `mit18_152f11_problemset_3.pdf`，PDF第2页。

- 齐次初值项加 Duhamel 源项并明确 f,g 假设。

需处理：C07。

### PS4-VI　单位球 Poisson 先验 C⁰ 估计

原件 `mit18_152f11_problemset_4.pdf`，PDF第1页。

- 一般 n 的单位球，允许只证 n=3，常数独立于 f,g。

需处理：C08。

### PS5-I　三维球 Green 函数的非正性

原件 `mit18_152f11_problemset_5.pdf`，PDF第1页。

- 直接用像点公式比较两距离。

需处理：C09。

### PS5-II　Green 核积分与 Poisson 数据估计

原件 `mit18_152f11_problemset_5.pdf`，PDF第1页。

- 计算 ∫G=(|x|²−1)/6。
- 推出 ∫|G|≤1/6。
- 推出解的 C⁰ 数据界。

需处理：C08。

### PS5-III　对数增长调和函数消失

原件 `mit18_152f11_problemset_5.pdf`，PDF第1页。

- 从 |u(x)|≤ln(1+|x|) 与 Harnack 极限证明 u≡0。

### PS6-I　波能量流与因果正性

原件 `mit18_152f11_problemset_6.pdf`，PDF第1页。

- a：无散度能量流。
- b：对 V=(1,ω)、|ω|≤1 证明 V·J≥0。

### PS6-II　光锥能量、有限传播与守恒

原件 `mit18_152f11_problemset_6.pdf`，PDF第1,2页。

- a：光锥侧面外单位法向。
- b：局部能量不增。
- c：紧支撑初值有限传播。
- d：另加论证得到全空间能量等号。

### PS6-III　一维波长期能量均分

原件 `mit18_152f11_problemset_6.pdf`，PDF第2,3页。

- 利用 d’Alembert 零方向导数及支撑分离，证明大时间 P²=K²=E²/2。

### PS7-I　三维波的 1/(1+t) 衰减

原件 `mit18_152f11_problemset_7.pdf`，PDF第1页。

- Kirchhoff 积分与移动球面交面积估计，明确常数依赖。

### PS7-II　Lorentz 变换代数

原件 `mit18_152f11_problemset_7.pdf`，PDF第1页。

- a：|det Λ|=1。
- b：乘积闭合。
- c：逆矩阵闭合。

### PS7-III　Lorentz boost

原件 `mit18_152f11_problemset_7.pdf`，PDF第1,2页。

- 给定 x¹ 方向速度矩阵满足 ΛᵀmΛ=m。

### PS7-IV　未来类时向量的静止系

原件 `mit18_152f11_problemset_7.pdf`，PDF第2页。

- 构造行列式1的 Lorentz 变换化为 (c,0,…,0)。

### PS7-V　共同零方向分解

原件 `mit18_152f11_problemset_7.pdf`，PDF第2页。

- 两个未来类时向量以同一规范化零向量对作正系数分解，n≥1。

### PS8-I　应力张量的严格能量正性

原件 `mit18_152f11_problemset_8.pdf`，PDF第1页。

- 用共同零标架证明 T(X,Y)>0，保持 spacetime 梯度非零假设。

### PS8-II　原卷有误的 Morawetz 能量题

原件 `mit18_152f11_problemset_8.pdf`，PDF第1,2,3页。

- a：K 未来类时。
- b：共形 Killing 方程。
- c：原无迹断言须勘误。
- d：原零散度断言须勘误。
- e：未修正 J_K⁰ 的零标架表达。
- f：原守恒断言须改用 Bonus 修正流。

需处理：E04。

### PS9-I　二阶方程分类

原件 `mit18_152f11_problemset_9.pdf`，PDF第1页。

- a：∂t²u+∂t∂xu+∂x²u=0。
- b：∂t²u+2∂t∂xu+∂x²u=0。
- c：2∂t²u−∂t∂xu−12∂x²u=0。

### PS9-II　sinc 与区间 Fourier 变换

原件 `mit18_152f11_problemset_9.pdf`，PDF第1页。

- a：sinc 在0光滑。
- b：[−a,a] 特征函数的变换为2a sinc(2aξ)。

### PS9-III　C₀ 的一致闭合性

原件 `mit18_152f11_problemset_9.pdf`，PDF第1,2页。

- 一致极限继续在无穷远消失。

### PS9-IV　L¹ 平移连续性

原件 `mit18_152f11_problemset_9.pdf`，PDF第2页。

- 连续紧支撑 f 的 ∥τ_yf−f∥₁→0。

### PS9-V　热核近似恒等

原件 `mit18_152f11_problemset_9.pdf`，PDF第2,3页。

- 分小位移与 Gaussian 尾部证明 Γ_t*f→f 于 L¹。

### PS9-VI　Riemann–Lebesgue 引理

原件 `mit18_152f11_problemset_9.pdf`，PDF第3,4页。

- a：热正则化的 Fourier 乘子。
- b：Fourier 连续有界与 C⁰ 误差界。
- c：正则化变换属于 C₀。
- d：变换的一致收敛。
- e：由 C₀ 闭合得原变换在无穷远消失。

### Bonus-I　修正 Morawetz 流与共形正能量

原件 `mit18_152f11_bonusproblem.pdf`，PDF第1,2,3页。

- a：K 未来类时。
- b：共形 Killing 方程。
- c：正确非零迹。
- d：未修正流的非零散度。
- e：修正流 J̃ 无散度。
- f₁：未修正 J_K⁰ 的表达式。
- f₂：修正 J̃⁰=J_K⁰+2tφ∂tφ−φ²。
- g：紧支撑函数径向积分分部。
- h：正平方式只在空间积分后成立。
- i：修正共形能量守恒。

需处理：E05, E06。

### PS10-I　Fourier 推导热核

原件 `mit18_152f11_problemset_10.pdf`，PDF第1,2页。

- a：频率 ODE。
- b：求解 Gaussian 乘子。
- c：逆变换 Gaussian。
- d：热核卷积表示。

需处理：C10。

### PS10-II　Heisenberg 不确定性

原件 `mit18_152f11_problemset_10.pdf`，PDF第2页。

- a：积分分部恒等式。
- b：Cauchy–Schwarz 尺度界。
- c：Plancherel 推 ∥f∥₂²≤4π∥xf∥₂∥ξ f̂∥₂。

### PS10-III　紧支撑 Fourier 变换解析性

原件 `mit18_152f11_problemset_10.pdf`，PDF第2,3页。

- a：指数幂级数绝对一致收敛。
- b：逐项积分及所得级数收敛。
- c：非零变换不能也紧支撑。

需处理：C11。

### PS10-IV　非齐次 Schrödinger Duhamel 式

原件 `mit18_152f11_problemset_10.pdf`，PDF第3,4页。

- a：频率 ODE 的积分因子。
- b：求频率解；源项指数须负号。
- c：形式逆变换为自由振荡核卷积。

需处理：E07, C12。

### PS11-I　逆矩阵导数

原件 `mit18_152f11_problemset_11.pdf`，PDF第1页。

- 微分 N⁻¹N=I 得 dN⁻¹/dq=−N⁻¹(dN/dq)N⁻¹。

### PS11-II　矩阵范数与 Neumann 级数

原件 `mit18_152f11_problemset_11.pdf`，PDF第1,2页。

- a：Frobenius 范数次乘性。
- b：行列式零点一阶展开。
- c：有限几何级数矩阵式。
- d：小范数逆矩阵收敛级数。

需处理：E08。

### PS11-III　带势标量场

原件 `mit18_152f11_problemset_11.pdf`，PDF第2页。

- a：Lagrangian 坐标协变意义。
- b：Euler–Lagrange 方程 □φ=V′(φ)。
- c：应力张量。
- d：直接证其在场方程上无散度。

### PS11-IV　连续等距流与 Noether 能量

原件 `mit18_152f11_problemset_11.pdf`，PDF第2,3页。

- a：微分等距流得 Killing 方程。
- b：Killing 流无散度，须修正原任意 Z 积分断言。
- c：无散度流产生守恒量。
- d：时间平移的带势能量守恒。

需处理：E09, E10, C13。

### Midterm-I　反向热方程不适定性

原件 `mit18_152f11_midtermexam.pdf`，PDF第1页。

- a：全部零 Dirichlet 分离变量解。
- b：高频小初值破坏连续依赖，对比正向热流。

需处理：C14。

### Midterm-II　次线性调和函数消失

原件 `mit18_152f11_midtermexam.pdf`，PDF第4页。

- |u(x)|≤√|x| 推 u≡0，核译官方 Harnack 证明。

### Midterm-III　吸收热方程最大原理

原件 `mit18_152f11_midtermexam.pdf`，PDF第6页。

- 非正初边值与 ∂tu−∂x²u=−u 推出 u≤0。

### Midterm-IV　Neumann 热流极限

原件 `mit18_152f11_midtermexam.pdf`，PDF第8页。

- a：空间积分守恒。
- b：猜长期常数为均值。
- c：严格证明向均值的收敛。

需处理：E11。

### Midterm-V　非齐次波方程全时能量界

原件 `mit18_152f11_midtermexam.pdf`，PDF第11页。

- a：能量导数恒等式。
- b：源项 L² 界1/(1+t²) 推 E(t)≤E(0)+C。

需处理：C15。

### Final-I　一维波有限传播

原件 `mit18_152f11_final.pdf`，PDF第1页。

- |x|≥R+t 时紧支撑数据的解消失。

### Final-II　特征函数变换与范数

原件 `mit18_152f11_final.pdf`，PDF第3页。

- a：[−2,2] 特征函数变换4 sinc(4ξ)。
- b：由 Plancherel 求其 L² 范数。

### Final-III　Fourier 波能量守恒

原件 `mit18_152f11_final.pdf`，PDF第5页。

- a：频率初值 ODE。
- b：解为余弦乘子。
- c：时间导数和空间梯度的频率式。
- d：只用 Fourier 证能量守恒。

需处理：E12。

### Final-IV　严格负热源与内部最大值

原件 `mit18_152f11_final.pdf`，PDF第8页。

- 内部时空最大点导数符号与源−(t²+x²)矛盾。

需处理：C16。

### Final-V　Schrödinger 能量与唯一性

原件 `mit18_152f11_final.pdf`，PDF第10页。

- a：L² 范数守恒。
- b：对差解用守恒得能量类唯一性。

需处理：C17。

### Final-VI　四次势场

原件 `mit18_152f11_final.pdf`，PDF第12页。

- a：Euler–Lagrange 方程。
- b：应力张量与 T⁰⁰≥0。
- c：应力张量散度。
- d：用 J^μ=T^{μ0} 得有用守恒量。

需处理：C18。

### Final-VII　六个课程短答

原件 `mit18_152f11_final.pdf`，PDF第14,15页。

- a：色散 PDE 例。
- b：非有限传播初值 PDE 例。
- c：Dirichlet Green 分布 PDE 与边界。
- d：−∂t²u+4∂t∂xu−∂x²u 分类。
- e：适定性与解空间。
- f：不适定线性 Cauchy 问题例。

## 未公开题面的商业书缺项

Sandro Salsa，*Partial Differential Equations in Action: From Modelling to Theory*，Springer，2010，ISBN9788847007512。

| 原作业号 | 书题号 | 书页 | 可见信息 |
|---|---|---:|---|
| PS2-I | 2.1 | 97 | 仅题号，无题面 |
| PS2-II | 2.3 | 97 | 仅补 L=π、U=0 |
| PS3-III | 2.13 | 99 | 仅题号，无题面 |
| PS3-IV | 2.14 | 99 | 可用热核表达显式解的提示 |
| PS4-I | 3.1 | 150 | 仅题号，无题面 |
| PS4-II | 3.2 | 150 | 仅题号，无题面 |
| PS4-III | 3.3 | 151 | 补充 u∈C³(Ω)∩C¹(闭Ω) |
| PS4-IV | 3.4 | 151 | 仅题号，无题面 |
| PS4-V | 3.8 | 152 | 仅题号，无题面 |
| PS5-IV | 3.14 | 153 | 提示中提及 a,b；Green 非正性与对称性提示不等于完整题面 |
| PS5-V | 3.21 | 155 | 提示中提及 a,b；Helmholtz 基本解提示不等于完整题面 |

这些条目不得由模型猜造原题，不打包商业教材；只在主PDF登记书目、原号及缺项。PS5-IV/V提示可知涉及a,b，但完整题面仍缺；其它书题小问总数未知。PS1-V是阅读Appendix A任务，不计可解题。

## 重复映射

完全重复三条：Bonus-I(a)↔PS8-II(a)，Bonus-I(b)↔PS8-II(b)，Bonus-I(f₁，0.0.7)↔PS8-II(e)。可回指同一证明，两个课程位置仍保留。

PS6-II(c)与Final-I、PS9-II(b)与Final-II(a)、PS4-VI与PS5-II最后要求是维数/参数/任务相关，不删考试或前置小要求。PS8错误式到Bonus修正式不算完全重复，不能以去重掩去勘误。

## 原卷与官方答案的条件和错误

判断来自实读原件和独立计算，不声称存在额外官方errata；PS8修正有官方Bonus直接对照。

### C01　PS1 I p.1

光滑域未写有界性或无穷远可积/边界通量条件，积分可能未定义。

处理：采用有界光滑域；无界版要附衰减或截断边界极限。

证据/复算：散度定理不能无条件用于任意无界域的发散积分。

### C02　PS1 IV p.2

L² 实内积须用实值及几乎处处等价类，否则正定性不成立；复值需共轭。

处理：先由2|fg|≤f²+g²确认积分存在，再证内积与不等式。

证据/复算：原题允许连续函数简化；严谨稿明确真实 L² 意义。

### C03　PS2 III p.1

x=1 初值为1，正时间边界为0，不能是闭矩形连续经典解。

处理：以 L² 初值或区间内部点态初值实现，说明不相容角点。

证据/复算：原 Remark 直接指出角点不连续；目测系数为2/(mπ)。

### E01　PS2 IV pp.1–2

后面能量不等式与最终范数误写 L²([0,1])，实际空间为[0,ℓ]。

处理：统一为 L²(0,ℓ)。

证据/复算：初值 ℓ⁻²x(ℓ−x) 的范数确为 √(ℓ/30)。

### C04　PS2 IV p.1 / PS3 I p.1

原PS2-IV及PS3-I取 C^{1,2}(闭S)，但抛物线初值与零边值的角点高阶相容性不满足。

处理：取 t>0 光滑并连续/L² 初值迹；先从δ>0积分能量再取δ↓0。

证据/复算：PS2角点初值 u_xx=−2/ℓ²，PS3-I为−2，而零边值的 u_t=0；若PDE连续到角点就矛盾。

### C05　PS2 V p.2

自相似 ζ=x/√(Dt) 与热核需 D>0。

处理：明确 D>0。

证据/复算：Gaussian 归一与扩散尺度。

### E02　PS3 II p.1

原末句 t→0 时 u→0 错误。

处理：勘误为 t→∞，保留原号。

证据/复算：目测原 PDF 确为0；x=1/2 的初值是1/4。

### C06　PS3 II p.1

边界常数由 C(闭S) 强制为0；“所有 α,β”不能只答超解充分条件 α≥1、β≤8。

处理：精确讨论可用谱公式定义 A(β)=sup e^{βt}u(t,x)/[x(1−x)]，证明 α≥A(β)、0<β≤π²；若只给超解法须标充分条件。

证据/复算：第一正弦模态正性推出β≤π²必要；初值给α≥1。α=1且β>8在中心初始导数失败。而α=π、β=π²成立：f≤sinπx/2，sinπx≤2πf，用正热流比较。故β≤8不是全部可行参数。

### E03　PS3 V p.1 (0.0.2)

齐次初值 u(0,x)=f(t,x) 右边错误保留自由 t。

处理：一般初值改 h(x)；参数族仍 v^(s)(0,x)=f(s,x)。

证据/复算：随后(0.0.5) 的参数族为正确式。

### C07　PS3 V–VI pp.1–2

Duhamel 微分换积分、卷积、初值极限需具体函数类。

处理：光滑紧支撑初值与时间局部统一紧支撑源下证明，较弱版本另界定。

证据/复算：原件允许自行作充分正则假设，不能把形式式称任意源项定理。

### C08　PS4 VI / PS5 II

开球光滑不自动在闭球有界或有有限max。

处理：f 连续到闭球或有界；u有连续边界迹；用sup。

证据/复算：f=1/(1−|x|²) 在开球光滑却无有限最大值。

### C09　PS5 I p.1

G在 x=y 非有限值。

处理：G≤0先写 x≠y；对角线是−∞极限/分布意义。

证据/复算：核含 −1/(4π|x−y|)。

### E04　PS8 II(c,d,f) pp.2–3

4维普通标量波应力张量非无迹，未修正 Morawetz 流非无散度，其加权能量不守恒。

处理：明确原(c,d,f)错误；由官方 Bonus(c,d,e,i) 给修正，保留(e)的正确代数式。

证据/复算：Q=m^{αβ}∂αφ∂βφ，D=n+1：tr_mT=(1−D/2)Q，D=4为−Q；∂μJ_K^μ=2tQ。φ=t 是波解，Q=−1，迹1、散度−2t。Bonus p.1 官方题面给正确非零式。

### E05　Bonus f labels pp.1–2

两个不同小问都标f，总共10个分问。

处理：依出现次序保留 f₁(0.0.7)、f₂(0.0.11) 映射。

证据/复算：目测页1的f是J_K⁰，页2另一个f是J̃⁰。

### E06　Bonus(h) p.2 (0.0.13)

原件由积分分部误得到点态正平方等式。

处理：给等式两边加空间积分，或说明模一个空间散度相等。

证据/复算：正平方右边P展开有 P−J̃⁰=2rφ∂rφ+3φ²=div_x(xφ²)。紧支撑时积分0，点态一般非0。

### C10　PS10 I pp.1–2

任意光滑全空间热解不自动可 Fourier 变换或唯一。

处理：明确标准热核解/Schwartz解或 C_tL² 能量类。

证据/复算：光滑不提供无穷远可积和边界控制。

### C11　PS10 III(c), Remark0.0.4

“变换不能在开集消失”需排除零函数。

处理：非零f的解析变换不能在非空开区间消失；保留零函数例外。

证据/复算：原(c)有例外，Remark应随之解释。

### E07　PS10 IV(b) p.3 (0.0.20)

Duhamel源项指数原件写+i2π²(t−s)|ξ|²，符号错误。

处理：改−i2π²(t−s)|ξ|²，与(c)的传播核一致。

证据/复算：由(a)得 ψ̂=e^(−iωt)φ̂−i∫e^(−iω(t−s))f̂ ds，ω=2π²|ξ|²；目测原PDF确为正号。

### C12　PS10 IV pp.3–4

逐时刻紧支撑不保证时间局部统一积分控制；Schrödinger核非L¹，逆变换形式式要界定。

处理：保留(c)形式推导含义；严格版用时间局部Schwartz族或 L¹_tL² 源与 Fourier 演化。

证据/复算：原(c)明写 formally，不能抹掉这一范围。

### E08　PS11 II(b) p.1 (0.0.4)

标量行列式展开首项写为矩阵 I。

处理：改标量1：det(I+A)=1+tr A+O(∥A∥²)。

证据/复算：标量/矩阵类型冲突，目测原件确为 I。

### E09　PS11 IV(b) p.3 (0.0.14)

任意光滑Z的积分恒等式缺边界限制，不成立。

处理：变分Z取内部紧支撑/边界消失；本题直接由无散度T与Killing方程证明目标流无散度。

证据/复算：V=0、φ=t、Z=(t,0,…,0) 给原 integrand −1，正体积区域积分非0。

### E10　PS11 IV(d) p.3 (0.0.16)

回指 Lagrangian(0.0.7) 当方程；守恒式右边梯度写t、势项写0。

处理：方程回指(0.0.8)；右边全部能量在0时刻。

证据/复算：目测页3确认混合t/0。

### C13　PS11 IV(d) p.3

一般V若V(0)≠0，紧支撑φ的全空间势能仍发散。

处理：设V(0)=0或改势为V(φ)−V(0)；紧支撑场解通常还要求V′(0)=0。

证据/复算：支撑外势能密度为常数V(0)。

### C14　Midterm I, official solution pp.1–2

官方对一般光滑f直接称指数增长 Fourier 级数为解，正时间通常不收敛。

处理：保留正确单频连续依赖反例；一般级数只形式式，可没有正时间解。非零分离模态m≥1。

证据/复算：延拓到τ>0的L²解需(c_m e^{m²π²τ})∈ℓ²；即使超多项式衰减也未必满足Gaussian加权条件。仅端点零的C∞[0,1]函数可只有多项式正弦系数，例如f=x(1−x)有c_m=4[1−(−1)^m]/(m³π³)。

### E11　Official Midterm IV(c) p.4

积分微分不等式时误回指(21)。

处理：应引用(22)。

证据/复算：(21)空间估计，(22)才是 dE²/dt≤−2E²。

### C15　Midterm V, official solution pp.4–5

官方直接除E而没处理E=0。

处理：用 E_δ=√(E²+δ²) 积分后δ↓0；明确能量/支撑控制。

证据/复算：题面未要求正能量。

### E12　Final III p.5 formula(4)

Fourier积分被积函数写f(x)，左边便不随t变，与题目波ODE冲突。

处理：改u(t,x)；f̂只用于初值(6)。

证据/复算：目测页5确认原件f(x)。

### C16　Final IV p.8

有界区间不设边界值却称唯一全局Cauchy光滑解，唯一性错误；所求内部最大值命题正确。

处理：写“给定一个光滑解”，注明原卷没有边界条件，不虚构新增边值。

证据/复算：t₀>0时源严格负，内部最大点局部导数符号足够矛盾。

### C17　Final V p.10

任意光滑ψ不保证L²守恒与全光滑类唯一。

处理：明确标准Schwartz/能量解类，如 C([0,T];L²) 的适当强解，在此类证明守恒和唯一。

证据/复算：光滑不限制无穷远增长，积分分部和Fourier工具都需额外条件。

### C18　Final VI(d) p.12

无散度流转全空间守恒需有限能量及无穷远零通量。

处理：给紧支撑或足够衰减版本，能量密度含φ⁴/4。

证据/复算：原卷此小问未给无穷远假设。

## 逐文件署名、许可与归档审查

33份PDF均在metadata及首页署Jared Speck，末页保留MIT OCW/terms；对应资源HTML均含CC BY-NC-SA4.0。已核实际页数、SHA-256、首页/末页与全页提取文字的第三方权利标记，未检出额外独立第三方版权通知。此项文本/metadata核验不冒充18讲义全部数学通读或逐页视觉。

现行 [MIT OCW Terms](https://ocw.mit.edu/pages/privacy-and-terms-of-use/) 与 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 要求署名、非商业、同许可改编和标明改变。中文稿须保留课号学期、Jared Speck、MIT OCW、原题号/链接，区分翻译、AI答案和勘误，不暗示MIT审定。Salsa/Springer书目是第三方例外；OCW许可不授予未公开书题或整书再分发权。

英文原件只sources归档，不嵌中文PDF、不进入中文源码ZIP。

| 文件 | 实际页数 | 署名/来源 | 哈希清单相符 | 额外第三方标记 |
|---|---:|---|---|---|
| `mit18_152f11_lec_01.pdf` | 8 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_lec_02.pdf` | 8 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_lec_03.pdf` | 4 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_lec_04.pdf` | 4 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_lec_05.pdf` | 11 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_lec_06.pdf` | 7 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_lec_07.pdf` | 11 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_lec_08.pdf` | 4 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_lec_09.pdf` | 7 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_lec_10.pdf` | 7 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_lec_11.pdf` | 4 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_lec_12.pdf` | 7 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_lec_13_14.pdf` | 7 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_lec_15.pdf` | 8 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_lec_16_18.pdf` | 12 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_lec_19_20.pdf` | 10 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_lec_21_23.pdf` | 11 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_lec_24.pdf` | 6 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_problemset_1.pdf` | 3 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_problemset_2.pdf` | 3 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_problemset_3.pdf` | 3 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_problemset_4.pdf` | 2 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_problemset_5.pdf` | 3 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_problemset_6.pdf` | 4 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_problemset_7.pdf` | 3 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_problemset_8.pdf` | 4 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_problemset_9.pdf` | 5 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_bonusproblem.pdf` | 4 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_problemset_10.pdf` | 5 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_problemset_11.pdf` | 4 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_midtermexam.pdf` | 13 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_mdtrmexm_sol.pdf` | 6 | Jared Speck / MIT OCW | 是 | 未检出 |
| `mit18_152f11_final.pdf` | 16 | Jared Speck / MIT OCW | 是 | 未检出 |

完整哈希、资源URL、直链、版权核验深度及索引HTML哈希存于同名JSON，可绑定冻结原件。

## 实际阅读边界与后续检查

15份考核PDF共78页提取文字逐项读取，空白答题页不增加题目数。另实际视觉核对：PS1 PDF1,2; PS2 PDF1,2; PS3 PDF1; PS8 PDF2; Bonus PDF1,2; PS10 PDF3; PS11 PDF1,2,3; Final PDF5,8,10。临时渲染只用于查看。18讲义只核页数、署名、许可及归档，不声称完整数学审稿。

建议同一主PDF按PS1–PS11、Bonus、Midterm、Final设课程题部分，或按章收录并留原号完整索引。公开PS7/PS8/PS11与Final-VI需要有限的Lorentz、应力张量与Noether内容，不能因正文只选热/Laplace/波而漏题。

主agent仍须完成：新编中文解答独立复算、主PDF实际逐页视觉、目录链接、源码ZIP干净重编和远端冻结上传验证。原题错误可作明确勘误式完整解答；商业书题只登记真实缺项。
