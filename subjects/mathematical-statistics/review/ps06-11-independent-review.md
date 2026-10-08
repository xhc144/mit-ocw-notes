# PS6–11 独立新增题复审

状态：PS6–11全部中文题面及数学解答已全文实际阅读，独立重建关键结果并实际执行复算；反馈修订均已实际复查。覆盖17个主问题、105个编号末级问，以及PS6无编号应用、PS7五个QQ图、PS11七个分布bullet，合计118条对照记录。当前未发现待修数学或题面项。复审者只写本报告，不改正文、源文件、Git或其他学科。

审阅依据：`subjects/topology/vendor/math-lecture-writing/references/writing-and-proof.md` 与 `review-gates.md`；原题 `/tmp/statistics-assignment-review/ps6.txt` 至 `ps11.txt`，对应原PDF及哈希见冻结清单。另已实际查看 PS6物理页2（qhat印X、Student根号与表格）、PS10物理页2（原印大写R^S）、PS11物理页2（score导数与latent threshold）及物理页3（已修正logistic密度），PS8物理页2（样本量缺口、随机设计与logistic原干）；还实际查看了两份QQ裁切资产截图，确认五幅图及原图编号均完整、图形与原件一致。

## 独立重建及实算

独立脚本 `/tmp/independent-statistics-ps6-11.py` 已实际执行，结果 `/tmp/independent-statistics-ps6-11-results.json`。未借用作者脚本。以下是符号推导、确定性枚举及矩阵恒等式检查，不是 Monte Carlo 模拟。

