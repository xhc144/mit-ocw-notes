# Lecture 21—22：位置模、Mercier 与 s—α 缺项复核

本轮针对 `chapters/ch17.tex` 缺少具体环形稳定理论的问题，实际核读 MIT OCW、Jeffrey Freidberg、22.615 Spring 2007 的以下公开 PDF。页码均为 PDF 页数与原件页脚一致的 **1 起算页码**：

- `sources/22-615-mhd-theory-of-fusion-systems-spring-2007/c50154763bbb2675fc4b71e4ae4f4203_lecture21.pdf`，10 页。
- `sources/22-615-mhd-theory-of-fusion-systems-spring-2007/3d8c6e9543029684ca2dd49d7dc6e31a_lecture22.pdf`，11 页。

来源入口：[MIT 22.615 Spring 2007](https://ocw.mit.edu/courses/22-615-mhd-theory-of-fusion-systems-spring-2007/)。原课程材料按主题来源清单保留作者、OCW 非商业/相同方式共享条款和逐件例外。本报告是独立核读与推导，不是官方解答；没有归档、复写第三方受限教材。

结论：现有泛型 A/C/M 和文字性 Mercier 说明不能代替下列实际公式。n=0 位置模、一般 ballooning 能量与 s—α 方程均已核实。一般 Mercier 原印末因子有量纲与磁面依赖错误；**本报告从 Lecture 21 的实际能量式独立导出应有的加权平均平方，并用同课程圆柱 Suydam 极限复算确认**。这可作为明确标注的编者推导，不能冒称取得了 MIT 官方勘误。近轴非圆公式中 βp0 的精确中心归一化在这两讲未定义，保留这一来源限制。

## 一、Lecture 21 前半：n=0 竖直/水平位置稳定

### 页码与模型假设

- 第 1 页：n=0 轴对称模；直柱中的 m=1 整体位移在无壁/对称条件下中性，环形中必须区分竖直与水平位移。
- 第 2 页：将等离子体视为理想导电电流环，忽略压强、内部磁场和抗磁性；嵌在外部磁场中，扰动时回路所链总磁通守恒。均匀竖直场下，竖直平移因对称性中性。
- 第 3—4 页：电感、守恒磁通、力及平衡、竖直恢复系数和场指数。
- 第 5 页：水平条件给成近似 `n≲3/2`，并转入高 n 压力模。

这是**细电流环的位置模近似**，不能说成任意压强、拉长形状、真空壁和反馈系统的完整 tokamak 稳定定理。对水平变化把有效线环截面半径 a 视为常数；竖直与水平单独判断还采用中平面的上下对称，避免混合力导数。若上下不对称，应检查完整二维力 Jacobian/势能 Hessian。

### 守恒量、力与平衡：不可误当固定电流

令 R 为电流环大半径，Z 为位置，I 的回路方向按原件磁通符号约定；R0,Z0 为平衡位置。采用

\[
L(R)=\mu_0R\left[\ln\frac{8R}{a}-2\right],\qquad
U(R,Z)=\frac12L(R)I(R,Z)^2,
\]

\[
\mathcal F=LI-\Phi_{\rm ext}=\mathrm{const},\qquad
\Phi_{\rm ext}=2\pi\int_0^R B_Z(R',Z)R'\,dR'.
\]

这里 `𝓕` 是**整回路所链磁通**；不要与后文每弧度极向磁通 ψ 混成同一个归一化变量。外场在环附近无电流，满足 `∇×Bext=0` 和 `∇·Bext=0`。由磁通约束得

\[
L I_Z+2\pi RB_R=0,\qquad
L I_R+I L'-2\pi RB_Z=0.
\]

因此能量梯度给

\[
F_Z=-LI I_Z=2\pi RI B_R,
\qquad
F_R=-LI I_R-\frac{I^2}{2}L'
=\frac{I^2}{2}L'-2\pi RI B_Z.
\]

第 3 页两处把所需 `∂L/∂R` 印成了 `∂I/∂R`（FR 最后一项及磁通径向导数式的第二项）；第 4 页使用 L 正确。以上从 `U=LI²/2` 和磁通式直接微分得到，给出可验证的勘误依据。

平衡条件为

\[
B_R(R_0,Z_0)=0,\qquad
B_Z(R_0,Z_0)=\frac{I}{4\pi R_0}L'(R_0)
=\frac{\mu_0I}{4\pi R_0}\left[\ln\frac{8R_0}{a}-1\right].
\]

### 两个恢复系数与场指数

为避免和后面的环向模数 n 混淆，将第 4 页的场指数记成

\[
n_B=-\frac{R_0}{B_Z}\frac{\partial B_Z}{\partial R}\bigg|_0.
\]

在平衡处 `BR=0`，利用 `∂ZBR=∂RBZ`：

\[
K_Z\equiv\frac{\partial F_Z}{\partial Z}\bigg|_0
=2\pi R_0I\frac{\partial B_R}{\partial Z}\bigg|_0
=-\frac{I^2L'}{2R_0}n_B.
\]

通常 `L′>0`，故竖直恢复力条件 `KZ<0` 是 **nB>0**，nB=0 中性。这一结论不因同时翻转 I、BZ 的回路方向而变。

原件只给水平近似结果；用相同磁通约束独立补全径向微分，在平衡处 `IR=−IL′/(2L)`，得到

\[
K_R\equiv\frac{\partial F_R}{\partial R}\bigg|_0
=\frac{I^2}{2}\left[L''-\frac{L'^2}{2L}
+(n_B-1)\frac{L'}{R_0}\right].
\]

所以在本固定 a 的线环模型中

\[
n_B<n_{B,\rm crit}
=1-\frac{R_0L''}{L'}+\frac{R_0L'}{2L}
=1-\frac1{\ell-1}+\frac{\ell-1}{2(\ell-2)},
\quad\ell=\ln(8R_0/a).
\]

在领先对数近似下它趋于 **3/2**，故第 5 页的合并条件是近似 `0<nB≲3/2`，不是没有模型误差的普适严格常数。若错误地固定 I 而非磁通，会丢失 `−L′²/(2L)` 项，得不到该水平限。

### 可独算的线环小例子

取 `R0=1 m,a=0.1 m,I=10⁶ A`：`L=2.9933429505 μH`、平衡 `BZ=0.3382026635 T`，保留电感式全对数项的 `nB,crit=1.4142245944`。

| nB | KZ（N/m） | KR（N/m） | 结论，仅在线环模型中 |
|---:|---:|---:|---|
| −0.5 | +1.0624950×10⁶ | −4.0677081×10⁶ | 竖直失稳，水平恢复 |
| 0.5 | −1.0624950×10⁶ | −1.9427181×10⁶ | 两方向均恢复 |
| 2 | −4.2499800×10⁶ | +1.2447669×10⁶ | 竖直恢复，水平失稳 |

辅助程序另从守恒磁通构造 I(R,Z) 并直接差分 `−URR,−UZZ`，与上述解析系数一致。它只使用局部外场 `BZ(R,0)∝R^(−nB)` 的真空 Taylor 延拓，未将有中心奇性的幂律外场假装成遍布整个装置的完整线圈解。

## 二、Lecture 21 后半：ballooning 的实际能量与变量

第 6—7 页用高环向模数 n、非零磁剪切、eikonal 表示 `ξ⊥=η⊥ exp(i𝓢)`、`B·∇𝓢=0`。选择平行位移消除气体压缩；再极小化最高阶磁压缩。领先幅度 `η⊥0=Y b×k⊥`，令 `X=YB`，平行电流 kink 项在这一高 n 领先阶不进入，剩下线弯曲与压力—曲率竞争。不要据此说 n=1 外 kink 项也消失。

第 7—8 页的具体坐标定义为

\[
\mathbf B=\frac F R\mathbf e_\varphi+
\frac{\nabla\psi\times\mathbf e_\varphi}{R},\qquad
\nabla\psi\cdot\nabla\chi=0,\quad
B_p=|\nabla\psi|/R,
\]

\[
dV=2\pi J\,d\psi\,d\chi,
\qquad \frac R J=\mathbf e_\varphi\cdot(\nabla\chi\times\nabla\psi)
=R\mathbf B_p\cdot\nabla\chi.
\]

`J` 是有量纲磁面坐标 Jacobian，**不是**期中逆坐标的无量纲 `𝓙`。令

\[
\mathbf n=\frac{\nabla\psi}{|\nabla\psi|},\quad
\mathbf b=\mathbf B/B,
\quad\mathbf t=\frac{B_\varphi}{B}\mathbf b_p-
\frac{B_p}{B}\mathbf e_\varphi,
\quad\boldsymbol\kappa=\kappa_n\mathbf n+\kappa_t\mathbf t.
\]

其中 κn 是法曲率，κt 是测地曲率。局部绕行量和整体 q 为

\[
\widehat q(\psi,\chi)=\frac{JB_\varphi}{R},\qquad
q(\psi)=\frac1{2\pi}\int_0^{2\pi}\widehat q\,d\chi.
\]

第 9 页解释磁剪切使普通 2π 周期表示失效，须用无限 χ 的衰减准模，再对 `χ+2πp` 求和恢复周期性。第 10 页给出

\[
\delta W_2=\frac\pi{\mu_0}\int d\psi\,W(\psi),
\]

\[
W(\psi)=\int_{-\infty}^{\infty}J\,d\chi\left[
(k_n^2+k_t^2)\left|\frac1{JB}\frac{dX}{d\chi}\right|^2
-\frac{2\mu_0RB_p}{B^2}\frac{dp}{d\psi}
(k_t^2\kappa_n-k_tk_n\kappa_t)|X|^2\right],
\]

\[
k_t=\frac{nB}{RB_p},\qquad
k_n=nRB_p\int_{\chi_0}^{\chi}\frac{\partial}{\partial\psi}
\left(\frac{JB_\varphi}{R}\right)d\chi'.
\]

允许边界是 `X(−∞)=X(+∞)=0` 且衰减足够快使能量和准模周期求和收敛。**每一磁面及各 χ0 都要检查**；一个位置/一条线上的正能不能证明全等离子体稳定。泛型 A/C/M 只有在这些具体系数、变量和边界已交代后才可作进一步概括。

## 三、Lecture 22：Mercier 判据及原件问题

### 第 1—3 页的量词与完整原式

第 1—2 页解释大 |χ| 渐近的两类解：违反 Mercier 条件时发生局域 interchange，不应把振荡且不满足收敛要求的无限角解当成有限能 ballooning 本征函数。Mercier 通过只是排除这一局域压力模，不排除进一步的 ballooning 不稳定；须再从一端的允许衰减解积分、看零点。第 3 页明确采用 **DM<1/4** 的稳定符号约定，不应换成其他文献名同而号不同的 D。

第 3 页印出的完整定义，忠实转录为

\[
D_M^{\rm printed}=\frac{\mu_0p'_\psi}{(q'_\psi)^2}
\left[2\left\langle\frac{RB_p\kappa_n}{B^2}\right\rangle_M
+\left\langle\frac{\Lambda_M}{B^4}\right\rangle_M
-\left\langle\frac1{B^2}\right\rangle_M
 \left\langle\frac{\Lambda_M}{B^2}\right\rangle_M\right]
\bigg/\left(\frac{R^2B_p^2}{JB^2}\right),
\]

\[
\Lambda_M=F\left(\mu_0p'_\psi F-
\frac{R^2B_p^2}{J}\frac{\partial\widehat q}{\partial\psi}\right),
\qquad p'_\psi=dp/d\psi,\quad q'_\psi=dq/d\psi,
\]

\[
\langle Q\rangle_M=
\frac{\int_0^{2\pi} Q\,\dfrac{B^2}{R^2B_p^2}\,J\,d\chi}
{\int_0^{2\pi}\dfrac{B^2}{R^2B_p^2}\,J\,d\chi}.
\]

这是 Mercier 特定的加权平均，不能换成期中普通的 `dlp/Bp` 磁面平均。以上 `ΛM` 也不是下一节 s—α 的 `ΛB`，更不是期末等效壁 `Λℓ`。

### 原件末除子的实际印刷问题

实际放大检查第 3 页 PDF：大方括号之后印的是**裸的** `R²Bp²/(JB²)` 作除子，没有磁面平均括号，也没有整体平方。不是仅 TXT 漏字。按第 7—8 页未归一化的原定义：

\[
[\psi]={\rm T\,m^2},\quad[J]={\rm m/T},\quad[F]={\rm T\,m},
\quad\left[\frac{R^2B_p^2}{JB^2}\right]={\rm T\,m},
\]

\[
[\mu_0p'_\psi/(q'_\psi)^2]={\rm T^3m^2},\quad
[\text{方括号}]={\rm T^{-1}}.
\]

所以字面 DM 带有 `T m` 量纲，并且末除子一般依赖 χ，不能直接作为只依赖 ψ 的无量纲阈值量与 1/4 比较。仅靠量纲相容不能确认应如何修正。以下实际从本课程上一讲的 W 推出修正，并用圆柱极限独算，而非换用另一套记忆中的 Mercier 定义。本次没有获得 MIT 的更正文件；正文必须区分原印错误与本卷独立推导的修正式。

### 从原能量式独立补全末因子

本段为编者独立推导。采用正 J 的磁面方向、非零 `q′ψ`、周期且光滑的磁面系数，避开磁轴/分离面奇异处；只取大 |χ| 渐近的局域 interchange 系数，不声称解出了整个 ballooning 谱。先令

\[
A=\frac{R^2B_p^2}{JB^2}>0,\quad w=A^{-1},\quad
c=\frac1{JR^2B_p^2},\quad
h=\int_{\chi_0}^{\chi}\partial_\psi\widehat q\,d\chi',
\quad h'=\partial_\psi\widehat q,
\]

\[
u=\frac{\mu_0p'_\psi F}{B^2},\qquad
C=\frac{RB_p\kappa_n}{B^2},\qquad
g_0=\frac{2\mu_0p'_\psi J\kappa_n}{RB_p}
=2\mu_0p'_\psi w C.
\]

这里对 χ 的导数只用于 `h′,u′,X′`；`p′ψ,q′ψ` 始终对 ψ 求导。将上一讲的 `kn=nRBph,kt=nB/(RBp)` 代入 W，除去正的 n² 因子：

\[
\frac W{n^2}=\int d\chi\left[
(Ah^2+c)|X'|^2-g_0|X|^2
+\frac{2\mu_0p'_\psi J RB_p\kappa_t}{B}h|X|^2\right].
\]

平衡的 t 方向上 `t·∇p=0`，由张力与磁压平衡得 `κt=(t·∇B)/B`；轴对称坐标下

\[
\mathbf t\cdot\nabla=
\frac F{RJB B_p}\frac\partial{\partial\chi},
\qquad
\frac{2\mu_0p'_\psi J RB_p\kappa_t}{B}=-u'.
\]

所以测地曲率项是 `−u′h|X|²`。对衰减函数分部积分并完成平方，可得（复 X 时交叉项取实部）

\[
\frac W{n^2}=\int d\chi\left[
A\left|hX'+\frac uA X\right|^2+c|X'|^2
-\mu_0p'_\psi w\left(2C+\frac{\Lambda_M}{B^4}\right)|X|^2\right].
\]

核验平方剩余项的恒等式是

\[
uh'-\frac{u^2}A
=-\mu_0p'_\psi w\frac{\Lambda_M}{B^4},
\]

故 ΛM 与原件第 3 页定义完全相同，不需更改任何曲率或 ΛM 符号。

接着 `h=q′ψχ+周期有界项`，记普通一周期平均为横杠，定义

\[
A_{\rm eff}=\frac1{\overline w}
=\langle A\rangle_M=\frac{2\pi}{\int_0^{2\pi}w\,d\chi},
\qquad \bar u_M=\langle u\rangle_M.
\]

令 X 由慢包络 Y 加 `f(χ)Y/χ` 的周期修正组成（`\overline{f′}=0`）。领先平方项中可变的周期梯度是
`q′ψχY′+q′ψ f′Y+(u/A)Y`。在一周期内极小化其 A 加权平方，使通量常数除以 A；结果为

\[
\overline{A\left|hX'+\frac uA X\right|^2}
\sim (q'_\psi)^2A_{\rm eff}
\left|\chi Y'+\frac{\bar u_M}{q'_\psi A_{\rm eff}}Y\right|^2.
\]

`c|X′|²` 比该项低两阶；周期势能项平均为
`−(μ0p′ψ/Aeff)〈2C+ΛM/B⁴〉M|Y|²`。展开平方中的交叉项，利用
`∫χ(|Y|²)′dχ=−∫|Y|²dχ`，再利用

\[
\langle Ah'\rangle_M=A_{\rm eff}q'_\psi,
\qquad
\left\langle\frac{\Lambda_M}{B^2}\right\rangle_M
=F\left(\bar u_M-A_{\rm eff}q'_\psi\right),
\]

得到大 |χ| 的包络能量

\[
\frac{W_{\rm asym}}{n^2}
\sim(q'_\psi)^2A_{\rm eff}\int
\left[\chi^2|Y'|^2-D_M|Y|^2\right]d\chi,
\]

\[
\boxed{
D_M=\frac{\mu_0p'_\psi}{(q'_\psi)^2\langle A\rangle_M^2}
\left[
2\left\langle\frac{RB_p\kappa_n}{B^2}\right\rangle_M
+\left\langle\frac{\Lambda_M}{B^4}\right\rangle_M
-\left\langle\frac1{B^2}\right\rangle_M
 \left\langle\frac{\Lambda_M}{B^2}\right\rangle_M
\right],\qquad A=\frac{R^2B_p^2}{JB^2}.
}
\]

**因此原件裸除子应由 `〈R²Bp²/(JB²)〉M²` 代替。** 它的量纲为 `(T m)²`，修正式无量纲、仅随磁面 ψ 改变。包络 Euler 方程

\[
(\chi^2Y')'+D_MY=0,
\qquad Y\sim|\chi|^{-1/2\pm\sqrt{1/4-D_M}}
\]

直接给出原件的 1/4：`DM>1/4` 时尾部按 log|χ| 振荡，可构造负能局域 interchange；`DM<1/4` 才有有限能的非振荡尾分支。等号是临界情形，不能靠这一步宣告稳定。通过只是局域必要条件；还须检查有限角 ballooning 能量及各 χ0。

### 圆柱极限：从完整修正式到同课程 Suydam，并实际复算

取周期直柱长度 `2πR0`，在同一磁通约定中令 `R=R0,Bp=Bθ,J=r/Bθ,F=R0Bz,ψr′=R0Bθ`。圆柱面所有系数与 χ 无关，故 ΛM 的协方差项恰好为零；曲率是

\[
\kappa_n=-\frac{B_\theta^2}{r(B_z^2+B_\theta^2)},\qquad
q=\frac{rB_z}{R_0B_\theta}.
\]

完整修正式简化为

\[
D_M=D_S=-\frac{2\mu_0p_r'q^2}{rB_z^2q_r'^2},
\quad D_S<\frac14
\iff rB_z^2\left(\frac{q_r'}q\right)^2+8\mu_0p_r'>0.
\]

这与实际公开 Lecture 18 第 8 页 `DS=−2k²μ0p′/(rF′²)`、`F′=kBzq′/q` 的直接代入结果，以及第 11 页最终 Suydam 判据一致（原件 prime 为 r 导数）。**再次视觉核对发现 Lecture 18 第 9 页首框的 DS 分母把 r 印成了 r²**，它与第 8 页和第 11 页不一致，也使 DS 带长度倒数的量纲；本报告不冒称与这行错误原印逐字一致。这里明确用第 8 页推导和第 11 页最终判据检验 Mercier 修式。该检验不是把直柱判据当成环形全局稳定判据。

小例子采用 `R0=3 m,r=0.5 m,Bz=2 T,Bθ=0.3 T,q=1.1111111111,q′r=0.8 m⁻¹`：

| p′r（Pa/m） | 完整修正式 DM | 直接 Suydam DS | Suydam 左端（T²/m） | 局域结果 |
|---:|---:|---:|---:|---|
| −100000 | 0.242406840554768 | 0.242406840554768 | +0.0314903508512661 | 通过 |
| −120000 | 0.290888208665722 | 0.290888208665722 | −0.169571578978481 | 失败 |

辅助程序另构造 Bθ′、Bz′，同时满足指定 q′ 和径向平衡
`μ0p′r+BθBθ′+BzBz′+Bθ²/r=0`，平衡残差小于 `9×10⁻16 T²/m`；不是给互不相容的 p′、q′ 作机械代入。完整 DM 和 DS 的实际差小于 `6×10⁻17`。本例只构成局部平衡数据，没有声称构造了带壁、有限半径的完整稳定螺旋箍缩。

### 第 3—4 页：圆截面与近轴非圆简化

对大长径比、圆截面、`βp∼1` 的 tokamak，第 3 页给

\[
\boxed{\frac{r^2q_r'^2}{q^2}+4r\beta_r'(1-q^2)>0},
\qquad q_r'=dq/dr,\quad\beta(r)=2\mu_0p(r)/B_0^2.
\]

这里 prime 改为 **对 r 求导**，不是上面精确式的对 ψ 求导；β 是局部压强 beta，不是体积平均 βt。向外减压时 βr′<0，q>1 使压力项为正，q<1 使它为负。轴附近 `q=q0+O(r²)` 时，剪切项通常 O(r⁴)，压力项 O(r²)，所以负压强梯度下需 **q0>1**；q0=1 是需要更高阶判断的边界，不能由本式首项直接宣告稳定。

原件第 3 页近轴非圆形式为

\[
1<q_0^2\left\{1-\frac4{1+3\kappa_e^2}
\left[\frac34\frac{\kappa_e^2-1}{\kappa_e^2+1}
\left(\kappa_e^2-\frac{2\delta}{\epsilon}\right)
+\frac{(\kappa_e-1)^2\beta_{p0}}{\kappa_e(\kappa_e+1)}\right]\right\}.
\]

其中 κe 为磁面拉长、δ 为三角度、ε 为小长径比；用 κe 与前文曲率 κ 区分。**第一系数是 `(3/4)×(κe²−1)/(κe²+1)`，不是 `(3κe²−1)/(4κe²+1)`**，TXT/OCR 不足以辨别这个乘积。第 4 页说明 κe=1 时三角度和 βp0 项消失；κe>1 时压力项降低稳定裕度，正三角度提高裕度。不能把拉长本身说成无条件稳定。

`βp0` 在这两讲所选公开页面中未给出精确的中心归一化定义，本报告保留原符号，不据记忆补成 `2μ0p0/Bp(0)²`（轴上 Bp=0，这个写法会出错），也不利用未明确的 βp0 构造数值例子。

### 可独算的圆截面 Mercier 小例子

取 `x=r/a`、`q=q0+0.4x²`、`β=0.04(1−x²)`，在 x=0.1 检查：

| q0 | 剪切项 | 压力项 | 判据左端 |
|---:|---:|---:|---:|
| 0.95 | 7.0320706×10⁻5 | −2.8762880×10⁻4 | −2.1730809×10⁻4，局域判据失败 |
| 1.05 | 5.7610116×10⁻5 | +3.5493120×10⁻4 | +4.1254132×10⁻4，该点局域判据通过 |

这只检验上述圆截面局域近似和该点；不推断全半径、ballooning 或外 kink 稳定。

## 四、Lecture 22 第 5—6 页：具体 s—α 方程

### 假设、变量、符号与边界

第 5 页采用大长径比圆截面、`βp∼1`，但压力梯度层较窄、`rβp′∼1/ε`。领先近似是

\[
\chi\to\theta,\quad J\to r/B_\theta,
\quad R\to R_0,\quad B\to B_0,\quad B_p\to B_\theta(r),
\quad \kappa_n\to-\cos\theta/R_0,
\quad \kappa_t\to\sin\theta/R_0,
\quad \frac{dp}{d\psi}\to\frac1{R_0B_\theta}\frac{dp}{dr}.
\]

**这里对原件两处作有依据的编者勘误。** 第 5 页将最后一个映射印成 `1/(rBθ)`；但由本讲沿用的 `Bp=|∇ψ|/R`，圆截面必须有 `dψ/dr=R0Bθ`，从而是 `1/(R0Bθ)`。否则下面 α 系数会错误地多出 R0/r。第 5 页相位积分及第 6 页局部 q 定义的分子印为 `JBθ`；按 Lecture 21 第 9—10 页的场线绕行定义，它应为 `JBφ`。用 `J=r/Bθ` 检查，错误下标会得到 `qhat=r/R0` 而不是实际 q。正文应解释这些修正，不能无说明照抄原印行。

θ 是从外侧坏曲率区 θ=0 起算的极向/无限场线角。定义

\[
S=\frac r q\frac{dq}{dr},\qquad
\alpha=-\frac{2\mu_0r^2p_r'}{R_0B_\theta^2}
=-q^2R_0\frac{d\beta}{dr},\qquad
q=\frac{rB_0}{R_0B_\theta}.
\]

向外减压的 p_r′<0 对应 **α>0**；S 是全局磁剪切，S 可正可负，假设非零剪切的高 n 推导不能不加说明在 S=0 奇异极限使用。θ0 是相位/定位参数，需要改变 θ0 找最危险情况。令

\[
\Lambda_B=S(\theta-\theta_0)-\alpha(\sin\theta-\sin\theta_0).
\]

原件 Euler—Lagrange 方程的全部系数为

\[
\boxed{\frac d{d\theta}\left[(1+\Lambda_B^2)\frac{dX}{d\theta}\right]
+\alpha(\Lambda_B\sin\theta+\cos\theta)X=0},
\quad X(-\infty)=X(+\infty)=0.
\]

这是边界/零频能量方程，不是已经给出惯性归一化 M 的完整增长率本征方程。对应正公共因子略去的能量是

\[
W_{S\alpha}[X]=\int_{-\infty}^{\infty}
\left[(1+\Lambda_B^2)|X'|^2
-\alpha(\Lambda_B\sin\theta+\cos\theta)|X|^2\right]d\theta.
\]

将上一节一般 W 代入圆截面近似可直接验系数：`kn/kt=ΛB`，线弯曲的公共正系数是 `n²/(rR0²Bθ)`；压力项除以同一系数后正好成为 `2μ0r²p_r′(cosθ+ΛB sinθ)/(R0Bθ²)=−α(cosθ+ΛB sinθ)`。这同时独立核验原 ODE 的 α 系数，以及 `dp/dψ` 映射应含 R0 的勘误。

在 θ=0、θ0=0 外侧，驱动项是 `−α|X|²`，核实其为坏曲率负能；不应把 ODE 中的加号误抄成能量中的加号。其导数 `ΛB′=S−α cosθ` 是第 6 页解释第二稳定区的局部剪切调制；全局 S 不能替代这个局部量。

第 6 页图示第一稳定区、夹在中间的不稳定区和第二稳定区；这不是“增加 alpha 总使系统更不稳”。同页的 `α≈0.6S` 是第一稳定区上界的估计，随后 `βt≲0.3ε/qa` 另假设 `qa≫1,q0=1`、圆截面。优化拉长/三角度的 ballooning 数值限 `βt≲0.22εκe/q*` 与后面第 9 页外 kink/Troyon 的 `0.14εκe/q*` 是不同结果，不可混称一个精确普适 beta 界。

### 可独算的负能小例子：有解析值，不靠采样图猜稳定

取 θ0=0，允许函数 `X(θ)=exp(−θ²/2)`，满足无穷远和有限能条件。Gaussian 的三角矩可直接积分，得到

\[
\frac{W_{S\alpha}[X]}{\sqrt\pi}
=\frac12+\frac34S^2
-\alpha e^{-1/4}\left(1+\frac74S\right)
+\frac{3-e^{-1}}4\alpha^2.
\]

取 S=1：

| α | 该试探函数能量 | 能证明什么 |
|---:|---:|---|
| 0 | +2.2155673136 | α=0 时整个泛函是非负线弯曲项；无压力驱动 |
| 1.4 | **−0.8129252194** | 一个允许负能方向足以证明此 s—α 模型在该参数/相位不稳定 |
| 4 | +5.6925432783 | 仅说明这一函数回到正能，不能证明所有 X/θ0 都稳定 |

这里不把 α=4 的单试函数结果称作已证明的第二稳定区，也不把本表说成精确稳定边界。辅助程序以 10,000、20,000 区间 Simpson 求积独立核对解析能量，误差小于 10⁻12；没有执行大范围新稳定扫描。

## 五、实际复算状态与正文建议

辅助文件仅在 QA 目录：

- `followup-mhd-theory-checks.py`：标准 Python 库，独算线环恢复系数、圆截面 Mercier 例子、完整修正式的圆柱/Suydam 极限以及 Gaussian ballooning 能量。
- `followup-mhd-theory-checks.json`：本次实际运行结果；程序断言均通过。

重现：

```bash
python subjects/plasma-physics/qa/followup-mhd-theory-checks.py
```

正文至少应补三个有具体公式的教学块：n=0 的磁通守恒—位置力—场指数；Mercier 特殊平均/局域量词、由原能量推导的完整修正式及圆截面简化；一般 ballooning 到具体 s—α 的系数、边界和负能例子。一般 DM 的末因子已由本报告推导及圆柱实际复算核验，但须明确原印问题和编者修正，不能冠以“MIT 官方勘误”。非圆近轴 βp0 的公开材料定义不足仍须保留。现有 ch17 的泛型 A/C/M 可以保留为抽象总结，不能当作上述三块的完成替代。

本轮仅写这份 QA 与必要独算辅助，没有改正文、其他主题、全局清单或既有考题数值。
