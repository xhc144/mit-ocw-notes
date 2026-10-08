# 图论：结构、染色与网络算法

[中文整册 PDF](dist/main.pdf) · [自足中文源码 ZIP](dist/source.zip) · [逐文件来源清单](source-manifest.json) · [英文出处档案](../../sources/graph-theory/)

以 MIT **18.315 Spring 2005** 专门图论课程为主源，Igor Pak 授课、Amanda Redlich 记录；结合指定的 18.433 Fall 2003、18.212 Spring 2019、18.217 Fall 2019 和 6.042J Spring 2015 内容，重编为一册完整简体中文讲义。157 个 PDF 物理页（前置 12 页、正文及参考文献 145 页）；17 章数学正文，新增官方评测题与中文解答一章，以及来源对应附录与参考文献。卷首列明五门官方课程的教师、学期、课时、先修、考核和 166 个课历位置。全文原生 LaTeX，定义、定理、证明、例题及题解均为中文；没有嵌入英文原页或位图截图。

主线包括图与度数、树和 Prüfer 编码、连通度和 Menger、Euler 与 Hamilton、匹配与 Hall/Kőnig/Tutte、顶点染色与 Brooks、边染色与 Vizing、平面图、染色及 Tutte 多项式、搜索与最短路、最小生成树与随机收缩、网络流、矩阵树与 BEST、电网络与随机游走、谱扩张与 Cheeger、极值图论、Ramsey 和概率方法、偏序。前 17 章有完整一般证明、经典例题、34 道编者配套练习及解答；第 18 章保留 127 个官方 PDF 原题位置、256 个一级回答单元（展开正式嵌套后为 258 个末端小问），另有 36 个公开在线页面的 75 个 Q。题面和解答均完整编入同册，保留题号、来源与官方答案有无，明确区分原材料和编者独立推导；重复题映射保留。完成绑定见 [assessment-completion.json](assessment-completion.json)，冻结题号见 [assessment-selection.json](assessment-selection.json)。

“完整”指本册声明的学习主线，**不是整门组合课程或全部研究级图论的逐讲全译**。前 17 章保持既有范围；第 18 章补入 Whitney 型平面三角剖分 Hamilton 构造、平面图自足五页书嵌入、匹配分阶段算法、最小返流费用界、树与停车函数、Erdős–Stone–Simonovits、Grothendieck 型有限维旋转构造及 Alon–Boppana 型谱题。四色、Kuratowski、一般四连通平面图 Hamilton 定理仍未全面证明；不含一般花算法、Gallai–Milgram、一般群 Hamilton 构造、图极限、Ramanujan 图、研究级稀疏正则性及加法组合。有限精度线性规划的通用多项式算法作为明确列出的背景定理，图上的分离预言机等专门论证完整给出。6.042 的逻辑、一般计数和一般概率章节没有整章抄入；入选图论题依赖的有限概率、随机游走等在解答中说明。逐项采用、补证与省略见 PDF 来源附录和原件 [SOURCE_MAP.md](../../sources/graph-theory/SOURCE_MAP.md)。

英文原件仅位于 `sources/graph-theory/`：讲义原件 34 份 PDF 共 1062 页，新增评测及公开答案 77 份 PDF 共 278 页，合计 111 份 PDF 共 1340 页；逐文件核作者、授课年、物理页数、许可和 SHA-256。在线题面、公开反馈和课程元数据另存。评测原件见 [assessment-source-manifest.json](assessment-source-manifest.json)。原件保持许可与内容完整，不作为中文阅读交付。18.225 Fall 2023 的344页作者书稿因独立作者版权和图片许可说明仅登记链接，没有打包正文或图片。扫描手写记录的 OCR 只作检索，数学解释以原图为依据。

## 从源码重编

ZIP 解压后进入 `graph-theory/`：

```bash
bash build.sh
```

需要 XeLaTeX、ctex/xeCJK、Fandol、Computer Modern Unicode 的 `cmunrm/cmunbx/cmunti/cmunbi` 字体，以及 TikZ、booktabs、longtable 等标准宏包。锁定类完整内置于 `main.tex`，与既有概率册的王者模板逐字一致；不需其他学科或源 PDF。字体、英文原件、渲染页、构建缓存、阶段PDF均不放入源码ZIP。

缺少中文资源或模板字体时，可以运行包内固定哈希的本地依赖脚本；它只安装到指定目录，不改系统，也不更换版式：

```bash
python3 tools/bootstrap_tex.py --texmf-dir /tmp/graph-texmf --cache-dir /tmp/graph-tex-downloads
TEXMFHOME=/tmp/graph-texmf XDG_CACHE_HOME=/tmp/graph-font-cache bash build.sh
```

构建关闭 shell escape，固定版本时间，运行三轮以收敛目录和引用。`qa/clean-rebuild.json` 是正式ZIP全新解压后的真实重编记录；`qa/package-manifest.json` 给每个包成员哈希。这两份记录及产物自身不嵌入ZIP，以免自指。

## 验收与边界

五份原始独立数学审稿覆盖全部 17 章，六组新增独立审稿覆盖全部入选题面、解答与共用引理；另有五门课程元数据交叉核对。困难证明返修后重读并绑定最终文件哈希；复算脚本与精确或数值有限检验另存。实际逐页视觉记录、自动排版结果、目录与书签目标核查、中文原生正文核查分别保存于 `qa/`。自动检查和有限实例计算不代替一般证明；独立代理模型审读不冒称人类专家审定。

署名、改编及许可见 [LICENSE.md](LICENSE.md)。原件保持原有许可，中文改编为 CC BY-NC-SA 4.0。所有书中图形为本稿原生 TikZ 或由源图转写的邻接表、数表；没有复制商业教材图片、受限题面或课网首页照片。本册由 MIT 课程材料重构，并不表示 MIT 或原作者认可本项目。
