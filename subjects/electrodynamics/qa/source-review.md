# 电动力学来源独立审查

审查日期：2026-10-11。审查对象：`/tmp/electrodynamics-candidates/collection.json` 所列 63 份官方 OCW PDF、其文本提取和两门课程官网。未改写、上传或替换原件。本审查只写本文件。

## 结论与分发建议

官方 [OCW 许可页](https://ocw.mit.edu/pages/privacy-and-terms-of-use/) 当前为 CC BY-NC-SA 4.0。公开非商业包必须保留 MIT、实际作者、课程学期、来源链接、许可链接与修改说明。不能将 PDF 全部元素无条件声明为自有版权。

尤其需要依据官方 [第三方内容 FAQ](https://ocw.mit.edu/fairuse) 区分：无相反标记的 OCW 材料通常可依 CC 分发；“Courtesy of … Used with permission” 在 OCW 的明确用法中是覆盖 CC 的第三方材料，需携带特别署名；“All rights reserved”或明确 excluded from Creative Commons 才不自动得到再分发权。不能把所有教材参考、所有 courtesy、所有图片来源统一判为禁止。

| 文件 | 实际检查证据 | 建议 |
|---|---|---|
| `mit8_07f12_ln7.pdf` | 第1页明确源自 Jackson 3版题3.2，第1页自行排版概括问题，后续为 Guth 的推导；未检出明确 CC 例外 | 可保留 MIT 原讲义及来源署名；不要另从 Jackson 补录完整题面。商业教材引用本身不等于例外标记。没有做商业原书逐字对照，不能承诺概括文字完全无第三方表达 |
| `mit8_07f12_ln13.pdf` | [官方讲义目录](https://ocw.mit.edu/courses/8-07-electromagnetism-ii-fall-2012/pages/lecture-notes/) 明列 Hongsheng Chen、Min Chen，并附 Courtesy / Used with permission；原件第25页已删除受限图片 | 可保留现有原件，携带 **Courtesy of Hongsheng Chen and Min Chen. Used with permission.**；作者不能仅写两门课教师或 Guth。不能因 courtesy 排除整份，也不得恢复被删除图片 |
| `mit8_07f12_ln15.pdf` | 原件 PDF 第19–26页八次明示 Standard YouTube License、excluded from Creative Commons；第19页放大视觉核对确认视频截图和声明 | 完整未改原件排除公开 CC 包，保留官网链接。若以后制作删去受限元素的派生件，须明确修改和页码，不冒充原件；本次未制作 |
| `mit8_07f12_ln17.pdf` | 44页缩略图总览；放大第25页确认教材题11.4全文与 Figure 11.7 的扫描式片段，印为 p.450，文本提取错误作 p.50。其余若干页也有教材式扫描内容 | 保守暂不打包完整原件，保留链接并标“商业教材扫描内容，元素许可待核”。**不是**官方明示整份 CC 排除；不能把这一保守处理写成已证实违法。无商业原书对照或权利人单独许可，因此本审查不为这些扫描内容授予新权利 |
| `mit8_07f12_pset03.pdf` | 第1页题3 based on Jackson 2.11；其他题多为仅给 Griffiths 题号 | 可按未另标例外的 MIT 原 sheet 分发，不补录书中题面 |
| `mit8_07f12_pset04.pdf` | 第2页题3 patterned after Jackson 3.5，MIT 自行排版条件和任务 | 同上；改编来源信用应保留，不等于明确例外 |
| `mit8_07f12_pset05.pdf` | 第1页题1 based on Jackson 3.3，MIT 自行排版并有挑战提示 | 同上；未作 Jackson 逐字比较 |
| `mit8_07f12_pset08.pdf` | 第2页题5 based on Griffiths 6.9 与 Jackson 5.19，完整 MIT 排版条件；其他题仅给题号及教师提示 | 同上；保留作者、教材出处，不额外重构教材原题 |
| `mit8_07f12_ln12.pdf` | 60页缩略图总览；第6、9、53–56页已移除受限图；第3、4、7、11等页明标 Image by MIT OpenCourseWare；放大第42页实验图，未见另标许可例外 | 可保留 OCW 当前清理后的原件和署名。删除占位语是既往清理证据，不意味着剩余整份受限；引用论文图或图片出处也不能单独等同禁止。没有追溯每个实验图的权利链，不宣称逐图权利已穷尽 |

只含教材题号、页码或阅读章号的 MIT 作业单可以随原 MIT sheet 依适用 CC 分发；这些引用不会把商业教材题面带入包中。**不得**把题号引用描述成“完整题面”，不得根据教材记忆伪造未提供题面。`pset06` 第2页题5仅引用 Jackson 4.10，正是这一情形。

## 作者元数据必须修正

[8.311 Spring 2004 官方首页](https://ocw.mit.edu/courses/8-311-electromagnetic-theory-spring-2004/)、[教学大纲](https://ocw.mit.edu/courses/8-311-electromagnetic-theory-spring-2004/pages/syllabus/)、[讲义目录](https://ocw.mit.edu/courses/8-311-electromagnetic-theory-spring-2004/pages/lecture-notes/) 均明确教师为 **Leonid Levitov**。collection.json 课程条目和该课程各文件的 `Robert L. Jaffe` 归属错误，应删除并改为官方可证实的教师署名；具体 PDF 未单独署名时，可注明“授课教师 Leonid Levitov”，避免将教师字段夸大为每份材料逐字作者证明。

另经独立核对 [8.311 作业目录](https://ocw.mit.edu/courses/8-311-electromagnetic-theory-spring-2004/pages/assignments/)，12份作业解答明确为助教 **Chiyan Luo**，每项均有 **Courtesy of Chiyan Luo. Used with permission.**。应按此写作者及特别署名，可依上述 FAQ 纳入；不能全部归为 Levitov。期末解答没有由此证明作者，保持个体作者未明确，不猜测。

8.07 官方目录：ln1–11、ln14–16 为 Alan Guth；ln12、ln17 为 Min Chen；ln13 为 Hongsheng Chen 与 Min Chen。课程层面教师为 Alan Guth、Min Chen，不能把课程教师集合机械当作每份文件作者。

## 实际课程范围

[8.07 Fall 2012 讲义目录](https://ocw.mit.edu/courses/8-07-electromagnetism-ii-fall-2012/pages/lecture-notes/) 有17个讲义编号：向量分析、指标记号、静电边值问题与镜像法、球坐标分离变量、无迹对称张量与球谐、磁多极与物质磁性、负折射超材料和反向切伦科夫、波、势、辐射及复习。候选有34个 PDF，包含10份作业、两次测验及解答、期末试卷与公式单。官网概述含相对论，但不能据此声称这17份讲义提供了完整系统的相对论电动力学讲义。

[8.311 Spring 2004 课表](https://ocw.mit.edu/courses/8-311-electromagnetic-theory-spring-2004/pages/calendar/) 为25次 lecture，重心是守恒律、响应与色散、波导腔体、拉格朗日/哈密顿与 Noether、洛伦兹变换、辐射散射、辐射反作用、切伦科夫和同步辐射。[实际可下载讲义](https://ocw.mit.edu/courses/8-311-electromagnetic-theory-spring-2004/pages/lecture-notes/) 只有4份补充笔记（wave guides、field oscillators、power spectrum、charge moving in a dielectric），并非25讲完整讲义。29份候选 PDF 为这4份、12份作业及12份解答、期末及解答。官方说明主要依教材授课，因此这一公开源集合不能宣传为完整教材替代品。

## 检查边界与元数据质量

- 全63份：核对 collection 条目、页数信息，扫描全部现有文本提取中的许可/来源词；未对全部63份逐页做高分辨率视觉审查。
- 重点原件：直接打开 PDF 渲染 ln12、ln13、ln15、ln17；前三者或后者的缩略图总览与重点页放大；阅读 ln7 和四份改编作业的 PDF 提取内容。文本检索不是对扫描图文字的穷尽检查。
- 8.311 `ps1`、`ps8` 文本提取有乱码，collection 的 exception_markers 中乱码包含“©”不构成版权证据。未人工逐页判定这两份，不能把它们列作明确版权例外，也不能以文本无结果代替视觉核查。
- `quizsol1` 的“excluded”是数学上排除解支，属于检索误报；ln8/ln9 的 Jackson 书目和公式引用也是来源标记，不是许可例外。
- 未购买、下载或对照商业教材；未取得权利人新增许可；没有为任何公开重新打包主张独立 fair use。ln17 暂停建议属对真实扫描内容的保守包边界，不应扩展成对所有教材改编的禁令。

最终打包建议：明确排除 ln15 完整原件，保守暂缓 ln17 完整原件；ln13 保留特别署名后可纳入；ln12 保留当前删图版本；ln7、四份 MIT 改编作业与仅含教材题号的 MIT sheets 不因这些引用自动排除。其余文件只获得上述筛查级证据，后续若发现明示例外应按元素修正记录。

本批最终建议为 **61份公开 PDF**（63份候选中排除 ln15 完整原件、暂缓 ln17 完整原件），前提是补齐 ln13、12份 Chiyan Luo 作业解答的特别署名与正确作者元数据。这一数量是本批打包边界，不表示完成了61份每个图像的独立权利链审计。
