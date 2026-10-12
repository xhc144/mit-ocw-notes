# 编译与复核

依赖：Python 3、XeLaTeX、ctex/xeCJK、Fandol OTF、CM Unicode OTF、amsmath、amsthm、geometry、fancyhdr、enumitem、xurl、hyperref、TikZ、PGFPlots、longtable、booktabs。建议完整TeX Live；正文保持仓库已批准锁定模板。字体不得随源码包再分发。

解压源码ZIP后在包根运行 `python3 tools/build.py --out build`。构建在干净临时目录复制所有TeX输入、禁shell escape，至少两轮并直到aux/toc/out收敛，遇字体缺字、字体警告或盒溢出停止。输出 build/main.pdf 与 standalone-build.json。编译不需网络或其他学科。

当前环境用TeX Live 2024兼容的ctex/xeCJK等包在临时TEXMFHOME下补齐依赖，未修改系统配置和模板字体。额外TeX安装是外部依赖，未进ZIP；完整本地TeX环境不需这个路径。

运行 `python3 tools/physics_checks.py` 重做需要NumPy的有限数值实验与向量图；PDF正常重编译使用已经包含的figures/*.tex，不必先重算数值。图数据、样本与误差见 qa/numerical-checks.json。QA将编译、链接、数学范围、逐页视觉、洁净ZIP重编译和远端哈希分别记录，不以自动脚本当成一般物理证明。
