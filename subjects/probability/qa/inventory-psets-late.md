# 作业6–10与Martingale Note清点

仅清单；不复制Ross题面。教材：Sheldon Ross, *A First Course in Probability*, 第8版，2009，ISBN 9780136033134。全部A区题均在MIT PDF公开完整题面，但按用户要求 `excluded_external_textbook`。

| 原件 | 组数 | 原件最细编号题数 | 叶子 | 合格叶子 | 排除教材叶子 | 补充查阅 |
|---|---:|---:|---:|---:|---:|---:|
| P6 | 6 | 17 | 28 | 27 | 1 | 3 |
| P7 | 7 | 23 | 54 | 52 | 2 | 2 |
| P8 | 6 | 23 | 41 | 39 | 2 | 0 |
| P9 | 7 | 23 | 33 | 32 | 1 | 1 |
| P10 | 7 | 19 | 30 | 25 | 5 | 0 |
| Note | 1 | 4 | 5 | 5 | 0 | 0 |

计数：以最细印刷编号为题，以可独立回答的明确要求为叶子。未编号任务计一题；提示内的两种条件按同一题的两个叶子登记。讨论、示例与可选感想不计正式题。正式提示中明确计算保留支撑叶子。补充查阅单列。

## P6：指数分布与正态近似

### P6.A：密度的仿射变换

- `P6.A.1` Ross教材指定题（不复制题面）（p.1；excluded_external_textbook）：`P6.A.1.density` 教材题指定要求；仅按原件结构登记
  Ross第5章 Theoretical Exercise 30；MIT公开完整题面，禁止重抄。

### P6.B：纯生过程达到n的时刻

- `P6.B.1` 达到n的期望（p.2；eligible）：`P6.B.1.expectation` 计算T_n期望
- `P6.B.2` 达到n的方差（p.2；eligible）：`P6.B.2.variance` 计算T_n方差
- `P6.B.3` 增长和数值估计（p.2；eligible）：`P6.B.3.expectation-unbounded` 判定期望是否无界；`P6.B.3.variance-unbounded` 判定方差是否无界；`P6.B.3.expectation-numerical` 估算n=10^30时的期望；`P6.B.3.variance-numerical` 估算n=10^30时的方差

### P6.C：抛币动力偏差与效应量

- `P6.C.1` 公平币实验（p.2；eligible）：`P6.C.1.sd` 40000次公平抛币头数标准差；`P6.C.1.tail-normal` 比例大于.506的正态近似概率
- `P6.C.2` 累积效应量（p.2；eligible）：`P6.C.2.proof` 证明均值差为.016 sqrt(N)倍标准差
- `P6.C.3` 大样本可辨性（p.2；eligible）：`P6.C.3.separation` N=10^6时均值间标准差数；`P6.C.3.distinguish` 是否能有信心区分两个观测及理由

### P6.D：开放初选投票的边际价值

- `P6.D.1` 条件期望（p.3；eligible）：`P6.D.1.verify` 验证候选组合下胜者效用的条件期望
- `P6.D.2` A1投票价值（p.3；eligible）：`P6.D.2.derive` 论证A1投票价值公式并解释1/2系数
- `P6.D.3` 相反候选票值（p.3；eligible）：`P6.D.3.A2` 证明A2票值是A1票值的相反数；`P6.D.3.B2` 证明B2票值是B1票值的相反数
- `P6.D.4` 反转效用（p.4；eligible）：`P6.D.4.primary` 解释效用改成负值后最优初选不变；`P6.D.4.candidate` 解释所投候选人变化（平局另作说明）

### P6.E：比较两个成交率与样本量

- `P6.E.1` 成交数之差（p.4；eligible）：`P6.E.1.mean` 计算S_N期望；`P6.E.1.variance` 计算S_N方差
- `P6.E.2` 标准化距离（p.4；eligible）：`P6.E.2.ratio` 计算E[S_N]/SD[S_N]
- `P6.E.3` 143周选择（p.5；eligible）：`P6.E.3.probability` 计算N=143时正态近似P(Z_N>0)；`P6.E.3.sample-size` 说明143约为95%识别所需样本量

### P6.F：球队优势与七场系列赛

