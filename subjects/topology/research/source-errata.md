# 原讲义数学勘误与译编修订依据

这些是对实际下载原件与官方 TeX 的核查记录。原件保持原样；中文译编应修复下列问题并补全证明。编号、页码属于来源，不能直接称为新稿中的编号。

| 来源定位 | 原文问题 | 正确处理 |
|---|---|---|
| L1 p3 Remark 6 | ℓp 度量显示式漏掉求和符号；未在该式注明 p 范围 | 使用 (Σ|x_i−y_i|^p)^(1/p)，1≤p<∞；p=∞ 单列 |
| L1 p6 Example 18 | unit ball 与 sphere 混用 | 使用单位球面 S²，并区分弦长距离与沿球面最短弧长 |
| L2 p3 Proposition 11 | 子序列证明混用 n、n_k 的下界 | 直接用 n_k≥k 和原序列的收敛定义 |
| L2 p5 Example 20 | “Suppose that y≠0” 与论证无关 | 对任意 y∈B(x,ε) 取 r=ε−d(x,y)>0 |
| L2 p6 Theorem 27 | “all but finitely many terms ... are not in the neighborhood” | 删除 not：除有限多项外都在任意给定邻域中 |
| L2 p7 Theorem 29 | 非连续性的量词原文写成“Let ε>0” | 应存在 ε₀>0，使每个 δ>0 均有违例；取 δ=1/n |
| L2 p7 Lemma 30 | 条件漏写 d_X(x,c)<δ；后文 V/W 混用 | 完整写出 ε–δ 条件并统一邻域字母 |
| L3 p3 Question 6 | “continuous on bounded intervals are bounded” 漏闭/紧条件 | 连续函数在紧区间 [a,b] 有界；开有界区间上不必有界 |
| L3 p3 Definition 7 周边 | 容易误读为只有紧支撑才可积 | 紧支撑连续是充分条件，非必要；例如 exp(−x²) |
| L3 p4 Recall 9 | 对空有限集取点、取最大最小值 | 极值命题要求非空有限集；空集紧致单独说明 |
| L3 p4 Definition 10 | 开覆盖定义写 A=∪U_i | 一般定义为 A⊂∪U_i；不要求覆盖集合的并恰好等于 A |
| L3 p5 Example 16 | 先写 0≤c<1 又要证明 c=1；上确界证明省略桥接与端点 | 先有 0≤c≤1；利用 c 的邻域和稍小的已覆盖点接上区间；c=1 后再用端点邻域得到 [0,1] 的有限覆盖 |
| L3 p7 Theorem 25 | 闭性证明省略从序列紧致取得子序列 | 先取在 K 内收敛子序列，由原序列同极限与唯一性推出 x∈K |
| L4 p1 Lemma 1 | 否定命题写“for some r” | 应为每个 r>0 都存在坏球；取 r=1/n，严格追踪 n_k |
| L4 p3 Theorem 7 | 写 {U_i}={f(V_i)}，一般不成立 | 只用 K⊂∪f⁻¹(U_i) 推出 f(K)⊂∪U_i |
| L4 p3 Theorem 10 | 后续再次提取子序列，却直接认同同一个极限 a | 固定第一条收敛子序列；其尾项在每个 K_j 内，闭性保证同一 a∈K_j |
| L4 p4 Theorem 12，(2)⇒(3) | 仅对 x_N 估计 | 对所有 n≥N，与同一充分靠后的子序列项比较 |
| L4 p4 Theorem 12，(3)⇒(2) | zk 的指标未确保递增；同球两点距离误写<1/N | 嵌套无限指标集且每步取递增 n_k；半径 1/N 给距离<2/N，或选半径 2^−N |
| L5 p1 Definition 1 周边 | Lipschitz 常数任取实数；连续性证明 δ=Kε | 取 K≥0；K>0 时 δ=ε/K；K=0 则常值 |
| L5 p3 Theorem 8 | 证明固定点的等式起点误写 x=f(lim x_n) | 连续性给 f(x)=lim f(x_n)=lim x_{n+1}=x；保留几何级数误差界 |
| L5 p4 Example 11 | Tf(x) 定义与估计的积分变量错误：k(x,y)f(x)dx | 统一 Tf(x)=g(x)+λ∫_a^b k(x,y)f(y)dy |
| L5 p4 Example 11 周边 | 连续核与 C¹ 的 g 被直接说成推出 C¹ 解 | 连续核只保证连续解；要微分须补核对 x 的相应正则性。Picard ODE 使用另外明确的连续/Lipschitz 假设 |
| L5 p5 Theorem 17 | “unique metric space” 未说明等距同构；证明只给存在 | 唯一是固定原空间嵌入的等距同构意义；补稠密嵌入和唯一等距延拓证明 |
| L5 p5 Lemma 18 周边 | “extreme value exists by boundedness” | 有界只保证有限上确界，不保证达到最大值；C_b(M) 的证明不依赖极值达到 |
| L5 p6 完备化证明 | 映射称为 bijective，目标实际为 C_b(M) | m↦g_m 仅对像为双射；需证明有界性、连续性、距离恰好相等，再对像取闭包；空空间单列 |
| L6 p3 | “most research has ended for topological spaces” 不成立 | 不照译这个判断；只说本课程选择度量空间作为工具与后续课程的联系 |
| L6 p4 Definition 15 | 将 functional 一律定义为有界线性映射，术语范围过窄 | 明确定义“有界线性泛函”；一般泛函不必线性或有界 |
| L6 pp4–5 Dirichlet 动机 | 任意 Ω 与边界数据就宣称经典 C² 解存在 | 作为动机，明确存在性需要域、边界数据与解的正则性假设；不凭概述承诺任意边界问题 |
| PSET1 p1 Q5 | 积分算子写 I_t: C→C¹，却把 t 固定，返回的是数 | 定义 (If)(t)=∫_a^t f(x)dx 为随 t 变化的函数 |
| PSET1 p2 Q6(b) | Minkowski 显示式多出 Σ|a+b|^p≤(Σ|a+b|^p)^(1/p)，一般错误 | 删除这一不等式，保留正确的 Minkowski 形式 |
| PSET2 p1 Q1.2 hint | |d(a,b)+d(a′,b′)|≤d(a,a′)+d(b,b′) | 左侧应为差的绝对值 |
| PSET3 p2 Q7 | |a_k|<k^−3 所定义的集合不闭，却要求证明紧 | 严格不等式集合非紧；改编题应使用≤，并记录修订；原题保留反例说明 |
| PSET3 p2 Q8 | Fourier 系数严格上界 <(1+|n|)^−2 的集合非闭 | 紧性改编用≤；用常数系数趋近边界即可反证原严格版本 |

## 与补充内容相关的提醒

- 18.102 Lecture 3 Theorem 34 的成书表述应加“非空”或采用“可数稠密开集之交稠密”的形式，避免空空间的边界问题。
- 18.102 Lecture 3 Theorem 36 的原证明在闭单位球中应用 Baire 后把相对开球当作全空间开球；若本册介绍一致有界原理，建议对全 Banach 空间定义 C_k={x:sup_n||T_nx||≤k}，重新证明，不复制原细节。
- 两个度量产生同样拓扑不意味着同样 Cauchy/完备/一致连续结构；d=|x−y| 与 ρ=|arctan x−arctan y| 是标准反例。补充正文不能将“等价度量”的两种含义混淆。
