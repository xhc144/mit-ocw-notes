# 曲线与曲面的微分几何

依据 Paul Seidel 的 MIT OpenCourseWare **18.950 Differential Geometry, Fall 2008** 四份实际公开讲义，重构本科欧氏曲线与二维曲面主线，并附10份官方作业的中文题面和独立解答。简体中文原生 LaTeX，使用本仓库 `subjects/probability/main.tex` 的锁定王者模板。

[阅读 PDF](differential-geometry.pdf) · [下载自足源码 ZIP](differential-geometry-source.zip) · [官方讲义目录](https://ocw.mit.edu/courses/18-950-differential-geometry-fall-2008/pages/lecture-notes/) · [来源及逐文件校验](source-manifest.json)

全册 **71 个物理页**。保留原12章专题与36题完整解答，新增原课程信息、教学大纲、公开讲次、先修和考核，以及10份官方作业。可点击目录、实际来源对应表和参考文献齐全。原课程四份 PDF 共60个物理页，其来源页和作者、年份信息保留于 `sources/differential-geometry/`。

内容包括弧长与平面曲率、闭曲线转角与四顶点、空间 Frenet 标架与挠率、正则曲面与面积、第一和第二基本形式、形算子及主曲率、旋转与直纹曲面、极小曲面、Levi-Civita 联络、Gauss 与 Codazzi 方程、曲面基本定理的局部存在与唯一性、测地线及第一变分、指数映射和 Gauss 引理、闭嵌入曲面的最短线、平行移动与测地曲率、带角点及整体 Gauss–Bonnet、Gauss 映射与 Hadamard 凸性、二维双曲圆盘。定理注明条件，核心证明、经典计算例题和另设练习均展开。

本册是上述主线的选编与增补，不是全部41讲的逐页直译。基础专题未系统展开高维外代数曲率、Lorentz/Minkowski 分支、Whitney 分类、系统的一般映射次数理论、CAT/Busemann 空间、Hamilton 动力系统、Schwarz–Pick、Jacobi 场和完整二阶变分理论未系统展开；作业部分补入所需外幂、特定球面映射次数、奇点标架和受约束粒子方程。拓扑工具只在需要处引用，未重复已有拓扑册。平均曲率采用 $H=(k_1+k_2)/2$，与原讲义取迹的约定有因子2差异；形算子统一为 $S=-dN$。

官方10份作业实际共 **32个顶层题**，逐份为3、2、3、5、3、4、3、2、4、3；四题内有10个显式子问，不能与32相加。30题的全部要求已作独立解答，包含错误原命题的反例与修正版。PS3.3折线/Hopf部分已解，但最后引用的Proposition6.3无法定位；PS9.4仅引用未找到陈述的Lemma28.3，故保留缺口，不猜题。PS6.1课堂/商业教材方法未取得，已明确另作自足隆起构造。无公开官方解答、考试原卷、逐日课历或截止日，不编造。见 [冻结题目库存](assignment-inventory.json) 与 [覆盖记录](review/assignment-coverage.json)。

原12章和36题的独立数学审稿保留；新增作业由三组独立Sol审稿逐题核对原件、所有子问与解答。31个新增或变化页逐页实际查看，40个基础正文/解答页与已审旧版逐页完整RGB像素完全相同，继承原真实视觉记录；八幅新增PGFPlots图另经300dpi放大检查。记录见 `review/`。自动编译检查、目录及内部链接核查、源码包的干净重编证据也在该目录。自动排版检查不替代数学审稿和真实视觉检查。

源码包含主文件、全部章节、两份仓库技能依赖快照、编译与打包脚本及来源清单，不依赖其他学科目录。字体及 TeX 运行时是外部依赖，未把字体二进制、缓存或构建产物放入源码 ZIP。需要 Python 3、XeLaTeX、`ctex`、TikZ/PGFPlots、Computer Modern Unicode 与 Fandol 字体；验证器需要其 `requirements.txt` 所列 Python 包。

```bash
unzip differential-geometry-source.zip
cd differential-geometry
bash build.sh
```

产物为 `build/main.pdf`。可用 `TEXMFHOME` 指向已安装的 TeX 用户树；脚本在本次工作环境使用已有 `/workspace/.local/texmf`，不下载或安装软件。测试记录只证明本次选定 Linux/XeLaTeX 环境中的实际重编结果。

原作者 Paul Seidel，MIT，2008；中文重组、勘误、证明增补、练习和独立 TikZ/PGFPlots 图形为本整理本的改动。依 MIT OCW 当前默认 **CC BY-NC-SA 4.0 International** 相同方式非商业分享，保留单独权利声明。见 [LICENSE.md](LICENSE.md) 和 [官方条款](https://ocw.mit.edu/pages/privacy-and-terms-of-use/)。未复制课程首页外部图片或商业教材，未冒称 MIT 官方中文教材或官方作业答案。
