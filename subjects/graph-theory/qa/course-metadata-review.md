# 课程参考信息：独立核查记录

2026-10-08只读独立审查两份书前课程资料，并对照五门课程调查清单、已归档官方HTML及相关PDF原页文字。发现两项措辞问题，已由主代理返修，本代理重新核对后均关闭；修后未发现其他实质元数据错误。审核者未编辑书前正文，只写本QA。本记录为模型的独立来源核查，不是人类专家校订，也不是最终合册版面的视觉验收。

## 最终绑定

| 文件 | 行数 | SHA256 |
|---|---:|---|
| `frontmatter/course-info.tex` | 102 | `8f489c139a8d334fc6cd843c5a5ebaea6750a50b6d1dda75340581a6f89c4631` |
| `frontmatter/supplementary-courses.tex` | 77 | `81c05c3000ae859edbdfec4636ec1b7d60aa5475eb322ce22d0a49777d5b452f` |

2026-10-08排版lint返修后复核：四个标准subsection星号标题替换为未编号粗体内容标题，实际规格为12/17pt、前距9pt、后距4pt、Needspace四行，与锁定originalsection的标题文字规格一致。只有这四行标题呈现命令变化，四个题名逐字保持。将四行机械逆替换后恰恢复上轮已审SHA256 `7974080ab351cd48fc7450d96c7ec3b1433bb2352b889bed413145f67aa0d3fb`，故正文、书目、讲次、评分及元数据零变化；course-info哈希仍未变。新hash更新上表，来源审核结论保持。此核验不宣称已查看新的PDF页。

主源书前资料末尾实际input补充资料，两个文件均在本轮范围。上述哈希再变动时需重新绑定，不能把本轮当成未来版本的验收。

| 调查清单 | SHA256 |
|---|---|
| `assessments-inventory-18315.json` | `3cd990e6752094a612c59043b44d597675fc6eda7b4a829beeaa21282d9e003d` |
| `assessments-inventory-18433.json` | `b0ccf07ed041d373dc3bf8d96900ecc2d29ab24c961af4ea16783bc964866940` |
| `assessments-inventory-18212.json` | `758203a1f5d479da8b3eaf6d60b3e58e49b795e8f5a872e27670f84bec580014` |
| `assessments-inventory-18217.json` | `3eb1ba9d4fcda3ac5817ad3e343d00500a3847381ab23a1f95898bf9a3f3b434` |
| `assessments-inventory-6042.json` | `9ec9654057ce99df80711605db6b31014a83085d1fa1123b2e4f753bf9dfa6c8` |

## 已发现并关闭的问题

1. 补充资料第70–71行原6.042阅读写为`13.1--14.8`、`16.1--19.5`，会将官网跳过的13.6、14.3、17.6等误列为连续指定阅读。主代理改为各节准确并集；还将第59–61行跨章笼统范围改为逐章集合。本代理再次对照官方Readings的35条逐课记录，确认第59–72行现有并集与原课指定范围吻合，并保留17/18课的9.5重叠。
2. 补充资料第50行原“写作可以是课堂笔记或维基百科贡献”给出二选一推断；官网Syllabus只并列Writing assignments: (1) course notes and (2) Wikipedia contributions。主代理已改为“写作作业包括课堂笔记和维基百科贡献”，不推断任选一种即可，也不编造额外提交次数；复查关闭。

没有遗留待修项。并未按记忆更正官网不完整书目，也未把另一学期安排或PDF数字创建时间改成授课年。

## 按课程核查

