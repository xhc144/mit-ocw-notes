# 22.611J Chap5：任意角冷波与 Landau／离子声阻尼来源复核

本轮只补等离子卷 QA，没有改正文或既有考题。实际读取仓库保存的 MIT OCW 公开 Chapter 5 *Electromagnetic Waves in Plasmas*，作者 **Ian Hutchinson**；2006 课程复用了他的讲义，不能因该课程授课人为 Ron Parker 而改署讲义作者。作者说明及逐件许可沿用 `qa/verified-attribution.json` 和课程来源清单；保留 OCW 非商业、相同方式共享及逐件例外。本报告的校核、代数补全和辅助计算均为自行完成，不能标成官方解答或官方勘误。

实际文件，两份均 49 页：

- Fall 2003：`sources/22-611j-introduction-to-plasma-physics-i-fall-2003/75c75c5df51f8fba1b2a903fde937ddc_chap5.pdf`；SHA256 `f87c212305063a3ee712f4c62cdc5ae81392c6484fd97e600a75f6dff0ade089`。
- Fall 2006：`sources/22-611j-introduction-to-plasma-physics-i-fall-2006/0940abd0f5c16aa3972c8796c8ca52e2_chap5.pdf`；SHA256 `945650190183c603108bfe6db6c393d1bb3416301e138f4d5452ff0d21b45cbd`。

