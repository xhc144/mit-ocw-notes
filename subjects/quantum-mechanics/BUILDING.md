# 编译中文量子力学册

源码 ZIP 是独立项目，解压后在含 `main.tex` 的目录执行：

```sh
python tools/build.py --out build
python tools/check_pdf.py build/main.pdf --out build/pdf-links.json
```

需要 Python 3、XeLaTeX、ctex/xeCJK、TikZ/PGFPlots、Fandol 字体和 CM Unicode OpenType 字体；PDF链接检查另需 PyMuPDF。建议使用完整 TeX Live。字体为运行时依赖，没有在 ZIP 内分发。若依赖安装在用户 TEXMF 树，通过正常的 `TEXMFHOME` 环境变量指向该目录。不得改用替代字体来假称原模板编译成功。

`main.tex` 内嵌固定适配类，不依赖仓库其他学科。编译程序隔离暂存源码、关闭 shell escape，至少运行两遍并等候目录与交叉引用收敛，遇到溢出、缺字、字体替代或源文件在编译期间变化时停止。自动编译和链接检查不等于数学正确或视觉审查。

本次公开成品采用仓库已有数学 LaTeX 排版 Skill 的固定模板验证器编译，自动检查通过；独立内容与每页图文审查另存 `qa/`。SOURCE ZIP 可重建相同页面布局；PDF 的创建时间等元数据可能不同。

数值图的TikZ坐标已经随`chapters/figure-*.tex`提供，普通编译不需联网或SciPy。若要独立重算数值证据，`python tools/assessment_numerics.py`重算原图，`python tools/addition_numerics.py`重算本次17个图表输入，二者另需NumPy与SciPy；计算结果保存在仓库`qa/assessment-numerics.json`和`qa/addition-numerics.json`。图的采样值不作为解析证明。

研究生增补数值检查用 `python tools/graduate_checks.py`（另需SymPy）；它复算辐射径向积分、超精细分支、Hartree、项符号、Clifford与Ramsey及散射数值。`tools/graduate_plots.py`可重绘硬球和中性原子TikZ输入；Kronig–Penney允许区已固化在figure-graduate-322-bands.tex。检验范围按QA逐项列出，不称独立全书审查。
