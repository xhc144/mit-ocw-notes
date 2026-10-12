# 实验与计算物理

中文合订PDF：[experimental-computational-physics-zh.pdf](dist/experimental-computational-physics-zh.pdf)（**38个PDF物理页**）。源码包：[experimental-computational-physics-source.zip](dist/experimental-computational-physics-source.zip)。

课程：8.13/14（Fall 2016–Spring 2017）；3.320（Spring 2005）；12.010（Fall 2024，只作工作流补充）。

本版正文：19个实际公开实验模块及Raman学生提案；原子势、DFT、声子、MD、MC、自由能、过渡态与KMC；15章文件。考核计数：6个公开考核单元（含Lab2第7题B这一个子问）+9道编者模型题+1个模拟读数例题。这是初始冻结后按扩展清单完成的连续中文重编，不是所有MIT课程、全部原件逐页翻译或全部作业译解。实际可获取文件与中文覆盖分开记录。

题面完整收录现行选定单元，解答说明假设、主要计算链及模型边界。官方数值或答案引用与编者独立解答分别标记。实验没有伪造现场观测；模拟数据均明确标注；代码实际运行。

## 范围与来源

- [冻结清单](research/coverage-frozen.json)及[冻结哈希](research/coverage-frozen.sha256)
- [逐文件来源、下载状态、页数和哈希](research/source-inventory.json)
- [扩展清单](research/coverage-amendment.json)与[完成对应](qa/coverage-completion.json)
- [题数口径](qa/assessment-count.json)
- [署名、许可和第三方例外](LICENSE.md)

- 初始九模块扩展到全部本次实际取得实验手册的主要方法；完整逐预习题和所有现场采集仍未完成。
- 3.320指定GULP/PWSCF/MOLDY原软件实验未执行，模型程序不冒充原材料计算。
- 3.320 Lab5热力学极限完整相图未计算。
- 行业讲次24无公开文件；第三方受限图、教材和表格未复制。
- 12.010仅工作流补充，不重译已有数学数值方法卷。

## 编译与复算

源码包不含字体、英文原PDF、第三方整书或构建缓存。需完整TeX Live的XeLaTeX、ctex/xeCJK、Fandol、Computer Modern Unicode、TikZ/PGFPlots与latexmk；在解压目录执行 `bash build.sh`。计算脚本依赖Python、NumPy、SciPy，运行 `python code/experiments.py`。

## 核验

已运行批准模板的多文件检查、XeLaTeX编译、日志检查、PDF页面和内部跳转检查，并渲染全部页面。最终逐页查看、干净ZIP重编译和远端下载证据分别见qa记录；自动PASS不能代替数学或视觉审查。
