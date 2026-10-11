# Course Notes 原例与中文正文独立复核

审阅快照：2026-10-11T17:08:58.695023+00:00。逐一比对14份冻结PDF的39个Worked Examples和70个Solved Problems，共109个原例，与 `main.tex` 实际纳入的 `ch01–ch12`、`tb01–tb12` 和 `ps01–ps11`。冻结原例的条件、图依赖、公式、重要数字和原请求见 `textbook-example-inventory.json`；本轮重新读实际中文题面和解答，不把该库存或题号出现视为通过。

本快照结论：完整 109；部分 0；存在错误 0；整例缺失 0；待审 0。本轮109例内容对应全部通过。每一例及其库存请求的实际文件、label、行号、SHA-256和审阅证据均写入 `textbook-example-coverage.json`。

## 计数与通过口径

109是原PDF中编号的Worked/Solved对象数。212是人工库存 `requests` 的语义项目数，包含若干复合请求，不能冒称212个原印字母小问或212个严格逻辑叶级。复合请求中的各分量、方向、数值和条件仍在逐例证据中核查。周五34题组169叶级为另一集合，其逐问审阅仍在 `assessment-review.md`，本报告不将两集合机械相加。65个Conceptual Questions和119个Additional Problems的完整库存保留在教材源清单，未因本例题复核自动删除或缩范围。

允许已经实写的共同推导跨引，允许明确的坐标旋转或符号重命名；前提是原条件和结论能具体对应。例如圆环R,Q轴场可以同时承接2.4、3.2、9.2的各自步骤，导体球壳自能可跨引原5.6与通用充电功。只有泛式、标题或源编号，没有实例条件/所求结果，则不通过。原题明确要求绘图时，仅给函数或“可画”不足以覆盖绘图请求。

## 初审缺口与返修复核

初次完整快照为101完整、7部分、1解释路径错误；经正文作者返修，本轮逐项重读确认下列8项已经闭环。JSON中保留初审计数和返修历史。

| 原例 / 小问 | 返修后实际内容 | 状态 |
|---|---|---|
| Example 2.2 | 固定Q,ℓ、x0≫ℓ的轴棒远场明确 | complete |
| 3.8.2 | 离轴r±精确根式、远场展开与Eφ=0完整 | complete |
| 7.9.3 | A→C→R2→负端与正板先入A的放电路径修正 | complete |
| 7.9.4(e) | 固定同端压、并联总功率严格大于串联 | complete |
| 10.9.1(b) | 线向上、环右方、场入纸与逆时针电流明确 | complete |
| 10.9.2 | B入纸条件恢复，最新句显式回答“所以电流顺时针” | complete |
| 10.9.6 | 线向上、环右方，外移感应顺时针明确 | complete |
| Example 11.4(b) | 本理想完全耦合的L1,L2及M=√L1L2等式已实例化 | complete |

初审7.9.3并非最终电流数值错误：`Is=ε/R1+(ε/R2)exp[−t/(R2C)]`正确，原错在“正板经R2流向A”的教学路径，该句现已修正。已实际重看原PDF物理21页图：A直接接C正板，R2在C负板与下节点之间；放电应由正板直接入A、经开关下行、经R2回负板。

10.9.4原问与原答案只要求动生电动势大小，稿实际给出的平行棒外移几何及大小已完整。最新正文也已补原水平图电流向左、棒在上方且向上移、场入纸与左端正右端负；独立按+y×(−z)=−x核对正确。此为依原图的补充解释，不虚构一个原题没有要求的独立极性小问。10.9.1和10.9.2明确要求电流方向；返修已恢复原图向，10.9.1明确逆时针，10.9.2最新句已显式回答顺时针。10.9.6也明确顺时针。

## 已实际复查通过的修订

