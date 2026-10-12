# 流体与非线性物理

中文合订PDF：[fluid-nonlinear-physics-zh.pdf](dist/fluid-nonlinear-physics-zh.pdf)（**72个PDF物理页**）。源码包：[fluid-nonlinear-physics-source.zip](dist/fluid-nonlinear-physics-source.zip)。

课程：1.63（Fall2002）；12.006J /18.353J /2.050J（Fall2022）。

本版正文：全部公开作业对应的连续中文讲义；守恒、黏性、边界层、热输运、多孔介质、旋转、气溶胶、均匀化、沿岸风场与混沌；26章。考核计数：1.63全部20份实际公开作业文件+混沌十套作业全部32道顶层题，共52单元，全部实际小问；无官方考试/答案文件。这是初始冻结后按扩展清单完成的连续中文重编；上述实际公开任务均有题面与解答。目录发现、文件取得和中文覆盖分别记录，不声称MIT所有课程或原件逐页全译。

题面完整收录扩展清单的现行公开单元，解答说明假设、主要计算链及模型边界。官方数值或答案引用与编者独立解答分别标记。实验没有伪造现场观测；模拟数据均明确标注；代码实际运行。

## 范围与来源

- [冻结清单](research/coverage-frozen.json)及[冻结哈希](research/coverage-frozen.sha256)
- [逐文件来源、下载状态、页数和哈希](research/source-inventory.json)
- [扩展清单](research/coverage-amendment.json)与[完成对应](qa/coverage-completion.json)
- [题数口径](qa/assessment-count.json)
- [署名、许可和第三方例外](LICENSE.md)

- 本版已覆盖20份流体公开作业和全部32道混沌题；不是51份流体讲义与16份混沌讲义的逐页全译。
- 原题缺几何或本构参数时给明确模型和参数化解；没有补造唯一数值。
- 沿岸风场已展开；源式两处量纲修正另列。
- 原课没有取得官方考试或答案，不造题。
- 有限时间Lyapunov、周期碰合、谱和延迟图不作为严格混沌证明。

## 编译与复算

源码包不含字体、英文原PDF、第三方整书或构建缓存。需完整TeX Live的XeLaTeX、ctex/xeCJK、Fandol、Computer Modern Unicode、TikZ/PGFPlots与latexmk；在解压目录执行 `bash build.sh`。计算脚本依赖Python、NumPy、SciPy，运行 `python code/checks.py`。

## 核验

已运行批准模板的多文件检查、XeLaTeX编译、日志检查、PDF页面和内部跳转检查，并渲染全部页面。最终逐页查看、干净ZIP重编译和远端下载证据分别见qa记录；自动PASS不能代替数学或视觉审查。
