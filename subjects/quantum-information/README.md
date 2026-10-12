# 量子信息与量子计算

[中文主 PDF](dist/quantum-information-zh.pdf) · [可编译源码 ZIP](dist/quantum-information-source.zip)

本卷为 MIT 官方公开材料的中文主题重编，采用仓库已批准的王者模板。共 **67 页、93 个官方原题大编号**。其中92个MIT原题号有答案，另有8个可读教材任务独立重述并解答；18.435J HW4.5的原PDF未含可恢复节点/边对象，特定图证明未完成，正文给明确标注的替代构造。

修订版已实际扩写正文推导、协议和原题解答，并按逐讲文件列出内容位置。逐讲覆盖见 [LECTURE-COVERAGE.md](LECTURE-COVERAGE.md)。

课程、题目实际年份、联列去重、逐件链接及未覆盖项见 [SOURCES.md](SOURCES.md)、[coverage.json](coverage.json) 和 [source-inventory.json](source-inventory.json)。没有把入口页、已下载的英文 PDF、教材引用题或研究计划计为中文交付。

内容与题号按主题合编到一个主 PDF；原子/量子基础衔接本仓库既有量子力学及波动光学卷。高级定理的引用层级、条件限定和源码数值图均在正文说明。

编译：安装 XeLaTeX、ctex/xeCJK、Fandol、CMU Serif/CMU Sans Serif/CMU Typewriter Text、TikZ/PGFPlots、amsmath、hyperref 等标准 TeX Live 组件。解压 ZIP，在含 `main.tex` 的目录执行：

```bash
mkdir -p build
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
```

完整自动检查可用 `python3 vendor/math-latex-typesetting/scripts/validate.py main.tex --out build`；Python 需 PyMuPDF。绘图脚本另需 NumPy 和 Matplotlib。字体文件不在包内。

实际执行的编译、全页渲染、逐页目检、数值检查、ZIP 干净目录重编译记录见 [qa/README.md](qa/README.md)。自动报告保留“未评数学/教学/视觉”的原始字段；人工逐页视觉记录另列，有限矩阵计算不会冒充一般证明。

许可与作者见 [LICENSE.md](LICENSE.md)。本项目改编适用内容依 CC BY-NC-SA 4.0 分享，逐件第三方例外保留，官方题面与编者补写解答分别标注。
