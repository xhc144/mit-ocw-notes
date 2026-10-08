# 独立覆盖审稿

审稿角色：Sol 独立覆盖审稿；最终复核时间：2026-10-08T14:08:05.323910+00:00。

## 最终结论

数学题面覆盖通过：独立重计为12份PDF、36个物理页、54道原编号题、87个显式字母子问、18道未分问原编号题、105个解答单元。期末第2题按原编号计一个单元，其两个积分分别译录、分别应用控制收敛、分别求得 π/2。12章已有54个原生 `proof[AI 独立解答]`；它们按原编号合并承载105个单位，未要求一问一个proof。原12讲章的30个 `solution` 全部逐字保留。

覆盖审稿通过：首轮提出的来源边界、署名及历史课程提示全部修复，12份考核PDF/TXT/TeX实际SHA、字节、页数、题数、子问及单位与最终JSON全部一致。主体范围内未发现遗漏、错误来源或未解决的覆盖阻断项。本审稿未声称中文成册PDF视觉通过、编译通过或独立完成全部数学证明审稿。

## 核对方法与边界

实际逐份读取12份源TXT及12份对应TeX全部内容；按源TXT行首原编号与字母标号独立识别，先手工记下每题字母数，再用独立Python正则重计交叉验证，随后才比较JSON。实际用PyMuPDF打开12份PDF读取页数及逐页文本、图像对象数，并检查末页OCW署名。所有PDF图像对象总数为0；文本未检出个别版权、许可或限制标记。抽取文本的横线/共轭/排版丢失不作源勘误依据。PS8等源PDF闭包符号由各分段数学审稿核对；本审稿还亲自渲染期末源PDF第1页，核对final3的闭包及final4的Piazza原提示。

计数规则：显式(a)、(b)等每个计一单位；未作字母分问的原编号题计一单位。定义、前置定理、许可页不另计数学题。PS10第6题注明“不提交”，但题及(a)(b)(c)全部计入。最终计数不从父Agent或JSON的合计栏读取。

逐题语义审查关注原目标、条件、量词、定义、提示、附加允许引用结论和历史信息；允许原提示进入解答或简洁改述。数学正确性详查由另三位独立数学审稿者负责，本报告只确认目标承载与条件覆盖。

## 独立计数

| 源 | 每题显式字母数（0表示未分问） | PDF页 | 原题 | 字母问 | 未分问 | 单位 |
|---|---|---:|---:|---:|---:|---:|
| ps01 | 2, 0, 0, 2, 3 | 3 | 5 | 7 | 2 | 9 |
| ps02 | 2, 2, 0, 2, 3 | 3 | 5 | 9 | 1 | 10 |
| ps03 | 2, 3, 0, 3 | 3 | 4 | 8 | 1 | 9 |
| ps04 | 0, 0, 2 | 2 | 3 | 2 | 2 | 4 |
| ps05 | 2, 2, 3, 2 | 3 | 4 | 9 | 0 | 9 |
| ps06 | 2, 0, 3, 0 | 3 | 4 | 5 | 2 | 7 |
| ps07 | 4, 2, 0, 2 | 2 | 4 | 8 | 1 | 9 |
| ps08 | 2, 2, 3, 2 | 3 | 4 | 9 | 0 | 9 |
| ps09 | 3, 2, 0, 2, 2 | 4 | 5 | 9 | 1 | 10 |
| ps10 | 3, 0, 0, 2, 5, 3 | 4 | 6 | 13 | 2 | 15 |
| midterm | 0, 0, 2, 2, 2 | 3 | 5 | 6 | 2 | 8 |
| final-assignment | 0, 0, 0, 2, 0 | 3 | 5 | 2 | 4 | 6 |
| 合计 | — | 36 | 54 | 87 | 18 | 105 |

## 逐组覆盖要点

