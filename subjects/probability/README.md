# 概率论与随机变量

Scott Sheffield 的 MIT 18.600 (Fall 2019) 中文重构本。单册正式PDF位于 `dist/main.pdf`，可编辑、自足源码包位于 `dist/source.zip`。当前仍在编写与复核，阶段记录见PROGRESS.md，正式产物存在且通过质量记录后才表示交付。

原课37份主讲义与1份补充讲义共2,413个实际PDF页（含渐显重叠与重复页），逐文件直链、版权状态、页数及SHA-256见source-manifest.json；原件在../../sources/18.600-fall-2019/。旧号18.440不另立科。

正文按依赖关系重构为12章，加综合练习和逐讲来源对应。原课的复习重复内容合并，核心计算完整推导；第三方外书原题面与受限图不复用。章节TeX由main.tex逐一input，数学图为TikZ，没有整页截图。署名与CC BY-NC-SA 4.0说明见LICENSE.md和PDF前言。

## 本地编译

需XeLaTeX、ctex/Fandol、Computer Modern Unicode的cmunrm/cmunbx/cmunti/cmunbi字体及tikz/pgfplots。字体仅为运行依赖，不随源码ZIP打包。执行 `bash build.sh`，输出dist/main.pdf。系统缺少中文TeX资源时，可设置TEXMFHOME为自行安装的本地TeX树；不得用另一字体或样式偷偷替代。

固定王者样式基于已交付的numerical-analysis/main.tex锁定类，qa/style-baseline.tex保存该基线。目录与书签均可点击。质量记录区分数学复核、自动检查、实际视觉查看和ZIP干净重编，不能由编译通过推定数学正确。
