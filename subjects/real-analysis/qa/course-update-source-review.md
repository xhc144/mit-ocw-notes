# 实变册课程参考增补：独立来源复核

审稿人：独立 agent `/root/math_review`。核验日期：2026-10-08。

## 结论与检查范围

新增 `frontmatter/course-reference.tex` 与 `sources/real-analysis/course-reference.json` 的课程信息、24讲课历和三组官方作业题号索引均有官方网页依据，实际读取后未发现来源错配或“官方作业解答已补齐”的虚假覆盖声明。前言明确：只收入安排索引，没有收入Rudin原书题面或官方解答，正文33道练习及解答仍为编者内容。

本次逐一重算 `chapters/ch01.tex` 至 `ch09.tex` 及 `chapters/source-map.tex` 的SHA-256和字节数，与 `/tmp/real-analysis-course-update-baseline.json` 对应项 **10/10完全一致**。因此数学正文、例题、证明、来源对照及33道编者练习均未改变。本轮复用 [independent-review.md](independent-review.md) 已完成的独立数学审稿，不宣称重新审读了全书全部证明。

实际工作：完整读取新增TeX与JSON；从三份本地HTML中提取并完整读取课程正文，另读取教师、学期及课程级别栏；独立打开相同官方在线页面核对内容；逐行对照24讲中文译录；读取作业页正文及其链接结构；检查当前源目录文件清单；重算哈希。没有编辑TeX、修改原审稿记录或执行上传。

本记录只核课程信息来源和旧正文保留，不认证新增页的PDF视觉、目录点击、ZIP重编或远端交付。

## 课程信息