- `P6.F.1` 单场胜率（p.6；eligible）：`P6.F.1.numerical` 101投、p=.52时第一队胜率数值
- `P6.F.2` 系列赛胜率（p.6；eligible）：`P6.F.2.numerical` 七场独立赛中赢至少四场的数值概率
- `P6.F.3` 总得分比较（p.6；eligible）：`P6.F.3.numerical` 707投中至少354投的数值概率；`P6.F.3.compare` 比较与系列赛胜率高低；`P6.F.3.explanation` 解释两种规则不同

补充查阅（不计正式题）：

- `P6.C.lookup-dynamics` 查阅Diaconis/Holmes/Montgomery 2007抛币动力偏差论文（p.2）
- `P6.C.lookup-experiment` 查阅40,000 coin tosses yield ambiguous evidence for dynamical bias（p.2）
- `P6.C.remark.cohen-d` 查阅Cohen d的精确定义（p.3）

缺口/注意事项：

- B：time zero immediately creates two bacteria; sum must start with population 2, not 1
- E preconceptions remark page 6：printed P(H|T)=.5 contradicts preceding story about Harper being behind; likely intended P(H|T^c)=.5; remark is not formal question

第三方材料：

- E remark, page 5：SSRN abstract_id=3034686 paper；omit verbatim quotation; independently paraphrase only if needed。
- C setup：Diaconis/Holmes/Montgomery and Berkeley undergraduate coin experiment；provide attribution when discussing lookup。

## P7：Cauchy、Beta与Gamma分布

### P7.A：Beta矩

- `P7.A` Ross教材指定题（不复制题面）（p.1；excluded_external_textbook）：`P7.A.expectation` 教材题指定要求；仅按原件结构登记；`P7.A.variance` 教材题指定要求；仅按原件结构登记
  Ross第5章 Theoretical Exercise 26；MIT公开完整题面，禁止重抄。

### P7.B：随机p币的联合模型

- `P7.B.1` 均匀随机数构造（p.1；eligible）：`P7.B.1.equivalence` 解释(p,X_i)联合概率律相同
- `P7.B.2` 联合密度（p.1；eligible）：`P7.B.2.density` 写p,Y1联合密度；`P7.B.2.expectation-identity` 推出P(X1=H)=E[p]
- `P7.B.3` 观测头后的后验（p.1；eligible）：`P7.B.3.conditional-cdf` 计算给定X1=H的p条件分布函数；`P7.B.3.derivative` 求其关于a的导数；`P7.B.3.posterior-density` 说明导数是后验密度并证明与x f(x)成比例；`P7.B.3.intuition` 一句话解释头观测的密度加权

### P7.C：实地采访与四轮Bayes更新

- `P7.C` 三次Marvel偏好采访（p.2；eligible）：`P7.C.interview-1` 实际采访第1位同学并记录yes/no（无法替用户伪造）；`P7.C.interview-2` 实际采访第2位同学并记录yes/no（无法替用户伪造）；`P7.C.interview-3` 实际采访第3位同学并记录yes/no（无法替用户伪造）；`P7.C.stage-0-counts` 第0轮累计yes/no数对；`P7.C.stage-0-density` 第0轮规范化后验密度多项式；`P7.C.stage-0-graph` 第0轮后验密度草图；`P7.C.stage-0-mean` 第0轮条件期望；`P7.C.stage-1-counts` 第1轮累计yes/no数对；`P7.C.stage-1-density` 第1轮规范化后验密度多项式；`P7.C.stage-1-graph` 第1轮后验密度草图；`P7.C.stage-1-mean` 第1轮条件期望；`P7.C.stage-2-counts` 第2轮累计yes/no数对；`P7.C.stage-2-density` 第2轮规范化后验密度多项式；`P7.C.stage-2-graph` 第2轮后验密度草图；`P7.C.stage-2-mean` 第2轮条件期望；`P7.C.stage-3-counts` 第3轮累计yes/no数对；`P7.C.stage-3-density` 第3轮规范化后验密度多项式；`P7.C.stage-3-graph` 第3轮后验密度草图；`P7.C.stage-3-mean` 第3轮条件期望

### P7.D：Gamma整数阶矩两种计算

