# 官方作业 PS8–PS10 作者完成记录

日期：2026-10-08。工作根：`/workspace/dg-revision-work`。范围仅为 `chapters/ps08.tex`、`ps09.tex`、`ps10.tex` 及本报告；未改主文件、模板、README、上传程序或其他学科，也未上传、安装或更改权限。

九道原题题面全部保留，题号、分值、六个显式子问及未编号要求均已对照原页。八道可核定题意的题目有 AI 独立完整解答；PS9.4 的所指引理陈述无法在公开修订版定位，按父任务明确要求保留原裸编号并登记缺口，没有猜题或伪造证明。三章章首均注明 MIT 18.950 Differential Geometry、Fall 2008、Paul Seidel，以及解答并非 MIT 官方答案。许可与统一来源说明由现有主书保留，本组不另改许可。

## 冻结源码与题目覆盖

| 文件 | SHA256 |
|---|---|
| `chapters/ps08.tex` | `82ab24b4a3bdea126f3aac52dc86411f2349db2fc8e2489f20cded28a0750886` |
| `chapters/ps09.tex` | `a7e9f1bd4e354bf66dfbf1cca60d9554bdb734b1fc95969cb90d1ff9e9a558fc` |
| `chapters/ps10.tex` | `1c004560bd4bd881b5e9bf0ee1cfae6d7dd5a189d72ed4e0f04f4ea33dd902e7` |

| 原题／标签 | 分值 | 实际完成内容 |
|---|---:|---|
| PS8.1／`ps:8-1` | 10 | 次数与逃逸路径；有限时间端点、紧致乘积正距离、半球显式收缩 |
| PS8.2／`ps:8-2` | 10 | (i) 实际拉回积分及原函数计算；(ii) 两个正则原像的局部度数 |
| PS9.1／`ps:9-1` | 4 | 嵌入环面 Gauss–Bonnet 与严格椭圆点反证 |
| PS9.2／`ps:9-2` | 6 | (i) 两个重数1奇点；(ii) 一个重数2奇点；显式场、正标架及局部绕数 |
| PS9.3／`ps:9-3` | 4 | 球面坐标平方积分；对称法及直接积分 |
| PS9.4／`ps:9-4` | 6 | 原题编号保留；所指引理缺失，暂无完整解答 |
| PS10.1／`ps:10-1` | 6 | 弧长母线度量、Christoffel 符号及两条测地线方程 |
| PS10.2／`ps:10-2` | 6 | 角动量守恒、负值反例、正确绝对值阈值、全时延拓与临界分类 |
| PS10.3／`ps:10-3` | 8 | (i) 内蕴力与切向投影；(ii) 坐标方程及换坐标逐项核验 |

原分值总计60；未将六个子问与九个顶层题重复计数。八个完整解答使用既有 `solution` 环境；PS9.4 使用明确的缺口批注，不使用空解答伪装完成。全部沿用锁定主书的 `originalchapter`、`exercise`、原生数学宏及题头空间保护。

## 原始文件与实际原页核对

下列原作业题页为 PDF 物理第2页。三页均以170dpi单页图实际打开；完整提取文本另逐题读过。物理第1页的课程元数据由文本核对，未将其列作图像视觉检查。

| 原始作业文件 | SHA256 |
|---|---|
| `sources/differential-geometry/assignments/originals/homework08.pdf` | `0f162ab05d3de500eb4fde905393d7713297c96f9bf7d2ce935209812ae5cf37` |
| `sources/differential-geometry/assignments/originals/homework09.pdf` | `e28be8f90f80d9b3ecfe96b089b757435bc8538217e53eb911eb383583762824` |
| `sources/differential-geometry/assignments/originals/homework10.pdf` | `5535f34f8af59485820911d6d3d1c23f41eb372fd3168e29560d2a63e256e918` |
| `sources/differential-geometry/assignments/text/homework08.txt` | `3aef575ec31c323deca48805036d7b1d2add26b64bee233e997b7b039d2382ed` |
| `sources/differential-geometry/assignments/text/homework09.txt` | `acc36f0bb74e72c54aff27621fe9f22c37cdeedc67e0305a4d1dc9bb48da0a3f` |
| `sources/differential-geometry/assignments/text/homework10.txt` | `738a40966c12a73eea824322bfa42ca0243e17064ded3367f973b0e068167ebb` |

所用讲义 `sources/differential-geometry/originals/ch3_revised.pdf` 的 SHA256 为 `3775e736a9a5532c93e18f98f0373904d8c50569ff958fb82cd8e4198c1538c4`；`ch4_revised.pdf` 为 `f7af9abd1fcacf69972c21dfedd6201b63696929da64f9c17f4579c061c2b8a9`。实际打开原讲义物理页：ch3 的7、8、13、14、16页，分别为 Lecture28、29、32、33、34；ch4 的3、5页，分别为 Lecture36、37。图像核对的重点为：

