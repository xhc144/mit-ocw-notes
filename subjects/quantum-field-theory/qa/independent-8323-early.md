# 8.323 作业1–6 独立内容复核

复核者：后六套作业编写Agent（与前六套编写者不同）；这是独立任务分支的逐题复算，不是外部专家认证。复核日期：2026-10-12。

## 实际读取与结论

完整读取 assessment-8323-ps01.tex 至 ps06.tex 全文，并读取 sources/8323-2023 下12份匹配的题单/官方解TXT（由存档PDF提取）。额外直接渲染并视觉读取官方ps06解PDF第3、4、6页，以核对图拓扑和对称因子；没有以文件名或摘要代替正文。未修改前六套正文。

结论：22道主问题的全部可获子问均有独立题面和解答；没有纯商业教材题号缺口。未发现需要作者返修的实质数学错误。以下结论绑定本报告末尾列出的源码SHA-256；不涵盖之后变动。

## 逐套复核

| 套题 | 原题及子问 | 核查结果 |
|---|---|---|
| 1 | 1(a–g), 2(a–c), 3(a–d), 4(a–d) | 谐振子H=ω(N+1/2)；正能量壳测度和delta的Jacobian；复标量动量/Noether流/能动量的(+---)空间负号一致。原解把荷流的i随意删去的问题已正文纠正。 |
| 2 | 1(a–d), 2(a–c), 3(a–c), 4(a–d，d为奖励) | KG负频率密度确实负；双同向Fourier核给δ(k+q)；H与P的模式系数及体积因子正确；旋转和boost生成元含正确半散度项。 |
| 3 | 1(a–c), 2(a–e), 3(a–d), 4(a–c) | 与ps02生成元统一，U=exp(−iωM/2)确给δk_i=ω_0i E−ω_ij k_j；位置态的额外boost平方根正确；C=−i m²t K2(ms)/(2π²s²)符号与定义一致；高斯乘子、抹平方差大小尺度系数和U(1)选择规则均复算。 |
| 4 | 1(a–d), 2(a–j) | 全部10个外源子问保留；retarded GF的−i delta、a_out移位、[F,G]=λ、exp(−λ/2)、n!的Wick投影抵消和全相空间再除n!完整一致；正文也区分了真实Dyson整体相位。 |
| 5 | 1(a–b), 2, 3, 4(a–c) | 动量积分测度dp/(2π)、短时高斯二矩iε/m与驻相尺度、自由核归纳配方、Dirichlet本征谱、离散三对角det=N及归一因子均复核。 |
| 6 | 1, 2(a–b), 3(a–c), 4 | 高斯源真空概率从±质量壳得到exp(−λ)；二点/四点/真空全部拓扑及S因子见下；真空分量指数与关联函数中真空泡消去证明没有误称完全连通。 |

## 高风险推导的独立检查

### Lorentz生成元

从ps02定义M^{0i}=−∫x^i H和M^{ij}=∫(x^iT^{0j}−x^jT^{0i})复算，得 M^{0i}=−i∫a†(E∂_i+p_i/(2E))a，M^{ij}=−i∫a†(p_i∂_j−p_j∂_i)a。其厄米性需要boost半散度项；正文具备该项。与ps03 G=ωM/2及U=exp(−iG)联用，[G,a]=i(δk·∇+δE/(2E))a，确给UaU†=sqrt(E_Λk/E_k)a_Λk。原官方旋转中间式存在1/2不一致；正文以定义重新推导的结果正确。

### 外源Poisson因子

源必须为实，J(−k)=J(k)*。F=i∫J(k)a†/sqrt(2E)，G=i∫J(−k)a/sqrt(2E)，因此[F,G]=+λ，而非−λ。正规序位移为exp(F)exp(G)exp(−λ/2)，真空概率exp(−λ)，n粒子振幅i^n∏J(k_i)exp(−λ/2)。指数展开的1/n!由投影时n!配对抵消，随后物理全相空间仍需独立除n!，故Pn=exp(−λ)λ^n/n!。ps04正文两种阶乘均正确。ps06高斯源方法的−π∫|J|²δ(p²−m²)由正、负壳两贡献得到相同λ，没有多2或少2。