- `P7.D.1.a` 隔板计数（p.2；eligible）：`P7.D.1.a.count` 计算a_j序列的数量
- `P7.D.1.b` 多项式项数（p.2；eligible）：`P7.D.1.b.multinomial` 计算固定序列对应项数A
- `P7.D.1.c` 项的期望（p.2；eligible）：`P7.D.1.c.single-term` 计算单项期望B；`P7.D.1.c.product` 计算AB
- `P7.D.1.d` 总和（p.2；eligible）：`P7.D.1.d.sum` 对所有a_j序列累加AB
- `P7.D.2` 密度积分（p.2；eligible）：`P7.D.2.density` 写Gamma密度；`P7.D.2.integral` 通过积分计算E[X^k]；`P7.D.2.agreement` 核对两种计算一致

### P7.E：IVF异质成功率

- `P7.E.a` 首轮成功率（p.3；eligible）：`P7.E.a.intuition` 直观解释首轮成功率.5
- `P7.E.b` 失败后的后验（p.3；eligible）：`P7.E.b.posterior` 求前k-1轮失败后p密度
- `P7.E.c` 下一轮成功率（p.3；eligible）：`P7.E.c.integral` 显式计算失败后的E[p]并解释为下一轮成功率
- `P7.E.d` 秩次对称法（p.3；eligible）：`P7.E.d.equivalence` 证明均匀变量模型等价；`P7.E.d.rank` 利用排列对称性解释条件成功率1/(k+1)
- `P7.E.e` 非均匀先验（p.3；eligible）：`P7.E.e.probability` 先验f(x)=2-2x时求第k轮条件成功率

### P7.F：Cauchy和的稳定性

- `P7.F` 独立Cauchy和比较（p.4；eligible）：`P7.F.probability` 求前5个Cauchy之和小于10加后5个之和的概率

### P7.G：影评与Pólya urn

- `P7.G.1` 两电影.5/.6（p.4；eligible）：`P7.G.1.normal-approx` 各143条评论时低质量电影比分更高的近似概率
- `P7.G.2` 两电影.8/.9（p.4；eligible）：`P7.G.2.normal-approx` 各100条评论时低质量电影比分更高的近似概率
- `P7.G.3` 新鲜/腐烂后验（p.4；eligible）：`P7.G.3.posterior` f fresh/r rotten后的Beta密度
- `P7.G.4` 预测评论（p.4；eligible）：`P7.G.4.predictive` 论证下一条fresh概率(f+1)/(f+r+2)；`P7.G.4.sequence` 求FRFF序列概率
- `P7.G.5` 从众评论（p.5；eligible）：`P7.G.5.sequence` Planet B启动两条后FRFF概率；`P7.G.5.compare` 与Planet A比较；`P7.G.5.general-sequence` 任意有限序列是否仍相同及理由
- `P7.G.6` 从众极限（p.5；eligible）：`P7.G.6.uniform-limit` 比较Planet A以说明极限Tomatometer均匀分布于[0,100]
- `P7.G.7` 推广启动参数（p.5；eligible）：`P7.G.7.beta-limit` 证明a条positive/b条negative时极限是100倍Beta变量；`P7.G.7.parameters` 判定Beta参数是否为a,b

补充查阅（不计正式题）：

- `P7.E.remark.lookup-ivf` 查阅NY Times With in vitro fertilization persistence pays off（p.3）
- `P7.G.7.lookup-polya` 查阅Pólya urn模型（p.5）

缺口/注意事项：

- B.3 page 1：PDF itself omits conditional bar in P(p≤a X1=H); surrounding explicit given-that wording disambiguates intended conditional CDF
- C：requires real student observations; symbolic all-sequence answer or clearly labeled example cannot claim interviews completed
- F：Cauchy means standard Cauchy by course convention; source does not spell scale/location

第三方材料：

- E remark page 3：NY Times IVF article；omit quoted numeric prose; paraphrase attributed context if needed。
- G quoted remark page 5：Cass R. Sunstein, On Rumors; discusses Matthew Salganik music experiment；exclude quotation from recreated assignment; original explanatory summary with attribution if needed。

## P8：相关、回归与悖论

### P8.A：条件矩与矩母函数

- `P8.A.1` Ross教材指定题（不复制题面）（p.2；excluded_external_textbook）：`P8.A.1.conditional-moment` 教材题指定要求；仅按原件结构登记
  Ross第7章 Problem 51；MIT公开完整题面，禁止重抄。
