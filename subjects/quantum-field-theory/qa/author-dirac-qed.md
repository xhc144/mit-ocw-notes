# ch07–ch12 作者交接记录

本记录报告实际完成的正文和作者自查，不构成独立审校通过。写作基线：读者懂普通量子力学、线性代数和基础微积分；旋量、Grassmann 变量和规范量子化由正文引入。采用现有 main.tex 原生版式及语义环境，未更改宏、样式、根 README 或 Git。

## 实际来源

2026-10-12 真实浏览以下 MIT OCW 页面正文：

- [8.323 Spring 2023 Calendar](https://ocw.mit.edu/courses/8-323-relativistic-quantum-field-theory-i-spring-2023/pages/calendar/)：核对 lectures 13–26 的排列与正式题目。
- [Lecture Videos](https://ocw.mit.edu/courses/8-323-relativistic-quantum-field-theory-i-spring-2023/video_galleries/lecture-videos/)：核对资源链接。
- [Lecture 13](https://ocw.mit.edu/courses/8-323-relativistic-quantum-field-theory-i-spring-2023/resources/ocw_8323_lecture13_2023mar20_mp4/)：页面概述包含线性化 Dirac 方程、gamma 代数、旋量及协变性。
- [Lecture 20](https://ocw.mit.edu/courses/8-323-relativistic-quantum-field-theory-i-spring-2023/resources/ocw_8323_lecture20_2023apr24_mp4/)：页面概述包含 Coulomb/Lorenz 规范、Coulomb 正则量子化、光子态。
- [Lecture 25](https://ocw.mit.edu/courses/8-323-relativistic-quantum-field-theory-i-spring-2023/resources/ocw_8323_lecture25_2023may10_mp4/)：页面概述包含 Compton 振幅、截面及物理意义。
- [Lecture 26](https://ocw.mit.edu/courses/8-323-relativistic-quantum-field-theory-i-spring-2023/resources/ocw_8323_lecture26_2023may12_mp4/)：页面说明该讲为环图物理入门，涉及质量、真空极化、电荷、异常磁矩及 Pauli 方程。并不宣称此讲原本完成了本书给出的全部 phi4 重整化计算。

真实读取本地官方下载文本 mit8_323_s23_pset07.txt、pset09.txt、pset11.txt、pset12.txt、rec10.txt。重点实际使用 pset07 的 gamma/流问题，pset09 的 u,v、手征与 Majorana 条件，pset12 的相空间和截面归一化。rec10 的电弱扩展未纳入正文；没有据其现代物理旁注扩展未核验的实证断言。

未逐帧观看视频，未读取不存在的 lecture PDF。官方材料使用 (-+++) 和无 i 的 Dirac 方程，本稿转换为冻结的 (+---) 与 (i slash∂−m)，不混用官方的旋量归一中的额外 i。

## 实际正文范围

| 文件 | 汉字数 | 源字符数 | 范围 |
| --- | ---: | ---: | --- |
| ch07.tex | 1599 | 7784 | 线性化、Clifford、Lorentz 旋量协变、伴随与流、u/v 解及完备关系、gamma 迹 |
| ch08.tex | 1748 | 6734 | CAR 模、正能量和荷、自由 Dirac 局部自旋统计论证、传播子、Weyl/螺旋度、Majorana |
| ch09.tex | 1797 | 6725 | C/P/T、反酉时间反演、CPT 范围、Berezin 积分、源 Gaussian、Wick/闭圈负号 |
| ch10.tex | 1680 | 6698 | Maxwell 约束、Coulomb 能量和横模、协变传播子/物理态、Abelian FP、QED 图规则 |
| ch11.tex | 1890 | 11320 | 通量、相空间、衰变、e+e−→μ+μ−详推、Compton双图/Ward/迹/KN/Thomson |
| ch12.tex | 2345 | 9152 | 量纲、phi4 tadpole/bubble、反项条件、维数正规化/首阶 beta、QED环结构和Pauli方程 |

合计 11059 汉字，48413 个源码字符（公式与 LaTeX 包含在字符数中，不把字符数称为中文词数）。没有为达字数添加重复段落。

## 明确未证明的外部输入或范围限制

1. ch08 等时 CAR 与约束约化一致，但未展开一般 Dirac 括号约束量子化的普遍算法。
2. 自旋统计只给自由 Dirac 场的正范数/正能量/类空反对易论证；不冒充一般相互作用自旋统计定理。
3. CPT 定理准确说明常见结构性假设，但完整解析性证明未提供。
4. ch10 Gupta–Bleuler 描述限于自由 Abelian 结构；非 Abelian BRST 和全阶 Ward 恒等式交给后续章节。
5. 连续费米行列式通过有限维离散化解释，未经正规化不声称为普通收敛行列式。
6. e+e−→μ+μ− 忽略 m_e、保留 m_mu；低能电子阈值不可套用。Compton 截面为树级自由电子过程。
7. ch12 Euclidean 球硬截断明确规定作用于平移后的变量，不声称其对任意动量路由严格不变。维数正规化的解析延拓、Wick旋转使用 Feynman 处方且先在阈值以下演算。
8. phi4 的一圈局部反项和 beta 主链已展开；全阶可重整化性和非微扰存在性未证明。
9. QED 一圈自能、真空极化、顶角只解释结构，不给异常磁矩数值或圈积分结果；非相对论 Pauli 方程本地推导。

## 作者自查与重点复核

- 六文件 begin/end 原生环境栈检查无不匹配；未发现 TODO/FIXME、擅自 section/chapter 或 newcommand 版式改造。
- 未运行整书 XeLaTeX，也未看整书 PDF；请整书 owner 编译两次并作版面检查。
- 用 NumPy 4×4 Dirac gamma 矩阵在 m=1, omega=.7, cos(theta)=.3 单点检查 Compton 干涉迹：计算 35.68322147651008，解析式 16m²(A−B+2m²)=35.68322147651007。此为代数报警检查，不是独立证明或泛用数值测试。
- 独立 reviewer 应重点核对 Lorentz 生成元参数符号、等时 v(E,−p) 完备关系、波函数与算符时间反演的区别、Grassmann 积分测度方向、带符号 e 与物理电荷、Compton 干涉迹及初态平均、泡图 Wick 旋转总体 i、反项负号、d=4−2epsilon 的耦合极点系数与 beta 因子二。

当前作者版本 SHA256：

```
ch07.tex 8830e8ee89a45a9c67c4b7aad6b2b9344d2778fe6acc9b4c2af5fed1fcafcb8f
ch08.tex c1e199964c0ff3ac2203b555154d08ceb2539522bf125e15f5a95019de717c0c
ch09.tex e16039fe28814aeaf33089b5f05b482a433001600e4a71883fc6128bba841bda
ch10.tex 4af91ee8473a89cea7afa1e625b533898e89a5b2b108ea52249fc744f7249d8f
ch11.tex 47e2addde963043135e0c1f0b78e72bae2fe4c5549040cc687cb9996e993b834
ch12.tex 8073306204ce82935f093b773c149c5dccccbb8390522ae07758c4c35bde229d
```

## 独立审校返修

2026-10-12 按独立代理 qft_review_dirac 的全文意见，由本作者修订 ch07 相位变换的 Noether 流符号，并补 N 为偶数以排除三分量；ch10 增补具体归一离散模的 Gupta–Bleuler 零范数商，明确上/下指标和纵向产生系数的负号；ch11 改相空间分母逗号，补 Compton 干涉迹按零/二/四质量因子分组的完整收缩链。以上指纹和字数已更新，等待该独立代理实际返修复读，不由本作者自行标通过。

追加返修：ch12 Pauli 约化明确典型协变动量、动力学剩余能量、频率及弱场条件；ch11 修正 root 首次编译实际定位的 U+000C 控制字符（Källén 公式的 frac）。作者再次扫描六正文文件的非空白ASCII控制字符，无剩余异常；此扫描不等于整书编译通过。

ch09 追加左Grassmann源导数的两点提取次序与 −1=1/i² 因子，接上原有四点Wick式；同步指纹后交独立代理复读。

最终相位一致性返修：ch08 Majorana 二次项随同一 χL→exp(−iα)χL 相位约定变成 exp(−2iα)，连续U(1)破坏的结论不变。ch11 新增中间变量 a=pprime 的 prime 已改为正确上标撇号。
