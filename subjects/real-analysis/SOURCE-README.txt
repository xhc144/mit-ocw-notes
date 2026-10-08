测度与积分：MIT 18.125 中文重编本源码

解压进入 real-analysis 目录，运行 bash tools/build.sh。
需要 XeLaTeX、ctex/xeCJK、Fandol、CM Unicode，以及 Python3、PyMuPDF、Pillow。
默认 TEXMFHOME=/workspace/.local/texmf，XDG_CACHE_HOME=/workspace/.cache；其他机器可自行设置。
依赖缺失时，可运行固定哈希校验的 tools/bootstrap_tex.py，指定可写的 --texmf-dir 与 --cache-dir，再设置 TEXMFHOME 后编译。
构建使用本包内的固定模板验证器；成功输出 build/main.pdf。

本包仅含中文编译输入、所需验证及依赖工具、署名许可；不含字体、英文原PDF、官方网页、QA记录或构建缓存。
英文原PDF及官方课程资料保存在项目仓库 sources/real-analysis/；查核证据在 subjects/real-analysis/qa/。

正文复用原72页版的九章数学内容、来源对照、29个例题与33道编者练习。新增卷首课程参考、官方课历、三组Rudin题号安排。
官方原书题面与解答未纳入。题号索引不是官方作业题解；33道编者练习不改称官方题。

Jeff Viaclovsky 讲授，Ethan Brown 原讲义排录。
MIT OpenCourseWare, 18.125 Measure and Integration, Fall 2003。
官方课程：https://ocw.mit.edu/courses/18-125-measure-and-integration-fall-2003/
原课程与中文改编遵循 CC BY-NC-SA 4.0，单独声明优先。详见 LICENSE.md。
排版工具的来源见 vendor/math-latex-typesetting/SOURCE.json；字体仅为外部运行依赖，不分发。
