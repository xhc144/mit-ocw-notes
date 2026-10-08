# PS9–11 作者覆盖与真实校验记录

本报告仅覆盖本次负责的三份作业。官方题面来自 `/tmp/statistics-assignment-review/ps9.txt`、`ps10.txt`、`ps11.txt` 的逐物理页提取与同目录官方 PDF。已实际通读三份全部题面、提示、原件修订说明及第4物理页来源声明；针对提取中的关键符号另实际查看 PS9/10/11 的第2物理页渲染。PS10 第2页原印域的大写 `R^S` 由 sourceagent 再核并据此保留。没有使用或引用非官方解答，也没有猜测外部书籍题号。

已实际阅读 `subjects/mathematical-statistics/main.tex` 的完整类、宏和正文输入结构，以及 topology 实际 vendor 副本中的 `STYLE_SPEC.md`、`ENVIRONMENTS.md`、`MATH_LAYOUT.md`、`EDITORIAL_RULES.md`、`writing-and-proof.md`、`review-gates.md`。三份使用既有 originalchapter、exercise、solution、enumerate，未增加或覆盖环境、counter、字体、行距或模板样式。

## 题面覆盖

| 作业 | 主问题 | 全编号节点 | 叶问 | 无编号实质项 | 实际截止时间 |
|---|---:|---:|---:|---:|---|
| PS9 | 2 | 17 | 16 | 0 | 2016-11-18 12:00 |
| PS10 | 3 | 28 | 23 | 0 | 2016-12-02 12:00 |
| PS11 | 3 | 19 | 15 | P1 七个分布 bullet | 2016-12-09 12:00 |

主问题均显式写出“原作业第N题.”，原子问层级逐个保持，PS11 P2.1.b 内的 1、2 两个编号子问完整保留。

| 官方物理页 | 题面与解答对应范围 |
|---|---|
| PS9 p1 | P1 假设、1、2(a) |
| PS9 p2 | P1 2(b)–(g)、3 选做及完整积分风险定义；P2 假设 |
| PS9 p3 | P2 估计式、内部点限制及1–7 |
| PS9 p4 | OCW 来源声明，正文来源链接与总书许可负责承接 |
| PS10 p1 | P1 1–3(a)–(c)、逆 Gamma 提示；P2 假设、1、2(a) |
| PS10 p2 | P2 2(b)–(c) 及高斯密度提示、3(a)–(d)；P3 1–5(a)–(c) |
| PS10 p3 | P3 6(a)–(b)、7 |
| PS10 p4 | OCW 来源声明，正文来源链接与总书许可负责承接 |
| PS11 p1 | 已更正 logistic 密度的原修订说明；P1 七分布及 Gamma 提示；P2 假设 |
| PS11 p2 | P2 1(a)、1(b).1、1(b).2、1(c)、2、3、4(a)–(c)；P3 假设、1–3 |
| PS11 p3 | P3 4(a)–(c) 及当前更正的 logistic 密度 |
| PS11 p4 | OCW 来源声明，正文来源链接与总书许可负责承接 |

## 每问解答与数学条件

- PS9 P1.1：截断下标的精确窗口大小、两侧均不足k时的下界证明。
- PS9 P1.2(a)–(d)：独立噪声方差、均值、Lipschitz 偏差与偏差方差分解。
- PS9 P1.2(e)–(g)：严格凸上界的连续最小点、边界截断与相邻整数比较；最优窗渐近上界；不依赖 L/σ² 的取整窗。
- PS9 P1.3：真实函数插值误差、相邻估计协方差的 Cauchy–Schwarz 控制、Tonelli 交换与明确 c1/c2。
- PS9 P2.1–7：Bernoulli 参数、风险分解、偏差原式、仅需一阶导数的中值余项、方差上界、风险上界、内部点 h=n^(-1/3) 的渐近选择。
- PS9 整理注：所选 k~n^(2/3) 下方差下界给出逐f匹配 Θ 速率，不误称已证 minimax 下界；密度边界的 uniform 明确反例。
- PS10 P1.1–2：S>0 时唯一 MLE、S=0 零概率异常样本、正态四阶矩与中心极限定理。
- PS10 P1.3(a)–(c)：Jeffreys 先验不正常；S>0 且 n≥1 时后验归一化；均值 n>2；均值存在与有限后验平方风险 n>4 的区别。题面未指定损失，正文明确平方损失约定。
- PS10 P2.1、2(a)–(c)：条件多元正态、λ=σ²/τ²、正定配方、后验协方差与均值。
- PS10 P2.3(a)–(d)：保留原印 R^S 并整理注修为 R^p；λ>0 下唯一解、对应有限正常先验、频率分布可退化、风险的矩阵式与谱式。另给 λ=0 及负 λ 的边界/反例。
- PS10 P3.1–7：矩阵维数、分母n的经验协方差（说明n−1约定）、半正定二次型、线性变换、秩导致奇异、样本变换、均值二次型加迹的完整展开。
- PS11 P1 七 bullet：分别计算 Bernoulli、固定方差正态、双参数正态、指数、均匀、Gamma、Poisson 的密度/质量函数；六族写 h/T/η/A 及归一化；均匀用变支撑正测度矛盾反证。
- PS11 P2.1(a)、1(b).1/2、1(c)：从总质量一/两次求导得到得分均值与信息恒等式，未遗漏分布对参数的变化。
- PS11 P2.2、3、4(a)–(c)：负号形式的导数、均值方差、Gamma 参数和函数、局部控制函数核验求导交换。
- PS11 P3.1–4(a)–(c)：一般CDF的左极限；G逆与 −F逆(1−p)、连续/可逆/对称条件；原子及非对称分布两个明确反例；probit 对称积分、logistic CDF 积分、logit 反解与模型命名。

