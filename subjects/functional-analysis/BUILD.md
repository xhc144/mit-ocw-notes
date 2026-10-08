# 重编本册

本目录包含独立中文文稿。`main.tex` 内置锁定的王者适配类，编译时生成该类；章节位于 `chapters/`，模板原件及验证脚本位于 `vendor/math-latex-typesetting/`。这里不需要运行 MIT 原 TeX，也不需要原件 ZIP。

运行依赖：XeLaTeX、CTeX/Fandol、CM Unicode（`cmunrm.otf`、`cmunbx.otf`、`cmunti.otf`、`cmunbi.otf`）、基础 LaTeX 数学/版式包、TikZ/PGFPlots、Python 3.11+。字体不在源码包中。

```bash
python -m pip install -r vendor/math-latex-typesetting/requirements.txt
bash tools/compile.sh
```

若缺少中文包和锁定字体，可在网络可用时使用 `tools/bootstrap_tex.py`，它只将经固定哈希核验的资源放到指定可写 TEXMF 路径。例如：

```bash
python tools/bootstrap_tex.py --texmf-dir /tmp/functional-texmf --cache-dir /tmp/functional-tex-downloads
TEXMFHOME=/tmp/functional-texmf bash tools/compile.sh
```

编译检查输出 `build/main.pdf` 与 `build/validation_report.json`。自动检查验证固定模板、编译日志、引用和 PDF 基本结构；数学正确性和逐页视觉结果须分别审查。原交付的两份独立数学审稿保留在 `qa/`。`tools/audit_pdf.py` 可检查所有目录/书签链接并逐页渲染，仍不自动宣称视觉验收。

```bash
python tools/audit_pdf.py build/main.pdf --out build/visual
```

使用 TeX Live 2025/dev/Debian、XeTeX 0.999996、上述固定资源与 PyMuPDF 1.26.6 完成过干净 ZIP 解压重编。PDF 创建时间等元数据可能不同；重编验收比较页数、逐页文本、目录/链接和文稿输入哈希。
