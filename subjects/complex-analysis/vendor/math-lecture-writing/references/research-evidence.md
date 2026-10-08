# 研究证据与使用边界

输入 v3 包附有下列 12 条研究文献记录。以下核验深度是旧包的自述，本次仅保留来历，不表示重新确认题名、正文或结论。它们不是本 Skill 的实验证明，也不能合计为独立验证次数。 研究级证明报告、对话辅导基准、一般数学论述、训练实验与教育综述的外推范围不同。机器可读详情见 `sources.json`。

## 核验记录

### R01 · Mathematics in the age of AI
作者：Terence Tao。版本：2026, arXiv:2608.16753v1。
原始来源：https://arxiv.org/html/2608.16753v1
类型：数学实践评论/讲演改写。旧包所记核验位置：§6；致谢；参考文献区（相关段落，不冒称全文）。
旧包概括的观察（本次未复核）：AI 数学文本可能把平凡步骤写长，却淡化关键困难；高层路线和文献定位也需关注。
设计主题：详细解释、隐含命题、自然连贯表达、理解与迁移。这是写作工程选择，不是效果证据。
边界：来自数学研究写作的专家观察，不是针对本 Skill 的教学随机实验。

### R02 · First Proof Second Batch
作者：Mohammed Abouzaid; Nikhil Srivastava; Rachel Ward; Lauren Williams。版本：2026, arXiv:2606.18119v1。
原始来源：https://arxiv.org/html/2606.18119v1
类型：研究级证明评测与专家审稿报告。旧包所记核验位置：§1.3；§5.7–5.9 的叙述性审稿总结（相关段落，不冒称全文）。
旧包概括的观察（本次未复核）：报告中具体出现常规部分冗长、关键论证缺失、引用不支持结论及需要图却无图等问题。
设计主题：详细解释、完整证明、数学审校、图片适用性。这是写作工程选择，不是效果证据。
边界：研究级题目和所测系统的案例，不能据此推算所有课堂讲义错误率；未逐一读全部外链原始审稿附件。

### R03 · Failure Modes of Large Language Models on Research-Level Mathematics: A Taxonomy and an Empirical Characterisation
作者：Arnesh Banerjee; Ayushi Bhattacharjee。版本：2026, arXiv:2606.24902v1。
原始来源：https://arxiv.org/html/2606.24902v1
类型：失败分类与小样本审计。旧包所记核验位置：摘要；§III；§V–VI 的陈述与限制（相关段落，不冒称全文）。
旧包概括的观察（本次未复核）：区分引用捏造、偷渡前提、暗改问题与局部到整体缺口；仅核查引用不能覆盖所有隐含前提。
设计主题：完整证明、隐含命题、数学审校、来源核验。这是写作工程选择，不是效果证据。
边界：实证部分是指定模型的八个一次生成证明，分类还取材于 First Proof；不是独立证明所有模型的普遍失败率。

### R04 · MathTutorBench: A Benchmark for Measuring Open-ended Pedagogical Capabilities of LLM Tutors
作者：Jakub Macina; Nico Daheim; Ido Hakimi; Manu Kapur; Iryna Gurevych; Mrinmaya Sachan。版本：2025, arXiv:2502.18940v2。
原始来源：https://arxiv.org/html/2502.18940v2
类型：对话辅导能力基准。旧包所记核验位置：摘要；§4 的任务定义；§6.1 的文字结论（相关段落，不冒称全文）。
旧包概括的观察（本次未复核）：区分数学能力、理解学生与教学能力；解题表现不能直接替代教学质量评价。
设计主题：例题的教学作用、理解与迁移、真实复核。这是写作工程选择，不是效果证据。
边界：主要是对话辅导任务，不是高等数学长篇讲义评测；苏格拉底辅导要求不能直接移植为省略完整讲义答案。

### R05 · On proof and progress in mathematics
作者：William P. Thurston。版本：1994, arXiv:math/9404236v1。
原始来源：https://arxiv.org/pdf/math/9404236
类型：数学理解与实践论述。旧包所记核验位置：PDF 页序 2–4；重点查看第 3 页渲染（相关段落，不冒称全文）。
旧包概括的观察（本次未复核）：数学理解不等于定义定理证明的产量；同一概念可以有不同而有价值的理解方式。
设计主题：自然连贯表达、范围与进度、章节连贯。这是写作工程选择，不是效果证据。
边界：观点论述，早于现代 LLM；不构成 AI 干预的效果实验，也不要求每个定义固定列多个视角。

