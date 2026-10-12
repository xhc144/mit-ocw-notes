# 离线编译

需要 Python 3.10+、XeLaTeX、ctex、fontspec、amsmath、amsthm、TikZ、PGFPlots、Fandol 和 Computer Modern Unicode 字体。源码不附字体。正文完全原生 TeX/TikZ，不将原英文 PDF 当正文。

```sh
python tools/build.py
```

构建在临时目录中进行，关闭 shell escape，最多五轮收敛目录与引用。产物为 `build/main.pdf`，日志及输入哈希为 `build/standalone-build.json`。编译不联网、不执行附带的 Mathematica notebook。

增强检查与每页渲染需 PyMuPDF/Pillow：

```sh
python vendor/math-latex-typesetting/scripts/validate.py main.tex --out build/validation
python tools/check_pdf.py build/main.pdf --out qa/pdf-links.json
```

作业10/11中的数值结果可用无第三方依赖的 `python tools/ps10_11_numerics.py` 重算。该程序用RK4并报告步长比较；物理模型的近似不等同于真实中子星预测。

用 `python tools/package_source.py` 从明确文件类别创建源码ZIP；不会包含缓存、日志、字体或仓库凭据。源PDF与网页快照在 `sources/`，是题源与许可证据，不是正文编译依赖。
