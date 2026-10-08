# 修订版独立来源与范围审核

审核日期：2026-10-08 UTC。审核者为独立来源审稿 Agent；未参与新增正文写作。仅写入本记录，未向 `sources/` 下载文件、未上传、未改其他学科或全局文件。公开 PDF 通过 HTTPS 读入内存，以 `pdfinfo -` 核页数、`pdftotext -layout - -` 核文字及权利标记。以下“实取”指已成功取得实际 PDF 字节并解析，不等于已完成各页图像权利审查，也不等于本项目已归档。

已读现有 `README.md`、`research/source-manifest.json`、`research/source-coverage.md`、`research/source-errata.md` 及批量上传 Skill。所检查的 `/AGENTS.md`、`/workspace/AGENTS.md`、仓库根、`subjects/`、`subjects/topology/` 的 `AGENTS.md` 在本工作副本均不存在。本审核不执行 Git 写入或上传。

## 结论与连贯范围

保留原八章和原有 37 道完整题解，在其上增加：一般拓扑空间与拓扑基、子空间、积空间和商空间、可数性及基础分离性；随后进入路径、保持端点同伦、基本群、圆周基本群、van Kampen、覆盖及提升；最后用组合复形、曲面、可定向性和欧拉示性数连接局部欧氏空间及流形。这个范围可成为一本连贯的本科基础修订版，不应称为全部拓扑学或全部几何拓扑。

一般拓扑入门的多数完整证明需标为编者补充：18.901 Fall 2004 公开的是补充笔记，并非该课主体教材。基本群和覆盖的完整证明也需标为编者补充：18.904 Spring 2011 提供详细讲课安排，而本次未找到该课程的完整逐讲证明 PDF。18.905 Fall 2016 明确把基本群和覆盖作为先修，不能将它列作这部分的原讲义。

曲面与组合拓扑可直接依据 18.900 的第 28–33 讲。第 40 讲的离散角亏及离散 Gauss–Bonnet 适合作为少量几何桥接；完整曲率、超曲面和测地线理论应另成微分几何范围。18.965 的前两讲及 18.901 Notes I 可支撑流形定义、图册与基本例子；Sard、Whitney 强嵌入、Morse、de Rham 等研究生理论不宜孤立塞入当前基础册。

## 官方课程实际资源

目录数只表示官方讲义目录中的独立 PDF 资源入口，不把课次数当文件数；未实取的入口不列入已验证下载量。