### R06 · No one-size-fits-all: a study of prompt techniques and large language models to enhance AI’s mathematics educational quality
作者：Sebastian Schorcht; Fabian Anton Müller; Nils Buchholtz。版本：2026, ZDM 58, 1057–1071; DOI 10.1007/s11858-026-01784-6。
原始来源：https://link.springer.com/article/10.1007/s11858-026-01784-6
类型：模型与提示设计比较实验。旧包所记核验位置：摘要；§1 的质量维度说明（相关段落，不冒称全文）。
旧包概括的观察（本次未复核）：在所测模型、任务和提示方法中，内容、过程与教学维度不由一个选择同时最优地解决。
设计主题：范围与进度、真实复核。这是写作工程选择，不是效果证据。
边界：只在论文的模型、初等数与代数任务及提示范围内成立；不能演绎为任何万能提示词永远不存在。

### R07 · A Scoping Survey of ChatGPT in Mathematics Education
作者：Birgit Pepin; Nils Buchholtz; Ulises Salinas-Hernández。版本：2025, Digital Experiences in Mathematics Education 11, 9–41; DOI 10.1007/s40751-025-00172-1。
原始来源：https://link.springer.com/article/10.1007/s40751-025-00172-1
类型：范围综述。旧包所记核验位置：摘要；Introduction and Research Question（相关段落，不冒称全文）。
旧包概括的观察（本次未复核）：汇总教育用途及不准确、过度依赖等问题，强调适当的人类监督。
设计主题：真实复核、来源核验。这是写作工程选择，不是效果证据。
边界：综述不是一个新的教学对照实验；与 R06 有共同作者，与其他综述可能覆盖相同原始研究。

### R08 · Applications, multidimensional challenges, and innovative pedagogical practices of generative AI in mathematics education: a systematic review 2022–2026
作者：Zengfu Chao; Tianhong Han。版本：2026, Frontiers in Education 11; DOI 10.3389/feduc.2026.1931535。
原始来源：https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2026.1931535/full
类型：系统综述。旧包所记核验位置：摘要；§1；方法与检索范围说明（相关段落，不冒称全文）。
旧包概括的观察（本次未复核）：将技术、教学和实施等问题区分；学习支持的流畅度不能替代推理准确与具体教学目标。
设计主题：例题的教学作用、真实复核、来源核验。这是写作工程选择，不是效果证据。
边界：检索限定英文与两个数据库，并于 2026 年 6 月结束；不把其中所引研究重复当作独立验证本 Skill。

### R09 · GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in Large Language Models
作者：Iman Mirzadeh; Keivan Alizadeh; Hooman Shahrokhi; Oncel Tuzel; Samy Bengio; Mehrdad Farajtabar。版本：2024, arXiv:2410.05229v1。
原始来源：https://arxiv.org/html/2410.05229v1
类型：变体与干扰信息压力测试。旧包所记核验位置：摘要；§4.4；§5 文字结论（相关段落，不冒称全文）。
旧包概括的观察（本次未复核）：题面数值或无关信息变化可暴露所测模型推理的脆弱性，支持设计变体与诱饵测试。
设计主题：数学审校、真实复核。这是写作工程选择，不是效果证据。
边界：是初等文字题和当时模型的实验；不据此宣布所有模型没有推理能力，也不把其结果当讲义教学效果。

### R10 · Let’s Verify Step by Step
作者：Hunter Lightman; Vineet Kosaraju; Yura Burda; Harri Edwards; Bowen Baker; Teddy Lee; Jan Leike; John Schulman; Ilya Sutskever; Karl Cobbe。版本：2023, arXiv:2305.20050v1。
原始来源：https://arxiv.org/html/2305.20050v1
类型：过程监督与结果监督研究。旧包所记核验位置：摘要；§1；方法结构（相关段落，不冒称全文）。
旧包概括的观察（本次未复核）：比较对中间步骤与最终结果反馈的训练方式，提示不能只凭答案正确评价推理。
设计主题：完整证明、真实复核。这是写作工程选择，不是效果证据。
边界：研究训练出的奖励模型和反馈数据，不等于在提示中增加自检就获得同样提升；本包没有训练其模型。

### R11 · Large Language Models Cannot Self-Correct Reasoning Yet
作者：Jie Huang; Xinyun Chen; Swaroop Mishra; Huaixiu Steven Zheng; Adams Wei Yu; Xinying Song; Denny Zhou。版本：2023/2024, arXiv:2310.01798v2。
原始来源：https://arxiv.org/html/2310.01798v2
类型：自纠错与评测设计研究。旧包所记核验位置：摘要；§5；§6 的讨论（相关段落，不冒称全文）。
旧包概括的观察（本次未复核）：无外部反馈的自纠错不能被当作可靠保证；比较流程时还须控制提示信息与生成预算。
设计主题：真实复核、诚实交付。这是写作工程选择，不是效果证据。
边界：针对所测模型和设计，不是对未来模型或所有自纠错方法的不可能性定理。

