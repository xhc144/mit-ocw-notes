# 偏微分方程

Jared Speck 的 MIT 18.152（Fall 2011）简体中文重构本。单册[中文PDF](dist/main.pdf)共49个实际PDF页（前置6页，正文及参考文献43页），可编辑[源码ZIP](dist/source.zip)解压后独立编译。保留仓库既有固定王者模板，不嵌英文原件页。

13个理论章节覆盖热方程、Laplace/Poisson、Green函数、波方程、能量法、Fourier变换、自由Schrödinger、Lorentz/变分守恒律及输运/Burgers。核心论证、例题和习题均有中文证明或解答，解类别、初边值与适定性条件明确。另收录全部11份作业、Bonus、期中和期末中公开完整题面：52道大题、114个细分要求，3个重复小问保留原号并复用证明。期中答案依据官方公开解答重构，其余为AI独立编写并交叉审读；原题错误在题解中说明和修订。

公开18份讲义共136页，考核及期中解答15份共78页，逐文件页数、URL、作者、许可和SHA256见[source-manifest.json](source-manifest.json)、[assessment-manifest.json](assessment-manifest.json)及[独立来源审查](review/source-assessment-review.md)。33份英文原件只在[原件归档](../../sources/partial-differential-equations/)；不嵌入中文PDF，不进入中文源码ZIP。

原课程商业书Salsa中11条只给题号的引用及1条阅读任务已逐项登记，完整题面未公开，不猜造、不冒称完成。Maxwell系统、一般非线性全局理论、一般粗糙域正则性、任意势算子理论和数值方法不在本册覆盖范围。具体原讲次映射、编者补充、缺项和边界见PDF末章。书前另有官方课程课时、先修、教材、评分、24讲进度及实际期末笔记规则。

## 编译

需XeLaTeX、ctex/Fandol、Computer Modern Unicode的cmunrm/cmunbx/cmunti/cmunbi字体、TikZ、booktabs、longtable及常规数学宏包。字体不随ZIP打包，main.tex内置完整锁定文档类；不依赖其他学科文件。依赖已安装时：

```bash
bash build.sh
```

输出dist/main.pdf。系统缺模板字体或中文TeX资源时，可用哈希固定的本地依赖工具，不修改系统安装：

```bash
python3 tools/bootstrap_tex.py --texmf-dir /tmp/pde-texmf --cache-dir /tmp/pde-tex-downloads
TEXMFHOME=/tmp/pde-texmf bash build.sh
```

## 检查记录

[独立正文审读](review/math-main-review.md)、[前段作业与Bonus审读](review/math-assessment-review.md)、[Fourier及场论作业审读](review/math-assessment-fourier-review.md)和[考试审读](review/math-exams-review.md)分别绑定实际源码快照。qa中的自动检查明确不替代数学与视觉审查；逐页视觉、目录目标和源码ZIP干净重编另有记录。正式ZIP只含本学科源码、说明、元数据与审查记录，不含英文原PDF、字体、构建缓存或凭据。

原作者Jared Speck，MIT OpenCourseWare。中文翻译、重排、补充证明、AI题解、勘误说明与自绘图沿用CC BY-NC-SA4.0，见[署名与许可](LICENSE.md)。本项目不代表MIT审定。