| 课程及作者 | 官方目录证据 | 目录中的资源数 | 本审核实取量 | 范围判断 |
|---|---|---:|---:|---|
| 18.901 Introduction to Topology，Fall 2004，James Munkres | [Lecture Notes](https://ocw.mit.edu/courses/18-901-introduction-to-topology-fall-2004/pages/lecture-notes/)、[Readings](https://ocw.mit.edu/courses/18-901-introduction-to-topology-fall-2004/pages/readings/) | 11 份 optional supplementary notes | Notes B–K 共 10 PDF、43 物理页；A 未实取 | 主体读 Munkres 商业教材；公开笔记并非从定义开始的一套完整通论 |
| 18.905 Algebraic Topology I，Fall 2016，Haynes Miller | [Lecture Notes](https://ocw.mit.edu/courses/18-905-algebraic-topology-i-fall-2016/pages/lecture-notes/)、[Syllabus](https://ocw.mit.edu/courses/18-905-algebraic-topology-i-fall-2016/pages/syllabus/) | 38 PDF 入口 | lec5、18、30 共 3 PDF、15 物理页 | 从奇异同调开始，后接 CW、同调代数、上同调及对偶；明确假设已熟悉基本群、覆盖 |
| 18.900 Geometry and Topology in the Plane，Spring 2023，Paul Seidel | [Course](https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/)、[Syllabus](https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/pages/syllabus/) | 40 个讲次页面，分别有讲义入口；本次未实取全部 40 PDF | lec28–33、40 共 7 PDF、35 物理页 | 本科、可视化的精选几何拓扑；线性代数支撑组合同调 |
| 18.904 Seminar in Topology，Spring 2011，Andrew Snowden | [Lecture Summaries](https://ocw.mit.edu/courses/18-904-seminar-in-topology-spring-2011/pages/lecture-summaries/)、[Teaching Notes](https://ocw.mit.edu/courses/18-904-seminar-in-topology-spring-2011/pages/teaching-notes/) | 39 次课的 HTML 安排；该页无逐讲讲义 PDF 链接 | 仅读官方 HTML | 基本群、van Kampen、覆盖有详细讲课任务，引用 Hatcher/Massey；不是现成完整证明讲义 |
| 18.950 Differential Geometry，Fall 2008，Paul Seidel | [Lecture Notes](https://ocw.mit.edu/courses/18-950-differential-geometry-fall-2008/pages/lecture-notes/)、[Syllabus](https://ocw.mit.edu/courses/18-950-differential-geometry-fall-2008/pages/syllabus/) | 4 个章节 PDF，覆盖课次 1–41 | 4 PDF、60 物理页 | 曲率为主线，要求实分析、多元微积分及线性代数，适合另册 |
| 18.965 Geometry of Manifolds，Fall 2004，Tomasz S. Mrowka | [Lecture Notes](https://ocw.mit.edu/courses/18-965-geometry-of-manifolds-fall-2004/pages/lecture-notes/)、[Syllabus](https://ocw.mit.edu/courses/18-965-geometry-of-manifolds-fall-2004/pages/syllabus/) | 26 PDF 入口，对应课次 1–35（若干合讲） | lecture1、2 共 2 PDF、6 物理页 | 研究生课，先修 18.101 与 18.905；当前册可选定义和基础例子 |

18.905 笔记的官方说明还列出课堂 LaTeX 记录者 **Sanath Devalapurkar** 和插图作者 **Xianglong Ni**，不能只用 PDF Author 元数据中的 Haynes Miller 覆盖这些贡献。应连同讲授者、课程及学期一并署名。

18.900 syllabus 明确：Spring 2023 实际课堂省略了 lec20、24–25、38、40；这些讲义仍被正式公开。应区分“公开 40 个讲次的材料”与“该学期实际讲完 40 讲”。第 40 讲如采用，标明是课程公开的补充讲义、当学期未讲。该页也明确 problem sets 与 exams 不向 OCW 用户提供；公开的配套材料是 comprehension questions，不能把自编题解称作官方习题集或标准答案。

## 18.900 可直接采用的七份实际讲义

七份 Author 元数据均为 Paul Seidel；各有 4 页正文及末尾 1 页 OCW 来源与条款提示。未发现逐页渐显重复；印刷页码在不同讲之间的跳号不能解释为遗漏该讲正文。本表只列已实取文件。

| 讲次与真实题名 | 印刷正文页 | 物理页 / 字节 | 用途 |
|---|---|---|---|
| 28 Delaunay Triangulations | 212–215 | 5 / 280549 | 有限点集三角剖分、翻边、Delaunay、形状复形；Delaunay 关键几何引理原文略证 |
| 29 Betti Numbers | 219–222 | 5 / 285230 | 平面复形、边界矩阵、欧拉示性数及 Betti 数 |
| 30 Betti Numbers (continued) | 225–228 | 5 / 304579 | 平面孔洞、抽象复形、四面体边界、Vietoris–Rips 例子 |
| 31 Surfaces | 232–235 | 5 / 335790 | 组合曲面、可定向性、环面、射影平面、Betti 数关系 |
| 32 Combinatorial Loops | 239–242 | 5 / 354416 | 组合环路与自由同伦、切割和绕数；与基点基本群需区分 |
| 33 Combinatorial Winding Numbers and the Boundary Operators | 246–249 | 5 / 391326 | 环路边计数、边界算子、同伦不变量的线性解释 |
| 40 Geometry of Combinatorial Surfaces | 292–295 | 5 / 356711 | 角亏、离散 Gauss–Bonnet；后半部讨论平移曲面与台球 |

资源页与文件页均已从官方链接解析，链接模式并非凭文件名猜测：

| 讲次 | 官方资源页 | 实际 PDF URL | SHA256 |
|---:|---|---|---|
| 28 | [resource](https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/resources/mit18_900s23_lec28_pdf/) | [PDF](https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/mit18_900s23_lec28.pdf) | `0ea6068429729cb54e5f03649e6f029d8746af99ab3b60b7a6c0a9f54217ea77` |
| 29 | [resource](https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/resources/mit18_900s23_lec29_pdf/) | [PDF](https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/mit18_900s23_lec29.pdf) | `7743654402c859242156cd9fe53f8de2d16121c96295f7dfa68a9ad86e3e2c55` |
| 30 | [resource](https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/resources/mit18_900s23_lec30_pdf/) | [PDF](https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/mit18_900s23_lec30.pdf) | `00fcb374381a4cd1de54b59239a494e2bd577164155b1226ed1c570c167d3972` |
| 31 | [resource](https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/resources/mit18_900s23_lec31_pdf/) | [PDF](https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/mit18_900s23_lec31.pdf) | `cd4dcbbfcbddd1c428070fcee3042a965317d18f3bb72d7846b09d4f3e2c2f86` |
| 32 | [resource](https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/resources/mit18_900s23_lec32_pdf/) | [PDF](https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/mit18_900s23_lec32.pdf) | `0e3445d837b0f82d9f4e6254a6f6e92e08b2c24a1e66b7d35f167d6d4c37d31c` |
| 33 | [resource](https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/resources/mit18_900s23_lec33_pdf/) | [PDF](https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/mit18_900s23_lec33.pdf) | `8fee491ead6faa829ba45c890afe81adfb791dd7f6f016c5018658ee98b3a9ee` |
| 40 | [resource](https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/resources/mit18_900s23_lec40_pdf/) | [PDF](https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/mit18_900s23_lec40.pdf) | `e70b8914645ae59f0152b92b155d2eaaaa1e37f17410e11d93566cffd9db8245` |

曲面分类定理不是 lec31 的实际覆盖范围。若新增闭曲面分类及完整证明，须作为明确的编者补充，不能把 lec31 的例子与 Betti 关系包装成官方分类证明。

## 18.901 补充笔记的真实题名

目录周主题与实际 PDF 内容不同，不能仅按目录周主题命名译编章节。以下 B–K 均已实取，页数合计 43。扫描原件 OCR 有误字，题名按内容作正常文字转写；题名不代表已对全篇数学证明作逐页审校。

| 原文件 | 实际题名 | 物理页 | 当前册适用性 |
|---|---|---:|---|
| Notes B | Proof of the Well-ordering Theorem | 7 | 良序基础，非当前扩充主线 |
| Notes C | The Long Line | 2 | 一般拓扑反例，正文可少量说明 |
| Notes D | Countability Axioms | 3 | 可数性关系与反例，可选 |
| Notes E | Normality of Linear Continua | 2 | 序拓扑正常性，选读 |
| Notes F | The Separation Axioms | 5 | 分离公理反例，可选 |
| Notes G | Normality of Quotient Spaces | 9 | 商空间正常性及相关构造，可选基础命题 |
| Notes H | Tychonoff via Well-ordering | 3 | 依赖选择公理，不为凑范围硬塞 |
| Notes I | Locally Euclidean Spaces | 3 | 流形的局部欧氏性质，适合基础桥接 |
| Notes J | The Prüfer Manifold | 4 | 非正常的局部欧氏反例，选读 |
| Notes K | Compactly Generated Spaces | 5 | 紧生成、proper/perfect 等，非当前基础主线 |

Notes I 的实际文件为 [8fade8afd61bc96576661ee625d076db_notes_i.pdf](https://ocw.mit.edu/courses/18-901-introduction-to-topology-fall-2004/8fade8afd61bc96576661ee625d076db_notes_i.pdf)，158348 字节，SHA256 `77f7b58275e6584f561ee40dc94e43ad3eeb3038ff602fc5a4cc3a653fe909e1`。其 [资源页](https://ocw.mit.edu/courses/18-901-introduction-to-topology-fall-2004/resources/notes_i/) 可作课程、学期、许可的归档证据。

Notes A 的 [资源页](https://ocw.mit.edu/courses/18-901-introduction-to-topology-fall-2004/resources/18901/) 明确特殊署名为 Dr. Joao P. Santos，并标 Used with permission；本审核未实取 A，不能给它虚报页数或未见限制的逐页结论。

## 18.905、18.950 与 18.965 的实际抽核文件

| 来源 | 实取题名 | 物理页 | 判断 |
|---|---|---:|---|
| 18.905 lec5 | Homotopy, Star-shaped Regions | 5 | 讨论同调比较及同伦；不是基本群与覆盖的完整课程 |
| 18.905 lec18 | Euler Characteristic and Homology Approximation | 5 | 有限 CW 与同调方法，要求前文工具；基础册优先用有限二维复形的自足证明 |
| 18.905 lec30 | Surfaces and Nondegenerate Symmetric Bilinear Forms | 5 | 上同调乘积及曲面配对；实际文件开头承接 lec29，不可机械删去所谓“标题前内容” |
| 18.950 ch1 | Local and Global Geometry of Plane Curves | 12 | 独立微分几何主线 |
| 18.950 ch2 | Local Geometry of Hypersurfaces | 17 | 独立微分几何主线 |
| 18.950 ch3 | Global Geometry of Hypersurfaces | 18 | 独立微分几何主线 |
| 18.950 ch4 | Geometry of Lengths and Distances | 13 | 独立微分几何主线 |
| 18.965 lecture1 | Manifolds: Definitions and Examples | 4 | 可选图册、球面、射影空间等基础内容 |
| 18.965 lecture2 | Smooth Maps and the Notion of Equivalence | 2 | 可选光滑映射、微分同胚与普通同胚的区别 |

18.965 两份实取文件：

- [lecture1.pdf](https://ocw.mit.edu/courses/18-965-geometry-of-manifolds-fall-2004/34fad8f392208544e2b1e9794c33cbe7_lecture1.pdf)，89818 字节，SHA256 `5a6433da86a8d5d5c4031b79d5b2ef5ae5f15b7a05bc0b4e3ce1c68761ec5920`。
- [lecture2.pdf](https://ocw.mit.edu/courses/18-965-geometry-of-manifolds-fall-2004/b481a27fb1583bbaf43153bcaf0643fe_lecture2.pdf)，63494 字节，SHA256 `894fb86d9ead48f10ad6b80874da32367da672b0b4897ee8cb3cc7b2679f874d`。

18.950 的四份文件均有 OCW 来源页；本次可提取文字中未发现版权例外标记，但这不代替将来整册归档前的图像核查。其 syllabus 中列举的 Kühnel、Spivak、do Carmo、Pressley 等商业书籍没有因被推荐而获得 OCW 许可。本次没有取得这些书籍。

## 权利核查与旧记录的必要更正

[OCW 现行条款](https://ocw.mit.edu/pages/privacy-and-terms-of-use/) 给出 CC BY-NC-SA 4.0：须保留作者与来源、注明翻译改编、非商业使用及同许可。署名只能说明来源，不能构成 MIT 认可或背书。外链书籍或其他网站不自动继承此许可。

关键证据是 MIT 官方 FAQ [How is “all rights reserved” content different from the rest of OCW content?](https://mitocw.zendesk.com/hc/en-us/articles/4414756181403-How-is-all-rights-reserved-content-different-from-the-rest-of-OCW-content)，更新于 2025-06-23：标有 “Courtesy of (copyright owner). Used with permission.” 的第三方素材可以在 OCW CC 许可内，改编或再分发须带全该特殊署名；标有 “All rights reserved” 的内容则不在 CC 许可内。后者不能仅凭课程开放就收入本项目。

因此现有 `research/source-manifest.json` 将 Notes A 排除的理由“Used with permission; no separate downstream redistribution permission inferred”与上述官方解释不符。可因本次范围不使用逻辑基础、或尚未逐页核查而不选 Notes A；**不得继续把 Used with permission 本身等同于限制下游重用**。源、署名、许可说明及覆盖记录应同步更正这个解释。本审核仅提出修订，不越界修改现有账。

Notes K 末段有 “This example is adapted from [Wd].” 的来源提示。该提示本身不是 “All rights reserved” 声明，不足以据此断言整份笔记受限；但如重用该例，应保持其出处并单独核查。当前基础主线不需要该例，可以保持不改编的选择。七份 18.900 实取讲义的可提取正文没有发现第三方版权例外；lec31 的一句 “permission” 是关于读者可以跳过置换证明的教学语句，不是版权许可。

权利结论的边界：本次检查官方资源说明、许可链接及可提取文字，没有声称对这些来源 PDF 的每一幅图都完成独立视觉权利核查。最终归档所采用的具体文件仍需由来源清单逐页记录；发现明确受限页或图时不得擅自再分发。

## 必须修复或补齐的数学问题

| 官方来源定位 | 问题 | 修订要求 |
|---|---|---|
| 18.900 lec30，印刷 p225，式 (30.4) | 同式写 `n₀−n₁−n₂` 却算 `5−7+2` | 正确为 `χ=n₀−n₁+n₂` |
| 18.900 lec30，印刷 p226，Corollary 30.5 后 | `b₁=χ−b₀−b₂=χ−b₀` 符号错误 | 正确为 `b₁=b₀+b₂−χ`；平面复形为 `b₀−χ` |
| 18.900 lec30，印刷 p227，Vietoris–Rips 定义 | 固定尺度 `σ`，边条件却写 `<δ` | 统一尺度符号；说明这里只取二维骨架，不能据其 `b₂` 声称完整 Rips 复形的二阶同调 |
| 18.900 lec31，印刷 p234，Proposition 31.5 | 可定向曲面的 `ker D₂` 恰一维及反向条件略去证明 | 用相邻三角形系数传播和三角形邻接图连通补全；保留“有限、连通、闭、无边界”的曲面条件 |
| 18.900 lec31 的 Betti 数结论 | 不可定向闭连通曲面 `b₂=0` 是实数系数情形 | 明确边界矩阵在实数域取秩；在 `F₂` 上不可定向曲面也有一维顶同调，不能混用 |
| 18.900 lec31，印刷 p235，置换证明文字 | 将 `sign(r)` 说成偶度顶点数 | 应为 `(-1)^(偶度顶点数)`；将配图蕴含的复合关系用明确旗标/侧定义说明 |
| 18.900 lec32，印刷 p239，允许改变起点 | 组合环路定义采用自由同伦 | 与保持基点的基本群区别开；不能直接把允许移动起点的关系当基本群等价关系 |
| 18.904 Lecture Summaries，Ses6 | 对一般同伦直接写 `f*=g*`，省略基点约束 | 对保持基点同伦才直接相等；移动基点须由基点轨迹的换基点同构说明相容性 |
| 覆盖与普遍覆盖的编者补充 | 课程安排只说“构造/验证”，未给本册可照搬的完整证明及全部假设 | 路径提升写清起始纤维点；提升判据要求适当的路径连通/局部路径连通条件；普遍覆盖存在及分类需半局部单连通等条件 |
| 曲面分类及 `S²` 单连通的编者补充 | 选定原讲义没有给出当前册所需的一套完整证明 | 若列作本册核心定理必须补全；不能凭“任意环路总避开一点”证明 `S²` 单连通，任意连续环路可能满射 |

以上是原资料抽核发现与编写约束，不表示已审过修订版所有新增证明。最终中文正文仍需独立数学交叉审稿。

## 编者补充与未覆盖内容的写法

建议在一般拓扑扩充章说明：“本章按照 MIT OCW 18.901 Fall 2004 的课程安排补充一般理论；除逐项注明的公开补充笔记外，定义、证明、例题与题解由编者编写。Munkres 商业教材未归档。”

在基本群与覆盖章说明：“范围参考 Andrew Snowden 的 MIT OCW 18.904 Spring 2011 Lecture Summaries；该网页提供教学任务与参考位置，并非完整证明笔记。本章证明与配套解答为编者补充。”如实际借鉴 Hatcher 的具体表达、图或成段证明，不能只换成“编者补充”就抹掉该来源，应另行核查授权；本次未归档 Hatcher/Massey。

在组合曲面章署名：“Paul Seidel，18.900 Geometry and Topology in the Plane，Spring 2023，MIT OpenCourseWare，公开讲义 lec28–33；相关几何补充使用公开 lec40（当学期课堂省略）。中文翻译、重排、勘误与补全由编者完成，CC BY-NC-SA 4.0。”仅为原文略证所补的论证，应注明补全而不是称官方完整证明。

当前册不据此宣称覆盖：18.901 的 Stone–Čech、一般维数理论和全部可度量化理论；18.905 的完整奇异同调、上同调及 Poincaré 对偶；完整闭曲面分类（除非新增完整证明）；18.900 的台球、谱问题、Arnold 不变量、代数曲线、热带几何与完整双曲/曲率理论；18.950 的完整微分几何；18.965 的研究生微分拓扑。实际成书的覆盖说明以最终逐章来源表为准。

审核状态：来源与范围审核完成；已将关键范围、许可纠正和原稿勘误回报主代理。没有上传阻塞；本审核没有执行交付 PDF、源码 ZIP、远端验证或整册逐页视觉审核，不为这些项目作完成声明。

## 当前实际归档复核：新增 14 PDF、77 物理页

复核日期仍为 2026-10-08 UTC。本节追加的是主代理随后实际写入 `sources/` 的归档结论，不能与前文为范围调查而实取的文件混算。复核时总清单 `research/source-manifest.json` 的 SHA256 为 `798e06f062b3db297ae950c2b6e9edf88484af3e4a276feea953e48c8cad9adc`，其记录获取时间为 `2026-10-08T05:30:17.321182+00:00`。本审核仍只写本报告，不修改来源或清单，不做 PDF 视觉审查。

### 文件完整性与清单对应

已独立从磁盘读出并计算总清单内全部 **160 条文件**的字节数和 SHA256，全部匹配；160 个路径无重复。8 份课程 `SOURCE.json` 共列 157 条记录，逐条与总清单一致；另外 3 条为许可法律文本、FAQ HTML 及其提取文本。磁盘中实际存在的 27 个来源 PDF 恰与总清单 PDF 路径集合相同，没有遗漏项或未登记 PDF。

已用 `pdfinfo` 复核全部 27 个来源 PDF 的物理页数、Author 和 Title：与总清单一致。作者或标题元数据空缺的扫描原件，清单保持空缺，没有替它们虚造元数据。署名需另以官方课程页及 PDF 正文为依据。

已通过官方 HTTPS URL **重新取得新增 14 个 PDF**，逐一计算字节数和 SHA256；14/14 与本地原件及两级清单完全一致。新增文件合计 **4,354,648 字节、77 物理页**。原有 13 PDF、67 物理页仍完整保留，因此本册来源归档当前合计 **27 PDF、144 物理页**。总清单中另有 **92 份取得自远端的来源文件及 68 份本地提取文本**；这些数字不是讲义 PDF 数。

### 本次真正新增的 14 份 PDF

下面页数、字节数和完整 SHA256 均经过上述独立磁盘及官方原件双重核验。路径相对于 `subjects/topology/`。没有将前文调查过、实际未归档的 18.900 lec28/32、18.905 lec30 或 18.950 ch1–3 计入。

| 当前归档路径 | 实际题名 | 物理页 | 字节 | SHA256 |
|---|---|---:|---:|---|
| `sources/18.901-fall2004/pdf/notes_g.pdf` | Normality of Quotient Spaces | 9 | 527120 | `be8e6ed2755cd5d741a830faa06c7f9092d2b6e39fd17e606ea2967f8a58bb72` |
| `sources/18.905-fall2016/pdf/mit18_905f16_lec5.pdf` | Homotopy, Star-shaped Regions | 5 | 423621 | `93ebdff23f26213525461c0c8748c7ab878406b7216e1a694df8b13b9c54f901` |
| `sources/18.905-fall2016/pdf/mit18_905f16_lec14.pdf` | CW-Complexes | 5 | 420221 | `f66e90131b531bc6015d6199551f98a52be46432672b55009d9242efba2f8478` |
| `sources/18.905-fall2016/pdf/mit18_905f16_lec18.pdf` | Euler Characteristic and Homology Approximation | 5 | 442084 | `38728d5c0c5d5bff8f40f54e2cf4f7f9f12f4528803cac21875f56c58afed484` |
| `sources/18.900-spring2023/pdf/mit18_900s23_lec4_pdf.pdf` | The Winding Number (continued) | 5 | 396016 | `d8a4be647c2eee13deeaef9e4759a772daf368a1e248379d9fbaf5c0c2afa57e` |
| `sources/18.900-spring2023/pdf/mit18_900s23_lec29_pdf.pdf` | Betti Numbers | 5 | 285230 | `7743654402c859242156cd9fe53f8de2d16121c96295f7dfa68a9ad86e3e2c55` |
| `sources/18.900-spring2023/pdf/mit18_900s23_lec30_pdf.pdf` | Betti Numbers (continued) | 5 | 304579 | `00fcb374381a4cd1de54b59239a494e2bd577164155b1226ed1c570c167d3972` |
| `sources/18.900-spring2023/pdf/mit18_900s23_lec31_pdf.pdf` | Surfaces | 5 | 335790 | `cd4dcbbfcbddd1c428070fcee3042a965317d18f3bb72d7846b09d4f3e2c2f86` |
| `sources/18.900-spring2023/pdf/mit18_900s23_lec33_pdf.pdf` | Combinatorial Winding Numbers and the Boundary Operators | 5 | 391326 | `8fee491ead6faa829ba45c890afe81adfb791dd7f6f016c5018658ee98b3a9ee` |
| `sources/18.900-spring2023/pdf/mit18_900s23_lec40_pdf.pdf` | Geometry of Combinatorial Surfaces | 5 | 356711 | `e70b8914645ae59f0152b92b155d2eaaaa1e37f17410e11d93566cffd9db8245` |
| `sources/18.965-fall2004/pdf/lecture1.pdf` | Manifolds: Definitions and Examples | 4 | 89818 | `5a6433da86a8d5d5c4031b79d5b2ef5ae5f15b7a05bc0b4e3ce1c68761ec5920` |
| `sources/18.965-fall2004/pdf/lecture2.pdf` | Smooth Maps and the Notion of Equivalence | 2 | 63494 | `894fb86d9ead48f10ad6b80874da32367da672b0b4897ee8cb3cc7b2679f874d` |
| `sources/18.965-fall2004/pdf/lecture4.pdf` | Inverse and Implicit Function Theorems | 4 | 82046 | `2561c0859ab342abcbc011b5e74191a79c3bfcdfd04f1b5d3b27375eb6d8d4d8` |
| `sources/18.950-fall2008/pdf/ch4_revised.pdf` | Geometry of Lengths and Distances | 13 | 236592 | `f7af9abd1fcacf69972c21dfedd6201b63696929da64f9c17f4579c061c2b8a9` |

新增项按课程汇总为：18.901 1 PDF/9 页；18.905 3 PDF/15 页；18.900 6 PDF/30 页；18.965 3 PDF/10 页；18.950 1 PDF/13 页。当前 18.901 全部归档为 C、D、G、K，共 4 PDF/19 页。来源归档不自动等于中文正文完整采用或翻译；具体采用范围仍须由最终逐章覆盖表说明。

14 份新增 PDF 的可提取全文中均未发现 `All rights reserved`、另行版权保留或受限第三方署名标记。该结论限于文字和官方资源说明；按此次任务约束没有做各页图像审查，不能据此声称图像权利已逐页核完。对于 18.900 lec40，“Spring 2023 课堂省略，但讲义正式公开”的说明仍须保留。

### 署名、许可及 18.904 的四个网页

14 个文件级记录均含 `CC-BY-NC-SA-4.0` 与其正式许可 URL。18.900/18.950 的 Paul Seidel、18.965 的 Tomasz S. Mrowka、18.905 的 Haynes Miller / Sanath Devalapurkar / Xianglong Ni 与官方课程及讲义说明相符。18.901 G 的署名明确区分 James Munkres 是授课者、扫描 PDF 无作者元数据；没有把缺失元数据伪报为 PDF 已登记作者。18.965 lecture1 正文第一页直接署 Tomasz S. Mrowka，可用于同课程其他讲义的署名依据；各文件记录的空 Author/Title 与原件相符。

18.904 确实只新增 **4 HTML 快照及 4 份提取文本，0 PDF**。已重新取得四个官方网页，原始 HTML 的字节数及完整 SHA256 均与本地及清单一致：

| 当前归档网页 | 字节 | SHA256 |
|---|---:|---|
| `sources/18.904-spring2011/html/revision-course-home.html` | 49893 | `c1a20e9c4191064081671bdbd0c5c9bcc1dc24e4847b757a23dcf26d3a0b3dd2` |
| `sources/18.904-spring2011/html/revision-syllabus.html` | 59086 | `0b27519efb2454376850ce37d490cad777b1d2395ebd0a36897cec7c96f3baa7` |
| `sources/18.904-spring2011/html/lecture-summaries.html` | 74793 | `40f8f023899933f1371270367ca60d7d1f13fdb7df56b6f658f65a6c408949f6` |
| `sources/18.904-spring2011/html/teaching-notes.html` | 57858 | `9512e77fac4de592ebd36dae3bed920c46a8d41e3a75e210cd973e7542b42368` |

Andrew Snowden 的署名正确，文件级许可与课程页 CC 链接相符。四网页提供课程安排、授课任务及教学观察，不能在书前、归档统计或参考文献中冒称“4 份完整代数拓扑讲义”。本册基本群、覆盖与 van Kampen 的完整论证仍按编者补充署名。

已重新取得 MIT 官方第三方 FAQ，确认本地 `sources/licenses/ocw-third-party-faq.html` 为 **29503 字节**、SHA256 **`36213728fd41217030c5d4b4d524825377a2f82b87c9fdec1166935b936bc8ed`**，与官方当前原始字节完全一致。其本地提取文本 **3340 字节**、SHA256 **`e0d9c138a526a7cd8e0014e4ef5e7499e7dd10a784e08406d4b3ca5e2bc76a90`** 亦与清单一致。两份包含前文所引的特殊署名与 All rights reserved 区别，旧 Used with permission 排除理由应据此纠正。

### 需随主稿更新的元数据

在本次复核快照中，`sources/18.901-fall2004/SOURCE.json` 的旧 `scope` 仍写 selected C、D、K，未加入新增 G，应更新为 C、D、G、K；这不影响已核完的具体文件记录、字节、哈希和数量。旧 `sources/ATTRIBUTION.md` 也仍写只归档 C、D、K，并保留前文指出的 Used with permission 误判，需与书前和总清单一起改正。

新建课程 `SOURCE.json` 顶层目前用如 `18.905-fall2016` 的课程目录名，未单列完整课程题名、`term`、`license_url` 和获取时间；文件级已有明确许可及官方 URL，课程网页快照也保留作者学期，尚未产生署名错误。为让脱离目录阅读 `SOURCE.json` 的读者也能直接复用署名，建议补齐这些顶层字段。

本次归档复核结论：**14/14 新 PDF 官方原件字节验证通过；27/27 来源 PDF 页数与元数据验证通过；160/160 清单文件本地完整性验证通过；4/4 18.904 HTML 及 FAQ 官方原始字节验证通过。** 仍待上述文字范围及许可解释同步更新；不包含 PDF 图像权利、中文数学证明、源码 ZIP、成书视觉或 GitHub 远端交付的完成认证。

## 归档说明修订的简短复核

2026-10-08 后续复核：18.901 的 `scope` 已准确改为 C、D、G、K；新课程 `SOURCE.json` 的完整 `course_name`、`term`、`license_url` 均正确，作者角色与前次已核官方证据相符。总清单、`ATTRIBUTION.md`、原覆盖表和书前的 Used with permission 解释已经修正，符合已归档的 MIT 官方 FAQ；Notes A 的未采用原因不再误称许可禁止。归档数仍为新增 14 PDF/77 物理页、总 27 PDF/144 物理页，18.904 为四个 HTML 而非四份 PDF。这些修订通过。

新 `research/revision-source-coverage.md` 有以下来源对应和页角色需订正，已即时通知主代理；此处只查来源说明，不扩大至正文证明审稿：

- **18.901 Notes G** 的实际题名为 *Normality of Quotient Spaces*，9 页涉及商空间正常性、粘合、相干拓扑及胞腔式构造，没有名为 *Products* 的积拓扑通论。覆盖表将其写作 Products 及据它指认各种积、积紧性，`ATTRIBUTION.md` 将题名写作 Products，均需改正。积拓扑、超滤子和 Tychonoff 的自足论证如由编者写成，应继续明确为编者补充，不能借这个错误题名归因。
- **18.900 lec4** 的实际题名为 *The Winding Number (continued)*，正文印刷页 30–33 讲多边形环路绕数、射线带符号交点计数及简单自交环路的区域数。覆盖表和署名用途应写绕数及其平面应用，不能将该讲直接列作一般有限图 Euler 数或自由群证明来源。
- **18.900 lec29** 的实际题名为 *Betti Numbers*，正文印刷页 219–222 讲平面复形、Euler 数、边界矩阵与 Betti 数；“曲面与有限三角剖分”的定位应改为上述实际内容。组合曲面和顶点 link 条件来自 lec31，实际归档中已包含 lec31，宜准确对应。
- **18.950 ch4** 的 13 个物理页角色应细分为 PDF p1 的 OCW 来源页、p2 的章节扉页、p3–13 共 11 页数学正文。Lecture 36 位于 PDF p3、Lecture 39 位于 p8 的定位准确。“12 正文页及 1 来源页”若把章扉也归入正文，须说明这一口径；作为逐页内容核查宜直接列出三种角色。

结论：数量、署名、课程学期、文件级许可及旧许可误判修订通过；上列四项来源题名/采用内容/页面角色说明尚待修正。没有重做原件哈希核验，没有 PDF 视觉审查，也未写入本报告以外文件。

## 当前四项来源说明：修订已完成

2026-10-08 再次只读复核当前 `sources/ATTRIBUTION.md` 与 `research/revision-source-coverage.md` 的上述四项。Notes G 已准确写为 *Normality of Quotient Spaces*，区分商空间分离性参照与积、Tychonoff 的编者补充；18.900 lec4 已写为多边形绕数及其应用，lec29 已写为平面复形、Euler 数和边界矩阵，并把组合曲面条件对应 lec31；18.950 ch4 已准确细分为 1 OCW 来源页、1 章扉和 11 数学正文页，L36/p3、L39/p8 的定位保留正确。四项在两个文件中的写法均已修订，通过本次核查。

绑定本次复核的文件 SHA256：

- `sources/ATTRIBUTION.md`：`40cd3e4a69c7eb2790f3db04bc0e09e83218032c2c627cb71810267e1b264fe5`。
- `research/revision-source-coverage.md`：`8f8344f22ca1b3a6035674b50303f024672870df080b9a00c5dbb3cbe3ccb4fd`。

**当前最终状态：前述四项来源对应及页面角色问题均已解决，无待修订项。** 前节的误配发现和“尚待修正”仅保留为当时快照及修订历史，不是当前状态。本次只核这四项及两文件 SHA，不扩大至正文、原件复取或 PDF 视觉审查；没有修改任何来源文件。