### 图拓扑与对称因子

ps06二点二阶图以顶点度数枚举：外线1+1时，内部边数r=1或3，得到串联tadpole与sunset；外线2+0时，连通唯一r=2并在无外线顶点有自环。对应Wick数288,288,192，除2!(4!)²=1152后为1/4,1/4,1/6。原官方表第二种坐标式把两条外线接不同顶点造成度数错误，正文已改为同一顶点，和原图一致。

四点一阶S=1；二阶1+3外线分配给4张外腿tadpole，每张S=2；2+2给3个泡道，每张S=2。原题只要求“列出全部图”，正文以代表TikZ加明确标签置换给出全部8种连通贡献，未漏外腿图。

连通真空图一阶双自环：3/4!=1/8；二阶双顶点各自环且连接双线：72/1152=1/16；四连线：24/1152=1/48。ε=iW0/(VT)使正文λ/8 D(0)²−iλ²/16 D(0)²∫D²−iλ²/48∫D⁴符号正确。

### 条件与源资料纠错

ps01壳测度明确限制orthochronous，避免原解错误的“能量数值不变”；ps03定位相位自由度和质量m=0大尺度例外明确；ps04相位对称性包含真空不变假设；ps05有限维归一和形式无穷行列式分开；ps06声明C在固定盒子只保证独立T，可依赖V，并说明真空边界归一如何取C=0。后者是对原题物理假设的必要澄清，不能只照抄“与时空体积无关”。

## 可重复数值/组合证据

离散三对角行列式递推d_n=2d_{n−1}−d_{n−2}在n=1,2,3,9,20检查均给n+1；二点Wick比值为0.25,0.25,1/6；真空图比值为0.125,0.0625,1/48。脚本只是复算辅助，不替代上述证明。

## 绑定文件与来源

### 作业1
- 正文：`chapters/assessment-8323-ps01.tex`
- 正文SHA-256：`daca7b29a293f00b556d38137dce3b1aad93b6f295c27ef10261bb2f76373451`
- 原PDF：`sources/8323-2023/mit8_323_s23_pset01.pdf`；SHA-256：`e04333927536440f3d2c5dfff3e84f29840cc8612b028569010731cd767815c1`
- 解PDF：`sources/8323-2023/mit8_323_s23_pset_01sol.pdf`；SHA-256：`f120dd52b167c67500470090f0f90ed304ca76194d8eb0d617efea34a1f4d361`
- 原题URL：https://ocw.mit.edu/courses/8-323-relativistic-quantum-field-theory-i-spring-2023/mit8_323_s23_pset01.pdf
- 官方解URL：https://ocw.mit.edu/courses/8-323-relativistic-quantum-field-theory-i-spring-2023/mit8_323_s23_pset_01sol.pdf

### 作业2
- 正文：`chapters/assessment-8323-ps02.tex`
- 正文SHA-256：`57d8b613444958257a6a893f28a32128a0458d7d7e82aea905de7a8a9ea02087`
- 原PDF：`sources/8323-2023/mit8_323_s23_pset02.pdf`；SHA-256：`22a3b41e9c2e53327b5d22a2990bc1315b8098ec0826c16f40a01ca93a7a10b9`
- 解PDF：`sources/8323-2023/mit8_323_s23_pset_02sol.pdf`；SHA-256：`b494a8f4c1ab7a173f02065d6df15cbceb4d86cf424f0c62b5ee80bf92c52ed9`
- 原题URL：https://ocw.mit.edu/courses/8-323-relativistic-quantum-field-theory-i-spring-2023/mit8_323_s23_pset02.pdf
- 官方解URL：https://ocw.mit.edu/courses/8-323-relativistic-quantum-field-theory-i-spring-2023/mit8_323_s23_pset_02sol.pdf

