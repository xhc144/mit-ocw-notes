# 电动力学中文正文独立数学与教学审查

审查日期：2026-10-11。实际通读 `main.tex` 的符号宏、`course-info.tex` 和 `chapters/01-vector.tex` 至 `11-advanced.tex`。以下行号指本次读取的版本；后续修改应按引用语句定位。考核章尚在编写，不在本轮结论内。

本审查直接按方程推导、量纲、极限及模型条件判断；来源校验、PDF 可打开、上传成功和 LaTeX 编译不构成数学内容通过的证据。本轮不是全部习题的独立求解，也没有声称每条进阶公式均已完整重推。

## 应修正文或明确条件

1. **确定的轴向符号问题**：`06-magnetostatics.tex:14`。精确圆环公式对正负轴都给同号的 $B_z$，但远场写成 $\mu_0IR^2/(2z^3)$ 在 $z<0$ 会变号。改为 $\mu_0IR^2/(2|z|^3)$，或例题明确只讨论 $z>0$。另外电流方向须约定按从 $+z$ 看逆时针，才能指定磁矩沿 $+z$。

2. **辐射区条件未写全**：`10-radiation.tex:3,8,13`。$a\ll c/\omega$、$r\gg a$ 是源的长波条件和几何远区条件；不保证 $1/r$ 场压倒 $1/r^2,1/r^3$。作为仅保留辐射场的近似还应有 $r\gg c/\omega$（定义 $k=\omega/c$，即 $kr\gg1$）。例如 $a\ll r\ll c/\omega$ 仍在准静态近场。第24行三阶场可用于这一情形，必须和首节区分。第13行“对任何时变偶极矩成立”宜改为“对理想点偶极，或满足各主要频率均有 $ka\ll1$ 的局域源，在辐射区给出电偶极主项”；不能把任意快速变化的有限源解释成仍可忽略源内部相位差。

3. **固定控制体的机械动量漏通量条件**：`08-conservation.tex:28,33`。局部式 $f_i+\partial_tg_i=\partial_jT_{ij}$ 正确，它积分直接给
   $$\int_\Omega\mathbf f\,d^3x+\frac d{dt}\int_\Omega\mathbf g\,d^3x=\oint_{\partial\Omega}\mathbf T\cdot\mathbf n\,da.$$
   只有选取包围同一物质系统且无物质穿越边界、并排除其他外力（或另计机械应力）时，才能把第一项直接替换成 $d\mathbf P_{\rm mech}/dt$。一般固定体积内有粒子流入流出时还要加机械动量通量。建议先给上面的力积分式，再明确物质系统条件；角动量“只通过边界应力矩交换”应继承同一条件。

4. **吸收符号遗漏正频率限制**：`11-advanced.tex:7`。该模型实际有
   $$\operatorname{Im}\chi_e(\omega)=\frac{Ne^2}{\varepsilon_0m}\frac{\Gamma\omega}{(\omega_0^2-\omega^2)^2+\Gamma^2\omega^2}.$$
   $\Gamma>0$ 时仅对 $\omega>0$ 为正；负频率为负，符合第14行的实响应对称性。改成“对正频率 $\omega>0$，$\operatorname{Im}\chi_e>0$；平均吸收功率密度为 $\varepsilon_0\omega\operatorname{Im}\chi_e|E_0|^2/2$”。这同时解释阻尼和吸收的关系。

5. **各向同性条件须落在实际使用公式处**：`09-waves.tex:17,22,25` 与 `11-advanced.tex:17,19,22`。标量阻抗、s/p 标量导纳、标量 $k^2$、$\mathbf S\parallel\mathbf k/\mu$、同轴 $L',C'$ 均依赖线性各向同性模型；“均匀无损”本身不排除各向异性。建议正入射节先声明两侧为静止、线性、均匀、各向同性的普通无损介质，$\varepsilon_j,\mu_j>0$；进阶负折射节另声明有效各向同性、单频透明频带。色散切伦科夫条件写成频率依赖的 $v>c/n(\omega)$、$\cos\theta_k(\omega)=c/[n(\omega)v]$（普通正折射传播分支）；不能暗示所有频率共用同一锥角。良导体趋肤近似还需正实近似常量的 $\mu,\sigma$ 及 $\omega>0$。

6. **静态能量公式的构成关系条件**：`08-conservation.tex:10`。仅“无损且瞬时线性”还应排除时变参数、预存极化/磁化偏置，并要求静止介质及对称、时间不变的构成张量（各向同性实常数是简单充分情形）。否则 $\partial_t(\mathbf E\cdot\mathbf D/2)=\mathbf E\cdot\partial_t\mathbf D$ 不自动成立。`05-matter.tex` 静态能量的限定较好，应在本处继承而非放宽。负折射节已提醒色散储能，避免再把负常数代入本行。

7. **电容矩阵的源条件**：`02-electrostatics.tex`“对多个导体，线性泊松问题给出 $Q_i=C_{ij}V_j$”及随后 $V=\sum V_iu_i$。这里需说明导体外无给定自由体电荷、无额外固定源或外加非零无穷远势；否则有特解和偏置电荷，关系是 $Q_i=\sum C_{ij}V_j+Q_i^{(0)}$。当前前文讨论一般泊松源，读者容易把一般情形带入。补一句假设即可。

8. **腔场振子省略标势条件**：`11-advanced.tex:24`。库仑规范 $\nabla\cdot\mathbf A=0$ 本身不强制 $V=0$，也不消除腔中静电解。应明确无源真空腔、无静电背景，取相容的辐射规范 $V=0$，并选择满足导体边界的横向模态，才能只用 $\mathbf A$ 得独立振子拉格朗日量。宜写出归一化 $\varepsilon_0\int\mathbf f_\alpha\cdot\mathbf f_\beta,d^3x=\delta_{\alpha\beta}$，使“选择归一化”可复算。

