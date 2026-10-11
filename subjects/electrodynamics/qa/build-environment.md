# 实际编译环境与兼容依赖

环境引擎：XeTeX TeX Live 2025/dev/Debian；LaTeX内核2024-11-01 patch level 2。初始环境没有ctex、xeCJK、zhnumber、Fandol和Computer Modern Unicode。

直接从CTAN下载的2026版ctex要求更新内核，未用于成品。兼容宏包使用CTeX官方仓库2024-11-27提交：

https://github.com/CTeX-org/ctex-kit/tree/1ee66c6f130802d3400f893db01fd6a6701ab164

下载该提交的源码，在其ctex、xeCJK、zhnumber目录，以官方support目录同时加入TEXINPUTS和LUAINPUTS，运行`luatex -interaction=nonstopmode ctex.dtx`（另外两包同理）完成docstrip生成。必须用LuaTeX生成ctex的编码文件；plain TeX/XeTeX的错误尝试没有用于成品。

字体从CTAN直连镜像的`fonts/fandol.zip`及`fonts/cm-unicode.zip`下载，仅供本地编译，不在仓库和源码ZIP中分发字体。宏包/字体下载源为https://ctan.math.illinois.edu/（CTAN镜像）；需要的包按各自许可证使用。

实际验证命令在学科目录执行：

```bash
TEXINPUTS=/tmp/electrodynamics-texmf-2024//:/tmp/electrodynamics-texmf//: \
OPENTYPEFONTS=/tmp/electrodynamics-texmf//: \
XDG_CACHE_HOME=/tmp/electrodynamics-fontcache \
python vendor/math-latex-typesetting/scripts/validate.py main.tex --out build
```

正常完整TeX Live中文安装可直接运行README中的命令，无需临时路径。用户固定模板类未被修改，未替代字体，XeLaTeX以禁用shell-escape的受控流程编译并达到引用收敛；实际报告为自动PASS。自动报告不认证数学或人工视觉质量，两者另有报告。
