# ch13–15 作者复核记录

范围：Hong Liu, MIT OCW 8.324 Relativistic Quantum Field Theory II, Fall 2010, Lectures 1–11。原件页码以下均指讲义印刷内容页，不含末尾MIT许可页。已逐份完整阅读本地提取文本；不把网页元数据或搜索摘要当正文。三章是据原理连续中文重编，公式从统一约定重推，不逐句翻译。官方入口：https://ocw.mit.edu/courses/8-324-relativistic-quantum-field-theory-ii-fall-2010/pages/lecture-notes/ 。

## 实际来源与覆盖

| Lecture | 实读文本 | 定位 | 本稿 |
|---|---|---|---|
| 1 | `sources/8324-2010/55d5413e73d973bc458b8e1313124c38_MIT8_324F10_Lecture1.txt` | pp.1–4；§1.1、§1.1.2 | ch13 |
| 2 | `sources/8324-2010/b29379aced2b46bbe9f2715922d72b10_MIT8_324F10_Lecture2.txt` | pp.1–3；Lie groups/algebras facts、§1.2 | ch13 |
| 3 | `sources/8324-2010/fa941a1dfc792c352ff23669a23f02de_MIT8_324F10_Lecture3.txt` | pp.1–4；comments、§1.3、§1.3.2 | ch13 |
| 4 | `sources/8324-2010/037bee6805af5c342ec137afeb631a9c_MIT8_324F10_Lecture4.txt` | pp.1–3；§1.3.3、§1.3.4 | ch13 |
| 5 | `sources/8324-2010/1b3e727b1edcd9b2f41182a3d8438701_MIT8_324F10_Lecture5.txt` | pp.1–4；§1.4.1–1.4.2全部例子 | ch14 |
| 6 | `sources/8324-2010/573db088e154cfa40d05a4b471461a28_MIT8_324F10_Lecture6.txt` | pp.1–4；§1.5.1–1.5.2及QED例 | ch14 |
| 7 | `sources/8324-2010/5b5cf13e21682d4ee52df89ddbe87d1a_MIT8_324F10_Lecture7.txt` | pp.1–3；§2.1全部 | ch15 |
| 8 | `sources/8324-2010/a6474b32e25c000dec30c9a737ef0e05_MIT8_324F10_Lecture8.txt` | pp.1–5；sum rule、§2.2全部 | ch15 |
| 9 | `sources/8324-2010/9931a2068899fda568129c581ff11674_MIT8_324F10_Lecture9.txt` | pp.1–4；§2.3全部 | ch15 |
| 10 | `sources/8324-2010/d32c13f5e734728beaec81b7a4e363d9_MIT8_324F10_Lecture10.txt` | pp.1–4；§2.4全部 | ch15 |
| 11 | `sources/8324-2010/9b9756b6f73bfd0c558e4ea9a933650d_MIT8_324F10_Lecture11.txt` | pp.1–4；§2.5、§2.5.2、§2.6 | ch15 |

ch13覆盖Lie群与代数、Jacobi、理想/单代数、SU(2)/SO(3)与全局群结构、生成荷、一般/伴随表示、局域规范原理、平行移动、Yang–Mills场强/作用量/Wilson环、场方程与两种守恒。三点四点顶点是对原讲经典作用量的详细教学补充。ch14覆盖零模、轨道、FP全部步骤、轴向与Lorenz规范、ghost、辅助场、BRST幂零性、恰作用量、荷、物理上同调与QED横向态。经典Gauss计数、自由双子收缩论证和Gribov边界是明确范围的补充。ch15覆盖全部谱论、一圈d=3例、d=6紫外反项、共振、第二页、宽度/时间膨胀、外腿与通道极点、LSZ以及Lecture11末尾光学定理。四维宽度与六维宽度并列，不把维数不同的阈值幂混用。

## 约定与关键复算

- 时空metric(+---)，hbar=c=1。原讲metric相反，全部传播子与质量壳改写为s=p²、s=m²。
- ch13–14严格D=∂−igA，厄米生成元[Ta,Tb]=ifabcTc，F=∂A−∂A−ig[A,A]，分量为+gfAA。有限变换、无穷小变换、伴随导数、Wilson路径方程一起核对。Dirac源由J=−δLmatter/δA定义，故本约定J=−g barΨγTΨ；没有把另一耦合符号约定的J直接抄入。
- 三点顶点写出6个外腿分配；四点顶点先给24置换原式再给分组式。另以SU(2)eps结构常数和两个Lorentz分量枚举1296组四点颜色/度规组合，置换式与分组式零差异。这是符号样例检查，不替代一般推导。
- BRST采用sbarc=b、sb=0和规范费米子barc(f+ξb/2)，对应Lgh=−barcMc。已逐行用分次乘法核对s²A、s²c和s²Ψ，消去b之后只在壳幂零的边界已写明。
- ch15定义1PI插入iΣ，因此Dyson分母为s−m0²+Σ，Z⁻¹=1+Σ′。正谱rho=−Im(G/i)/π，正宽度ImΣ=MΓ。
- d=3积分显式算出ln3，导数积分精确为4/3−ln3≈0.23472；无UV发散仍有质量和留数变化。
- d=6极点为−α(m²−s/6)/ε；在同一正则化下两次在壳减除后取极限，有限式的质量及导数条件逐项核对。
- 宽度从四维两体相空间与log虚部各算一次；六维β³公式也按相空间面积核对。
- LSZ先实际计算三个时间区间，分别跟踪±能量壳的i、2E和sqrtZ，再给波包边界算符与多外腿约化。完整外腿截去后乘sqrtZ的图规则与LSZ中的除sqrtZ相容。树级phi4例核对M=−λ。
- 光学定理off-diagonal右侧保留两个不同振幅乘积；只在forward情形写绝对值平方。

