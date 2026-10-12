# 量子力学：波函数、态空间与近似方法

从[一本连续中文讲义 PDF](quantum-mechanics-zh.pdf)开始阅读。本次合订 **194 页**，保留本科分编19章理论、39份考核题解、227道可用大题；续接研究生分编，采用现有固定中文数学 LaTeX 模板。主轴为 Barton Zwiebach 的 MIT OCW 8.04 Spring 2016 → 8.05 Fall 2013 → 8.06 Spring 2018；从干涉观察、复数振幅、概率与波函数开始，逐步建立算符、测量、角动量与近似方法。卷首保留教师、学期、先修、大纲、课历和考核方式。


新增 **[8.321 Fall 2017](https://ocw.mit.edu/courses/8-321-quantum-theory-i-fall-2017/)** 与 **[8.322 Spring 2003](https://ocw.mit.edu/courses/8-322-quantum-theory-ii-spring-2003/)** 连续分编：课堂理论按实际公开主题衔接，65道可用研究生作业题和16道公开考试题给中文题面及自写解答。8.321有24份讲义、4份习题课、12套作业及2016/2017四份考试；8.322有4个理论合本168页、3页课程安排PDF、12套作业，无公开考试或官方解答。原章内容保留，新增主线包括路径积分与规范、纠缠/熵、辐射多极/线宽、Young表示、散射极点和Dirac氢原子，不以英文PDF拼接。

新增 **20+29道纯教材题号**、PS4版权撤除题及S.14定义依赖缺失逐项保留，旧本科10道缺项不关闭。8.321第16、17讲缺稿，8.322课堂导航无官方答案。全部新增答案标为自主解答；不是MIT官方答案，不宣称逐段全文翻译或未公开讲稿已补齐。当前验收证据见[研究生发布检查](qa/graduate-release.json)、[逐件来源冻结](qa/graduate-source-freeze.md)、[公式复算](qa/graduate-formula-checks.json)、[PDF目录链接](qa/graduate-pdf-links.json)和[视觉核查](qa/graduate-visual-review.md)。

[可编辑源码 ZIP](quantum-mechanics-source.zip) · [逐项覆盖清单](coverage.json) · [编译方法](BUILDING.md) · [交付审校记录](qa/release.json) · [接管与验证说明](qa/handoff.md)

原有 17 章理论与 19 份考核的 112 道大题正文保留。本次补入此前遗漏的 20 份作业中 115 道大题，以及 8.05 Chapter 1、Chapter 3 和 8.06 Chapter 4 的理论缺口：线性代数全章七节主题、一维谱与多点势、连续谱计数、含时微扰、光电离与 Einstein 系数等。逐题写出推导、近似条件、符号检验与自学解释，数值曲线和表格自行计算与 TikZ 重绘。

本科39份考核文档的全部可用题面均已中文转述并独立解答。另有 **10 道只有商业教材题号、没有完整题面的引用对象**只列引用；两张公式表另行归档。8.05 作业 10 第 3 题指向 MIT 自身 Chapter 9 的七道练习，全部解答，按一道大题计；作业 11 正式六题与 PRACTICE 六题分别标明。解答均为 **AI 独立解答**，所选 OCW 课程页面未提供这些题目的官方答案；改编、Inspired 或 based on 的信用保留，不把全部题目冒称 MIT 原创。

新增稿四组数学独审通过；父审定位的七处题面条件/请求与线代首次定义已限定返修，另经三组增量独审绑定最终源哈希，见[修订映射](qa/parent-review-revisions.md)。旧153页版[实际图文检查](qa/visual-parent-revisions.md)查看153页联系页与13个修订/关联单页；旧151页全新增稿视觉证据按版本保留。自动模板检查通过，353个内部链接、350个书签均解析正确。98成员源码ZIP全新解压独立编译，89个TeX输入一致，153页渲染与交付版逐字节相同。

本册按概念重编，覆盖边界逐项列在册末与清单，没有宣称三课每页逐字翻译。Airy 复路径变形、非终止超几何级数增长、低能 Dirac 有效项及原有 Runge–Lenz 长算符恒等式明确作为进阶输入；新增相关练习补上有序算符推导。场论、辐射修正及完整多体理论未纳入本册。

<details>
<summary>原件、缺失材料与许可核对</summary>

公开目录保留 78 份不同 PDF，共 874 页。逐文件 PDF 格式、可读性、页数、字节数和 SHA256 已再次核验；网页快照不计作 PDF。

[原始材料目录](../../sources/quantum-mechanics/README.md) · [逐文件出处与许可记录](../../manifests/quantum-mechanics-sources.json) · [11份历史原件证据表](qa/historical-source-evidence.md) · [本次逐项增补表](qa/additions-coverage.md)

依官方 FAQ 及资源页逐件核查，23 份曾过宽暂缓的原件已全部恢复，其中可用题目和理论已合入同一本册。商业教材本体未打包；题号引用不补造题面，外书改编信用按项保留。历史撤下与恢复记录均保留，未改写 Git 历史。

8.06 Spring 2018 第 5 章原件缺失，两次考试明确不向 OCW 公开，课纲所述末周不计分作业未在作业页提供。这些官方材料仍不可取得；中文带电粒子章为独立补充，没有冒称缺失原件翻译。

</details>

本册是非官方中文改编。原件与改编按[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)署名、非商业、相同方式共享；详见[署名与许可](LICENSE-NOTICE.md)。
