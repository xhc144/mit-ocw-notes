# 电动力学中文讲义

入口是一本连续的中文 PDF，理论与题解合订。

- [下载中文 PDF](electrodynamics-zh.pdf)
- [下载可编辑 LaTeX 源码 ZIP](electrodynamics-zh-source.zip)
- [查看实际覆盖及缺失题面](coverage.md)

主线采用 MIT OCW **8.07 Electromagnetism II，Fall 2012**（Alan Guth、Min Chen）。17章涵盖矢量分析、静电与边值问题、多极展开、介质、稳恒磁场、麦克斯韦方程、能量动量、电磁波和偶极辐射；后接十次作业中取得自含题面的27项、两次Quiz的9题及本科期末5题。Quiz采用官方解答中文整理，作业和本科期末为明确标注的AI独立解答。不是MIT官方中文讲义，也不表示MIT认可。

**向后进阶**采用8.311 Spring 2004（Leonid Levitov）的选讲资料，并纳入三道期末题及官方解答的中文SI换算。其12套作业和官方解答已归档，尚未逐题中文重编；协变理论、色散关系和相对论总辐射功率的证明范围在书中说明。不能把本版当成完整8.311中文教材。8.312未取得可核验官方原件。

纯教材题号不视为取得题面。缺少完整条件的项目逐项列在书中和覆盖清单；没有补造商业教材原题。官方Quiz2解答的磁四极系数笔误公开说明并修正。

中文稿使用用户固定中文LaTeX模板，全部新增图为TikZ/PGFPlots可编辑图。内容审查、编译检查、目录链接检查和实际PDF视觉检查各自记录，不用编译成功代替数学证明。

<details>
<summary>原始资料、许可证与核对入口</summary>

已实际校验并归档61份官方PDF，共474页，包括8.07讲义、十份作业、两个Quiz及官方解答、本科期末及公式表，及8.311四份补充笔记、12套作业和解答、期末和官方解答。

- [来源文件](../../sources/electrodynamics/README.md)
- [逐份URL、作者、学期、哈希、页数及许可](../../manifests/electrodynamics-sources.json)
- [源文件独立审查](qa/source-review.md)
- [理论独立审查](qa/theory-review.md)
- [本科考核独立审查](qa/assessment-review.md)
- [修订与进阶复核](qa/revision-review.md)

8.07第15讲含明确YouTube许可例外，第17讲含商业教材扫描页，整件暂不打包。保留获准第三方材料的个别署名，包括Hongsheng Chen、Min Chen和Chiyan Luo。商业教材本身没有归档。原件及中文改编按CC BY-NC-SA 4.0和MIT OCW条款使用；个別许可例外不纳入默认范围。

</details>

编译：安装XeLaTeX及常规中文TeX依赖（ctex、xeCJK、zhnumber、Fandol、Computer Modern Unicode），在本目录执行：

```bash
python vendor/math-latex-typesetting/scripts/validate.py main.tex --out build
```

`build/validation_report.json` 是自动检查结果；人工视觉和内容复核另见 `qa/`，不能把自动PASS解释成整本内容保证。
