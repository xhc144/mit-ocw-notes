# 复变函数与应用

完整简体中文讲义，14 章数学正文、逐文件来源表及参考文献，共 50 页。按 MIT 18.04 Spring 2018 的 13 个专题重编，补入选定的 18.112 Fall 2008 材料；采用已交付概率论讲义相同的锁定王者模板。定义、定理条件、证明、例题与 38 道自设习题的解答均进入正文。

- [完整 PDF](complex-analysis.pdf)
- [可编辑源码 ZIP](complex-analysis-source.zip)：含 LaTeX、真实模板、构建工具、审查记录及 37 份原讲义。
- [原件归档](../../sources/complex-analysis/README.md)与[逐文件清单](source-manifest.json)
- [独立数学审稿](qa/independent-math-review.md)、[逐页视觉审查](qa/visual-review.json)、[链接与文本检查](qa/pdf-audit.json)、[源码重编证据](qa/zip-rebuild.json)

正文覆盖复数与分支、全纯性、复积分、Cauchy 理论、Taylor/Laurent 级数、奇点与留数、轮廓积分、辐角原理、调和函数、复势、保角映射、Laplace/Fourier 应用、解析延拓及 Gamma 函数；选用拓展含一般 Cauchy 定理、Schwarz、Montel、Hurwitz 和 Riemann 映射的完整证明。相似计算例合并，编者补证与自设习题均明确标识，不宣称逐句复刻全部例题。

大 Picard 定理仅保留原课引用式陈述，后文不依赖；Stirling 公式证明限正实轴。18.112 的一般 Mittag–Leffler、素数定理、zeta 延拓与函数方程等仅归档，未编入本册。独立作业、习题课、考试和外部指定教材未整批收录。详见 PDF「来源与覆盖」。

## 重编

需要 XeLaTeX、常规 TeX Live 宏包（含 PGF/TikZ、hyperref、booktabs），Python 3.11+、PyMuPDF 与 Pillow。中文 Fandol 和固定模板所需 CM Unicode 字体可由校验固定哈希的 `tools/bootstrap_tex.py` 安装到本项目运行目录，不打包系统字体。

```bash
python -m pip install -r vendor/math-latex-typesetting/requirements.txt
python tools/bootstrap_tex.py --texmf-dir .runtime/texmf --cache-dir .runtime/downloads
TEXMFHOME="$PWD/.runtime/texmf" bash tools/build.sh
python tools/verify_sources.py
```

若已有可用的中文 TeX/字体环境，设置对应 `TEXMFHOME` 后运行构建即可。脚本从 `main.tex` 生成适配类，再运行三轮或收敛后的 XeLaTeX、引用与溢出检查及逐页渲染；自动通过不代表人工审稿完成。构建输出在 `build/`，不进入干净源码 ZIP。

## 署名与许可

原主课：Jeremy Orloff，MIT OpenCourseWare，18.04 Complex Variables with Applications，Spring 2018；课程改编自 André Nachbin，Jörn Dunkel 提供修正。拓展：Sigurdur Helgason；lecture notes prepared by Zuoqin Wang，18.112 Functions of a Complex Variable，Fall 2008。原文中的其他论证来源保留在原 PDF。

中文为翻译、按依赖重排、补证及新增练习的改编，原机构不为此版本背书。原件及本中文改编按 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 使用；[MIT OCW 条款](https://ocw.mit.edu/pages/privacy-and-terms-of-use/)与个别权利声明优先。逐页核查未发现所选原 PDF 的另行受限页或图。模板及工具保持各自随附声明。
