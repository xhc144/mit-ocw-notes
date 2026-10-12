# 电动力学中文讲义

理论与考核题解合订为一本连续中文 PDF。当前为78页研究生公开理论续编版，整体物理续编仍在进行；本册的实际覆盖和缺失范围逐项公开。

- [下载中文 PDF](electrodynamics-zh.pdf)
- [下载可编辑 LaTeX 源码 ZIP](electrodynamics-zh-source.zip)
- [查看理论逐文件对应及全部考核编号](coverage.md)
- [查看审校与交付证据](qa/README.md) · [研究生续编验收](qa/graduate-release.json)

本科主线采用 MIT OCW **8.07 Electromagnetism II，Fall 2012**（Alan Guth、Min Chen），包括矢量分析、静电边值、介质、多极展开、稳恒磁场、麦克斯韦方程、能量动量、电磁波与辐射。中文稿共30章、110个考核题解单元；本科十套作业中26道一级题具有完整取得题面并给出解答，另1道只取得(c)，两次Quiz共9题，本科期末5题。Quiz为官方解答的中文整理及补充推导；本科作业和期末为AI独立解答。

向后进阶采用 **8.311 Electromagnetic Theory，Spring 2004**（Leonid Levitov）的四份真实补充笔记，纳入研究生期末3题与**十二套作业全部66道一级题**。研究生作业题解为AI独立推导，并参照可匹配官方解核对；官方缺解、符号约定、模型限制和确定勘误在题旁说明。12个命名的官方作业解答文件仅匹配11套：solution7.pdf实际是作业8，作业7匹配官方解未取得。书中说明迟滞势全场求导、场模态拉格朗日量、频谱约定及Frank–Tamm谱的计算步骤。第11.6节依据Field Oscillators原件第1–2页，补齐SI制带源作用量、库仑规范消标势产生的即时库仑项，以及一般受迫模态的因果卷积解；归一、初值与点源耦合均经独立复核。

原件全部取得不代表全课程理论全部完成。8.311仅公开四份补充笔记；第30章现将全部15页的公式与论述逐页映射、中文重编，并补齐波导阻抗/能量速度、场动量、共振模态功、一般辐射谱及有限时碰撞谱。其课历中的Noether定理、完整协变作用量、辐射反作用及同步辐射全套理论尚未建立。本册明确标出Kramers–Kronig基本复分析关系与Liénard总辐射功率作为引用工具的证明边界，不冒称完整研究生电动力学教材。8.312未定位可核验官方原件。

本科65个作业编号组中，38组缺完整商业教材题面或依赖条件；PS5 Q5只写已取得的(c)。教材题号不视为取得题面或再发布许可，没有补造商业教材原题。研究生PS11 Q3已自绘天线角功率，但未取得原题要求比较的教材Fig.34.4，不能声称完成实图比对。

中文内容使用用户固定LaTeX模板，新增图采用TikZ/PGFPlots可编辑矢量图。原件复核、数学/物理独立复核、自动编译、PDF目录链接检查与实际逐页看图分别记录。中文重编并非MIT官方中文讲义，也不表示MIT认可。

<details>
<summary>原始资料与许可证</summary>

实际下载解析校验63份候选PDF，其中61份、共474页已归档；包括8.07的可打包讲义、十套作业、两次Quiz及解答、本科期末及公式表，以及8.311四份笔记、十二套作业、十二个命名解答文件、期末及官方解答。

- [来源说明](../../sources/electrodynamics/README.md)
- [逐份URL、标题、作者、学期、许可、哈希及页数](../../manifests/electrodynamics-sources.json)
- [源文件独立审查](qa/source-review.md)
- [十二套作业真实题面核对](qa/advanced-source-coverage.md)
- [扩充稿修订复核](qa/revision-second-review.md)
- [带源作用量与因果模态解的专项复核](qa/field-oscillator-closure-review.md)

8.07第15讲含明确YouTube许可例外，第17讲含商业教材扫描页，整件暂不打包。保留获准第三方材料的特别署名，包括Hongsheng Chen、Min Chen和Chiyan Luo。商业教材本身没有归档。原件及中文改编按CC BY-NC-SA 4.0与MIT OCW条款使用，个别例外不纳入默认范围。

</details>

安装XeLaTeX及中文TeX依赖（ctex、xeCJK、zhnumber、Fandol、Computer Modern Unicode），在本目录执行：

~~~bash
python vendor/math-latex-typesetting/scripts/validate.py main.tex --out build
~~~

经验证的具体构建环境见 [build-environment.md](qa/build-environment.md)。源码包不分发字体。自动PASS只说明编译及结构等相应检查通过，数学内容与实际视觉复核另见qa记录。
