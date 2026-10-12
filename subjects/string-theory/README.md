# 弦论与全息对偶

本册为 MIT OCW 公开材料的中文主题讲义, 十个理论章和 35 道入选原编号问题的完整题面及解答. 正文、题面、推导和自绘图均为可编辑 LaTeX; 不用原PDF整页背景. 它是冻结范围的专题卷, 不代表相关课程所有作业、考试或高阶研究内容全译.

- [中文主PDF](dist/string-theory-zh.pdf)
- [可编译源码ZIP](dist/string-theory-source.zip)
- [覆盖范围、未选题及高阶边界](coverage.md)
- [冻结题目清单](sources/coverage-frozen.json)
- [逐文件官方来源、页数、SHA-256与许可边界](sources/resource-inventory.json)
- [核验记录](qa/review.md)

## 编译

解压源码包后, 用已安装 ctex、Fandol、Computer Modern Unicode、TikZ/PGFPlots 的 TeX Live 运行:

```sh
python3 scripts/build.py
```

脚本严格比较仓库批准模板的锁定类, 在新临时目录以 XeLaTeX 三次编译, 禁用 shell escape, 输出到 `build/main.pdf`. 字体由系统安装, 源码包不分发字体. `python3 scripts/numerical_checks.py` 需要 numpy、scipy, 可重现随包数值表; 编译本身只读取已给的CSV, 不需要联网或科学计算库.

本环境复现使用已存在的 `/workspace/.local/texmf`, 因系统没有全局ctex, 编译命令显式设置 `TEXMFHOME=/workspace/.local/texmf` 并使用 `/tmp` 的字体缓存. 正常已完整安装TeX Live的机器无需该路径.

## 署名与许可

课程教师、学生笔记署名及版本差异见 `course-info.tex`. 中文翻译、主题重组、独立推导、题解补写与自绘图采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). 保留署名、非商业、相同方式共享, 不暗示MIT或作者认可. 原件只保留链接与校验记录; 第三方图像、书本题面、未经确认的数据及字体不打包. 完整边界见 [LICENSE.md](LICENSE.md).
