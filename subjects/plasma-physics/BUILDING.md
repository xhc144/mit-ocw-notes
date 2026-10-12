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

历史增补版另含 2005 旧参数冷波图生成器和物理量复核，可在本目录执行：

```bash
python tools/historical_2005_cold.py
python tools/historical_revision_checks.py
python qa/followup-chap5-checks.py
python qa/followup-mhd-theory-checks.py
```

`historical_2005_cold.py` 以 2005 原题的两组密度和 5 T 重新生成矢量 PGFPlots 片段；与 2006 当期不同参数的图不可互换。`historical_revision_checks.py` 核算 Saha 温度、Fermi 镜、漂移、自由程、环电压、Z 箍缩力平衡和 2003 MHD 理想壁边际式，并数清历史题原编号。2002 PS8 的印刷目标系数与同页算子逐字积分不合，题解明示该差异，不用脚本“通过”来掩盖原件矛盾。

历史来源的 34 份考核 PDF（含 11 件官方扫描答案）与 3 份模拟说明在 `qa/historical-supplement-freeze.json` 独立冻结；它们已包含于总数 99 的原始 `source-manifest.json`，而该原清单的初次发现角色标签保持冻结。`qa/coverage-revision.json` 给写成正文后的新覆盖状态。
