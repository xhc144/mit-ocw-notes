# 生物物理

中文合订PDF：[biophysics-zh.pdf](dist/biophysics-zh.pdf)（**25个PDF物理页**）。源码包：[biophysics-source.zip](dist/biophysics-source.zip)。

课程：8.592J / HST.452J（Spring 2011）。

本版正文：15份详细讲义及主题页面的选定统计生物物理主线；9章理论、3章题解、1章来源。考核计数：24道公开顶层题（全部选定小问）+1个编者例题。这是冻结选定范围的连续中文重编，不是所有MIT课程、全部原件逐页翻译或全部作业译解。实际可获取文件与中文覆盖分开记录。

题面完整收录冻结单元，解答说明假设、主要计算链及模型边界。官方数值或答案引用与编者独立解答分别标记。实验没有伪造现场观测；模拟数据均明确标注；代码实际运行。

## 范围与来源

- [冻结清单](research/coverage-frozen.json)及[冻结哈希](research/coverage-frozen.sha256)
- [逐文件来源、下载状态、页数和哈希](research/source-inventory.json)
- [题数口径](qa/assessment-count.json)
- [署名、许可和第三方例外](LICENSE.md)

- PS1.2、PS1.4的全基因组扫描与PS1.6人群数据拟合。
- PS2.3明确来自Durbin书题，不擅自复制；PS2.5 BLAST在线实验。
- PS3.2同源/异源二聚体。
- PS4.3噬菌体包装数量估算题。
- PS5.3第三方MJ矩阵与PS5.4结构数据实验。
- PS6.2受力DNA完整相图、PS6.3受限实验图、PS6.5旧在线服务。
- PS7.1全基因组权重扫描。
- 第26讲协同效应没有链接或原文件；不宣称26讲全译。
- 官网提及解答不等于实际公开答案；未找到八套官方答案，24题解答均为编者推导。

## 编译与复算

源码包不含字体、英文原PDF、第三方整书或构建缓存。需完整TeX Live的XeLaTeX、ctex/xeCJK、Fandol、Computer Modern Unicode、TikZ/PGFPlots与latexmk；在解压目录执行 `bash build.sh`。计算脚本依赖Python、NumPy、SciPy，运行 `python code/checks.py`。

## 核验

已运行批准模板的多文件检查、XeLaTeX编译、日志检查、PDF页面和内部跳转检查，并渲染全部页面。最终逐页查看、干净ZIP重编译和远端下载证据分别见qa记录；自动PASS不能代替数学或视觉审查。
