# 中文源码编译说明

主文件为 `main.tex`，请在同一目录用 XeLaTeX 连续编译至少两次（目录与交叉引用收敛时可需第三次）：

```sh
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

使用本书锁定的王者版式。适配类嵌在 `main.tex`，首轮编译会生成它；无需从仓库另取模板。所有图形直接由各章中的 TikZ 代码绘制，没有外链图片。所需宏包为通常 TeX Live 中的 ctex、fontspec、amsmath、amssymb、mathrsfs、amsthm、etoolbox、xcolor、geometry、setspace、fancyhdr、enumitem、needspace、xurl、hyperref 和 TikZ。

需要 XeLaTeX、Fandol 中文字体及 Computer Modern Unicode 的 `cmunrm.otf`、`cmunbx.otf`、`cmunti.otf`、`cmunbi.otf`。字体属于运行时依赖，不随本源码包分发，不能悄悄改用另一字体或引擎。编译结果使用 letter 纸，正文10pt、行距1.6。

本包只收实际编译所需中文 TeX、许可和来源说明。英文源PDF、网页原件、文本提取、审稿及发布证据留在公开仓库 `xhc144/mit-ocw-notes/subjects/topology/`；成品 `topology.pdf` 单独交付，不在本包中重复打包。许可、作者和改编角色见 `LICENSE.md`、`source-provenance.md` 和原样保留的法律文本。

本书的中文证明补全、题解、勘误及新增图形由编者提供，不是 MIT 官方题解。原15章与58道编者题保留；新增指定原课程题面与解答见第16—18章。缺少完整题面的教材习题只登记，不根据题号重构。
