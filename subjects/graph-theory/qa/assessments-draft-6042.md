# 6.042J Spring 2015 新增题稿：作者核对记录

记录时间（UTC）：2026-10-08T09:29:54.771402+00:00。

这是独立代理编写完成后的**作者自检**，不是人类专家审核，也不是另一模型的独立交叉审稿。全部数学题面与解答已写出；父代理及另一独立代理的数学复审、全册编译、实际逐页视觉、目录链接与最终ZIP重编仍须另行记录。本文件不对那些尚未完成的验收作通过声明。

## 写入范围

仅写 `subjects/graph-theory/assessments/6042/` 中八个 LaTeX 子文件、必要只读复核脚本 `review-checks.py` 和本 QA 文件。没有修改主书 main.tex、原十七章、旧数学或视觉 QA、PDF、ZIP、其他课程题集、根 README、全局清单或远端。metadata.tex 按父代理要求删除，书前元数据使用父代理已写并独核的 supplementary-courses.tex。

课程题以既有原生 `exercise` / `solution` 环境呈现；现有类没有名为 nativeexercise 的环境。总节用 originalsection，内部标题使用7pt间距未编号粗体段落，没有默认 subsection 编号。中文 emph 已全部改为 textbf。全部新图均用等价边集、邻接关系或转移矩阵确定数学对象，没有嵌入英文页、截图或第三方图像。

## 冻结覆盖与来源

- PDF：50 个主问题，147 个原顶层回答单元，保留 (a) 等字母；CP17:4(f) 另保留 (i)–(iii)。
- 在线：36页、75个原Q回答单元，逐Q标签全部存在；公开反馈仅作为答案标记和实际公开解释依据，缺省证明由编者补写。
- CP32:1–5 与CP19正文重复，五个CP32标签映到对应CP19同一习题；不重复抄写。
- 明确不选CP9:4、CP27:3、PS11:1及原清单已排除的逻辑、一般关系、一般计数、一般概率题。
- 三种原PDF分类索引明确未公开solutions，两个官方Download Course ZIP均无这些评测答案文件；本稿所有PDF解答均标编者独立解答。在线HTML有公开答案标记，与PDF未公开解答分开。
- PDF作者Eric Lehman、F. Tom Leighton、Albert R. Meyer，2015，CC BY-NC-SA 3.0；在线课程HTML按CC BY-NC-SA 4.0。已逐个重校冻结来源PDF、36 HTML及图像的SHA，不扩展许可或伪作官方答案。

| 冻结证据 | SHA-256 |
|---|---|
| assessments-inventory-6042.json | `9ec9654057ce99df80711605db6b31014a83085d1fa1123b2e4f753bf9dfa6c8` |
| online-feedback-index.json | `d5317eab12538a341f510cfbc2bdf962fddb4105ebf754a13a92a8caa905316c` |

## 源错误与显式修订

1. PS7:4的line graph按该题自身定义译作路径图，避免与通常线图混淆。
2. PS8:1及CP21:3补明连通以保证生成树存在。不同权是MST唯一的充分条件，不是必要条件；在线Multiple Choice:Q1原解释已纠正。
3. PS8:3(c)原提示隐含偶数n；偶数双人组构造完整，奇数n≥3另给三人循环组，n=1原数目断言不成立。
4. CP16:2补明有限可达距离；∞=∞不能等价于位于最短路径。CP16:3(d)同点“positive path”改按正闭合游走解释。
5. 在线Adjacency Matrix:Q1中A²数两步游走，不是无重复顶点路径；官方措辞明确纠正。
6. 在线Extreme Graphs:Q1总度44为22边，K7加一顶点及一条边才正确；原解释添两条边会得到总度46。
7. 在线Graph Algorithm:Q1固定V上的初始无标边子图是森林而非空真树，官方解释纠正。
8. 在线Scheduling Prerequisites:Q4给出的12门先修表实际最大反链6，官方隐藏答案5错误；给六元反链及六链分解双证，并穷举传递闭包全部反链核对。该表与CP17历史示例不同，后者宽度5。
9. 在线DAGs:Q1原教材定义9.0.1（书印刷319页）要求非空顶点集；本册允许空图。两套约定分别说明，未称其中一套为计算错误。
10. 在线Derived Variables把rank解释为越好越大的质量；采用“名次1最好”时数字单调方向相反。
11. 在线Bipartite equivalence relation实际求全定义单射，不是数学等价关系；标题误用注明。
12. 在线Mating Ritual:Q1的unique只可解释为固定申请侧最终输出确定，不能解释为所有稳定匹配唯一；以CP22的双输出反例和最优性证明说明。
13. 在线Chromatic Number:Q2总点数n偶数时外圈n−1奇数，色数4；若n是外圈点数才为3。原总点数措辞与官方答案3的冲突保留。
14. 在线Graph Coloring II区分有边森林χ=2、非空无边χ=1、空图χ=0；树唯一两点路径等价式补非空条件。
15. CP33:4(f)含sqrt(mu log mu)、1/log mu的界需mu>1，即均匀三色时n≥5；小n条件明确。
16. CP35:3补明正出度及e>0；关于网页排名只讨论原对称玩具模型，不当作当前真实搜索规则。
17. 延迟接受共同引理现分清按日重访与逐次新申请版本。按日版无拒绝日终止，拒绝日至少永久删一对；逐次版每对至多一次新申请。在线日不变量没有错误使用逐次申请次数界。
18. 作者复核已修CP20:4(a)距离2第三条路径的一条非邻接边，当前路径为000,001,011,111,110；九条显示路径已全部逐边核对。

