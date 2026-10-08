# MIT 18.950 Fall 2008 作业来源审查

本轮只冻结题目来源与课程元信息，不编写解答，不重做四份讲义的全册数学审稿。四份讲义 PDF 的现存字节哈希与先前 `../audit.json` 一致，已复用其逐页来源审查。本轮十份 Homework 的十张题面均实际打开 130 dpi 单页原图核对；Homework 1 封面实际打开，另九张封面完整 RGB 像素与之完全相同。六张必要讲义原页亦已实际打开。生成图片已移入 `/tmp/dg-source-audit/assignment-rendered/`，仅供 QA，不在最终交付树内。

## 数量与计数口径

[官方 Assignments](https://ocw.mit.edu/courses/18-950-differential-geometry-fall-2008/pages/assignments/) 有十份作业。每份 PDF 都有一页 OCW 封面、一页题面，共 20 物理页。

| Homework | 顶层题数 | 显式字母/罗马子问 | 截止日 |
|---|---:|---:|---|
| 1 | 3 | 4 | 未提供 |
| 2 | 2 | 0 | 未提供 |
| 3 | 3 | 0 | 未提供 |
| 4 | 5 | 0 | 未提供 |
| 5 | 3 | 0 | 未提供 |
| 6 | 4 | 0 | 未提供 |
| 7 | 3 | 0 | 未提供 |
| 8 | 2 | 2 | 未提供 |
| 9 | 4 | 2 | 未提供 |
| 10 | 3 | 2 | 未提供 |
| 合计 | **32** | **10** | — |

32 是原件顶层编号数。10 个显式子问位于 PS1.1、PS8.2、PS9.2、PS10.3 内部，不能把 32+10 冒称 42 道作业题。未编号的多项要求逐题另列于 `frozen-inventory.json`，不冒充源件正式子问编号。PS2.2 的三个多项式只是 “for instance” 示例，不另算三题。PS4.1、PS4.2 原件没有分值，库存保留 null，不猜分配。

## 给题完整性和未解决来源缺口

“完整给题”表示原件给出了题面，不能据此判定题面陈述都没有错误。32 题的状态为：27 题完整给题；两题可由已定位官方讲义补全上下文；一题部分题面包含缺失引用；一题课堂方法细节缺失；一题只有缺失引理索引。没有仅列 Kuhnel 等书上习题号而不给作业指令的条目。

- **PS3.3 部分来源缺口：**折线曲率、闭折线定义及 Hopf 转角定理要求确实给出；最后一项所引 `Proposition 6.3 from the class` 未定位。实际 `ch1_revised.pdf` 物理第 8 页第 6 讲是 Theorem 6.1、Proposition 6.2、Example 6.3/6.4。Example 6.3 是平面 Frenet 标架说明，不可冒认为所指命题。不能确证这是旧课堂编号与 revised 的编号变化；没有旧版本证据。独立折线判据只能标为编者补充。
- **PS6.1 方法细节缺口：**题面要求完成 Wednesday lecture 的 hump reversal，另参照 Kuhnel 2002 p.157 Remark 4.25(ii)，并验证第一基本形式相同、通常第二基本形式不同。公开作业没有给构造细节，本轮未取得教材该 Remark 的正文或对应课堂逐日记录。可独立实现满足要求的构造并明说“编者构造”，不能声称还原课堂或教材原文。书籍引用不等于取得教材正文许可。
- **PS9.4 原题面缺失：**作业只写证明 `Lemma 28.3`，没有引理内容。实际 `ch3_revised.pdf` 物理第 7 页第 28 讲仅有 Example 28.1 和 Theorem 28.2，没有 Lemma 28.3。第 8 页第 29 讲的 29.3 是 Definition（局部参数化），不是引理；附近 Lemma 29.2 也没有语境证据可与该题对应。因此不能猜换编号，不能声称已解决原题。
- **PS7.1 上下文已定位：**`ch2_revised.pdf` 物理第 13 页第 21 讲 Corollary 21.3 确实要求局部重参数化后 G(p)=I 且所有一阶导数为零，可据此明示补全原条件。
- **PS10.1 错号且实际主题已定位：**原作业写 lecture 32；当前第 32 讲讨论映射度。旋转曲面专门测地线方程实际在 `ch4_revised.pdf` 物理第 5 页第 37 讲 Example 37.2。通用测地线方程在物理第 3 页第 36 讲 Proposition 36.4。应注明实际 37.2 出处，不只换成 36。

## 原文条件、符号与核对结果

1. **PS3.3 仿射段笔误：**原页首段确实是 c₀t+v₀，后段是 cᵢ+tvᵢ，又把 vᵢ 作为非零方向。若统一首段写法，应明确标出源文修订。
2. **PS7.2 两项修订：**原页确写 “second fundamental form” 却用 gᵢⱼ 并推正规坐标。按本课程 g 的定义应是 first。且 Corollary 21.3 的正规化包含 G(0)=I；仅有 g(x)=g(−x) 不保证此值，须补该条件或明确还要作线性标准化。
3. **PS10.2 有符号角动量：**原页明确用 τ<1 与 τ>1，没有绝对值或 τ≥0 方向约定。应按 |τ| 分类，或先说明非负角动量约定；原有 τ<1 包含负的大角动量，不能直接保留为正确条件。
4. **PS10.1 依赖公式的变量说明：**Example 37.2 第二式分母印 l₁(x₁)；沿 c(t) 使用时应明确 x₁=c₁(t)。原母线条件是单位速。该原页已实际核对。
5. **PS1.1 膨胀参数：**r 没有在原题限定；正则曲率问题须排除 r=0。
6. **PS2.2 奇异半径：**原题明确不要求证明观察，要求计算机绘图。发生 p′(Reⁱᵗ)=0 的半径可能导致曲线非正则，不能直接按普通正则曲线计算曲率；跳跃应保留这种条件说明。
7. **易误提取公式已核对：**PS5.3 的 ε、PS6.2 的 e^ψ 和 Cauchy–Riemann 式、PS8.2 球面映射的分子及根号分母、PS10.3 Newton 方程和两个罗马子问均已对原图核对，并在库存给出准确公式。机器提取全文原样保留，不把乱码当原文数学错误。

## 课程信息、课历与考试材料

[官方 Syllabus](https://ocw.mit.edu/courses/18-950-differential-geometry-fall-2008/pages/syllabus/) 和课程元信息确认：MIT 18.950 Differential Geometry，Paul Seidel，Mathematics，Undergraduate，Fall 2008。描述要求良好多元微积分、线性代数基础及定义—定理—证明式阅读能力。正式先修行是 Analysis I (18.100) plus Linear Algebra (18.06 or 18.700) or Algebra I (18.701)。教材为 Wolfgang Kuhnel，AMS 2002，Student Mathematical Library vol.16，ISBN 9780821826560；课程大致跟随前半本。

评分列为期中考试 30%、作业 30%、期末考试 40%。该列不用于推断考试次数；PS9.1 还明说可以使用第二次期中考试答案。当前 [官方 download 资源页](https://ocw.mit.edu/courses/18-950-differential-geometry-fall-2008/download/) 仅列四份讲义及十份作业，共14个PDF，没有公开官方解答或考试PDF。该结论限于已核对的该课程公开资源，不断言线下或其他网站从未存在。

官方课程导航只有 Syllabus、Lecture Notes、Assignments，没有 Calendar。所查页面未给具体逐日日期课历、每周上课时刻或作业截止日；不能从 Wednesday 字样编造日历。[官方 Lecture Notes 目录](https://ocw.mit.edu/courses/18-950-differential-geometry-fall-2008/pages/lecture-notes/) 给出可使用的讲次分组：1–10 平面曲线，11–23 超曲面局部几何，24–35 超曲面整体几何，36–41 长度和距离几何。

## 许可、归属及冻结证据

十份 PDF 的 OCW 封面均保留课程、Fall 2008 与引用/条款链接，未在 PDF 内标许可版本。当前 [MIT OCW 官方条款](https://ocw.mit.edu/pages/privacy-and-terms-of-use/) 的默认许可为 [CC BY-NC-SA 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)。需保留 MIT、课程、讲师、年份、来源与许可，标明改动，不表示 MIT 或讲师认可。单独权利声明优先。

实际查看的十张题面及相同封面没有见到第三方受限标记、独立图像或照片；只能说“逐页未见标记”，不能保证不存在全部第三方权利。Kuhnel 的书籍与 Remark 仅作为引用，未下载或转载受限教材正文。

`frozen-inventory.json` 为主记录，逐份含真实资源页/PDF URL、SHA256、页数、提取全文、题号、显式子问、未编号要求、条件与原文问题；每份截止日明确记为未提供。`download-record.json` 保存网页/PDF下载与哈希记录，`context-source-pages.json` 绑定六张实际核对的讲义原页。资源页 HTML 和提取文字留作本地源记录。生成 PNG 均为 QA-only，已移出交付树；最终推荐选定文件为十份源 PDF 及来源报告，由主任务显式冻结上传选择。