### 作业3
- 正文：`chapters/assessment-8323-ps03.tex`
- 正文SHA-256：`97a22f456f51b30af986a678f64052f1efdc139f012227b619c9ba43ce118cf1`
- 原PDF：`sources/8323-2023/mit8_323_s23_pset03.pdf`；SHA-256：`bcb394db113b4cc2477a2e61e5420a3c93f2d9d7dd724a3f9e16e8b7174c900c`
- 解PDF：`sources/8323-2023/mit8_323_s23_pset_03sol.pdf`；SHA-256：`4839733d907074a8298e01a00165e00dbc054187eaf7959c8c60356bd71bd364`
- 原题URL：https://ocw.mit.edu/courses/8-323-relativistic-quantum-field-theory-i-spring-2023/mit8_323_s23_pset03.pdf
- 官方解URL：https://ocw.mit.edu/courses/8-323-relativistic-quantum-field-theory-i-spring-2023/mit8_323_s23_pset_03sol.pdf

### 作业4
- 正文：`chapters/assessment-8323-ps04.tex`
- 正文SHA-256：`b54521299722c793e24ed66918b450969e58b3bd73091ed284e326c6c2a39559`
- 原PDF：`sources/8323-2023/mit8_323_s23_pset04.pdf`；SHA-256：`01e274c77a1bad976f6b5dd5587ac4fe9a1657f1c18e39ed8236ca39dfc3fcb8`
- 解PDF：`sources/8323-2023/mit8_323_s23_pset_04sol.pdf`；SHA-256：`b80a8d0bac62304302e221879c857b3e26f8fcf36a1e316cb8dea33e77649fab`
- 原题URL：https://ocw.mit.edu/courses/8-323-relativistic-quantum-field-theory-i-spring-2023/mit8_323_s23_pset04.pdf
- 官方解URL：https://ocw.mit.edu/courses/8-323-relativistic-quantum-field-theory-i-spring-2023/mit8_323_s23_pset_04sol.pdf

### 作业5
- 正文：`chapters/assessment-8323-ps05.tex`
- 正文SHA-256：`f985426562b2e65d79be2d5ece03a4f04b0166081b6fcf6351e489c56c3b1d6f`
- 原PDF：`sources/8323-2023/mit8_323_s23_pset05.pdf`；SHA-256：`d4ffd46ca2a3c0a7cda64103b6bca271ea598639e7ca7d5060e7bc385d952798`
- 解PDF：`sources/8323-2023/mit8_323_s23_pset_05sol.pdf`；SHA-256：`cd87d611f32253f1a902671a7e5b70f3d0ae82406f1f5f5d228b810a516341b0`
- 原题URL：https://ocw.mit.edu/courses/8-323-relativistic-quantum-field-theory-i-spring-2023/mit8_323_s23_pset05.pdf
- 官方解URL：https://ocw.mit.edu/courses/8-323-relativistic-quantum-field-theory-i-spring-2023/mit8_323_s23_pset_05sol.pdf

### 作业6
- 正文：`chapters/assessment-8323-ps06.tex`
- 正文SHA-256：`063485bde558de299b0986ae564291d1b0c34cc661ad2b37310c876a6dc2a41a`
- 原PDF：`sources/8323-2023/mit8_323_s23_pset06.pdf`；SHA-256：`4ee35a2c495130043b1f88abe9ab7b76e1a53a0fd341c2843bdcc1c027cb87d5`
- 解PDF：`sources/8323-2023/mit8_323_s23_pset_06sol.pdf`；SHA-256：`c5e5a7d9fb5db93be1034b1750b54a7e569a29588e3d7f618b8a7bc9717df020`
- 原题URL：https://ocw.mit.edu/courses/8-323-relativistic-quantum-field-theory-i-spring-2023/mit8_323_s23_pset06.pdf
- 官方解URL：https://ocw.mit.edu/courses/8-323-relativistic-quantum-field-theory-i-spring-2023/mit8_323_s23_pset_06sol.pdf

## 剩余限制

没有在本分支编译或视觉审查前六套最终书页；全书排版由root负责。已视觉审查的是官方ps06题解的图页，不能据此声称中文书页版式已通过。没有使用商业教材外部题面或书页截图。
