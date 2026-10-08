# 课程作业与考试覆盖清单

本轮在原66页、13章讲义上增补课程资料和题解。原交付保留在提交 `cb7e27ae7a1cff846ab46871d7ab81bdc59e8132`；原13章正文仅增加两处例题交叉引用标签及一处系数与全1向量之间的薄空格。

计数以原题内容为单位。主问题是原来的 Problem / Question，不是文件数；第一层作答块按原 a、b 或 1、2 编号计，未分问的主问题计一个。更深的嵌套要求另列，不混入308这个数。

| 课程与原版本 | 主问题 | 第一层作答块 | 处理 |
|---|---:|---:|---|
| 6.253 Spring 2010 五组作业 | 27 | 48 | 全部中文题面与解答 |
| 6.253 Spring 2010 / 2012 两份期中卷 | 4 | 25 | 逐年保留；2012 Q2(a)独立补解 |
| 15.053 Spring 2013 作业1–6，含PS1/2两组版本 | 24 | 104 | 前两题去重，第三题保留版本差异 |
| 15.053 十次Recitations | 36 | 112 | 保留原编号、数据及明确的原件缺陷 |
| 15.053 期中2综合练习 Practical Problem Set | 6 | 19 | 原重复题号保留映射 |
| 合计 | 97 | 308 | 数学与逐项覆盖审读单独记录 |

逐题来源、子问编号、页码、解答来源见 [assessment-coverage.json](assessment-coverage.json)。原件链接、实际格式与SHA-256见 [sources/assessment-resources.json](sources/assessment-resources.json)。每题在PDF中有可点击的编号。官方解答重构、AI补充证明、AI独立解答及原解错误均在题解中区分。

课程库存来自 [6.253作业](https://ocw.mit.edu/courses/6-253-convex-analysis-and-optimization-spring-2012/pages/assignments/)、[考试](https://ocw.mit.edu/courses/6-253-convex-analysis-and-optimization-spring-2012/pages/exams/)，以及 [15.053作业](https://ocw.mit.edu/courses/15-053-optimization-methods-in-management-science-spring-2013/pages/assignments/)、[习题课](https://ocw.mit.edu/courses/15-053-optimization-methods-in-management-science-spring-2013/pages/recitations/)和[复习资料](https://ocw.mit.edu/courses/15-053-optimization-methods-in-management-science-spring-2013/pages/study-materials/)。两门原课的课历独立列于书前，没有合成新的课表。

## 原件缺口及处理

- 15.053的实际两份期中卷和七份小测题面未出现在已核官方库存。三份Quiz Guides是考试范围，已收入课程说明，不当成试卷。期中2综合练习不是实际期中卷。
- 6.253的五组作业题头实际为2010，尽管资源页面属于2012课程。2012期中Q2(a)原解为“To be added”，本稿提供标明来源的AI独立解答。
- PS1/2的组别网页标题与个别原题头不一致，PS5截止日期原写“Thursday April 2th, 2013”，星期与日期矛盾；不据此猜造新日期。
- Rec9原题号1、3、3、5及综合练习的重复题号在书中映射保留。Rec9最后选择题按实际印刷的`2m`审读，指出官方选择与其反例的矛盾。
- Rec10原件已删除的版权图片不恢复。涉及外书的PS1组1、PS2、PS4、Rec4及综合练习背景模型仅重述数学数据、模型和全部作答要求，不翻译外书故事段落；12份含这类行文的原题与解答只留链接和哈希，不随仓库或ZIP分发。6.253出版社授权的概念摘要同样仅保留链接和哈希。

## 实际计算与表格读取

九份工作簿的30张表均已实际读取，不以文件名判断题目内容。PS3 `ps3_sol.xls`实际为XLSX，PS6题目工作簿实际为XLSB；分别用openpyxl和pyxlsb读取，传统XLS用xlrd读取，提取单元格保存在`*.cells.json`。当前技能目录未提供可调用的专用spreadsheet skill，故使用上述实际解析，并未声称调用不存在的技能。

可复现计算运行：

```bash
python tools/audit_convex_inventory.py
python tools/audit_lp_homework.py
python tools/audit_lp_recitations.py
python tools/check_coverage.py
```

LP、整数枚举、表枢轴及原/对偶证书报告在`review/`中。数值检查不能代替数学证明；独立审读报告另列稿件哈希与检查范围。原66页的逐讲覆盖继续由 [COVERAGE.md](COVERAGE.md) 和 [coverage.json](coverage.json)记录。
