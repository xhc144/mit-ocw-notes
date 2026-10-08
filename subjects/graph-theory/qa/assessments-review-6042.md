# 6.042J Spring 2015 新增评测题：独立数学与来源对象复审

审查者：独立模型代理 `matrix_electric_audit`。记录日期：2026-10-08（UTC）。

已逐字读完下表八个最终 LaTeX 文件中的全部中文题面、原小问、答案、证明、反例和共用引理；按原卷定位核对 50 个去重后的 PDF 主问题（147 个原顶层回答单元，另读 CP17:4(f) 的三个子项），以及 36 个公开在线页面的全部 75 个原 Q。CP32:1–5 的五个重复来源位置及标签仍保留，内容与 CP19 合并。当前版本未发现需要继续阻止合册的数学错误。此次结论针对下列字节版本，后续数学改动须重新核对。

这是一份独立模型的审读记录，不能称为人类专家审定。有限实例检查支持具体计算和算法互逆，但不代替下文所审的一般证明。没有在此宣称最终主 PDF 逐页视觉、版权法律审定、PDF 目录点击、ZIP 干净重编或远端完整性验收；这些是父代理另行完成的门槛。

## 最终文件绑定

本次只写本 QA 文件；没有改动八个被审源文件。作者对独审意见的返修仍由作者或父代理实施。前次作者任务中另获父代理授权的 18.212 行内排版改动与本次只读 6.042 审读分开记录。

| 文件（相对 `subjects/graph-theory/`） | SHA-256 |
|---|---|
| `assessments/6042/cp-a.tex` | `a6790e7b2f4e6d4f090edf29bbec6b8eb862c4e28fe2e409ba3a0319d3b3b77e` |
| `assessments/6042/cp-b.tex` | `b9ca1c409d5fe5ad066be5142408f7e613fcc10a20195a39a1ea666a6efa026a` |
| `assessments/6042/cp-c.tex` | `23086af3c917d7b3dbf9bc60187d7f0d2be344f201c952b79f668a622ed215b2` |
| `assessments/6042/exams.tex` | `f95329518e719f1d57440689c387badeb362fa58fbdfc72bf5017f388c2c4651` |
| `assessments/6042/lemmas.tex` | `4e79f6499dce917893b6ae065ff27ccdfdcadfa5de0bd18098f8475f1f241870` |
| `assessments/6042/main.tex` | `8e825fab1f89df0637cb192c2087f43c99df09b282d227639042df13a082a198` |
| `assessments/6042/online.tex` | `23d65e945c9ac95f5141bf312015a4f6c0b5e70be12bdf577420e57d374c6705` |
| `assessments/6042/ps.tex` | `f56962553ce7e5cb5a30e641e1ce346ea75b2583fd34d99230605244f8a6bb27` |
| `qa/assessments-draft-6042.md` | `7f0b0a8c34d87421572cf615f50e412374817cb541b4dc180daf258a8104eb0d` |
| `qa/assessments-inventory-6042.json` | `9ec9654057ce99df80711605db6b31014a83085d1fa1123b2e4f753bf9dfa6c8` |


## 实际来源比对范围

逐项读取了对应 19 份官方来源 PDF 的入选题正文提取文本；题干跨页时连读其后续页。Final 和 Midterm 的标题形式与 PS/CP 不同，按题号而非仅按 `Problem n.` 句点检索。原卷没有可用的官方完整 PDF 解答，本稿标为编者独立解答；在线 HTML 的答案标记、实际公开解释、原图资产单独核对，未将二者混称为官方完整答案。

实际打开 `review-images/` 内全部 17 张已留存来源页图，另直接渲染并打开 CP32 第2页以核实重复图形，并放大 CP33 第2页公式，确认根号覆盖的是 `mu log mu`，不是仅 `mu`。源页查看是题面对象核对，不是新书的全页视觉验收。实看的 17 张为 CP10:4、CP16:2、CP17:2及4、CP18:2、CP19:2、CP20:3、CP25:1、CP33:2、CP35:1及2、Final:5及6、Midterm3:2、PS6:2、PS7:2、PS8:1。

36 个入选 HTML 的公共正文全部读取，包括题目 div 外的共同前提、先修表和边集；另核对索引中原 Q 的控制器答案与公开解释。15 种不同图像资产全部实际打开（共有16个依赖路径，两个随机游走 JPG 内容相同）。透明 PNG 在临时白底上显示后才判断边和标签。Tree or Not Tree 的无标签图按位置重标号；边的几何交叉未当成额外顶点。

原图与中文版数学对象逐一吻合：PS7 四图的边数/度数及同构映射，PS8 五圈 Mycielski 图，CP10 满二叉树的左右子树及四个叶位置，CP16 二位 de Bruijn 图的八弧（含自环），CP17 两个先修图和工时表，CP19/32 两图的七边，CP20 OR 器件的三角形/虚线边/曲线边，CP25 最大叶示例树，Midterm3 八任务七弧，CP35 三个转移图及在线同图；在线四树图、三对同构图、两张五点图、整除覆盖图、三二分图例、七点轮图均核对了原资产。CP21 网格由原题坐标与权公式定义，未需要猜图。