## 重点核对后未发现反号的问题

- `10-radiation.tex:10,29` 的 $\mathbf n\times(\mathbf n\times\ddot{\mathbf p})$ **正确**。它是 $-\ddot{\mathbf p}_\perp$，来自 $-\partial_t\mathbf A$；不要改成 $\mathbf n\times(\ddot{\mathbf p}\times\mathbf n)$。取 $\mathbf n=\hat x$、$\ddot{\mathbf p}\parallel\hat z$ 得电场沿 $-\hat z$，与标势抵消纵向分量后相符。三阶场静态极限、感应磁场和 $\mathbf B_{\rm rad}=\mathbf n\times\mathbf E_{\rm rad}/c$ 一致。
- `10-radiation.tex:35–44` 的对偶 $\mathbf p=\mathbf m/c$、$\mathbf B_m=\mathbf E_e/c$、$\mathbf E_m=-c\mathbf B_e$ 量纲与系数正确，磁偶极功率系数也正确。当前明确限于源外真空区是必要的；它不延拓到接触项。第4章电接触项 $-\mathbf p\delta/(3\varepsilon_0)$ 与第6章磁接触项 $2\mu_0\mathbf m\delta/3$ 保留了这一差别。
- `08-conservation.tex:15–30` 局部应力推导正确，法拉第替换的符号正确，应力 $T_{zz}=-u$ 与向外场动量通量 $-T$ 一致。问题仅在积分式的物质系统条件，非应力张量反号。
- 第7章推迟时间导数、$\kappa$ 雅可比、Liénard–Wiechert 两项场；第10章匀速场横向增强及纵向减弱、Liénard 总功率；第11章给定新系速度的场变换符号，均经公式一致性与简单极限检查，未发现错误。Liénard–Wiechert 还宜声明粒子亚光速、远离粒子世界线，点源自场不用于未正则化的自力。
- 第1章内边界负号、第4章四极归一化与主值接触项、第5章介质球内场系数、第8章旋转球壳角动量系数均相互一致。

## 为完整教学目标补足的推导

本稿有清楚的主线和必要警示，但01–11章许多章节实际是数十行摘要。以下不是现有公式错误，而是面向此前仅学普通物理、微积分、常微分方程读者的可定位跳步。

- `07-maxwell.tex:14–20`：由规范自由跳到洛伦兹规范，缺规范能否达到及残余自由。补 $ (\nabla^2-c^{-2}\partial_t^2)\Lambda=-\nabla\cdot\mathbf A-c^{-2}\partial_tV$；达到后满足齐次波动方程的 $\Lambda$ 仍可变换。对库仑规范也应说明静态与动态的区别，避免读者误以为两种规范都是全时刻 $\nabla^2\mathbf A=-\mu_0\mathbf J$。第27行格林函数应标明当前算子的 $LG=-\delta^3\delta$ 约定，防止和 $LG=+\delta$ 习惯混淆。
- `10-radiation.tex:8–13,24–32`：写出电偶极势 $V=(4\pi\varepsilon_0)^{-1}[\mathbf n\cdot\mathbf p/r^2+\mathbf n\cdot\dot{\mathbf p}/(cr)]$ 与 $\mathbf A=\mu_0\dot{\mathbf p}/(4\pi r)$，至少展开一次 $-\nabla V-\partial_t\mathbf A$ 的辐射项，得到 $\mathbf n(\mathbf n\cdot\ddot{\mathbf p})-\ddot{\mathbf p}$。当前“横向投影来自抵消”是正确解释，但尚不是展示抵消的推导。再从 $dP/d\Omega=r^2S$ 和 $S=E^2/(\mu_0c)$ 给角功率并做 $\int\sin^2\theta,d\Omega$，能完成从场到功率的关键桥梁。
- `09-waves.tex:22,27`：斜入射只提供导纳而不实际给菲涅耳系数；波导只给模态表，没有从 PEC 条件推出 TM 的 Dirichlet、TE 的 Neumann，也未用横向场表达式解释 TE00 为什么不能传播。各补一个短推导及一个计算例题，比仅增加术语更有教学价值。
- 第3章球谐函数和第4章 STF：未定义 $Y_{\ell m}$ 的索引范围 $-\ell\le m\le\ell$，也没证明不同 $\ell$ 模态的正交性或给最低阶具体函数。读者先修中没有特殊函数，建议补 $\ell=0,1$ 与轴对称系数 $a_\ell=(2\ell+1)\int_{-1}^1f(x)P_\ell(x),dx/2$ 的例子，并说明 STF 维数 $2\ell+1$。
- `11-advanced.tex:9–14`：已诚实标为引用结论；为可用性应写明未减除形式要求 $\chi(\omega)\to0$ 的高频行为（若趋常数则对 $\chi-\chi_\infty$ 写关系），不只用“适当衰减”带过。无需假装给本科读者从零证明。

## 完成边界

正文宏中 $\eps=\varepsilon_0$，SI 恒等式 $c^{-2}=\varepsilon_0\mu_0$ 在前言明确，避免把第2章真空 $\eps$ 错当任意介质常数。本次核对没有依靠编译判定数学正确。最应优先修的是轴向绝对值、辐射区范围、固定控制体动量条件及正频率吸收限制；其余条件说明与教学展开按成书目标补足。尚未审查12–17考核章，不能把本报告称为整本题解已通过独立审查。