- PS6P3：令g=(-q,-p,1)，单对(X,Y,XY)的协方差矩阵对角为p(1-p), q(1-q), r(1-r)，非对角为r-pq,r(1-p),r(1-q)。独立展开V=gᵀCg为−4p²q²+p²q+pq²+6pqr−2pr−2qr−r²+r；r=pq时化为pq(1-p)(1-q)。数据表p=.384,q=.506,r=.205，Z=1.3909986007009167，双侧p值=.16422585107547472，5%不拒绝。边界p或q为0/1时不能照用零分母。
- PS6P1：用样本均值标准化Z=√50(1−.98)=.14142135623730964，对应p=.44376854199085747；若选择MLE在null方差标准化，Z=√50(1/.98−1)=.1443075063646017，对应p=.4426288255651387。必须与前问所选统计量一致，两者均不拒绝。
- PS7P1实际原图识别：1 Cauchy、2 U[-√3,√3]、3 N(0,1)、4 Exp(1)、5 Laplace(√2)。图1极端重尾，图2有界端点饱和，图3近直线，图4非负右偏，图5对称且双尾较重。
- PS7P3：独立枚举n=3的6及n=5的120个排列。均值为0，方差分别1/2、1/4；n=5单侧95%分位数=.8，严格大于阈值size=5/120；|S|的95%分位数=.9，严格大于阈值size=2/120。离散检验不能无条件以≥替代>。独立枚举KS的n=3,m=4全部35种合并标签，95%分位数1。
- PS8P1：独立构造4×2满秩X及非对角正定Σ，验证G=(XᵀΣ⁻¹X)⁻¹XᵀΣ⁻¹满足GX=I（最大误差1.5e−15），GΣGᵀ=(XᵀΣ⁻¹X)⁻¹（1.1e−15）；该例二次风险trace=1.5242197970515021。
- PS8P2：条件Gaussian OLS为N_p(β,σ²(XᵀX)⁻¹)。n≥p支持满秩，n>p支持残差除n−p。条件无偏不能自动无条件无偏：p=n=1，X~U(-1,1)、独立N(0,1)误差时βhat=β+ε/X无绝对一阶矩。简单回归Q=E[(1,X)ᵀ(1,X)]，CLT协方差σ²Q⁻¹=σ²/Var(X)[[E X²,−E X],[−E X,1]]。有限样本Sxx=0需另行定义。
- PS9P1：|Ii|=min(n,i+k)−max(0,i−k)+1，方差σ²/|Ii|，偏差≤Lk/n。连续最优k=(σ²n²/(2L²))^(1/3)，实际整数取整并截断至[1,n]；最优上界常数3·2^(−2/3)L^(2/3)(σ²)^(2/3)，速率n^(−2/3)。未知常数取k~n^(2/3)。独立确定性n=40,k=12,f(x)=1.3x,σ²=.7核全41个设计点，上界最大比例.4365808039576455。线性插值用Jensen控制邻点误差并补L/n插值偏差，不能假设相邻估计独立。
- PS9P2：p_h=∫[x−h,x+h]f，Var=p_h(1−p_h)/(4nh²)≤L/(2nh)，平均积分偏差≤Lh/2，风险≤L²h²/4+L/(2nh)。h~n^(−1/3)用于固定内部x且最终h<min(x,1−x)；不声称对整个含边界[0,1]统一成立。
- PS10P1：Jeffreys π(θ)∝1/θ不proper；S=ΣXi²>0时后验IG(n/2,S/2)在n>0 proper，而均值S/(n−2)仅n>2存在。CLT渐近方差2θ²。
- PS10P2：λ=σ²/τ²>0，A=(XᵀX+λI_p)⁻¹，后验N_p(AXᵀY,σ²A)，ridge分布均值AXᵀXβ、协方差σ²AXᵀXA，风险λ²||Aβ||²+σ²tr(AXᵀXA)。独立4×2矩阵算例bias恒等式误差5.6e−16，风险1.6084137758262351。
- PS10P3：协方差p×p，AΣAᵀ为q×q且rank≤p，q>p必不逆；总体和样本二次型均非负，均值与trace恒等式由中心化与E[(X−μ)(X−μ)ᵀ]=Σ得到。
- PS11P1：固定支撑定义下，除U([0,ϑ])外六族均为指数族；两参数normal用T=(x,x²)，gamma用T=(ln x,x)。不得用随ϑ改变的h将uniform误判为regular指数族。
- PS11P2：题中负号规范使score=−X+b′(θ)，二阶=b″(θ)；EX=b′(θ)，VarX=−b″(θ)。独立符号核gamma b=αlnθ，EX=α/θ，Var=α/θ²；分别审1.b内两条恒等式。
- PS11P3：一般CDF，P(Z=1|X)=1−F((−Xᵀβ)−)。连续且严格递增时link g(u)=−F⁻¹(1−u)，还要对称才简化成F⁻¹(u)。正态为probit，logistic积分F(t)=1/(1+e^(−t))，link ln(u/(1−u))。

### PS7 真实独立软件运行补充

`/tmp/independent-statistics-ps7-simulation.py`实际执行于2026-10-08T12:52:37Z，脚本SHA256 `1265e52b11b14645e2f07d61c4401429fef513eeaa90dd2c4c2338d0d7833f35`；结果`/tmp/independent-statistics-ps7-simulation-results.json`。NumPy default_rng种子65007，B=50000；KS n=20,m=25，q95=.39、平均统计量=.24209；Spearman n=10单侧q95=.5515151515151515、绝对值q95=.6363636363636364，均值−.0005364848484848487、方差.11107085414911294（理论1/9），直接相关系数与展开公式误差2.8e−17。R代码实际阅读核查、R未执行；不把Monte Carlo分位数当作exact临界值。

## 逐问对照清单

源页为原PDF物理页。每一行“通过”表示已实际读过对应中文题面和解答并核过所述推理，不以脚本运行替代数学审阅。

