# 核与粒子物理（中文自学讲义）

主 PDF 将核物理与粒子物理分编，不以现有 QFT 卷替代粒子物理。18章正文后收录完整选定作业、三份期中和20套习题课题面与解答，共135个原题级问题（子问不另计）：8.701六套作业28题、22.02九套作业51题、2010/2011/2012期中13题、8.701习题课43题。

- [中文 PDF](dist/nuclear-particle-physics-zh.pdf)
- [可重新编译的 LaTeX 源码 ZIP](dist/nuclear-particle-physics-source.zip)
- [编译说明](BUILDING.md)
- [冻结来源清单](source-manifest.json)
- [习题课增补来源清单](qa/recitation-coverage-freeze.json)
- [考试原题图来源](qa/exam-figure-provenance.json)
- [独立数学审读](qa/independent-review-8701.md)
- [全部目录与书签检查](qa/pdf-links.json)

## 实际覆盖

|课程|教师/学期|本卷收录|实际公开文件|
|---|---|---|---|
|[8-701-introduction-to-nuclear-and-particle-physics-fall-2020](https://ocw.mit.edu/courses/8-701-introduction-to-nuclear-and-particle-physics-fall-2020/)|Markus Klute|章节0—10讲义主题、当期PS1—6、20套习题课43题和官方答案重编|原清单118件PDF，增补习题课题面与答案40件PDF；逐件URL/哈希/页数见两份清单|
|[22-02-introduction-to-applied-nuclear-physics-spring-2012](https://ocw.mit.edu/courses/22-02-introduction-to-applied-nuclear-physics-spring-2012/)|Paola Cappellaro|核物理章节1—8主题、PS1—9、三个年份期中题与对应解答|34件PDF，逐件URL/哈希/页数见清单|

## 范围与未覆盖项

课程站点列出一门课，不等于每类文件都可下载。本清单先实际取得文件再冻结选编。8.701的20次recitation题目及答案已全部按原编号纳入；其课堂视频、讲座逐字稿不计作已编入。22.02的Final链接在该站点实际指向2010/2011期中答案，未取得独立期末题面，所以没有编造期末卷。题目引用核数据的条目由AME2020/NUBASE2020官方表核验，原表不捆绑。未将第三方教材和受限图片收进源码包。

本卷讲义为按概念组织的中文重编，完整选定题面保留原题条件；官方答案重编与独立补解分别标注。对源件的符号、数值或条件冲突明确给出修正与限制，例如动量测量、浅势阱、氘核方阱三参数不相容、离轴中微子能谱和屏蔽势模型。新示意图使用可编辑TikZ/PGFPlots；三道期中题的四幅原始题图保留为裁切矢量图，出处、页码及哈希见图源清单。

## 署名与许可

MIT OpenCourseWare课程作者和各文件链接见清单及卷末；8.701官方解答作者中含Tianyu Justin Yang，22.02由Paola Cappellaro授课。课程中文改编和本项目新增正文按[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)发布，须署名、非商业和相同方式共享。本稿为AI辅助的非官方中文重编，不是MIT官方译本。逐件例外见`qa/license-exceptions.json`；41件课件存在排除图片或all rights reserved提示，均未原样转载其图片。项目保留源许可与作者，不把第三方材料重新授权。

## 验证

全卷XeLaTeX交叉引用收敛；固定版式、缺字/溢出/字体检查；全部目录书签跳转；全部物理页逐页渲染审读；独立粒子题推导及核物理敏感数值抽检。源码包在干净目录重新编译，发布后远端下载比对哈希与页数，结果记录于`qa/delivery-verification.json`。视觉旧版记录保留并明确其哈希，最终版结果单独记录；自动检查不冒称全部数学已由独立审稿人证明。
