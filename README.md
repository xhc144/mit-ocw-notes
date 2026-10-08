# MIT OCW 讲义归档与中文重编

本仓库用于个人非商业学习，保存授权归档的 MIT OpenCourseWare 课程讲义及其中文原生 LaTeX 重编成果。仓库保持私有。

## 讲义下载

| 学科 | 官方原讲义 | 中文整册 |
|---|---|---|
| [数值分析](subjects/numerical-analysis/) | [18.330 原件](sources/18.330-spring-2012/)：7章、99页 | **59页** · [下载中文PDF](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/numerical-analysis/dist/main.pdf) · [源码ZIP](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/numerical-analysis/dist/source.zip) |
| [数值代数](subjects/numerical-linear-algebra/) | [18.335J 原讲义](sources/18.335j-spring-2019/)：25份PDF、227页；核心12份59页 | **67页** · [下载中文PDF](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/numerical-linear-algebra/dist/main.pdf) · [源码ZIP](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/numerical-linear-algebra/dist/source.zip) |
| [最优化](subjects/optimization/) | [6.253原稿](sources/6.253-spring-2012/)及[线性规划补充](sources/15.053-spring-2013/) | **66页** · [下载中文PDF](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/optimization/dist/main.pdf) · [源码ZIP](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/optimization/dist/source.zip) |
| [数理统计](subjects/mathematical-statistics/) | [18.650 原讲义与来源清单](sources/18.650-fall-2016/)：当前10份PDF、24讲、292源页；九份原件275页归档，PCA原件17页保留链接 | **66页** · [下载中文PDF](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/mathematical-statistics/dist/main.pdf) · [源码ZIP](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/mathematical-statistics/dist/source.zip) · 10章涵盖统计模型与参数推断、极大似然与矩估计、检验与拟合优度、回归、贝叶斯、PCA和GLM · [内容及核验详情](subjects/mathematical-statistics/README.md) |
| [拓扑](subjects/topology/) | [18.S190 度量空间及选读补充](subjects/topology/sources/)：主课六讲，另有原习题及18.901、18.102选读；范围见详情 | **105页** · [下载中文PDF](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/topology/topology.pdf) · [源码ZIP](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/topology/topology-source.zip) · 15章涵盖度量空间、一般拓扑、积与商、基本群、覆盖空间、曲面与流形入门，含58道完整题解；完整微分几何与同调体系未纳入 · [内容及核验详情](subjects/topology/README.md) |
| [概率论](subjects/probability/) | [18.600 原讲义与来源清单](sources/18.600-fall-2019/)：37份主讲义及1份补充，共2,413源页 | **108页** · [下载中文PDF](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/probability/dist/main.pdf) · [源码ZIP](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/probability/dist/source.zip) · 12章及综合练习涵盖计数、条件概率、分布、期望、极限、有限马尔可夫链、熵和鞅 · [内容及核验详情](subjects/probability/README.md) |
| [实变](subjects/real-analysis/) | [官方来源与许可](sources/real-analysis/)：18.125 Fall 2003：24份讲义、95页 | **72页** · [下载中文PDF](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/real-analysis/real-analysis.pdf) · [源码ZIP](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/real-analysis/real-analysis-source.zip) · 测度、可测函数、Lebesgue积分、收敛定理、Fubini、Lp、卷积与微分；9章，33道带解答练习 · [范围与核验](subjects/real-analysis/README.md) |
| [复变](subjects/complex-analysis/) | [官方来源与许可](sources/complex-analysis/)：18.04主线及18.112选读：37份原讲义、325页 | **50页** · [下载中文PDF](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/complex-analysis/complex-analysis.pdf) · [源码ZIP](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/complex-analysis/complex-analysis-source.zip) · 全纯函数、Cauchy理论、级数、奇点与留数、辐角原理、解析延拓及保角映射；14章，38道带解答习题 · [范围与核验](subjects/complex-analysis/README.md) |
| [泛函](subjects/functional-analysis/) | [官方来源与许可](sources/functional-analysis/)：18.102 Spring 2021：125页合订本、23讲 | **40页** · [下载中文PDF](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/functional-analysis/functional-analysis.pdf) · [源码ZIP](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/functional-analysis/functional-analysis-source.zip) · Banach/Hilbert空间、算子、Hahn–Banach、统一有界、开映射/闭图、弱拓扑、紧算子与紧自伴谱；含30个题解 · [范围与核验](subjects/functional-analysis/README.md) |


## 第一阶段

优先整理应用数学的三个具体学科，每个学科最终形成一本独立的中文 TeX 源文件与 PDF：

1. 数值分析
2. 数值代数
3. 最优化

同一学科可以参考多个 OCW 源课程。源课程逐门登记，不以课程数量代替学科成果数量。

## 目录约定

- `sources/<course-id>/`：源课程登记、原始讲义、课程页与资料页来源信息
- `subjects/numerical-analysis/`：数值分析中文讲义及构建材料
- `subjects/numerical-linear-algebra/`：数值代数中文讲义及构建材料
- `subjects/optimization/`：最优化中文讲义及构建材料
- `manifests/`：课程清单、文件来源、许可证、校验和及归档进度
- `manifests/metadata/`：官方全站课程目录清单及归档范围核查说明
- `scripts/`：增量下载与本地完整性校验工具
- `LICENSES/`：授权说明及第三方例外记录

## 完成标准

下载成功须有实际文件及 SHA-256 校验记录；中文稿须使用可编辑的原生 LaTeX，完成数学审校、编译及页面检查后才标为完成。尚未下载或验证的条目保持待处理状态。修订在原文件路径继续，保留 Git 版本历史。

## 来源、署名与许可

MIT OCW 的默认内容许可为 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)，详见 [MIT OCW 使用条款](https://ocw.mit.edu/pages/privacy-and-terms-of-use/)。归档时保留每门课程的名称、教师／原作者、学期、源页面、原始文件 URL、许可和权利说明；中文重编明确注明翻译、重排、增补或其他改动，不表示 MIT 或作者认可本项目。

原文件中单独标注的第三方材料或许可例外不由上述默认许可覆盖，须逐项保留并核实。中文重编中基于 OCW 的改编部分遵循对应署名、非商业及相同方式共享要求；仓库私有状态不替代许可证义务。

## 当前状态

截至2026-10-08，已核验并交付 **9册中文整书，共633个PDF物理页**：数值分析59页、数值代数67页、最优化66页、数理统计66页、拓扑105页、概率论108页、实变72页、复变50页、泛函40页。下表提供PDF下载、源码包及各科学习范围；册数只统计已有实际成品并完成交付核验的学科，原件下载不计作中文讲义完成。

首批数值分析、数值代数、最优化三科共192页，对应41份可归档原PDF已提交，6份有第三方权利例外的原文件保留来源链接。全站归档仍在分批进行，课程目录总量不能用作已交付讲义分母。

官方站点地图清单登记了 2,587 个课程目录项。这是课程站点目录数量，不是讲义数量、已下载文件数量或可交付译文数量。详细目录及计数含义见 `manifests/metadata/`；实际文件归档进度由文件清单单独记录。


原件的逐文件官方链接、页数和SHA-256见[数值分析来源清单](manifests/numerical-analysis-sources.json)。
