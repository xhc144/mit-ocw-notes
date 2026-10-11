# 实际编译环境

XeLaTeX 使用系统可执行文件 `/usr/bin/xelatex`；中文包与原模板所需 Fandol / Computer Modern Unicode 来自已有 `/workspace/.local/texmf`。最初默认环境找不到 ctex.sty；build.sh 检测缺包后接入这一现有 TEXMFHOME，未替换用户字体或改动锁定模板。可写字体缓存使用 /tmp。

字体不在源码 ZIP 分发。其他机器需合法安装相同 TeX 组件和 Python PyMuPDF/Pillow。所有 40 页确实编译及渲染，未因依赖问题止于 TeX。独立 ZIP 临时目录重建结果另见 rebuild.json。
