# 概率论与随机变量

Scott Sheffield 的 MIT 18.600 (Fall 2019) 简体中文重构本。正式单册 PDF 为 [dist/main.pdf](dist/main.pdf)，可编辑且可独立编译的源码包为 [dist/source.zip](dist/source.zip)。全书237个PDF页（前置9页、正文及参考文献228页），保留原12个理论章及综合练习，增补课程信息、原40项教学进度、作业与考试完整题解；目录、书签和来源链接可点击。

原课37份主讲义与1份补充讲义共2,413个实际PDF页，包含渐显重叠和重复复习页。作业、考试及补充资源另实核65份、436页，其中55份368页归档，10份混有Ross教材题面的作业原件整份hold，只保留源链接与校验记录。可分发归档合计93份、2,781页。逐资源直链、版权状态、页数、字节数与SHA-256见 [source-manifest.json](source-manifest.json) 和 [course-materials-manifest.json](course-materials-manifest.json)；归档在 [../../sources/18.600-fall-2019/](../../sources/18.600-fall-2019/)。第16、29讲无讲义，旧课号18.440不另算学科。

10份作业及鞅补充共134道顶层题，排除17道Ross教材题面后完整收录117题、169个正式末级子问、281项要求输出。数学、说明与图形有278项解答支持；3项真实采访仍须读者执行，书中参数化推导与示例数据明确区分。27份考试卷完整覆盖199道原编号题、582个末级子问，含1道附加题；1道整题完全重复用可点击回指保留两处来源。作业解答为AI补充，考试按官方答案重构并补齐过程；Practice中13个没有实质官方答案的子问明确标注AI补解。逐题来源和解答位置见qa/coverage-*.json。

正文按依赖关系完整重构计数、公理、条件概率、分布、期望、极限、有限马尔可夫链、熵及鞅。原课重复复习合并，自设训练题与官方题目来源区分；补充核心证明及条件，勘误登记在qa/。第三方外书题面和受限图不复用。全文为原生文字/数学公式及TikZ图，没有整页截图。署名、改编说明和CC BY-NC-SA 4.0见 [LICENSE.md](LICENSE.md) 与PDF前言。

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

[qa/QUALITY.md](qa/QUALITY.md)汇总38/38份讲义、65/65份补充资源、原12章交叉审校、6/6组新增题解独立审校、自动版式检查与逐页视觉证据。自动报告本身明确不验证数学。一般条件期望存在性、Lévy连续性、一般有限均值强律及布朗运动构造等调用边界在正文及质量记录中说明。

仓库中的qa/clean-rebuild.json和qa/release.json保存正式ZIP的干净重编、页面/文字一致性、包成员与产物哈希；这两份产物自身的校验记录不嵌入ZIP，以避免自指哈希。历史阶段记录保留在PROGRESS.md，旧失败尝试未冒充最终通过。