## 实际检查

复核命令：`python subjects/graph-theory/assessments/6042/review-checks.py`。只读脚本不改变源文件，不联网，不编译，不宣称视觉验收。当前实际运行退出码0。检查覆盖标签唯一、原题147回答单元计数、75Q逐ID映射、86exercise/solution配对、5重复映射、当前冻结PDF/HTML/图像SHA；这些属于机械覆盖检查，不声称它们自动审完数学。

数学对象有限核对：

- `ps7_isomorphism`：{"G1_G4":"explicit mapping verified","G1_four_cycles":0}
- `ps8_source_graph`：{"actual_vector_edges":20,"source_relettering":"equal","triangles":0,"four_coloring":"verified","three_coloring":"impossible by exhaustive search"}
- `ps8_stability`：{"partial_completions":256,"displayed_matchings_each":3,"odd_three_person_gadget":3}
- `logic_gadget`："all eight OR/AND input cases exhaustively verified"
- `cube_path_families`："all nine displayed paths adjacent and internally disjoint"
- `cp21_grid_mst`：{"prim_sequence":["h02","h12","h22","v01","h01","h11","h21","v00","h00","h10","h20","v02","h03","h13","h23"],"kruskal_same_edges":true,"exact_weight":"369/100"}
- `register_allocation`：{"live_set_edges":13,"displayed_four_register_partition":"proper","lower_bound_clique":"acde"}
- `cp18_subsequences`：{"all_longest_increasing":2,"all_longest_decreasing":6}
- `mt3_dag`：{"maximum_antichains":[["A","B","C"],["B","C","D"]],"two_person_schedule":4}
- `cp17_schedule`：{"five_antichains_without_1803":9,"two_per_term":8,"three_per_term":6}
- `online_schedule_corrigendum`：{"official_Q4":5,"actual_width":6,"six_antichain":["18.02","18.03","8.02","6.046","6.006","6.034"]}
- `cp30_random_graph_enumeration`：{"graphs":64,"event_counts":[28,28,28,17,20]}
- `walk_stationary_equations`："exact rational equations verified"

共同引理及其使用者按严格完整偏好说明；首次拒绝稳定可行配对的反证、双方最优/最差及唯一性夹逼写出。H_n连通度通过删点归纳完整证明，另给H_3三种距离的显式不交路径。MST唯一、灰边法、Prüfer最大叶规则、偏序与递增/递减子序列、随机游走平稳方程和吸收概率都写出推导，而非只列结论。正文已完整证明的Euler、Menger、树刻画、割安全性等仅作精确引用，剩余计算仍给实际结果。

新增稿所有ref/pageref/eqref均在当前全书TeX标签集合中找到；此为静态存在性，不代替PDF可点击链接验收。所有display数学分隔符计数相等，仍由父代理完成完整编译检查。作者源图视觉使用：PS7:2、PS8:1、CP17:4、CP19:2、MT3:2、CP20:3实际打开；在线全部15种不同图像实际打开（16个HTML依赖路径中随机游走两文件像素相同）；PS8另直接解析PDF矢量点/线并与中文重标号边集逐边相等。之前库存17张源页核查见旧inventory。这里没有宣称193页来源PDF逐页验收，更没有宣称新增主PDF逐页验收。

## 独立审稿后的本次返修

2026-10-08T09:33:53.836159+00:00：matrix_electric_audit 指出 CP17:2(d) 需排除连续实数工期39.5等情形。仅在cp-a.tex补入完整整数规范化：固定每人的任务次序，加入正工时先后弧；可行时刻排除有向圈；拓扑序最早开始递推给整数时刻且不晚于原方案。因而任意<40方案能化为≤39，再与已证明39不可行矛盾。已重新运行只读复核脚本，退出码0，并逐个核对其余七个TeX的原QA哈希未变。本次没有修改其他已冻结TeX；数学完整返修正交给原独立审稿代理复核。

## 最终子文件字节绑定

| 文件 | SHA-256 |
|---|---|
| `cp-a.tex` | `a6790e7b2f4e6d4f090edf29bbec6b8eb862c4e28fe2e409ba3a0319d3b3b77e` |
| `cp-b.tex` | `b9ca1c409d5fe5ad066be5142408f7e613fcc10a20195a39a1ea666a6efa026a` |
| `cp-c.tex` | `23086af3c917d7b3dbf9bc60187d7f0d2be344f201c952b79f668a622ed215b2` |
| `exams.tex` | `f95329518e719f1d57440689c387badeb362fa58fbdfc72bf5017f388c2c4651` |
| `lemmas.tex` | `4e79f6499dce917893b6ae065ff27ccdfdcadfa5de0bd18098f8475f1f241870` |
| `main.tex` | `8e825fab1f89df0637cb192c2087f43c99df09b282d227639042df13a082a198` |
| `online.tex` | `23d65e945c9ac95f5141bf312015a4f6c0b5e70be12bdf577420e57d374c6705` |
| `ps.tex` | `f56962553ce7e5cb5a30e641e1ce346ea75b2583fd34d99230605244f8a6bb27` |
| review-checks.py | `7a40894b940f1f3c6d9383851ab1e92a272accf508f280d026991ff351be5f6d` |