| 组别 | 核查的全部目标及容易漏掉的条件 |
|---|---|
| PS1 | 有限Hölder/Minkowski与原Young提示；p=1端点；ℓp赋范及完备；c0闭及Banach；全p范围单位球面闭而不紧；无限Hölder、泛函范数等式与双射。 |
| PS2 | Neumann级数算子范数收敛；可逆集开；真闭子空间商范数、单位代表元近距离、商完备；核闭及值域闭当且仅当拓扑同构；加权W的真稠密、不完备、闭图无界及逆有界满射不开。定义箭头源笔误明确记录。 |
| PS3 | 极限泛函与Hahn–Banach延拓无ℓ1表示；转置范数等式、各p右移范数、对偶配对左移；任意集合外测度平移；开集分量(a)(b)(c)、有理索引及允许无穷端点。 |
| PS4 | 任意函数的可测原像σ代数；有限外测度Littlewood第一原则双向与原逆向提示；有限区间并可测引用；可测集平移与正缩放。 |
| PS5 | 并交测度等式、有限首项递减连续性（原“从下”笔误明示）；扩展实函数乘积所有无穷/零约定及相反无穷求和指定a；限制、零延拓、平方模可测；E有限测度、几乎处处收敛及两部分Egorov构造。 |
| PS6 | 阶梯定义；阶梯、简单、有界可测函数近连续，保留共同B界、例外测度、严格误差及连续逼近零端点；L1三层密度与截断提示；复值Riemann–Lebesgue双侧频率极限。 |
| PS7 | 前置所有有限p的阶梯与零端点连续联合逼近定理完整；有限区间Lp→Lq、区间及全轴可分、全轴紧支连续密度；任意可测E的L∞完备、连续范数等式及不稠密；乘法算子全p范数等式；极化及平行四边形逆向构造。 |
| PS8 | 无限正交系闭张成及ℓ2展开、投影不等式及等号；双正交补为闭包；s≥0加权Sobolev定义、k阶周期端点含s=k、Hermitian内积、完备；s>1/2绝对和控制、连续代表元及嵌入界与M-test。 |
| PS9 | 前置L1趋零子列定理及证明、光滑偶非负紧支质量1磨光核；卷积光滑支集、一致逼近、L2光滑密度、L2收缩及逼近；自伴投影闭值域；闭凸最近点与变分条件；任意非负hk圆盘约束闭凸及逐坐标投影。源闭凸题缺非空条件明确作为条件勘误，未悄悄改题。 |
| PS10 | Arzelà–Ascoli前置定理与共同等度连续；C1双范数界和L2子列；连续核紧算子；s>0 Sobolev球是L2紧集；平方可和矩阵范数、双方向截断与紧性；左右移紧性、特征值/空间、闭圆盘谱全部五问；不提交Volterra全部三问含所有简单函数积分与C1代表元/初值。 |
| 期中 | 逐题分值与40分合计；Lipschitz范数完备；ℓ∞/c0上极限与允许事实；强极限非算子范数、双范数完备；扩展本质上确界包括无穷、零乘无穷说明；非负简单函数限制与不交分割积分。 |
| 期末 | 正确名称Final Assignment；逐题分值与40分合计；符号函数全Fourier系数及奇数平方倒数和；final2两个原积分；双正交补闭包；有界复对角列、自伴充要条件、趋零紧性及Piazza提示；乘法谱全闭区间、端点与无特征值。 |

## 旧内容保留

以git HEAD `b6446b546264788d5b45e1ac6cfc538101141cd2` 为基线，分别读取ch01–ch12，移除新增 `legacy:*` 标签后逐字比较全章文本，12/12一致。进一步按 `\begin{solution}...\end{solution}` 抽取逐段比较，30/30逐字一致。各章solution数为3,3,2,3,2,3,3,2,2,3,2,2。此证据强于仅复核环境数量。

## 来源许可及课程信息

12份源PDF末页都保留MIT OpenCourseWare、课程18.102/18.1021、Spring 2021与terms地址。12个已下载官方资源页HTML均含CC BY-NC-SA 4.0及OCW使用条款链接；本地官方terms HTML给出相同默认许可、署名、变更说明、非商业与相同方式共享要求。本轮没有把检测不到限制标记说成第三方权利的穷尽保证。现有LICENSE.md与ATTRIBUTION.md保留授课者Casey Rodriguez、笔记者Andrew Lin、来源及相同许可；考核题面作者归属应明确教师，不能将Andrew Lin记为所有考核题作者。

