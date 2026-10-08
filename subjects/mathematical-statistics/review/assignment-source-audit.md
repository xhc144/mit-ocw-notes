# 18.650 Fall 2016 作业原件、题目结构与权利审核

冻结日期：2026-10-08。范围为[官方 Assignments 内容页](https://ocw.mit.edu/courses/18-650-statistics-for-applications-fall-2016/pages/assignments/)当前逐条列出的 11 份 Problem Set。该页明确说明有 11 份作业，且没有提供 solutions。这里没有以自动资源索引补作业、没有猜文件名、没有寻找或导入非官方答案。每份 PDF URL 均从该页所链接的实际 resource 页面获得。

## 原件与许可结论

11 份作业原件共 **42 个物理 PDF 页**。已经下载实际官方 PDF、读取所有页面的提取文本并查看全部 42 页渲染总览；全文声明扫描与缩览覆盖全部42页；复核后实际查看可读的单页图为 PS4 p1/p2、PS5 p2、PS6 p1/p2、PS7 p1/p2/p3/p5、PS8 p1/p2/p3、PS10 p1/p2、PS11 p1/p2/p3；涉及15条源问题的页面均以原归档PDF2倍重渲染并实际打开。缩览不等同逐页可读放大检查，各检查类别已在原件JSON分别标明。每份原件末页均为 MIT OCW 署名与 Terms of Use 页面。只有 PS7 的物理第 1–2 页含题目需要的五幅 QQ 图，图旁没有发现独立第三方转载声明或 rights-reserved 例外。其余作业为数学文字、公式及 PS6 的表格，亦未发现独立第三方权利例外。资源页逐份保存并检查，没有发现给这些作业设置不同许可的文字。

本批 **11 份均可在用户授权范围内按默认 CC BY-NC-SA 4.0 保存原件和提取文本**，没有本批新增 hold。结论限定为“已检查原件和资源页没有发现明确独立权利例外”，不声称能够从网页默认许可排除所有潜在第三方权利。[MIT OCW 当前官方条款](https://ocw.mit.edu/pages/privacy-and-terms-of-use/)给出 CC BY-NC-SA 4.0，要求署名、非商业、相同许可共享和说明改动；[许可证正文](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode)为法律文本。此批原 PDF 按官方字节原样保留，文本是 PyMuPDF 的未经数学修正的机器提取，JSON 结构与审核笔记是新增整理。

默认许可的独立证据保存在 `sources/18.650-fall-2016/html/assignment-license-terms.html`，其 SHA-256 列于 `assignment-manifest.json`；每份 PDF 的末页、资源 HTML、原件 URL、完整官方文件名、字节数、SHA-256、真实物理页数与逐页提取文本哈希也列入该清单。Assignments 内容页为 `html/assignments.html`，resource 页面为 `html/problem-set-N.html`。原件和提取文本分别在 `pdf/` 与 `text/`，沿官方完整原文件名保存，文本扩展名改为 `.txt`。

**既有 PCA 课件的整份 hold 继续有效，本任务未恢复其原件或全文，也未修改讲义 source-manifest、既有九份讲义 PDF 或其他学科文件。** 其既有独立转载许可证据另见 [source-rights.md](source-rights.md)，不能用本批无例外的结论覆盖 PCA 的已知例外。

## 冻结计数与口径

“主问题”按印刷 `Problem N` 计数。“编号子问节点”计入主问题下每一个原印刷数字编号、字母编号及嵌套后代，父项和末级项分别计入；例如 PS11–2.1.b 的两个内层数字项也计入。“编号叶问”只计没有编号后代的节点。不能将两种数量混称为独立题数。题干中的分布 bullet、说明、图名和多个动词不人为编作 a/b 子问。

| PS | 主问题 | 编号子问节点 | 编号叶问 | 未编号任务记录 | 物理 PDF 页 | 印刷截止日期（均12 noon） |
|---|---:|---:|---:|---:|---:|---|
| 1 | 3 | 27 | 22 | 0 | 4 | Friday, Sep. 16 |
| 2 | 4 | 20 | 20 | 0 | 3 | Friday, Sep. 23 |
| 3 | 4 | 11 | 11 | 1 | 3 | Friday, Sep. 30 |
| 4 | 3 | 16 | 15 | 1 | 3 | Friday, Oct. 7 |
| 5 | 3 | 8 | 8 | 1 | 3 | Friday, Oct. 14 |
| 6 | 3 | 15 | 13 | 1 | 4 | Friday, Oct. 21 |
| 7 | 3 | 20 | 18 | 1 | 6 | Friday, Oct. 28 |
| 8 | 3 | 22 | 20 | 0 | 4 | Friday, Nov. 4 |
| 9 | 2 | 17 | 16 | 0 | 4 | Friday, Nov. 18 |
| 10 | 3 | 28 | 23 | 0 | 4 | Friday, Dec. 2 |
| 11 | 3 | 19 | 15 | 7 | 4 | Friday, Dec. 9 |
| **合计** | **34** | **203** | **181** | **12** | **42** | Fall 2016 |

12 个未编号记录是：PS3–2、PS4–2、PS5–3、PS7–1 四个没有编号子问的独立主问题；PS6–3 在 2.e 后的幸福/关系数据应用；PS11–1 的七个分布 bullet 案例。PS4–2 是一个交叉引用任务组，要求对 PS4–1 的六个分布分别作矩估计，保留六个案例的对应关系，不伪造新编号。PS7–1 的一个匹配任务包含五个 QQ 图与五个分布，也不能把“一个任务记录”解读为只需回答一个图。由于任务组大小不等，12 与 181 不构成具有统一原印刷口径的“总小题数”。

`assignment-inventory.json`逐 PS、逐主问题、逐原标明子问冻结 ID、父子关系、原标签、标签所在物理页、完整节点覆盖页、原提取文本的字符范围、起始定位片段、编程属性、可选属性与问题审核 ID。物理页全部 1-based，包含末尾 OCW 页；数学符号的权威仍是实际 PDF 页图。各页先原样提取，再按一换行连接，字符范围仅为追溯用，不当作完整数学转录。

每份仅印 `Fall 2016` 和截止日期，未印独立发布日期，故 `printed_issue_date` 为 null；2016 年份据印刷学期归入截止日期，PDF 未明确写时区，不额外伪称已写 Eastern。PS9–1.3 仍作为可选题保留并计数。

## 完整性、数据与编程

没有主问题只引用外书题号而缺少题面的情况，没有外部书籍题号需要推测恢复，也没有需另下载的外部数据文件链接。PS6 的 2×2 观测表和 PS5 数值观测已在题面内。PS7–1 依赖 PDF 图形，纯文字提取缺少点云形状，作者须读取原图。

PS7–2.3.e 与 PS7–3.8 要求描述可在软件（原文举 R）运行的模拟分位数算法，未明示必须提交已执行程序；JSON 明确区分算法要求与执行要求。PDF 注释中 PS1 页1的 `http:interval[.33,.53` 是不成立的自动超链接，与题面区间有关，不是数据地址；kind=4 的内部命名链接也不是数据 URL。所有实际 HTTP 外链与注释均在原件清单逐页保留供核查。

## 印刷问题与条件疑点

全部15条源问题现已逐条绑定实际打开的2倍原页图、原PDF哈希与物理页号；印刷观察与进一步数学判断在JSON分开记录。未把提取丢掉 `≠`、根号、prime、求和号等误认作原文错误。全部位置与影响记录在 JSON 的 `issues`，对应节点列出 issue ID。

- PS4 物理1页已有官方红字 log-normal pdf 修正说明；冻结当前修订版本。PS4–3 的阈值要取正数才能形成非退化薪资二值观测模型。
- PS5–2.5（物理2页）两侧完整均印 `H0:μ1=μ2`，是两个H0标签、两个等号；解答推荐将右侧修订为 `H1:μ1≠μ2`，必须明确这是编辑修订。早期缩览/低倍率审核曾把右侧等号误看成≠并错误记为“确实≠”；查看作者3倍裁图及自行2倍重渲染原页后，该错误断言已撤回，不能作为源事实保留。PS5–2.6 问“显著相同”应说明不拒绝不能证明相同，且数值 sample variance 的分母须明确。
- PS6 物理1页已有 Problem2 Question3 的官方修正提示，物理2页当前Question3要求提出并证明非渐近水平α检验；未获得旧版本，不能据提示推断旧错文。PS6–3.2.a（物理2页）的 qhat 求和确实印 X_i，应按定义改为 Y_i；常规独立性正态检验要说明边界方差为零的退化情形。
- PS7–3.8–9（物理5页）使用 S_n 单侧分位数；若为一般不独立备择给双侧相关检验，应校准绝对值或双尾并解释区别。离散临界值只能保证水平至多 α；零秩相关也不等价于独立，不能声称该秩相关检验检测所有依赖备择。
- PS8–2.3.b（物理2页）rank=p 至少需 n≥p，3.f 的 n−p 无偏方差估计需 n>p。PS8–3 只声明 pairs 独立及 X1 的密度 f；共同设计密度应补同分布假设或分别用 f_i。
- PS10–1.3（物理1页）Jeffreys 后验 proper 与后验均值存在是不同条件，均值需 n>2。PS10–2.3（物理2页）argmin 下标实际是未定义的 R^S（大写S），应为 R^p；此前小写s的记法也已纠正；与有限正 τ² 高斯先验相等还要求 λ>0，不能把未限定的 tuning parameter 自动当作已印正数。
- PS11 物理1页确有 Problem3 Question4 logistic function 的官方修正提示，物理3页当前红色密度确为 `e^(−t)/(1+e^(−t))²`；这是当前版事实，不是对未获得旧版本的还原。PS11–3.1–2（物理2页）一般 F 要用左极限处理 `Y≥0`，连续时成功概率为 `1−F(−Xᵀβ)`；变成 `F(Xᵀβ)` 需对称性，普通可逆 link 还需严格单调。正态和 logistic 示例满足这些附加性质。

这些是题解须解释的源条件，JSON没有替换官方原文，也没有在这次源审核中编写题解。归档检查重新核算全部11 PDF字节数、SHA-256、页数，校验完整203节点的标签/层级和181叶问；既有九份讲义原件的哈希仍与其原清单一致。这些文件/结构检查不证明符号转录无误，此前以完成校验描述结项不能覆盖已发现的PS5审核误判。本修订明确纠正该误判，并逐条重审15条来源记录。

## 逐条复核依据（修订2）

以下均是实际打开归档原PDF2倍单页渲染后的复核。原件完整路径、SHA-256、物理页、渲染方法与本次查看图像SHA-256逐条附于JSON的`source_evidence`。图像放在`/tmp/statistics-assignment-recheck/`供本会话检查；可用归档PDF与所记方法复现，不把临时图当作新的官方来源。

| issue ID | 实际查看物理页 | 原印刷观察 | 判断类别 |
|---|---|---|---|
| PS4-printed-correction | PS4 1 | 页首红字明确指出 Log-normal pdf 曾有 typo；第1题6分布的当前密度分母为 x√(2πσ²)，指数为−(ln x−μ)²/(2σ²)。 | official_correction_notice |
| PS4-positive-threshold | PS4 2 | 题干只说固定 threshold z，未印 z>0；问题要求二值样本识别λ、渐近方差与Fisher信息。 | condition_to_state |
| PS5-duplicate-H0 | PS5 2 | 原PDF整式为 H0:μ1=μ2 vs. H0:μ1=μ2；两个标签H0、两个关系等号。 | confirmed_printed_typo |
| PS5-identical-conclusion | PS5 2 | 第6问印 significantly identical；给均值8.43/8.07和sample variance0.22/0.17，没有另写方差分母。 | interpretation_caution |
| PS6-printed-correction | PS6 1,2 | 第1页红字只说明 Problem2 Question3 曾有typo；当前第2页第3问要求提出并证明非渐近水平α检验，没有展示旧错文。 | official_correction_notice |
| PS6-qhat-X | PS6 2 | 原定义 q=P[Y=1]，而2.a中qhat的求和与phat一样印X_i；rhat印X_iY_i。 | confirmed_printed_typo |
| PS6-nondegenerate-independence | PS6 2 | 2.d当前印 V=pq(1−p)(1−q)，2.e要求渐近水平α检验；题干未排除p,q边界。 | condition_to_state |
| PS7-two-sided-independence | PS7 3,5 | 第3页备择是X1与Y1不独立；第5页第8问明确将qα定义为S_n而非|S_n|的(1−α)分位数，第9问要求非渐近水平α检验。 | test_calibration_caution |
| PS8-sample-size-rank | PS8 1,2 | 第1页仅给n与p≥1且X1有密度g；第2页3.b声称rank=p，没有明示n≥p；3.f的统计量分母含n−p。 | condition_to_state |
| PS8-common-design-density | PS8 2,3 | 第2页Problem3仅写independent random pairs；第3页只写X1有未知密度f，却要求以β和f写似然。 | condition_to_state |
| PS10-posterior-mean | PS10 1 | 第1页θ>0、n样本、Jeffreys posterior及Bayesian estimator；给逆Gamma期望β/(α−1)，没有明示n>2。 | condition_to_state |
| PS10-ridge-domain | PS10 2 | argmin下标实际印t∈R^S，S是大写；PDF文本字形也提取为S，原题此前参数空间是R^p。 | confirmed_printed_typo |
| PS10-ridge-penalty | PS10 2 | λ只称tuning parameter且没有正号条件；3.b要求与N_p(0,τ²I_p)先验的Bayesian estimator相等。 | condition_to_state |
| PS11-printed-correction | PS11 1,3 | 第1页红字指出Problem3 Question4 logistic function曾有typo；第3页当前红色密度为 e^(−t)/(1+e^(−t))²，分母平方清晰可见。 | official_correction_notice |
| PS11-general-link | PS11 2 | 题干F是一般ε的cdf、Z_i=1_{Y_i≥0}，第2问要求以F写link，未先假定连续/对称/严格单调；第3问才假定标准正态。 | condition_to_state |