## PDF逐原ID映射

| 原件 | 题号 | 原起始物理页 | 原字母 | 原回答单元 | 本稿标签 |
|---|---:|---:|---|---:|---|
| `MIT6_042JS15_cp10.pdf` | 4 | 3 | a,b,c | 3 | `mit:6042-cp10-q4` |
| `MIT6_042JS15_cp16.pdf` | 1 | 1 | a,b,c | 3 | `mit:6042-cp16-q1` |
| `MIT6_042JS15_cp16.pdf` | 2 | 1 | a,b | 2 | `mit:6042-cp16-q2` |
| `MIT6_042JS15_cp16.pdf` | 3 | 1 | a,b,c,d | 4 | `mit:6042-cp16-q3` |
| `MIT6_042JS15_cp16.pdf` | 4 | 2 | a,b | 2 | `mit:6042-cp16-q4` |
| `MIT6_042JS15_cp17.pdf` | 1 | 1 | a,b,c,d,e | 5 | `mit:6042-cp17-q1` |
| `MIT6_042JS15_cp17.pdf` | 2 | 1 | a,b,c,d | 4 | `mit:6042-cp17-q2` |
| `MIT6_042JS15_cp17.pdf` | 3 | 3 | a,b,c | 3 | `mit:6042-cp17-q3` |
| `MIT6_042JS15_cp17.pdf` | 4 | 3 | a,b,c,d,e,f | 6 | `mit:6042-cp17-q4` |
| `MIT6_042JS15_cp18.pdf` | 3 | 1 | a,b,c,d | 4 | `mit:6042-cp18-q3` |
| `MIT6_042JS15_cp19.pdf` | 1 | 1 | a,b,c,d | 4 | `mit:6042-cp19-q1` |
| `MIT6_042JS15_cp19.pdf` | 2 | 1 | a,b,c | 3 | `mit:6042-cp19-q2` |
| `MIT6_042JS15_cp19.pdf` | 3 | 1 | 无字母 | 1 | `mit:6042-cp19-q3` |
| `MIT6_042JS15_cp19.pdf` | 4 | 1 | a,b,c,d,e,f,g,h,i,j | 10 | `mit:6042-cp19-q4` |
| `MIT6_042JS15_cp19.pdf` | 5 | 2 | a,b | 2 | `mit:6042-cp19-q5` |
| `MIT6_042JS15_cp20.pdf` | 1 | 1 | a,b,c | 3 | `mit:6042-cp20-q1` |
| `MIT6_042JS15_cp20.pdf` | 2 | 2 | a,b | 2 | `mit:6042-cp20-q2` |
| `MIT6_042JS15_cp20.pdf` | 3 | 2 | a,b,c | 3 | `mit:6042-cp20-q3` |
| `MIT6_042JS15_cp20.pdf` | 4 | 3 | a,b,c | 3 | `mit:6042-cp20-q4` |
| `MIT6_042JS15_cp21.pdf` | 1 | 1 | a,b,c,d | 4 | `mit:6042-cp21-q1` |
| `MIT6_042JS15_cp21.pdf` | 2 | 1 | 无字母 | 1 | `mit:6042-cp21-q2` |
| `MIT6_042JS15_cp21.pdf` | 3 | 1 | 无字母 | 1 | `mit:6042-cp21-q3` |
| `MIT6_042JS15_cp21.pdf` | 4 | 2 | a,b | 2 | `mit:6042-cp21-q4` |
| `MIT6_042JS15_cp22.pdf` | 1 | 1 | a,b | 2 | `mit:6042-cp22-q1` |
| `MIT6_042JS15_cp22.pdf` | 2 | 1 | a,b,c,d,e | 5 | `mit:6042-cp22-q2` |
| `MIT6_042JS15_cp22.pdf` | 3 | 1 | 无字母 | 1 | `mit:6042-cp22-q3` |
| `MIT6_042JS15_cp22.pdf` | 4 | 2 | 无字母 | 1 | `mit:6042-cp22-q4` |
| `MIT6_042JS15_cp25.pdf` | 2 | 1 | a,b | 2 | `mit:6042-cp25-q2` |
| `MIT6_042JS15_cp30.pdf` | 3 | 2 | a,b,c,d | 4 | `mit:6042-cp30-q3` |
| `MIT6_042JS15_cp33.pdf` | 4 | 2 | a,b,c,d,e,f,g | 7 | `mit:6042-cp33-q4` |
| `MIT6_042JS15_cp35.pdf` | 1 | 1 | a,b,c,d,e,f,g | 7 | `mit:6042-cp35-q1` |
| `MIT6_042JS15_cp35.pdf` | 2 | 2 | 无字母 | 1 | `mit:6042-cp35-q2` |
| `MIT6_042JS15_cp35.pdf` | 3 | 2 | a,b | 2 | `mit:6042-cp35-q3` |
| `MIT6_042JS15_finalexam.pdf` | 2 | 3 | 无字母 | 1 | `mit:6042-final-q2` |
| `MIT6_042JS15_finalexam.pdf` | 4 | 5 | a,b | 2 | `mit:6042-final-q4` |
| `MIT6_042JS15_finalexam.pdf` | 5 | 6 | a,b,c,d | 4 | `mit:6042-final-q5` |
| `MIT6_042JS15_finalexam.pdf` | 9 | 10 | a,b | 2 | `mit:6042-final-q9` |
| `MIT6_042JS15_finalexam.pdf` | 12 | 13 | a,b,c | 3 | `mit:6042-final-q12` |
| `MIT6_042JS15_midterm3.pdf` | 1 | 2 | a,b,c | 3 | `mit:6042-mt3-q1` |
| `MIT6_042JS15_midterm3.pdf` | 3 | 4 | a,b | 2 | `mit:6042-mt3-q3` |
| `MIT6_042JS15_midterm3.pdf` | 4 | 5 | 无字母 | 1 | `mit:6042-mt3-q4` |
| `MIT6_042JS15_midterm3.pdf` | 5 | 6 | a,b,c,d,e,f,g | 7 | `mit:6042-mt3-q5` |
| `MIT6_042JS15_ps4.pdf` | 2 | 1 | 无字母 | 1 | `mit:6042-ps4-q2` |
| `MIT6_042JS15_ps6.pdf` | 2 | 1 | a,b | 2 | `mit:6042-ps6-q2` |
| `MIT6_042JS15_ps6.pdf` | 3 | 1 | a,b,c | 3 | `mit:6042-ps6-q3` |
| `MIT6_042JS15_ps7.pdf` | 3 | 1 | 无字母 | 1 | `mit:6042-ps7-q3` |
| `MIT6_042JS15_ps7.pdf` | 4 | 1 | a,b | 2 | `mit:6042-ps7-q4` |
| `MIT6_042JS15_ps8.pdf` | 1 | 1 | 无字母 | 1 | `mit:6042-ps8-q1` |
| `MIT6_042JS15_ps8.pdf` | 2 | 1 | a,b | 2 | `mit:6042-ps8-q2` |
| `MIT6_042JS15_ps8.pdf` | 3 | 1 | a,b,c | 3 | `mit:6042-ps8-q3` |

