# 中文电动力学修订稿独立复核

日期：2026-10-11。正文只读，本轮检查01–16章此前报告列出的修订位置，并通读新增 `17-advanced-assessments.tex`。实际阅读 8.311 `final.txt`，直接渲染并查看 `final_solution.pdf` 的全部四页手写原件，逐题比较模型、子问、场幅值和高斯制系数。独立复算如下；不以编译、上传或来源哈希推定数学通过。

## 前轮问题处理

- 圆环远场已改 $|z|^3$ 并明确电流方向；电容矩阵已加无外部固定源条件。
- 固定控制体的应力积分先保留 $\int\mathbf f$，机械动量与角动量通量条件已补，符号无回退。
- 辐射区增加 $kr\gg1$，几何远区与准静态近场区分明确。电偶极势的标势–矢量势抵消和场到角功率的推导已补，现有 $\mathbf n\times(\mathbf n\times\ddot{\mathbf p})$ 符号正确。
- 规范函数波动方程、残余自由、动态库仑规范、格林函数负源约定及亚光速点电荷限制已补，未发现新反号。
- 介质能量的静止、瞬时、时间不变、对称构成条件补齐；反射、导体和负折射公式的各向同性与频带限制补齐；正频率吸收及 KK 高频减除条件补齐；无源腔、无静电背景及模态归一化补齐。
- 新增球谐低阶函数、正交性说明、轴对称系数、菲涅耳切向振幅关系、布儒斯特例子及波导例子经计算核对一致。TE 横向电场 $-i\omega\mu_0\hat z\times\nabla_\perp H_z/k_\perp^2$ 的号与 $e^{ik_zz-i\omega t}$ 相符。
- 作业1恢复草图要求并给正确无量纲曲线；作业5的 $d_{\ell m}$、相位及归一化补齐；介质插板近似及有限厚度补充已标为附加模型；作业9(e)写出测试函数乘积分布的附加项和抵消；Quiz2官方 Eq.(3.6) 系数勘误已明示；脉动球新增亚光速条件并注明不是原题要求。

这些是逐条回看修订位置的结论，未把01–16所有旧式重新从头计算。前轮 Final2、Final4、Final5 的关键解法未变，有限距离三阶场仍完整保留。

## 新增第17章独立复算

### TEM 与负载能量

取非磁介质 $\varepsilon=\varepsilon_0\varepsilon_r$，TEM 场满足 $E_r=A/r$、$B_\phi=(k/\omega)E_r=\sqrt{\varepsilon_r}E_r/c$。磁场环流给
$$I=\frac{2\pi rB_\phi}{\mu_0}=\frac{2\pi A}{Z},\quad Z=\frac{Z_0}{\sqrt{\varepsilon_r}},\quad
Z_c=\frac{Z\ln(b/a)}{2\pi}.$$
与稿件及第11章 $\sqrt{L'/C'}$ 一致。对负 $z$ 方向反射波，$B_\phi$ 的反号正确，负载条件给 $\eta=(R_L-Z_c)/(R_L+Z_c)$。

独立积分平均能流，得到 $P_i=\pi|A|^2\ln(b/a)/Z=|V_i|^2/(2Z_c)$，反射输出功率大小 $P_r=\eta^2P_i$。平均焦耳功率 $|V_i|^2(1+\eta)^2/(2R_L)$ 与净输入 $(1-\eta^2)P_i$ 相等。复峰值振幅的 $1/2$ 正确，开路、短路是极限处理，避免把短路的 $0/0$ 直接代入焦耳式。官方四页手写解答中的高斯制 $c\mathbf E\times\mathbf B/(4\pi)$ 和 $4\pi I/c$ 均已在中文按 SI 改写。

原题确有半径称谓互换，中文解释按 $a<b$ 及间隙 $a<r<b$ 与官方推导一致。全部(a)–(c)保留。

### 等离子体

从 $\varepsilon_r=1-\omega_p^2/\omega^2$ 得 $c^2k^2=\omega^2-\omega_p^2$，$v_g=c^2k/\omega$。SI 的 $\omega_p^2=ne^2/(\varepsilon_0m)$ 正确，不能保留高斯制 $4\pi ne^2/m$。

正频率传播支的 $n_\omega>0$、$E_r/E_0=(1-n_\omega)/(1+n_\omega)$、$E_t/E_0=2/(1+n_\omega)$ 与连续电场/磁场的联立一致。$\omega<\omega_p$ 取 $n_\omega=i\kappa$，因约定 $e^{ikz-i\omega t}$，选 $\operatorname{Im}k>0$ 才衰减；中文分支正确。电场和磁场振幅在倏逝区相差 $\pi/2$，故平均法向能流零，与 $|r|=1$ 一致。“没有传播体波”和“内部非零倏逝场”正确区分；结论明确只对无碰撞局域横向模态，未推广到纵向等离子体振荡。

