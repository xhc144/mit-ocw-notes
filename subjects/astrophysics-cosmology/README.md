# 天体物理与宇宙学

本卷是依据实际可获取的 MIT OpenCourseWare 材料重新编写的**中文 LaTeX 合订讲义**，合订 8.901 *Astrophysics I*（Spring 2006）、8.902 *Astrophysics II*（Fall 2023）和 8.286 *The Early Universe*（Fall 2013）。正文按恒星物理、星系动力学、宇宙学及观测的知识依赖编排，包含推导、条件明确的题解、原创示意图与可复核数值实验。已有的广义相对论卷是本卷的前置，不重复其完整课程。核定页数与校验哈希见发布记录。

8.901 的 47 组公开题有 43 组自足译解、4 组标明外部依赖；另 8 组只有受限教材题号，未编造题面。8.902 的 21 份分讲均有中文教学对应，20 个公开作业和期中原编号题组已解；另收录五页数值项目的公开要求和可验证算法，课堂 Canvas 配置包及快照未取得。8.286 的十份作业共 49 个原编号映射为 48 道独立题，三次正式测验 12 组均入卷；53 组复习题中 52 组已详解、1 组与测验完全重复并精确回指。正式测验与作业之间还有三处原题重复，因此不能把各栏简单相加称为独立题数。具体原编号和缺口见覆盖表。

- [中文主PDF](dist/astrophysics-cosmology-zh.pdf)
- [可编译源码ZIP](dist/astrophysics-cosmology-source.zip)
- [覆盖范围、未选题及高阶边界](coverage.md)
- [冻结题目清单](sources/coverage-frozen.json)
- [逐文件官方来源、页数、SHA-256与许可边界](sources/resource-inventory.json)
- [逐讲对应表](qa/lecture-coverage.csv)、[逐题对应表](qa/assessment-coverage.csv)
- [最终核验记录](qa/final-review.md)

## 编译

解压源码包后，用已安装 ctex、Fandol、Computer Modern Unicode、TikZ/PGFPlots 的 TeX Live 运行:

```sh
python3 scripts/build.py
```

脚本严格比较仓库批准模板的锁定类，在新临时目录以 XeLaTeX 三次编译，禁用 shell escape，输出到 `build/main.pdf`。字体由系统安装，源码包不分发字体。`python3 scripts/numerical_checks.py` 需要 numpy、scipy，可复现随包数值表；编译本身只读取已给的 CSV，不需要联网或科学计算库。

本环境复现使用已存在的 `/workspace/.local/texmf`，因系统没有全局 ctex，编译命令显式设置 `TEXMFHOME=/workspace/.local/texmf` 并使用 `/tmp` 的字体缓存。正常已完整安装 TeX Live 的机器无需该路径。

## 署名与许可

课程教师、学生笔记署名及版本差异见 `course-info.tex`。中文翻译、主题重组、独立推导、题解补写与自绘图采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)。保留署名、非商业、相同方式共享，不暗示 MIT 或作者认可。原件只保留链接与校验记录；第三方图像、书本题面、未经确认的数据及字体不打包。官方材料没有公开的整套答案不冒称“官方解答”；其余中文推导为独立补写。完整边界见 [LICENSE.md](LICENSE.md)。