| 课程 | 人员、学期与层次 | 课时及先修 | 进度、阅读与考核结论 |
|---|---|---|---|
| 18.315 | 官方完整课程名、Igor Pak授课、Amanda Redlich课堂记录者分别有官方页面支持。Graduate；官方Spring 2005与作业Fall 2005冲突明确保存，部分手写秋季日期另归档，不推断哪个应当改。 | 每周3次×1小时；无正式先修课，但组合熟悉度及Catalan/Ramsey/生成函数/Euler迹/凸三维多面体三连通/Markov/Chebyshev/有限群准备均来自大纲。 | 39讲逐行主题和8个作业截止讲次一致，未推造具体日期。八作业等权、无考试、每题至多四人合作且各自写答案来自官网。四主要书目/两补充书目及1999/1998/2004/2000/1997/2002逐项按此课阅读页登记。 |
| 18.433 | Combinatorial Optimization，Santosh Vempala授课，Fall 2003，Undergraduate；未把Lovasz等参考作者当授课者。 | 每周2次×1.5小时；18.06或18.700，均线性代数。 | 全27讲范围及A1–4截止、两场Exam I/II讲次相符；不把Exam II擅称期末统考。25+25+20+6+24=100，项目研究/展示分别20/6。个人或两人项目、第五次课后次日确定来自大纲。七参考书缺年份/版次/ISBN忠实留缺，不补Plummer等官网未列作者。 |
| 18.212 | Algebraic Combinatorics，Alexander Postnikov授课、Andrew Lin讲义记录，Spring 2019，Undergraduate；Richard P. Stanley为教材作者。 | 每周3次×1小时；18.701 Algebra I或18.703 Modern Algebra。 | 全39讲相邻范围无缺号，PSet1/2/3截止12/23/37与讨论13–14/24–25/38均一致。三作业评分未推断等权或百分比；约六题足够只归PSet1。阅读AC2018/在线2013、EC1官方1997、EC2官方2001及选列的四项图论阅读准确。 |
| 18.217 | Graph Theory and Additive Combinatorics，Yufei Zhao授课，Fall 2019，Graduate；讲义由学生记并获其协助编辑，不能把PDF制作者误作全部原作者。 | 每周2次×1.5小时；无指定课程号，数学成熟度为数学研究生一年级。 | 全26讲与六次作业截止6/10/13/17/20/26相符；无考试，最终取两类表现较低者、边界参与、A−/星号指导明确，未编百分比。写作包括两项、不二选一。课程未列必读教材/逐周书目，讲义文献不冒称指定阅读；2023书仅链接。 |
| 6.042J/18.062J | Mathematics for Computer Science，Spring 2015，Undergraduate；Albert R. Meyer和Adam Chlipala授课。Eric Lehman、F. Tom Leighton、Albert R. Meyer为教材作者，与教师分别列。 | 每周3次×1.5小时；18.01一元微积分，数列/级数/极限/微积分准备正确；翻转课堂6–8人团队来自大纲。 | 全35课与阅读精确并集一致；25/5/15/30/25=100，三期中各80分钟、单张双面纸，期末180分钟、两张双面纸及舍弃最低一次作业/三次课堂均有原文。PDF答案限制与公开在线反馈解释分开；2019重发布不改变2015编写年。2015教材原封面及版权页文字确认作者与2015-05-18修订，不用2020数字加工日期替换年。 |

18.315与18.212的Stanley卷I年份不同是两门课程官网书目自身不同：前者合列卷I/II为1999，后者分别列1997/2001，稿件均说明“按官方/课程列”，不将这些差异私自统一。本核查没有重新确认出版社历史版次，声明范围限于课程所列书目。18.433的Lovasz/Linear Optimization等缩写同理保留原列法，不冒称完整出版书目。

## 讲次覆盖与表格压缩

除逐行读官方进度、主题及关键事件外，机械展开稿中区间核对：

| 课程 | 期望序列 | 实际覆盖 | 缺号/重号 |
|---|---|---:|---|
| 18.315 | 1…39 | 39 | 无 |
| 18.433 | 1…27 | 27 | 无 |
| 18.212 | 1…39 | 39 | 无 |
| 18.217 | 1…26 | 26 | 无 |
| 6.042 | 1…35 | 35 | 无 |

共166个官方课次位置。补充课程将相邻讲次主题合并概述，没有删去课次或调换进度；详目保留在官网/五调查清单相应course_metadata，不能把概述表当成每讲逐字翻译。周课时未外推总学期周数、总课时或公历日期；只有讲次的官网Calendar不凭空填日期。主源39讲与本册17章阅读顺序区别清晰，不声称课程进度全部内容编入正文。

## 官方证据文件

以下是本轮实际读取的主要网页证据，哈希从本地归档原HTML读取；官方URL在两份书前文中及各清单中已有对应。HTML正文提取只为阅读与核字段，不当作实际PDF版面视觉。完整ZIP与评测可得性本轮依照已审调查清单及归档目录核对，没有重新下载并猜测未来版本。

