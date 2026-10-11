# 重建

本册采用固定 CTeX/XeLaTeX 版式，生成一本连续 PDF。需要 Python 3.11+、XeLaTeX、CTeX、Fandol、Computer Modern Unicode OTF 字体、TikZ/PGFPlots、amsmath、amsthm、hyperref、xurl、needspace、enumitem 等常规 TeX Live 包。字体由 TeX 发行版提供，不在源码包另行分发。

解压源码 ZIP 到一个新目录，从该目录运行：

```bash
python subjects/thermal-statistical-physics/tools/reproduce_math.py
python subjects/thermal-statistical-physics/tools/build.py
```

输出 `subjects/thermal-statistical-physics/build/main.pdf`。构建器复制本册所有 TeX 到隔离临时目录、禁止 shell escape，执行 XeLaTeX 直到辅助文件收敛，遇到缺字、字体替换或溢出时报错。固定 `SOURCE_DATE_EPOCH=1791676800` 使同一工具链下的 PDF 日期与字节可复现。`build/standalone-build.json` 记录逐输入哈希、编译次数和 PDF 哈希。

本轮环境为 Debian TeX Live 2022，`xelatex` 0.999994、Python 3.12.14。CTeX 等补充包位于 `/workspace/.local/texmf`，实际使用：

```bash
TEXMFHOME=/workspace/.local/texmf python subjects/thermal-statistical-physics/tools/build.py
```

该绝对路径仅说明本轮环境；新机器可使用其正常 TeX Live 安装，不需相同路径。PyMuPDF、Pillow 只用于 PDF 审校与渲染，不参与正文编译。

```bash
python subjects/thermal-statistical-physics/tools/check_pdf.py subjects/thermal-statistical-physics/build/main.pdf --out /tmp/navigation.json
python subjects/thermal-statistical-physics/tools/render_pages.py subjects/thermal-statistical-physics/build/main.pdf --out /tmp/thermal-render
```

渲染器本身不会把“已生成 PNG”当成“已人工看完”；实际逐页审阅另外写在 QA 记录。原件按冻结清单归档，5 份图片对象处理前后的 SHA256 分开保存；ZIP 中包含可再构建的中文源稿、审校工具和公开归档来源，不包含凭据或未获许可的被分离图片。
