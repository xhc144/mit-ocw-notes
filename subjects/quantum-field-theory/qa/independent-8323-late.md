# 8.323 后六套独立审读

审读者：负责8.324写作的另一团队Agent（独立于8.323后六套作者）。时间：2026-10-12T01:36:17.222276+00:00。

已逐篇实际阅读 assessment-8323-ps07.tex 至 ps12.tex 全文，以及 sources/8323-2023 对应六份题单TXT和六份官方解TXT；不是仅依文件名或覆盖表判断。公式审校与最终PDF视觉审查分开，本记录未检查整书最终PDF。

## 结论

本次审读发现并要求修正一处Majorana模式归一化证明中的矩阵错误；作者已修正，审读者重读修订段落后核验下述同动量恒等式。未发现其他需要阻止本次公开来源范围交付的数学错误。该结论是实际内容复核，不是“100%无错”认证。商书题面缺失仍保留为来源限制。

## 发现与返修

ps10 原题2(d) 原句用 U(p)σ²U(−p)^T 的“反对称性”证明 {χ,χ}=0，这个矩阵一般并不反对称。正确收缩是 ∑u(p)v(p)^T=U(p)σ²U(p)^T=detU(p)σ²=mσ²，与 ∑v(p)u(p)^T=−mσ²；等时将第二项 p→−p 后两项抵消。已经向root与qft_ps_late发送具体意见，作者修改后本次实读复核通过，下面SHA256绑定修订后的正文。

## 重点复核

- ps07：共同平移坐标的Fourier积分确实给总动量δ；带电标量的箭头守恒和三道外腿配对一致；导数耦合从原负时向度规转换后顶点为 +iλ′p₁·p₂；Higgs玩具模型最低阶两三角与六开线次序齐全。四维gamma5只含0,1,2,3，未沿用官方解多写gamma4的错误。
- ps08：Γ=iγ、barψ_o=i barψ与Σ_o=−Σ的转换逐式一致。有限Lorentz共轭指数证明、旋量归一化、H中c c†负号和−2∫E零点能正确；静止自旋子空间中的Σij平方给3/4。前文明确m>0、波包/盒子正则化，没有将delta归一分布态平方当普通态。
- ps09：gamma5平方为+1，已纠正官方解末行−1。Majorana条件给 ψ_R=iσ²χ*；代回Dirac作用量出现两个相同动能项，χ′=sqrt2 exp(−iπ/4)χ同时修正重复计数与质量相位，A=−iA′/2、B=iB′/2可逐项复算。二分量EOM共轭使用同一σμ；质量破坏连续U(1)，m=0例外保留。
- ps10：p·σ=E−p⃗·σ⃗、p·barσ=E+p⃗·σ⃗，正定矩阵平方根WU=m1与σ²U*σ²=W保证两极化解；模式只含一套a/a†，等时CAR经上述返修闭合。Berezin积分的次序、detA导数的索引kl正确。Yukawa作者明确区分iM和M，并声明原g与统一实耦合y的相位转换，未静默混用原正负号。
- ps11：π⁰=−∂₀A₀给等时散度对易子−iδ³。b±零自对易、交叉对易正号，物理小空间取b+核；多项式分解覆盖线性组合，零态与小空间正交，最后取商空间，未把含零态项的任意叠加错误称为全零范数。单零光子χμ=−kμ exp(−ikx)/(sqrt2 ω)与λ=−i exp(−ikx)/(sqrt2 ω)的符号一致。
- ps11 Casimir：无板周期非零模E0系数2π/L、Dirichletπ/(2a)一致；质量零模单独处理。同一个能量截止给LΛ²/(2π)−π/(6L)与aΛ²/(2π)−π/(24a)，先减再依次去UV和L，U=−π/(24a)、F=−π/(24a²)。
- ps12：相同末态2!、标量玩具模型的g/g′及s^(−3)量纲正确。Rutherford原PDF sin²排印错误显式改为sin⁴，(a)–(c)书题指针未倒造；(d)外场点源模型明确标为独立补充条件。eμ spin迹紧凑式2e⁴[(s−A)²+(u−A)²+2At]/t²、质心相空间与不同末态无2!一致。
- ps12 finite-M：从四动量守恒复得(E+M)E′−pp′cosθ=ME+m²，稿中显式E′根确为M>m的物理分支；δ能量径向积分给p′²/|(E+M)p′−pE′cosθ|，与原导数乘E′E′₂后的化简相同。M→∞时相空间系数1/(64π²M²)，与振幅主项相乘恢复Mott公式。用四组参数(m,M,E,θ)=(1,3,2,0.3),(1,3,5,2.2),(0.511,105.6,20,1),(0.511,10^7,20,2)作辅助数值核查，能量残差最大约1.4e−14，Jacobian两式差最大约2.2e−16；这些数值只作代数复核，不代替一般证明。