重复映射：`mit:6042-cp32-q1` → `mit:6042-cp19-q1`；`mit:6042-cp32-q2` → `mit:6042-cp19-q2`；`mit:6042-cp32-q3` → `mit:6042-cp19-q3`；`mit:6042-cp32-q4` → `mit:6042-cp19-q4`；`mit:6042-cp32-q5` → `mit:6042-cp19-q5`。

## 在线75Q逐ID映射及HTML绑定

HTML没有PDF物理页码；题目按页面标题和原Q编号定位。下列完整相对路径以 `sources/graph-theory/assessments/6042/online/` 为根；历史官方URL及每Q原控制器见已冻结online-feedback-index.json。

| 官方页面标题 | 原Q → 本稿标签 | HTML相对路径 | SHA-256 |
|---|---|---|---|
| Walks and Paths | Q1 → `mit:6042-online-walks-and-paths-q1`<br>Q2 → `mit:6042-online-walks-and-paths-q2` | `structures/tp6-3/vertical-5a67aa9a3a6d/index.htm` | `fafc5eff5ce1c3739b211a4790a64beb2281cf08a98282d0eb6326fa40c9dfd2` |
| Counting Paths | Q1 → `mit:6042-online-counting-paths-q1`<br>Q2 → `mit:6042-online-counting-paths-q2`<br>Q3 → `mit:6042-online-counting-paths-q3` | `structures/tp6-3/counting-paths/index.htm` | `15569e8839c168f2f55f1ac55fcd124be6c4326304a024249243ebacc17ad140` |
| Adjacency Matrix | Q1 → `mit:6042-online-adjacency-matrix-q1` | `structures/tp6-3/adjacency-matrix/index.htm` | `467027f0266e646faa9efd298f129ee2def7e35d611042f207a55981462c9146` |
| Longest Path | Q1 → `mit:6042-online-longest-path-q1`<br>Q2 → `mit:6042-online-longest-path-q2` | `structures/tp6-3/vertical-588ea67bd5d7/index.htm` | `213919ae8b738569ea0f642fab0a797e4e918c1280add6327e373fdd6841aea1` |
| Span all the Graphs! | Q1 → `mit:6042-online-span-all-the-graphs-q1`<br>Q2 → `mit:6042-online-span-all-the-graphs-q2`<br>Q3 → `mit:6042-online-span-all-the-graphs-q3`<br>Q4 → `mit:6042-online-span-all-the-graphs-q4` | `structures/tp8-1/vertical-63394d192790/index.htm` | `fa92776e5d6446d90678cdf6842ad9b61cf8866846c049eeeccf85be54201315` |
| Leaves | Q1 → `mit:6042-online-leaves-q1`<br>Q2 → `mit:6042-online-leaves-q2`<br>Q3 → `mit:6042-online-leaves-q3`<br>Q4 → `mit:6042-online-leaves-q4` | `structures/tp8-1/vertical-425ace1eec7d/index.htm` | `be2683bf12337ed0beaa9a5ce34b94cae0914c5171458a3403d6593977f39c40` |
| 2-Colorable Trees | Q1 → `mit:6042-online-2-colorable-trees-q1` | `structures/tp8-1/vertical-b69812803f1e/index.htm` | `0f73efe5cdc07801446a10f748c28c0b6210d078c959146dccbd0c60317e5c6a` |
| Graph Algorithm | Q1 → `mit:6042-online-graph-algorithm-q1`<br>Q2 → `mit:6042-online-graph-algorithm-q2`<br>Q3 → `mit:6042-online-graph-algorithm-q3`<br>Q4 → `mit:6042-online-graph-algorithm-q4`<br>Q5 → `mit:6042-online-graph-algorithm-q5`<br>Q6 → `mit:6042-online-graph-algorithm-q6` | `structures/tp8-1/vertical-f8c5c236b9c0/index.htm` | `faa1f2cf2106d560891b8c06b853086fb46c0c0743cfa101d64ef7a07e41e3d4` |
| Tree or Not Tree? | Q1 → `mit:6042-online-tree-or-not-tree-q1` | `structures/tp8-1/vertical-7bacea60d91e/index.htm` | `64d833c1aeab201fda832fdb71ba6603f6ac9dceeb632d37c8a2f8264b52bff2` |
| Multiple Choice | Q1 → `mit:6042-online-multiple-choice-q1`<br>Q2 → `mit:6042-online-multiple-choice-q2` | `structures/tp8-1/minimum-spanning-trees/index.htm` | `61d81c0afda96e4cb0b7e3bfdc22d7824f8b71af361456fae890d63c5b35e5f9` |
| Trees: Many Definitions | Q1 → `mit:6042-online-trees-many-definitions-q1` | `structures/tp8-1/vertical-91c45efd7596/index.htm` | `1d8fe8b3f4fd58bdf2146b7d853ca479f2639ba83d51a835ea78ba47e6ab93a9` |
| Counting Degrees & Edges | Q1 → `mit:6042-online-counting-degrees-and-edges-q1`<br>Q2 → `mit:6042-online-counting-degrees-and-edges-q2` | `structures/tp7-2/vertical-0403a1f6fa4c/index.htm` | `3fdba25dbf1b9c55b4cdbd893201a623bbe399c070bcb53e31a285da9b09b069` |
| Extreme Graphs | Q1 → `mit:6042-online-extreme-graphs-q1`<br>Q2 → `mit:6042-online-extreme-graphs-q2` | `structures/tp7-2/vertical-0d59158da590/index.htm` | `8747600f4347e45306062c7a81359f33fdc239245d893fd97bf57db1e0fe8386` |
| Isomorphism | Q1 → `mit:6042-online-isomorphism-q1`<br>Q2 → `mit:6042-online-isomorphism-q2` | `structures/tp7-2/vertical-206635abfb7b/index.htm` | `3ac3f1ec998f3211d38f18f36f945c0b8cc661457c9814b8fc5aaf1f6a0ec598` |
| Isomorphic Graphs | Q1 → `mit:6042-online-isomorphic-graphs-q1` | `structures/tp7-2/vertical-b30a643c515e/index.htm` | `7989b240a572c145bdfc72ff659c5e0f10931e1696730829a732bfad4fadef1d` |
| Non-Isomorphic Graphs | Q1 → `mit:6042-online-non-isomorphic-graphs-q1` | `structures/tp7-2/vertical-3c93d1aadcac/index.htm` | `0a68b00e4fe3366c992bcf5fddfc5373595a648f737404989f6159dc14127934` |
| Scheduling Prerequisites | Q1 → `mit:6042-online-scheduling-prerequisites-q1`<br>Q2 → `mit:6042-online-scheduling-prerequisites-q2`<br>Q3 → `mit:6042-online-scheduling-prerequisites-q3`<br>Q4 → `mit:6042-online-scheduling-prerequisites-q4`<br>Q5 → `mit:6042-online-scheduling-prerequisites-q5` | `structures/tp7-1/vertical-cb2dbc0f9d11/index.htm` | `cd3106ea21bb473806e1e6b1bae93a705f287bbc614b0f9ff08ce2f0b3d90913` |
| DAGs | Q1 → `mit:6042-online-dags-q1`<br>Q2 → `mit:6042-online-dags-q2`<br>Q3 → `mit:6042-online-dags-q3` | `structures/tp7-1/vertical-dcde59c77eab/index.htm` | `9b61a84892b9a2371638ae37fdc2dbd39880d446479a924fa17baeb63bbb2d68` |
| The Divisibility DAG | Q1 → `mit:6042-online-the-divisibility-dag-q1` | `structures/tp7-1/vertical-839e7a19a176/index.htm` | `b785da17fed6c418faff55efe808635460c392ebfb92894bd9c505c9b3108b61` |
| Processor Time Bounds | Q1 → `mit:6042-online-processor-time-bounds-q1`<br>Q2 → `mit:6042-online-processor-time-bounds-q2`<br>Q3 → `mit:6042-online-processor-time-bounds-q3`<br>Q4 → `mit:6042-online-processor-time-bounds-q4` | `structures/tp7-1/vertical-a69125071411/index.htm` | `4e584f73b6a38540153c23a0e19828117f14c47e4937256a3e07d9df99f44c8f` |
| Bipartite Graphs | Q1 → `mit:6042-online-bipartite-graphs-q1` | `structures/stable-matching/bipartite-graphs-5/index.htm` | `3043338d0f36d8110d20322a565d3fd4cf831486ff459c224057b54751180ac5` |
| Derived Variables | Q1 → `mit:6042-online-derived-variables-q1`<br>Q2 → `mit:6042-online-derived-variables-q2` | `structures/stable-matching/derived-variables-0/index.htm` | `7e4e60ab0727a52006cb3494cbc937b2eae9df7eebcfae52951db51b25dc1ae5` |
| Bipartite equivalence relation | Q1 → `mit:6042-online-bipartite-equivalence-relation-q1` | `structures/stable-matching/bipartite-equivalence-relation/index.htm` | `04c77465300ea1adca5ba6eac506f0c2a89cbea7a4d37992af3695faef4e7bbf` |
| Boy Optimal | Q1 → `mit:6042-online-boy-optimal-q1` | `structures/stable-matching/boy-optimal/index.htm` | `35829da7b719d0274c5b9a95786a691bef109f60fa908ca9d27a77b3f90478fb` |
| Bottleneck | Q1 → `mit:6042-online-bottleneck-q1` | `structures/stable-matching/bottleneck-3/index.htm` | `ff05e8e91f2ff3abce938e6ecbf184987dab3247d4028bfe8a8246077d9a6e91` |
| Mating Ritual | Q1 → `mit:6042-online-mating-ritual-q1`<br>Q2 → `mit:6042-online-mating-ritual-q2` | `structures/stable-matching/mating-ritual-0/index.htm` | `52d4b08cc154ee8651036203a2e3cc48a5e82971a89a0814d2bcfc859bed7dad` |
| Match or No Match | Q1 → `mit:6042-online-match-or-no-match-q1`<br>Q2 → `mit:6042-online-match-or-no-match-q2` | `structures/stable-matching/matching/index.htm` | `b9ffeda42e730ae011ffdd96be30a1bbc31b90219acdadc45ccb4f25998c23dd` |
| Stable Matching Invariants | Q1 → `mit:6042-online-stable-matching-invariants-q1` | `structures/stable-matching/stable-matching-invariants/index.htm` | `52cda2594518120bf2b2d6be25b768dea6ccf0be79b58c4365111b244c9dd0ce` |
| Connected Components Among the Integers | Q1 → `mit:6042-online-connected-components-among-the-integers-q1` | `structures/tp7-3/vertical-fef93eac28bc/index.htm` | `a55ec8f1dd31e1ce03f7dc54462ed83c56f32104cbe24dfcb65263c9acdda8dd` |
| Graph Coloring II | Q1 → `mit:6042-online-graph-coloring-ii-q1` | `structures/tp7-3/vertical-5c29d46d85ff/index.htm` | `554b5e1c1240a448a7713cd4f3573663fb299f12efa8a8b3fb9a1de84bb4755a` |
| Graph Coloring I | Q1 → `mit:6042-online-graph-coloring-i-q1` | `structures/tp7-3/vertical-c79a8bf5b197/index.htm` | `11b16c72a27bce3037e6dec87e6e627d0ad2942e4b9670b22889cb4e8577f264` |
| k-Connected [optional] | Q1 → `mit:6042-online-k-connected-q1`<br>Q2 → `mit:6042-online-k-connected-q2` | `structures/tp7-3/vertical-7dbbc5839c46/index.htm` | `3f6bc8ac77dd3cc432efbd630b772220e8e1eb4a3eba8243b3c50141690392fd` |
| Chromatic Number | Q1 → `mit:6042-online-chromatic-number-q1`<br>Q2 → `mit:6042-online-chromatic-number-q2`<br>Q3 → `mit:6042-online-chromatic-number-q3` | `structures/tp7-3/vertical-312af3a98ad1/index.htm` | `02080350fb33fcdb3d69256cbbd4969c6b2024d905b4fe929ba0cac9b25891e3` |
| Random Walks (cont.) | Q1 → `mit:6042-online-random-walks-cont-q1`<br>Q2 → `mit:6042-online-random-walks-cont-q2`<br>Q3 → `mit:6042-online-random-walks-cont-q3` | `probability/random-walks-pagerank/random-walks-cont/index.htm` | `a9de2f6fb7a17189e0d34560937a71f7bb0189d690c17afc231fedd99fc08f43` |
| Random Walks | Q1 → `mit:6042-online-random-walks-q1`<br>Q2 → `mit:6042-online-random-walks-q2`<br>Q3 → `mit:6042-online-random-walks-q3`<br>Q4 → `mit:6042-online-random-walks-q4` | `probability/random-walks-pagerank/random-walks-0/index.htm` | `684249a6bd63754439ec4dea64cf6364a2efa38eb8213c1bf1e07679da2590b7` |
| Friends and Strangers [optional] | Q1 → `mit:6042-online-friends-and-strangers-q1` | `proofs/tp1-2/vertical-9380624edebc/index.htm` | `6a5121ac56953fc13377ecadcf7512c2943e6817d4116b5f30eeac5b39a1878f` |

