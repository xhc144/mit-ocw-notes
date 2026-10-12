# 核查范围

`coverage-freeze.sha256` 固定先行建立的逐件来源清单；`assessment-inventory.json` 给四类作业/复习包的原题计数、卷内与先修卷重复引用、原件缺口。`prior-volume-reference.json` 固定热统卷的已发布提交、题目位置、PDF/TeX哈希，保证“已覆盖”不是空泛引用。

`numerical-checks.json` 记录物理量级、Gaussian热流积分、谐链协方差、Mehler核、实空间RG、Potts星三角关系、cubic固定点、有限一维Metropolis样本、Bose热容与矢量图的数值检查。计算是对这些特定公式及有限样本的复核，无法代替无穷体系证明。

`render-and-links.json` 记录PDF物理页、每页渲染图哈希、逐页目视、书签与内部链接目标、锁定模板一致性。`standalone-build.json` 保存XeLaTeX输入哈希和收敛轮数；`archive-validation.json` 保存解压源码包后的洁净重编译结果；`remote-validation.json` 保存公开仓库下载文件的哈希、页数及远端ZIP重编译结果。

复习题中官方给出的答案与本卷中文独立推导不作同一作者声称。有明确错误、隐含条件或解答形式差异者在题内指明。作业6表格缺项、公开历史年界与未发布的当期正式考试保留缺口，不凭课程大纲编造题面。来源原PDF、OCR及第三方例外图片仅供本地核对，公开成果仅保存元数据、链接和本项目编写的TeX/PDF。