本地大纲/日历/考核目录快照支持：每周2次1.5小时、两组先修课程、无指定教材、10份作业1份期中1份期末作业、作业50%/期中25%/期末25%、最低作业分舍去、第7周24小时带回期中、课末48小时期末作业；日历作业截止位置为讲次2,4,6,8,10,14,16,18,20,22，期中在11–12讲间，期末在最后。译稿未虚构公历日期。Final PDF写Final/exam，大纲与资源目录明确Final Assignment，中文命名正确。

## 首轮问题的最终复核

| 首轮发现 | 最终状态 |
|---|---|
| 来源说明仍将考核题译编列为未覆盖 | 已修复：source-map明确全部12考核已收录，保留测度构造和一般Sobolev的范围边界；逐份36页/54题/105单位表与独立计数一致。 |
| 署名说明尚未列新增考核 | 已修复：ATTRIBUTION明确Casey Rodriguez课程的10作业/期中/期末、大纲及日历，区分课堂笔记与新增AI题解，保留OCW与许可依据。原件README的后续编译页数等元数据不属于本报告主体审核范围。 |
| 原件允许参考材料及历史规则细节略写 | 已修复：course-information列明Melrose、教师手写、Andrew Lin、Royden（已购）、Piazza等材料及MIT Institute Policy 10.2，另补合作者右上角、延期邮件、90/A和80/B上界；准确区分PS6及PS8提交说明。 |
| PS4与PS7历史提示定位未出现 | 已修复：PS4第8讲改排第5周、PS7(b)当周第二讲证明提纲均已补回。 |
| ps10及final-assignment翻译SHA因返修过期 | 已修复：最后复核12/12译稿SHA、12/12PDF SHA、12/12TXT SHA全部匹配JSON；每题子问数组、units数组、对应TeX标签及all_original_targets_retained逐题对应。 |

最终source-map复用表所列旧例题/习题标签均实际存在；新增题解及source-map所有源码交叉引用目标均存在。这里只验证源码级引用闭合，不代替编译后引用检查。旧章节本轮再次确认只增加legacy标签，30旧solution与基线逐字一致。两个最终source-manifest副本中的12考核条目按实际下载文件再次逐项验证字节、PDF页数及SHA，并核对授课者Casey Rodriguez、Spring 2021、资源页和默认许可。

最终排版复核：source-map移除表内合计行，改为表后正文合计句，36页/54题/105单位/87字母问/18未分问的内容完全保留；作业10及期中行尾使用longtable不分页标记，仅影响排版。main新增Casey Rodriguez课程考核书目，正确链接官方考核目录并保留12份/36页及非官方答案说明。全部12个考核章节哈希再次匹配清单。此轮未验证成册页数或视觉效果。

## 实际SHA-256绑定

以下为最终复核实际读取字节的哈希。后续README编译页数等元数据、成册PDF与ZIP不在本报告SHA绑定范围；主体文件若再修改须重核。

