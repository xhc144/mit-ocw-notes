# 恢复题目的独立原件与代数预审

审查日期：2026-10-11。此报告仅核原件与独立解算，供后续成稿审查使用；未修改讲义。范围为8.05 Fall 2013 PS5 #9、PS10 #1、PS11 PRACTICE #1–4、#6。PS11正式作业部分与PRACTICE #5不在本次委托范围。

## 原件绑定与实际查看

原件均读取自 `/tmp/quantum-rights-hold`。SHA256：

| 文件 | SHA256 |
|---|---|
| f27e1a04f93fecaa9b34b70a54f6f6a4_MIT8_05F13_ps5.pdf | 882a5f19445d5bed736659d334078b456d27dad05259ed8025062ba8486823f4 |
| 37f7cca01c735980107575d9d465536b_MIT8_05F13_ps10.pdf | 56ac96b73aa66b6829a78968d46975cf053d5471c44abf7cd62920225becb808 |
| 33244de5a887410f525661ddf08e7103_MIT8_05F13_ps11.pdf | f882417dd54ace5fc2cc253396dc1168d1c2393bca9a6b16fe6fc695334dbb15 |

实际将PS5物理第4页、PS10物理第2页、PS11物理第6、7页渲染为单页PNG，逐张调用view_image并看到原图；没有仅依赖OCR。PS11其余相关小问读取PDF提取正文。PS10的绝对值竖线在文本提取中丢失，页图清晰可见，见下。

## PS5 #9：共同酉基

实际页图确认矩阵为

\[
A_1=\begin{pmatrix}1&1&0&-1\\1&1&-1&0\\0&-1&1&1\\-1&0&1&1\end{pmatrix},\qquad
A_2=\begin{pmatrix}1&1/2&-1&1/2\\1/2&1&1/2&-1\\-1&1/2&1&1/2\\1/2&-1&1/2&1\end{pmatrix}.
\]

直接乘法给出[A1,A2]=0。取以下列向量为共同正交基：

\[
v_1=\tfrac12(1,1,1,1)^T,\quad
v_2=\tfrac12(1,-1,1,-1)^T,\quad
v_3=\tfrac12(1,1,-1,-1)^T,\quad
v_4=\tfrac12(1,-1,-1,1)^T.
\]

逐列乘法得到本征值对分别为(1,1)、(1,−1)、(3,2)、(−1,2)。因此

\[
U=\tfrac12\begin{pmatrix}1&1&1&1\\1&-1&1&-1\\1&1&-1&-1\\1&-1&-1&1\end{pmatrix},\quad
U^\dagger U=I,
\]
\[
U^\dagger A_1U=\operatorname{diag}(1,1,3,-1),\qquad
U^\dagger A_2U=\operatorname{diag}(1,-1,2,2).
\]

SymPy用精确有理数独立复算了对易子与全部向量乘积。教学上必须说明：A1的λ=1空间二维，需要在该空间继续对角化A2；任取A1的一组本征基不能保证同时对角。列相位与列排列可变，但两个对角阵必须跟随同一排列。

## PS10 #1：原件Bell符号、角度与最小更正

原件实际印刷的是

\[
|C(\mathbf a,\mathbf b)-C(\mathbf a,\mathbf c)|-C(\mathbf b,\mathbf c)\le1.
\]

**不可删绝对值，也不需要更改减号或给定角序。** 原件给θab=θbc=θ、θac=2θ，完全可以产生违反。

用局域预定结果s_n=2S_n^(1)/ħ∈{±1}，并用单态完全反关联s_n^(2)=−s_n，则C(a,b)=⟨−s_a s_b⟩。逐次结果

\[
g=-s_a s_b(1-s_b s_c)=-s_a s_b+s_a s_c,
\quad |g|=1-s_b s_c.
\]

于是⟨g⟩=Cab−Cac，⟨|g|⟩=1+Cbc，再由|⟨g⟩|≤⟨|g|⟩得到原式。预定结果和对不同方向同时赋值是此经典推导的关键假设。

量子单态满足⟨σi⊗σj⟩=−δij，故C(a,b)=−a·b=−cosθab。在0≤θ≤π/2令x=cosθ∈[0,1]，有cos2θ−cosθ=2x²−x−1≤0，Bell左侧成为

\[
|\cos2\theta-\cos\theta|+\cos\theta
=1+2x-2x^2.
\]

因此严格违反发生在 **0<θ<π/2**；θ=0及π/2恰为等号。θ=π/3时最大值3/2。原件末句“violated for θ≤π/2”若包含端点是不精确的；最小更正为“在0<θ<π/2严格违反，两端饱和”。若中文稿误以为给定角度不能违反，原因应首先检查是否在OCR转写时漏掉了绝对值。

## PS11 PRACTICE #1：从正则对易推导守恒

在r>0的共同光滑测试函数域上推算；f为实的径向光滑函数。所有下式均是算符有序恒等式，不能把p当普通向量。令q=ħ/i=−iħ，h=f′/r，L=r×p，T=p×L−L×p。由[r_i,p_j]=iħδij得[p_i,F(r)]=q∂iF，[L_i,f]=0。

