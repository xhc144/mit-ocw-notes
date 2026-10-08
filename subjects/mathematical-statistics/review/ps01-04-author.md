# PS1–4 作者覆盖与验算记录

范围：`assignments/ps01.tex` 至 `ps04.tex`。四份官方原题完整中文翻译与 AI 独立推导解答，未读取或复制外部答案，未冒称官方 solutions。没有修改原十章、全局模板、main、其他学科或 Git。

已实际完整读取 `subjects/mathematical-statistics/main.tex` 的锁定类及宏、topology vendor 副本的 STYLE_SPEC、ENVIRONMENTS、MATH_LAYOUT、EDITORIAL_RULES、writing-and-proof、review-gates。各章只用 originalchapter、exercise、solution 及模板已加载的 enumerate。没有新宏、重定义环境、计数器或版式。未引用十章标签；本组只登记自身标签，无未核实回指。

## 原件读取与页定位

已实际完整读取 `/tmp/statistics-assignment-review/ps1.txt` 至 `ps4.txt`（包含物理页界）。官方链接及实际截止日期在每章首段给出，来源身份与 AI 独立解答身份明确。

| 原件 | 实际截止日期 | 主问题与原 PDF 物理页 | 保留编号叶问 / 全编号节点 |
|---|---|---|---|
| PS1 | 2016-09-16 中午12时 | P1、P2：p1；P3题首：p1，1–6a：p2，6b–8b：p3；p4为OCW声明 | 22 / 27 |
| PS2 | 2016-09-23 中午12时 | P1、P2.1–7：p1；P2.8、P3、P4：p2；p3为OCW声明 | 20 / 20 |
| PS3 | 2016-09-30 中午12时 | P1、P2、P3、P4.1–3：p1；P4.4：p2；p3为OCW声明 | 11 / 11，另P2无编号要求 |
| PS4 | 2016-10-07 中午12时 | P1、P2：p1；P3：p2；p3为OCW声明 | 15 / 16，另P2六分布交叉要求 |

另外实际用 PyMuPDF 将 PS1p1、PS3p1、PS4p1 渲染为 `/tmp/statistics-assignment-review/ps{1,3,4}-verify-p1.png` 并用 view_image 查看可读尺寸：核对 PS1 的两个概率、PS3P1.3 的 `sqrt(theta) x^(sqrt(theta)-1)` 和 PS4 的修正后对数正态密度（根号覆盖 `2*pi*sigma^2`）。未以文本提取猜测这些符号。

## 逐题覆盖

- PS1P1：1；2a、2b；3a、3b。分别计算依概率与L2极限、Bin(n,p)、均方误差和Poisson零质量；父编号2、3保留。
- PS1P2：1、2、3、4。逐条真假与证明；第3问反例明确指定极限变量的联合关系，第4问给p=.8的正概率数据反例。
- PS1P3：1、2、3、4；5a、5b、5c；6a、6b、6c；7；8a、8b。CLT、正态对称、覆盖事件、分位数、三种区间全部推导。5、6、8父编号保留；8a给三个实际数值区间，8b区分J1/J3最小1537与Wilson最小1533。
- PS2P1：1–4。方差、一致性、精确偏差、n>=2无偏修正；n=1不存在无偏估计补充证明。
- PS2P2：1–8。每项均有样本空间、参数空间、观测概率族与可辨识性证明，含正态符号、比例的theta<=1限制、通勤时间二元观测、67台机器右删失。
- PS2P3：1–4。CLT归一化、对称性、参数依赖区间、反解二次不等式得到参数无关区间。
- PS2P4：1–4。最大值分布、一致性、缩放偏差CDF与指数极限、渐近及精确区间、偏差积分。
- PS3P1：1–5。五种原密度分别写似然与全局极值理由；支撑限制与概率零边界样本单独说明。
- PS3P2（无编号）：N(theta,theta)的MLE计算及一致性两项要求完整写出，未遗漏。
- PS3P3：1–2。明确KL方向，正态期望与Bernoulli求和分别计算。
- PS3P4：1–4。统一TV定义及半L1公式简证，均匀/Bernoulli/随机经验Bernoulli/Poisson到Dirac四种计算全部保留。
- PS4P1：1–6。逐一MLE、得分、信息和样本信息；Bernoulli/Poisson开放参数边界没有MLE时明确说明；正态、对数正态、移位指数n=1和全相同样本的退化条件保留。
- PS4P2（无编号交叉要求）：第1题六分布均独立展开矩方程与真实计算（Bernoulli、Poisson、指数、正态、移位指数、对数正态），解答内编号1–6仅用于对应第1题；题面明确P2本身未另编子问。
- PS4P3：1–5；6a、6b、6c、6d。父编号6保留；Bernoulli观测模型、CLT、反解一致性、delta方差、阈值正根唯一性、两个模型与信息比较全部写出。