- `P8.A.2` Ross教材指定题（不复制题面）（p.2；excluded_external_textbook）：`P8.A.2.mgf` 教材题指定要求；仅按原件结构登记
  Ross第7章 Theoretical Exercise 48；MIT公开完整题面，禁止重抄。

### P8.B：最小二乘回归

- `P8.B.a` 标准化相关（p.2；eligible）：`P8.B.a.verify` 验证相关系数为E[XY]
- `P8.B.b` 斜率最优化（p.2；eligible）：`P8.B.b.dependence` 证明最优斜率仅取决于rho；`P8.B.b.value` 求r(rho)
- `P8.B.c` 常数最优化（p.2；eligible）：`P8.B.c.proof` 证明最佳常数为E[Z]
- `P8.B.d` 仿射最优化（p.2；eligible）：`P8.B.d.proof` 推出a=r,b=0最优

### P8.C：暴露差异与相关强度

- `P8.C.a` 吸烟星球（p.3；eligible）：`P8.C.a.correlation` 计算每日吸烟数与寿命相关
- `P8.C.b` 芹菜星球（p.4；eligible）：`P8.C.b.correlation` 计算40年暴露年数与寿命相关

### P8.D：Gaussian观测与均值回归

- `P8.D.a` 重复观测相关（p.4；eligible）：`P8.D.a.correlation` 求Z和Ztilde相关rho
- `P8.D.b` 条件预测（p.4；eligible）：`P8.D.b.latent` 计算E[X|Z]并用rho表示；`P8.D.b.repeat` 计算E[Ztilde|Z]并用rho表示
- `P8.D.c` 投篮重复表现（p.4；eligible）：`P8.D.c.sd` 计算Z标准差；`P8.D.c.repeat-zscore` 首轮高2SD时下轮预测高于均值几个SD
- `P8.D.d` 九人队选一人（p.5；eligible）：`P8.D.d.conditional-mean` 总能力6时随机队员能力的条件期望
- `P8.D.e` 药效复现（p.5；eligible）：`P8.D.e.conditional-mean` 第一次观测药效2时第二次观测条件期望

### P8.E：五大学录取的共同因素

- `P8.E.a` 单校条件录取率（p.6；eligible）：`P8.E.a.conditional` 计算给定X=x的单校录取概率
- `P8.E.b` 入围与稳录门槛（p.6；eligible）：`P8.E.b.threshold-.05` 求条件录取率超过.05的X门槛；`P8.E.b.threshold-.95` 求条件录取率超过.95的X门槛；`P8.E.b.probability-.05` 数值计算X超过第一个门槛的概率；`P8.E.b.probability-.95` 数值计算X超过第二个门槛的概率
- `P8.E.c` 至少一校（p.6；eligible）：`P8.E.c.conditional` 用Phi和C计算A(x)
- `P8.E.d` 总体概率（p.6；eligible）：`P8.E.d.admitted-integral` 论证至少一校录取的积分表达式；`P8.E.d.rejected-integral` 论证全部拒绝的积分表达式
- `P8.E.e` 数值计算（p.6；eligible）：`P8.E.e.admitted-numerical` 数值求至少一校录取率；`P8.E.e.rejected-numerical` 数值求全部拒绝率；`P8.E.e.computation-report` 说明数值工具计算过程及是否成功
- `P8.E.f` 入学与yield（p.6；eligible）：`P8.E.f.admission` 解释至少一校录取概率.166363；`P8.E.f.students` 解释总体约6655名录取学生；`P8.E.f.class-size` 解释各校约1331名入学；`P8.E.f.yield` 解释各校约.67 yield及对称/全部就读等假设

### P8.F：无限期望的两信封悖论

- `P8.F.1` 已见100（p.7；eligible）：`P8.F.1.larger` 另一个含1000的条件概率；`P8.F.1.smaller` 另一个含10的条件概率
- `P8.F.2` 条件收益（p.7；eligible）：`P8.F.2.stay` 不换的期望收益；`P8.F.2.switch` 扣1元换费后的期望收益
- `P8.F.3` 推广10^n（p.7；eligible）：`P8.F.3.larger` n≥1另一个较大信封条件概率；`P8.F.3.smaller` n≥1另一个较小信封条件概率；`P8.F.3.stay` 一般n不换的条件期望；`P8.F.3.switch` 一般n换后的净条件期望；`P8.F.3.boundary-n0` n=0的边界条件概率及收益
- `P8.F.4` 消解悖论（p.7；eligible）：`P8.F.4.resolution` 解释永远交换与无条件无限期望下比较的矛盾