19 个 PDF、36 个 HTML 和16个图像依赖路径的现有文件 SHA 均实际重新计算，与冻结清单及反馈索引一致。来源本次审读用到的清单与各 PDF 字节值见后表；完整 HTML/资产逐文件证据由下列索引哈希绑定。此项是来源字节和题面归属核对，不扩展许可。

## 一般证明、条件及逐题结论

**稳定匹配共用引理、PS8:3、CP22:1–4、Midterm3:5及所有在线匹配题。** 共用引理明确等人数、严格完整偏好，完美匹配与阻塞对均已定义。最初按日算法的“每对至多一次申请”计数不成立，因为保留者会每日重访；独审提出后，最终文本分别用拒绝日至少永久删一对、无拒绝日停止，和逐次新申请总数至多 n² 证明有限终止。名单耗尽时所有女方已保留其他不同男方的计数矛盾、女方质量单调、终局稳定的阻塞反证均成立。首次拒绝稳定可行配对的论证使用“在此之前”与严格偏好，未偷用最终男方最优；继而得男方最优、女方最差、换侧极端、两极相同当且仅当稳定解唯一，依赖关系没有循环。

PS8:3(a)(b) 不依赖未指定排序尾部；组内男方或女方已得首选，跨组由较早组一方拒绝潜在阻塞。偶数 n 的双人组与奇数 n≥3 的三人循环组均实际给出稳定构造，n=1 原断言失败注明。CP22:1 两次申请的逐轮拒绝链符合源表，两种输出确不同。CP22:2 的 (e) 反例完整可达，(a)(c)(d) 保持；在线不变量承认恒假谓词也满足保持定义，并区分等人数与 Midterm3 男方较多时的最后名字可能划去。原 Midterm3(d) 的 “women he is serenading” 是对当前全部申请对象的量词，因此名单空时的空真解释成立。

CP22:4 的官方核心模型按双方严格完整排序、真实对象全可接受理解；医院按个人排序保留容量内最优者，即响应性选择，而非任意医院对学生集合的偏好。该模型的容量 DA、有限申请、被拒后容量满且更优、质量单调证明通过。允许不可接受对象的扩展在最后一段用克隆岗位、固定内部次序、虚拟对象及删去不可接受真实配对处理；若删除后在医院模型有双方可接受的阻塞，空岗位或较差真实学生对应的槽位原来只能是虚拟/不可接受对象或较差对象，于是也阻塞克隆模型，故转换有效。独审曾建议直接算法也明说过滤不可接受对象；父代理维持冻结，此为扩展算法措辞建议，不将当前核心模型误读为任意集合偏好模型的证明。

**PS4:2、CP10:4、CP21:2及4、Final:2、在线树题。** PS4 所数的是不同标签集合，两个子树不交与新根标签不重复恰用于两处基数加法；CP10 所数的是叶位置，重复 win 标签允许，结构归纳没有混淆二者。唯一端点路径与树的等价式补非空；单点及空森林边界分别注明。“width 1”按原题为存在每点至多一个更早邻点的次序，不是精确退化度也不是树宽，最新顶点反驳圈与删叶归纳皆完整。在线叶数 2、98、1000 都有下界/上界与达到构造；孤立点没有错误计为叶。标边算法固定全部 V，初态无边森林并非树的空真情形，六个单调性逐次增减量正确。

**PS6:2–3、CP16:1–4、PS7:4、CP20:2、Midterm3:3及在线游走题。** 互相可达不推出共同简单圈的三点构造，以及某点正闭合游走推出该点有向圈的最短化正确；奇闭合游走拆成两个闭合段时取奇段的归纳，不能错误推广为原指定顶点也在奇圈。竞赛图王的两个例子和最大出度反证正确，Hamilton 路插入归纳覆盖首/中/尾全部情况。CP16:2 补有限可达距离，拼接最短游走若重复就严格缩短；无 `infinity=infinity` 假等价。de Bruijn 例的八个窗口、八弧对应、好串下界、一般 k 的移位/入出度/正闭合游走和 Euler 拼接引用均正确。

PS7:4 的路径图译名按原题自己定义，K2 不交并 C3 是反例；伪归纳未覆盖任意更大图的量词缺口清楚。CP20:2 删点可能使唯一邻点孤立，归纳条件不能保留。Midterm3:3 两不同路径在首次分离至首次重新相遇间成圈，两个原端点可以是叶。在线邻接矩阵 A² 计两步游走、完全有向图路径计数及16点10弧的有向汇点极端构造符合源单元。

**PS7:3、CP19/32:1–5及所有在线同构/度数题。** PS7 源四图只有 G1/G4 同构，给出的十点映射保持全部15边；G3 有16边和两个度4点，G2 有四圈而 G1 无，圈长保持证明完整。CP19/32 七边图恰四个同构，两对特殊顶点的选像与剩余路径强制性证明穷尽，不只列候选。等長画法的“存在一种画法”与当前长度的差别处理正确；邻点集逐元素 iff 使用逆双射，出度计数随之保持。平均伴侣数的两侧度和相等而分母不同，边数 e>0 假设使比例可除；16/19 与10/11计算正确。奇度结论在 George 所在分支内用，故另一奇度点确实可达。Final:5 四个度序列的上限、奇偶、连通边数与两个全度顶点反证齐全。

