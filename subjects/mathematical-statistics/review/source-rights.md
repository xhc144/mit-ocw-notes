# 18.650 Fall 2016 原件权利与页序审核

审核日期：2026-10-08。范围严格为[官方 Lecture Slides 页面](https://ocw.mit.edu/courses/18-650-statistics-for-applications-fall-2016/pages/lecture-slides/)目前列出的十份 PDF，覆盖课程 sessions 1–24，共 **292 个物理 PDF 页**。不纳入 automatic resource / lecture-notes 索引中的 Old6、Old17-18。原文件身份、官方 URL、SHA-256 和物理页数由 `sources/18.650-fall-2016/source-manifest.json`记录；逐页内容范围和逻辑页对应见同目录 `source-frame-map.json`。

本次读取十份 PDF 的文本，逐页检查渲染总览；对所有真正的图页与 overlay 聚焦组放大检查。搜索 permission、copyright、reserved、courtesy、© 等文字仅辅助定位，没有把“未搜到”当作全部审核。含图页既包括嵌入 raster 图，也包括直接绘制的 vector 图。字体轮廓、矩阵括号、公式和表格不机械计为非文本图。

## 结论与默认许可

**整份原 PDF 应 hold、仅保留官方链接的文件是 Principal Component Analysis（17 个物理页）**。独立例外在原 PDF **物理第 14 页，印刷页脚 14/16**。用户规则将带单独权利例外的整份原件暂缓上传；本审核不移动、删除或提交原文件，交由主代理处理。其余九份在已检查原件中没有发现单独权利保留或转载许可标记，可按默认许可与用户授权范围处理。

MIT OCW 当前[官方使用条款](https://ocw.mit.edu/terms/)给出 **CC BY-NC-SA 4.0**：复制与改编须署名、注明改动、非商业使用、相同许可共享。条款也说明许可未必覆盖所有用途所需权限。默认 CC 不等于把独立第三方转载许可也授予后来使用者；私有仓库同样不自动取得该许可。这里只对已审原件中的明确例外作处置，不把“Nature 论文被提到”或书名参考文献本身误判为整份 hold 原因。

## 逐源结果

所有页码均为 PDF 阅读器的 **1-based 物理页序**，不是 Beamer 页脚编号。

| Sessions | 官方课件 | 物理页数 | 已核非文本图页 | 原件末尾引用/条款页 | 处置与例外 |
|---|---|---:|---|---:|---|
| 1–2 | Introduction to Statistics | 46 | 无真正图页 | 46 | 默认 CC；无独立权利例外 |
| 3 | Parametric Inference | 12 | 无真正图页 | 12 | 默认 CC；无独立权利例外 |
| 4–5 | Maximum Likelihood Estimation | 25 | 无真正图页 | 25 | 默认 CC；无独立权利例外 |
| 6 | The Method of Moments | 15 | 无真正图页 | 15 | 默认 CC；无独立权利例外 |
| 7–10 | Parametric Hypothesis Testing | 38 | 无真正图页 | 38 | 默认 CC；无独立权利例外 |
| 11–12 | Testing Goodness of Fit | 24 | 无真正图页 | 24 | 默认 CC；无独立权利例外 |
| 13–16 | Regression | 44 | 2、8–11、13、32、37、38、40–42 | 44 | 默认 CC；这些图中未见单独声明 |
| 17–18 | Bayesian Statistics | 18 | 无真正图页 | 18 | 默认 CC；无独立权利例外 |
| 19–20 | Principal Component Analysis | 17 | **14** | 17 | **hold 整份；只留链接与来源元数据** |
| 21–24 | Generalized Linear Models | 53 | 7、25、26 | 53 | 默认 CC；这些图中未见单独声明 |

PCA 原件：[官方 PDF](https://ocw.mit.edu/courses/18-650-statistics-for-applications-fall-2016/d85e1a9d113142ade8ce5e4f5ef0b4e8_MIT18_650F16_PCA.pdf)。第 14 页题头是欧洲人群基因表达的示例，主体为带国家缩写的 PCA 散点图，右上角有欧洲地图插图。图旁短权利原文为：

> Reprinted by permission from Macmillan Publishers Ltd: Nature.
>
> © 2008.

同一图旁注明 John Novembre 等人的“Genes mirror geography within Europe”，Nature 456 (2008), 98–101。**该声明证明课件里有出版社许可转载的图，并不证明用户可以再次上传这一图或整份原件。** 没有把上述声明扩写成 PDF 未出现的“All rights reserved”。整份 hold 的具体原因是用户对独立 rights 例外的规则，而不是声称全课件都不适用 CC。整理后的中文知识讲义可以独立讲解协方差、谱分解、PCA 算法与低秩估计；不要复制这一图或由其做实质性改绘，示例只保留来源链接即可。

## Beamer 页序与内容范围

292 个物理页对应 **285 个逻辑页**：**275 个内容/章标题页，另有 10 个 MIT OCW 引用/条款页**。这里只合并经人工检查的同页脚 overlay；“同标题”不是去重规则，“文字完全相同”也不是可见画面相同的证据。

| 课件 | 物理页组 | 页脚 | 主要保留页 | 必须共同读取的内容与依据 |
|---|---|---|---:|---|
| Introduction | 8、9、10 | 9/43 | 10 | 9 新增 RANDOMNESS，10 新增 average/chance/significance 问题；10 累积完整 |
| Introduction | 11、12、13、14 | 10/43 | 14 | **必须同时读取 11、12、13**：概率定义、单骰例题、双骰例题、总结轮换聚焦；其余文字淡灰却仍被抽取。14 不是全可见正文的单一完整版本 |
| Introduction | 17、18 | 14/43 | 18 | **必须同时读取 17**：about 与 not-about 两组条目轮换聚焦；文字抽取相同，视觉展示不同 |
| Maximum Likelihood | 6、7 | 6/23 | 7 | 7 新增“无法构造总变差估计量”的问题；最终页覆盖此前内容 |

其余物理页均作为独立逻辑页保留，含页脚跳号或相同标题的页。导论实际缺少页脚 7/43、12/43、16/43、32/43；Goodness of Fit 缺少 17/25、18/25。**这是当前官方 PDF 的页序现象，不凭页脚补造遗失页，也不混入旧课件。**

回归物理 **7–11** 的标题均为“Linear regression of a r.v. Y on a r.v. X (3)”，页脚却分别为 7/43–11/43，应全部记录为独立编号页。7 没有点云图；8 新增点云；9 新增蓝色真实回归线；10 改成红色估计回归线；11 同时展示两线，并把样本 pair 记号修正为 `(X1,Y1), …, (Xn,Yn)`。物理 13 展示竖直残差，32 是 Lasso 系数路径，37–38 展示局部窗口，40–42 比较三种 bandwidth；这都是文字抽取难以呈现的新内容。Method of Moments 6、7 虽同“Gaussian quadrature (2)”标题，但分别推导线性方程组与 Vandermonde 可逆性，不能合并。GLM 7 的饱和曲线、25 的两条 CDF、26 的两条逆链接曲线均为不同图。

额外数学原文核准：Introduction 物理 **12** 页单骰例题为 Alice 得 $1 的条件 **dots ≤ 3**，Bob 得 $2 的条件 **dots ≤ 2**。相应期望为 1/2 与 2/3，应选 Bob；PDF 文字抽取漏掉不等号，必须据渲染图核准。

`source-frame-map.json`对每个 frame 记录全部物理页、原页脚、核准标题、主要保留最大页、必要辅助页和逐页新增可见内容；普通源的抽取文字增量明确标成辅助证据。PCA 仅保存简要知识范围、短声明和来源元数据，没有在审核 JSON 中另行复制其全文或图。数学命题范围仍应以各源独立页内容共同覆盖，不能通过一张“最后页”覆盖上述轮换聚焦组。
