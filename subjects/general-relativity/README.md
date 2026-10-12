# 广义相对论

[中文合订 PDF](dist/general-relativity-zh.pdf) · [可独立重建源码 ZIP](dist/general-relativity-source.zip)

以 Scott A. Hughes 的 [MIT OCW 8.962，Spring 2020](https://ocw.mit.edu/courses/8-962-general-relativity-spring-2020/) 为主来源，按公开 Lecture Guide 第 1–25 讲的理论主题重编。正文从狭义相对论、四矢量和张量开始，补齐流形、度规、联络与曲率的先修桥梁，进入爱因斯坦方程、线性引力与引力波、宇宙学、紧致天体、黑洞及高级求解方法；不要求读者预先学过微分几何。第 24、25 讲未录制 2020 年课堂视频，公开 Guide 有文字概要，本卷以此为范围补充推导，不宣称还原未公开的完整课堂。

本轮冻结 1 份 20 页 Lecture Guide、11 套作业、4 份局部提示，共 16 份 PDF、75 原件页，以及官方 PS10.nb 数值计算示例和 6 个课程页面。**门户标为 Spring 2020，11 套公开作业实际均为 Spring 2006；2020 年版作业不可获。** 55 个原作业编号中，51 道大题具有可获得或可由官方提示恢复的题面并给出本稿独立解答。PS7 第 3 题的拉氏量与变分要求由官方提示恢复；PS3.5、PS3.6、PS7.4、PS7.5 仅有 Carroll 教材题号，题面未取得，四项缺口如实列出。原大纲明确无考试，所以没有伪造期中或期末卷。题数不把小问、正文例题或缺题编号算作已完成原题。

官方四份提示不是完整解答集。本卷的中文推导和作业解答由中文重编贡献者在 AI 辅助下独立编写，来源处区分公开题面、提示所恢复的要求和独立解答。数学校勘在对应题解中标明，保留原题的条件与记号边界。图用原生 TikZ 自绘；不捆绑商业教材、课堂视频、照片或许可未单独确认的外链手写笔记。PS10.nb 保留为公开的辅助原件，静态审阅后归档，讲义构建不依赖 Mathematica，也不把它称作官方题解。

成稿为 **109 页**。XeLaTeX 三轮收敛，159 个内部链接与 89 个书签已解析；逐页视觉及修订复审记录见 [final-visual-review.json](qa/final-visual-review.json)。数学检查为有来源定位的抽检与独立推导复核，不能代替读者或专家的完整数学审稿。

从本目录构建：

```sh
python tools/build.py
```

需 Python 3、XeLaTeX、仓库版式依赖和系统中文字体。源码 ZIP 保留原课程署名、许可、来源快照、原生 TeX 与 TikZ，并排除字体及临时构建垃圾。完整讲义的编译、公式、视觉、目录链接和 ZIP 重建验收记录由本目录 [qa/](qa/) 随交付保留；原件许可审查见 [source-audit.json](qa/source-audit.json)。

[来源与真实缺口](SOURCES.md) · [冻结清单](sources/scope.json) · [下载地址与 SHA256](sources/manifest.json) · [署名与许可](LICENSE-NOTICE.md)

本卷只覆盖上述公开资料范围，不代表 MIT 的全部广义相对论课程或全部历史学期。MIT 原材料与本卷中文改编按 CC BY-NC-SA 4.0 分发；本稿非官方，MIT 未审核或认可。
