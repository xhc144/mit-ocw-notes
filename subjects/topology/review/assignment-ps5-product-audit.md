# 18.901 PS5 第五行专项数学审稿：任意积 \(\mathbb R^I\)

审稿日期：2026-10-08。对象：官方题表第五行，product topology，原题未限定指标集 \(I\) 大小。审稿独占此文件；不修改题解 writer 的正文。以下证明均在 ZFC 中成立，属于编者解答，不是 MIT 官方答案。

## 1. 最终判定

记 \(\mathfrak c=2^{\aleph_0}\)。包括空指标集的约定为 \(\mathbb R^\varnothing=\{*\}\)。采用教材中的 Hausdorff/T₁ 分离约定。

| 原列 | 性质 | \(\mathbb R^I\) 具有该性质的充要条件 |
|---|---|---|
| C1 | connected | 任意 \(I\) |
| C2 | path connected | 任意 \(I\) |
| C3 | compact | \(I=\varnothing\) |
| C4 | locally compact Hausdorff | \(I\) 有限 |
| C5 | Hausdorff | 任意 \(I\) |
| C6 | Regular | 任意 \(I\) |
| C7 | Normal | \(|I|\leq\aleph_0\) |
| C8 | First-countable | \(|I|\leq\aleph_0\) |
| C9 | Second-countable | \(|I|\leq\aleph_0\) |
| C10 | Lindelöf | \(|I|\leq\aleph_0\) |
| C11 | Has countable dense subset | \(|I|\leq\mathfrak c\) |
| C12 | Locally metrizable | \(|I|\leq\aleph_0\) |
| C13 | Metrizable | \(|I|\leq\aleph_0\) |
| C14 | Completely regular | 任意 \(I\) |

三个敏感判定没有独立性悬而未决：不可数积在 ZFC 中总是不正规、不 Lindelöf；可分性的界是连续统，而不是可数。尤其 \(\mathbb R^{\omega_1}\) 在 ZFC 中可分、非正规、非 Lindelöf，这三项并不矛盾。

## 2. 可直接收入附录的完整非正规证明

以下是 Stone 闭集构造的有限坐标递归写法；它不使用 Jones 引理、CH、连续统的大小比较、Urysohn 引理或“连续实值函数只依赖可数坐标”的额外定理。

令 \(N=\{0,1,2,\ldots\}\) 取离散拓扑，\(X=N^{\omega_1}\)。对有限 \(F\subseteq\omega_1\) 与 \(x\in X\)，记基本柱集

\[
[F,x]=\{y\in X:y|_F=x|_F\}.
\]

定义

\[
H_j=\{x\in X:\text{每个 }m\in N\setminus\{j\}\text{ 至多在一个坐标上出现}\},
\qquad j=0,1.
\]

若 \(x\notin H_j\)，存在两个不同坐标 \(\alpha,\beta\) 使 \(x(\alpha)=x(\beta)=m\ne j\)；固定这两个坐标的柱集包含 \(x\) 且不交 \(H_j\)，故 \(H_j\) 闭。若 \(x\in H_0\cap H_1\)，每个自然数都至多出现一次，即 \(x:\omega_1\to N\) 为单射，矛盾。因此这两个闭集不交。

任取开集 \(U\supseteq H_0\)、\(V\supseteq H_1\)。递归构造递增有限集 \(F_n\) 与彼此相容的单射

\[
q_n:F_n\longrightarrow\{2,3,\ldots\}.
\]

从 \(F_0=\varnothing\)、空映射 \(q_0\) 开始。已有 \(F_n,q_n\) 后，令 \(f_n\) 在 \(F_n\) 上等于 \(q_n\)，在其外等于 \(0\)。由于 \(f_n\in H_0\subseteq U\)，可选有限 \(F_{n+1}\supseteq F_n\) 使

\[
[F_{n+1},f_n]\subseteq U.
\]