## 源PDF文件SHA绑定

| 文件 | 页数 | SHA-256 |
|---|---:|---|
| `MIT6_042JS15_cp10.pdf` | 5 | `a3c4980db0405d42f516af75c36c211faa821022d2bc60a4a08741b24062a11e` |
| `MIT6_042JS15_cp16.pdf` | 3 | `bc25610de63a8f6bab48b9345792f456b0cc6026e121ce84cd82196e5258218a` |
| `MIT6_042JS15_cp17.pdf` | 5 | `cfb35659156304bf3d186dbd1ecba80e3a32ff162d391ab09aad665461f1279c` |
| `MIT6_042JS15_cp18.pdf` | 3 | `a515cb9cf4a98d08e44b54bc44bd9ec53616fd7f292dc1012d06a99a78a8485b` |
| `MIT6_042JS15_cp19.pdf` | 3 | `78968e0f7a7cc8794d5f8ca14943041f4cd91df931008cd89f47676f4337cd85` |
| `MIT6_042JS15_cp20.pdf` | 4 | `5a6eacfaf1ce9fc6ed6c251fe783be58a2bd70b880e0e91959d4565b6dc3c8dc` |
| `MIT6_042JS15_cp21.pdf` | 3 | `387a6b77c0b00fdb4c043529f6facde5f2e7930be963484e0701b96e84a97e9e` |
| `MIT6_042JS15_cp22.pdf` | 3 | `bc993c7230aafb90e91674bf4e1d3b479e22e937f03837766f92d18535855e3c` |
| `MIT6_042JS15_cp25.pdf` | 3 | `46825a62f7052da76aa1e3fc232d00e7e30fc24af2b0c52475c5b50b50957012` |
| `MIT6_042JS15_cp30.pdf` | 4 | `a9c63b5d6139a87dc78dfe65721995639df9fc940483839f53b5371c84ec2621` |
| `MIT6_042JS15_cp32.pdf` | 3 | `d52ea17d754978687cb0da4e841b97227b046b65eabc62426b3eb72edb809ff8` |
| `MIT6_042JS15_cp33.pdf` | 4 | `3651ae59179fb8c3309325b60d093242ed8beebf1f3600887a8283df93581d24` |
| `MIT6_042JS15_cp35.pdf` | 3 | `1d03abf86a07682ba4e98ba2331813261fe8e3ad35057a1c588b0aa53cd8279a` |
| `MIT6_042JS15_finalexam.pdf` | 14 | `a0b0ebb14be62481fd49884d7356ae9973179723263304dd60561dac3f4771b2` |
| `MIT6_042JS15_midterm3.pdf` | 8 | `1cc46956aa6a2eb840b223cb6d7267314bfe11e03eff2c1360268a51cc6722a7` |
| `MIT6_042JS15_ps4.pdf` | 3 | `54dee69b84c0aae9ace647734d871fdf38e613bd1d79fac2d62f854fa77adbf7` |
| `MIT6_042JS15_ps6.pdf` | 3 | `ea4d03b7b9565ffff138fab84f6d792a04bba0de257690071d2d8e32a8932748` |
| `MIT6_042JS15_ps7.pdf` | 4 | `d13092fdd041c61bfc24e023d0792cee1ad8f75a8b7f4dc36bea9ebac0d872a4` |
| `MIT6_042JS15_ps8.pdf` | 3 | `9e582132b94a97b03935c748a1ee427eba82d225feff71ce1dcc4cfe697c9f93` |

