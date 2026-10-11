# 重建

使用 Python 3、XeLaTeX、CTeX/xeCJK、TikZ/PGFPlots、Fandol、CM Unicode OpenType字体。建议完整TeX Live。字体不随ZIP分发。依赖装在用户TEXMF树时，用TEXMFHOME指向实际目录；本次环境使用 `/workspace/.local/texmf`。

在解压目录运行：

```bash
python3 tools/build.py --out build
```

脚本在隔离目录关闭shell escape，检查源码不变，至少两次编译至目录/引用收敛，拒绝溢出、缺字、字体回退。输出 `build/main.pdf` 和编译记录。SOURCE_DATE_EPOCH默认固定为2026-10-11，重建时间不改变文档日期。

排版技能完整验证与所有页渲染：

```bash
python3 vendor/math-latex-typesetting/scripts/validate.py main.tex --out build/validation
python3 tools/check_pdf.py build/main.pdf --out build/pdf-links.json
```

链接检查需要PyMuPDF；页渲染还需要Pillow。程序只生成图像，不代替人工逐页视觉检查。

数值例子复现需要numpy和mpmath：

```bash
python3 tools/numerical_checks.py
```

它复现特定例子的矩阵、曲线采样和Bessel零点，并非一般证明。

原件保存在仓库 `sources/waves-and-optics/`，冻结选课与48份材料的官方链接/页数/SHA在 `manifests/waves-and-optics-sources.json`。在完整仓库执行 `python3 subjects/waves-and-optics/tools/collect_sources.py` 校验本地原件，`--fetch` 按已冻结链接重取；若上游哈希改变则停止，不悄悄重新选课。源码ZIP包含成书全部输入及排版验证工具，不复制原件PDF或字体，正常构建不需要网络或原件。
