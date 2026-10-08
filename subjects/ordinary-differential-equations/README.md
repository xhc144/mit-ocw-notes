# 常微分方程与动力系统

完整简体中文原生 LaTeX 讲义，共196个 PDF 页面（13页前置部分、183页正文），含原13章数学内容、完整课程说明与日历、题库、作业、习题课、考试及来源覆盖，共42章和参考文献。沿用 `subjects/probability/main.tex` 的锁定王者模板。

- [完整 PDF](ordinary-differential-equations.pdf)
- [自足源码 ZIP](ordinary-differential-equations-source.zip)：42个文件，仅含中文正文、实际模板、必要构建代码及许可来源。英文原件、网页、审稿记录及研究清单留在仓库。
- [逐文件来源清单](source-manifest.json)、[课程习题来源清单](coursework-source-manifest.json)与[原件归档说明](../../sources/ordinary-differential-equations/README.md)
- [课程题目覆盖总表](research/coursework-coverage.json)、[原章习题复用核对](research/chapter-exercise-reuse.json)
- [逐页视觉记录](review/visual-review.json)、[目录及链接检查](review/pdf-audit.json)、[ZIP 重编证据](review/zip-rebuild.json)、[成品校验值](review/artifact-checksums.json)

主源为 Haynes Miller、Arthur Mattuck 的 MIT 18.03 Differential Equations（Spring 2010），动力系统补充采用 Daniel H. Rothman 的 12.006J Nonlinear Dynamics: Chaos（Fall 2022）。另署名 Jeremy Orloff 的差分与 Z 变换补充。课程年份与原写作年份分开记录，以官方目录、原件署名和实际正文为准。逐文件去重后归档152份 PDF，共920页，新增保存5份课程说明与习题网页（连同既有来源页共10份网页）；12份含第三方图片例外的动力系统文件仅保留链接。

数学主线覆盖局部存在唯一性、最大延续与连续依赖、一阶解析方法、高阶线性方程、强迫振动、Laplace 与 Fourier 响应、线性系统、相图、稳定性、Lyapunov 与 LaSalle、极限环、级数与边值问题、Lorenz 模型和离散动力学。补充 Riccati、SIR 阈值与最终规模、非线性单摆周期、Van der Pol 及边值共振例子。保留原章29个例题、26道自设习题及解答；不宣称逐句翻译全部英文课程。

课程部分纳入原课程介绍、先修要求、安排、评分与日历，以及公开题面和对应中文解答。覆盖数量按原题编号与显式小问统计，不能相加后声称全部为互不重复的新题。

| 类别 | 已核范围 | 小问与边界 |
|---|---|---|
| Notes题库 | 7组、217主问题 | 466个命名末级小问；5B-4另保留条件适用性记录 |
| Problem Sets | 1–9全部公开作业任务 | 前5份159条末级记录，后4份24个问题单元、139小问；包括题库回指与教材位置 |
| Recitations | 22份公开习题课、106主问题 | 147小问；第6、12、20、26次无公开题面，明确记缺 |
| Exams | 3次期中、期末及4份练习卷，53主问题 | 183小问；2010期末解答由编者独立补全 |

总表1094条末级记录包含53条公开题库回指及40条商业教材引用（38个不同位置）。未取得公开题面的 Edwards–Penney 教材题，仅保留原作业要求、精确位置与缺口说明，不编造题面。练习期末链接的2008年答案逐条件与2010题面核对；原答案缺漏、算术或因子错误逐处注明。编者补解与官方答案的来源区别保留在正文中。

原数学章已由[前六章](review/independent-early.md)与[后七章](review/independent-late.md)两个独立会话交叉复核；新增内容由六个独立会话交叉审核：[题库1–3](review/bank01-03-independent-review.md)、[题库4–7](review/bank04-07-independent-review.md)、[作业1–5](review/ps01-05-independent-review.md)、[作业6–9](review/ps06-09-independent-review.md)、[习题课](review/recitations-independent-review.md)、[考试](review/exams-independent-review.md)。这是独立 AI 会话复核，非 MIT 或外部人类审定。

Hartman–Grobman、Poincaré–Bendixson 和所用 Liénard 定理版本明确为引用工具；一般 Hopf、稳定流形、全局混沌证明、流体 PDE、分形测度、一般平均法与奇异摄动不在本册已完成的证明范围。数值 ODE 算法沿用数值分析册，只在实际课程题目中补必要计算与理论衔接。不能据此断言常微分方程是2027年考纲独立新增科目。

## 重编

需要 Python 3.11+、XeLaTeX、常规 TeX Live 宏包及模板校验脚本的 Python 依赖。所有图形在 TeX 中以 TikZ/PGF 独立构造；重编无需下载或嵌入任何课程原件。

```bash
python -m pip install -r vendor/math-latex-typesetting/requirements.txt
python tools/bootstrap_tex.py --texmf-dir .runtime/texmf --cache-dir .runtime/downloads
TEXMFHOME="$PWD/.runtime/texmf" bash tools/build.sh
```

已有 Fandol、CM Unicode 与 ctex 环境时可设置相应 `TEXMFHOME` 后执行构建。字体和外部运行依赖不随包分发；引导脚本下载固定版本并验证哈希。构建生成 `build/` 中间文件及根目录 PDF。自动检查、数学审核与实际逐页视觉检查各自记录真实范围。

仓库内执行 `python tools/verify_sources.py` 核查152份出处原件，执行 `python tools/freeze_coursework.py` 检查来源、原编号、标签及最终数学审稿哈希绑定。源码 ZIP 排除这些调查脚本、英文 PDF、网页、研究及审稿清单、字体、渲染图片、运行缓存和已生成 PDF。

## 署名与许可

原件及本中文改编适用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)，以 [MIT OCW 条款](https://ocw.mit.edu/pages/privacy-and-terms-of-use/)及单件权利例外为准。中文进行了翻译、依赖重排、证明补充、新设题目和独立 TikZ 构图；原作者和 MIT 未为此版本背书。12份动力系统文件存在第三方图片例外，整份仅保留链接，未收入原件目录或 ZIP。详见[许可声明](LICENSE.md)。