依据为MIT OCW官方 [Syllabus](https://ocw.mit.edu/courses/18-125-measure-and-integration-fall-2003/pages/syllabus/)。本地HTML正文从第879行开始；教师栏第347行，学期与级别栏在第385–410行。在线页面同日核验内容一致。

| 项目 | 已核事实及译录判断 |
|---|---|
| 课程 | 18.125 Measure and Integration；研究生课程 |
| 教师与学期 | Jeff Viaclovsky；Fall 2003，译为2003年秋季 |
| 授课安排 | 每周2次，每次1.5小时；未提供具体星期、钟点或逐课公历日期 |
| 先修 | Analysis I (18.100)，题名与课号均一致 |
| 考试 | 大纲明确没有考试；前言没有编造试卷安排 |
| 考核 | 到课与提交作业；未提供权重比例，前言未添加比例或改称按作业得分考核 |
| 必读教材 | Walter Rudin，Real and Complex Analysis，1986，ISBN 9780070542341；出版社与系列按官网记录 |
| 推荐教材 | Jones（1993）及Evans/Gariepy（1991）书目与官网一致；只记录书目，没有取得或转载外部教材正文 |
| 大纲范围 | RN、Hausdorff及面积/余面积公式确列于大纲；前言仍区分大纲与实际24PDF，不扩张原书覆盖结论 |

Ethan Brown依据课堂手稿排录的署名复用原讲义已经核实的来源信息，不是把大纲教师栏当作排录者证据。Fourier简介及24PDF未覆盖的说明也复用原源内容审查，本次没有新增Fourier正文。

## 24讲课历逐行对照

依据为官方 [Calendar](https://ocw.mit.edu/courses/18-125-measure-and-integration-fall-2003/pages/calendar/) 及本地 `calendar.html`。实际读取全部24行主题与截止事项，中文压缩保留相应主题，没有把网页主题误作源PDF正文覆盖证据。

| 讲次 | 中文译录核对要点 | 结果 |
|---:|---|---|
| 1 | 动机、测度空间/σ-代数、可测运算与Borel | 一致 |
| 2 | 实可测函数、极限、简单函数、正测度与积分定义 | 一致 |
| 3 | Riemann判据、两种积分比较及基本性质 | 一致 |
| 4 | 可加、单调收敛、求和交换与Fatou | 一致 |
| 5 | 复积分、DCT、零测与完备化 | 一致 |
| 6 | 矩形/多面集、开紧集、内外测度 | 一致 |
| 7 | 有限到一般可测域与测度空间 | 一致 |
| 8 | Carathéodory、Cantor与非Borel；作业1截止 | 一致 |
| 9 | 平移/伸缩/旋转与不可测集 | 一致 |
| 10 | 正泛函Riesz与两种积分衔接 | 一致 |
| 11 | Lusin与Vitali–Carathéodory | 一致 |
| 12 | 连续逼近、a.e.积分定理、可列可加；作业2截止 | 一致 |
| 13 | Egorov、依测度/a.e./子列与DCT | 一致 |
| 14 | 凸性、Jensen、Hölder、Minkowski | 一致 |
| 15 | Lp、赋范/Banach与Riesz–Fischer | 一致 |
| 16 | Cc在有限指数Lp及C0稠密 | 一致 |
| 17 | Lp/lp包含、局部Lp、凸性与平滑稠密 | 一致 |
| 18 | 欧氏非负Fubini | 一致 |
| 19 | 欧氏L1 Fubini与一般乘积测度 | 一致 |
| 20 | 产品Fubini、完备化、卷积；作业3截止 | 一致 |
| 21 | Young、磨光与有限指数光滑稠密 | 一致 |
| 22 | Lebesgue FTC、Vitali覆盖及弱L1最大估计 | 一致 |
| 23 | 微分、Lebesgue点及FTC第一部分 | 一致 |
| 24 | 广义Minkowski、Young另证、分布函数与最大算子插值 | 一致 |

第8讲网页列Cantor/nonBorel、第17讲网页列平滑稠密、第18–21讲的Fubini/Young位置，与实际PDF的已知错位被保留为“官方课历”，没有据此更改原 `source-map.tex` 的实际正文映射。第24讲表述是最大算子专门插值估计，不冒称新增了一般Marcinkiewicz定理。

## 官方作业索引与取得边界

独立读取官方 [Assignments](https://ocw.mit.edu/courses/18-125-measure-and-integration-fall-2003/pages/assignments/) 与本地 `assignments.html` 第879–946行；在线页面同日内容一致。三组都来自上述1986年Rudin教材，章号及题号没有换成本册编号。

| 作业 | 截止讲次 | Rudin原书章号 | 题号 |
|---:|---:|---:|---|
| 1 | 8 | 1 | 3–12 |
| 2 | 12 | 2 | 5–9, 20 |
| 3 | 20 | 3 | 4c, 4d, 10, 11, 13, 18b, 23, 25 |

24讲Calendar也在第8、12、20讲分别标记这三次截止，与作业页交叉一致。题号中的小题字母c/d/b均完整保留。

本地作业页的 `course-content-section` 中没有任何链接，只有教材书目、讲次和题号表；没有完整题面、作业PDF或官方解答。当前 `sources/real-analysis/` 文件清单中的PDF仍只有24份课程讲义，没有新增Rudin教材、作业题面或官方解答文件。这支持“本次核实的公开页面没有提供、且本次没有取得/收入这些内容”的范围说明；不将这一有限核验扩大为互联网上绝不存在相应材料。

`course-reference.json` 的 `problem_statements_included` 与 `official_solutions_included` 均为false，`editor_exercises_reused` 为33；与实际TeX声明一致。章内exercise环境逐章计数为4、5、3、3、5、3、3、4、3，合计33；文件完全不变，原有解答也随正文保留。没有用33道编者解答冒充Rudin题目的官方答案。

## 原数学正文逐项完整性

基线记录标记commit：`3c11b8bed5f5c1ed91002cdbaeceabee011b7a6b`。比较对象是该基线JSON的10个对应条目；本表不声称再次独立验证了该commit的远端内容。

| 文件（相对本册目录） | 当前字节数 | 与基线相同的SHA-256 | 比较 |
|---|---:|---|---|
| chapters/ch01.tex | 21462 | eb63b9e41a8e5ba37ddaa8e15dd31c358981dc53eee7221bb270a613872486a5 | 字节数及哈希一致 |
| chapters/ch02.tex | 32951 | 4a96af6dc296a3b4dbfd09e6e69ee2564ad94206dd417efaca289034e95179d1 | 字节数及哈希一致 |
| chapters/ch03.tex | 24543 | 1af5b89fd8c976d7bea08ecf817f79ab4e51348eebe46021accf80c3deddd83e | 字节数及哈希一致 |
| chapters/ch04.tex | 31873 | b5e3a787e22b642b61a6b15f00ee2bd1f47cac4f8f69c6fd570242a67c423b0e | 字节数及哈希一致 |
| chapters/ch05.tex | 34897 | 425e0f11aaa0e088edafee89dc2a6c5d2afcf7b957644b4fd99ee5f40f9abbc0 | 字节数及哈希一致 |
| chapters/ch06.tex | 17706 | 5a4f14f1460df224176ceb538ac881e31ea63e032bc5cc1cf45a253c79d1a74f | 字节数及哈希一致 |
| chapters/ch07.tex | 15502 | b1e3c5a1b7a5fda69816b5962b48464a679fdd37c1da5b8ee8c222ff2ff53f4e | 字节数及哈希一致 |
| chapters/ch08.tex | 23813 | 9db7f10b25962a53276cd62da0ce31f16e50ca645785324bdc60ee3fb0f3f218 | 字节数及哈希一致 |
| chapters/ch09.tex | 18689 | 7457fa95435a46d8d0e210798ff3e3dd08e7cb14e925d0008dd4bb90b30b4931 | 字节数及哈希一致 |
| chapters/source-map.tex | 4965 | d9de9c976965aea5dace241089af2bd82e57b5e580606b6debb2f4411cdc5fe9 | 字节数及哈希一致 |

这些哈希也正是原独立数学审稿最后绑定的版本。因此本次来源增补没有导致需要重新数学审稿的正文变更。

## 已实际核验的新文件快照

三个HTML的当前字节数与SHA-256均独立重算，逐项符合 `course-reference.json` 的来源记录；在线正文与保存快照的课程事实和表格一致。未要求整个在线HTML逐字节相等，因为网页通用模板不构成本次课程事实的变化证据。

| 文件 | 字节数 | SHA-256 |
|---|---:|---|
| frontmatter/course-reference.tex | 6185 | 6e653aacc5b4fd0047dff6f5660b18141bb6d84e5aba337b4d3374a52638ba18 |
| sources/real-analysis/course-reference.json | 2498 | b3b26329b4516e829fdd24b8cc1b82a2c1c590d2b006b8e4d94a3d9a59526b92 |
| sources/real-analysis/syllabus.html | 43183 | 8df0b0b31460fe7002062413f918507d73323b4bdba83063d6ee1c7f1f620ecc |
| sources/real-analysis/assignments.html | 42278 | 9e92bf2150d9d14c7f1d41f54f83d2222ed38abb338b36402d54c9863a2cbe9b |
| sources/real-analysis/calendar.html | 46979 | e25cc04357d15a016e92ac1e01d7d92bbfd536e7388d28756a6431983f34b5c9 |

前言保留MIT OCW、课程、教师和年份署名，注明OCW许可与外部教材题面许可的边界。此轮没有取得外部教材题面，也没有将OCW许可冒用于该类内容。
