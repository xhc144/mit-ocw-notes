# 固定版式核对表

权威文件为 `templates/wangzhe_baiti_style.tex` 的 `WZ-LOCKED-CLASS` 区段；不是官方 ElegantBook 完整类。源头是用户提供的王者百题原稿复刻适配类，v4 继续使用此固定版式；锁定类内容与输入 v3 相同。

锁定：`book` 的 `10pt,letterpaper,oneside`；纸张 612×792bp；`ctex` 使用 Fandol；西文 `cmunrm/cmunbx/cmunti/cmunbi`；页眉 FandolKai；左右各 20mm，上 95.04bp，下 20mm；`headheight=12pt,headsep=25pt,footskip=30pt`；正文 `setstretch=1.6,parindent=2em,parskip=0pt`。

主结构色 `#880E4F`，例题色 `#9C27B0`；目录及内部链接统一使用主结构色，不再使用旧版纯红色。双侧页眉、居中页码，页眉线 0.4pt。目录深度为 1，只收章和节。章标题 14.4/20，节标题 12/17；不改成默认 `book` 巨大章标题。

行间公式：上/下间距均为 `4pt plus 1pt minus 1pt`；短显示上方 2pt、下方 3pt。保留 `allowdisplaybreaks[2]`、`emergencystretch=2em`、孤行控制和 `raggedbottom`。公式编号按章。

章/节使用 `originalchapter/originalsection`。题目、引理、证明等按 `ENVIRONMENTS.md` 使用预设环境。没有手写编号。完整证明自动空心方框；定理/题目本身不加结尾方框。

书名、作者、日期是内容槽；未提供作者/日期就留空，模板不输出空行。不自动署名模型或虚构作者。不自动添加封面或目录；是否需要由用户或内容作者决定。前言不编号，正文首章从 1 开始。参考文献不占数学章号。

禁止框、卡片、灰底、侧边条、图标和水印。禁止正文再定义 theorem/proof 等样式或用另一个主题覆盖本模板。允许为数学内容增加记号宏、非冲突功能环境或必要绘图/表格包，不得覆盖锁定环境与版式。

`check_style.py` 比对完整锁定区并检查项目中已解析的内容文件。注释和逐字代码不作为正在执行的排版命令。新版没有“只允许 original 四个命令”的规则；使用语义环境是必需的。
