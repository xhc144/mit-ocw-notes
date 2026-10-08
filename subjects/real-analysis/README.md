# 测度与积分：MIT 18.125 中文重编本

[整册 PDF](real-analysis.pdf) · [完整源码 ZIP](real-analysis-source.zip) · [原件归档与逐文件来源](../../sources/real-analysis/source-manifest.json)

本册75个PDF物理页（前置7页、正文及来源参考68页），以 MIT OpenCourseWare 的 **18.125 Measure and Integration, Fall 2003** 为主源。Jeff Viaclovsky 讲授，Ethan Brown 根据课堂笔记排录。实际归档24份讲义PDF，共95个物理页。本次复用原72页版的全部数学正文与33道编者练习，仅增补卷首课程参考、官方课历及三组作业安排索引；十个章节源码字节不变，正文68页的文字和字形位置保持一致。

卷首记录官方每周2次课、每次1.5小时，先修Analysis I (18.100)，按到课及提交作业考核、明确无考试。三组Rudin教材题号及截止讲次8、12、20依官方页面译录；**原书题面与官方解答未纳入**，正文33道练习仍为编者题。官方页面仅给教材章号和题号，没有独立完整作业题面或解答下载。

九章数学内容依次为可测空间与函数、Lebesgue积分及收敛、Lebesgue测度构造、一般局部紧Hausdorff空间的正泛函Riesz表示与正则逼近、Lp空间、欧氏及抽象乘积测度与Tonelli/Fubini、卷积与光滑逼近、最大函数及Lebesgue微分、积分密度与测度分解。另有逐讲来源对照、参考文献、29个例题及33道有完整解答的配套练习；练习为编者新增，并非官方独立作业答案。

第1–8章覆盖这24份文件的主要内容。第9章的Radon–Nikodym与Lebesgue分解是显式编者补充，并完整补证第22讲原稿只陈述的两条逆向微积分基本定理。与泛函分析的交叉限于Lp完备性、积分泛函及本章直接证明的实Hilbert表示引理；未宣称证明完整Lp对偶理论。

课程大纲列出、但24份实际PDF不含的Hausdorff测度、面积与余面积公式尚未译编；课程描述提及的Fourier变换也无对应讲义正文。外部教材原题与官方解答不在本次归档范围。第24讲只给最大算子的专门插值估计，不冒充一般Marcinkiewicz插值定理。

## 重编

源码ZIP仅含完整中文编译输入、锁定模板、所需验证及依赖工具、署名许可，无英文原PDF、网页、QA记录、字体或构建缓存。英文原件继续保存在仓库`sources/real-analysis/`。解压后进入`real-analysis`目录：

```bash
bash tools/build.sh
```

需要XeLaTeX、ctex/xeCJK、Fandol和CM Unicode字体，以及Python3和PyMuPDF。`tools/build.sh`默认使用`/workspace/.local/texmf`与`/workspace/.cache`；其他机器可设置`TEXMFHOME`和`XDG_CACHE_HOME`。依赖缺失时，可用仓库已有的固定哈希依赖脚本安装到可写目录：

```bash
python3 tools/bootstrap_tex.py --texmf-dir /tmp/real-analysis-texmf --cache-dir /tmp/real-analysis-tex-cache
TEXMFHOME=/tmp/real-analysis-texmf XDG_CACHE_HOME=/tmp/real-analysis-cache bash tools/build.sh
```

字体仅作为运行依赖，不随ZIP分发。正文复用已交付概率册的锁定王者类，真实模板与数学讲义技能在`vendor/`中；锁定类未重新设计。

## 审读证据

原版独立数学agent完整审读24份源文件和九章正文：[数学审稿](qa/independent-review.md)、[逐讲覆盖与源勘误](qa/source-checklist.md)，保留为原数学正文的历史证据。本次未重写数学，复用证据见[正文保持核验](qa/course-update-preservation.json)，新增课程信息另行独立核实。新版75页的实际视觉记录见`qa/course-update-visual-*.json`。数学审读、机械编译、链接核查及逐页视觉分别记录，不以自动检查代替数学或视觉结论。本册无嵌入图或TikZ图。

`qa/clean-rebuild.json`绑定交付源码ZIP与全新解压目录重编结果；`qa/package-manifest.json`列出ZIP中每个成员的字节数及SHA256。`qa/final-checks.json`汇总最终PDF、来源、目录链接及全部逐页审查记录。

## 署名与许可

官方[讲义目录](https://ocw.mit.edu/courses/18-125-measure-and-integration-fall-2003/pages/lecture-notes/)及[MIT OCW使用条款](https://ocw.mit.edu/pages/privacy-and-terms-of-use/)核验于2026-10-08。原件与中文改编遵循[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)，需保留作者及课程署名、非商业使用、相同方式共享；单独声明优先。逐件核对未发现第三方受限页或嵌入图片。课程首页的第三方Lebesgue肖像未下载、未复用。署名不表示MIT或原作者认可本改编。详见[本册许可](LICENSE.md)及[原件署名](../../sources/real-analysis/ATTRIBUTION.md)。