缺口/注意事项：

- E.f：class-size/yield claims tacitly assume admitted applicants attend one of five universities and symmetric school choice; mark assumptions in solution
- F：must treat n=0 separately; Lecture24 hints referenced but not necessary to recover full problem

第三方材料：

- C remark page 4：WHO red-meat carcinogenicity FAQ；omit verbatim quotation。
- D remark page 5：Nosek reproducibility study abstract；omit verbatim quotation; attribution for context。

## P9：中心极限定理、大数律与试验

### P9.A：Kelly策略

- `P9.A.1` Ross教材指定题（不复制题面）（p.2；excluded_external_textbook）：`P9.A.1.expected-fortune` 教材题指定要求；仅按原件结构登记
  Ross第7章 Problem 67；MIT公开完整题面，禁止重抄。

### P9.B：95%区间

- `P9.B.1` 大学yield（p.2；eligible）：`P9.B.1.interval` 计算均值±2SD的95%区间
- `P9.B.2` 症状平均持续时间（p.2；eligible）：`P9.B.2.interval` 计算均值±2SD的95%区间
- `P9.B.3` 毕业生平均收入（p.2；eligible）：`P9.B.3.interval` 计算均值±2SD的95%区间
- `P9.B.4` 两司机评分（p.3；eligible）：`P9.B.4.Lisa-interval` Lisa平均评分区间；`P9.B.4.Laura-interval` Laura平均评分区间
- `P9.B.5` 考试总分（p.3；eligible）：`P9.B.5.interval` 计算均值±2SD的95%区间
- `P9.B.6` Poisson篮球比分（p.3；eligible）：`P9.B.6.interval` 计算均值±2SD的95%区间
- `P9.B.7` 投资平均收益（p.3；eligible）：`P9.B.7.interval` 计算均值±2SD的95%区间

### P9.C：均值变化的标准化效应量

- `P9.C.1'` 大学yield（p.3；eligible）：`P9.C.1'.effect-size` 计算修改后相对原SD的均值位移
- `P9.C.2'` 症状平均持续时间（p.3；eligible）：`P9.C.2'.effect-size` 计算修改后相对原SD的均值位移
- `P9.C.3'` 毕业生平均收入（p.3；eligible）：`P9.C.3'.effect-size` 计算修改后相对原SD的均值位移
- `P9.C.4'` 两司机评分（p.3；eligible）：`P9.C.4'.Lisa-effect-size` Lisa均值位移/原SD；`P9.C.4'.Laura-effect-size` Laura均值位移/原SD
- `P9.C.5'` 考试总分（p.3；eligible）：`P9.C.5'.effect-size` 计算修改后相对原SD的均值位移
- `P9.C.6'` Poisson篮球比分（p.3；eligible）：`P9.C.6'.effect-size` 计算修改后相对原SD的均值位移
- `P9.C.7'` 投资平均收益（p.3；eligible）：`P9.C.7'.effect-size` 计算修改后相对原SD的均值位移

### P9.D：有限预算的剂量/样本量

- `P9.D` 蓝莓试验（p.5；eligible）：`P9.D.allocation` Nb固定时比较N大b小与N小b大；`P9.D.explanation` 从估计r的精度解释选择

### P9.E：p值随样本量变化

- `P9.E` 中位p值（p.5；eligible）：`P9.E.randomness` 解释p值为何为随机变量；`P9.E.scaling` 论证6.25倍人数使中位p值Phi(-2)变为Phi(-5)

### P9.F：Jeopardy权重与爆冷

- `P9.F.1` 等权900（p.5；eligible）：`P9.F.1.mean` 求D均值；`P9.F.1.variance` 求D方差；`P9.F.1.sd` 求D标准差
- `P9.F.2` 不同题价（p.5；eligible）：`P9.F.2.mean` 求D均值；`P9.F.2.variance` 求D方差；`P9.F.2.sd` 求D标准差
- `P9.F.3` Kevin赢的概率（p.6；eligible）：`P9.F.3.equal-weights` 等权场景爆冷的正态近似数值概率；`P9.F.3.unequal-weights` 不同题价场景爆冷的正态近似数值概率