再给 \(F_{n+1}\setminus F_n\) 的有限个新坐标分配尚未使用的、互不相同的整数 \(\geq2\)，得到扩张 \(q_{n+1}\)。这里包含于 \(U\) 的柱集固定的是 \(f_n\)，不是刚重新标号后的 \(f_{n+1}\)；不能混淆下标。

令 \(F=\bigcup_nF_n\)、\(q=\bigcup_nq_n\)，并定义

\[
g(\alpha)=
\begin{cases}
q(\alpha),&\alpha\in F,\\
1,&\alpha\notin F.
\end{cases}
\]

单射 \(q\) 的值均 \(\geq2\)，故 \(g\in H_1\subseteq V\)。取有限 \(G\) 使 \([G,g]\subseteq V\)。因为 \(G\cap F\) 有限且 \(F_n\) 递增，可选 \(n\) 使 \(G\cap F\subseteq F_n\)。于是

\[
G\cap F_{n+1}\subseteq F_n,
\qquad g|_{F_n}=f_n|_{F_n}.
\]

因此有限规定 \(h|_G=g|_G\) 与 \(h|_{F_{n+1}}=f_n|_{F_{n+1}}\) 在交集上一致，可以同时满足。任选其余坐标，即得

\[
h\in[G,g]\cap[F_{n+1},f_n]\subseteq V\cap U.
\]

任意这样的开邻域都相交，故 \(X\) 不正规。

若 \(I\) 不可数，ZFC 允许选择 \(J\subseteq I\)、\(|J|=\aleph_1\)。在其余坐标固定 \(0\)，则

\[
Y=N^J\times\{0\}^{I\setminus J}
\]

是 \(\mathbb R^I\) 的闭子空间，并同胚于 \(X\)：\(N\) 是 \(\mathbb R\) 的闭离散子空间，积中逐坐标取闭子集仍闭。正规性遗传给闭子空间，因此 \(\mathbb R^I\) 不正规。若 \(I\) 至多可数，则第 5 节的乘积度量给出可度量化，从而正规，完成充要性。

正文实际需要：两个闭集的定义及闭性/不交性、一段递归与有限坐标相容论证、闭嵌入一句。合理排版约一页；不需要为此引入集合论或函数依赖大引理。

## 3. 非 Lindelöf 的直接短证明

仍用第 2 节的闭集 \(H_0\)。每个 \(x\in H_0\) 的非零坐标集合至多可数，因为在该集合上 \(x\) 单射到 \(N\setminus\{0\}\)。因此相对开集

\[
W_\alpha=\{x\in H_0:x(\alpha)=0\},\qquad \alpha<\omega_1,
\]

覆盖 \(H_0\)。任取可数 \(J\subseteq\omega_1\)，选单射 \(r:J\to\{1,2,\ldots\}\)，在 \(J\) 上令 \(x=r\)、在其外令 \(x=0\)。这个 \(x\in H_0\)，但不属于任何 \(W_\alpha\)、\(\alpha\in J\)。故此开覆盖无可数子覆盖。

\(H_0\) 在 \(N^{\omega_1}\) 中闭，后者是上节的 \(\mathbb R^I\) 闭子空间，所以 \(H_0\) 也是 \(\mathbb R^I\) 的闭子空间。Lindelöf 性遗传给闭子空间，故不可数 \(I\) 时 \(\mathbb R^I\) 不 Lindelöf。可数 \(I\) 时，其可数基由有限坐标上的有理端点区间组成；第二可数空间 Lindelöf。因此判定完整。

这一证明本身只需一段，且能复用非正规证明中的 \(H_0\)。也可由正则 Lindelöf 空间正规反推，但上面的具体开覆盖证据更直接。

## 4. 可分性的完整短证明

### 充分性：\(|I|\leq\mathfrak c\)

选单射 \(i\mapsto t_i\) 从 \(I\) 到 \(\mathbb R\)。令

