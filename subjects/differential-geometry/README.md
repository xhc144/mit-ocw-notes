# 曲线与曲面的微分几何

依据 Paul Seidel 的 MIT OpenCourseWare **18.950 Differential Geometry, Fall 2008** 四份实际公开讲义，重构本科欧氏曲线与二维曲面主线。简体中文原生 LaTeX，使用本仓库 `subjects/probability/main.tex` 的锁定王者模板。

[阅读 PDF](differential-geometry.pdf) · [下载自足源码 ZIP](differential-geometry-source.zip) · [官方讲义目录](https://ocw.mit.edu/courses/18-950-differential-geometry-fall-2008/pages/lecture-notes/) · [来源及逐文件校验](source-manifest.json)

全册 **46 个物理页**，包括前言、可点击目录、12章专题、36题完整解答、实际来源对应表和参考文献。原课程四份 PDF 共60个物理页，其来源页和作者、年份信息保留于 `sources/differential-geometry/`。

内容包括弧长与平面曲率、闭曲线转角与四顶点、空间 Frenet 标架与挠率、正则曲面与面积、第一和第二基本形式、形算子及主曲率、旋转与直纹曲面、极小曲面、Levi-Civita 联络、Gauss 与 Codazzi 方程、曲面基本定理的局部存在与唯一性、测地线及第一变分、指数映射和 Gauss 引理、闭嵌入曲面的最短线、平行移动与测地曲率、带角点及整体 Gauss–Bonnet、Gauss 映射与 Hadamard 凸性、二维双曲圆盘。定理注明条件，核心证明、经典计算例题和另设练习均展开。

本册是上述主线的选编与增补，不是全部41讲的逐页直译。高维外代数曲率、Lorentz/Minkowski 分支、Whitney 分类、一般映射次数、CAT/Busemann 空间、Hamilton 动力系统、Schwarz–Pick、Jacobi 场和完整二阶变分理论不在本册范围。拓扑工具只在需要处引用，未重复已有拓扑册。平均曲率采用 $H=(k_1+k_2)/2$，与原讲义取迹的约定有因子2差异；形算子统一为 $S=-dN$。

独立数学交叉复审覆盖12章和全部36题解答；逐页真实视觉记录及图形放大检查见 `review/`。自动编译检查、目录及内部链接核查、源码包的干净重编证据也在该目录。自动排版检查不替代数学审稿和真实视觉检查。

源码包含主文件、全部章节、两份仓库技能依赖快照、编译与打包脚本及来源清单，不依赖其他学科目录。字体及 TeX 运行时是外部依赖，未把字体二进制、缓存或构建产物放入源码 ZIP。需要 Python 3、XeLaTeX、`ctex`、TikZ/PGFPlots、Computer Modern Unicode 与 Fandol 字体；验证器需要其 `requirements.txt` 所列 Python 包。

```bash
unzip differential-geometry-source.zip
cd differential-geometry
bash build.sh
```

产物为 `build/main.pdf`。可用 `TEXMFHOME` 指向已安装的 TeX 用户树；脚本在本次工作环境使用已有 `/workspace/.local/texmf`，不下载或安装软件。测试记录只证明本次选定 Linux/XeLaTeX 环境中的实际重编结果。

原作者 Paul Seidel，MIT，2008；中文重组、勘误、证明增补、练习和独立 TikZ/PGFPlots 图形为本整理本的改动。依 MIT OCW 当前默认 **CC BY-NC-SA 4.0 International** 相同方式非商业分享，保留单独权利声明。见 [LICENSE.md](LICENSE.md) 和 [官方条款](https://ocw.mit.edu/pages/privacy-and-terms-of-use/)。未复制课程首页外部图片或商业教材，未冒称 MIT 官方中文教材或官方作业答案。
