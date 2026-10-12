# 凝聚态与量子多体

中文主卷：[condensed-matter-zh.pdf](condensed-matter-zh.pdf)；独立源码：[condensed-matter-source.zip](condensed-matter-source.zip)。64个PDF物理页（6页前置目录、58页正文与参考文献），18章理论、9章作业、1章来源说明。正文使用仓库已批准的中文XeLaTeX模板，公式为TeX，图为TikZ/PGFPlots；没有原PDF整页背景。

| 课程版本 | 实际公开材料 | 本卷位置 |
|---|---|---|
| [8.511 Fall 2004](https://ocw.mit.edu/courses/8-511-theory-of-solids-i-fall-2004/)，Patrick A. Lee | 24讲摘要、11套作业；摘要并非完整课堂逐字稿 | 理论1–6章、作业19–20章 |
| [8.512 Spring 2009](https://ocw.mit.edu/courses/8-512-theory-of-solids-ii-spring-2009/)，Patrick A. Lee；讲义1–10署名Mark Spencer Rudner | 25讲主题、12套当期作业、10套2004年补充作业；若干讲合并在同一文件 | 理论7–12章、作业21–24章 |
| [8.513 Fall 2021](https://ocw.mit.edu/courses/8-513-modern-quantum-many-body-physics-for-condensed-matter-systems-fall-2021/)，Xiao-Gang Wen | 4组幻灯片覆盖1–24讲、11套作业、学期论文要求 | 理论13–18章、作业25–27章 |

先冻结的逐文件清单见 [coverage-frozen.json](sources/coverage-frozen.json)，最后出版政策及92份原文件的URL、字节数、SHA-256和547个源PDF物理页记录见 [source-manifest.json](sources/source-manifest.json)。重复Kondo文件、幻灯片重复动画页均计入原文件页数，因此547不是独立教学页数。课程目录、下载到的文件、书本指针三者分开记录。原PDF仅用于核查，公开产物不重分发有逐件例外的原文件。

按原卷顶层编号共有89个位置：8.511有19（其中1个阅读要求），8.512当期22、2004补充25，8.513有23。84个位置完整覆盖（含15个重复题的卷内完整解答引用）、3个位置仅公开部分可完成、1个位置全为不可取得的书本题、1个阅读要求。去重复后可取得的计算位置72个，全部明确公开小问均写入；其中69个位置完整、3个保留比较/题面缺口。PDF将有共同背景的原编号合编为63个习题环境；不能把89说成89道不同题。逐套数字和缺口见 [assessment-inventory.json](qa/assessment-inventory.json)。所有解答为本项目独立补写，课程未公开这些作业的官方解答。

未覆盖：8.511 PS2题1的Marder第38页2.5(b)题面；PS7题1的Marder第17章题6；PS3题1(e)商业教材KKR图对比、PS4题1(e)完整三维APW曲线对比。公开附加题、自由费米能与模型拟合点已做。PS8题2是Marder附录C阅读要求，不虚构成计算题。未公开的8.511测验、8.513学生论文及官方评分答案不在公开文件中；论文历史要求保留。一般Bott周期与高阶范畴分类不作本书已证明定理，正文明确说明采用的稳定分类规则与有限模型推导范围。

数值验证包括FCC自由折叠能带、CuO2费米面、Hubbard二聚体全Fock矩阵、一二维有限无序样本、Mattis–Bardeen积分、Majorana开链和64维质量约束。小样本曲线不是热力学极限证明；长无序链的能级曲率有浮点分辨率限制，正文与QA保留该限制。

[BUILDING.md](BUILDING.md)说明依赖及洁净构建；[qa/README.md](qa/README.md)区分编译、链接、数值、逐页视觉、源码ZIP复编与远端核验。许可、作者和第三方例外见 [LICENSE-NOTICE.md](LICENSE-NOTICE.md)，基于OCW的改编以CC BY-NC-SA 4.0发布，不表示MIT背书。已有热统、量子与电动力学卷只作前置知识，不被覆盖或改写。
