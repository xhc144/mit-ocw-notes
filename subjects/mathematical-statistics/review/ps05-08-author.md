# PS5–8 作者记录

范围：`subjects/mathematical-statistics/assignments/ps05.tex`–`ps08.tex`，原题面中文翻译及 AI 独立完整解答；另有原 PS7 五幅 QQ 图的必要题面资产。官方文件只有题目，本稿不称答案为官方答案。未改原十章、main、根 README、其他学科或 Git。

## 实际读取

完整读取 `subjects/mathematical-statistics/main.tex` 的类及正文，及 `subjects/topology/vendor/math-latex-typesetting/references/{STYLE_SPEC,ENVIRONMENTS,MATH_LAYOUT,EDITORIAL_RULES}.md`、`math-lecture-writing/references/{writing-and-proof,review-gates}.md`。亦通过 skills.read 读取两项 Skill 的完整 SKILL.md。第一次错指项目根 main.tex（该文件不存在），随后实际读正确的科目 main.tex；没有以此错误读取代替正确读取。

逐字读取 `/tmp/statistics-assignment-review/ps5.txt`–`ps8.txt` 全部逐页文本，结合 `download-review.json` 取到原 PDF 文件名。实际将每份原 PDF 所有题目页按 1.3 倍渲染后逐页 view_image：PS5物理页1–2、PS6页1–3、PS7页1–5、PS8页1–3。末页来源声明另已从逐页文本读到。PS5P2.5符号另在物理页2裁为3倍图 `/tmp/ps5-p25-symbol.png` 后实际查看，确认两侧都印 H0、两侧关系都为等号。

官方来源和原始截止时间均写在各章首：PS5 2016-10-14中午12点、PS6 2016-10-21中午12点、PS7 2016-10-28中午12点、PS8 2016-11-04中午12点。每份三个主题 exercise 紧接 solution，显式原作业第1/2/3题、原编号层级与 `psNN:pMM` 标签齐备；不重定义排版、计数器、字体或语义环境。

## 逐题覆盖与源页

| 文件 | 原题 | 原编号覆盖 | 物理页 | 解答覆盖 |
|---|---|---|---|---|
| PS5 | P1 | 1–2 | 1 | 泊松学生化置信区间及覆盖证明；区间反演检验及固定备择一致性 |
| PS5 | P2 | 1–6 | 1–2 | 两组MLE；两个卡方及独立和；均值差正态；等方差合并t检验；数值/p值、两种方差分母与“不拒绝≠证实相同” |
| PS5 | P3 | 无编号子问 | 2 | 隐式边界μ=σ的Delta方差3σ²/2；严格原假设上的sup渐近水平；两组数值及5%/10%决定 |
| PS6 | P1 | 1、2、3(a,b) | 1 | 指数率参数双侧/单侧检验；整个复合原假设单调耦合；来电数值与n=49/50字面歧义 |
| PS6 | P2 | 1–3 | 1–2 | MLE；独立正态/卡方学生化；严格μ>0下有限样本sup α |
| PS6 | P3 | 1、2(a–e) | 2 | 四格独立性等价；一致估计；三维CLT；完整Delta方差；零假设因式分解；边界退化及双侧检验 |
| PS6 | P3 | 末尾无编号应用 | 2–3 | 1000人原表完整保留，p=.384,q=.506,r=.205，Z和p值、5%决定 |
| PS7 | P1 | 无编号子问，五图 | 1–2 | 原图保留；依次Cauchy、uniform、Gaussian、Exp、Laplace；每图以分位数曲线/尾部形状解释 |
| PS7 | P2 | 1、2、3(a–f) | 3 | 实验例、积分变换、有限最大值、枢轴性、可运行R模拟代码与Python实跑、精确分位数严格拒绝、有限MC加一p值 |
| PS7 | P3 | 1–5、6(a,b)、7–9 | 3–5 | 秩依赖、均匀排列、向量独立、联合分布、均值与平方和完整展开、相关系数化简、同分布、可运行R算法与实跑、原单侧局限和绝对值双侧校准 |
| PS8 | P1 | 1–5 | 1 | GLS与OLS、正态似然、满秩唯一性、正规方程/正态分布、无偏与trace风险 |
| PS8 | P2 | 1、2、3(a–f) | 1–2 | 条件密度似然和g消去、Gaussian fx、设计满秩条件、OLS/条件正态、可积性反例、方差MLE/无偏/χ²及n=p失败 |
| PS8 | P2 | 4(a–d) | 2 | 一元OLS及Sxx=0事件；LLN一致性；向量CLT与2×2逆矩阵；未知矩和方差学生化、strict b>0边界、零噪声规则 |
| PS8 | P3 | 1–3 | 2–3 | logistic概率、似然、f独立性、共同密度缺口、梯度/Hessian/Newton及分离无有限MLE反例 |