## 来源文本中容易误读之处

- Lecture1把U(n)写成SU(n)×U(1)是局域/代数层面的常用简写。本稿群层次补明确Zn商；代数表示可积分到单连通覆盖群，不能无条件下沉到任意同代数群。
- Lecture7–9提取文本中phi_phys与Z、立方项次数等有数学字形/OCR歧义。本稿从<0|phi|p>=sqrtZ明确推出phi_phys=phi/sqrtZ，未据含糊提取字形宣称原PDF必然排印错误。
- Lecture7连续谱阈值4m²按允许两粒子通道解释，本稿补量子数限制和其他阈值可能。
- Lecture10混合场拉氏量/顶点的提取符号有歧义；本稿明定−gPhi chi²/2，再从同一模型核对Phi→2chi。
- Lecture11 off-diagonal光学定理的提取式有不一致，本稿直接由T†T矩阵元推导乘积式，而不推广forward平方式。

## 未在本稿证明的工具输入及物理边界

1. 紧致群Haar测度的存在、单李代数分类和Lie代数表示积分到单连通覆盖群；说明实际用途，核心局域代数/规范推导均本地完成。
2. 连续谱与积分按分布处理，UV需减除时保留接触多项式；不构造一般相互作用QFT的存在性。
3. 无异常BRST正则化与量子Noether荷的存在；经典nilpotency不冒充无异常量子理论的证明。四重态收缩论证限定为自由微扰渐近空间，非微扰禁闭/全局物理空间未证明。
4. FP局域截面及可逆Jacobian，明确Gribov副本/零模使全局公式失效。
5. Haag–Ruelle稳定孤立质量壳的渐近散射态存在作为工具输入；不证明渐近完备，不把绝热开关宣称为所有QFT存在的酉映射。massless红外/charged infraparticle/unstable外腿明确不直接适用。
6. 纯实phi3模型仅作形式微扰例，未主张势能有全局稳定真空。

## 文件指纹

- `chapters/ch13.tex`：`07d266ea3f70c683ce8a51b925b943a5cfcaf50aec011f1c4e2b03f2f1d9cee2`
- `chapters/ch14.tex`：`6f5b204987829351153dd930efebd41b8f5e7d47174ab83f8478f0ae6444dcd8`
- `chapters/ch15.tex`：`0bdaab4c9555c3742167f5054978d098e4d21e2ccd76b8bd53d6c533d55f045d`

## 构建证据状态

首次使用系统xelatex的三章子集在/tmp/qft-gauge-lsz-check运行，因ctex.sty不在默认搜索路径而未生成PDF。root随后提供已存在的/workspace/.local/texmf字体/宏包路径，正在用TEXINPUTS与OPENTYPEFONTS重试。正式整书编译及页级视觉审查由root统筹；本记录未把尝试失败或仅有源码当作视觉通过。

## root 委派的后续小修（原作者复核后发生）

原作者代理 stream 断连后，root 于2026-10-12明确委派独立审校代理 qft_dirac_qed 完成三处小修：ch13 回指第十章 D+ 约定，明确同一 Abelian 连接 g=−e；ch15 回指第十二章 −iΣ 约定，明确本章 iΣ 的同名自能为其负值；ch15 optical theorem相空间分母逗号修为细空白。原作者上列指纹保留其实际复核时的历史快照，不声称原作者重新看过这些修订。修订后内容复读及最终sha详见 qa/independent-gauge-lsz.md，当前指纹如下：

- `chapters/ch13.tex`：`f1502a65b35d86b493331bcb80a74a4fe7b646b66bfaf60fe7e2a7ea2683e635`
- `chapters/ch14.tex`：`6f5b204987829351153dd930efebd41b8f5e7d47174ab83f8478f0ae6444dcd8`
- `chapters/ch15.tex`：`f338e9e5a9968c18a3c30cfb688f701641bc431f5630c7246d8ababaccefce71`