在线 Extreme Graphs 总度44为22边，K7添一新点一边实现八点；原公开解释添两边错误已注明。五圈十个同构、Non-Isomorphic 中虚假的最后一项、数字名字与画角并非不变量，都符合原图。源轮图若总顶点 n 偶，则外圈 n−1 奇，色数4；只有把 n 改为外圈点数才得3，稿件明确源冲突，没有悄悄改定义。

**PS8:1–2、CP20:1及3–4、CP21:1及3、在线 MST/连通/染色题。** MST 唯一和唯一全局最轻边证明明确连通，交换边必不在候选树、权比较严格；不同边权只是唯一的充分条件，源在线“只有互异才唯一”已纠正。CP21 的24边权均互异；Kruskal、Prim 的15条实际次序和并行三棵初树第一轮相遇位置正确，最后同一边集总权369/100。引用正文安全边定理时森林包含于某个 MST 的不变量成立；没有将每次独立安全当作任意同时选边均安全，本例另外给出共同包含的 MST。

PS8 Mycielski 无三角形的两类论证、显式四色与若三色就把原色3顶点改成其影点颜色而二染奇五圈的反证正确。寄存器13条冲突边对应输入和每步活跃集，最后一次读取后可同一步覆盖的源约定已留；四寄存器分配及 K4 下界一致，重复赋值拆值而不永久视为同一顶点。逻辑门完全边集与原图一致，四输入的存在表、任何扩张的强制输出及改变 Tx 为 Fx 的 AND 表均通过，不只验证单一色表。

CP20 H3 的九条最终显示路径逐边为一位翻转，各距离组内部顶点互不相交；作者自己发现并修正距2第三条非邻接步骤，独审实际重新逐边检查了修正版。删点归纳证明一般 Hn 连通度 n，完美匹配剩余边数、删除集中在一份时的对应点连接及 K2 约定均正确。正文 ch03 的全局 Menger 推论还处理相邻端点（删 st、用 k−1 路再加直接边），因此 H4 路数引用并未误用仅非相邻端点的定理。在线 k 连通关系用的 kappa≤lambda 也在同章已有一般证明。

**CP17:1–4、CP18:3、Midterm3:1、Final:4及全部在线偏序调度题。** CP17 的历史15课表与在线12课表分别按源数据核对，未混合时代或以其当代先修规定。前者六学期关键链、九个排除18.03的最大反链、8学期两门/6学期三门的可行课表正确且先修均在更早时段。八任务表原工时和全部先修弧一致，总工时74/2=37、关键链39、40天方案逐项可行。

独审指出“39不可能+40方案”尚需排除连续非整数39.5等可能，作者新加入完整整数规范化：把任一可行方案的每人任务顺序加入 DAG；正工时的时间不等式排除圈；拓扑序最早开始给整数时刻，逐项不晚于原方案。因此任意<40的方案可化为≤39，再由关键链与39不可行证明排除。该返修完整复读，填补的正是一般下界推理，未靠有限模拟替代。关键链连续占据一人时链外任务2和4不能重叠，两种顺序分别违反任务4/2的最后期限，39不可行的论证也成立。

n任务、最长t链的最小可能人数 ceil(n/t) 有非空不交链构造，最大 n−t+1 有分层上界与末层星形下界，t=1 分开处理。CP17 覆盖弧由正可达关系的中间点刻画，最长路径替代不可能重复（否则成圈），所以删非覆盖弧保持可达且最长路径不变；正可达包含对角这一约定解释了任意同关系图必仍无圈，以及自环反例。三圈的三弧均覆盖、完全三点有向图无覆盖，却同为全部九个正可达对，均按源定义正确。CP18 全部最长序列、十条 Hasse 覆盖弧、链/反链双向解释、n≤hw 后不对称平方根界证明完整。

在线 Scheduling Prerequisites Q4 的隐藏数值答案5与该页自己的先修表冲突；本稿正确值6，六元反链与六链覆盖分别证明下界/上界，且独立全部4096顶点子集复算确认唯一六元最大反链。Q1–3链/反链分类及Q5十二学期对应同一源表。DAG 在线题原二元关系非空约定与本册空图约定明确分开；整除图添加24只需8、12两覆盖弧，必要性由中间点不存在给出。处理器上下界都由链和分层推导，没有声称所有实例总等于某个下界。

**CP25:2、CP30:3、CP33:4、CP35:1–3、Final:9及12、全部在线随机游走题。** 最大叶 Prüfer 解码的当前点集/剩余串候选至少两个、首项还留存、逆向接叶成树均正确；计数次数为度−1在每个残树成立，故两个方向逐步恢复同一规则。对任意串直接解码后的树，某顶点的记录邻边数就是其串出现次数，加自身删除/最后连接边恰为度−1；这也说明任意串再编码返回原串，并非只从集合等势推测双射。两例树边与官方图逐边相同。

随机图事件独立性依赖不同随机边组；两步事件与本对直接边独立，而共享或不同四端点的两步事件均可能依赖。n4,p1/2 的64边集联合计数17/64与20/64实际复算，和(7/16)²不同；p0、p1退化独立注明。无二步路径概率(1−p²)^(n−2)与三角形概率p(1−r)无重复边组假设错误。三色三角形同时单色共边时须五条边同色，均匀时两两指示量独立但不需要相互独立；方差8mu/9及含sqrt(mu log mu)的 Chebyshev 界注明 mu>1，即n≥5。Final:9 期望线性性未误要求各度独立，n≤2 与n0不可指定顶点边界明确。

