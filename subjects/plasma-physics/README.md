# 等离子体物理：MIT 公开课程中文自学讲义

本卷在一份中文 LaTeX PDF 中连贯讲解单粒子运动、碰撞与输运、流体与 Vlasov、冷波和 Landau 阻尼，再进入 Grad–Shafranov 平衡、磁通守恒、加热及 MHD 稳定性。理论为 18 章；作业与试卷按课程和年份分编，给完整公开题面、物理假设及独立中文解答，不按课堂节次拆散成大量 PDF。2002、2005 的基础历史题与 2003 年的 MHD 历史期末也已纳入主卷。

- [中文主 PDF](dist/plasma-physics-zh.pdf)
- [可编译源码 ZIP](dist/plasma-physics-source.zip)
- [编译与数值复现](BUILDING.md)
- [冻结来源清单](source-manifest.json)及[历史补编清单](qa/historical-supplement-freeze.json)
- [作者与许可](LICENSE.md)
- [历史题去重及官方答案逐页配对](qa/historical-supplement-independent-review.md)

## 课程与实际覆盖

| 课程、学期 | 主要署名 | 讲义及考核选编 | 实得课程 PDF |
|---|---|---|---:|
| [22.611J Fall 2003](https://ocw.mit.edu/courses/22-611j-introduction-to-plasma-physics-i-fall-2003/) | Ian H. Hutchinson、Jeffrey Freidberg，逐件以原件署名为准 | 五章理论主题、PS1—6 全部24题；三份模拟使用说明只解读方法 | 14 |
| [22.611J Fall 2006](https://ocw.mit.edu/courses/22-611j-introduction-to-plasma-physics-i-fall-2006/) | Ron Parker 及历史文件实际署名作者 | 当期 PS1—9 全部25题、期中3题、期末4题；2005 历史新增9题；2002 历史新增39题及其官方扫描答案 | 48 |
| [22.615 Spring 2007](https://ocw.mit.edu/courses/22-615-mhd-theory-of-fusion-systems-spring-2007/) | Jeffrey Freidberg 及原件署名教师 | 第1—22讲和补讲主题；HW4完整1题、期中1道综合题、期末2个综合分题；2003 MHD 历史期末1道五步骤综合题及官方答案 | 37 |

99 件课程 PDF 已逐件冻结 URL、页数、SHA256 和来源角色；34 件历史考核及3件模拟说明是其中的子集，不重复合计。按一张考试内的完整综合组计，正文 **109 组**：原精选60组、2005新增9组、2002新增39组、2003 MHD 综合题1组；若把后者的原编号1—5分别计，则为113个编号任务。2005 年18题、2002 年2题与已选题完全重复，交叉索引而不重排；小问不另算题。2002 八套作业和期中期末共10件扫描官方答案，2003 MHD 另1件，共11件、125 PDF 页。中文解答仍为编者独立推导，2005 历史题没有取得相应官方答案，绝不混称。

## 缺项与可核查的限制

22.615 五份作业中有12条商业教材题号引用，公开文件未给题面：5.5／5.8／5.9、6.2／6.5／6.11、6.17／6.18、8.6／8.7、9.3／9.4。2005 PS5 的两条仅引用缺失的前一年 Quiz2；2002 PS3 Q4 只是“下周做”的占位。这些均不编造。三份 2003 模拟说明只取得 PDF，未取得其所提历史程序或运行数据，也未冒称运行原模拟。

2006 PS4 指向的 2002 NRL Formulary 原 DTIC 外链本环境返回403；本次从大学公开镜像逐式核对同版并恢复正文，镜像及版本核验见[QA](qa/nrl2002-mirror-verification.json)，未收录手册全文。2002 PS8 题面与手写答案中的热速定义、归一化及数值前因子不完全自洽，中文题解保留印刷目标和逐字算子核算的区别。2005 SOL 题未给课堂热导常数，保留系数和适用条件，不制造“官方靶板数值”。早期 MHD 题的理想壁模型与 2007 当期题条件各异，分别计算。

## 验证与使用

使用 XeLaTeX 构建；所有交叉引用需收敛，且无缺字、字体替换或溢出。冷波图采样、2003 MHD 理论极限、原题数值已独立复核；本卷的图为新绘 TikZ／PGFPlots 或原创矢量图。对最终 PDF 做逐页渲染、书签与链接检查，源码包在新解压目录实际重编；远端提交后下载并核对 PDF 页数／SHA256 和 ZIP CRC。实际发布版证据见 `qa/revision-validation.json`、`qa/final-visual-review.json`、`qa/clean-zip-build-revision.json`、`qa/delivery-verification-revision.json`。此前同名 QA 文件记录初版，不应与此次增补版哈希混用。

MIT OCW 原课程许可与逐件例外见[许可文件](LICENSE.md)。本稿为 AI 辅助的非官方中文重编，遵守署名、非商业及相同方式共享（CC BY-NC-SA 4.0）；不收入第三方受限教材或原课整页背景。