### P9.G：发表偏差与共同知识

- `P9.G.a` 个人阳性后验（p.6；eligible）：`P9.G.a.posterior` Harry给定自己阳性的后验
- `P9.G.b` 至少一个阳性后验（p.6；eligible）：`P9.G.b.posterior` Sherry给定10组中至少一个阳性的后验
- `P9.G.c` 交流后的判断（p.6；eligible）：`P9.G.c.random-order` 按提示1的随机独立完成顺序求合并信息后的共同后验/结论；`P9.G.c.Harry-first` 按提示2 Harry知道自己最先完成时求共同后验/结论

补充查阅（不计正式题）：

- `P9.A.remark.lookup-kelly` 查阅Kelly策略的对数效用来源（p.2）

缺口/注意事项：

- G.c：without submission-order assumptions no unique answer; both page7 cases required
- B intro：statement 1.5≤|N|≤2.5 about12% requires standardized N; pedagogical aside, not extra formal question
- C.5'：p changes from .8 to .08, so actual SD is not roughly unchanged; obey explicitly requested denominator SD(original N) and flag introductory approximation caveat

第三方材料：

- B/C remarks page 4：ACT writing reliability research letter；do not reproduce the quoted list; optional attributed paraphrase。

## P10：熵、鞅与金融

### P10.A：Markov链与熵

- `P10.A.1` Ross教材指定题（不复制题面）（p.2；excluded_external_textbook）：`P10.A.1.proof` 教材题指定要求；仅按原件结构登记
  Ross第9章 Problem/Theoretical Exercises 7；MIT公开完整题面，禁止重抄。
- `P10.A.2` Ross教材指定题（不复制题面）（p.2；excluded_external_textbook）：`P10.A.2.rain-frequency` 教材题指定要求；仅按原件结构登记
  Ross第9章 Problem/Theoretical Exercises 9；MIT公开完整题面，禁止重抄。
- `P10.A.3` Ross教材指定题（不复制题面）（p.2；excluded_external_textbook）：`P10.A.3.maximization` 教材题指定要求；仅按原件结构登记；`P10.A.3.entropy-value` 教材题指定要求；仅按原件结构登记
  Ross第9章 Problem/Theoretical Exercise 13；MIT公开完整题面，禁止重抄。
- `P10.A.4` Ross教材指定题（不复制题面）（p.2；excluded_external_textbook）：`P10.A.4.proof` 教材题指定要求；仅按原件结构登记
  Ross第9章 Problem/Theoretical Exercise 17；MIT公开完整题面，禁止重抄。

### P10.B：掷骰停止路径的熵

- `P10.B` 骰子首次6（p.2；eligible）：`P10.B.entropy` 计算完整停止序列X的H(X)；`P10.B.hint-length-identity` 说明H(X)=H(X,K)；`P10.B.hint-length-entropy` 直接计算几何长度K的熵；`P10.B.hint-conditional-entropy` 计算H_K(X)并用链式公式合并

### P10.C：相对熵与主观预期

- `P10.C.a` Gibbs不等式（p.2；eligible）：`P10.C.a.nonnegative` 证明期望smugness非负；`P10.C.a.equality` 证明零值当且仅当p=q并处理零概率
- `P10.C.b` 双方主观期望（p.2；eligible）：`P10.C.b.intuition` 解释零和结果为何双方均期望自己正收益
- `P10.C.c` 相对熵查阅（p.2；eligible）：`P10.C.c.lookup` 查阅relative entropy；`P10.C.c.relation` 说明与expected smugness的关系

### P10.D：赌徒破产与信念

