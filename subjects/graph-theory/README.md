# 图论：结构、染色与网络算法

[中文整册 PDF](dist/main.pdf) · [自足中文源码 ZIP](dist/source.zip) · [逐文件来源清单](source-manifest.json) · [英文出处档案](../../sources/graph-theory/)

以 MIT **18.315 Spring 2005** 专门图论课程为主源，Igor Pak 授课、Amanda Redlich 记录；结合指定的 18.433 Fall 2003、18.212 Spring 2019、18.217 Fall 2019 和 6.042J Spring 2015 内容，重编为一册完整简体中文讲义。56个PDF物理页（前置5页、正文及参考文献51页）；17章数学正文，加来源对应附录与参考文献。全文原生 LaTeX，定义、定理、证明、例题及题解均为中文；没有嵌入英文原页或位图截图。

主线包括图与度数、树和 Prüfer 编码、连通度和 Menger、Euler 与 Hamilton、匹配与 Hall/Kőnig/Tutte、顶点染色与 Brooks、边染色与 Vizing、平面图、染色及 Tutte 多项式、搜索与最短路、最小生成树与随机收缩、网络流、矩阵树与 BEST、电网络与随机游走、谱扩张与 Cheeger、极值图论、Ramsey 和概率方法、偏序。正文有完整一般证明、经典例题、34道配套练习及解答；按数学依赖合并重复内容。

“完整”指本册声明的学习主线，**不是整门组合课程或全部研究级图论的逐讲全译**。四色、Kuratowski 与四连通平面图 Hamilton 定理只明确提及；不含花算法、费用流、Gallai–Milgram、一般群 Hamilton 构造、图极限、Ramanujan 图、研究级稀疏正则性及加法组合。6.042 的逻辑、一般计数和概率没有抄入图论。逐项采用、补证与省略见 PDF 来源附录和原件 [SOURCE_MAP.md](../../sources/graph-theory/SOURCE_MAP.md)。

英文原件仅位于 `sources/graph-theory/`：34份PDF共1062页，逐文件核作者、授课年、物理页数、许可和SHA-256。原件保持许可与内容完整，不作为中文阅读交付。18.225 Fall 2023 的344页作者书稿因独立作者版权和图片许可说明仅登记链接，没有打包正文或图片。扫描手写记录的 OCR 只作检索，数学解释以原图为依据。

## 从源码重编

ZIP 解压后进入 `graph-theory/`：

```bash
bash build.sh
```

需要 XeLaTeX、ctex/xeCJK、Fandol、Computer Modern Unicode 的 `cmunrm/cmunbx/cmunti/cmunbi` 字体，以及 TikZ、booktabs、longtable 等标准宏包。锁定类完整内置于 `main.tex`，与既有概率册的王者模板逐字一致；不需其他学科或源PDF。字体、英文原件、渲染页、构建缓存、阶段PDF均不放入源码ZIP。

缺少中文资源或模板字体时，可以运行包内固定哈希的本地依赖脚本；它只安装到指定目录，不改系统，也不更换版式：

```bash
python3 tools/bootstrap_tex.py --texmf-dir /tmp/graph-texmf --cache-dir /tmp/graph-tex-downloads
TEXMFHOME=/tmp/graph-texmf XDG_CACHE_HOME=/tmp/graph-font-cache bash build.sh
```

构建关闭 shell escape，固定版本时间，运行三轮以收敛目录和引用。`qa/clean-rebuild.json` 是正式ZIP全新解压后的真实重编记录；`qa/package-manifest.json` 给每个包成员哈希。这两份记录及产物自身不嵌入ZIP，以免自指。

## 验收与边界

五份独立数学审稿覆盖全部17章，困难证明返修后重读并绑定最终文件哈希；复算脚本与精确或数值有限检验另存。实际逐页视觉记录、自动排版结果、目录与书签目标核查、中文原生正文核查分别保存于 `qa/`。自动检查和有限实例计算不代替一般证明；独立代理模型审读不冒称人类专家审定。

署名、改编及许可见 [LICENSE.md](LICENSE.md)。原件保持原有许可，中文改编为 CC BY-NC-SA 4.0。所有图形为本稿原生 TikZ；没有复制商业教材图片、受限题面或课网首页照片。本册由 MIT 课程材料重构，并不表示 MIT 或原作者认可本项目。