## 真实缺口

ps12 原题3(a)–(c)仅指定Peskin–Schroeder 4.4，没有授权完整商书题面。稿中明确不称这些子问已完成，不通过官方解重造它们。(d)需(a)–(c)的模型背景，作者已把采用的静态点源Born模型标为独立补充条件。没有伪造试卷、课号或考试。

## 复核快照

| 文件 | SHA256 |
|---|---|
| chapters/assessment-8323-ps07.tex | 6695f5603c8d9722c456cd49bd34b95a020f4f3a06672b9e4b930355b15f8699 |
| sources/8323-2023/mit8_323_s23_pset07.pdf | f803db2c90b26b74d1ed5d10c8e0806ea67fe8920f1987633a063f0e566b1ec4 |
| sources/8323-2023/mit8_323_s23_pset_07sol.pdf | 26fc06e09cfebc6e3c5693ea193934cb31dd9521b7270f66a73a478a9e4a5b70 |
| chapters/assessment-8323-ps08.tex | 91de719803361ec47d4487541037ff73c9e9b9f2a9efcd6bd07549017738b9e0 |
| sources/8323-2023/mit8_323_s23_pset08.pdf | 07ccd2728d93c1a84aa73b9ec59d5c533c2b146e3e2b5d09e752af6f8f325412 |
| sources/8323-2023/mit8_323_s23_pset_08sol.pdf | d8a6193c39c079dba7cc55ed798c7a7a8a8024eb4ad136b36a496382821c74f0 |
| chapters/assessment-8323-ps09.tex | acfeb60665cd51859ab5f8f3992ab64f55e63748a59ac8320778104944f81e6e |
| sources/8323-2023/mit8_323_s23_pset09.pdf | af715e5f2c404dc82733ceaf14deed5ea847cfa632c67d04651728d15371dd99 |
| sources/8323-2023/mit8_323_s23_pset_09sol.pdf | 161eab866656927ddeaefd8a5ec6bd83fc50dc3ea00d34403ba647f07ccf75ca |
| chapters/assessment-8323-ps10.tex | 4223f98e4cff5bf9110871c5a350c4c263c28f29b793f8f6015afef34af9b1de |
| sources/8323-2023/mit8_323_s23_pset10.pdf | 697a92d5cd1949c71f91c9e1e95b2432ea1fb4fd69279d140ecfe7d22268da49 |
| sources/8323-2023/mit8_323_s23_pset_10sol.pdf | 05bcb3afac70ca7ac52d60202b30c9189c61f09c71f890cc753837bfad911f08 |
| chapters/assessment-8323-ps11.tex | 94c0f5e6cc3afe877aa4e3c8093451d3d6636588fa58e483dead8baa4acb7bc6 |
| sources/8323-2023/mit8_323_s23_pset11.pdf | bbe2ef2fc401736046d4e8ca95a5bfd31f5acde580ddb172af7d22afc32201ba |
| sources/8323-2023/mit8_323_s23_pset_11sol.pdf | 5c920e84d256e119196e4edb8d48593e90e28bfc7bc998adfb88623eeacdc775 |
| chapters/assessment-8323-ps12.tex | d3156294a22da52387b807d9c555de909ed3df5271595866fc4bf4190ae6ac1c |
| sources/8323-2023/mit8_323_s23_pset12.pdf | 16c9f2abc86f9b3c7b54f4ed1fffb448e160c6b82bcd1b0ced63bae56f1167e0 |
| sources/8323-2023/mit8_323_s23_pset_12sol.pdf | c23c2f40a349c3ce6f2d70f90d94333d14ed6af05a444053afb476e6c835bf9b |

正文或源文件若再改动，上述哈希快照需要更新后才能继续声称覆盖同一版本。此报告不改他人正文，不替代root的最终整书构建、渲染和页级视觉检查。
