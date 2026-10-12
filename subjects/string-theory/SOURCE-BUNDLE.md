# 独立源码包

在本目录运行 `python3 scripts/build.py`，需完整安装带 ctex、Fandol、Computer Modern Unicode 与 TikZ/PGFPlots 的 TeX Live/XeLaTeX。脚本执行三次无 shell escape 的隔离编译。编译不需网络、源课程 PDF、系统以外字体或数值计算库。

包内保留中文正文、入选完整题面和解答、绘图用 CSV、模板、数值复核脚本、来源及许可。README 中 PDF/ZIP、clean-rebuild.json 和发布回执的链接指向仓库版本；包本身不嵌套 PDF/ZIP，也不打包编译缓存或字体。

有限数值复核需 numpy/scipy；其结果已随包给出。逐页视觉自查记录为本模型检查，尚未进行独立专家终审。
