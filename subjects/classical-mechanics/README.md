# 理论力学中文讲义

**[阅读中文合订 PDF](classical-mechanics-zh.pdf)** · **[下载可编辑源码 ZIP](classical-mechanics-source.zip)**

一本连续的 **89 页**简体中文讲义：十章正文讲解约束与拉格朗日方程、对称守恒、中心力、小振动、刚体、哈密顿方程、正则变换、Hamilton–Jacobi、作用角及摄动，后接连续介质、完整Stokes球流推导与非线性动力学，并收录 **76 道实际作业原题的中文题面、解答或数值复现**及课程项目分析。采用用户已有的王者 LaTeX 模板；卷首先说明课程教师、学期、大纲、课历与考核方式。

有官方答案的8.223作业逐题标明“官方解答中文改写”；新增推导、错误修正及8.09作业1–7选择的20题、作业8–10及项目答案标为AI独立内容。所有图与数值结果直接进入合订PDF，读正文无需另外打开一组英文原版。

这是按学科重组的扩编版，**不是两课全部原稿的逐页全译本**。覆盖和未完成部分在PDF末章及 [机器可读覆盖清单](source-coverage.json) 中明确列出。已补入旋转系/Euler角、分子模式、三维Kepler作用量、多频运动、HJ摄动算法、Stokes速度/压力/阻力和湍流量纲分析。8.09第4章实际没有三体或Lagrange点内容，首版错误来源映射已删除。项目给可复现数值候选，不冒称全局最优；不伪造实物演示。无阻尼摆的局部周期岛与参数扫描已给出，作业10第3题(a)要求的固定实验周期窗口仍未复现，明确标为部分完成；301点扫描之外又进行了601点固定初值射击，未用另初值周期岛替代该要求。

<details>
<summary>出处、原件与许可（供核对）</summary>

主课：Iain W. Stewart, MIT 8.09 Classical Mechanics III, Fall 2014；基础补充：Matthew Evans, MIT 8.223 Classical Mechanics II, January IAP 2017。8.09讲稿编辑 Francisco Machado、Thanawuth Thanathibodee、Prashanth S. Venkataram；8.223讲稿由听课学生打字整理，个人署名未在课程页逐项列出。

实际取得44份PDF、656页，保守许可审查后保留37份PDF、624页。计数包含8.09合本与分章的重叠；不代表624页独立内容，也不代表已将原件逐页中文化。

原件位于 [来源目录](../../sources/classical-mechanics/)，逐项URL、标题、作者、学期、许可、SHA-256和页数见 [来源清单](../../manifests/classical-mechanics-sources.json)。7份混有商业教材题的8.09作业原PDF不打包；其中20道可分离课程题已经逐题核查，以自写中文题面和独立解答单独纳入，图形重新绘制；7份notebook暂缓权利审查，未执行。没有把推荐商业教材或其题号引用当成已获再发布许可。

8.09大纲有期中期末，但公开页未提供实际试卷或解答；8.223明确无考试。8.223第7、9、19讲未取得。第12讲实际10页PDF已核验，保留“目录称缺失”、资源标题与正文标题不一致的原始记录。

资料与改编遵循 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)，原件另有权利声明时优先；[MIT OCW条款](https://ocw.mit.edu/pages/privacy-and-terms-of-use/)。这是非商业独立学习整理，没有MIT官方中文或官方认可身份。

</details>

<details>
<summary>审查证据与复现方法</summary>

[首版独立内容审查](qa/independent-content-review.md)保留历史记录；扩编的[主干物理审查](qa/extension-physics-review.md)、[刚体与振动审查](qa/rotation-modes-independent-review.md)、[基础方法审查](qa/foundations-extension-independent-review.md)和[新增20题独立复核](qa/selected-assessment-independent-review.md)分别记录公式、条件、来源差异与修正闭环。89 页均已查看实际渲染：1–48页检查接触表并放大重点页，49–50页查看单页，51–89页由独立审查者逐张查看；两处返修页重编后实际复查，其余87页PNG字节相同。方法与逐页证据见 [前50页审查](qa/expanded-visual-review-1-50.md)、[后39页审查](qa/expanded-visual-review-51-89.md)及[汇总记录](qa/expanded-review-summary.json)。[发布检查](qa/release-evidence.json) 记录本次实际验证的111个目录书签、115个内部链接及嵌入字体。[覆盖清单](source-coverage.json) 将原题取得、中文编写、开放任务和未完成内容分开。

源码ZIP包含同版LaTeX、TikZ/PGFPlots、完整计算CSV、印刷抽稀CSV、Python脚本及说明；不附字体或商业教材。印刷抽稀保留全部参数网格，逐点检查见 [印刷数据检查](qa/printed-data-check.json)。源码ZIP足以编译中文PDF；`audit_release.py`校验原件时须在含sources与manifests的仓库中运行。

在本目录运行 `xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex` 至少两次。需XeLaTeX、ctex/Fandol、Computer Modern Unicode字体、TikZ、PGFPlots。模板类代码完整包含于main.tex；无需原版PDF即可编译中文版。

数值复算用NumPy/SciPy，运行 `python tools/reproduce_numerics.py`；会重新生成本学科CSV与数值报告。全部模型是原课理想数学模型，未运行外部notebook。当前环境依赖版本见 [数值环境记录](qa/numerical-environment.json)。编译与逐页审查证据位于qa目录；自动版式通过与数学、视觉审查分别记录。

</details>