| ID | PDF SHA-256 | TXT SHA-256 | TeX SHA-256 |
|---|---|---|---|
| ps01 | `40aea0451b95316b12aca2a0fb9d2b9ad42cc377a98860e1064bd5f22b1203be` | `027f7f6b9745e5c8c0907e966afb185c7d78ff8fc39baa6b35438224a397d00a` | `7190537d3582a4d146c494dd83ebd9648a6f0a18977d907082de3477db50ccdb` |
| ps02 | `113bece19c82c39d6d25319b937b6cae2960b3966e91b908cda3145c5eab0214` | `759d076a88cf4af2df05737a60fc99b66d3cf7384fe0618ce3d18729ecfbef60` | `335bc22d9a2e9223bca62deb63e2a6cd183a7f443ea64ddc5317dd5abbbdd7ad` |
| ps03 | `0a5c62b71b0eef906d203a46ce2f2e6b8b05f5066acb06da92c7d9feb7fb5fca` | `f900624be4cee64aac08709a584ea9bda53978f50c879c505178cbc8f574c7b6` | `a4799312365c50f233eb2d70a25eff8055023af4f84c31dae02b8549c9a1cbe4` |
| ps04 | `80e94b464666200b10e8cc08726c1bae18c6754f383ba721e4efe3e003a80aa7` | `448f1a13000305adcdb4a3ea639f0aa618ff3150f16497025a72a0208b0801ab` | `12012ed48c6a320c07d830400584a34c3202752db09be8ca047613c00faf3f6e` |
| ps05 | `58cba454875308fab6b3b533226b049df0dc9613535068adf9a4d2d1c26ab928` | `fbfc928bff62d38e9933c5a7b3f625c058133c80ca3ee6a6347b2a45571bd54a` | `4e6571e5c247eb82ab0aa9c9357eeccff426bcdab7a3e4211d34d229b62751f8` |
| ps06 | `78ea994f611d080a14b89d2f6401394a05994f6d2b0676b5a941ee174516e303` | `e403a6d74b12848a174d283b6fea717e68cfe980251c83e62ddc8dadd63864a3` | `2a8c38d9c3cd2ed479e7e688849c112bedc1afdfa6fa2fb5150c114e7540a4f8` |
| ps07 | `4539f14904fc1f68d44b3b1a9f2ff8b7d0cf720dc1d38338a02d5372bc26329b` | `cd445b91c9e9abf5e15e2584087c725584e4f0b56552aeb2c2c9b6190c13361f` | `78d44864839ee82402ff2a8ace2f45ede20b1addd9064a6ecf52b025a4754124` |
| ps08 | `f9b28762cf195cd2ba99932c38cbe73274cb40fab934bb3045ee93c16e7f1a39` | `13f2ea4457a21d00bb77bf4af095bed766dc2ca933a6a8cf22dd7dfb424e9603` | `b6665046cab778426231b2fecc3abdb4237e6ab4776c44ce6d48ae872929a726` |
| ps09 | `a61245e67874af0b25ffe85df0d24c3a0afa45b0f65b80c4bf182cb058f76107` | `460d99752f3866d31e47d86017d2d9d71a69fdca5624b0a77f5254fac2efdb06` | `1db0816ebff00f191bc7982d05be6751e0e72b75307ad6f9926e2a327341e0cd` |
| ps10 | `409bfec7a5d10e4987f75238f479f4ab73784da57f9157a5747f5e8ae6b92abe` | `6a323b62cc62a758b7ba9ccb8997ada5f321dcb0533a2fda8decf5dfb835860e` | `51ba41c4faeac77bd004f09db8d2748100a7c986c8adb18148a68d5ff7cd8bce` |
| midterm | `c6becb52622c4ad20fc5caaf12993928808f3715d3d684bc2a1dda9b0463ae80` | `8212a77d2fc161a189df8010c75b369bed1fed28b7ec898abd3b43e9aa29d699` | `cdbf690ec79230396e740c300eeee309cf419422a04bab747492eb5718d0b3ed` |
| final-assignment | `b09cb1a93738680c597e9bea89c2f18e45cf1a79fa28f7e9f4bc831a5d60291d` | `2b9367fdd0dd9ddbb0bbeeb759e03cf925c0edb6fbc90b00300e1cbc0aeb4775` | `568b6e88d44b774c1a02cefe14f89d90f69404119820c157f2487a955cdae69b` |

