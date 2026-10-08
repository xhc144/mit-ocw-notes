# 数值分析导论: MIT 18.330 中文整理本

59页 · [下载PDF](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/numerical-analysis/dist/main.pdf) · [源码ZIP](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/numerical-analysis/dist/source.zip) · [版本历史](https://github.com/xhc144/mit-ocw-notes/commits/main/subjects/numerical-analysis/dist/main.pdf)

Laurent Demanet 原讲义, MIT 18.330 Introduction to Numerical Analysis, Spring 2012. 中文整理版本: 2026-10-08.

主文档只有一册: `main.tex` 生成 `main.pdf`. 七章正文通过 `chapters/chapter01.tex` 至 `chapter07.tex` 输入; 图形使用可编辑 TikZ/PGFPlots. 各章节没有作为单独最终 PDF 交付.

## 范围

完整对应 MIT OCW 官方讲义目录中的七章, 共 99 个原 PDF 页, 包括每份原件末尾的 OCW 来源声明. 目录把这些资料对应到第1–25讲. 本册并不声称提供原课程大纲列出的全部其他主题或独立作业集. 原件未写出的证明、图及函数公式, 在正文中保留明确说明; 新增证明、数学条件修订及补图都作整理标记.

完整逐章覆盖见 `chapter-coverage.json`, 重点数学修订及真实检查范围见 `QA.md`. 七份未改动原件的官方直链、页数及 SHA-256 见 `source-manifest.json`. 原件单独归档, 不在源码 ZIP 中重复打包.

## 编译

使用 XeLaTeX, 需 TeX Live 中的 ctex/Fandol, CM Unicode 字体, amsmath/amsthm, TikZ/PGFPlots, hyperref 等宏包. 从本目录运行:

    xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
    xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex

固定王者适配类嵌在 main.tex 的 filecontents 中, 编译会自动生成. 不修改锁定类来迁就页面, 不需要外部图片截图, 不需要 shell escape. 不捆绑字体文件.

## 文件

- main.tex: 主源码与固定版式
- chapters/: 七章正文
- figures/runge.tex: 可编辑的 Runge 数值演示图
- dist/main.pdf: 一册正式 PDF
- dist/source.zip: PDF、完整可编辑源码及来源/检查说明
- LICENSE.md 与 licenses/: 署名、CC BY-NC-SA 4.0 许可链接及条款快照
- QA.md: 覆盖和检查边界

## 许可

原材料: Massachusetts Institute of Technology, MIT OpenCourseWare, Laurent Demanet. 默认 CC BY-NC-SA 4.0 International; 原件中的个别权利声明仍优先. 中文翻译、补图与改编使用相同许可, 仅非商业使用并相同方式共享. 不表示 MIT、原作者或参考书作者认可此整理本. 外部参考书仅作为原稿书目或核实的出版信息, 没有复制整书或第三方图版.