|编号或无编号任务|源物理页|中文正文定位|数学/题面复核状态|
|---|---|---|---|
|PS6-1.1|1|assignments/ps06.tex:19|通过：双尾CLT与固定备择一致性|
|PS6-1.2|1|assignments/ps06.tex:20|通过：单调耦合控制复合H0上确界|
|PS6-1.3.a|1|assignments/ps06.tex:23|通过：α原题未定；常用水平不拒绝|
|PS6-1.3.b|1|assignments/ps06.tex:24|通过：独立复算p=.44376854199|
|PS6-2.1|2|assignments/ps06.tex:40|通过：MLE方差分母n|
|PS6-2.2|2|assignments/ps06.tex:41|通过：正交Gaussian分解及独立χ²比|
|PS6-2.3|2|assignments/ps06.tex:45|通过：n≥2；μ>0严格原假设的sup仍α|
|PS6-3.1|2|assignments/ps06.tex:79|通过：四格概率逐格因子化|
|PS6-3.2.a|2|assignments/ps06.tex:86|通过：印X错误明示；修正Y后LLN|
|PS6-3.2.b|2|assignments/ps06.tex:87|通过：三维CLT和协方差逐项核|
|PS6-3.2.c|2|assignments/ps06.tex:96|通过：梯度及V独立符号展开一致|
|PS6-3.2.d|2|assignments/ps06.tex:102|通过：独立影响量及连续映射|
|PS6-3.2.e|2,3|assignments/ps06.tex:107|通过：零分母/退化边界与双尾Slutsky|
|PS6-3:application|2,3|assignments/ps06.tex:115|通过：1000表格全数吻合；独立Z=1.3909986007、p=.1642258511|
|PS7-1:QQ图1|1|assignments/ps07.tex:14|通过：原图实际查看；总体QQ公式与独立识别相符|
|PS7-1:QQ图2|1|assignments/ps07.tex:15|通过：原图实际查看；总体QQ公式与独立识别相符|
|PS7-1:QQ图3|2|assignments/ps07.tex:16|通过：原图实际查看；总体QQ公式与独立识别相符|
|PS7-1:QQ图4|2|assignments/ps07.tex:17|通过：原图实际查看；总体QQ公式与独立识别相符|
|PS7-1:QQ图5|2|assignments/ps07.tex:18|通过：原图实际查看；总体QQ公式与独立识别相符|
|PS7-2.1|3|assignments/ps07.tex:44|通过：实验比较全分布|
|PS7-2.2|3|assignments/ps07.tex:45|通过：PIT均匀及独立性|
|PS7-2.3.a|3|assignments/ps07.tex:50|通过：所有跳点右连续有限最大值|
|PS7-2.3.b|3|assignments/ps07.tex:55|通过：单调变换与端点|
|PS7-2.3.c|3|assignments/ps07.tex:56|通过：乘积U[0,1]^(n+m)|
|PS7-2.3.d|3|assignments/ps07.tex:57|通过：仅H0枢轴分布|
|PS7-2.3.e|3|assignments/ps07.tex:58|通过：R算法阅读核查；独立Python50000次实际运行|
|PS7-2.3.f|3|assignments/ps07.tex:75|通过：离散strict>及交换对称MC p值|
|PS7-3.1|4|assignments/ps07.tex:109|通过：成对测量实验|
|PS7-3.2|4|assignments/ps07.tex:110|通过：排列内秩依赖|
|PS7-3.3|4|assignments/ps07.tex:111|通过：iid交换对称与1/n!|
|PS7-3.4|4|assignments/ps07.tex:112|通过：H0跨样本向量独立|
|PS7-3.5|4|assignments/ps07.tex:113|通过：(n!)²排列对等概率|
|PS7-3.6.a|4|assignments/ps07.tex:116|通过：两种求和式独立重建|
|PS7-3.6.b|4|assignments/ps07.tex:124|通过：分子中心化及系数|
|PS7-3.7|4,5|assignments/ps07.tex:133|通过：确定函数同分布|
|PS7-3.8|5|assignments/ps07.tex:134|通过：排列等价算法；独立Python50000次实际运行|
|PS7-3.9|5|assignments/ps07.tex:148|通过：单尾局限/双尾修订/零秩依赖例|
|PS8-1.1|1|assignments/ps08.tex:17|通过：正常数倍保持极小点集合|
|PS8-1.2|1|assignments/ps08.tex:18|通过：Gaussian已知Σ似然|
|PS8-1.3|1|assignments/ps08.tex:24|通过：rank=p充要及n≥p|
|PS8-1.4|1|assignments/ps08.tex:27|通过：p维GLS分布与白化；独立矩阵验算|
|PS8-1.5|1|assignments/ps08.tex:36|通过：参数欧氏损失trace风险|
|PS8-2.1|2|assignments/ps08.tex:74|通过：条件密度雅可比1|
|PS8-2.2|2|assignments/ps08.tex:78|通过：g与β分离；存在性限定|
|PS8-2.3.a|2|assignments/ps08.tex:81|通过：独立误差Gaussian条件密度|
|PS8-2.3.b|2|assignments/ps08.tex:82|通过：n≥p、Lebesgue密度与满秩|
|PS8-2.3.c|2|assignments/ps08.tex:87|通过：条件p维正态；无条件混合|
|PS8-2.3.d|2|assignments/ps08.tex:92|通过：条件均值/无条件可积性及实际反例|
|PS8-2.3.e|2|assignments/ps08.tex:95|通过：RSS/n且n=p无联合MLE|
|PS8-2.3.f|2|assignments/ps08.tex:97|通过：n>p、投影χ²及无偏|
|PS8-2.4.a|2|assignments/ps08.tex:105|通过：样本方差0事件的定义|
|PS8-2.4.b|2|assignments/ps08.tex:110|通过：cov=0及LLN一致性|
|PS8-2.4.c|2|assignments/ps08.tex:118|通过：独立乘积二阶矩CLT与2×2逆|
|PS8-2.4.d|2|assignments/ps08.tex:132|通过：残差方差一致性/单尾规则/退化边界|
|PS8-3.1|3|assignments/ps08.tex:156|通过：logit代数反解|
|PS8-3.2|3|assignments/ps08.tex:159|通过：原题缺共同密度明示；f_i版本|
|PS8-3.3|3|assignments/ps08.tex:166|通过：条件似然、Hessian/Newton、分离不存在例|
|PS9-1.1|1|assignments/ps09.tex:29|通过：两侧不足k情形纳入计数|
|PS9-1.2.a|1,2|assignments/ps09.tex:37|通过：独立噪声方差及端点|
|PS9-1.2.b|2|assignments/ps09.tex:38|通过：期望与三角不等式|
|PS9-1.2.c|2|assignments/ps09.tex:44|通过：MVT得Lipschitz偏差|
|PS9-1.2.d|2|assignments/ps09.tex:45|通过：bias²+variance|
|PS9-1.2.e|2|assignments/ps09.tex:46|通过：凸性、截断和相邻整数比较|
|PS9-1.2.f|2|assignments/ps09.tex:52|通过：最优常数独立重建|
|PS9-1.2.g|2|assignments/ps09.tex:53|通过：ceil(n^(2/3))不依赖未知量|
|PS9-1.3|2|assignments/ps09.tex:60|通过：选做未漏；共享噪声Cauchy–Schwarz、Tonelli|
|PS9-2.1|3|assignments/ps09.tex:97|通过：Bernoulli及无原子端点|
|PS9-2.2|3|assignments/ps09.tex:98|通过：风险恒等式|
|PS9-2.3|3|assignments/ps09.tex:99|通过：p_h/(2h)期望|
|PS9-2.4|3|assignments/ps09.tex:100|通过：仅一阶导数的积分余项|
|PS9-2.5|3|assignments/ps09.tex:105|通过：独立Bernoulli方差|
|PS9-2.6|3|assignments/ps09.tex:111|通过：两界相加|
|PS9-2.7|3|assignments/ps09.tex:112|通过：内部点限制及边界反例|
|PS10-1.1|1|assignments/ps10.tex:22|通过：S=0无MLE的零概率异常样本|
|PS10-1.2|1|assignments/ps10.tex:23|通过：四阶正态矩与CLT|
|PS10-1.3.a|1|assignments/ps10.tex:30|通过：单观测信息及不proper|
|PS10-1.3.b|1|assignments/ps10.tex:31|通过：归一化换元且S=0异常说明|
|PS10-1.3.c|1|assignments/ps10.tex:42|通过：n>2均值；n>4有限平方风险另区分|
|PS10-2.1|1|assignments/ps10.tex:87|通过：条件Gaussian n维|
|PS10-2.2.a|1|assignments/ps10.tex:90|通过：先验似然λ=σ²/τ²|
|PS10-2.2.b|2|assignments/ps10.tex:91|通过：p维配方及正定性|
|PS10-2.2.c|2|assignments/ps10.tex:97|通过：平方损失风险分解|
|PS10-2.3.a|2|assignments/ps10.tex:101|通过：梯度/Hessian及唯一性|
|PS10-2.3.b|2|assignments/ps10.tex:102|通过：λ>0才能匹配有限τ²|
|PS10-2.3.c|2|assignments/ps10.tex:103|通过：随机先验与固定β区分；可退化|
|PS10-2.3.d|2|assignments/ps10.tex:109|通过：偏差与trace风险，独立矩阵复算|
|PS10-3.1|2|assignments/ps10.tex:145|通过：p×p且有限二阶矩|
|PS10-3.2|2|assignments/ps10.tex:146|通过：分母n与n−1约定|
|PS10-3.3|2|assignments/ps10.tex:147|通过：二次型总体非负|
|PS10-3.4|2|assignments/ps10.tex:148|通过：样本平方和非负|
|PS10-3.5.a|2|assignments/ps10.tex:151|通过：q×q线性变换|
|PS10-3.5.b|2|assignments/ps10.tex:156|通过：q>p秩不足|
|PS10-3.5.c|2|assignments/ps10.tex:157|通过：uΣu标量方差|
|PS10-3.6.a|3|assignments/ps10.tex:161|通过：样本均值同步变换|
|PS10-3.6.b|3|assignments/ps10.tex:167|通过：标量样本方差|
|PS10-3.7|3|assignments/ps10.tex:169|通过：中心化交叉项消失及trace逐分量|
|PS11-1:bullet-1|1|assignments/ps11.tex:21|通过：Ber logit及归一化|
|PS11-1:bullet-2|1|assignments/ps11.tex:26|通过：单均值正态配方|
|PS11-1:bullet-3|1|assignments/ps11.tex:32|通过：双参数正态自然域与归一化|
|PS11-1:bullet-4|1|assignments/ps11.tex:38|通过：指数族率参数|
|PS11-1:bullet-5|1|assignments/ps11.tex:39|通过：uniform参数变支撑反证|
|PS11-1:bullet-6|1|assignments/ps11.tex:40|通过：Gamma自然域及换元|
|PS11-1:bullet-7|1|assignments/ps11.tex:51|通过：Poisson计数测度与级数|
|PS11-2.1.a|2|assignments/ps11.tex:88|通过：密度外延拓和归一化|
|PS11-2.1.b.1|2|assignments/ps11.tex:91|通过：一次积分求导及score零均值|
|PS11-2.1.b.2|2|assignments/ps11.tex:97|通过：二次求导含score²不可漏|
|PS11-2.1.c|2|assignments/ps11.tex:104|通过：单观测Fisher信息|
|PS11-2.2|2|assignments/ps11.tex:106|通过：score=−X+b′、二阶b″|
|PS11-2.3|2|assignments/ps11.tex:107|通过：Var=−b″号与凹性|
|PS11-2.4.a|2|assignments/ps11.tex:114|通过：α>0固定及支撑|
|PS11-2.4.b|2|assignments/ps11.tex:115|通过：a,b及Gamma归一化|
|PS11-2.4.c|2|assignments/ps11.tex:116|通过：均值方差及求导控制函数|
|PS11-3.1|2|assignments/ps11.tex:139|通过：threshold≥需CDF左极限|
|PS11-3.2|2|assignments/ps11.tex:146|通过：G逆及−F逆(1−p)，反例逐算|
|PS11-3.3|2|assignments/ps11.tex:153|通过：对称严格递增probit|
|PS11-3.4.a|3|assignments/ps11.tex:156|通过：密度积分与端点归一化|
|PS11-3.4.b|3|assignments/ps11.tex:157|通过：可逆logit|
|PS11-3.4.c|3|assignments/ps11.tex:162|通过：潜变量与观察变量角色区分|