冻结计数核对：各PS主题题均3；编号叶问数8、13、18、20；包括编号母节点在内全部编号节点8、15、20、22。PS5P3及PS7P1无编号，不添伪造编号；PS6P3的末尾表格应用无编号但完整解答。

## 保留原条件并说明的缺口

- PS5P2.5原PDF两侧均H0、关系均等号；保留原印刷题面，解首明确采用H1:μ1≠μ2版本。P2.6方差分母歧义给两种数值；P3使用非退化σ²>0与n≥2，严格原假设以边界上确界控制。
- PS6P3.2(a)原qhat以Xi求平均；题面保留并给反例，然后明确更正为Yi。p、q等于0或1的退化模型只能保证“至多α”。PS6P1.3原句50次来电可能只有49个间隔，保留原来电数量并同时给n49/n50，不暗改观测数。
- PS7P3的秩要求n≥2、无并列的连续边际。第8问仍为S单侧分位数，第9问原单侧规则有level但识别不了负相关；另给|S|双侧规则，反序备择示例；再用Y=X²说明双侧Spearman也非一般独立性的全能一致检验。所有精确水平用strict >分位数，离散分布可保守；有限模拟分位数仅近似，另给加一MC p值作精确秩控制。
- PS8P2.3(b)必须n≥p，否则秩断言错误；3(e)联合MLE在n=p且RSS=0时不存在参数域内的σ²最大点；3(f)必须n>p。3(d)条件期望为β但无条件可积性不保证；给X~U[-1,1]、n=p=1、ε/X无绝对一阶矩的反例。4(a)设计全相等有限概率时估计不唯一，任意选一个最小二乘解，LLN保证该事件渐近消失；4(c/d)明示有限、正噪声方差及零方差退化规则。
- PS8P3只写独立、未写同分布，却仅给X1密度f。题面原条件保留，解中明确共同f是补充条件，或用不同fi，条件似然不受影响。逻辑回归有限MLE可能因完全分离不存在，给连续正设计/全1响应的反例，不将优化目标存在误说成极大点存在。

## QQ图资产

`assignments/assets/ps07-qqplots.pdf` 是原PS7物理页1 `Rect(87,435,612,714)` 裁切；`ps07-qqplots-2.pdf` 是物理页2 `Rect(70,108,596,676)` 裁切。用PyMuPDF `show_pdf_page(...,clip=...)` 精确复用源PDF对象，不新随机抽样改画、不把整页截图作为题面。已分别渲染并实际view_image，五图坐标刻度、原Normal Q-Q Plot标题、原QQ-Plot 1–5标签及顺序完整，没有无关题面或答案区。

原五幅图自身是512×511 JPEG嵌入，而非纯矢量：源页1 xref583/584，源页2 xref3/4/5，DCTDecode。裁切PDF保留原嵌入图与原生文字标签，不能声称这五图是纯矢量。最终rights来源核由sourceagent/root负责，不在本作者记录伪报独立来源审查通过。

## 真实运行证据

