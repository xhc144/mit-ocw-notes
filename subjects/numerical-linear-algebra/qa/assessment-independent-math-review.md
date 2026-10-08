# 数值线性代数考核增补：独立数学复审

复审目录：`subjects/numerical-linear-algebra/assessments/`。审查以新增中文 LaTeX、MIT 原 PDF 对应的提取文本及 PS1 官方 notebook 为依据。只读仓库，修订意见发给主任务；本报告写于 `/tmp`，不做 Git 提交。

## 已核定范围

- 4 份作业：4 + 4 + 3 + 4 = 15 道一级题。
- MIT 作业纸印出的叶槽：9 + 8 + 7 + 5 = 29，含教材引用 11 处及 MIT 自定义子问 18 处。未取得的教材完整题面及其隐藏子问不计作已取得内容。
- 8 份考试：2008、2009、2010、2011、2012、2013、2015、2019，一级题 6 + 3 + 3 + 4 + 3 + 3 + 3 + 4 = 29，叶问 12 + 4 + 7 + 9 + 7 + 7 + 9 + 5 = 60。
- 2019 Problem 0 诚信声明和 Q4 的两条叙述前提不计作数学子问。
- `question-inventory.json` 的 44 个题条目对应 PDF 的 SHA-256 逐项重算匹配。
- 2009 未提供官方答案；三题解答必须明确标为 AI 编写。
- PS1 Q2/Q3 的官方答案来自官方 notebook，不能把答案 PDF 说成独立含有完整解答。

## 第一轮作业复审

PS1–PS4 共 15 道已逐条与原题纸及官方答案核对。PS1 高精度 Newton 误差位数独立重算，依次 0.380211、1.511377、5.010844、15.509654、47.006085、141.495375；误差比 e_new/e^3 趋于 −1/3，与新增稿吻合。

PS2 的复数无穷范数取等向量、Frobenius 条件数、实 SVD、满秩稠密性及长方矩阵块谱推导正确。PS3 的 Schur 回代总成本 4m^3/3 采用标量乘加计数；复数拆分计数应另述。缓存三角解的大矩阵条件和输入输出项已保留。PS4 FOM、连续两轮幂法二维提取及 Arnoldi 不变子空间推导正确。逆迭代已使用正交投影估计替代无效的 Neumann 展开。

两处文字意见已发送：PS3 Q1(c) Givens 每次更新“附近三列中的元素”，并非仅三个元素；PS4 Q4 Hermitian 是 B=0 的充分条件，不是必要条件。

## 原题/官方答案的关键校正意见

1. 2008 Q1：一般 Sylvester 方程的唯一回代要求两谱不交；共谱时要检查相容性与自由度。
2. 2008 Q2：一般浮点矩阵向量乘不能对共同输入向量宣称后向稳定。残差应直接用成分舍入误差界，得到 O(u)(||A||||x_tilde||+||b||)。改成 κ(A)||b|| 尺度需小 uκ 等条件。
3. 2008 Q6：权矩阵作用于残差空间，应为 m×m；原题写 n×n 是维度错误。
4. 2010 Q1(c)：SVD 三元组 max 范数应为 max(1,||A||)，不能无条件等同 ||A||。
5. 2010 Q2：正规方程右端应含 b，三角回代应为 Rx=Q*b，官方存在 x/b 及 R*/R 的笔误。
6. 2010 Q3(b)：平方算子与 shift-invert 的迭代次数依赖谱间隔，不存在一般“恰翻倍”结论；逆算子 Lanczos 仍可能有正交损失及内解误差。
7. 2012 Q3：QR 收敛须泛性旗标条件；按列相位调整后的 Q、T 才有通常的极限表述。非 Hermitian 不等于非 normal。
8. 2013 Q1：happy breakdown 的精确求解结论需要 A 非奇异；奇异 A 下可失败。
9. 2013 Q2(a)：官方逆矩阵顺序错误。由 A*A=R*R，C=R^{-1}R^{-*}，故必须解 R* y_i=e_i，再取 y_i* y_j。
10. 2015 Q1(a)：√u 精度障碍对应非退化二阶极小值；首个非零 Taylor 项为 2p 阶时障碍为 u^{1/(2p)}。原假设不能保证 f''>0。
11. 2015 Q1(b)：可表示反例 A=(1,3)^T，x=1+2^{-52}，fl(3x)=3+2^{-50} ≠ 3x；共同输入由首分量固定，第二分量矛盾。

