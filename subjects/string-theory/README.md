# 弦论与全息对偶

本卷已从选讲扩写为两门实际公开课程材料的合订稿：8.251 Spring 2007 的 26 讲、8.821 OCW Fall 2014 的 24 讲，正文与题解为可编辑中文 LaTeX，自绘 TikZ/矢量图。原笔记的作者、学期差异与逐件许可保留；原 PDF 不作整页背景或替代交付。

当前已通过机械编译的工作稿为 **126 页**，包含 **67 道完整独立题及一题公开补充式**，对应 68 个已完整编写的原编号（其中 HW4.5/HW5.1 同题重发）。本次为完整公开材料对应稿的审阅检查点，尚待整卷视觉审查和独立内容复核。源码 ZIP 已进行隔离重编译；编译与远端核对回执单列，不能将机械检查当作学术终审。

- [126 页中文 PDF](dist/string-theory-zh.pdf)
- [可独立编译的源码 ZIP](dist/string-theory-source.zip)
- [逐讲与逐题状态、缺失题面及高阶待补范围](coverage.md)
- [50 讲对应矩阵](qa/lecture-coverage.csv)
- [128 个原编号及阅读任务的处理矩阵](qa/assessment-coverage.csv)
- [当前扩写与核验进度](qa/expansion-progress.json)
- [逐文件官方来源、页数、SHA-256、权利声明](sources/resource-inventory.json)

dist/ 已更新为上述 126 页完整对应稿，保留每卷一个主 PDF。旧 qa/build/、review.json、visual-review.json 等回执仅对应历史 28 页精选稿；当前编译见 expanded-working-validation.json，干净重编译见 clean-rebuild.json。整卷视觉与独立内容验收仍待完成。

## 实际覆盖

8.251：完整公开作业 20 个原编号、2007 年 Test 1/Test 2/Final 的 13 题、2005 与 2004 历史测验 11 题、第 26 讲复习 3 题。未取得教材题面只保留真实题号；HW10.9 只解公开补充条件，缺失主体及 (b) 未伪造。8.821：21 道必做作业题均有题面与解答；PS3.3 为阅读任务，单列解释而不虚加题数。58 个纯教材引用项目没有完整题面。

官方解答与独立补写解答分开：2005 历史测验和 8.821 前四组按官方解答核对；其他正式/历史考试、公开作业与 PS5 独立推导。源文件对近视界几何、闭弦闭合条件、单位和非退化假设的具体问题，在题解中说明。

## 编译

已完整安装 ctex、Fandol、Computer Modern Unicode、TikZ/PGFPlots 的 TeX Live 下：

~~~sh
python3 scripts/build.py
~~~

脚本检查批准模板的锁定类，在新临时目录用 XeLaTeX 三次编译，禁用 shell escape，输出 build/main.pdf。源码不分发字体。普通编译仅读取给定 CSV，不要求联网或科学计算库。

物理数值与符号复核脚本另需 numpy、scipy、sympy；它们的范围与结果见 qa/。本环境沿用已存在的 TEXMFHOME=/workspace/.local/texmf，完整系统 TeX Live 不需该本地路径。

## 署名与许可

教师 Barton Zwiebach、Alan Guth、Hong Liu；学生笔记 Bryan Owens 根据 Kayla Jacobs 手稿整理，官方未全面校阅声明保留。改编与独立增补采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)，保留署名、非商业、相同方式共享，不暗示 MIT 或作者认可。第三方受限书本、论文全文、图像和字体不收录。许可复核见 [rights-reassessment.json](sources/rights-reassessment.json) 与 [LICENSE.md](LICENSE.md)。