- `P10.D.1` 30到0/80（p.3；eligible）：`P10.D.1.expectation` 求离开时财富期望；`P10.D.1.win-probability` 求到80的概率
- `P10.D.2.a` 当前输的信念（p.3；eligible）：`P10.D.2.a.truth` 判定Harriet thinks she will lose
- `P10.D.2.b` 未来认为赢（p.3；eligible）：`P10.D.2.b.truth` 判定认为将有时认为自己会赢
- `P10.D.2.c` 41后20（p.3；eligible）：`P10.D.2.c.truth` 判定认为先到41随后到20
- `P10.D.3` 停止时长（p.3；eligible）：`P10.D.3.expectation` 求总下注数期望；`P10.D.3.recursion` 用首次投掷条件期望证明F递推；`P10.D.3.quadratic` 找满足递推与边界的二次式；`P10.D.3.uniqueness` 证明解唯一

### P10.E：Black-Scholes显式积分

- `P10.E` 欧式看涨期权（p.3；eligible）：`P10.E.discounted-expectation` 显式计算exp(-rT) E[max(exp(N)-K,0)]并完成公式

### P10.F：概率阈值候选人的期望数

- `P10.F.a` 总统候选求和法（p.4；eligible）：`P10.F.a.sum` 将各人10p_i阈值命中率相加求人数期望
- `P10.F.b` 总统候选下注法（p.4；eligible）：`P10.F.b.fair-game` 以可选停止论证赌徒期望净收益0；`P10.F.b.expected-cost` 推出期望买约支出100美元并求候选人数期望
- `P10.F.c` 几乎首任配偶（p.4；eligible）：`P10.F.c.expectation` 总婚姻概率.85下超过.5阈值人数期望
- `P10.F.d` 认真候选配偶（p.4；eligible）：`P10.F.d.expectation` 超过.1阈值人数期望

### P10.G：计价单位与风险中性概率

- `P10.G` 美元/欧元支付（p.5；eligible）：`P10.G.pricing` 论证P_e=2P_d

缺口/注意事项：

- E：source omits Var(N) in this paragraph; lecture Black-Scholes context supplies σ²T; must state it explicitly
- F.c/d：threshold formula assumes each initial individual probability below threshold, continuity and final indicator; marriage variants do not explicitly repeat small-initial-probability assumption
- F：exceed vs reach threshold requires care; use supremum crossing and usual continuous bounded martingale terminal assumptions

第三方材料：

- F setup page 4：David Aldous, orally communicated to Sheffield；retain credit; original solution。
- intro page1：C3PO Star Wars asteroid odds；omit decorative quotation。

## Note：Doob可选停止定理补充题

### Note.Problems：鞅停止和往返事件

- `Note.Problems.1` 7到0/50（p.2；eligible）：`Note.Problems.1.expectation` 求最终财富期望；`Note.Problems.1.win-probability` 求最终财富50的概率
- `Note.Problems.2` 终值0或100（p.2；eligible）：`Note.Problems.2.probability` 初价47时求终值100概率
- `Note.Problems.3` 离开[15,55]出售（p.2；eligible）：`Note.Problems.3.expectation` 求首次价格above55/below15时S(T)期望
- `Note.Problems.4` 先低40后高60（p.2；eligible）：`Note.Problems.4.impossibility` 证明初价50终值0/100且往返事件概率至少.6不能为鞅

缺口/注意事项：

- 3：finite terminal N in preceding question guarantees a crossing; price is conditional expectation of [0,100] terminal value under martingale assumption
- 4：source typo sixy interpreted as sixty; explicitly retain fourth problem

第三方材料：

- page1 theorem discussion：David Williams, Probability with Martingales (1991), Theorem10.10；only cite; do not import book text。
- page1 finance discussion：Zastawniak and Capiński text；not formal exercise; do not import text。

## 重复检查与边界

本批未发现完全重复题。Note1与P10D1参数不同；P6E3与P7G1要求的概率互补；Beta题共享工具但任务不同，均保留。更早作业需由总清单合并者跨批检查。

所有六份原件完整读取；另外对原PDF重新进行layout提取。P7页1视觉复核证明条件概率竖线在原PDF即遗漏，按下文given-that解释。六份原件清单均无嵌入位图；未复制第三方长引文。

优先待补：真实采访数据；Black-Scholes段落省略的正态方差；配偶阈值题的初始概率假设。Note第4题已完整登记。

## 统一顶层题数

P6/P7/P8/P9/P10/Note依次为17/16/10/21/12/4，总80题，Ross排除9题，MIT自设71题. 109是末级显式子问数，不是顶层题数. P9 B1–3位于p3，D题跨p4–5.