\[
D=\{(p(t_i))_{i\in I}:p\in\mathbb Q[t]\}.
\]

有理系数多项式集合可数，故 \(D\) 可数。给定任意非空基本柱集，它只要求有限个互异坐标 \(i_1,\ldots,i_k\) 的值分别落入非空开区间 \(U_1,\ldots,U_k\)。各选 \(a_j\in U_j\)。由 Lagrange 插值，存在实系数多项式

\[
P(t)=\sum_{j=1}^ka_j\prod_{\ell\ne j}\frac{t-t_{i_\ell}}{t_{i_j}-t_{i_\ell}}
\]

满足 \(P(t_{i_j})=a_j\)。有限次求值随有限个系数连续，所以把 \(P\) 的系数用有理数充分逼近后，可得 \(p\in\mathbb Q[t]\) 仍满足 \(p(t_{i_j})\in U_j\)。因此 \(D\) 遇到每个非空基本开集，是稠密集。

### 必要性：可分 \(\Rightarrow |I|\leq\mathfrak c\)

将一个可数稠密集重复枚举为 \(D=\{d_n:n\in\mathbb N\}\)。映射

\[
i\longmapsto(d_n(i))_{n\in\mathbb N}\in\mathbb R^{\mathbb N}
\]

必须单射：若 \(i\ne j\) 的两个序列相同，则所有 \(d_n\) 满足 \(d_n(i)=d_n(j)\)，即 \(D\) 落在闭的真对角线 \(\{x:x_i=x_j\}\) 中，和稠密性矛盾。又 \(|\mathbb R^{\mathbb N}|=\mathfrak c\)，故 \(|I|\leq\mathfrak c\)。最后这个基数等式可由 \(\mathfrak c=2^{\aleph_0}\) 与 \((2^{\aleph_0})^{\aleph_0}=2^{\aleph_0\cdot\aleph_0}=2^{\aleph_0}\) 得到。

这给出 \(\mathbb R^I\) 特殊情形的自足证明，不必把一般 Hewitt–Marczewski–Pondiczery 定理的名称当作所求证明。

## 5. 其余性质的短核与证明

**连通与道路连通。** 任意 \(x,y\) 可由 \(\gamma(t)_i=(1-t)x_i+ty_i\) 连接；每个坐标函数连续，故 \(\gamma:[0,1]\to\mathbb R^I\) 在积拓扑下连续。道路连通蕴含连通。

**Hausdorff、完全正则、正则。** 两个不同点在某坐标不同，用该坐标的分离区间即得 Hausdorff 性。给定闭集 \(A\) 与 \(x\notin A\)，选不交 \(A\) 的基本柱邻域，涉及有限坐标 \(F\)；在各坐标上取连续三角形帽函数 \(\varphi_i\)，满足 \(\varphi_i(x_i)=1\)，支撑包含在对应开区间中。有限乘积 \(\varphi(y)=\prod_{i\in F}\varphi_i(y_i)\) 连续，\(\varphi(x)=1\)、\(\varphi(A)=0\)，故完全正则。由 \(\{\varphi>2/3\}\) 的闭包包含于 \(\{\varphi\geq2/3\}\subseteq X\setminus A\) 也直接得正则性。

**紧性。** 非空 \(I\) 的某坐标投影把 \(\mathbb R^I\) 连续满射到非紧的 \(\mathbb R\)，故积非紧；空积是一点空间。

**局部紧性。** 有限 \(I\) 为有限维 Euclidean 空间。若 \(I\) 无限且某点有紧邻域 \(K\)，取基本柱集 \(x\in B\subseteq K\)，其有限限制集为 \(F\)。选择 \(j\in I\setminus F\)，则 \(\pi_j(B)=\mathbb R\)，所以 \(\pi_j(K)=\mathbb R\)；这与紧集的连续像紧矛盾。