## 反馈与修订复查

已反馈PS8无条件无偏可积性、离散设计Sxx=0，以及PS7五图识别。PS9初稿remark误称当前条件不给每个f匹配下界；独立复审指出Var≥σ²/(2k+1)，作者已补为所选k下Θ速率并区分minimax，数学修订已实际复读通过；新remark一度含BEL输入控制字符，作者已修为literal \asymp，已实际复读通过。PS6、PS10、PS11全文及每个末级问已实际审阅，与独立结果相符。PS10原域先转录为小写R^s，parent源审核指出实际大写R^S，已实际复看原页及最终题面/remark两处修为R^S并说明S=p。PS7初稿将joint CDF连续与joint无点原子混淆，反馈后已实际复读改为无点原子；joint CDF连续确实保证边际无原子。PS6题面“50次来电”被改成“50个间隔”数量不忠实，反馈后已还原题面，并实际复读n=50通常意图与n=49字面解释，决定相同，n=49独立复算p=.44432999519409355。

PS8初稿的单调耦合未限定非奇异事件，复审指出SZZ=0时规定的hatb=0不随b平移；作者已加SZZ>0且sigmahat>0事件，并明确零噪声的精确检验及H0错误率0，已实际复读4(d)通过。n=p残差零的联合MLE不存在、条件无偏/逆设计不可积、SZZ=0样本定义、有限二阶矩CLT、共同f不足与分离反例，均已在最终正文逐项实际核查。PS7最终新增数值两段已再次全文实际审阅，所写KS .39、Spearman .55152/.63636与独立真实运行一致。

