# 复变函数与应用：中文编译源码

此包用于重编已验收的124页中文讲义。包含49个实际TeX输入文件（正文及原生TikZ图）、锁定王者模板、模板出处、必需构建代码和简短来源/许可说明。适配类由 `main.tex` 内的 `filecontents*` 自动生成。

MIT英文原件、原始网页、完整来源哈希和数学/视觉审稿档案保留在 [仓库](https://github.com/xhc144/mit-ocw-notes/tree/main/subjects/complex-analysis) 与 [英文原件归档](https://github.com/xhc144/mit-ocw-notes/tree/main/sources/complex-analysis)，不在源码ZIP中，也不是编译依赖。正文不使用 `includepdf` 或截图嵌入原书。

## 重编

需要 XeLaTeX、常规 TeX Live 宏包（含 PGF/TikZ、hyperref、booktabs）、Python 3.11+、PyMuPDF 和 Pillow。系统字体、Python环境和编译缓存不打包。若系统尚缺固定模板所用 Fandol/CM Unicode 字体，可运行随附工具；它按固定哈希校验下载内容。

```bash
python -m pip install -r vendor/math-latex-typesetting/requirements.txt
python tools/bootstrap_tex.py --texmf-dir .runtime/texmf --cache-dir .runtime/downloads
TEXMFHOME="$PWD/.runtime/texmf" bash tools/build.sh
python tools/audit_pdf.py complex-analysis.pdf --out build/pdf-audit.json
```

已有相同字体环境时可设置对应 `TEXMFHOME`，直接执行构建。输出为 `complex-analysis.pdf`，编译日志及逐页渲染在 `build/`。自动校验不代替数学与人工视觉审查；已验收版本的审查记录在仓库中。

`ZIP-CONTENTS.json` 记录包内每个文件的字节数和SHA256（清单自身除外）。原作者、课程与许可见 [SOURCES.md](SOURCES.md) 和 [LICENSE.md](LICENSE.md)。