## 真实数值运行

命令：`python subjects/mathematical-statistics/experiments/ps09_11_checks.py`，输出 `subjects/mathematical-statistics/experiments/ps09_11_checks.json`，实际 status=passed，seed=18650911，Python 3.12.14，NumPy 2.3.5，SciPy 1.17.0。运行文件与三份题解 SHA256 绑定在该 JSON。

- PS9 正弦回归 n=120/k=24/σ²=.49，全部121节点精确风险不超过上界；20,000重复的均方误差最大偏差为2.323个模拟标准误。积分精确风险约 .0241163，上界约 .9086811，显式保留相邻协方差 .00979592。
- PS9 密度 f(u)=3u²，x=.5/h=.125/n=200/L=6，偏差 .015625，方差 .01238159，风险 .01262573，上界 .260625；另写出 uniform 边界偏差−.5。
- PS10 n=6/S=7.5 的逆 Gamma 后验数值积分质量1，均值1.875；满秩与秩亏 X 的 Ridge 风险矩阵式/偏差方差式吻合，20,000重复检查一致；样本协方差变换误差 ≤1.78e−15。
- PS11 七分布逐个积分/求和的总质量均为1（Gamma误差约7e−15），不是仅用族名称判断。Gamma 一、二阶矩积分符合 α/β、α/β²；五个预测量的 logistic CDF 积分及 logit/probit 反解吻合。

首次真实运行中，固定方差正态归一化积分把正态密度与 exp(μt) 分开运算，在无穷积分的极远采样点产生 overflow/0×∞，程序断言失败。已合并到一个指数避免数值溢出，重新实际完整运行成功。没有将失败运行伪记为通过。

数值算例和模拟只检验具体参数与实现，不能替代正文的一般证明。

## 独立审读与构建状态

独立 reviewer `/root/statistics_ps06_11_review` 已实际逐行读完三份：PS10全部23叶问、PS11七bullet与15叶问未发现数学缺口；PS9指出最初整理注错误地否认本估计器所选窗口的逐f匹配下界，已补出方差下界修正。修正时的Python字符串转义引入BEL字符也已删除，三份扫描无异常控制字符。PS10原印 R^S 大写的更正已通知reviewer复读。

临时驱动位于 `/tmp/statistics-assignment-review/ps09-11-compile/`，原样复制 main 的完整 preamble，仅输入本次三份作业，不改主书 main。第一次不带 TEXMFHOME 的 XeLaTeX 实际失败于 ctex.sty 找不到（并有Fontconfig cache提醒）；随后读取项目 build.sh，使用其 TEXMFHOME=/workspace/.local/texmf 与临时 XDG_CACHE_HOME 重试。随后带项目 TEXMFHOME 与临时 cache 的两次 XeLaTeX 编译均成功，12页；第二次设置 SOURCE_DATE_EPOCH=1791417600 / FORCE_SOURCE_DATE=1。最终日志未匹配 Overfull、Underfull、Missing character、undefined、LaTeX Error。已实际按可读尺寸查看全部12页渲染，公式、上下标、层级、原印R^S、页边与QED均无可见问题；最后一页的正常章末留白保留。本临时独立驱动章号1–3仅用于本次校验，不是用户交付主书。主书最终合并的章号、目录和全书连续页仍由root构建并审看。

最终临时 PDF SHA256：`0fc007ee32e266b0990f8cdb7a479f8fdfae80e552f9467f101c0724db4017af`。第二次编译后重新渲染全部12页，12个PNG均与已实际逐页查看的PNG逐字节哈希相同，因此视觉证据绑定最终临时PDF内容。日志搜索命令的退出1表示没有找到上述告警，并非XeLaTeX失败；两次实际XeLaTeX本身均退出0。

最终三份题解哈希：

- ps09.tex：`e6b5ba7db774d4be4919b39b3f1d7ffe254e44180aded95e4159b92b5a992df5`
- ps10.tex：`05c2dc322fbebb671900f54974c9fdb98efaa78a008cb6f2ff62dce6ad21c9da`
- ps11.tex：`b58d7ebd23d2e040aa6c57265c713ee44a1fdae8f68f6c594cf5a46a6515d592`

已另外实际验证数值JSON绑定的脚本与三份题解哈希均与当前文件一致。待root执行最终全书合并；本作者没有修改原十章、main、根README、其他学科、.agents/tools，也没有执行Git操作。

## 交付源码解包后的独立运行核验

按root最新要求，将数值脚本的根定位修为自身 `parents[1]`（学科根），题解快照路径改为 `assignments/ps09.tex` 等；不再依赖外层仓库的 `subjects/mathematical-statistics` 路径。数学题解未改。实际从工作目录 `/tmp` 运行仓库中的脚本，7组检查再次passed；另把本脚本与三份assignments原样复制到 `/tmp/statistics-ps09-11-portable/{experiments,assignments}` 的独立学科根布局，再从 `/tmp` 实际运行该副本成功。两处生成JSON逐项完全相同（包括全部源哈希），说明该脚本不依赖当前工作目录或外层仓库目录。

最终脚本 SHA256：`852192292d9f81fd387aa0a156dc0157ef45390e14bbba7d7b07ad1dd098b574`。最终运行JSON SHA256：`d92b2d8696b2c5c05314fbf02ba45c56028cbb820b76e00ed6ed56666ebd8498`。JSON中源快照键现为学科根相对路径，已实际逐个核对当前文件。
