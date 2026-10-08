# 凸分析与最优化

126页 · [完整PDF](dist/main.pdf) · [可编辑LaTeX源码ZIP](dist/source.zip) · [交付哈希清单](release-manifest.json) · [版本历史](https://github.com/xhc144/mit-ocw-notes/commits/main/subjects/optimization/dist/main.pdf)

以Dimitri P. Bertsekas的MIT 6.253 Spring 2012完整讲义为主源，保留原13章正文，并增补两门原课独立的课程大纲、课历、教师、时间、先修及考核说明。15.053采用James Orlin与Ebrahim Nasrabadi的Spring 2013资源。新增97道主问题、308个第一层作答块的完整中文题面与解答，均收入同册；更深的嵌套任务另列，不混算成308。

| 增补资料 | 主问题 | 第一层块 |
|---|---:|---:|
| 6.253五组2010作业 | 27 | 48 |
| 6.253两份2010/2012期中卷 | 4 | 25 |
| 15.053八份作业版本，按内容去重 | 24 | 104 |
| 15.053十次习题课 | 36 | 112 |
| 15.053期中2综合练习 | 6 | 19 |

题后明确区分官方解答重构、AI补解及原解错漏。2012期中Q2(a)原解“To be added”由AI独立补解。PS1/2共同题只写一次，各组不同的第三题均保留。PS3等表格题已实际读取九份工作簿的30张表，数值、枢轴、枚举及对偶证书由可运行脚本复核。

原66页版本仍可从[原PDF](https://raw.githubusercontent.com/xhc144/mit-ocw-notes/cb7e27ae7a1cff846ab46871d7ab81bdc59e8132/subjects/optimization/dist/main.pdf)及[原源码ZIP](https://raw.githubusercontent.com/xhc144/mit-ocw-notes/cb7e27ae7a1cff846ab46871d7ab81bdc59e8132/subjects/optimization/dist/source.zip)取得。原正文只增加两处对应例题的交叉引用标签及一处公式薄空格；根README未在本轮修改。

## 覆盖与来源

- 原25讲数学正文：[COVERAGE.md](COVERAGE.md)、[coverage.json](coverage.json)，原来源元数据[source-metadata.json](source-metadata.json)继续记录66页基线。
- 新增逐题与子问清单：[ASSESSMENTS.md](ASSESSMENTS.md)、[assessment-coverage.json](assessment-coverage.json)。
- 原件URL、实际格式、页数与哈希：[sources/assessment-resources.json](sources/assessment-resources.json)。
- 独立数学审读、实际计算、构建与视觉检查：[QA.md](QA.md)、[review/](review/)。同模型独立代理审读不是外部专家认证。

15.053实际期中卷及小测试卷未出现在已核官方库存，不能从三份复习指南反造试卷。综合练习不是正式期中卷。原版本年份、重复题号和日期矛盾保留说明。Rec10已删除的版权图片不恢复；涉及外书背景的作业、Rec4和综合练习模型独立重述数学数据和任务，不重译故事段落；含这类叙事的原题与解答仅保留链接与哈希。更多边界见覆盖清单。

## 许可

署名MIT OpenCourseWare及原课程教师。中文改编按CC BY-NC-SA 4.0提供，MIT及教师未为改编背书。原件的出版社、外书和图像权利例外逐项保留，不因OCW页面而自动获得转授权。自行绘制的数学图为TikZ；原件删除的图片不补回。详见[LICENSE.md](LICENSE.md)。

## 编译与复现

源码入口[main.tex](main.tex)，原章在`chapters/`，增补题解在`assessments/`。需要XeLaTeX、ctex/Fandol、CM Unicode字体及常规TeX Live宏包，包括amsmath、amsthm、hyperref、TikZ、longtable和booktabs。不捆绑字体或原件PDF。干净解包后运行：

```bash
bash build.sh
```

建模与精确计算脚本需要Python 3及numpy、scipy、sympy，使用随包的实际单元格数据：

```bash
python tools/audit_lp_homework.py
python tools/audit_lp_recitations.py
```

在完整仓库检验逐题覆盖与原13章字节保留。库存复核脚本需要先按来源清单取回本地核对原件；仅链接的文件不随仓库和ZIP分发：

```bash
python tools/audit_convex_inventory.py
python tools/freeze_coverage.py
python tools/check_coverage.py
```

`acquire_assessments.py`用于重新获取官方原件与读取表格，额外需要xlrd、openpyxl及pyxlsb；同哈希资源保留已有人工权利标记，新增或变更字节的资源标为待重新审查。当前技能目录没有专用spreadsheet skill，表格由上述解析器实际读取，并未声称调用不存在的技能。

自动排版验证与数学证明、实际视觉检查分开记录。检查结果说明已核范围，不是全书零数学错误的保证。