## 剩余关卡

父代理协调另一独立模型审读实际完整题面、解答及源映射；若返修，更新本字节绑定并重新运行脚本。随后由父代理做合册三轮编译、数学与图表排版、实际逐页视觉、目录及链接、源ZIP干净重编和远端完整性验证。本代理没有上传、提交远端或改变公开权限。

## 印刷嵌套小问与末端计数规范（本次补核）

2026-10-08T09:39:48.800168+00:00：重新逐题读50个选定原题的原PDF文本与现稿；另实际打开CP17物理第3–4页、CP30物理第2页、CP33物理第2页核对疑似层级。PDF提取时CP33仍报既有字体/流警告，该选定题已用实际页图补核。本次只补作者QA，未修改题面、解答、复核脚本或旧inventory。

历史 **147** 是原卷的**顶层回答单元**数，不是递归展开后的末端小问数。一级有(a)等标签时按每个一级标签计一个；未标一级小问的主问题计一个。新的末端口径保留该计数基线，只将正式印刷的嵌套小问展开，不再重复计其父节点；选项、术语配对填空、步骤/任务编号、图面板标签、公式号和文献引用号不新增嵌套末端。

仅发现一个有子节点的一级单元：**CP17:4(f)**。它的三个子问在原PDF清楚印作(i)、(ii)、(iii)，现稿题面与解答逐项保留。

