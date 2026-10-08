# 测度与积分：MIT 18.125 中文重编本

[整册 PDF](real-analysis.pdf) · [完整源码 ZIP](real-analysis-source.zip) · [原件归档与逐文件来源](../../sources/real-analysis/source-manifest.json)

本册72个PDF物理页（前置4页、正文及来源参考68页），以 MIT OpenCourseWare 的 **18.125 Measure and Integration, Fall 2003** 为主源。Jeff Viaclovsky 讲授，Ethan Brown 根据课堂笔记排录。实际归档24份讲义PDF，共95个物理页。中文正文是原生LaTeX重编，按概念依赖合册；原稿省略的关键证明予以补齐，勘误与新增内容有明确记录。

九章数学内容依次为可测空间与函数、Lebesgue积分及收敛、Lebesgue测度构造、一般局部紧Hausdorff空间的正泛函Riesz表示与正则逼近、Lp空间、欧氏及抽象乘积测度与Tonelli/Fubini、卷积与光滑逼近、最大函数及Lebesgue微分、积分密度与测度分解。另有逐讲来源对照、参考文献、29个例题及33道有完整解答的配套练习；练习为编者新增，并非官方独立作业答案。

第1–8章覆盖这24份文件的主要内容。第9章的Radon–Nikodym与Lebesgue分解是显式编者补充，并完整补证第22讲原稿只陈述的两条逆向微积分基本定理。与泛函分析的交叉限于Lp完备性、积分泛函及本章直接证明的实Hilbert表示引理；未宣称证明完整Lp对偶理论。

课程大纲列出、但24份实际PDF不含的Hausdorff测度、面积与余面积公式尚未译编；课程描述提及的Fourier变换也无对应讲义正文。独立作业和外部教材不在本次归档范围。第24讲只给最大算子的专门插值估计，不冒充一般Marcinkiewicz插值定理。

## 重编

源码ZIP内有完整正文、锁定模板、验证脚本、来源原件及审读记录，无字体、构建缓存或阶段PDF。解压后进入`real-analysis`目录：

```bash
bash tools/build.sh
python3 tools/verify_sources.py
```

需要XeLaTeX、ctex/xeCJK、Fandol和CM Unicode字体，以及Python3和PyMuPDF。`tools/build.sh`默认使用`/workspace/.local/texmf`与`/workspace/.cache`；其他机器可设置`TEXMFHOME`和`XDG_CACHE_HOME`。依赖缺失时，可用仓库已有的固定哈希依赖脚本安装到可写目录：

```bash
python3 tools/bootstrap_tex.py --texmf-dir /tmp/real-analysis-texmf --cache-dir /tmp/real-analysis-tex-cache
TEXMFHOME=/tmp/real-analysis-texmf XDG_CACHE_HOME=/tmp/real-analysis-cache bash tools/build.sh
```

字体仅作为运行依赖，不随ZIP分发。正文复用已交付概率册的锁定王者类，真实模板与数学讲义技能在`vendor/`中；锁定类未重新设计。

## 审读证据

独立数学agent完整审读24份源文件和九章正文，并复查最终修订：[数学审稿](qa/independent-review.md)、[逐讲覆盖与源勘误](qa/source-checklist.md)。最终PDF全部72页分别以130dpi单页图实际打开；记录见`qa/final-visual-*.json`。数学审读、机械编译、链接核查及逐页视觉分别记录，不以自动检查代替数学或视觉结论。本册无嵌入图或TikZ图，因此没有图形标签重叠项。

`qa/clean-rebuild.json`绑定交付源码ZIP与全新解压目录重编结果；`qa/package-manifest.json`列出ZIP中每个成员的字节数及SHA256。`qa/final-checks.json`汇总最终PDF、来源、目录链接及全部逐页审查记录。

## 署名与许可

官方[讲义目录](https://ocw.mit.edu/courses/18-125-measure-and-integration-fall-2003/pages/lecture-notes/)及[MIT OCW使用条款](https://ocw.mit.edu/pages/privacy-and-terms-of-use/)核验于2026-10-08。原件与中文改编遵循[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)，需保留作者及课程署名、非商业使用、相同方式共享；单独声明优先。逐件核对未发现第三方受限页或嵌入图片。课程首页的第三方Lebesgue肖像未下载、未复用。署名不表示MIT或原作者认可本改编。详见[本册许可](LICENSE.md)及[原件署名](../../sources/real-analysis/ATTRIBUTION.md)。
