# 概率论与随机变量

Scott Sheffield 的 MIT 18.600 (Fall 2019) 简体中文重构本。正式单册 PDF 为 [dist/main.pdf](dist/main.pdf)，可编辑且可独立编译的源码包为 [dist/source.zip](dist/source.zip)。全书108个PDF页（前置5页、正文及参考文献103页），12个正文章节，加综合练习与逐讲对应一章；目录、书签和来源链接可点击。

原课37份主讲义与1份补充讲义共2,413个实际PDF页，包含渐显重叠和重复复习页。逐文件原始直链、资源页、版权状态、页数、字节数与SHA-256见 [source-manifest.json](source-manifest.json)；原件归档在 [../../sources/18.600-fall-2019/](../../sources/18.600-fall-2019/)。第16、29讲为考试、没有讲义，旧课号18.440不另算学科。本批来源范围是讲义，独立作业集和考试卷未纳入。

正文按依赖关系完整重构计数、公理、条件概率、分布、期望、极限、有限马尔可夫链、熵及鞅。原课重复复习合并，自设例题与练习保留训练目标，给出完整计算和解答；补充核心证明及条件，勘误登记在qa/。第三方外书题面和受限图不复用。全书原生文字/数学公式与3幅TikZ图，没有整页截图。署名、改编说明和CC BY-NC-SA 4.0见 [LICENSE.md](LICENSE.md) 与PDF前言。

## 本地编译

需要XeLaTeX、ctex/Fandol、Computer Modern Unicode的cmunrm/cmunbx/cmunti/cmunbi字体以及TikZ/PGFPlots。字体是运行依赖，不随ZIP打包。已配置这些依赖时执行：

```bash
bash build.sh
```

输出为dist/main.pdf。源码ZIP解压后进入probability/即可执行，无须其他学科或仓库文件。main.tex内置完整锁定类，chapters/通过input组织。

系统缺少中文TeX资源及模板字体时，可使用包内哈希固定的本地依赖脚本，不修改系统安装：

```bash
python qa/bootstrap_tex.py --texmf-dir /tmp/probability-texmf --cache-dir /tmp/probability-tex-downloads
TEXMFHOME=/tmp/probability-texmf XDG_CACHE_HOME=/tmp/probability-cache bash build.sh
```

脚本下载的字体/TeX资源仅安装到指定本地目录，校验失败会停止。不可偷偷更换字体或锁定样式。固定王者样式与已交付numerical-analysis/main.tex的锁定类一致，基线保存在qa/style-baseline.tex。

## 质量记录

[qa/QUALITY.md](qa/QUALITY.md)汇总38/38份来源、12/12章作者自查和独立交叉审校、自动版式检查以及最终108/108页的实际视觉覆盖。自动报告本身明确不验证数学。一般条件期望存在性、Lévy连续性、一般有限均值强律及布朗运动构造等调用边界在正文及质量记录中说明。

仓库中的qa/clean-rebuild.json和qa/release.json保存正式ZIP的干净重编、页面/文字一致性、包成员与产物哈希；这两份产物自身的校验记录不嵌入ZIP，以避免自指哈希。历史阶段记录保留在PROGRESS.md，旧失败尝试未冒充最终通过。