## 最终快照

以下完整SHA256绑定实际审阅的最终.tex。每次修改后应比较哈希，对实质变化复读；本报告未执行整稿编译或最终PDF逐页排版视觉审查，这部分由parent执行，不能将数学复审充作该证据。

- `assignments/ps06.tex`：`b45aa3bfb657252f09c83fcd04045251584631938c2193c3e5850faede3b0c3d`
- `assignments/ps07.tex`：`bc8b6e60b514136e3fbfc2f73927b629e6c113457954cc9702ca883c77b405b6`
- `assignments/ps08.tex`：`009ed1e999ad87644015984d80c69e3eb4f42b64b31e1faa950a4cf81779d936`
- `assignments/ps09.tex`：`e6b5ba7db774d4be4919b39b3f1d7ffe254e44180aded95e4159b92b5a992df5`
- `assignments/ps10.tex`：`05c2dc322fbebb671900f54974c9fdb98efaa78a008cb6f2ff62dce6ad21c9da`
- `assignments/ps11.tex`：`b58d7ebd23d2e040aa6c57265c713ee44a1fdae8f68f6c594cf5a46a6515d592`
- 清单 `review/assignment-inventory.json`：`905ddaea21ee1cd7b3ecedf04e2935869c2935067a4c19a6cfec19e6097d7c0b`
- QQ资产 `assignments/assets/ps07-qqplots.pdf`：`46ecdfeebad198219d562af4287564d23b8f595d0eaed3d14d73166238fc6267`
- QQ资产 `assignments/assets/ps07-qqplots-2.pdf`：`faf01265694750c2bb993fcf3273562bcfefb912cd1b366cea49a492dc40aa7a`

复核机械检查：六份.tex未发现除TAB/换行/回车外的ASCII控制字符；这只核输入，不构成数学正确性的证明。独立脚本输出证据的具体数字已保留在本报告。
