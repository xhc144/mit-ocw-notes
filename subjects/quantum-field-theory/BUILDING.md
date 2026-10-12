# 从源码编译

需要 Python 3.10+、XeLaTeX、ctex/xeCJK/zhnumber、Fandol、Computer Modern Unicode（cmunrm.otf等）、amsmath/amsthm、TikZ/PGFPlots、booktabs/longtable。PDF校验和页面渲染需要PyMuPDF及Pillow。字体由编译环境提供，不在ZIP内分发。

在本目录或解压后目录执行：

```bash
python tools/build.py --out build
python tools/check_pdf.py build/main.pdf --out build/pdf-links.json
```

`build.py` 在临时目录中复制全部实际TeX输入，使用XeLaTeX且关闭shell escape，至少两轮直至目录/引用收敛，记录源码及PDF SHA256。图在TeX中用TikZ生成，不需要网络、原英文PDF、外部图像或商用教材。主文件内含固定适配类，编译时自动生成；无需跨目录读取其他学科。

仓库额外保留用户排版技能检查器，可运行：

```bash
python vendor/math-latex-typesetting/scripts/validate.py main.tex --out build
```

该检查器负责模板、依赖、编译、字体、盒溢出、页尺寸及全页渲染。自动PASS不证明内容无误，也不代替实际视觉查看。真实语义复核与图像查看证据分别见qa。

源码ZIP排除PDF原件、字体、缓存、构建日志和页面渲染文件。解压至全新目录后运行上面的两条命令即可重新编译合订本；所需运行环境属于外部依赖。参考课程链接留在PDF来源附录，离线编译不使用这些链接取资料。