三个 Markov 矩阵方向/自环概率符合原 PDF 及在线图；图1仅初始均匀分布收敛，图2平稳(9/19,10/19)和误差(−0.9)^t，图3全部平稳(s,0,0,1−s)均推导充分。b吸收到d概率1/3由第一步方程和未吸收质量2^(−t)同时保证为实际极限，而非仅形式 Dirichlet 解。均匀平稳 iff 列和1的证明补有限非空；对称等概率游走的度数平稳公式补正出度和e>0，并使用入度=出度。Google-graph 讨论限于源对称玩具模型，没有当作当前搜索系统规则。Final三种构造的不可数、唯一非强连通、强连通却周期不收敛都正确。在线 Friends and Strangers 单独区分六点论证仅得R(3,3)≤6，再以五圈补下界才得等号。

## 独立计算证据

下面脚本由本审查代理独立在 `/tmp/6042-independent-check.py` 编写并实际运行，未调用作者 `review-checks.py` 作为数学证明。两段 JSON 为同一脚本的实际输出。脚本仅使用 Python 标准库，不联网，不改正文。所有断言通过，退出码0。

- 最大叶 Prüfer：n=2–7全部18248个码串，检查解码→编码及所得树互不重复；明确n=2是额外边界检查，原题为n>2。
- OR/AND：枚举每一输入下所有辅助点三色赋值，输出只能是目标值且扩张非空。
- 两步随机图：n=4全部64图；K4均匀三色的729个赋色精确均值4/9、方差32/81。
- 在线先修全部4096子集，CP17全部32768子集，独立传递闭包后检查所有反链。
- PS8全部256种未指定尾部补全；每种检查所有24个匹配，并验证原匹配及两个指定更差/更优稳定匹配。CP22按官方完整偏好全部24匹配实际恰两个稳定解。
- Markov有理数方程及t=0–12的分布/生存概率；九条立方体路径逐边与内部不交；全部512个序列子集复得两条LIS与六条LDS；PS7映射/四圈、CP19全部720双射、Mycielski 7776种固定中心三色候选和四色见证、寄存器四色与K4均通过。

机械覆盖另独立核对：86对exercise/solution、132个新label无重复、75个在线Q label、22个正文引用均在当前本册TeX标签集合找到。仅静态存在性不等于PDF链接可点。147的口径是原顶层回答单元；CP17:4(f)(i)–(iii)等嵌套内容仍已逐项读审，未以顶层计数掩盖遗漏。

```json
{
  "maximum_leaf_prufer_two_way": [
    {
      "n": 2,
      "codes": 1
    },
    {
      "n": 3,
      "codes": 3
    },
    {
      "n": 4,
      "codes": 16
    },
    {
      "n": 5,
      "codes": 125
    },
    {
      "n": 6,
      "codes": 1296
    },
    {
      "n": 7,
      "codes": 16807
    }
  ],
  "gadget_OR": [
    {
      "P": 0,
      "Q": 0,
      "output": 0,
      "extensions": 4
    },
    {
      "P": 0,
      "Q": 1,
      "output": 0,
      "extensions": 1
    },
    {
      "P": 1,
      "Q": 0,
      "output": 0,
      "extensions": 1
    },
    {
      "P": 1,
      "Q": 1,
      "output": 1,
      "extensions": 2
    }
  ],
  "gadget_AND": [
    {
      "P": 0,
      "Q": 0,
      "output": 0,
      "extensions": 2
    },
    {
      "P": 0,
      "Q": 1,
      "output": 1,
      "extensions": 1
    },
    {
      "P": 1,
      "Q": 0,
      "output": 1,
      "extensions": 1
    },
    {
      "P": 1,
      "Q": 1,
      "output": 1,
      "extensions": 4
    }
  ],
  "two_step_random_graph_counts_out_of64": {
    "wx": 28,
    "xy": 28,
    "yz": 28,
    "wx_and_xy": 17,
    "wx_and_yz": 20
  },
  "K4_729_edge_colorings": {
    "mean": "4/9",
    "variance": "32/81"
  },
  "online_schedule_4096_subsets": {
    "width": 6,
    "max_antichains": 1,
    "witness": [
      "18.02",
      "18.03",
      "8.02",
      "6.046",
      "6.006",
      "6.034"
    ]
  },
  "CP17_32768_subsets": {
    "width": 5,
    "max_antichains_without1803": 9,
    "witnesses": [
      [
        "18.02",
        "6.042",
        "6.034",
        "6.003",
        "6.004"
      ],
      [
        "18.02",
        "6.046",
        "6.034",
        "6.003",
        "6.004"
      ],
      [
        "18.02",
        "6.840",
        "6.034",
        "6.003",
        "6.004"
      ],
      [
        "18.02",
        "6.042",
        "6.034",
        "6.003",
        "6.033"
      ],
      [
        "18.02",
        "6.046",
        "6.034",
        "6.003",
        "6.033"
      ],
      [
        "18.02",
        "6.840",
        "6.034",
        "6.003",
        "6.033"
      ],
      [
        "18.02",
        "6.042",
        "6.034",
        "6.003",
        "6.857"
      ],
      [
        "18.02",
        "6.046",
        "6.034",
        "6.003",
        "6.857"
      ],
      [
        "18.02",
        "6.840",
        "6.034",
        "6.003",
        "6.857"
      ]
    ]
  },
  "PS8_all_256_preference_completions_original_and_both_extremes_stable": 256,
  "CP22_stable_assignments_of24": {
    "count": 2,
    "assignments": [
      [
        1,
        2,
        0,
        3
      ],
      [
        2,
        1,
        0,
        3
      ]
    ]
  },
  "Markov_exact_13_times": {
    "pi2": [
      "9/19",
      "10/19"
    ],
    "b_to_d_absorption": "1/3",
    "survival": "2^-t"
  }
}
{
  "final_9_cube_paths": true,
  "CP18_all512_subsequences": true,
  "PS7_supplied_map_and_all4cycles": true,
  "CP19_all720_vertex_maps_isomorphisms": 4,
  "Mycielski_7776_colours_excluded_and_4colour_witness": true,
  "register_4colour_K4_witness": true
}
```