| 官方证据相对路径 | SHA256 |
|---|---|
| `sources/graph-theory/assessments/18315/syllabus.html` | `dfce0868b89c87dcd0d2d2f63927f920e7c8da39d4eb0dea5ba6fb9602a4f361` |
| `sources/graph-theory/assessments/18315/calendar.html` | `b8fb7a0d75afc1f3fe35f4e8111ac569724dba5d7d28375078775f822f869ff3` |
| `sources/graph-theory/assessments/18315/readings.html` | `fb74d0a253a0eae64fc92009179615f42063ac3d63d983887b568c7b1612b879` |
| `sources/graph-theory/assessments/18315/assignments.html` | `e61cfa30efb9fc312f791a28d4914ec021ef3a10e4acd8bc153b964691072eaf` |
| `sources/graph-theory/assessments/18433/html/course.html` | `9961a25b07f36eba9f6a287a608a42019c02a49b950e6bd864767c36f694e764` |
| `sources/graph-theory/assessments/18433/html/syllabus.html` | `589ab6464e156010bbb2fd4e917ea2ce871b0baa6ed28f355fb9a9760c46701d` |
| `sources/graph-theory/assessments/18433/html/calendar.html` | `6c5bea69bbf421d41d6024b12c259d7227daaa705942fcc20f9f166aec85d823` |
| `sources/graph-theory/assessments/18433/html/readings.html` | `8183001a741dbeee289ba611ca37bcf42ffaf47b858ed46a104667bf9ab9d18b` |
| `sources/graph-theory/assessments/18212/html/home.html` | `1b02de92fdedf344963ae54d2dc87e8df1eb8461743727834f6705158cdc2ac4` |
| `sources/graph-theory/assessments/18212/html/syllabus.html` | `ed7efba048721243ec733b1d95519df8b6fdc4d93fc4b42f99d3e37e1e0ae9ca` |
| `sources/graph-theory/assessments/18212/html/calendar.html` | `decc15d642ef4ac3dfdffb60b724d60ac359759733fb362bcd9ceb18fd010876` |
| `sources/graph-theory/assessments/18212/html/readings.html` | `ad8c71232b803c09cc68460c9fea5d41280ea812bc645f0bb63754235fd10ee7` |
| `sources/graph-theory/assessments/18217/html/course.html` | `7dced92faff1cf3b504ce6592a873c944449cd3c8c89d97bdc724afb22c31017` |
| `sources/graph-theory/assessments/18217/html/syllabus.html` | `358c9f0e4b6ce90df9a3ed78d5af63a2f6390951cf27163ad410cf458225ad91` |
| `sources/graph-theory/assessments/18217/html/calendar.html` | `e614c0ca92b68296972cdec0cac70b4af1d87244c4078978f3399099d9e3ff91` |
| `sources/graph-theory/assessments/18217/html/lecture-notes.html` | `3542f219c45ac9d7c2e0483b6daf211434d5be34359ebb0d78f93d18c0b9f4d7` |
| `sources/graph-theory/assessments/18217/html/assignments.html` | `4670f6696832089ec14f189b5dfa80bad7c1c4ab213150b5013fd972ae1c5d66` |
| `sources/graph-theory/assessments/6042/pages/ocw-course-home.html` | `afe4f3ed4daacb78241cad45b78a7824f66bbbe6feb3d05aa013903e7359f996` |
| `sources/graph-theory/assessments/6042/pages/ocw-syllabus.html` | `95af25a44bfe543b2d08b54615859703ec0c38e0b4f5cdc57551554f347e26ef` |
| `sources/graph-theory/assessments/6042/pages/ocw-readings.html` | `aab08928d22563a2b2391a5ece3a918745af424282a47dcc13df9bba6d98ccef` |
| `sources/graph-theory/pages/18315-lecture-index.html` | `c06d9d20b77458b366175cdae6248c6c2eeaa477bcf6bcebeecc1b9698d16240` |
| `sources/graph-theory/assessments/6042/legacy-metadata/in-class-questions/index.htm` | `afad192925d568fd6c34b41a1cc3625742d49af547ea15fd659fe7e216451bb1` |

其他已审来源：PSet1关于提交约六题说明、6.042教材原封面/版权页及五调查清单逐文件许可与答案可得性。未变动两正文及任何旧QA，仅新增本记录。最终合册书前分页与字体实际视觉检查仍待独立执行，本文不声称已完成。