### 圆偏振电子散射

按中文明确的 $q=-e$、$\mathbf B_0=B_0\hat z$、$\mathbf E=E_0(\cos\omega t\hat x+s\sin\omega t\hat y)$ 独立计算
$$\dot{\mathbf r}\times\mathbf B_0=s\omega B_0\mathbf r_\perp.$$
所以 $-m\omega^2A=-eE_0-se\omega B_0A$，即
$$A=\frac{eE_0}{m\omega(\omega-s\omega_c)},\qquad \omega_c=eB_0/m.$$
符号正确，$s=+1$ 与电子自由回旋一致，共振在 $\omega=\omega_c$；$s=-1$ 分母是 $\omega+\omega_c$。本稿未用含糊的观察者“左右旋”标签替代实际 $s$ 约定。无阻尼共振处没有有界周期稳态，已正确说明。

圆周特解 $|\ddot{\mathbf r}|^2=\omega^4A^2$ 是常数；拉莫尔平均功率 $e^2|\ddot{\mathbf r}|^2/(6\pi\varepsilon_0c^3)$ 无额外 $1/2$。同样圆偏振实场的模长是 $E_0$，平均入射能流为 $\varepsilon_0cE_0^2$，不是线偏振峰值振幅式的一半。相除得
$$\sigma_s=\frac{e^4}{6\pi\varepsilon_0^2m^2c^4}\frac{\omega^2}{(\omega-s\omega_c)^2}
=\frac{8\pi}{3}r_e^2\frac{\omega^2}{(\omega-s\omega_c)^2}.$$
与稿件一致，$B_0\to0$ 得 Thomson 截面，量纲为面积且 $E_0^2$ 消掉。官方末页高斯制系数 $8\pi e^4/(3m^2c^4)$ 中高斯 $e^2$ 换成 SI $e^2/(4\pi\varepsilon_0)$ 正是上述系数；没有漏 $4\pi$ 或多乘2。

只求受迫特解而非任意初值电子的全部辐射是必要限定，中文已说明自由回旋和位置常量可叠加；散射截面指与驱动相关的特解辐射。弱场及非相对论范围也已明确，共振附近仍需阻尼和自洽检查，未把模型发散冒充有限物理截面。

## 新发现的两处小修订

1. `04-multipoles.tex`，“形如 $r^2H_{\ell-2}$ 的迹部分维数 $\binom\ell2$”。该维数减法结果 $2\ell+1$ 正确，但 $H$ 前文用于调和齐次多项式，若此处也理解为调和 $H_{\ell-2}$，其维数仅 $2\ell-3$，并非 $\binom\ell2$（$\ell\ge4$ 明显不等）。建议改“$\mathcal P_\ell=\mathcal H_\ell\oplus r^2\mathcal P_{\ell-2}$，其中 $\mathcal P_j$ 为任意 $j$ 阶齐次多项式、$\mathcal H_j$ 为调和者；$r^2\mathcal P_{\ell-2}$ 维数为 $\binom\ell2$”。不改STF结论，修清空间记号即可。

2. `17-advanced-assessments.tex` 的后续资料表把解答写 `solutions1.pdf` 至 `solutions12.pdf`。实际 `sources/electrodynamics/8-311-spring-2004/assignments/` 中为 **`solution1.pdf` 至 `solution12.pdf`（单数）**，已用实际目录核对。请改表中三行文件名，否则读者按定位找不到原件。这是资料定位错误，不是数学公式问题。

## 审查范围

本轮未发现第17章三个主解需要改符号或系数；旧报告的主要修订已落实，以上两点应再修清。没有直接改正文。暂未收到最终中文 PDF，故本报告只涉及数学、教学条件、原件对照与实际文件定位；不宣称排版视觉通过。没有做形式化证明或对全稿每步重新独立求解，不作100%数学保证。最终 PDF 实际视觉检查需另记所看的页面及结果。

## 追加复核

已在修订后的实际正文中复核上述两点：第4章改为 $r^2P_{\ell-2}$ 并明确 $P$ 为任意齐次多项式；第17章表中的三组文件名均改为单数 `solution*.pdf`。两项已关闭。本报告的数学审查结论不受影响。最终 PDF 视觉审查仍待实际编译产物，另以 SHA256 绑定报告。