| 原主问题 | 父一级单元 | 原印刷嵌套ID | 原物理页 | 所求内容 | 单个末端计数 |
|---|---|---|---:|---|---:|
| CP17:4 | (f) | **CP17:4(f)(i)** | 3 | 三点无自环完全有向图的覆盖弧 | 1 |
| CP17:4 | (f) | **CP17:4(f)(ii)** | 3 | 定向三圈的覆盖弧 | 1 |
| CP17:4 | (f) | **CP17:4(f)(iii)** | 4 | 比较二者的正长度可达关系 | 1 |

父节点CP17:4(f)：历史顶层数1，展开末端数3；整道CP17:4：历史顶层数6（a–f），展开末端数8（a–e各1，加f(i)–f(iii)各1）。其余49个选定主问题没有正式嵌套小问，末端数保持各自原顶层单元数。CP32:1–5仍只是CP19重复映射，不新增计数。

因此本课所选PDF的末端小问数为 **149 = 147 − 1 + 3**。36个在线页的75个Q作为另一个回答单元口径单列，不混入149个PDF末端。若父代理原全册PDF计数256中的其他课程109不变，则此次展开后全册为 **258 = 109 + 149**；这里仅复核6042部分，不重新背书其他课的计数。

### 疑似嵌套而不展开的项目

