# 基础电磁学中文合订本

- [下载中文 PDF](introductory-electromagnetism-zh.pdf)
- [下载可编辑 LaTeX 源码 ZIP](introductory-electromagnetism-zh-source.zip)
- [逐份来源与许可清单](../../manifests/introductory-electromagnetism-sources.json)

主线采用 MIT OCW **8.02 Physics II: Electricity and Magnetism，Spring 2007**。现为 **80 个 PDF 物理页**（卷首 i–vi，正文及附录 1–74），12 章连续理论与 11 章习题课合订，从电荷、电场与电势，经过导体、介质、直流电路、磁场和感应，发展到交流电路、麦克斯韦方程、电磁波、干涉与衍射。正文补充需要的数学工具；官方先修是 8.01 经典力学。

两批材料清单均在下载前冻结：全部 **14 章长篇 OpenTextbook Course Notes**（540 原页），以及全部 **36 份课堂摘要和 11 份周五习题课**（161 原页），合计 **61 份 PDF、701 原页**。长篇教材的实质理论、附录及 **39 个 Worked Examples、70 个 Solved Problems，共 109 个原例**已按知识依赖整合进本册。原教材附有这些例题的官方解答；本册中文推导与解答由 AI 独立重编，原解仅作为核对来源，并注明确认的原件误印或近似。

周五习题课合并重复答题页后为 **34 题组、169 个叶级小问**，均有中文题面和 **AI 独立解答**，未取得这 11 份习题课的对应官方答案。目录、课历、教师、考核及逐份主题映射在同册。原件的旧页头、编号遗漏和公式笔误逐项说明，未据此猜造缺题。

**184 个文末自测对象的边界：**原教材另有 **65 个 Conceptual Questions 和 119 个 Additional Problems**，完整题意已逐项登记并保留在官方原件中；其中新方法已融入正文，但本版尚未逐题收入这 184 题的完整中文题面与答案。因此，109 个已重编教材例题、169 个已解周五小问与 184 个文末自测对象应分别理解；701 原页也不表示逐页逐字译完。

本轮未选周一/周三小组题、实验指导、幻灯片及在线平台题。官方不公开每周书面作业；习题中的 Sample Exam Question 是练习，不冒充正式试卷。8.022 Fall 2004 仅核课程信息。高阶边值与辐射可继续阅读同仓库的电动力学册。

原资料署名 MIT / MIT OpenCourseWare；材料作者为 Peter Dourmashkin、Eric Hudson、Sen-Ben Liao 及课程署名教师团队。中文翻译、重排、展开推导、独立题解及新增 TikZ 图属于修改，按 **CC BY-NC-SA 4.0** 发布，保留署名、非商业与相同许可。summary_w01d1 第 2 页风场图的 National Oceanic and Atmospheric Administration 署名在原件保留，中文稿未复制该图。不是 MIT 官方中文教材，也不表示 MIT 认可。

核对记录：[长篇教材来源](qa/textbook-source-review.md)、[109 原例逐项复核](qa/textbook-example-recheck.md)、[理论内容终审](qa/textbook-theory-final-review.md)、[周五习题逐问复核](qa/assessment-review.md)、[80 页逐页视觉](qa/visual-review.md)、[教材有限数值复现](qa/textbook-numerical-reproduction.json)、[源码 ZIP 实际重建](qa/rebuild.json)、[交付范围与文件哈希](qa/release.json)。自动检查和有限数值复现不能代替内容审查、视觉审查或一般证明。

重建需要 XeLaTeX、ctex、xeCJK、zhnumber、Fandol、Computer Modern Unicode、TikZ/PGFPlots，以及 Python 的 PyMuPDF 与 Pillow。字体通过合法的 TeX/系统发行版安装，不在 ZIP 分发。解压后执行：

```bash
bash build.sh
```

产物为 `build/main.pdf`，检查为 `build/validation_report.json`。脚本在此共享环境中会使用已有 `/workspace/.local/texmf`；其他机器使用其已安装的 TeX 环境。