- PS8.1：次数解释所需的光滑、定向、无边界及 n≥1 条件另作批注，未悄改原题。Lecture32–33的积分定义、整数性与正则值公式作为原课程工具明确引用。路径只使用有限时间段；紧致性给出该段与曲面的正距离，避免把无穷远作为同伦端点。
- PS9.1：说明对象是 R³ 中紧致嵌入环面；抽象平坦环面不能用来替代原题对象。
- PS9.2：Lecture34 Definition34.1 的第一列分量展开与紧接的矩阵 `X=\widetilde X exp(mθJ)` 存在符号不一致。按矩阵式及总重数 χ(S²)=2 的约定定义正指标，并用正向立体图实际核算 +1、+1 和 +2，没有仅以图像宣称绕数。
- PS9.4：Lecture28 原页只有 Example28.1 与 Theorem28.2；Lecture29 的29.3是 Definition。所指 Lemma28.3 的陈述仍不可得，本题是唯一未完成解答的来源缺口。
- PS10.1：原作业“第32讲”照译保留；当前公开修订版的通式实在 Proposition36.4，旋转曲面在 Example37.2。原页分母 `l₁(x₁)` 在沿曲线取值时明确读作 `l₁(c₁(t))`。
- PS10.2：原题有符号 τ<1、τ>1 全部保留。另给 τ=−2 的合法单位速初值反例，证明正确的 |τ| 分界，并补充 |τ|=1 的颈圆与渐近行为。所有逃逸结论明确针对最大延拓轨迹，且先证明全时延拓。
- PS10.3：原题的切向力、局部运动律及更换参数化要求逐项作答；换坐标含二阶链式项和势梯度变换，不以一句“坐标无关”代替核验。

## 与原36题的精确对应

本组没有一道原题与基础册原36题完全相同，没有以主题相近练习替代官方题解。

| 新题 | 对应状态 |
|---|---|
| PS8.1、PS8.2、PS9.2、PS9.3、PS9.4、PS10.3 | 无原36题的完整匹配；相关基础定义或球面面积公式属于理论依赖 |
| PS9.1 | 引用 `thm:global-gb`，并采用与 `prop:elliptic-point` 相同的距离函数方法；正文另给严格椭圆点证明。均为理论依赖，不是原36题匹配 |
| PS10.1 | 使用第8章旋转曲面度量／Christoffel 方法；无原36题完整匹配 |
| PS10.2 | 与原 `ex:8b` 及其答案部分共用 Clairaut 守恒和单位速能量工具。该原题求 dθ/ds 和纬线条件，未涵盖本题的双曲面绝对值阈值、负 τ 反例或临界分类；本题这些要求均重新完整证明 |

## 独立数学复审

独立 Sol 已先读原题、独立计算，再逐问检查本稿，结论为八道可核定题目的完整解答通过；PS9.4来源缺口登记准确。复审未提出必需数学返修。报告见 [`ps08-10-sol-review.md`](ps08-10-sol-review.md)，其审核表绑定上列三个源码哈希。读取时该报告 SHA256 为 `4d5d0e8b609cf5217e2d90ddd5cc738d884e9423d6fba432329e3b34deb1aedf`。

复审另独立验证了球面面积拉回、立体图定向、W的局部分量、V(F)=F_u、北极分量−(a+ib)²、角动量临界积分和坐标链式项。本稿无需据此改动数学。后续若更改数学内容，现有哈希结论须重新绑定并复核。

## 隔离编译与实际预览

作者在 `/tmp/dg-ps08-10-preview` 使用锁定主书的原有导言及基础12章，仅加入本组三章作诊断编译。调用仓库现有 `/workspace/.local/texmf` 运行时，缓存仅写入临时目录，无安装。两轮 `xelatex -no-shell-escape -halt-on-error -interaction=nonstopmode` 成功；最终日志未见 Overfull、Missing character、未解析引用或重复标签。该诊断 PDF 共40物理页，SHA256：`29eeb36ea97e4fa90be413f463b234800e8a487790094d4303c83f07c6993c24`，输入绑定记录在临时目录 `compile-record.json`。

实际逐张打开其新增范围物理33–40页，130dpi，每页1105×1430像素，未用联系表代替观察。八页无裁切、重叠、公式越界、孤题头或孤立证明终止符。该诊断预览不含统一出版PDF的其他新增作业、前言、来源表与原36题答案，不能用其页数或观察记录代替最终整册的编译与视觉验证。

| 诊断物理页 | PNG SHA256 | 观察 |
|---:|---|---|
| 33 | `e610874057f071c8fbef90e0856417cd113c1b90c41b938dc8e0a32d6a4e7517` | PS8章首与8.1题面／证明首段同页；同伦公式清楚 |
| 34 | `d390022f91f820d53a96f5ada06c7b761cd237109a09c0b0fd0d8c57cb12cdeb` | 8.1接续与8.2两种方法完整；拉回积分与行列式显示正常 |
| 35 | `045a282be3496b213c82812656901224dd9a779766e9bea61b53cb8f661e0cff` | PS9章首、环面论证与9.2正向图公式清楚 |
| 36 | `29cb2695589bd5276e5daf446e2ebdaaf1b15ec6bffbfc64e300c0122f36510a` | −w²、重数2、9.3积分及9.4缺口批注明确 |
| 37 | `c52880f8d6cb8893ef78983bb5d959d45837bb9edcf8f859abdd3063dc4c3c79` | PS10章首与10.1方程完整；10.2守恒首段正常 |
| 38 | `62c80ccbd41ae5332732b7ea70b7d054aaf768801a60d3c3e7f4b88266a571ab` | 双曲面阈值、负值反例及临界分类显示清楚 |
| 39 | `e04bef5fa884356511c7929f36075cf8abe893fe0968ad3070c1f53aaae3457e` | 10.3运动律与换坐标推导正常；两行对齐公式在行间跨页 |
| 40 | `8c1198baa85126670e7302864fc2d57e3d525e9bb3e2c2437abc6c6b5c752654` | 续行公式、实际结论与QED同页；不是孤立QED页 |

本组无需新增几何图。统一PDF的目录链接、所有作业整合、最终逐页视觉、源码ZIP与远端校验属于父任务；作者没有把隔离预览当作上述交付证据。唯一尚未可完成的数学内容为 PS9.4 所指引理正文，现有八道解答均已完成并经独立复审。