### (a) 第一长恒等式

令F_i=fr_i，则∂jF_i=fδij+hr_i r_j，因此

\[
[p^2,F_i]=q\sum_j(p_j\partial_jF_i+\partial_jF_i p_j)
=q\{p_i f+fp_i+(\mathbf p\cdot\mathbf r)r_i h+hr_i(\mathbf r\cdot\mathbf p)\}.
\]

这正是原件第一长式，包括第一项h在最右的次序。括号前两动量项互为伴随，后两项也互为伴随；括号厄米而q纯虚，所以整个对易子反厄米，与两个厄米算符的对易相容。

### (b) 第二长恒等式

用[L_i,f]=0逐项展开叉积：

\[
[T_i,f]=q h\{(\mathbf r\times\mathbf L)_i-(\mathbf L\times\mathbf r)_i\}.
\]

进一步从ε缩并和[L_i,r_j]=iħεijk r_k得

\[
\mathbf r\times\mathbf L=\mathbf r(\mathbf r\cdot\mathbf p)-r^2\mathbf p,
\quad \mathbf L\times\mathbf r=-\mathbf r\times\mathbf L+2i\hbar\mathbf r.
\]

故K=r×L−L×r=2r(r·p)−2r²p−2iħr，也可写为显式成对伴随的形式

\[
K=\mathbf r(\mathbf r\cdot\mathbf p)+(\mathbf p\cdot\mathbf r)\mathbf r-r^2\mathbf p-\mathbf p r^2.
\]

K与径向h对易（r及L都与h对易），所以hK厄米。最终[T,f]=q hK。这不是只引用Runge–Lenz守恒结论。

### (c) 相消、唯一性与符号

[p²,T]=0。把(a)中括号记作B，设g=f+rf′，注意[p·r,h]=q rh′，得到