- 1.10.1：常矢量恢复为(3,−5)，四个原函数都有实际坐标箭头图；1.10.2两个原标量曲面正负峰与原式一致。
- 3.1：新补有限均匀棒中垂线的实际对数势、求导场与长棒近似；最终重读确认该完整段落仍保留，轴延长线题首错误重复来源编号已清除、仅归源3.8.4；逆转该唯一短语可精确复现上次tb03 SHA，核实没有其他内容变化；3.8.1补了绝对值轴势的分段图；2.13.4补了原+y偶极的Cartesian两分量。
- 4.8.3：原球壳内引力零场已恢复，实心球明确另作变式；4.8.4实际势图亦已补。
- 5.4：三电容C1,C2并联后串C3，原件没有数值；5.10.1才是六只相同电容的三支路。5.7厚t介质任意位置及三个极限已补。
- 8.1：实际磁场恢复为+y，闭合半圆逆时针，直径和弧分别±z；9.2(b)实际圆环对固定轴向磁矩的力与同向/反向结论已补。
- 9.4：均匀厚电流板原三段场及固定K=J0b薄板极限已補；9.5孔内、环外和环体内均明确；9.11.5已交付实际双线场线图，解析场线不变量与场函数相切。
- 11.11.4开闸四阶段实际拓扑与反流，11.11.5消元时间函数，11.11.6孤立LC四问均完整。12.9.1–12.9.6所有原模型、重要数值和旁路开关各小问均有实际对应。
- 13.1/13.2及13.12.1–13.12.4的原太阳数字、波方向、驻波瞬时/平均能流、圆板充电与导体焦耳输入均有具体推导；向外法向积分负号自洽。
- 14章9个原例全部有实际对应，包含原级数/有效数字、斜入射约定、单缝第二旁峰原640nm近似与严格约651nm的区别、有限双缝11名义方向扣±4缺级得9非零级。

## 独立核算及库存更正

本轮用Python再次核算 `9e9*(1.6e−19)^2/(0.53e−10)^2 = 8.202207191171235e−8 N`，`Fe/e = 5.126379494482022e11 N/C`。原2.13.1(a)实际PDF物理29页印的是8.2e−8N，正文该力值正确。此前审阅者误读原力值、继而错误估算2.05e−8N的判断已撤回并更正库存。原(b)按0.5e−10m算得5.76e11，是与题面0.53e−10m不一致的舍入，正文已用同一题面半径。

原2.13.3图中E向下、电子向上；此前人工库存一度把图向反写，已重看原图和解答，库存方向更正，正文方向通过。上述两个更正均在覆盖JSON和例题库存内明确记录；没有依据旧库存把正确正文判错。

另核算12.9.1阻抗43.8634Ω、电流0.9119215A，故正文0.912A正确；14.11.6第2级强度4/π²=0.4052847，正文0.405正确；14.11.5第二旁峰精确波长650.6633nm，与正文约651nm一致。

最后图文件复核：`figures/vector-fields.tex`下排两个y轴标签由`node[above]`改为`node[right]`；已阅读两处差分，逆转两处可精确复现上一快照SHA，箭头端点、坐标、函数和数学文字均未改变。

本报告提供源—正文的内容/数学复核。新图的函数、方向和源码条件已读；本轮不声称完成新整册的编译、排版或逐页视觉验收，后者由相应QA记录承担。文件SHA记录的是本快照，正文并发返修后必须重读受影响条目再刷新状态，不能靠更新hash自动放行。

## 109例完整覆盖索引