## 2009 三题独立数学研究

Q1：令 C=Q1*Q2，B=Q2−Q1C，H=I−C*C=B*B。原矩阵满列秩使 H 正定。分块/递归 Cholesky H=R*R 后取 Q_tilde2=BR^{-1}，则 Q=[Q1,Q_tilde2] 为所需正交因子，且与原列序 QR 相容。合并缓存量 Θ(mn+mn²/√Z)。列基例 b≈√Z 只需 b² 工作块入缓存，不要求整个 m×b 入缓存；流式 Gram、Cholesky、三角解的基例 Θ(mb)。整层递归给 Θ(mn+mn²/√Z)。该 Gram 构造是精确算术复杂度解答，不能另宣称数值稳定。随机 50×8 独立验算给正交误差约 7.1e−16、下三角残差约 1.8e−15、重构残差约 8.3e−15。

Q2：Krylov 子空间始终位于缺失简单特征向量的正交补，维数至多 m−1，因此精确算术下必有 β_n=0。中止空间不变，T_n 是 A 在该空间上的限制；若 T_n 含 λ_i，则提升后得到与缺失 q_i 正交的 λ_i 特征向量，违背 λ_i 单特征值。

Q3：设 y 为计算解，(A+E)y=b+f，取 E'=E−fy*/||y||²。当 b≠0 且相对误差常数 u<1 时 y≠0，由 ||b||≤||A+E||||y||+||f|| 得 ||f||/||y||=O(u)||A||，故 ||E'||=O(u)||A|| 且 (A+E')y=b。b=0 时 f=0，原 E 已足够，不必除以零。随机独立验算修正方程残差约 2.1e−15。

## 最终结论

已读完 12 份新增中文考核 LaTeX，共 44 道一级题；全部显式子问均已与原题冻结清单核对。上述数学修订已复查落实，未发现尚未解决的实质数学错误。2009 三题的 AI 归属明确保留。PS1 编程来源已区分官方 notebook、本次 Julia 运行和 Python 补充验证。有限样本不是普遍数学证明。

Julia 1.10.10 的最终脚本以仅标准库、独立 `/tmp` 副本及新 depot 重跑，39 项通过。Python 3.12.14 / NumPy 2.5.3 / SciPy 1.18.1 最终脚本以独立 `/tmp` 副本重跑，50 项通过。最终脚本副本与仓库字节一致；复核不在仓库写入数值结果。Julia QR 样本 450 轮后相对特征残差 1.9967833286720947e−13。修正的 O(u) 扰动逆迭代样本给未归一化相对误差 0.9999000099990001、归一化方向误差 1.0541979626447985e−16。2013 正确逆顺序相对误差 1.279866711016721e−15，官方错误顺序相对误差 0.584745024459031。

执行中发现并反馈 Julia 顶层 soft-scope 变量错误、Python QA 目录变量覆盖；修复后的最终脚本实际重跑通过。PS1 说明已同步成对求和图的 Julia 实跑来源。2011 大根溢出时保留小根的独立公式、2012 反向级数求和、2015 秩亏 SR 补基后的 t_j=Bs_j 均已在正文复查。

剩余限制为 11 处教材完整题面缺失，未将反推结论冒称教材原题；物理页 1–50 已另行完成实际视觉审查，见 `/tmp/nla-visual-review-001-050.md`；页 51–90、内链、干净源码 ZIP 重编及远端 Git/哈希交付验证由主任务完成。


## 卷首与版本来源补充核对

已读最终卷首课程上下文与其冻结来源记录，并分别核对 OCW 原大纲、课历、Week 9 与 MIT 教师仓库 `spring19` 的 README。授课/答疑钟点、原先修、考核比例、项目要求和四份实际作业来源均正确；仓库绝对日期与 OCW 按周/讲次课历的差异已分列，未拼接成年份混合课历。已核对 Julia 官方 v1.1.0 源文件 `opnormInf`，PS2 最大行绝对值和的解释与之相符。版本注记只确认该源码版本，不推定全班当年的具体安装版本。

来源：[MIT spring19 README](https://github.com/mitmath/18335/blob/spring19/README.md)，[Julia v1.1.0 generic.jl](https://github.com/JuliaLang/julia/blob/v1.1.0/stdlib/LinearAlgebra/src/generic.jl)。

## 11 处教材题面缺口

PS1 Q1：13.2；PS2 Q1(a/b)：15.1、16.1；PS2 Q2(b)：3.4；PS2 Q4(a/b/c)：4.5、5.2、5.4；PS3 Q1(a/c)：10.4、28.2；PS4 Q3：27.5；PS4 Q4：33.2。这些位置的原教材全文未取得，以上引用号和 MIT 官方答案支持的论证已核对；对混合题其 MIT 自定义部分仍完整核对。

## 逐题覆盖

| 冻结题目 ID | 新增源码 | 显式叶槽 | 复审范围 |
|---|---|---|---|
| pset01-q1 | pset1.tex | reference | MIT 自定义部分完整核对；教材部分仅核对引用与官方答案支持的结论 |
| pset01-q2 | pset1.tex | a, b | 完整 MIT 题面及译审解答 |
| pset01-q3 | pset1.tex | a, b, c | 完整 MIT 题面及译审解答 |
| pset01-q4 | pset1.tex | a, b, c | 完整 MIT 题面及译审解答 |
| pset02-q1 | pset2.tex | a, b | MIT 自定义部分完整核对；教材部分仅核对引用与官方答案支持的结论 |
| pset02-q2 | pset2.tex | a, b | MIT 自定义部分完整核对；教材部分仅核对引用与官方答案支持的结论 |
| pset02-q3 | pset2.tex | whole | 完整 MIT 题面及译审解答 |
| pset02-q4 | pset2.tex | a, b, c | MIT 自定义部分完整核对；教材部分仅核对引用与官方答案支持的结论 |
| pset03-q1 | pset3.tex | a, b, c | MIT 自定义部分完整核对；教材部分仅核对引用与官方答案支持的结论 |
| pset03-q2 | pset3.tex | a, b | 完整 MIT 题面及译审解答 |
| pset03-q3 | pset3.tex | a, b | 完整 MIT 题面及译审解答 |
| pset04-q1 | pset4.tex | whole | 完整 MIT 题面及译审解答 |
| pset04-q2 | pset4.tex | a, b | 完整 MIT 题面及译审解答 |
| pset04-q3 | pset4.tex | reference | MIT 自定义部分完整核对；教材部分仅核对引用与官方答案支持的结论 |
| pset04-q4 | pset4.tex | reference | MIT 自定义部分完整核对；教材部分仅核对引用与官方答案支持的结论 |
| exam19-q1 | exam2019.tex | whole | 完整 MIT 题面及译审解答 |
| exam19-q2 | exam2019.tex | a, b | 完整 MIT 题面及译审解答 |
| exam19-q3 | exam2019.tex | whole | 完整 MIT 题面及译审解答 |
| exam19-q4 | exam2019.tex | whole | 完整 MIT 题面及译审解答 |
| exam08-q1 | exam2008.tex | a, b, c, d | 完整 MIT 题面及译审解答 |
| exam08-q2 | exam2008.tex | whole | 完整 MIT 题面及译审解答 |
| exam08-q3 | exam2008.tex | a, b, c, d | 完整 MIT 题面及译审解答 |
| exam08-q4 | exam2008.tex | whole | 完整 MIT 题面及译审解答 |
| exam08-q5 | exam2008.tex | whole | 完整 MIT 题面及译审解答 |
| exam08-q6 | exam2008.tex | whole | 完整 MIT 题面及译审解答 |
| exam09-q1 | exam2009.tex | 1, 2 | 完整 MIT 题面与 AI 补写证明 |
| exam09-q2 | exam2009.tex | whole | 完整 MIT 题面与 AI 补写证明 |
| exam09-q3 | exam2009.tex | whole | 完整 MIT 题面与 AI 补写证明 |
| exam10-q1 | exam2010.tex | a, b, c | 完整 MIT 题面及译审解答 |
| exam10-q2 | exam2010.tex | a, b | 完整 MIT 题面及译审解答 |
| exam10-q3 | exam2010.tex | a, b | 完整 MIT 题面及译审解答 |
| exam11-q1 | exam2011.tex | a, b | 完整 MIT 题面及译审解答 |
| exam11-q2 | exam2011.tex | whole | 完整 MIT 题面及译审解答 |
| exam11-q3 | exam2011.tex | a(i), a(ii), b | 完整 MIT 题面及译审解答 |
| exam11-q4 | exam2011.tex | a, b, c | 完整 MIT 题面及译审解答 |
| exam12-q1 | exam2012.tex | a, b, c | 完整 MIT 题面及译审解答 |
| exam12-q2 | exam2012.tex | a, b, c | 完整 MIT 题面及译审解答 |
| exam12-q3 | exam2012.tex | whole | 完整 MIT 题面及译审解答 |
| exam13-q1 | exam2013.tex | a, b | 完整 MIT 题面及译审解答 |
| exam13-q2 | exam2013.tex | a, b | 完整 MIT 题面及译审解答 |
| exam13-q3 | exam2013.tex | a, b, c | 完整 MIT 题面及译审解答 |
| exam15-q1 | exam2015.tex | a, b(i), b(ii) | 完整 MIT 题面及译审解答 |
| exam15-q2 | exam2015.tex | a, b, c | 完整 MIT 题面及译审解答 |
| exam15-q3 | exam2015.tex | a, b, c | 完整 MIT 题面及译审解答 |

## 最终复审源码 SHA-256

以下 18 份快照对应实际复审及独立实跑的源码；后续若改源码应重算并复核相关内容。卷首最终仅增加段落分隔，已复核且同步哈希。

| 文件 | SHA-256 |
|---|---|
| `subjects/numerical-linear-algebra/assessments/exam2008.tex` | `2fe7675b1758cdc586c40a648980d40a075c639b5841ddc99dfb464d9a6b455c` |
| `subjects/numerical-linear-algebra/assessments/exam2009.tex` | `dff53aeebb5752e117517064ec3cf9efeb9ad2e325015d38ff9563cf8600a3fb` |
| `subjects/numerical-linear-algebra/assessments/exam2010.tex` | `cd8ddea72a78a16028bda9786497fababd861a0797011f4fc7a138369ed580e2` |
| `subjects/numerical-linear-algebra/assessments/exam2011.tex` | `bf68a8a21033f8b62f1384bba0f38a579fb7559ba0b271d762d04d49034268f1` |
| `subjects/numerical-linear-algebra/assessments/exam2012.tex` | `081c1b7b652ddada3959b3090646121fb915b5cd20ec342bffcc76b2265c70f1` |
| `subjects/numerical-linear-algebra/assessments/exam2013.tex` | `14f426a85b3409d89e71f879248b52f0578d11de9f10cbf99d37da0162b67abd` |
| `subjects/numerical-linear-algebra/assessments/exam2015.tex` | `6b2529d18799a992c8ac56a977b499fa1fe38c132208a3df5dfe048b3875843d` |
| `subjects/numerical-linear-algebra/assessments/exam2019.tex` | `6df6f77081e9cc3e0b87f1ab77400387771b16d3032bf12b1b7add291c5fa6c3` |
| `subjects/numerical-linear-algebra/assessments/pset1.tex` | `9dad54e04971e4e9dd7efe4ef3468c38cef8ba0050cdecd137666485f7a814a3` |
| `subjects/numerical-linear-algebra/assessments/pset2.tex` | `cd791564301bbb76edef54f1e0df37018b4b89e088b276caad2c5c118f360c54` |
| `subjects/numerical-linear-algebra/assessments/pset3.tex` | `e00498fd6f51050720de0589ad391ce94a206b6ec8fe9d0cd2a5f156cd512d2e` |
| `subjects/numerical-linear-algebra/assessments/pset4.tex` | `a9b50eea164f802ae66ae8ccc4b4c68b7a510e036b1970f35c262fff2c17b2a1` |
| `subjects/numerical-linear-algebra/chapters/course-context.tex` | `49c4df3bc60ed37a0e5807592be525230d8b9a4468bd15586c03b304fa9ad8f2` |
| `subjects/numerical-linear-algebra/experiments/assessment_checks.jl` | `c8978da9bfcd640674215dec3c7453eaef3d0d8bdf6f1dc668d9421ca6af70f7` |
| `subjects/numerical-linear-algebra/experiments/assessment_checks.py` | `907b0c8675107389c1190608b627475935dc81db1ad111ca7cc6bee9d759a985` |
| `sources/18.335j-spring-2019/assessments/question-inventory.json` | `c04ad586886b902227d6eedcaa55457ac59dea03f8d201b564c98c28461bfdce` |
| `sources/18.335j-spring-2019/assessments/course-repository-context.json` | `e487d84e75fc349cbabff42c609905f78f2ab8e132e0af534668c502a2132762` |
| `sources/18.335j-spring-2019/assessments/julia-api-context.json` | `535033df45fac92794aa0686f3b578627a33d6b81fd6b638a245c78d0ad124fe` |