来源：[2003 官方讲义页](https://ocw.mit.edu/courses/22-611j-introduction-to-plasma-physics-i-fall-2003/pages/lecture-notes/)，[2003 Chap5 资源页](https://ocw.mit.edu/courses/22-611j-introduction-to-plasma-physics-i-fall-2003/resources/chap5/)，[2006 官方课程](https://ocw.mit.edu/courses/22-611j-introduction-to-plasma-physics-i-fall-2006/)。下文按 2003 PDF 视觉核读；2006 同页关键公式的 TXT 也交叉核对，未将不同 SHA 的 PDF 说成同一二进制文件。

页码以下均明确区分 **PDF 页码（1 起算）／原印页码**，原印 96—144 比 PDF 页码多 95。

| 内容 | PDF／原印页码 | 公式或小节 |
|---|---|---|
| 冷流体方程、带符号回旋频率 | 10／105 | 5.58—5.64 |
| S,D,P,R,L，任意角完整波矩阵 | 11／106 | 5.65—5.75 |
| A,B,C、两根与判别式、Appleton—Hartree、角度形式 | 12／107 | 5.76—5.85 |
| 极点、初值与因果延拓 | 31—35／126—130 | 5.208—5.221，5.9.2—5.9.3 |
| 大相速实部、Maxwell 阻尼 | 35—36／130—131 | 5.223—5.232 |
| 离子声两物种响应、展开假设 | 44／139 | 5.274—5.278 |
| 离子声实部、弱阻尼通式 | 45／140 | 5.279—5.287 |
| 两物种 Maxwell 斜率及阻尼式 | 46／141 | 5.288—5.294 |
| Te≫Ti 的理由与完整 Z 函数的必要性 | 47／142 | 5.295—5.296 |

## 一、任意角冷等离子体波：不能止于平行和垂直端点

### 约定与适用模型

沿用原件空间时间因子 `exp[i(k·x−ωt)]`，背景均匀、静止、无碰撞，`B0=B0 ez`，忽略热运动。物种回旋频率 `Ωs=qsB0/ms` **带电荷符号**，电子 Ωe<0；`ωps²=nsqs²/(ε0ms)>0`。冷模型一般需热效应与吸收可忽略；原件第 9／104 页说明波相速远大于热速的适用范围。回旋共振附近仍需谨慎，不把理想冷极点当成完整吸收模型。

第 11／106 页：

\[
\epsilon=\begin{pmatrix}S&-iD&0\\iD&S&0\\0&0&P\end{pmatrix},\quad
S=1-\sum_s\frac{\omega_{ps}^2}{\omega^2-\Omega_s^2},\quad
D=\sum_s\frac{\Omega_s\omega_{ps}^2}{\omega(\omega^2-\Omega_s^2)},\quad
P=1-\sum_s\frac{\omega_{ps}^2}{\omega^2},
\]

\[
R=S+D=1-\sum_s\frac{\omega_{ps}^2}{\omega(\omega+\Omega_s)},\qquad
L=S-D=1-\sum_s\frac{\omega_{ps}^2}{\omega(\omega-\Omega_s)}.
\]

定义 `N=ck/ω`，θ 是 **k 与 B0 的夹角**；选择 ky=0、`Nx=N sinθ,Nz=N cosθ`。用 `𝕄` 表示原件 5.75 的归一化波矩阵，避免与介电标量 D 混用：

\[
\boxed{
\mathsf M=\epsilon-N^2I+\mathbf N\mathbf N
=\begin{pmatrix}
S-N^2\cos^2\theta&-iD&N^2\sin\theta\cos\theta\\
iD&S-N^2&0\\
N^2\sin\theta\cos\theta&0&P-N^2\sin^2\theta
\end{pmatrix},\quad\mathsf M\mathbf E=0.}
\]

原件早先 5.18 的 D 是有量纲矩阵，5.75 省略了公共 `ω²/c²`；正文明确用上面的无量纲矩阵即可，其非零标量因子不影响色散零点。

### 四次式与两根的全部系数

第 12／107 页 5.76—5.81 给

\[
\det\mathsf M=A N^4-BN^2+C=0,
\]

\[
\boxed{A=S\sin^2\theta+P\cos^2\theta,\quad
B=RL\sin^2\theta+PS(1+\cos^2\theta),\quad C=PRL,}
\]

\[
\boxed{N_\pm^2=\frac{B\pm F}{2A},\quad
F^2=B^2-4AC=(RL-PS)^2\sin^4\theta+4P^2D^2\cos^2\theta.}
\]

这里 A、B、C、F 均是波系数，不是前述背景磁场、频率或密度；**B 项是 `1+cos²θ`，F 第一项是 `sin⁴θ`**，易被 OCR 混成 `cos(2θ)`、`sin²θ`。这是一元 N² 的二次式，源于冷 ε 不显含 k；不能照搬到有空间色散的热／动力学 ε。

原件另给等价 Appleton—Hartree 形式及角度关系：

\[
N_\pm^2=1-\frac{2(A-B+C)}{2A-B\pm F},\qquad
\tan^2\theta=-\frac{P(N^2-R)(N^2-L)}{(SN^2-RL)(N^2-P)}.
\]

在 A 或所除因子为零时要回到完整行列式／矩阵；不能用除法式删去退化分支。特别地 θ=0 时 `det𝕄=P(N²−R)(N²−L)`：横场两根 R,L，另有 P=0 的纵向条件；θ=π/2 时 `(P−N²)(RL−SN²)=0`，普通支 P、非常支 RL/S。P=0、S=0、A=0 的特殊点不可盲目套两根式。

对一般角度、非退化根，取 Ex≠0 可由后两行直接得极化：

\[
\frac{E_y}{E_x}=-\frac{iD}{S-N^2},\qquad
\frac{E_z}{E_x}=-\frac{N^2\sin\theta\cos\theta}{P-N^2\sin^2\theta}.
\]

通常 E·k≠0，不能给两个斜传播模都贴“纯横波”标签。实 ω 且远离极点的冷 S,D,P 为实数，F²≥0；实 N²>0 可传播，N²<0 为倏逝。倏逝不是不可逆吸收。在非退化情形 C=0 给截止，A=0 可给无穷折射率；若分子也消失，应回矩阵判断消去或退化，不能把每个 A=0 都宣告物理共振。

### 可手算的小例子与实际矩阵复核

固定离子只中和电荷，保留冷电子响应；取 `ω/|Ωe|=1.5,ωpe²/Ωe²=0.5,θ=45°`。得
`S=0.6,D=−0.2666666667,P=0.7777777778,R=0.3333333333,L=0.8666666667`，
`A=0.6888888889,B=0.8444444444,C=0.2246913580,F²=0.09393689986`。

| 根 | N² | Ey/Ex | Ez/Ex | (E·k̂)/Ex |
|---|---:|---:|---:|---:|
| − | 0.390449883166 | +1.27256749218 i | −0.335119716965 | +0.470141356811 |
| + | 0.835356568447 | −1.13303260846 i | −1.15989689433 | −0.113064178272 |

辅助程序独立计算 3×3 行列式、代入极化验证 `𝕄E=0`，最大残差小于 `3×10⁻16`，并核对判别式恒等式和 Appleton—Hartree 两根。两模都含纵向电场。这是指定无量纲参数的独算，不是原课程提供的数值图或官方答案。

## 二、Landau 阻尼：初值轮廓、热速约定与完整指数

### 原件初值逻辑与一般纵向介电函数

第 31—35／126—130 页先处理 Imω>0，再连续解析延拓，保持速度轮廓在极点下方；第 34—35 页把这一做法与单侧 Laplace 初值变换联系起来。取 k>0、实正相速，令一维 `f0s(v)` 积分为 ns，`F0s=f0s/ns` 积分为 1。由 5.208、5.221 和 5.299 的等价整理：

\[
\epsilon_L(\omega,k)=1-\sum_s\frac{\omega_{ps}^2}{k^2}
\int_{\mathcal L}\frac{F'_{0s}(v)}{v-\omega/k}\,dv=0.
\]

对实 ω，从上半平面取因果边界值：

\[
\epsilon_r=1-\sum_s\frac{\omega_{ps}^2}{k^2}
\mathcal P\!\int\frac{F'_{0s}(v)}{v-\omega_r/k}\,dv,
\quad
\boxed{\epsilon_i=-\frac\pi{k^2}\sum_s\omega_{ps}^2F'_{0s}(\omega_r/k).}
\]

积分本身为主值 **加** `iπF′`；ε 前有负号，所以 εi 为上式负号。向下半平面延拓时不能重新沿未变形实轴积分，也不能用纯主值抹掉共振粒子。初值相混合可使波振幅衰减，完整无碰撞 Vlasov 系统的总能量仍守恒。

第 45—46／140—141 页 5.284—5.288 的弱阻尼通式是

\[
\omega=\omega_r+i\gamma,\quad \epsilon_r(\omega_r)=0,
\qquad\boxed{\gamma=-\frac{\epsilon_i(\omega_r)}{\partial_\omega\epsilon_r(\omega_r)}}.
\]

需 `|γ|≪|ωr|`，并且局部 `|∂ωεi|≪|∂ωεr|`、实部根非退化。不能在 εr=0 处声称简单的“εi≪εr”就是有意义的条件。正相速单峰 Maxwell 的 F′<0、通常正波能分母，给 γ<0；一般分布／负能模仍须核查分母，不能只看分布斜率。

### Maxwell 电子 Langmuir 波：第 35—36／130—131 页

原件 T 是能量单位温度（若用 K，应替换为 kBT），其热速尺度是
`σ=vt,source=√(T/m)`，Maxwell 一维分布

\[
F_0(v)=\frac1{\sqrt{2\pi}\sigma}\exp\!\left[-\frac{v^2}{2\sigma^2}\right],
\qquad\lambda_D=\frac\sigma{\omega_p}.
\]

单电子物种、固定离子、`kλD≪1`、弱阻尼的大相速展开给

\[
\omega_r^2\simeq\omega_p^2+3k^2\sigma^2,
\qquad
\boxed{\frac\gamma{\omega_p}\simeq
-\sqrt{\frac\pi8}\frac1{(k\lambda_D)^3}
\exp\!\left[-\frac1{2k^2\lambda_D^2}-\frac32\right].}
\]

这正是 5.232。**指数中的 −3/2 不能因外侧允许 ωr≈ωp 就一并丢弃**；由 5.231，将 Bohm—Gross 实频率修正放进共振速度的 Maxwell 指数产生此常数。γ 是场振幅增长率；波能的指数率为 2γ。

现有正文另用 `vt=√(2T/m)=√2σ` 的 Z 函数 convention；应明确转换：此时同式为

\[
\frac\gamma{\omega_p}\simeq-\sqrt\pi
\left(\frac{\omega_p}{kv_t}\right)^3
\exp\!\left[-\left(\frac{\omega_p}{kv_t}\right)^2-\frac32\right].
\]

不能用 √(2T/m) 却照抄 source 的 √(π/8) 及指数 1/2。对一般 k，用 |k| 与正频支写阻尼率即可，不应引入使对称 Maxwell 的负 k 波反而增长的 k³ 符号。

实际渐近公式复算：`kλD=0.15` 时 `γ/ωp=−9.2539245893×10⁻9`；0.2 时 `−6.5135418702×10⁻5`，后者 `|γ|/ωr=6.1547185510×10⁻5`。这些是上述受控渐近公式的实际值，未宣称已经求得完整复色散根。

## 三、离子声阻尼：电子小相速、离子大相速必须同时检查

第 44／139 页 5.274—5.278 对无磁化 Maxwell 电子、单电荷离子、无漂移且 ne=ni=n 采用
`σi≪ωr/k≪σe`，**两物种都可能共振**。电子实部按低相速展开得到 Boltzmann 响应、γe,fluid=1；离子按高相速展开保留三维中的一维 γi,fluid=3 热项。

令 `τ=Ti/Te,μ=me/mi,x=k²λDe²`，`λDe²=ε0Te/(ne²)`（分母这里是 n×e²，非 `(ne)²`）。第 45／140 页 5.279—5.280：

\[
\boxed{\epsilon_r\simeq1+\frac1x
-\frac{\omega_{pi}^2}{\omega_r^2}
\left(1+\frac{3T_i k^2}{m_i\omega_r^2}\right),
\quad
\epsilon_i=-\frac\pi{k^2}
[\omega_{pe}^2F'_{0e}(v_\phi)+\omega_{pi}^2F'_{0i}(v_\phi)],
\quad v_\phi=\omega_r/k.}
\]

### 原印内部不一致：必须说明，不静默照抄

1. 第 46／141 页 **5.289、5.290 实际把导数括号印成 `2+4×4Ti k²/(miωr²)`**，即 16Ti 项。直接微分上一页 5.279 必须是

\[
\boxed{\partial_\omega\epsilon_r
=\frac{\omega_{pi}^2}{\omega_r^3}
\left[2+\frac{12T_i k^2}{m_i\omega_r^2}\right]
=\frac{\omega_{pi}^2}{\omega_r^3}
\left[2+4\frac{3T_i k^2}{m_i\omega_r^2}\right].}
\]

后面的 5.293 已使用 3Ti，故修正有本页自证依据；没有找到 MIT 官方勘误。

2. 第 45／140 页 5.282 建议将离子实部换成 Padé／流体形式
`−ωpi²/(ω²−3Tik²/mi)`，而 5.283 印出

\[
\frac{\omega_r^2}{k^2}\simeq
\frac{T_e+3T_i}{m_i(1+x)}.
\]

这可作长波组合近似，**不是上述 Padé 介电函数保留任意 x 的精确代数根**。该 Padé 式实际给
`ωr²/k²=3Ti/mi+Te/[mi(1+x)]`；两者差为 `3Ti x/[mi(1+x)]`。若要同时保留 Ti 修正和有限 Debye 修正，必须交代遗漏的 τx 阶。原截断动理论式 5.279、Padé 替代式 5.282、组合近似 5.283 是三种不同的近似，不能一边用一个根一边把另一个函数的导数当成精确结果。

3. 第 46／141 页 5.294 按原印完整转录为

\[
\frac\gamma{\omega_r}\simeq
-\sqrt{\frac\pi2}\frac{(1+3\tau)^{3/2}}
{(1+x)^{3/2}[2+12\tau/(1+3\tau)]}
\left[\sqrt\mu+\tau^{-3/2}
\exp\!\left(-\frac{1+3\tau}{2\tau(1+x)}\right)\right].
\]

由前一个 5.293 中 `12Ti k²/(miωr²)` 与 5.283 代入，分母本应出现 `2+12τ(1+x)/(1+3τ)`；5.294 另丢掉了其中 τx。它不是对所有有限 x 与 τ 都精确等价的式子。第 47／142 页 5.296 又把 x→0 时的额外前因子印成
`(1+3τ)^(3/2)(1+3τ)/(1+6τ)≈1+3τ/2`。**这不能由 5.294 的分母推出**：5.294 对应的是

\[
\frac{(1+3\tau)^{5/2}}{1+9\tau}
=1-\frac32\tau+O(\tau^2),
\]

故不能把原件“保留一阶”的 +3τ/2 说成已核验系数。本报告只给清楚标明来源的原印式，以及下段一致地从指定 εr 微分的核验式。

### 可以直接用于正文的受控式与一致计算方法

最稳妥的教学顺序是先写两物种一般 `γ=−εi/∂ωεr`，说明各物种共振斜率，再给严格长波、τ≪1、μ≪1 的常用领先式：

\[
\boxed{\frac\gamma{\omega_r}\simeq
-\sqrt{\frac\pi8}
\left[\sqrt\mu+\tau^{-3/2}
\exp\!\left(-\frac1{2\tau}-\frac32\right)\right],
\quad\frac{\omega_r^2}{k^2}\simeq\frac{T_e+3T_i}{m_i}.}
\]

这是明确的弱阻尼、长波渐近式，第一项电子、第二项离子。有限 x 若使 `x/τ` 不小，不能随便在离子指数内设 x=0；要回到保留 x 的一致实根和一般弱阻尼式。T_i=0 时第二项取 τ→0 极限 0。第 47／142 页的物理结论准确：Te≫Ti 才将相速推离离子分布主体；Te~Ti 时离子阻尼可能很强，不能再套小 γ 的推导。

若选择明确保留 **5.279 截断模型**，不混用 Padé，可令 `y=mi(ωr/k)²/Te`；这个模型的实根、导数与两种 Maxwell 斜率给出

\[
\boxed{y=\frac{1+\sqrt{1+12\tau(1+x)}}{2(1+x)},}
\]

\[
\boxed{\frac\gamma{\omega_r}\simeq
-\sqrt{\frac\pi2}\frac{y^{3/2}}{2+12\tau/y}
\left[\sqrt\mu e^{-\mu y/2}
+\tau^{-3/2}e^{-y/(2\tau)}\right].}
\]

这是本报告从指定 εr 独立整理的式子，**在截断模型内代数一致，不是完整动理论精确复根**。电子指数 `exp(−μy/2)` 通常近 1，本报告保留以便直接与 Maxwell 斜率核对。其适用条件仍是 √(μy)≪1、√(y/τ)≫1 和小 |γ|/ωr，不能因写成闭式就越过渐近范围。

如需 Te~Ti 或较强阻尼，原件 47／142 页要求完整 Plasma Dispersion Function。由原件两物种积分 5.274 代入 Maxwell 并改用正文 `vts=√(2Ts/ms)` 可直接得到全 Maxwell 动理论公式：

\[
\boxed{\epsilon_L=1+\sum_s\frac1{k^2\lambda_{Ds}^2}
[1+\zeta_sZ(\zeta_s)]=0,
\quad\zeta_s=\frac\omega{k v_{ts}},\quad
\lambda_{Ds}^2=\frac{\epsilon_0T_s}{n_sq_s^2},}
\]

\[
Z(\zeta)=\frac1{\sqrt\pi}\int_{\mathcal L}
\frac{e^{-u^2}}{u-\zeta}\,du
=i\sqrt\pi e^{-\zeta^2}\operatorname{erfc}(-i\zeta).
\]

这里 Z 采用因果解析延拓；实轴弱阻尼展开中的指数项不能不加区分推广成所有复 ζ 的统一渐近式。完整复根求解才适合检验较强阻尼，本轮未声称已执行这类求解。

### 实际小例子与导数勘误验证

取氢质量比 μ=1/1836、x=0.01，采用上述 **明确的 5.279 截断模型**。辅助程序先求该 εr 的精确实根，然后分别用 Maxwell 斜率／解析导数和整理后的 y 式计算弱阻尼；另以中心差分核验导数。

| τ | y | γe/ωr | γi/ωr | γ合计/ωr | 5.289 原印导数相对误差 |
|---:|---:|---:|---:|---:|---:|
| 0.01 | 1.019241247206 | −0.0142084596465 | −4.48809×10⁻20 | −0.0142084596465 | +1.85315% |
| 0.05 | 1.122416115344 | −0.0137188884231 | −0.000702007502036 | −0.0144208959251 | +7.03029% |

εr 的实际根残差小于 `3×10⁻14`；中心差分导数与正确解析导数相对误差小于 `3×10⁻10`，而原印 16Ti 项偏离。两个 γ 算法之差小于 `10⁻14`。这验证本报告转录、微分和截断模型整理的内部一致性，不验证完整 Z 色散根，也不将图上看起来“振荡”当成弱阻尼的证明。

## 四、交付与范围

- 本 QA：`qa/followup-chap5-wave-kinetic-review.md`。
- 标准库辅助：`qa/followup-chap5-checks.py`。
- 本次实际运行结果：`qa/followup-chap5-checks.json`；全部断言通过。

重现：

```bash
python subjects/plasma-physics/qa/followup-chap5-checks.py
```

已完成来源页码／公式视觉核读、任意角矩阵和根复核、热速与 Landau 指数核验、离子声原印内部不一致的推导与独算。没有使用受限教材，没有新增旧考题扫描，没有改正文或全局清单。正文补写时可采用上面已定义全部变量的公式，并明确区分官方原印、编者勘误和受控近似。