\[
B-hK=2g\mathbf p+q(f''+2f'/r)\mathbf r
=g\mathbf p+\mathbf p g=\{g,\mathbf p\}.
\]

原题Hf=p²/(2m)−f，Rf=T/(2m)−fr，故

\[
[H_f,\mathbf R_f]
=\frac{[T,f]-[p^2,f\mathbf r]}{2m}
=\frac{i\hbar}{2m}\{f+rf',\mathbf p\}.
\]

g=0即守恒；反之要求算符恒等为零，其一阶微分系数为2g，必须g=0。于是(rf)′=0，f=c/r（含c=0）。若写[Rf,Hf]，整体符号反转。这个推导在r>0成立；不应随意声称对奇点处任意算符域已完成自伴性证明。

## PS11 PRACTICE #2：长度平方的完整正则核推

本题R是**无量纲**向量，不是#1的有量纲R。记n=r/r、C=p×L、D=L×p。从[L_i,p_j]=iħεijk p_k逐项交换得D=−C+2iħp，因此

\[
R=(C-i\hbar p)/(me^2)-n=(-D+i\hbar p)/(me^2)-n.
\]

原件三项中间恒等式分别核算如下。

1. D·r=∑εijk L_j p_k r_i。交换p_k r_i引出的δki与ε缩并为零，余项∑L_j εijk r_i p_k=−∑L_j²=−L²。
2. p·n−n·p=∑[p_i,n_i]=−iħ div(r/r)=−2iħ/r。因此iħ(p·n−n·p)=2ħ²/r，**正号**。
3. 直接用εijk εiab=δjaδkb−δjbδka：

\[
D\cdot C=\sum_{jk}L_jp_kp_jL_k-\sum_{jk}L_jp_k^2L_j
=(L\cdot p)(p\cdot L)-p^2L^2=-p^2L^2.
\]

其中L·p=p·L=0由ε对称反对称缩并得到，且[p²,L_j]=0。再同样缩并得D·p=0、p·C=0。因此

\[
(-D+i\hbar p)\cdot(C-i\hbar p)
=-D\cdot C+i\hbar D\cdot p+i\hbar p\cdot C+\hbar^2p^2
=p^2(L^2+\hbar^2).
\]

交叉项需要保留n的顺序。D·n=−L²/r（p作用1/r产生的εijk r_i r_k项为零），n·C=L²/r，故

\[
(-D+i\hbar p)\cdot n+n\cdot(C-i\hbar p)
=2(L^2+\hbar^2)/r.
\]

最后n²=1，得到

\[
R^2=1+\left(\frac{p^2}{m^2e^4}-\frac{2}{me^2r}\right)(L^2+\hbar^2)
=1+\frac{2H}{me^4}(L^2+\hbar^2).
\]

ħ²量子修正源于有序乘积与div n，不能用经典向量乘法跳过。e²沿用原件库仑常数记法；若SI化须同时替换成e²/(4πε0)，不能只改部分式子。

## PS11 PRACTICE #3：1⊗1/2的全部六态及观测量

以下|m_l,±⟩中±表示m_s=±1/2。取通常使j=1/2最高态最大m_l项为正的整体相位；另一套整条multiplet同时乘−1等价。

\[
|3/2,3/2\rangle=|1,+\rangle,
\quad |3/2,1/2\rangle=\sqrt{2/3}|0,+\rangle+\sqrt{1/3}|1,-\rangle,
\]
\[
|3/2,-1/2\rangle=\sqrt{1/3}|-1,+\rangle+\sqrt{2/3}|0,-\rangle,
\quad |3/2,-3/2\rangle=|-1,-\rangle,
\]
\[
|1/2,1/2\rangle=\sqrt{2/3}|1,-\rangle-\sqrt{1/3}|0,+\rangle,
\quad |1/2,-1/2\rangle=\sqrt{1/3}|0,-\rangle-\sqrt{2/3}|-1,+\rangle.
\]

从最高态每次用J−=L−+S−并除ħ√((j+m)(j−m+1))，得到第一组；在M=1/2二维空间取其正交向量得到第二组，再降一次。维数4+2=6，故(e)没有更低j要继续。原题(f)提到卷末CG表，但此实际PDF正文后只有OCW条款页；不要伪称已比对不存在的卷末表。上述相位约定已显式声明。

(g)在|1/2,1/2⟩，⟨Lz⟩=2ħ/3，⟨Sz⟩=−ħ/6。(h)原件电子HB=μB B(Lz+2Sz)/ħ，故全六态统一为⟨HB⟩=μB B g_j m，g3/2=4/3、g1/2=2/3。(i)该态能量测量有0（来自|1,−⟩，概率2/3）与μB B（来自|0,+⟩，概率1/3），均值μB B/3。这里问期望或测量分布，不能把所有耦合态都叫有限磁场HB精确本征态。

## PS11 PRACTICE #4：一般j最高两multiplets

记|m1,m2⟩为两粒子的j各自固定的未耦合态。J=2j的最高两态为

\[
|2j,2j\rangle=|j,j\rangle,\qquad
|2j,2j-1\rangle=(|j,j-1\rangle+|j-1,j\rangle)/\sqrt2.
\]

J=2j−1的最高态由正交得到

\[
|2j-1,2j-1\rangle=(|j,j-1\rangle-|j-1,j\rangle)/\sqrt2.
\]

降一次时|j−1,j−1⟩的两项正好相消，剩下√(2(2j−1))系数；除去总降算符系数后

\[
|2j-1,2j-2\rangle=(|j,j-2\rangle-|j-2,j\rangle)/\sqrt2\quad(j\ge1).
\]

最大multiplet对称，次大反对称；交换算符与J−对易，所以各自整条multiplet同一交换性。(b)边界必须交代：j=1/2时次大J=0仅一态，没有“第二最高态”；j=0时没有次大multiplet。

## PS11 PRACTICE #6：三spin-1全部能级、简并与基态

粒子可区分，空间维数3³=27。原题三条边均出现，H=Δ(S1·S2+S2·S3+S3·S1)/ħ²=Δ(S²/ħ²−6)/2，Δ>0。先1⊗1=0⊕1⊕2，再分别与1合成，得到0⊕3(1)⊕2(2)⊕3。

| 总S | multiplicity | E | 能级总简并 |
|---|---:|---|---:|
| 0 | 1 | −3Δ | 1 |
| 1 | 3 | −2Δ | 9 |
| 2 | 2 | 0 | 10 |
| 3 | 1 | 3Δ | 7 |

总简并1+9+10+7=27。不能把2S+1当作这里的全部简并。

为明确完成(c)的七系数要求，写M=0候选为a|+0−⟩+b|+−0⟩+c|0+−⟩+d|0−+⟩+e|−+0⟩+f|−0+⟩+g|000⟩。S+杀死基态给六个独立输出态的系数方程：

\[
a+c=0,\ b+d=0,\ e+f=0,
\quad a+b+g=0,\ c+e+g=0,\ d+f+g=0.
\]

前三式消去c,d,f，后三式给b=−a、e=a、g=0；归一化|a|=1/√6。取a正则

\[
|G\rangle=\frac{|+0-\rangle-|+-0\rangle-|0+-\rangle+|0-+\rangle+|-+0\rangle-|-0+\rangle}{\sqrt6}.
\]

M=0且S+|G⟩=0，故S²|G⟩=(S−S++Sz²+ħSz)|G⟩=0，确为唯一最低S=0态；不能只凭M=0就宣称单态。

## 后续成稿的优先检查项

1. PS10绝对值必须保留，违反区间端点须更正，原角度无需改动。
2. 两种Runge–Lenz定义不能混用；两长式中算符顺序、[H,R]符号及ħ²修正须完整保留。
3. PS5共同基的列序和两个对角阵必须一致。
4. CG给出全六态、期望与实际测量值的区分；一般j题保留j=1/2的边界。
5. 三spin-1应给27维核对及七系数消元，避免把multiplicity误当总简并。

本次没有中文新增成稿可绑定哈希；以上PDF哈希绑定了实际原件，待正文完成后另行审查。
