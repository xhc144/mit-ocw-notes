本册使用 XeLaTeX、固定王者模板、CTeX/Fandol 中文与 Computer Modern Unicode 英文字体。不得用替代字体的编译结果冒充本版。源码 ZIP 解压后，以解压目录为工作目录；不需要仓库其他学科、原始970页PDF或联网才能编书。

依赖：Python 3.10+，PyMuPDF、Pillow；XeLaTeX 及 ctex、fontspec、amsmath/amssymb/amsthm、mathrsfs、geometry、setspace、fancyhdr、enumitem、needspace、xurl、hyperref、tikz、pgfplots、booktabs、longtable、etoolbox。字体文件 cmunrm/cmunbx/cmunti/cmunbi.otf、FandolSong/FandolKai 等应在 TeX 可搜索目录。不分发字体。

```bash
bash tools/build.sh
```

该命令先实际重算三个数值模型并写数据/表格，再进行模板、引用、日志、PDF边界与全页渲染检查。成功后生成 `introductory-mechanics.pdf`。仅手工编译时至少两次运行 `xelatex -no-shell-escape -halt-on-error -output-directory=build main.tex`，但这不替代校验工具。

本次环境：Debian XeTeX 3.141592653-2.6-0.999994 (TeX Live 2022)，缺少的宏包及 cm-unicode 在 `/workspace/.local/texmf`；已用 `TEXMFHOME=/workspace/.local/texmf bash tools/build.sh` 实测。此绝对目录是本次机器说明，不是源码依赖；其他系统正常 TeX Live 安装无需该设置。

ZIP 重建验收比较页数、逐页抽取文字及渲染像素；PDF元数据时间可能改变，不要求另一次编译的PDF字节哈希相同。每页PNG在 `build/`，工具报告仍如实保留 mathematical_verification=false / visual_review=not_performed；独立内容审稿与人工全页审校另存 `qa/`。脚本渲染不是人工查看证明。

完整 OCW 来源存于仓库 `sources/introductory-mechanics/`，冻结清单在 `manifests/introductory-mechanics-sources.json`。在完整仓库运行 `python3 subjects/introductory-mechanics/tools/acquire.py` 可恢复缺失原件并核冻结哈希；远端字节变更会停止，不重新选来源或自动接受新哈希。