```python
from itertools import product, combinations, permutations
from collections import Counter
from fractions import Fraction
import json
out={}
def norm(e):return tuple(sorted(e))
def pdecode(code,n):
 rem=set(range(1,n+1));edges=[]
 for i,a in enumerate(code):
  leaf=max(rem-set(code[i:]));assert leaf!=a
  edges.append(norm((leaf,a)));rem.remove(leaf)
 edges.append(tuple(sorted(rem)));return tuple(sorted(edges))
def pencode(edges,n):
 adj={a:set() for a in range(1,n+1)}
 for a,b in edges:adj[a].add(b);adj[b].add(a)
 code=[]
 for _ in range(n-2):
  leaf=max(a for a in adj if len(adj[a])==1);b=next(iter(adj[leaf]));code.append(b);adj[b].remove(leaf);del adj[leaf]
 return tuple(code)
pr=[]
for n in range(2,8):
 seen=set()
 for c in product(range(1,n+1),repeat=n-2):
  e=pdecode(c,n);assert pencode(e,n)==c;seen.add(e)
 assert len(seen)==n**(n-2);pr.append({'n':n,'codes':len(seen)})
assert pdecode((6,5,6,2,2),7)==tuple(sorted(map(norm,[(7,6),(4,5),(5,6),(6,2),(3,2),(1,2)])))
assert pdecode((4,3,2),5)==((1,2),(2,3),(3,4),(4,5))
out['maximum_leaf_prufer_two_way']=pr
# Edge-table OR/AND gadget; T=0 F=1 N=2, P,Q Boolean.
base=[('T','F'),('F','N'),('N','T'),('N','P'),('N','Q'),('N','O'),('x','O'),('x','z'),('O','u'),('O','v'),('u','v'),('u','P'),('v','Q'),('P','z'),('Q','z')]
for kind,a in [('OR','T'),('AND','F')]:
 edges=base+[ (a,'x') ];table=[]
 for p,q in product((0,1),repeat=2):
  sol=[]
  for cc in product(range(3),repeat=6):
   col=dict(zip(['O','u','v','x','z','unused'],cc));col.update(T=0,F=1,N=2,P=p,Q=q)
   if all(col[a]!=col[b] for a,b in edges):sol.append(col['O'])
  exp=0 if ((p==0 or q==0) if kind=='OR' else (p==0 and q==0)) else 1
  assert sol and set(sol)=={exp};table.append({'P':p,'Q':q,'output':exp,'extensions':len(sol)//3})
 out['gadget_'+kind]=table
# All 64 G(4,1/2) edge sets, two-step events.
edges=list(combinations(range(4),2));cnt=Counter()
for bits in product((0,1),repeat=6):
 E={e for e,b in zip(edges,bits) if b}
 adj=lambda a,b:norm((a,b)) in E if a!=b else False
 W=lambda a,b:any(adj(a,k) and adj(k,b) for k in range(4))
 cnt['wx']+=W(0,1);cnt['xy']+=W(1,2);cnt['yz']+=W(2,3)
 cnt['wx_and_xy']+=W(0,1) and W(1,2);cnt['wx_and_yz']+=W(0,1) and W(2,3)
assert cnt['wx']==cnt['xy']==cnt['yz']==28 and cnt['wx_and_xy']==17 and cnt['wx_and_yz']==20
out['two_step_random_graph_counts_out_of64']=dict(cnt)
# Uniform 3-colouring of every edge of K4, exact mean/variance.
tri=list(combinations(range(4),3));sumM=sumM2=0
for colors in product(range(3),repeat=6):
 C=dict(zip(edges,colors));M=sum(len({C[norm((a,b))],C[norm((a,c))],C[norm((b,c))]})==1 for a,b,c in tri)
 sumM+=M;sumM2+=M*M
mu=Fraction(sumM,3**6);var=Fraction(sumM2,3**6)-mu**2
assert mu==Fraction(4,9) and var==Fraction(32,81)
out['K4_729_edge_colorings']={'mean':str(mu),'variance':str(var)}
# DAG closure and exhaustive antichains.
def dag(vertices,edges):
 R={v:set() for v in vertices}
 for a,b in edges:R[a].add(b)
 for k in vertices:
  for i in vertices:
   if k in R[i]:R[i]|=R[k]
 anti=[]
 for mask in range(1<<len(vertices)):
  A=[v for j,v in enumerate(vertices) if mask>>j&1]
  if all(b not in R[a] and a not in R[b] for a,b in combinations(A,2)):anti.append(A)
 width=max(map(len,anti));return R,[A for A in anti if len(A)==width]
V=['18.01','18.02','18.03','8.01','8.02','6.042','6.01','6.046','6.02','6.006','6.034','6.004']
E=[('18.01',b) for b in ['6.042','18.02','18.03']]+[('8.01',b) for b in ['8.02','6.01']]+[('6.042',b) for b in ['6.046','6.006']]+[(a,'6.02') for a in ['18.02','18.03','8.02','6.01']]+[('6.01',b) for b in ['6.006','6.034']]+[('6.02','6.004')]
R,A=dag(V,E);assert len(A[0])==6;witness=['18.02','18.03','8.02','6.046','6.006','6.034'];assert witness in A
out['online_schedule_4096_subsets']={'width':6,'max_antichains':len(A),'witness':witness}
V=['18.01','18.02','18.03','8.01','8.02','6.001','6.042','6.046','6.840','6.034','6.002','6.003','6.004','6.033','6.857']
E=[('18.01',b) for b in ['6.042','18.02','18.03']]+[('8.01','8.02')]+[('6.001',b) for b in ['6.034','6.003','6.004']]+[('6.042','6.046'),('6.046','6.840')]+[(a,'6.002') for a in ['18.03','8.02']]+[('6.002',b) for b in ['6.003','6.004']]+[('6.004','6.033'),('6.033','6.857')]
R,A=dag(V,E);no1803=[a for a in A if '18.03' not in a];assert len(A[0])==5 and len(no1803)==9
out['CP17_32768_subsets']={'width':5,'max_antichains_without1803':9,'witnesses':no1803}
# Stable matching exhaustive 4!=24 permutations for every completion of the partial PS8 table.
def stable(M,men,women):
 inv={g:b for b,g in enumerate(M)}
 return all(not(men[b].index(g)<men[b].index(M[b]) and women[g].index(b)<women[g].index(inv[g])) for b in range(len(M)) for g in range(len(M)))
count=0
for flags in product((0,1),repeat=8):
 men=[];women=[]
 for i in range(4):
  tail=[2,3] if i<2 else [0,1];tail=tail if flags[i]==0 else tail[::-1]
  men.append(([0,1] if i==0 else [1,0] if i==1 else [])+tail+([3,2] if i==2 else [2,3] if i==3 else []))
 for i in range(4):
  tail=[2,3] if i<2 else [0,1];tail=tail if flags[i+4]==0 else tail[::-1]
  women.append(([1,0] if i==0 else [0,1] if i==1 else [])+tail+([2,3] if i==2 else [3,2] if i==3 else []))
 ss=[M for M in permutations(range(4)) if stable(M,men,women)]
 assert (0,1,2,3) in ss and (1,0,2,3) in ss and (0,1,3,2) in ss
 count+=1
out['PS8_all_256_preference_completions_original_and_both_extremes_stable']=count
men=[[0,1,2,3],[2,1,3,0],[0,3,2,1],[3,2,1,0]]
# Company names HP=0 Bellcore=1 AT&T=2 Draper=3.
women=[[3,2,0,1],[2,1,0,3],[3,0,2,1],[1,3,2,0]]
ss=[M for M in permutations(range(4)) if stable(M,men,women)]
assert (1,2,0,3) in ss and (2,1,0,3) in ss
out['CP22_stable_assignments_of24']={'count':len(ss),'assignments':ss}
# Cubical paths explicitly printed in final CP20, checked separately by parsing evidence below.
# Exact Markov calculations at steps t=0..12.
P2=[[Fraction(0),Fraction(1)],[Fraction(9,10),Fraction(1,10)]];pi=[Fraction(9,19),Fraction(10,19)]
assert [sum(pi[i]*P2[i][j] for i in range(2)) for j in range(2)]==pi
q=[Fraction(1),Fraction(0)]
for t in range(13):
 assert q[0]==Fraction(9,19)+Fraction(10,19)*Fraction(-9,10)**t
 q=[sum(q[i]*P2[i][j] for i in range(2)) for j in range(2)]
P3=[[Fraction(1),0,0,0],[Fraction(1,2),0,Fraction(1,2),0],[0,Fraction(1,2),0,Fraction(1,2)],[0,0,0,Fraction(1)]]
h=[0,Fraction(1,3),Fraction(2,3),1];assert [sum(P3[i][j]*h[j] for j in range(4)) for i in range(4)]==h
q=[0,Fraction(1),0,0]
for t in range(13):
 assert q[1]+q[2]==Fraction(1,2)**t
 q=[sum(q[i]*P3[i][j] for i in range(4)) for j in range(4)]
out['Markov_exact_13_times']={'pi2':list(map(str,pi)),'b_to_d_absorption':str(h[1]),'survival':'2^-t'}
print(json.dumps(out,ensure_ascii=False,indent=2))
# Independent checks of final reconstructed concrete objects.
paths=[['000','100'],['000','010','110','100'],['000','001','101','100'],['000','100','110'],['000','010','110'],['000','001','011','111','110'],['000','100','110','111'],['000','010','011','111'],['000','001','101','111']]
for p in paths:
 assert len(p)==len(set(p));assert all(sum(a!=b for a,b in zip(x,y))==1 for x,y in zip(p,p[1:]))
for i in range(0,9,3):
 assert len({p[-1] for p in paths[i:i+3]})==1
 assert all(not(set(p[1:-1])&set(q[1:-1])) for p,q in combinations(paths[i:i+3],2))
# Sequence lists exhaustively regenerated from all 2^9 subsequences.
S=[6,4,7,9,1,2,5,3,8]
ss=[[S[j] for j in range(9) if m>>j&1] for m in range(512)]
inc=[a for a in ss if all(x<y for x,y in zip(a,a[1:]))];dec=[a for a in ss if all(x>y for x,y in zip(a,a[1:]))]
assert [a for a in inc if len(a)==max(map(len,inc))]==[[1,2,5,8],[1,2,3,8]]
assert {tuple(a) for a in dec if len(a)==max(map(len,dec))}=={(6,4,1),(6,4,2),(6,4,3),(6,5,3),(7,5,3),(9,5,3)}
# PS7 graph edge sets and supplied bijection.
G1={norm(e) for e in [(1,2),(2,3),(3,4),(4,5),(5,1),(1,6),(2,9),(3,7),(4,10),(5,8),(6,7),(7,8),(8,9),(9,10),(10,6)]}
G2={norm(e) for e in [(1,2),(2,3),(3,4),(4,5),(5,1),(1,6),(2,7),(3,8),(4,10),(5,9),(6,7),(7,8),(8,10),(10,9),(9,6)]}
G3={norm(e) for e in [(1,2),(2,3),(3,4),(4,5),(5,1),(1,6),(2,7),(3,8),(4,10),(5,9),(6,10),(6,8),(9,7),(9,10),(7,8),(10,8)]}
G4={norm(e) for e in [(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,1),(1,10),(4,10),(7,10),(9,5),(2,6),(8,3)]}
f=dict(zip(range(1,11),[1,2,3,4,10,9,8,7,6,5]));assert {norm((f[a],f[b])) for a,b in G1}==G4
has4=lambda G:any(all(norm(e) in G for e in [(a,b),(b,c),(c,d),(d,a)]) for a,b,c,d in permutations(range(1,11),4))
assert not has4(G1) and has4(G2) and not has4(G4);assert len(G3)==16 and Counter(a for e in G3 for a in e)[8]==4 and Counter(a for e in G3 for a in e)[10]==4
# CP19 all 6! maps, count four.
left={norm(e) for e in [(1,3),(1,4),(2,3),(2,4),(3,5),(5,6),(6,4)]};right={norm(e) for e in [('a','c'),('a','d'),('b','c'),('b','d'),('c','e'),('e','f'),('f','d')]}
iso=[]
for a in permutations('abcdef'):
 f=dict(zip(range(1,7),a))
 if {norm((f[u],f[v])) for u,v in left}==right:iso.append(a)
assert len(iso)==4
# Mycielski triangle-free and no 3-colouring, with w's colour fixed at 2.
E={norm((i,(i+1)%5)) for i in range(5)}|{norm((i+5,(i+d)%5)) for i in range(5) for d in [-1,1]}|{(i+5,10) for i in range(5)}
assert not any(all(norm(e) in E for e in combinations(A,2)) for A in combinations(range(11),3))
for v in product(range(3),repeat=5):
 for u in product(range(2),repeat=5):
  c=v+u+(2,);assert not all(c[a]!=c[b] for a,b in E)
c=(0,1,0,1,2,0,1,0,1,2,3);assert all(c[a]!=c[b] for a,b in E)
# Register graph valid four-colouring and K4 lower witness.
E={norm(e) for e in ['ab','ac','ad','cd','ae','ce','de','af','df','dg','fg','dh','gh']};C={x:i for i,s in enumerate(['ag','bcfh','d','e']) for x in s}
assert all(C[a]!=C[b] for a,b in E);assert all(norm(e) in E for e in combinations('acde',2))
print(json.dumps({'final_9_cube_paths':True,'CP18_all512_subsequences':True,'PS7_supplied_map_and_all4cycles':True,'CP19_all720_vertex_maps_isomorphisms':len(iso),'Mycielski_7776_colours_excluded_and_4colour_witness':True,'register_4colour_K4_witness':True},indent=2))
```

