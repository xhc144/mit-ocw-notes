# 最终书稿物理页85–97视觉审查

已实际以 `view_image` 逐张查看13页PNG，每张1105×1430；没有以接触表或文本提取代替页面查看。此次范围覆盖PS6、PS7及PS8前段。结果：未发现需要修订的可见裁切、文字/公式重叠、缺字、图像遗漏或QED碰撞。

PDF冻结SHA256：`094d5f3c6d11fd3eace9b9595355fe6fb1b13239b5f2625c2eef237de6f56c56`（110物理页）。原render记录 `build/main.render.json` SHA256：`e3f077e333e3e2807ad5ebd268f0bab90b992db0c2758ac839996bc4c8fa4fac`。该记录指向原PNG目录 `build/.qa/main-hrykcpjo`，dpi=130。parent已告知会修改卷首前言后重建，本报告仍绑定实际看过的原快照；对新PDF应使用逐页RGB等值映射或重新实际看变化页，不能只替换哈希。

|物理页|印刷页码|实际观察|结论|
|---|---|---|---|
|85|78|作业六开章、来电题面与两种样本量说明均可读；P1 QED独立显示且未遮挡；P2题干及解答第1项在页底，下一页第2项自然续接。|通过|
|86|79|Student比值两条陈列公式完整，QED与后续习题分开；Bernoulli表格四数205/301/179/315齐全、表头与横线清楚；原印qhat的X及更正说明均可见。|通过|
|87|80|3×3协方差矩阵及两行V展开完整；标准化分式、方差与p值未碰页边；QED可见；作业七标题与导言在同页下部完整。|通过|
|88|81|PS7 QQ图1、图2完整且原编号清楚；两轴刻度、图1极端点及图2端点饱和可读；未裁切。页下留白来自图组分页，不构成内容丢失。|通过|
|89|82|PS7 QQ图3、图4、图5全部完整，原编号、轴刻度、正态直线、指数右偏及Laplace双尾均可辨；图后解答开始，图3识别文字在页底续至下一页。|通过|
|90|83|QQ解答图4/5续接正确，P1 QED可見；KS题干的sup、两个经验分布和根式/下标均完整；finite-max公式以及3(b)证明跨页续接未截断。|通过|
|91|84|KS R代码的两个函数、括号及调用齐全且在版心内；模拟示例及精确分位数/Monte Carlo p值段可读；QED未悬空到下一页。|通过|
|92|85|秩相关题面1–9及6(a)/(b)齐全，相关系数分子与根式分母完整；解答1–5自然跨页，未见编号碰撞或缺字。|通过|
|93|86|秩平方和展开及T_n两步公式完整、无越界；R排列算法各行可读并留在同一页；单侧/双侧说明与下一页的零Spearman例自然续接。|通过|
|94|87|PS7零Spearman例结束和QED可见；作业八标题/导言完整；异方差回归题面、Gaussian似然及GLS估计公式完整，下一页续讲分布。|通过|
|95|88|GLS协方差和trace风险可读，QED独立可见；随机设计题干的全部子问3(a)–(f)、4(a)–(d)齐全；两乘积似然在页底完整、无裁切。|通过|
|96|89|随机设计3(a)–(f)证明与不可积反例可读；条件正态/χ²及残差比例完整；行内Σ、逆矩阵、求和式未碰上下行；4(a)斜率分式完整后自然续页。|通过|
|97|90|SZZ=0说明与一致性完整续接；行内2×2矩阵撑高但上下行有净间距，无碰撞；中心极限定理向量公式及渐近协方差完整；4(d)长段与QED可见；logistic题干开始与logit分式完整。|通过|

重点结论：QQ五图在物理88–89页完整保留，原编号1–5、轴刻度与分布形态可读；88页下部有留白，是原图组分页结果。PS8物理97页的行内2×2矩阵确实撑高当前行，但相邻文字有净间距，不发生碰撞。长代码、协方差矩阵、Student/相关系数根式、跨页段落及页末QED均已实际核对。

## PNG完整SHA256

- `build/.qa/main-hrykcpjo/page-0085.png`：`649994c88d091a95b68cba39c01ab2cf96b8b2878973e034be7a0c1e410f92c3`
- `build/.qa/main-hrykcpjo/page-0086.png`：`3469c7ab328f01f9d3754c186cde9ed91925dfe1f2a8210b020829b159228306`
- `build/.qa/main-hrykcpjo/page-0087.png`：`fa5a6b109dbac24a7577c8446615e31b54b7841da5e26cac439b1df17ce4d90f`
- `build/.qa/main-hrykcpjo/page-0088.png`：`d3690415943c0eabf48c1714383ed818efcf7c21e015081b4c9c21941117c7d4`
- `build/.qa/main-hrykcpjo/page-0089.png`：`c448da3ebc0f9f48daa543b5f3d3745fa472efff790c867681b2aa1f7aaf42dd`
- `build/.qa/main-hrykcpjo/page-0090.png`：`bfc5f86e1f53a0765174cf55eec4c407a72cdbc8b203e2189513806e2a1d90a4`
- `build/.qa/main-hrykcpjo/page-0091.png`：`3b458460c2b4ba8c1e9706edb4dd045ec3afc87a604f0e555d7217ffe6fc7352`
- `build/.qa/main-hrykcpjo/page-0092.png`：`5e84692587a51b527894b76ee61801f6d6a02d7db1d6bfd745e73dd86616c353`
- `build/.qa/main-hrykcpjo/page-0093.png`：`ee69c538a5d00924ffca53c13bc6f1377b53c5bd0251c12122a1c2794f5e26fa`
- `build/.qa/main-hrykcpjo/page-0094.png`：`1e1020f2a12e419db65990680f14a4369e93e024a19478bcbc648dd5e443a134`
- `build/.qa/main-hrykcpjo/page-0095.png`：`57a0b3815b94bf6a7c7b02055693a74025fb5595a15d43950820029c05815801`
- `build/.qa/main-hrykcpjo/page-0096.png`：`4375b2dcd0882334dfee7dbf890eb0fb820eefe52c4819ef05a46be16fced6a9`
- `build/.qa/main-hrykcpjo/page-0097.png`：`c611948877b6152b97e42f2167db9cdd63865ee2ab63ad9a641c927755345288`

完整逐页结构记录见 `review/assessment-visual-85-97.json`。本审查只声明上述13页已看，不替代数学审阅、编译检查或其他页面的视觉审查。未改正文。
