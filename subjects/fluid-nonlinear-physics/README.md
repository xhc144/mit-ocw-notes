# 流体与非线性物理

中文合订PDF：[fluid-nonlinear-physics-zh.pdf](dist/fluid-nonlinear-physics-zh.pdf)（**39个PDF物理页**）。源码包：[fluid-nonlinear-physics-source.zip](dist/fluid-nonlinear-physics-source.zip)。

课程：1.63（Fall 2002）；12.006J / 18.353J / 2.050J（Fall 2022）。

本版正文：1.63七章流体主题与12.006J全部28讲的主要物理机制、方程和核心推导；12章理论、4章题解、1章来源。考核计数：17个公开顶层题/单元（选定小问全部保留）。这是初始冻结后按扩展清单完成的连续中文重编，不是所有MIT课程、全部原件逐页翻译或全部作业译解。实际可获取文件与中文覆盖分开记录。

题面完整收录现行选定单元，解答说明假设、主要计算链及模型边界。官方数值或答案引用与编者独立解答分别标记。实验没有伪造现场观测；模拟数据均明确标注；代码实际运行。

## 范围与来源

- [冻结清单](research/coverage-frozen.json)及[冻结哈希](research/coverage-frozen.sha256)
- [逐文件来源、下载状态、页数和哈希](research/source-inventory.json)
- [扩展清单](research/coverage-amendment.json)与[完成对应](qa/coverage-completion.json)
- [题数口径](qa/assessment-count.json)
- [署名、许可和第三方例外](LICENSE.md)

- 核心物理机制和方程已补全；Oseen完整远场系数、全Re谱图、具体沿岸风初边值精确场仍未逐式展开。
- 题解保留原冻结17个公开单元，不宣称全部作业完成。
- 原课没有取得官方考试或答案，不造题。
- 有限时间Lyapunov、谱和延迟图不作为严格混沌证明。

## 编译与复算

源码包不含字体、英文原PDF、第三方整书或构建缓存。需完整TeX Live的XeLaTeX、ctex/xeCJK、Fandol、Computer Modern Unicode、TikZ/PGFPlots与latexmk；在解压目录执行 `bash build.sh`。计算脚本依赖Python、NumPy、SciPy，运行 `python code/checks.py`。

## 核验

已运行批准模板的多文件检查、XeLaTeX编译、日志检查、PDF页面和内部跳转检查，并渲染全部页面。最终逐页查看、干净ZIP重编译和远端下载证据分别见qa记录；自动PASS不能代替数学或视觉审查。
