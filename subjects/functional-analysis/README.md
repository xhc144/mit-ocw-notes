# 泛函分析

MIT 18.102 *Introduction to Functional Analysis*, Spring 2021 的简体中文重构本。Casey Rodriguez 授课，Andrew Lin 原笔记。以官方 125 页合订本及其 23 讲原 TeX 为主源；Richard Melrose 的 2020 年 176 页讲义仅作指定内容的交叉核对。

- [完整中文 PDF](functional-analysis.pdf)：40 页，12 章正文及来源附录；使用已交付概率论的锁定王者版式。
- [可重编源码 ZIP](functional-analysis-source.zip)：主文件、全部章节、模板与验证工具、来源清单、署名许可和编译说明。
- [逐文件来源清单](source-manifest.json)：实际下载 URL、作者课程年份、字节、SHA-256、PDF 页数及许可核对依据。
- [原讲义归档](../../sources/functional-analysis/README.md)：49 个不同的官方文件；分讲 PDF 与合订本内容重复，不能相加为讲义覆盖页数。

正文按依赖次序展开赋范与 Banach 空间、有界算子与商空间、Hahn–Banach 与对偶、统一有界和开映射/闭图、必要积分与 Lᵖ、Hilbert 正交展开、投影/Riesz/伴随、弱与弱星拓扑、Fourier/Fejér、紧算子、紧自伴谱与 Fredholm、连续非负势的区间 Dirichlet 问题。核心证明、例题与配套习题解答完整写入同一册。可分对偶球的弱星紧性、完备化等补充在正文和来源附录标明；两幅图以 TikZ/PGFPlots 重绘。

测度为先修接口：本册证明所需积分收敛、Riemann–Lebesgue 衔接与 Lᵖ 完备性；外测度构造的全部细节、Vitali 集、乘积测度及 Tonelli–Fubini 的构造证明交由实变科。未覆盖所有原作业与考试、视频转录、一般不可分 Banach–Alaoglu、非自伴 Fredholm 全理论、一般非紧自伴谱测度、无界算子域、Sobolev/分布、迹类与 Schatten 理论。没有把辅助讲义的全部专题计为本册覆盖。

## 重编

需要 XeLaTeX、基础 LaTeX 数学/排版包、CTeX 与 Fandol、CM Unicode OpenType 字体、TikZ/PGFPlots；验证脚本另需 Python 3.11+ 和 PyMuPDF。字体是运行依赖，ZIP 不分发字体。

```bash
python -m pip install -r vendor/math-latex-typesetting/requirements.txt
# 环境缺少中文包/锁定字体时，可在有网络的可写 TEXMF 目录安装经哈希锁定的资源：
python tools/bootstrap_tex.py --texmf-dir /tmp/functional-texmf --cache-dir /tmp/functional-tex-downloads
TEXMFHOME=/tmp/functional-texmf bash tools/compile.sh
```

已有完整 TeX 环境时直接 `bash tools/compile.sh`。输出 `build/main.pdf`；脚本执行固定模板检查及三遍收敛编译。自动报告不替代数学和视觉审查。

## 验收证据

- [前六章独立审稿及修订复查](qa/review-banach.md)、[后六章独立审稿及修订复查](qa/review-hilbert.md)。
- [编译与模板自动检查](qa/validation-report.json)、[逐页视觉记录](qa/visual-review.json)、[PDF 链接及书签检查](qa/pdf-audit.json)。
- [原件完整性](qa/source-integrity.json)、[干净 ZIP 解压重编](qa/zip-rebuild.json)、[最终交付哈希](qa/deliverables.json)。

正文按 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 改编；详见 [署名与改动](ATTRIBUTION.md)。本项目不是 MIT 的官方译本，MIT 不为改编背书。