| 原ID | 印刷对象 | 分类理由 | 本次处理 |
|---|---|---|---|
| CP17:2题干1–8 | 银河项目任务清单 | 调度输入数据，不是(a)–(d)的子问 | 不新增 |
| CP17:3(a)术语1–8及描述1–3 | 选择术语编号并填入三处 | 原题明确是术语配对填空；按本次排除填空的规范不是正式嵌套小问 | 保留a为1个顶层/末端单元；三处实际回答仍全部写出 |
| CP30:3(b)条目1–5 | 圈选独立的事件对 | 原题说circle the event pairs，五条为该圈选题的选项 | 保留b为1个单元；五选项的判断全部保留 |
| CP20:1题干步骤1–6 | 寄存器程序输入 | 程序步骤，不是小问 | 不新增 |
| PS7:3图1(a)–(d) | G1–G4图面板标签 | 四图为同一道同构任务的输入，非四个作答子问 | 主题仍计1 |
| CP19:4(i)，同题CP32:4(i) | a–j中的一级字母i | 与(a)至(j)同一层，非罗马嵌套 | 已在顶层10单元中，不能再次展开 |
| CP33:4(c)两种共享边情形 | 一个(c)内的两个未另编号情形 | 没有正式印刷子标签，按明确嵌套标签口径不另拆 | c仍1；两情形都解答 |
| CP16:3(d)内定义/验证/求长度 | 一个(d)内多句任务 | 没有正式印刷嵌套标签 | d仍1；所有要求均已覆盖 |

### 每原PDF题组的顶层与末端合计

| 原PDF | 选定主问题 | 顶层回答单元 | 正式嵌套父节点 | 末端小问数 |
|---|---|---:|---|---:|
| `MIT6_042JS15_cp10.pdf` | 4 | 3 | 无 | 3 |
| `MIT6_042JS15_cp16.pdf` | 1,2,3,4 | 11 | 无 | 11 |
| `MIT6_042JS15_cp17.pdf` | 1,2,3,4 | 18 | 4(f) → (i),(ii),(iii) | 20 |
| `MIT6_042JS15_cp18.pdf` | 3 | 4 | 无 | 4 |
| `MIT6_042JS15_cp19.pdf` | 1,2,3,4,5 | 20 | 无 | 20 |
| `MIT6_042JS15_cp20.pdf` | 1,2,3,4 | 11 | 无 | 11 |
| `MIT6_042JS15_cp21.pdf` | 1,2,3,4 | 8 | 无 | 8 |
| `MIT6_042JS15_cp22.pdf` | 1,2,3,4 | 9 | 无 | 9 |
| `MIT6_042JS15_cp25.pdf` | 2 | 2 | 无 | 2 |
| `MIT6_042JS15_cp30.pdf` | 3 | 4 | 无 | 4 |
| `MIT6_042JS15_cp33.pdf` | 4 | 7 | 无 | 7 |
| `MIT6_042JS15_cp35.pdf` | 1,2,3 | 10 | 无 | 10 |
| `MIT6_042JS15_finalexam.pdf` | 2,4,5,9,12 | 12 | 无 | 12 |
| `MIT6_042JS15_midterm3.pdf` | 1,3,4,5 | 13 | 无 | 13 |
| `MIT6_042JS15_ps4.pdf` | 2 | 1 | 无 | 1 |
| `MIT6_042JS15_ps6.pdf` | 2,3 | 5 | 无 | 5 |
| `MIT6_042JS15_ps7.pdf` | 3,4 | 3 | 无 | 3 |
| `MIT6_042JS15_ps8.pdf` | 1,2,3 | 6 | 无 | 6 |
| **合计** | **50主问题** | **147** | **1个父节点、3个末端子问** | **149** |

### 正文未变的本次字节核验

| 子文件 | 本次只读SHA-256 |
|---|---|
| `cp-a.tex` | `a6790e7b2f4e6d4f090edf29bbec6b8eb862c4e28fe2e409ba3a0319d3b3b77e` |
| `cp-b.tex` | `b9ca1c409d5fe5ad066be5142408f7e613fcc10a20195a39a1ea666a6efa026a` |
| `cp-c.tex` | `23086af3c917d7b3dbf9bc60187d7f0d2be344f201c952b79f668a622ed215b2` |
| `exams.tex` | `f95329518e719f1d57440689c387badeb362fa58fbdfc72bf5017f388c2c4651` |
| `lemmas.tex` | `4e79f6499dce917893b6ae065ff27ccdfdcadfa5de0bd18098f8475f1f241870` |
| `main.tex` | `8e825fab1f89df0637cb192c2087f43c99df09b282d227639042df13a082a198` |
| `online.tex` | `23d65e945c9ac95f5141bf312015a4f6c0b5e70be12bdf577420e57d374c6705` |
| `ps.tex` | `f56962553ce7e5cb5a30e641e1ce346ea75b2583fd34d99230605244f8a6bb27` |
