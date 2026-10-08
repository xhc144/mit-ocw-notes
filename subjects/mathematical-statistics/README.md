# 数理统计与数据分析：MIT 18.650 中文整理本

十章连贯简体中文讲义和十一章官方作业完整中文题解，以 Philippe Rigollet 的 MIT 18.650 Statistics for Applications (Fall 2016) 为主源，按统计问题和先修关系重编。统一王者固定模板，原生文字、公式、自绘 TikZ 与保留来源的 PS7 原 QQ 图，带可点击目录和 PDF 书签。

## 成品

- `dist/main.pdf`: 唯一整书 PDF，110 个物理页（前置7页，正文与参考文献103页）。
- `dist/source.zip`: 完整可编辑 LaTeX 工程、11份作业题解、可重跑数值脚本、必要构建/来源/许可说明和两份许可可追溯的 PS7 图形裁切 PDF。无字体、旧成品、官方完整原件、编译缓存或受限 PCA 原件。
- 官方原件在仓库 `sources/18.650-fall-2016/`，与源码包分开保存。

## 范围

统计模型、收敛与误差控制、参数估计、最大似然、矩估计、参数检验、拟合优度、线性/多元/高维与非参数回归、贝叶斯、PCA、GLM。必要定义、条件、证明、推导与例子已补齐；LLN/CLT 等概率先修及经验过程定理的调用边界在正文明确声明。

自编补充: 简单随机与分层抽样、有限总体修正、均值/中位数/方差/分位数/箱线图、相关与配对、符号翻转和交换性标签置换检验、回归现象。用户资料库六页考纲第4页的统计条目已实际读取；这不是整份考纲或另一概率任务的交付。

主源当前内容页仅 **10 份 PDF，对应第1–24讲，共292个物理PDF页**；不是全站课程数量。新版矩估计15页、贝叶斯18页，旧版两份排除。Beamer 逐步显现按真实新增内容合并，轮换聚焦和新增图层另核。其余九份原件共275页归档；**PCA原件17页整份hold**，因其第14页有Nature/Macmillan单独授权图。本书不复制该图，PCA数学独立推导。当前主源的所有实质数学内容与例子有对应正文，课程管理、无内容标题与来源页统一归元数据/许可说明。

新增官方 PS1–PS11 共42源页：34个主问题、203个原印层级节点、181个编号末级问，另12个无编号要求（含PS11七个分布）。保留原编号、Fall2016及每份星期五中午截止日期。MIT官方明确没有公开作业答案，全部解答为本项目独立推导并经另一任务代理实际审读。印误和必要新增条件分别标注；没有外部教材缺失题干或依赖外部数据的待补题。PS7五幅QQ点图原本为内嵌JPEG，两份裁切PDF保留原图像字节及原图号/坐标文字，未新栅格化题面。

卷首列教师/学期/先修/课时/主题/作业日期和考试安排，官方Syllabus与Intro评分及先修版本有冲突，分别保留。没有发现公开考试PDF，不虚构考试题解。讲义与作业合计21个源PDF334页，20份317页可归档、PCA17页整份hold。

## 构建

需要 XeLaTeX、ctex/xeCJK、Fandol、CM Unicode OpenType (`cmunrm.otf,cmunbx.otf,cmunti.otf,cmunbi.otf`)、amsmath、amsthm、TikZ/PGFPlots、booktabs、longtable 等模板依赖。

```sh
export TEXMFHOME=/path/to/your/texmf
bash build.sh
```

本环境的已校验运行时依赖在 `/workspace/.local/texmf`。`build.sh` 在干净临时目录关闭shell escape，编译三次，只发布成功的 `dist/main.pdf`。源码内嵌的锁定类与仓库数值分析已验证模板逐字一致，不另设计字体、页边距、颜色或环境。字体不打包。

## 证据与许可

`source-manifest.json` 与 `assignment-manifest.json` 给出讲义/作业原链接、真实页数、SHA-256、许可及hold结果；`source-coverage.json` 和 `review/*author.md` 给出逐源/逐物理页去向。`review/*cross-review.md` 与 `review/ps*independent-review.md` 是独立任务代理对数学与来源覆盖的实际复核，非外部专家认证。最终机械、页面、链接与源码重编证据见 `QA.md` 与 `review/final-qa.json`。

改编采用 CC BY-NC-SA 4.0，具体署名、修改和第三方例外见 `LICENSE.md`。PCA受限原件、外部版权书、原考纲全文、字体和凭据均不上传。
