# 课程信息卷首来源复核

复核日期：2026-10-08；已复读root更新考试措辞后的当前卷首全文，并冻结本报告所绑定的版本。范围为 `subjects/mathematical-statistics/course-information.tex` 全部59行；同时只读核对 `course-metadata.json`、已保存的官方 Syllabus/course-home/lecture-slides/Assignments HTML、实际 Introduction PDF 物理3–5页与11份作业PDF首页。未修改卷首、数学正文或题解。

结论：**来源事实复核通过，没有必须修复的日期、主题、版本混合或身份陈述。** 本结论限定为所读版本的来源忠实度，不代替作业解答数学审校、PDF布局审校或对整个互联网资料的穷尽检索。

最终全文读过的 `course-information.tex` SHA-256：

`c5acddd41795b643d8965034d2b15232ae083033cc01e6bd513f6594f757b064`

## 逐项来源核对

| 卷首位置 | 内容 | 实际核对来源与结论 |
|---|---|---|
| 第4行 | MIT18.650、Fall2016、数学系本科、教师Philippe Rigollet | [官方课程首页](https://ocw.mit.edu/courses/18-650-statistics-for-applications-fall-2016/)及其保存HTML；一致。 |
| 第4行 | 初讲助教Victor-Emmanuel Brunel | Introduction物理3页，以原PDF2倍渲染实际查看；姓名与角色一致，没有冒称当前网页列出TA。 |
| 第4行 | 将实际问题建模、理解方法依据及局限 | [官方Syllabus](https://ocw.mit.edu/courses/18-650-statistics-for-applications-fall-2016/pages/syllabus/)的课程描述和目标；中文概述覆盖其建模、选方法、理解适用范围的意思。 |
| 第10行 | 每周2次、每次1.5小时；18.440概率水平及线性代数 | Syllabus对应栏目；一致。 |
| 第11行 | 18.600或6.041、Calculus2、矩阵/向量/乘法/正交、无指定必读教材 | Introduction物理5页2倍原图实际查看；一致。 |
| 第12行 | 周二/四1:00–2:30am、习题课TBD | Introduction物理4页2倍原图实际查看；`am`确实印在原片，保留未核正的源词、不推时区准确。 |
| 第13–14、18行 | 网页20/30/50与初讲30/30/40分别列出；每周作业11次取最好10次 | Syllabus评分表和Introduction物理4页；两版来源被显式区分，未把一版替换成另一版。 |
| 第15行 | Nov8、随堂、80分钟、闭卷闭笔记/可带cheatsheet；finalTBD、2小时、可带书笔记 | Introduction物理4页2倍原图实际查看；日期、时长和开闭卷身份一致；当前“不可带笔记，可带cheatsheet”准确对应原片，没有扩大或缩小笔记/cheatsheet范围。 |
| 第18行 | 所核公开页面未发现考试题卷PDF | 保存的课程导航只有Syllabus、Lecture Slides、Lecture Videos、Assignments；现有表述限定所核页面，没有声称没有举行考试或所有公共网站都没有题卷。 |
| 第21、26–35行 | 10主题分组覆盖讲次1–24 | [官方Lecture Slides页](https://ocw.mit.edu/courses/18-650-statistics-for-applications-fall-2016/pages/lecture-slides/)保存表逐行对照；所有区间和主题一致。 |
| 第21行 | 导航未提供逐次日期独立课历 | 已读公开导航及lecture分组表不含逐次授课日期；该句指导航范围，不能扩写成全站不存在课历。 |
| 第40行 | 11PS、未公开官方解答、AI解答非MIT答案 | [官方Assignments页](https://ocw.mit.edu/courses/18-650-statistics-for-applications-fall-2016/pages/assignments/)明确11份且不提供solutions；卷首对项目自行推导解答与官方身份区分准确。独立推导/复审的过程属于项目声明，网页仅支持官方未提供答案这一部分。 |
| 第42、47–57行 | 2016年各PS截止日期、中午12点、无独立发布日期/明确时区 | 11份实际官方PDF物理第1页重新读取，与冻结源清单和下表一致；每个日期按Python日期历核验均为星期五。 |

各课件原始页的位置以**物理PDF页**为准，本次另实际打开 `/tmp/course-information-source-review/intro-p3.png`、`intro-p4.png`、`intro-p5.png`；这些是原Introduction文件以`fitz.Matrix(2,2)`渲染，未重新排写内容。其原文件为 `sources/18.650-fall-2016/pdf/7836ea6d101679d495194bc3c5f227fa_MIT18_650F16_Introduction.pdf`，SHA-256仍与既有source-manifest一致。

## 作业主题与截止日

所有主题均以 `assignment-inventory.json` 中实际主问题标题对照，而不是从授课主题猜测。原题未编号任务及嵌套子问的覆盖由作业冻结清单及独立题解审核负责，本表不增加或改写原题结构。

| 卷首行 | PS | 核准截止日期 | 对照主问题标题的主题判断 |
|---:|---|---|---|
| 47 | 1 | 2016-09-16 12noon | Convergence、True or false、Bernoulli confidence interval；“统计断言”是恰当中文概述。 |
| 48 | 2 | 2016-09-23 12noon | Biased/unbiased、Models/identifiability、Poisson CI、Uniform CI；一致。 |
| 49 | 3 | 2016-09-30 12noon | MLE、一致性、KL、Total variation；一致。 |
| 50 | 4 | 2016-10-07 12noon | MLE/Fisher、Method of moments、Censored data；一致。 |
| 51 | 5 | 2016-10-14 12noon | Tests/CI、Comparing two means、Implicit hypotheses testing；一致。 |
| 52 | 6 | 2016-10-21 12noon | Basics、Student one-sided、Bernoulli independence；一致。 |
| 53 | 7 | 2016-10-28 12noon | QQ plots、Two-sample KS、Independence continuous cdf；一致。 |
| 54 | 8 | 2016-11-04 12noon | Heteroscedastic、Random design、Logistic regression；一致。 |
| 55 | 9 | 2016-11-18 12noon | Fixed-design nonparametric regression、Density estimation；一致。 |
| 56 | 10 | 2016-12-02 12noon | Bayesian estimation、Bayesian linear regression、Covariance matrices；一致。 |
| 57 | 11 | 2016-12-09 12noon | Exponential families、One-parameter canonical families、Latent-variable linear model；一致。 |

不存在把PS9错误移到11月11日、或把PS10错误移到11月25日的情况；按原PDF保留实际间隔。

## 许可、原图与来源身份

本批作业的默认许可身份仍是MIT OCW的CC BY-NC-SA4.0，源与中文改编的署名、非商业、同许可要求见既有 `assignment-source-audit.md` 和官方条款保存证据。未发现新增作业第三方权利例外。此项不撤销PCA课件中既有Nature转载例外，PCA原件/全文仍维持hold。

PS7官方原PDF物理1页有2个JPEG对象，物理2页有3个JPEG对象，五个对象均512×511；外部`QQ-Plot 1`至`QQ-Plot 5`图号是PDF文本。原图已实际查看，没有见到独立第三方声明。只读检查作者的两份PDF裁切结果，重新提取的JPEG字节SHA-256全部与官方原PDF对应对象相同：

| 裁切文件 | 保留JPEG对象 | 图号文本 | 文件SHA-256 |
|---|---:|---|---|
| `assignments/assets/ps07-qqplots.pdf` | 2，均原字节匹配 | QQ-Plot1、2 | `46ecdfeebad198219d562af4287564d23b8f595d0eaed3d14d73166238fc6267` |
| `assignments/assets/ps07-qqplots-2.pdf` | 3，均原字节匹配 | QQ-Plot3、4、5 | `faf01265694750c2bb993fcf3273562bcfefb912cd1b366cea49a492dc40aa7a` |

因此`main.tex`第158行“原题QQ图PDF剪裁，其中五幅点图保持原有图像数据”的身份陈述准确；这些图不是纯矢量点云，也不是PNG新绘图或重新随机生成的替代样本。该核查只确认裁切保留对象和许可出处，不代替最后排版图形的视觉检查。

## 当前考试措辞复核与审核界限

无必须修复项，先前措辞建议已由root落实。最终复读第15行当前文字为“闭卷且不可带笔记，可带 \textit{cheatsheet}”。本次重新由归档Introduction物理4页渲染2倍原图并实际打开 `/tmp/course-information-source-review/intro-p4-final-recheck.png`，确认原片连续文字确为 `Closed books closed notes. Cheatsheet.`；当前卷首准确对应，不再将notes限为课堂笔记或将cheatsheet限为公式单。原片没有公布cheatsheet尺寸，本报告不补规则。复读过程中未修改卷首或任何source/manifest，仅更新本报告的当前文件哈希和已落实建议状态。该报告绑定版本现已冻结。

保存的Syllabus和course-home快照字节数/SHA均与root提供的course-metadata吻合：Syllabus42944字节，SHA `4a3469a277e8e733a3c969d584dded8a7aa982fe1a9572775a25649d4421e98e`；course-home37725字节，SHA `d26e9fb238c5272cfadd7e84169a151451dd30b8fe094e23aa3cbf7e34598f0e`。本次未重新下载远程网页，结论据2026-10-08已归档实际来源及原PDF，未运行任何网页脚本。
