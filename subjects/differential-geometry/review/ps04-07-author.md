# 官方作业 PS4–PS7 作者交接记录

日期：2026-10-08。作者 Agent：math_middle。工作根：`/workspace/dg-revision-work`。

完成四章、15 道官方原题的完整中文题面与 AI 独立完整解答。仅写 `chapters/ps04.tex` 至 `ps07.tex` 和本报告；没有修改主文件、锁定类、基础章、根 README、权限，也未上传或安装。以下四章已正式冻结为本报告绑定版本；后续内容修改须重新绑定并复核。

解答不是 MIT 或 Paul Seidel 的官方答案。实际读到的四份公开作业原件均未附解答；正文每章明确标为 AI 独立推导。章节保持 Paul Seidel、MIT 18.950 Differential Geometry、Fall 2008 来源，并使用实际核实的官方资源链接。原题翻译、数学批注与解答分开呈现。

## 冻结文件

| 文件 | SHA-256 |
| --- | --- |
| `chapters/ps04.tex` | `336c6b90a1131295016a81297fdb4f2dbccdcabf91fe09a0de1355ecd2196eba` |
| `chapters/ps05.tex` | `a4d1af0e7b95b70995f4936fd27d413bea92c9f2288b14369e6792904f3313bf` |
| `chapters/ps06.tex` | `0345d9ca9b8a9e603410b0da23f2b9fb84d00716fd6289d4538816c66e12be19` |
| `chapters/ps07.tex` | `26237fddcb553b98a08327a3e964a07a6d37beb1c8a4258fda1a6b3a39f6f385` |

## 原件核对与绑定

来源表路径相对 `sources/differential-geometry/assignments`。四份 PDF 的 SHA 独立重算并与 `download-record.json` 一致。每份原件两个物理页都已实际打开其 130dpi 单页 PNG：第 1 页为 MIT OCW 课程及条款封页，第 2 页为完整原题。提取文本仅辅助检索，未代替原页查看。

| 原件 | 路径 | PDF SHA-256 | 实际查看 |
| --- | --- | --- | --- |
| Homework 4 | `originals/homework04.pdf` | `4bf6d4d5d9711e17e0fd7f68c01dfeea5a1893af7d681901f98fc340fd4bb4af` | 物理页 1、2 均实际单页打开 |
| Homework 5 | `originals/homework05.pdf` | `e34ba77256483d1e83d266879bfb9fac6e5216c24c856fdb5f8dfaaa04203ad2` | 物理页 1、2 均实际单页打开 |
| Homework 6 | `originals/homework06.pdf` | `52be42cc85d9763463a89f3010c5a2bb681dfc9da241d617abee6feb6805fe97` | 物理页 1、2 均实际单页打开 |
| Homework 7 | `originals/homework07.pdf` | `18a403fac2c274e6a065418e1bbf1421e4f4da76343c85f3cc83103603c4bd77` | 物理页 1、2 均实际单页打开 |

实际核对重点：PS4 的二阶外幂、转置、第三基本形式的矩阵与平方；PS5 的 epsilon、分母负号和所有分值；PS6 的指数为 ψ 而非 2ψ、两条 Cauchy–Riemann 方程；PS7 的“second fundamental form”与 g_ij 矛盾。原 QA PNG 目录随后由统一整理移出；该事实不改变先前已实际逐页查看的记录。本报告绑定仍在的原 PDF，不主张旧 PNG 仍在原路径。为保留可复查的作者临时图像，又把同一 PDF 渲染到 `/tmp/dg-ps04-07-source-views`，没有写回来源目录。

另实际打开并再次查看 Lecture 21 的原页，Corollary 21.3 位于 `sources/differential-geometry/originals/ch2_revised.pdf` 物理页 13，原句为指定点的度量单位矩阵以及所有一阶导数为零。再次查看的 PNG 在 `/tmp/dg-ps04-07-source-views/context-lecture21.png`，SHA-256 为 `2a8308ded59f7cc64493404b409dc4eb8297d701a49aebe9f4c13e19b27c9758`。

读取官方 `ch2_revised.txt` 的 Lecture 12、Definition 12.2–12.6，核对 Gauss 法向的正行列式约定与 Weingarten 关系；读取 Lecture 14、Definition 14.4，核对源平均曲率取 trace、源标量曲率取两两乘积之和。这两处仅记录实际文本阅读，没有声称其 PDF 页已作新的图像检查。

## 题面覆盖与作者数学自检