执行 `python subjects/mathematical-statistics/experiments/ps05_08_checks.py`，退出0；记录 `subjects/mathematical-statistics/experiments/ps05_08_checks-results.json`。时间和版本以JSON实际字段为准：Python3.12.14、NumPy2.3.5、SciPy1.17.0、seed65007、B50000。环境没有R，`R_executable_found=null`、`R_run=false`，未声称跑过R。正文R代码与Python实现等价，但跨语言随机数不承诺相同样本。

- PS5P2 MLE方差约定：t=1.7293840611、p=.1008518119；无偏方差约定：t=1.8229308608、p=.08496781287，df18，5%双侧临界2.1009220402。
- PS5P3：Z=.4642184229，p=.6787543683；Z=-1.4592079004，p=.07225394751。
- PS6来电n50：Z=.1414213562，p=.4437685420；n49：Z=.14，p=.4443299952。
- PS6伯努利表：V=.059127484416，Z=1.3909986007，p=.1642258511。四个可行联合分布下，a'Σa、展开式、直接离散方差最大差4.86e-17。
- PS7 KS n20,m25，50000次均匀零假设模拟q95≈.39；n3,m4穷举35排列验证strict拒绝在α=.05时概率0（离散保守）。
- PS7 Spearman n10，50000次均匀排列模拟单侧q95=.5515151515，|S|q95=.6363636364，模拟方差.1114901923对照1/9；公式与直接相关系数差2.22e-16。n5穷举120排列的|S|临界.9，strict拒绝概率1/60≤.05，分布对称、方差.25。
- PS8 GLS固定示例正规方程残差2.03e-15、协方差恒等式最大差1.11e-16；2×2渐近协方差公式最大差4.44e-16。

这些数值核验支持计算及实现，不代替概率极限、有限样本水平或一般数学证明。

## 复核与边界

PS5已由独立reviewA实际全文读取、复算，零概率MLE边界与P3非退化条件小修已实际复看。PS6/7已由独立reviewB实际全文读取及独立算法运行；PS8由其实际全文读取并针对单调耦合事件及零噪声规则返修。独立审稿的最终版本/哈希以reviewer报告为准，本记录不冒充审稿结论。

本作者负责正文及数值，不声称已完成最终整书编译、逐页最终PDF视觉审查或发布。root负责将四份输入单本固定版式main.pdf、构建及最终视觉检查。


路径修正：作者原先把本脚本、结果JSON及本报告误存项目根目录下的 experiments/review，现已只移动这三个自有文件至数理统计科目目录。脚本以自身绝对解析路径定位科目根，输出与调用 cwd 无关；再次真实运行后刷新下列快照。未改已冻结的四份作业正文。

## 作者交稿快照 SHA-256

- `subjects/mathematical-statistics/assignments/ps05.tex`: `a1458e29a8dad4321420efbd462110cf840d6fe9da24e1cc4211f4235ecb5b72`
- `subjects/mathematical-statistics/assignments/ps06.tex`: `b45aa3bfb657252f09c83fcd04045251584631938c2193c3e5850faede3b0c3d`
- `subjects/mathematical-statistics/assignments/ps07.tex`: `bc8b6e60b514136e3fbfc2f73927b629e6c113457954cc9702ca883c77b405b6`
- `subjects/mathematical-statistics/assignments/ps08.tex`: `009ed1e999ad87644015984d80c69e3eb4f42b64b31e1faa950a4cf81779d936`
- `subjects/mathematical-statistics/assignments/assets/ps07-qqplots.pdf`: `46ecdfeebad198219d562af4287564d23b8f595d0eaed3d14d73166238fc6267`
- `subjects/mathematical-statistics/assignments/assets/ps07-qqplots-2.pdf`: `faf01265694750c2bb993fcf3273562bcfefb912cd1b366cea49a492dc40aa7a`
- `subjects/mathematical-statistics/experiments/ps05_08_checks.py`: `50bc6ae96aed3223b4f8eb5983223306c2ed26adb488c2501d604e1b32054e74`
- `subjects/mathematical-statistics/experiments/ps05_08_checks-results.json`: `eefea28852a3be182be451fb91e6925b0d9e52ad009fb5212296c4a43ec6290c`