### R12 · Reasoning and proof in mathematics education: a systematic literature review
作者：Mary-Jane Lessing; Ugorji I. Ogbonnaya。版本：在线 2025-12-11；2026 卷 5, Article 31; DOI 10.1007/s44217-025-01016-1。
原始来源：https://link.springer.com/article/10.1007/s44217-025-01016-1
类型：证明教学系统综述。旧包所记核验位置：摘要；§1 的研究问题（相关段落，不冒称全文）。
旧包概括的观察（本次未复核）：关注学习者论证困难、证明理解与教学干预，而不是只看最终命题真伪。
设计主题：自然连贯表达、不擅自改题、真实复核。这是写作工程选择，不是效果证据。
边界：研究对象分布并不覆盖所有大学数学；本包只借鉴需明确论据与理解障碍的方向。

## GitHub 与格式参考

下面是工程参考，不计入学术来源数量。没有把它们原封不动复制为新的 Skill，也没有假设有许可证即可证明质量。

**E01 · Agent Skills specification**
https://agentskills.io/specification
所读位置：SKILL.md frontmatter / directory structure / progressive disclosure。
采纳：单入口、清楚触发描述和按需读取资源。不照搬：格式合规不等于教学有效或通用平台已安装。
未取得固定版本哈希，记录的是本次访问版本；后续使用需重新核验。

**E02 · anthropics/skills — skill-creator**
https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md
所读位置：SKILL.md lines 1–150。
采纳：真实用例、测试与迭代、主文件节制。不照搬：没有工具时不模仿实际并行基线实验。
已返回的文件 blob SHA：`65b3a402dbd09b8e83f9d637c6b553875189085c`。

**E03 · Wholiver/Math.Skill**
https://github.com/Wholiver/Math.Skill/blob/main/SKILL.md
所读位置：Mathematical Reasoning Workflow / Verification Engine。
采纳：定义域、边界、反例、独立方法检查作为可用手段。不照搬：不要求每个算式逐步说明；不把任何两种检查当必然数学证明；不默认用反向推演证明原推论。
未取得固定版本哈希，记录的是本次访问版本；后续使用需重新核验。

**E04 · killerfirst/math-textbook-to-skill**
https://github.com/killerfirst/math-textbook-to-skill/blob/master/SKILL.md
所读位置：SKILL.md lines 1–180。
采纳：依赖关系、证明路径、去重、边界与诱饵测试。不照搬：不强制七个子代理、十个定理、固定通过比例或逐阶段等待确认。
已返回的文件 blob SHA：`392e1c9215a49b00b7c0519704871c371e60fc60`。

**E05 · optsuite/MathResearchPrompts**
https://github.com/optsuite/MathResearchPrompts/blob/main/prompt_templates.md
所读位置：prompt_templates.md §§3–7。
采纳：证明义务、假设显式化、证明/反例双向核查、数值只是筛查。不照搬：不把研究提示的逐行证明和固定候选数量搬成整本教材的版式。
已返回的文件 blob SHA：`12968fc0d163d13ac387ce75b1d25e3d9fe41d5b`。

## 从陶哲轩文末继续追踪的边界

已核对该文参考文献区的 23 个条目，但**书目核对不是 23 篇原件都已读完**。直接用于本包且另读相关正文的是其 [6]（本表 R02）与 [21]（R05）；文章自身为 R01。其余条目不能仅因被陶哲轩引用就视为已核验的支持证据。

| 原文编号 | 主题/性质 | 本次处理 |
|---|---|---|
| [1], [10], [12] | 数学形式化、Lean、mathlib | 书目层面辨识；本包不声称运行了形式化证明 |
| [2], [18], [19] | 数学价值与工具箱论述 | 书目层面辨识；不增加“独立团队”数量 |
| [3], [17] | Bourgain 数学论文与纪念文章 | 不是讲义质量实验，未作为直接证据 |
| [4], [5], [7], [15], [20] | 数学传播/题库/评测/数据库项目 | 工程背景，未当作论文效果证据 |
| [8], [14] | 数学基础历史文献 | 与当前缺陷修复无直接验证关系 |
| [9], [16] | 指标与评价背景 | 不借它们推出本 Skill 的量化效果 |
| [11], [22], [23] | 声明、开放科学与数据原则 | 书目层面辨识；不冒充法律意见或教学实验 |
| [13] | 数学实践研究 | 未取得用于本包结论的原文核验，暂不作承重来源 |

## 未纳入硬证据的旧引用

旧版提过 seductive details、worked examples、自我解释、expertise reversal 与解释深度错觉等经典研究。本轮部分出版页面返回访问限制或没有可读正文，因此不把旧版转述冒充新核验，不用其效应量或强结论背书。其合理设计方向可作为用户偏好或待验证假设保留，例如“简单例子不一定无用”，而不是写成“论文已证明此 Skill 最好”。

没有转载论文正文、受限教材或第三方图片。引用原始链接不代表作者认可本包。
