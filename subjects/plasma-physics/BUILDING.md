# 编译与计算复现

使用正常XeLaTeX发行版，具ctex、xeCJK、Fandol、CM Unicode、PGFPlots和graphicx。主体采用仓库批准的王者模板，10pt/letter及Fandol/CMU。字体不捆绑。5份嵌图均为原创数值矢量图，包含在figures，原MIT课件和受限教材不作为编译输入。

在本目录执行：

```bash
python tools/build.py --out build
python tools/basic_numerical_checks.py
python tools/cold_wave_plots.py
python -m pip install pymupdf pillow
python tools/check_pdf.py build/main.pdf --out build/links.json
python vendor/math-latex-typesetting/scripts/validate.py main.tex --out build/style
```

`build.py`将TeX和5份矢量图复制至隔离临时目录，无网络、无shell escape，检查引用收敛和输入哈希不变化，并拒绝溢出、缺字和字体替换。数字检查与冷波采样只用标准库。冷波脚本是可编辑PGFPlots片段的产生器，正值/截止/共振分段，不画abs(n²)。

要重跑完整MHD数值扫描，另安装NumPy、SciPy、Matplotlib：

```bash
python -m pip install numpy scipy matplotlib
MHD_OUTPUT_DIR=/tmp/mhd-reproduction python tools/mhd/run_review.py
MHD_OUTPUT_DIR=/tmp/mhd-reproduction python tools/mhd/hw4_ldx_reference.py
```

完整扫描可能需数分钟。输出与解析模型、求积加密和分支限制见`qa/independent-mhd-review.md`；本卷源码包包含实际运行后的CSV/JSON与可执行程序。普通LaTeX重编无需重跑扫描；若改了计算条件，应重新生成矢量图和正文数值，而非只改图。

本次系统中文宏包缺失，实际将兼容Debian TeX Live2022中文包加载于独立TEXMFHOME，由系统XeLaTeX2024编译：

```bash
TEXMFHOME=/tmp/mitphysics-debian/usr/share/texlive/texmf-dist \
XDG_CACHE_HOME=/tmp/mitphysics-font-cache \
python tools/build.py --out build
```

该临时依赖路径不是源码硬编码。干净源码ZIP解压后已实际构建；不同编译器/宏包或创建时间可能改变字节，须以同页文字和渲染审查建立内容一致性。
