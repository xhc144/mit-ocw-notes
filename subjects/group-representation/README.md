# 有限群表示论：MIT 18.712 中文重构本

本书以 MIT OpenCourseWare 18.712（Fall 2010）公开旧讲义为依据，采用仓库固定王者版式。定义、定理、证明、例题、题面及解答均用简体中文重写。旧讲义首页日期为 2011-02-01，完整 PDF 为 109 页；作者为 Pavel Etingof、Oleg Golberg、Sebastian Hensel、Tiankai Liu、Alex Schwendner、Dmitry Vaintrob、Elena Yudovina。

前九章形成有限群复表示的本科主线：不可约表示、Schur 引理、Maschke 定理、特征标及矩阵系数正交、正则表示、群代数分块、经典特征标表、张量与对偶、诱导与限制、Frobenius 互反、Mackey 分解和 Frobenius–Schur 指标。循环群、S₃、S₄、二面体群、四元数群和 A₄ 贯穿正文。

书前保留官方课程信息、先修要求、12 周阅读进度及考核办法。同一主 PDF 收录官网 11 次作业的全部 52 道原题（51 必做、1 选做）及 4 道期末题，保留课程年份、作业次序和原题号。所有解答为 AI 辅助独立编写并经数学复核的编者解答；官方页面未提供独立 Solutions 文件。源文条件遗漏和印刷错误在题解中注明。课程题目所需的结合代数、李代数、Young 模、箭图、根格和有限一般线性群只作局部展开。

未系统覆盖旧讲义全部范畴论、一般有限维代数的根基与投射覆盖、Gabriel 定理全套证明、完整 Young 表与 Schur–Weyl 分类、Artin 定理、Frobenius 整除性及 Burnside 可解性。旧讲义中未列为官方作业的练习也未全部收录。1.58 明示复数版本与特征 2 反例，不宣称分类其他正特征版本。

## 文件

以下为仓库目录。源码 ZIP 只包含中文稿、构建脚本、说明、许可及题目定位清单；来源档案与审核记录留在仓库。

- `dist/main.pdf`：中文主 PDF。
- `dist/group-representation-source.zip`：可在独立目录重编的中文源码。
- `main.tex`、`chapters/`：可编辑主源，固定适配类直接嵌入主文件。
- `source-manifest.json`：官方逐文件页数、署名、许可、例外和 SHA-256 核查。
- `assignments-manifest.json`：全部题号、源页与中文文件定位。
- `qa/`：独立数学审读、实际视觉和构建验证记录。

## 编译

需要 XeLaTeX、CTeX、Fandol 字体、Computer Modern Unicode OTF 字体及常见的 AMS、TikZ、booktabs、longtable、hyperref 等 TeX 宏包。完整 TeX Live 安装可提供这些依赖；源码包不分发字体。解压后在本目录执行：

```bash
bash build.sh
```

脚本连续编译三次，PDF 写入 `dist/main.pdf`。无需仓库其他学科、英文原 PDF、图片缓存或网络下载。若使用单独的 TeX 用户树，可在命令前设置相应的 `TEXMFHOME`；本项目验证环境为 `TEXMFHOME=/workspace/.local/texmf`，该路径只是本次环境配置，源码不依赖此绝对路径。

## 来源与许可

官方 [讲义目录](https://ocw.mit.edu/courses/18-712-introduction-to-representation-theory-fall-2010/pages/lecture-notes/)、[旧版 PDF](https://ocw.mit.edu/courses/18-712-introduction-to-representation-theory-fall-2010/24d8b3fa2ce48e48ee6c2d8d5e3562f6_MIT18_712F10_replect.pdf)、[作业与期末](https://ocw.mit.edu/courses/18-712-introduction-to-representation-theory-fall-2010/pages/assignments/)。

英文原件只在 `sources/group-representation/` 归档，没有嵌入中文 PDF，也不收入中文源码 ZIP。旧版分章 PDF 与完整旧 PDF 对照后去重；保留完整旧 PDF 和独立期末 PDF。官方另链的 2016 年 AMS 出版书明示不得上传至非作者网站，未下载、归档或用作本书改编源。

本中文改编依 CC BY-NC-SA 4.0 非商业共享。翻译、重排、补证、编者练习和自绘图均为改动，不表示 MIT 或原作者认可。逐文件单独权利标记优先，见 `LICENSE.md` 与来源清单。