| 标签 | 原题分值 | 完整解答的主要链条 |
| --- | --- | --- |
| `ps:4-1` | 原件未标 | 二阶外积为零与线性相关的等价，秩 ≤1 的双向证明。 |
| `ps:4-2` | 原件未标 | 明确循环外幂基，体积配对，C^T A=det(A)I；核对转置及顺序。 |
| `ps:4-3` | 2 | 参数叉积给向内法向，两基本形式、形算子、主曲率 0 与 +1；另列外法向。 |
| `ps:4-4` | 4 | 原题 ν=−f，Weingarten 关系与 Df 单射，形算子为单位算子。 |
| `ps:4-5` | 6 | 第三基本形式为 Dν 的 Gram 形式，自伴性给 I(L²X,Y)；矩阵式 h g⁻¹ h。 |
| `ps:5-1` | 10 | 高度极小点与 Hessian 半正定；两种法向及半定形算子给 λ_iλ_j≥0。 |
| `ps:5-2` | 3 | 图像度量及其逆，Γ^k_ij=φ_k φ_ij/(1+|Dφ|²)，乘积求导得 ∂_mΓ^k_ij=φ_km φ_ij。 |
| `ps:5-3` | 7 | 局部小距离、Df_ε=Df(I−εS)、正则性与法向保持，S_ε=(I−εS)⁻¹S。 |
| `ps:6-1` | 6 | 两块支撑不交的 C∞ 隆起及边界平坦性，只翻左隆起；逐点 g 相同、h 左侧变号，中心显式验证。 |
| `ps:6-2` | 8 | 连接形式及 dω=−K dA 给 K=−e⁻ψ Δψ/2；CR 情形 q>0、Δlog q=0，平面 K=0。 |
| `ps:6-3` | 3 | r=cosh s、z′=sqrt(1−sinh²s)，给全部正则域；弧长、r>0、K=−r″/r=−1。 |
| `ps:6-4` | 3 | 参数反射与 Gauss 法向变号，负共轭形算子及三种曲率；另列保持法向的版本。 |
| `ps:7-1` | 10 | 矩阵平方根归一化，Christoffel 常数与二次换元消 dg；逆函数定理及正定向保证合法坐标。 |
| `ps:7-2` | 4 | 保留原文矛盾，II 偶性的正则平面反例；I 偶性得 dg=0，再常线性归一化。 |
| `ps:7-3` | 6 | 正常点 Γ=0、逆度量导数零，曲率分量推出二阶度量公式；图像 Hessian 核对符号。 |

题量 5+3+4+3=15。所有未编号附加要求亦保留：PS5.3 允许 epsilon 足够小；PS6.2 的 CR 核对；PS6.3 排除课堂伪球面；PS6.4 三种曲率；PS7.1 使用课堂开头须概述给阅卷者。PS4 前两题没有虚构分值。

## 特别约定与来源限制

PS6.1 只保留原题的教材第 157 页 Remark 4.25(ii) 引用。未读取或复制该受限教材段落，也未取得星期三课堂讨论的完整细节。正文中两个隆起的图像是自足独立实现，不冒称 Kuhnel 或课堂原例；证明不依赖未读材料。

PS7 正常坐标严格按 Corollary 21.3 的点态一阶条件使用，不假设指数坐标的径向测地线性质。PS7.2 原印刷句不能直接证明：正文保留“第二基本形式”与 g_ij，随后给反例及第一基本形式的可成立版本；I 的偶性若未另归一化，也不保证原坐标 g(0)=I。

PS6.4 源 κ_mean=trace(S)，二维时本册 H=κ_mean/2；源 κ_scalar=Σ_{i<j}λ_iλ_j。按新参数定向重新选 Gauss 法向，κ_mean 变号、κ_scalar 不变、κ_gauss 乘 (−1)^n；保持原几何法向时三者均不变。关系均在 x 与 Px 对应点比较。

## 引用与机械核验

作者实际阅读了四章全部稿件并复算关键推导。15 个 exercise、15 个 solution 正确闭合，标签精确为预期 15 个且不重复。ref/eqref 目标实际存在于基础册：`prop:shape`、`prop:graph-curvature`、`prop:metric-transform`、`prop:metric-K`、`prop:rotation`、`prop:connection-curvature`、`eq:christoffel`、`eq:gauss-eq`。引用在实际公式或证明步骤旁使用，不是仅列同主题映射。未增加排版宏或另定环境，继续用 originalchapter、exercise、solution、remark。

作者自检修正了 PS7.3 最后图像核对式中 φ_11 的反斜杠，独立审稿者随后实际复核此符号。上述 SHA 已包含修正。

隔离构建在 `/tmp/dg-ps04-07-author-check`：主文件 begin-document 前的锁定模板及内容宏逐字复制，临时加入基础 ch04–ch07 以解析所需引用，再加入四个作业稿。首次未带统一环境时因 ctex.sty 缺失停止，未生成 PDF；之后使用主 Agent 提供的现有 `TEXMFHOME=/workspace/.local/texmf` 与可写 XDG 缓存，连续三轮 XeLaTeX 成功，没有安装或改模板。

最终日志无未定义引用、缺字、Overfull、Underfull；唯一 LaTeX 告警是模板预期覆写 adapter.cls。隔离 PDF SHA-256 为 `def440800ba58581d334c2adec07a5c53d2869e007062a18b90ada9ab750439e`。这是隔离编译证据，不能代替统一主PDF的编译和最终视觉；本报告不将未查看的隔离PDF标为视觉通过。

## 后续验收边界

作者自检未发现剩余数学阻断。独立 Sol 交叉审稿由主 Agent 安排，本作者报告不替代其独立报告。四个冻结哈希已正式通知审稿者，待其将报告绑定这些哈希。统一主PDF编译、逐页视觉、目录链接、干净重编、打包和远端校验由后续统一验收覆盖，本次没有宣称未完成项目通过。