## 原件条件与疑义处理

1. PS1P1.1在n=1时两个取值重合，原题同时给同一事件概率0和1。中文题面照录，解答明确尾部按n>=2定义；有限首项不影响收敛。
2. PS1P3.8b原题未指定置信区间族。没有把J1的1537冒称所有区间的全局最优；Wilson1533可使所有经验比例下长度<=.05，同时仍只有题中固定参数渐近覆盖保证。
3. PS2P2.8原题只说机器相同和各寿命为指数，没有明说独立。乘积似然前明确增加独立建模假设；若不采用需规定联合寿命分布。67-k删失台数作为观测信息保留。
4. PS2P4.3的c须允许依赖数据与n；若固定正c覆盖趋1而非.95。正文解释此点，并写n>log20的渐近区间和所有n适用的精确区间。
5. PS4移位指数：正则Fisher信息不满足通常条件，另给普通几乎处处得分二阶矩的实际数值矩阵，不混淆两种定义。
6. PS4P3原题未显式要求z>0。正文明确z<=0全部回答1、无信息，估计与阈值优化只在z>0解答。f(0)有限约定及其概率趋零也明确。

## 确实运行的数值与模拟

执行：`python subjects/mathematical-statistics/experiments/ps01_04_checks.py`。实际退出0，结果保存在 `experiments/ps01_04_results.json`，绑定四份TeX当时SHA256。脚本使用Numpy/Scipy，固定seed=186504，不使用网络，不生成新的题目答案来源。

- PS1三置信区间端点与长度、1537/1533样本量数值，另外用Binomial精确枚举给固定p=.7341、n=10000的有限样本覆盖；用以强调正文是渐近保证。
- PS3五个标量似然独立使用bounded数值最大化，对照解析最大点，误差均<2e-6。包括Pareto形状、sqrt(theta)模型、Rayleigh尺度、Weibull速率、N(theta,theta)。支撑端点模型的极值理由在正文证明，不用优化器替代。
- 正态KL在整条实线上实际数值积分、均匀TV按两个区间积分，分别对照闭式公式。
- 正态参数(mu,variance)得分外积矩阵在整条实线上实际积分，对照diag(1/v,1/(2v²))。
- PS4阈值方程在(1,2)求正根，同时独立数值最大化信息比；lambda*z=1.59362426004004，最大I_X/I_Y=.6476102378919149。
- 均匀最大值的精确与渐近区间：n=5,20,100各50000次模拟。使用最大值精确逆CDF采样，另有渐近区间有限n的精确覆盖公式对照。
- 删失阈值估计：lambda=.7、最优阈值、n=2000、60000次Binomial样本比例模拟，实际估计量n倍经验方差与delta方法方差之比在4%内。

这些计算是公式数值支持，不是数学正确性或全部PDF页面视觉合格的自动证明。四份稿已交独立reviewer逐题审读并收到无修改项通过消息；其审读记录由reviewer单独保存。主PDF编译、页级视觉审查和最终文件交付由root统筹，本作者没有声称已经完成这些步骤。

## 临时局部编译与有限页抽看

root授权后，在 `/tmp/statistics-ps01-04-build/driver.tex` 使用实际main完整前导区（含未改变的锁定类），只input本组四章。`TEXMFHOME=/workspace/.local/texmf XDG_CACHE_HOME=/tmp/mit-statistics-font-cache xelatex -interaction=nonstopmode -halt-on-error driver.tex` 第一、第二遍均实际退出0，产出14页 `driver.pdf`。首遍日志只有正常重跑引用提示，无Overfull、Underfull、Missing character、Undefined。已实际用fitz提取全部14页文本，并实际view_image查看第1、4、10、14页可读尺寸。

在第12页文本发现PS4P1的自动QED单独落在下一页页首，随后只在该解答第6项末句补原生 `\qedhere`，数学内容不变；已通知reviewer更新SHA，并实际重跑数值脚本成功绑定最新TeX。局部编译和四页抽看不代表整本最终PDF已做全部页面视觉审查；其余页与整书最终分页仍由root统筹。

修复后第三遍XeLaTeX实际退出0，仍14页，日志只有生成适配类的正常overwrite提示，没有引用重跑、Overfull、Underfull、Missing character或Undefined提示。实际重新查看第11、12页PNG：PS4P1的QED已留在第11页解答末尾，第12页以PS4P2题面开始，不再有孤立方框。最终源码、实验JSON与独立审稿SHA已同步；临时PDF仅为局部证据，不作为用户最终分卷交付。