**第一可数性的必要性。** 若 \(x\) 有可数邻域基 \(U_n\)，各选基本柱集 \(x\in B_n\subseteq U_n\)，令 \(F_n\) 为其有限限制集。不可数 \(I\) 中可选 \(j\notin\bigcup_nF_n\)。邻域 \(W=\{y:|y_j-x_j|<1\}\) 不包含任何 \(B_n\)，于是也不包含任何 \(U_n\)，和邻域基性质矛盾。这里要用 \(B_n\subseteq U_n\) 的方向；不能从一族任意选取的邻域直接跳到基的否定。

**第二可数。** 当 \(I\) 至多可数时，有限坐标上有理端点区间柱集组成可数基。反向用第二可数蕴含第一可数及上一段。

**可度量化与局部可度量化。** 可数无限 \(I=\{i_n:n\geq1\}\) 时

\[
d(x,y)=\sum_{n=1}^{\infty}2^{-n}\min\{1,|x_{i_n}-y_{i_n}|\}
\]

给出积拓扑：指定有限坐标约束时，足够小的 \(d\)-球同时满足这些约束；给定 \(d\)-球时，先截去充分小的尾和，再在前有限坐标上选充分小的区间，得包含于球的柱集。有限与空 \(I\) 也可度量化。不可数 \(I\) 时第一可数性已失败，所以不可度量化。若某点有可度量化开邻域，该点在该邻域中的可数邻域基也成为全空间中的可数邻域基；故不可数积甚至没有局部可度量化点。

**可数情形正规。** 度量空间中，不交闭集 \(A,B\) 可由开集 \(\{x:d(x,A)<d(x,B)\}\) 与 \(\{x:d(x,B)<d(x,A)\}\) 分离。若一集合为空显然可分离。因此上面的乘积度量足以完成正规性的正向证明。

## 6. 原拟 \(f_\alpha,g_\alpha\) 闭离散构造的核验

对每 \(\alpha<\omega_1\) 选单射 \(e_\alpha:\alpha\to N\)，定义

\[
f_\alpha(\beta)=
\begin{cases}e_\alpha(\beta)+1,&\beta<\alpha,\\0,&\beta\geq\alpha,\end{cases}
\qquad
g_\alpha(\beta)=
\begin{cases}e_\beta(\alpha)+1,&\alpha<\beta,\\0,&\alpha\geq\beta.\end{cases}
\]

正确结论是点对集合

\[
D=\{(f_\alpha,g_\alpha):\alpha<\omega_1\}
\subseteq N^{\omega_1}\times N^{\omega_1}
\]

闭离散且大小 \(\aleph_1\)。每个点对在第 \(\alpha\) 坐标两分量均为 \(0\)，其他点对不满足这一条件，故离散。若 \((x,y)\in\overline D\)，其第一分量 \(x\in H_0\)，所以有某 \(\beta\) 满足 \(x(\beta)=0\)。限制第一分量第 \(\beta\) 坐标为 \(0\) 后，只余 \(\alpha\leq\beta\)；再限制第二分量为 \(y(\beta)\)，若该值为 \(0\)，只余 \(\alpha=\beta\)，若为正值，由 \(e_\beta\) 单射，只余至多一个 \(\alpha<\beta\)。故存在一个基本邻域，其与 \(D\) 的交集至多一个点。这个邻域含有闭包点，因此不能完全不交 \(D\)；再由单点闭性，闭包点恰为这唯一点。故 \(D\) 闭。

两个单独的集合不能替代这个配对集合。

- \(\{f_\alpha\}\) 甚至不保证离散：取 \(e_n(k)=k\)、\(e_\omega(k)=k\)，则 \(f_n\to f_\omega\)。把 \(e_\omega\) 改为不同排列还会得到不属于这族的极限，故也不保证闭。
- \(\{g_\alpha\}\) 不闭：对于任意有限坐标限制，取 \(\alpha\) 大于全部这些坐标，则 \(g_\alpha\) 在它们上均为 \(0\)。所以全零函数是该族的闭包点，但不是任何 \(g_\alpha\)。