| 其他实际核对文件 | SHA-256 |
|---|---|
| `subjects/functional-analysis/assessment-inventory.json` | `2ffef4911b59fdadaa7375d48e80e7779a759395da16a56af4ed2ac2a2e30ac8` |
| `subjects/functional-analysis/chapters/course-information.tex` | `b41593fe2f9dd596db249d9f97f85395f944f325415eccda130dda27e67be7dd` |
| `subjects/functional-analysis/chapters/source-map.tex` | `5d8ada75dddd4b68d62541666affd8f4fe7b909eaed13a975fbad47481604167` |
| `subjects/functional-analysis/main.tex` | `36c53c2138f609d65a0158d08fda6b5ec65b2599c575dbf7a210867456a3d770` |
| `subjects/functional-analysis/ATTRIBUTION.md` | `958a7926b4575fc11d66764e4b9cffaeb2714099f0766697bbca393a773f0c47` |
| `subjects/functional-analysis/LICENSE.md` | `fe2356ebc3baa6b23076d83c43289c26a8aa540e1c9f64586f0f11d249653546` |
| `subjects/functional-analysis/source-manifest.json` | `52547c803275f851985ac97bcfe09bbd6ae25e97c79bc3806322c2b13a6faaa2` |
| `sources/functional-analysis/18.102-spring-2021/source-manifest.json` | `52547c803275f851985ac97bcfe09bbd6ae25e97c79bc3806322c2b13a6faaa2` |
| `sources/functional-analysis/18.102-spring-2021/assessments/syllabus.html` | `bfcacfb0b005e74198bf380d056c77632200c99bc9cd2f6d38097332b04e26be` |
| `sources/functional-analysis/18.102-spring-2021/assessments/calendar.html` | `77328a2f73c7f042ee87a7b03edc37a04fe98ccb519b56830b90fc7beda6494d` |
| `sources/functional-analysis/18.102-spring-2021/assessments/assignments-and-exams.html` | `8cd42657ca61c3d15dda4367fb816d2cf62b664436e2ecb66cc4bd09a55d8b2d` |
| `sources/functional-analysis/18.102-spring-2021/ocw-terms.html` | `8888d5224b8c134f7b4f2dd0c0116839678815c913a6ad94927c1c64c3c3b055` |
| `subjects/functional-analysis/chapters/ch01.tex` | `083a3708ac617aaf7c29363dd6be17339d86a257c7f9c1ea87fe315be30a80f1` |
| `subjects/functional-analysis/chapters/ch02.tex` | `360acb6c340e8df790193fd9f862b15855bdb1fcdbbd95d8eef2789ea38d01a0` |
| `subjects/functional-analysis/chapters/ch03.tex` | `f9bab4dcef55dce157f78779a5ea596df1c0a5cb160448f7f7481bbb1fdd6827` |
| `subjects/functional-analysis/chapters/ch04.tex` | `c50b5ecd9559b4611a507b1d74fbee9fef890efa4b42cf421e1af1c029892456` |
| `subjects/functional-analysis/chapters/ch05.tex` | `d5661e517d199183ff17dfb3906f106fae57c45ffbd8ac0d158744c133479bdf` |
| `subjects/functional-analysis/chapters/ch06.tex` | `790872007fa96df530c6c0f8c1ca6c2ae51b4f67ced901f0859bb034b2efe272` |
| `subjects/functional-analysis/chapters/ch07.tex` | `64054485c8858f6ba8b07dfd3731c91ec5f8a7672f9a391ed7bf850cea48876f` |
| `subjects/functional-analysis/chapters/ch08.tex` | `b1498b21c34f72ecbca44ce29b757aeb3f6291a29a20639223c944d38967a2b5` |
| `subjects/functional-analysis/chapters/ch09.tex` | `24d2be56eea6ce2d4c875665e80f60603a3cb00aa874c4b0178dbd4296cb7d4c` |
| `subjects/functional-analysis/chapters/ch10.tex` | `63c033c12eb1e39b96fbdfd1c1854da34ec688ac1981b864407cbe9a7f5ec94c` |
| `subjects/functional-analysis/chapters/ch11.tex` | `67e793632b259828df813a6b2eccd02cf60f622db16a8720b815f9b2742407aa` |
| `subjects/functional-analysis/chapters/ch12.tex` | `abd2c5bb70367ac69923ebffad2180959f80f496406ea86b609be49d79b5d193` |