## 冻结来源快照

反馈索引 `sources/graph-theory/assessments/6042/online-feedback-index.json`：`d5317eab12538a341f510cfbc2bdf962fddb4105ebf754a13a92a8caa905316c`。索引中 scope=graph-theory 的36 HTML及其16个图像依赖路径均重算一致。

| 官方来源 PDF | 入选原题号 | 本地 PDF SHA-256 |
|---|---|---|
| `MIT6_042JS15_cp10.pdf` | 4 | `a3c4980db0405d42f516af75c36c211faa821022d2bc60a4a08741b24062a11e` |
| `MIT6_042JS15_cp16.pdf` | 1, 2, 3, 4 | `bc25610de63a8f6bab48b9345792f456b0cc6026e121ce84cd82196e5258218a` |
| `MIT6_042JS15_cp17.pdf` | 1, 2, 3, 4 | `cfb35659156304bf3d186dbd1ecba80e3a32ff162d391ab09aad665461f1279c` |
| `MIT6_042JS15_cp18.pdf` | 3 | `a515cb9cf4a98d08e44b54bc44bd9ec53616fd7f292dc1012d06a99a78a8485b` |
| `MIT6_042JS15_cp19.pdf` | 1, 2, 3, 4, 5 | `78968e0f7a7cc8794d5f8ca14943041f4cd91df931008cd89f47676f4337cd85` |
| `MIT6_042JS15_cp20.pdf` | 1, 2, 3, 4 | `5a6eacfaf1ce9fc6ed6c251fe783be58a2bd70b880e0e91959d4565b6dc3c8dc` |
| `MIT6_042JS15_cp21.pdf` | 1, 2, 3, 4 | `387a6b77c0b00fdb4c043529f6facde5f2e7930be963484e0701b96e84a97e9e` |
| `MIT6_042JS15_cp22.pdf` | 1, 2, 3, 4 | `bc993c7230aafb90e91674bf4e1d3b479e22e937f03837766f92d18535855e3c` |
| `MIT6_042JS15_cp25.pdf` | 2 | `46825a62f7052da76aa1e3fc232d00e7e30fc24af2b0c52475c5b50b50957012` |
| `MIT6_042JS15_cp30.pdf` | 3 | `a9c63b5d6139a87dc78dfe65721995639df9fc940483839f53b5371c84ec2621` |
| `MIT6_042JS15_cp32.pdf` | 1, 2, 3, 4, 5 | `d52ea17d754978687cb0da4e841b97227b046b65eabc62426b3eb72edb809ff8` |
| `MIT6_042JS15_cp33.pdf` | 4 | `3651ae59179fb8c3309325b60d093242ed8beebf1f3600887a8283df93581d24` |
| `MIT6_042JS15_cp35.pdf` | 1, 2, 3 | `1d03abf86a07682ba4e98ba2331813261fe8e3ad35057a1c588b0aa53cd8279a` |
| `MIT6_042JS15_finalexam.pdf` | 2, 4, 5, 9, 12 | `a0b0ebb14be62481fd49884d7356ae9973179723263304dd60561dac3f4771b2` |
| `MIT6_042JS15_midterm3.pdf` | 1, 3, 4, 5 | `1cc46956aa6a2eb840b223cb6d7267314bfe11e03eff2c1360268a51cc6722a7` |
| `MIT6_042JS15_ps4.pdf` | 2 | `54dee69b84c0aae9ace647734d871fdf38e613bd1d79fac2d62f854fa77adbf7` |
| `MIT6_042JS15_ps6.pdf` | 2, 3 | `ea4d03b7b9565ffff138fab84f6d792a04bba0de257690071d2d8e32a8932748` |
| `MIT6_042JS15_ps7.pdf` | 3, 4 | `d13092fdd041c61bfc24e023d0792cee1ad8f75a8b7f4dc36bea9ebac0d872a4` |
| `MIT6_042JS15_ps8.pdf` | 1, 2, 3 | `9e582132b94a97b03935c748a1ee427eba82d225feff71ce1dcc4cfe697c9f93` |