虽然配对构造完全正确，第 3 节 \(H_0\) 的开覆盖证更短，且不用第二份坐标。建议正文选后者，配对构造仅作为独立核验保留。

## 7. 来源、证据边界与集合论陷阱

**官方题面。** [MIT OCW 18.901 Fall 2004 Problem Set 5](https://ocw.mit.edu/courses/18-901-introduction-to-topology-fall-2004/d6c5d6d30bf26300b6f1b2c278791796_problemset_5.pdf)，本次原件为 `/tmp/topology-audit-ps5.pdf`。原表第五行只写 \(\mathbb R^I\) in product topology，不给 \(I\) 的基数；它是待填写的题表，不是印出的答案。

**非正规构造的原论文。** A. H. Stone, *Paracompactness and product spaces*, Bulletin of the American Mathematical Society **54** (1948), 977–982，DOI [10.1090/S0002-9904-1948-09118-2](https://doi.org/10.1090/S0002-9904-1948-09118-2)，[Project Euclid 原出版页](https://projecteuclid.org/journals/bulletin-of-the-american-mathematical-society-new-series/volume-54/issue-10/Paracompactness-and-product-spaces/bams/1183512390.full)。出版记录及 DOI 已查；本次直接获取原 PDF 遇到站点防护，因此不把它登记为全文实读。此获取限制不影响第 2 节已经逐步写出的完整证明。

**作者研究稿的实际复核。** N. Noble, *Poorly Separated Infinite Normal Products*, [arXiv:2002.02483](https://arxiv.org/pdf/2002.02483)，第 6.1 节、物理第 25–26 页实际阅读。该研究稿明确记录 Stone 使用上述两个闭集直接证明非正规；第 26 页也记录 \(H_0\) 的“坐标为零”开覆盖。这里引用它核对构造归属与结论，正文证明已完整展开，不以引用替代证明。本地临时原件 `/tmp/noble2020.pdf`。

**可分性原论文的实际复核。** Edward Marczewski, *Séparabilité et multiplication cartésienne des espaces topologiques*, Fundamenta Mathematicae **34** (1947), 127–143，DOI [10.4064/FM-34-1-127-143](https://doi.org/10.4064/FM-34-1-127-143)。[原扫描 PDF](https://matwbn.icm.edu.pl/ksiazki/fm/fm34/fm34117.pdf) 的物理第 7 页左/右栏为印刷第 138/139 页；第 3.2 节已实际渲染并视觉阅读，原定理给出可分非平凡空间之积的连续统指标界。本审稿第 4 节对 \(\mathbb R\) 因子使用有理多项式求值构造，专门写成可直接核验的短证。注意搜索偶尔返回 `fm34116.pdf`，其主要是前一篇文章，不能用错误文件当已核实全文。正确临时原件 `/tmp/marczewski1947-correct.pdf`，9 个双页扫描物理页，第一物理页包含前文最后的印刷第 126 页。

**Jones 引理不能在这里代替 Stone 证明。** 从“可分 + 有一个大小为 \(\aleph_1\) 的闭离散子空间”用 Jones 引理，正规性至多推出 \(2^{\aleph_1}\leq\mathfrak c\)。要使之成为矛盾，还需要 \(2^{\aleph_1}>\mathfrak c\)，这个严格不等式不能仅由 \(\aleph_1>\aleph_0\) 和幂集基数的单调性得到；ZFC 中不能普遍假定它。CH 下该严格不等式成立，但原题没有 CH。第 2 节证明完全绕过这个问题。

审稿结论：上述第五行 14 格及三项关键充要条件数学核验通过；完整证明没有剩余数学阻塞。此记录不自动表示其他八行已审稿，须在 writer 草稿完成后另行复核。
