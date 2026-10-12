# 高级统计力学与统计场论

中文主卷：[advanced-statistical-physics-zh.pdf](advanced-statistical-physics-zh.pdf)；可独立编译的源码：[advanced-statistical-physics-source.zip](advanced-statistical-physics-source.zip)。主卷为89个PDF物理页（6页前置内容、83页正文及参考文献），含19章理论、19章作业与复习题，以及1章来源和证明范围说明。两门课程合成一卷，理论按先修关系贯通，原编号保留在练习标题和来源清单中。

| 课程版本 | 官方站实际公开材料 | 本卷位置 |
|---|---|---|
| [8.333 Fall 2013](https://ocw.mit.edu/courses/8-333-statistical-mechanics-i-statistical-mechanics-of-particles-fall-2013/)，Mehran Kardar | 26份讲义、6套作业、3套阶段复习题与对应官方答案、1套期末复习包与答案；讲义注明来自较早版本，确切原稿年份不明 | 理论1–7章、作业与复习题20–29章 |
| [8.334 Spring 2014](https://ocw.mit.edu/courses/8-334-statistical-mechanics-ii-statistical-physics-of-fields-spring-2014/)，Mehran Kardar | 26份讲义、6套作业、3套阶段复习题与对应官方答案；讲义注明来自较早版本，确切原稿年份不明 | 理论8–19章、作业与复习题30–38章 |

两门课合计取得78份讲义、作业及复习PDF，另有20份公开文字视频参考PDF；共98份、1226个源PDF物理页，其中包含题目与答案重叠页面。还保存官方日历、大纲及52条视频链接的元数据。本卷没有冒称逐字翻译52场视频，也没有把文字视频参考算作课程题集。逐文件URL、名称、字节数、SHA-256、页数和例外见 [source-manifest.json](sources/source-manifest.json)；编写前冻结的范围见 [coverage-frozen.json](sources/coverage-frozen.json)，52节官方日历主题与中文小节的对应见 [coverage.json](coverage.json)。原PDF和网页只在本地核查，公开包不重分发。

按原卷顶层编号，8.333有56个作业位置和47个复习位置，8.334有29个作业位置和32个复习位置，共164个原位置。本卷新写138个位置，合并同源的三维与二维Dirac题为137个习题环境；10个完整重复位置指向本卷已有解，16个位置指向已公开热统卷的12道习题及4次历史重复引用。因此164不是164道不同的新题。原题全部明确公开的小问均有答案或精确到现有解答的引用；[assessment-inventory.json](qa/assessment-inventory.json)逐套列明。官方有解答的复习包与本卷独立推导的中文解答分别标明，并在题内保留可核对的差异。

先修热统卷的8.333作业5已完整收入其第33章（原题1–12，对应习题33.1–33.12），本卷给固定版本、原题到中文题的索引和哈希，不再次复制12题。[prior-volume-reference.json](qa/prior-volume-reference.json)固定链接与核对记录。8.333复习包中的期末题来自1998、1999、2000、2003、2004、2005、2006年历史试卷，源包本身标为2007年复习；未得到的2001、2002年题或2013、2014年当期正式试卷均未编造。8.333作业6题1的原表中He3能量系数缺失，书中原样注明且不拿缺项计算。

理论包括Liouville与BBGKY、Boltzmann与输运、量子系综与virial、场论、Ginzburg与临界标度、一回路RG、Ising/对偶、BKT与二维熔化、临界动力学及开放系统增长。第19章无序与聚合物是针对大纲的编者补充，不冒称存在未公开的第27份讲义。准确解与近似、有限数值与热力学极限、官方答案与自行修正均在正文说明；特别列明连续模型的边界条件、RG截断、Bose热容的临界侧以及官方答案的可核对修正。

源码使用仓库已批准的锁定中文XeLaTeX类模板，图均为原生TikZ/PGFPlots矢量代码。编译方法见 [BUILDING.md](BUILDING.md)，QA记录见 [qa/README.md](qa/README.md)。原作者、OCW条款、CC BY-NC-SA 4.0及逐件例外见 [LICENSE-NOTICE.md](LICENSE-NOTICE.md)；本项目不表示MIT背书。
