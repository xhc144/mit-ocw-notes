# 常微分方程与动力系统

完整简体中文原生 LaTeX 讲义，共38个 PDF 页面（4页前置部分、34页正文），含13章数学内容、来源覆盖章及参考文献。沿用 `subjects/probability/main.tex` 的锁定王者模板，包含29个例题和26道自设习题及解答。

- [完整 PDF](ordinary-differential-equations.pdf)
- [自足源码 ZIP](ordinary-differential-equations-source.zip)：含正文、真实模板、构建工具、审阅记录及60份原件。
- [逐文件来源清单](source-manifest.json)与[原件归档说明](../../sources/ordinary-differential-equations/README.md)
- [前六章数学复核](review/independent-early.md)、[后七章数学复核](review/independent-late.md)
- [逐页视觉记录](review/visual-review.json)、[目录及链接检查](review/pdf-audit.json)、[ZIP 重编证据](review/zip-rebuild.json)、[成品校验值](review/artifact-checksums.json)

主源为 Haynes Miller、Arthur Mattuck 的 MIT 18.03 Differential Equations（Spring 2010），动力系统补充采用 Daniel H. Rothman 的 12.006J Nonlinear Dynamics: Chaos（Fall 2022）。另署名 Jeremy Orloff 的差分与 Z 变换补充。课程年份与原写作年份分开记录，以官方目录、原件署名和实际正文为准。

内容覆盖局部存在唯一性、最大延续与连续依赖、一阶解析方法、高阶线性方程、强迫振动、Laplace 与 Fourier 响应、线性系统、相图、稳定性、Lyapunov 与 LaSalle、极限环、级数与边值问题、Lorenz 模型和离散动力学。补充 Riccati、SIR 阈值与最终规模、非线性单摆周期、Van der Pol 及边值共振例子。来源顺序经过重组，例题合并或另设；不宣称逐讲逐句翻译全部课程。

Hartman–Grobman、Poincaré–Bendixson 和所用 Liénard 定理版本明确为引用工具；一般 Hopf、稳定流形、全局混沌证明、流体 PDE、分形测度、一般平均法与奇异摄动不在本册已完成的证明范围。数值 ODE 算法沿用数值分析册，本册只补理论衔接。不能据此断言常微分方程是2027年考纲独立新增科目。

## 重编

需要 Python 3.11+、XeLaTeX、常规 TeX Live 宏包（PGF/TikZ、hyperref、booktabs、longtable 等）及模板校验脚本的 Python 依赖。ZIP 解压目录中的 `originals/` 已含全部归档原件，重编正文无须下载任何课程材料。

```bash
python -m pip install -r vendor/math-latex-typesetting/requirements.txt
python tools/bootstrap_tex.py --texmf-dir .runtime/texmf --cache-dir .runtime/downloads
TEXMFHOME="$PWD/.runtime/texmf" bash tools/build.sh
python tools/verify_sources.py
```

已有 Fandol 与 CM Unicode 的环境可设置相应 `TEXMFHOME`，直接执行构建。字体不随 ZIP 分发；引导脚本下载固定版本并验证哈希。构建生成 `build/` 中间文件及根目录 PDF，自动检查与人工审阅记录各自陈述实际范围。

`investigate_sources.py` 和 `finalize_sources.py` 是本次仓库来源调查脚本，需仓库目录与调查缓存；不属于 ZIP 内离线重编的依赖。源码 ZIP 排除这些调查脚本、临时调查表、渲染图片、运行缓存和已生成 PDF。

## 署名与许可

原件及本中文改编适用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)，以 [MIT OCW 条款](https://ocw.mit.edu/pages/privacy-and-terms-of-use/)及单件权利例外为准。中文进行了翻译、依赖重排、证明补充、新设题目和独立 TikZ 构图；原作者和 MIT 未为此版本背书。12份动力系统文件存在第三方图片例外，整份仅保留链接，未收入原件目录或 ZIP。详见 [许可声明](LICENSE.md)。
