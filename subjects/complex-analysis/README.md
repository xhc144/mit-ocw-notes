# 复变函数与应用

完整简体中文讲义，共 124 页、20 章，含课程说明及完整官方日历。原 14 章数学正文及 38 道自设习题保持已交付版本，按 MIT 18.04 Spring 2018 的 13 个专题重编，补入选定的 18.112 Fall 2008 材料；采用已交付概率论讲义相同的锁定王者模板。定义、定理条件、证明与例题完整。新增章节逐题收录 18.04 全部公开作业、习题课及模拟卷，并收录 18.112 页面提供的三份 2006 年历史试卷，中文题面与完整解答配对。

- [完整 PDF](complex-analysis.pdf)
- [可编辑源码 ZIP](complex-analysis-source.zip)：仅含49个实际TeX输入文件、原生TikZ图、真实模板、必要构建工具及简短许可/来源说明。97份英文原PDF（578页）、9份官方页面快照及审稿档案保留在仓库，不打入源码包，也不是编译依赖。
- [原件归档](../../sources/complex-analysis/README.md)与[原讲义清单](source-manifest.json)、[新增题卷清单](assessment-manifest.json)
- [数学审查总表](qa/mathematical-review.md)、[逐页视觉审查](qa/visual-review.json)、[链接与文本检查](qa/pdf-audit.json)、[源码重编证据](qa/zip-rebuild.json)

正文覆盖复数与分支、全纯性、复积分、Cauchy 理论、Taylor/Laurent 级数、奇点与留数、轮廓积分、辐角原理、调和函数、复势、保角映射、Laplace/Fourier 应用、解析延拓及 Gamma 函数；选用拓展含一般 Cauchy 定理、Schwarz、Montel、Hurwitz 和 Riemann 映射的完整证明。相似计算例合并，编者补证与自设习题均明确标识，不宣称逐句复刻全部例题。

大 Picard 定理仅保留原课引用式陈述，后文不依赖；Stirling 公式证明限正实轴。18.112 的一般 Mittag–Leffler、素数定理、zeta 延拓与函数方程等仅归档，未编入本册。本次新增 9 次作业（74 大题、179 印刷小项）、12 次公开习题课（44 大题、84 印刷小项，含 1 个阅读任务）及 6 份试卷（42 大题、98 印刷小项）。共 160 大题、361 印刷小项；重复题保留原编号并注明，数学修订与官方缺省条件由独立审稿逐项登记。第 10 次习题课没有公开文件，未虚补。

18.112 的 6 份作业文件实为 Ahlfors 教材习题的 MIT 解答，原题未公开；24 项书页、题号及解答页码在第 19 章准确登记，官方解答原件归档，未推测教材题面。外部教材与 MATLAB 教程未归档。历史考试的实际年份依据题面为 2006，未标作 2008。详见 PDF「来源与覆盖」及三个独立题号库存。

## 重编

需要 XeLaTeX、常规 TeX Live 宏包（含 PGF/TikZ、hyperref、booktabs），Python 3.11+、PyMuPDF 与 Pillow。中文 Fandol 和固定模板所需 CM Unicode 字体可由校验固定哈希的 `tools/bootstrap_tex.py` 安装到本项目运行目录，不打包系统字体。

```bash
python -m pip install -r vendor/math-latex-typesetting/requirements.txt
python tools/bootstrap_tex.py --texmf-dir .runtime/texmf --cache-dir .runtime/downloads
TEXMFHOME="$PWD/.runtime/texmf" bash tools/build.sh
```

若已有可用的中文 TeX/字体环境，设置对应 `TEXMFHOME` 后运行构建即可。脚本从 `main.tex` 生成适配类，再运行三轮或收敛后的 XeLaTeX、引用与溢出检查及逐页渲染；自动通过不代表人工审稿完成。构建输出在 `build/`，不进入干净源码 ZIP。

源码包使用独立的[简短重编说明](SOURCE-PACKAGE.md)和[来源署名](SOURCES.md)。在完整仓库中可另行运行 `python tools/verify_sources.py` 校验英文档案；这项归档检查不属于源码包编译步骤。

## 署名与许可

原主课：Jeremy Orloff，MIT OpenCourseWare，18.04 Complex Variables with Applications，Spring 2018；课程改编自 André Nachbin，Jörn Dunkel 提供修正。拓展：Sigurdur Helgason；lecture notes prepared by Zuoqin Wang，18.112 Functions of a Complex Variable，Fall 2008。习题课原署名 Vishesh Jain；历史考试文件没有署名者时不猜测作者。原文中的其他论证来源保留在原 PDF。

中文为翻译、按依赖重排、补证及新增练习的改编，原机构不为此版本背书。原件及本中文改编按 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 使用；[MIT OCW 条款](https://ocw.mit.edu/pages/privacy-and-terms-of-use/)与个别权利声明优先。逐页核查未发现所选原 PDF 的另行受限页或图。模板及工具保持各自随附声明。
