# 数值分析导论: MIT 18.330 中文整理本

79页 · [下载PDF](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/numerical-analysis/dist/main.pdf) · [源码ZIP](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/numerical-analysis/dist/source.zip) · [版本历史](https://github.com/xhc144/mit-ocw-notes/commits/main/subjects/numerical-analysis/dist/main.pdf)

Laurent Demanet 原讲义, MIT 18.330 Introduction to Numerical Analysis, Spring 2012. 中文整理版本: 2026-10-08.

主文档只有一册: `main.tex` 生成 `main.pdf`. 保留已交付的七章正文和固定模板, 在卷首增补课程大纲与课历, 在正文后收入八份作业的完整中文题面与解答. 各章节没有作为单独最终 PDF 交付.

## 范围

七章对应官方讲义目录的第1–25讲, 原件共99页（含每份末尾的OCW署名页）. 原件未写出的证明、图及函数公式, 保留明确说明; 新增证明、数学条件修订及补图都作整理标记. 大纲列出的最小二乘与主成分分析没有独立来源讲义, 不冒称已补全.

新增PS1–PS8共33道原编号题、68个末级单元, 含附加问. 按原字母或bullet计数, 无子问的题记一单元; PS8第4题末条同时含微分与求积, 两项均已作答. PS8原标“Not due”, 不需提交, 无分值. 逐题原号、分值、子问和来源哈希冻结在`assessment-inventory.json`.

**全部新增解答均为AI编写, 不是MIT官方答案.** 官方Assignments没有链接答案或公开考试卷, 本册不猜补考试. 原题日期、原印星期及重复子问编号保留并说明; 课程大纲仅有每周两次、每次1.5小时的安排和讲义讲次范围, 不制造逐日课历或考试时间.

完整逐章覆盖见`chapter-coverage.json`, 修订与真实检查范围见`QA.md`及`qa/`. 七章原件见`source-manifest.json`, 八份作业原件见`assessment-sources.json`, 网页元数据见`course-sources.json`. 所有原件均单独归档在`../../sources/18.330-spring-2012/`, 不在源码ZIP中重复打包.

## 编译

使用 XeLaTeX, 需 TeX Live 中的 ctex/Fandol, CM Unicode 字体, amsmath/amsthm, TikZ/PGFPlots, hyperref 等宏包. 从本目录运行:

    xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
    xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex

固定王者适配类嵌在 main.tex 的 filecontents 中, 编译会自动生成. 不修改锁定类来迁就页面, 不需要外部图片截图, 不需要 shell escape. 不捆绑字体文件.

如需重跑数值实验, 安装Python 3及NumPy、SciPy、Matplotlib、mpmath, 运行`python3 experiments/run_experiments.py`. 脚本实际生成CSV、`results.json`及七张矢量PDF图; 普通LaTeX重编直接使用已有矢量图, 不依赖Python. 题中明确要求MATLAB的部分同时保留相应核心代码; 实际数值验算使用Python.

## 文件

- main.tex: 主源码与固定版式
- chapters/: 七章正文
- course-info.tex: 教师、安排、先修、考核、大纲与作业课历
- assessments/: 八份作业的完整中文题面与AI解答
- assessment-inventory.json: 33题、68末级单元的冻结清单
- experiments/: 实际运行的数值脚本、结果及CSV
- figures/runge.tex: 可编辑的 Runge 数值演示图
- figures/assessments/: 从脚本生成的矢量图
- dist/main.pdf: 一册正式 PDF
- dist/source.zip: PDF、完整可编辑源码及来源/检查说明
- LICENSE.md 与 licenses/: 署名、CC BY-NC-SA 4.0 许可链接及条款快照
- QA.md: 覆盖和检查边界
- qa/: 独立复审、逐页视觉检查、目录链接、干净ZIP重编与文件哈希证据

## 许可

原材料: Massachusetts Institute of Technology, MIT OpenCourseWare, Laurent Demanet. 默认 CC BY-NC-SA 4.0 International; 原件中的个别权利声明仍优先. 中文翻译、补图与改编使用相同许可, 仅非商业使用并相同方式共享. 不表示 MIT、原作者或参考书作者认可此整理本. 外部参考书仅作为原稿书目或核实的出版信息, 没有复制整书或第三方图版.
