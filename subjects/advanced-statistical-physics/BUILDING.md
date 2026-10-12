# 编译与复核

解压源码ZIP后，在包根运行 `python3 tools/build.py --out build`。程序把所有TeX输入复制到洁净临时目录，禁用shell escape，并反复运行XeLaTeX直到aux/toc/out收敛（至少两轮）；字体缺字、未定义引用、溢出盒和字体警告会使构建失败。输出为 `build/main.pdf` 及 `build/standalone-build.json`。构建不访问网络，也不依赖其他学科目录。

所需环境为Python 3、XeLaTeX、ctex/xeCJK、Fandol OTF、CM Unicode OTF、amsmath、amsthm、geometry、fancyhdr、enumitem、xurl、hyperref、TikZ、PGFPlots、longtable和booktabs。建议完整TeX Live安装；字体与原课程PDF不打入ZIP。当前执行环境用临时TEXMFHOME补齐兼容TeX Live 2024的包，未改系统或仓库模板。

`python3 tools/physics_checks.py` 另用NumPy、SciPy、mpmath复核有限维矩阵、Gaussian动量矩、Bose热容及示意曲线，并重建 `figures/*.tex`。源码ZIP已包含这些向量图，普通PDF重编译不需先运行数值脚本。检查报告见 `qa/numerical-checks.json`，不把有限样本当作一般物理定理的证明。
