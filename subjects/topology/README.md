# 度量空间、拓扑与几何基础

完整修订版：18章、132个PDF物理页（前置11页，正文及参考文献121页）。在105页版的15章和58道编者练习题解上，增补八门原课程各自的课程信息与三章官方习题中文题面、编者解答。前15章逐文件字节不变，用户固定王者模板的锁定类不变。

## 交付与验收

- [完整中文PDF](topology.pdf)：132页，1,395,878字节。
- [精简可编辑源码ZIP](topology-source.zip)：26个文件，187,218字节；只含22个实际编译TeX、中文构建说明、来源与许可文件。
- [本次最终验收](review/ASSIGNMENT_FINAL_CHECKS.json)、[官方原题覆盖清单](review/assignment-inventory.json)、[原件与范围说明](research/assignment-source-coverage.md)。
- [源码包逐文件字节与SHA256](release-source-manifest.json)、[原件来源清单](research/source-manifest.json)、[署名与许可](sources/ATTRIBUTION.md)。
- [远端逐文件实下载核验](review/assignment-upload-verification.json)：成功发布以收据内完整提交与实际检查结果为准。

八门课程分别记录作者、学期、上课安排、先修、评分与官方Calendar的公开情况，未合并成一个虚构课表。原课程包括18.S190 IAP2023、18.901 Fall2004、18.900 Spring2023、18.904 Spring2011、18.905 Fall2016、18.950 Fall2008、18.965 Fall2004和18.102 Spring2021；补课材料保持选读角色。

正文贯通度量、连续性、紧性、完备化、不动点、Baire与一致有界原理、可数性/分离/可度量化、任意积/商/紧化、同伦/基本群、覆盖提升与分类、van Kampen、有限组合曲面/Euler–Poincaré、离散Gauss–Bonnet、流形图册/逆函数/切空间和基本长度几何。完整定义、条件、主要证明、例题与原有题解保留。

## 原课程题目

| 官方材料 | 本册实际覆盖 | 解答角色 |
| --- | --- | --- |
| 18.S190三份PS | 全部24道原号大题、33个显式末级子问，包括所有Optional | 中文编者补充；完整正文证明通过准确链接复用 |
| 18.900所选六讲CQ | 第4/29/30/31/33/40讲共22题，原图必要信息以TikZ重绘；31.5的lec6依赖图另归档 | 中文编者补充，保留原号 |
| 18.901 PS5 | 两页完整原题、九行十四性质126格全部判定及九段证明 | 中文编者补充；精确处理任意索引集 |
| 18.901其他作业 | PS0—4与weekly exercises的官方教材节号/题号目录 | 完整公开题面缺失，不据编号虚构题面与答案 |

前15章的58道编者练习不计为官方作业。S190 PS3第7/8题的严格不等号紧性结论不成立；正文保留原题，给出反例，再显式提出≤修正版及完整证明。其他实际排印错误、缺非空条件和记号歧义亦披露。没有把解答称作MIT官方标准答案。

源档共35份实际PDF、165物理页，另含官方HTML与TeX；206个原件/提取文件均核对实际字节、SHA及PDF页数。35份包含讲义、作业、CQ及许可页，不等于35份讲义，也不代表八门课全部翻译。英文原件与审稿保留在仓库，不进入源码ZIP。

18.950另见固定提交[80b9182650861c1a4830fb812032abbc93a429e7](https://github.com/xhc144/mit-ocw-notes/commit/80b9182650861c1a4830fb812032abbc93a429e7)中的[《曲线与曲面的微分几何》PDF](https://raw.githubusercontent.com/xhc144/mit-ocw-notes/80b9182650861c1a4830fb812032abbc93a429e7/subjects/differential-geometry/differential-geometry.pdf)与[源码ZIP](https://raw.githubusercontent.com/xhc144/mit-ocw-notes/80b9182650861c1a4830fb812032abbc93a429e7/subjects/differential-geometry/differential-geometry-source.zip)。该册自身说明32个顶层题中30题全部要求已答，PS3.3引用的Proposition6.3与PS9.4引用的Lemma28.3尚有定位缺口；本册只互链，不将其纳入本册覆盖分母。

本册不宣称涵盖所有几何拓扑。未收入任意拓扑曲面的三角剖分及完整分类、完整奇异同调/上同调/对偶、一般维数理论、完整曲率测地线理论、Hopf–Rinow、Sard、Whitney与Morse。未选的18.900其他CQ/正式PS/考试、18.901教材练习完整题面及补课全部内容不在本次范围。原详细招生考纲PDF未重新取得的证据边界保留在书前。

## 核查与历史

第16、17、18章各经过两份独立Sol数学复审，绑定最终TeX SHA，保留初审发现与修正。来源、原题计数、课程事实与图依赖另由独立审稿核对。最终132页全部真正逐页打开130dpi PNG，记录在review/assignment-visual-*.json，不以自动渲染代替视觉检查。

131个书签目标标题全部与实际页面匹配；286个PDF链接包括231个有效内部目的地及55个HTTP链接，新题解回指亦核对目的地附近的真实题名。ZIP在空目录三遍XeLaTeX重编，所得132页PDF与交付文件二进制SHA256完全相同，同时检查逐页文字、链接和书签。

旧72/105页验收仅作历史证据。72页完整提交fd08654b6a9bfb79de8473bbf2814015db4dd159、105页交付1c676e4c765fb6dfb0493d178353e2c7e4f2d232均保留正常历史，旧记录不充作132页验收。本次只写subjects/topology/，根主页、全局清单及其他学科由统筹者维护。

## 构建与许可

源码ZIP解压后，依照其中中文README的三个XeLaTeX命令重编main.tex。TeX工程不依赖英文源档、vendor、review或tools；需系统安装XeLaTeX、列出的宏包和字体，ZIP不捆绑字体。锁定类嵌入main.tex，18个chapter可编辑，图形为内联TikZ。

仓库开发可运行vendor/math-latex-typesetting/scripts/validate.py main.tex --out build、research/verify-sources.py与tools/package_sources.py。自动PASS不替代数学/视觉审稿。译编、重排、勘误与增补采用CC BY-NC-SA4.0，保留MIT OCW及各原作者署名和第三方条款；MIT与原作者不为本项目背书。
