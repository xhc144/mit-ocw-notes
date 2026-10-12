# 从源码重新编译

安装 XeLaTeX、ctex、xeCJK、Fandol、CM Unicode 字体及 PGFPlots。推荐完整 TeX Live 2024 或更新版本。不要将与旧 LaTeX 内核不兼容的最新 ctex 混装。版式沿用本仓库批准的王者模板，10pt、letter、Fandol 和 CMU；字体来自正常 TeX 发行版，不在源码包中捆绑。

在此目录执行：

```bash
python tools/build.py --out build
python tools/numerical_checks.py
python -m pip install pymupdf pillow
python tools/check_pdf.py build/main.pdf --out build/links.json
python vendor/math-latex-typesetting/scripts/validate.py main.tex --out build/style
```

`build.py` 将全部 TeX 输入复制到隔离临时目录，禁用 shell escape，检查交叉引用收敛与源文件未变化，并拒绝溢出版心、缺字符或字体替换。默认 `SOURCE_DATE_EPOCH=1791763200` 使重编可比；编译器/宏包版本不同仍可能改变字节或分页。数值检查仅用 Python 标准库。PDF 链接检查遍历全部目录链接和书签，逐页视觉审读另在 QA 中记录。

本次执行环境缺少系统中文宏包，兼容的 Debian TeX Live 2022 ctex/xeCJK/Fandol 加载到独立 TEXMFHOME，由系统 XeLaTeX 2024 编译。没有修改系统权限，也没有打包这些依赖。实际环境变量：

```bash
TEXMFHOME=/tmp/mitphysics-debian/usr/share/texlive/texmf-dist \
XDG_CACHE_HOME=/tmp/mitphysics-font-cache \
python tools/build.py --out build
```

此路径只是本次环境安装位置，其他机器使用正常 TeX Live 即可。原 MIT PDF 不属于编译依赖。源码 ZIP 应在新目录解压后实际运行上述构建，不能仅检查 ZIP 能列文件。
