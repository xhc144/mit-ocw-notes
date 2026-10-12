# 独立源码包

运行 `python3 scripts/build.py`。需完整 TeX Live/XeLaTeX（ctex、Fandol、Computer Modern Unicode、TikZ/PGFPlots）。脚本检查批准模板锁定区，在隔离临时目录禁用 shell escape 编译三遍，产出 build/main.pdf。无需联网或原课程 PDF；不分发字体。

本包是 126 页公开课程对应稿的审阅检查点，含 44 个实际输入章节文件、完整可取得题面及解答、来源许可、覆盖清单、绘图 CSV 与有限数值核验结果。未取得的教材题面、部分高阶证明及项目论文明确列在 coverage.md。官方答案与独立补写分开。

机械编译通过不等于学术终审。整卷视觉自查已完成；有限独立内容审阅完成，三处反馈已修正，范围见包内 qa/parent-review-feedback.json。ZIP 不嵌套 PDF、旧选编正文、编译缓存、字体或凭据。科学复核脚本另需 numpy/scipy/sympy。
