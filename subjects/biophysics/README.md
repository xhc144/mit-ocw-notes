# 生物物理

中文合订PDF：[biophysics-zh.pdf](dist/biophysics-zh.pdf)（**51个PDF物理页**）。源码包：[biophysics-source.zip](dist/biophysics-source.zip)。

课程：8.592J / HST.452J（Spring 2011）。

本版正文：15份实际详细讲义的统计生物物理核心推导逐项展开；10章理论、5章题解及数据、1章来源。考核计数：八套作业全部37道题面；35道解析/数据题、1道当前Swiss-Prot方法复算、1道旧RNA服务执行缺口；+1个编者例题。这是冻结选定范围的连续中文重编，不是所有MIT课程、全部原件逐页翻译或全部作业译解。实际可获取文件与中文覆盖分开记录。

题面完整收录冻结单元，解答说明假设、主要计算链及模型边界。官方数值或答案引用与编者独立解答分别标记。实验没有伪造现场观测；模拟数据均明确标注；代码实际运行。

## 范围与来源

- [冻结清单](research/coverage-frozen.json)及[冻结哈希](research/coverage-frozen.sha256)
- [逐文件来源、下载状态、页数和哈希](research/source-inventory.json)
- [题数口径](qa/assessment-count.json)
- [署名、许可和第三方例外](LICENSE.md)

- 原冻结24题范围已被扩展覆盖记录取代，全部37题逐项状态见qa/coverage-completion.json。
- 原第25/26讲目录与cooperativity纲要分别记录；提及的2009讲义无下载超链接。
- PS6.5原RNA服务请求503/403，没有原服务曲线。
- PS2.5在当前Swiss-Prot实际完成方法实验，2011nr无法恢复，今日nr请求状态单列。
- 第三方MJ表仅临时分析聚合事实，不重分发原表；受限实验图不复制。

## 编译与复算

源码包不含字体、英文原PDF、第三方整书或构建缓存。需完整TeX Live的XeLaTeX、ctex/xeCJK、Fandol、Computer Modern Unicode、TikZ/PGFPlots与latexmk；在解压目录执行 `bash build.sh`。计算脚本依赖Python、NumPy、SciPy，运行 `python code/checks.py`。

## 核验

已运行批准模板的多文件检查、XeLaTeX编译、日志检查、PDF页面和内部跳转检查，并渲染全部页面。最终逐页查看、干净ZIP重编译和远端下载证据分别见qa记录；自动PASS不能代替数学或视觉审查。