| 原ID | 状态 | 实际正文位置 |
|---|---|---|
| Example 1.1 | complete | [chapters/tb01.tex:6](../chapters/tb01.tex) `ex:planet` |
| 1.10.1 | complete | [chapters/tb01.tex:42](../chapters/tb01.tex) `ex:fieldplots` |
| 1.10.2 | complete | [chapters/tb02.tex:21](../chapters/tb02.tex) `ex:scalarplots` |
| Example 2.1 | complete | [chapters/tb01.tex:61](../chapters/tb01.tex) `tb:coulombexamples` |
| Example 2.2 | complete | [chapters/ps02.tex:1](../chapters/ps02.tex) `全章/具体题见JSON`；[chapters/tb03.tex:35](../chapters/tb03.tex) `tb:potentialexamples` |
| Example 2.3 | complete | [chapters/ps02.tex:1](../chapters/ps02.tex) `全章/具体题见JSON`；[chapters/tb03.tex:4](../chapters/tb03.tex) `ex:offaxisrod` |
| Example 2.4 | complete | [chapters/ch03.tex:1](../chapters/ch03.tex) `ch:potential` |
| Example 2.5 | complete | [chapters/ch03.tex:1](../chapters/ch03.tex) `ch:potential`；[chapters/tb03.tex:52](../chapters/tb03.tex) `ex:annulus` |
| 2.13.1 | complete | [chapters/tb01.tex:72](../chapters/tb01.tex) `ex:hydrogen` |
| 2.13.2 | complete | [chapters/tb01.tex:80](../chapters/tb01.tex) `ex:millikan` |
| 2.13.3 | complete | [chapters/tb01.tex:87](../chapters/tb01.tex) `ex:electronplates` |
| 2.13.4 | complete | [chapters/tb03.tex:35](../chapters/tb03.tex) `tb:potentialexamples`；[chapters/ch03.tex:1](../chapters/ch03.tex) `ch:potential` |
| 2.13.5 | complete | [chapters/tb03.tex:28](../chapters/tb03.tex) `ex:chargedarc` |
| 2.13.6 | complete | [chapters/tb03.tex:4](../chapters/tb03.tex) `ex:offaxisrod`；[chapters/ps02.tex:1](../chapters/ps02.tex) `全章/具体题见JSON` |
| Example 3.1 | complete | [chapters/tb03.tex:1](../chapters/tb03.tex) `tb:finitesources` |
| Example 3.2 | complete | [chapters/ch03.tex:1](../chapters/ch03.tex) `ch:potential` |
| Example 3.3 | complete | [chapters/tb03.tex:52](../chapters/tb03.tex) `ex:annulus`；[chapters/ch03.tex:1](../chapters/ch03.tex) `ch:potential` |
| Example 3.4 | complete | [chapters/tb03.tex:35](../chapters/tb03.tex) `tb:potentialexamples` |
| 3.8.1 | complete | [chapters/tb03.tex:65](../chapters/tb03.tex) `ex:dipoleaxis` |
| 3.8.2 | complete | [chapters/tb03.tex:35](../chapters/tb03.tex) `tb:potentialexamples`；[chapters/ch03.tex:1](../chapters/ch03.tex) `ch:potential` |
| 3.8.3 | complete | [chapters/tb03.tex:52](../chapters/tb03.tex) `ex:annulus` |
| 3.8.4 | complete | [chapters/tb03.tex:39](../chapters/tb03.tex) `ex:rodpotential` |
| Example 4.1 | complete | [chapters/ch04.tex:1](../chapters/ch04.tex) `ch:gauss` |
| Example 4.2 | complete | [chapters/ch04.tex:1](../chapters/ch04.tex) `ch:gauss` |
| Example 4.3 | complete | [chapters/ch04.tex:1](../chapters/ch04.tex) `ch:gauss` |
| Example 4.4 | complete | [chapters/ch04.tex:1](../chapters/ch04.tex) `ch:gauss` |
| Example 4.5 | complete | [chapters/tb04.tex:42](../chapters/tb04.tex) `tb:electric-pressure`；[chapters/ch05.tex:1](../chapters/ch05.tex) `ch:capacitor` |
| Example 4.6 | complete | [chapters/tb04.tex:59](../chapters/tb04.tex) `tb:charged-sphere`；[chapters/tb04.tex:42](../chapters/tb04.tex) `tb:electric-pressure`；[chapters/tb05.tex:12](../chapters/tb05.tex) `tb:energy-create`；[chapters/ch05.tex:1](../chapters/ch05.tex) `ch:capacitor` |
| 4.8.1 | complete | [chapters/tb04.tex:1](../chapters/tb04.tex) `tb:gauss-local` |
| 4.8.2 | complete | [chapters/tb04.tex:9](../chapters/tb04.tex) `ex:squareflux` |
| 4.8.3 | complete | [chapters/tb04.tex:1](../chapters/tb04.tex) `tb:gauss-local` |
| 4.8.4 | complete | [chapters/tb04.tex:59](../chapters/tb04.tex) `tb:charged-sphere` |
| Example 5.1 | complete | [chapters/ch05.tex:1](../chapters/ch05.tex) `ch:capacitor` |
| Example 5.2 | complete | [chapters/ch05.tex:1](../chapters/ch05.tex) `ch:capacitor` |
| Example 5.3 | complete | [chapters/ch05.tex:1](../chapters/ch05.tex) `ch:capacitor`；[chapters/tb05.tex:12](../chapters/tb05.tex) `tb:energy-create` |
| Example 5.4 | complete | [chapters/tb05.tex:1](../chapters/tb05.tex) `tb:cap-networks` |
| Example 5.5 | complete | [chapters/tb05.tex:12](../chapters/tb05.tex) `tb:energy-create` |
| Example 5.6 | complete | [chapters/tb05.tex:12](../chapters/tb05.tex) `tb:energy-create`；[chapters/ch05.tex:1](../chapters/ch05.tex) `ch:capacitor` |
| Example 5.7 | complete | [chapters/tb05.tex:72](../chapters/tb05.tex) `tb:atomic-forces` |
| 5.10.1 | complete | [chapters/tb05.tex:1](../chapters/tb05.tex) `tb:cap-networks` |
| 5.10.2 | complete | [chapters/tb05.tex:26](../chapters/tb05.tex) `tb:dielectric-boundary` |
| 5.10.3 | complete | [chapters/tb05.tex:26](../chapters/tb05.tex) `tb:dielectric-boundary`；[chapters/ch05.tex:1](../chapters/ch05.tex) `ch:capacitor` |
| 5.10.4 | complete | [chapters/tb05.tex:57](../chapters/tb05.tex) `tb:cap-force` |
| 6.5.1 | complete | [chapters/tb06.tex:1](../chapters/tb06.tex) `tb:drude` |
| 6.5.2 | complete | [chapters/tb06.tex:1](../chapters/tb06.tex) `tb:drude` |
| 6.5.3 | complete | [chapters/tb06.tex:1](../chapters/tb06.tex) `tb:drude` |
| 6.5.4 | complete | [chapters/tb06.tex:1](../chapters/tb06.tex) `tb:drude` |
| 6.5.5 | complete | [chapters/tb06.tex:1](../chapters/tb06.tex) `tb:drude` |
| 7.9.1 | complete | [chapters/tb06.tex:51](../chapters/tb06.tex) `tb:kirchhoff-examples` |
| 7.9.2 | complete | [chapters/tb06.tex:51](../chapters/tb06.tex) `tb:kirchhoff-examples` |
| 7.9.3 | complete | [chapters/tb06.tex:80](../chapters/tb06.tex) `tb:rc-switch` |
| 7.9.4 | complete | [chapters/tb06.tex:51](../chapters/tb06.tex) `tb:kirchhoff-examples` |
| 7.9.5 | complete | [chapters/tb06.tex:73](../chapters/tb06.tex) `ex:resistorcube` |
| Example 8.1 | complete | [chapters/tb08.tex:20](../chapters/tb08.tex) `tb:rod-magnetic` |
| 8.9.1 | complete | [chapters/tb08.tex:20](../chapters/tb08.tex) `tb:rod-magnetic` |
| 8.9.2 | complete | [chapters/tb08.tex:20](../chapters/tb08.tex) `tb:rod-magnetic` |
| 8.9.3 | complete | [chapters/tb08.tex:1](../chapters/tb08.tex) `tb:selector` |
| 8.9.4 | complete | [chapters/tb08.tex:20](../chapters/tb08.tex) `tb:rod-magnetic` |
| Example 9.1 | complete | [chapters/tb07.tex:1](../chapters/tb07.tex) `tb:finite-b` |
| Example 9.2 | complete | [chapters/ch07.tex:1](../chapters/ch07.tex) `ch:magnetostatics`；[chapters/tb07.tex:74](../chapters/tb07.tex) `tb:offaxis-loop` |
| Example 9.3 | complete | [chapters/ch07.tex:1](../chapters/ch07.tex) `ch:magnetostatics` |
| Example 9.4 | complete | [chapters/tb07.tex:74](../chapters/tb07.tex) `tb:offaxis-loop` |
| 9.11.1 | complete | [chapters/tb07.tex:1](../chapters/tb07.tex) `tb:finite-b` |
| 9.11.2 | complete | [chapters/tb07.tex:1](../chapters/tb07.tex) `tb:finite-b` |
| 9.11.3 | complete | [chapters/tb07.tex:1](../chapters/tb07.tex) `tb:finite-b` |
| 9.11.4 | complete | [chapters/tb07.tex:1](../chapters/tb07.tex) `tb:finite-b` |
| 9.11.5 | complete | [chapters/tb07.tex:44](../chapters/tb07.tex) `tb:distributed-current` |
| 9.11.6 | complete | [chapters/tb07.tex:44](../chapters/tb07.tex) `tb:distributed-current` |
| 9.11.7 | complete | [chapters/tb07.tex:44](../chapters/tb07.tex) `tb:distributed-current` |
| 9.11.8 | complete | [chapters/tb07.tex:1](../chapters/tb07.tex) `tb:finite-b` |
| Example 9.5 | complete | [chapters/tb07.tex:74](../chapters/tb07.tex) `tb:offaxis-loop`；[chapters/ch07.tex:1](../chapters/ch07.tex) `ch:magnetostatics` |
| 10.9.1 | complete | [chapters/tb09.tex:23](../chapters/tb09.tex) `tb:wire-flux` |
| 10.9.2 | complete | [chapters/tb09.tex:23](../chapters/tb09.tex) `tb:wire-flux` |
| 10.9.3 | complete | [chapters/tb09.tex:23](../chapters/tb09.tex) `tb:wire-flux` |
| 10.9.4 | complete | [chapters/tb09.tex:23](../chapters/tb09.tex) `tb:wire-flux` |
| 10.9.5 | complete | [chapters/tb09.tex:10](../chapters/tb09.tex) `tb:induced-e` |
| 10.9.6 | complete | [chapters/tb09.tex:23](../chapters/tb09.tex) `tb:wire-flux` |
| Example 11.1 | complete | [chapters/tb09.tex:98](../chapters/tb09.tex) `tb:coupled-l` |
| Example 11.2 | complete | [chapters/ch09.tex:1](../chapters/ch09.tex) `ch:induction` |
| Example 11.3 | complete | [chapters/tb09.tex:73](../chapters/tb09.tex) `tb:toroid-l` |
| Example 11.4 | complete | [chapters/tb09.tex:98](../chapters/tb09.tex) `tb:coupled-l`；[chapters/tb09.tex:111](../chapters/tb09.tex) `tb:magnetic-pressure` |
| Example 11.5 | complete | [chapters/ch09.tex:1](../chapters/ch09.tex) `ch:induction` |
| 11.11.1 | complete | [chapters/tb09.tex:73](../chapters/tb09.tex) `tb:toroid-l` |
| 11.11.2 | complete | [chapters/tb09.tex:73](../chapters/tb09.tex) `tb:toroid-l` |
| 11.11.3 | complete | [chapters/tb09.tex:23](../chapters/tb09.tex) `tb:wire-flux` |
| 11.11.4 | complete | [chapters/tb10.tex:1](../chapters/tb10.tex) `tb:rl-networks` |
| 11.11.5 | complete | [chapters/tb10.tex:1](../chapters/tb10.tex) `tb:rl-networks` |
| 11.11.6 | complete | [chapters/tb10.tex:31](../chapters/tb10.tex) `tb:rlc-initial` |
| 12.9.1 | complete | [chapters/tb10.tex:49](../chapters/tb10.tex) `tb:phasor-diagrams` |
| 12.9.2 | complete | [chapters/tb10.tex:49](../chapters/tb10.tex) `tb:phasor-diagrams` |
| 12.9.3 | complete | [chapters/tb10.tex:75](../chapters/tb10.tex) `tb:resonance-design` |
| 12.9.4 | complete | [chapters/tb10.tex:106](../chapters/tb10.tex) `tb:ac-filters` |
| 12.9.5 | complete | [chapters/tb10.tex:106](../chapters/tb10.tex) `tb:ac-filters` |
| 12.9.6 | complete | [chapters/tb10.tex:106](../chapters/tb10.tex) `tb:ac-filters` |
| Example 13.1 | complete | [chapters/tb11.tex:11](../chapters/tb11.tex) `tb:solar` |
| Example 13.2 | complete | [chapters/tb11.tex:50](../chapters/tb11.tex) `tb:standing-wave` |
| 13.12.1 | complete | [chapters/tb11.tex:1](../chapters/tb11.tex) `tb:wave-directions` |
| 13.12.2 | complete | [chapters/tb11.tex:1](../chapters/tb11.tex) `tb:wave-directions` |
| 13.12.3 | complete | [chapters/ch11.tex:1](../chapters/ch11.tex) `ch:maxwell`；[chapters/ps10.tex:1](../chapters/ps10.tex) `全章/具体题见JSON` |
| 13.12.4 | complete | [chapters/tb11.tex:25](../chapters/tb11.tex) `tb:coax-poynting` |
| Example 14.1 | complete | [chapters/tb12.tex:1](../chapters/tb12.tex) `tb:young-geometry` |
| Example 14.2 | complete | [chapters/tb12.tex:15](../chapters/tb12.tex) `tb:n-slit` |
| Example 14.3 | complete | [chapters/tb12.tex:34](../chapters/tb12.tex) `tb:single-slit-extrema` |
| 14.11.1 | complete | [chapters/tb12.tex:53](../chapters/tb12.tex) `tb:interference-examples` |
| 14.11.2 | complete | [chapters/tb12.tex:53](../chapters/tb12.tex) `tb:interference-examples` |
| 14.11.3 | complete | [chapters/tb12.tex:1](../chapters/tb12.tex) `tb:young-geometry` |
| 14.11.4 | complete | [chapters/tb12.tex:53](../chapters/tb12.tex) `tb:interference-examples` |
| 14.11.5 | complete | [chapters/tb12.tex:34](../chapters/tb12.tex) `tb:single-slit-extrema` |
| 14.11.6 | complete | [chapters/tb12.tex:53](../chapters/tb12.tex) `tb:interference-examples` |