只读核对的正文依赖：

| 文件 | SHA-256 | 已读证明范围 |
|---|---|---|
| `chapters/ch01.tex` | `dc34464bf90b64d561100ddc64cc83e4134789e2ffcd04a37fc18e5af16e1e95` | 图/有向图约定及路圈定义 |
| `chapters/ch02.tex` | `65f0a73dfb6f8b51ffdbb289ac2ea4551a9bb0a2cb9f96174756736f86cf38cd` | 两叶引理、树的等价刻画与所依边数/删圈证明 |
| `chapters/ch03.tex` | `ce919eb9210202863c76a4705cf39aa048424f7b693ff046ab23827a8254d551` | kappa≤lambda、不相邻Menger及紧接相邻端点/全局推论 |
| `chapters/ch04.tex` | `9126efd0bff12d58e8f70ff67e69c6ab16eed6e49c47f69f84569a213a80dc39` | 有向Euler判据及拼接证明 |
| `chapters/ch11.tex` | `138d9efd770cddd21ac9dfc12af17bdeb9f49672efb8c8d47a6931848d21a0a1` | 安全边定理、交换证明、Kruskal/Prim不变量 |


## 结论边界

上述指定八个最终子文件的题面覆盖、条件、一般证明、反例、具体计算与来源图表数学对象通过本次独立审读；已提出的按日DA计数、CP17连续时刻缺口都在所绑定版本闭合。CP22不可接受对象的直接算法筛选措辞建议保留为非阻断边界说明，核心完整可接受模型与克隆转换已核实。此次没有改正文、其他课程、全局清单、Git状态、远端或公开权限。

下一步仍由父代理对最终合册做实际逐页视觉、目录/题号交叉引用点击、干净ZIP重编及发布完整性核验。正文引用的ch02/ch03/ch04/ch11证明只读了所需对应论证段落，本次不是对整章再作全面审定；这些依赖字节也列入快照便于合册追踪。
