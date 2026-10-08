# 度量空间、拓扑与几何基础

完整修订版：15章、105个PDF物理页（前置6页、正文及参考文献99页）、58道带完整解答的练习。保留原72页版八章与37道题解，新增一般拓扑、基本群与覆盖、组合曲面及流形长度几何七章。沿用用户固定王者 v4.0.0 真实模板的锁定类；与原版、已交付概率册及vendor金标准逐字一致。

## 交付

- [一册完整PDF](topology.pdf)
- [干净可编辑源码ZIP](topology-source.zip)
- [修订最终核查](review/REVISION_FINAL_CHECKS.json)
- [逐文件来源与实际覆盖](research/revision-source-coverage.md)
- [逐文件源码包校验和](release-source-manifest.json)

主源为Paige Bright的MIT OCW 18.S190 IAP 2023；新增选用18.901 Fall 2004、18.905 Fall 2016、18.900 Spring 2023、18.965 Fall 2004、18.950 Fall 2008的实际官方文件，18.904 Spring 2011仅参考官方课程与Lecture Summaries。共归档27份PDF144物理页；这不是所列全部课程的逐字全译。商业教材未归档，原件署名、逐文件URL/字节/SHA/页数及许可见[sources/ATTRIBUTION.md](sources/ATTRIBUTION.md)和[来源清单](research/source-manifest.json)。练习题解与略证补全为编者编写，章节明确标注，不冒称OCW官方答案。

新增内容包括闭包与连续性、可数性、正规性、Urysohn与Tietze、可度量化、任意积与Tychonoff、商与紧化、基本群/圆周/二维Brouwer、覆盖提升及分类、van Kampen/自由群/附胞腔、有限组合曲面与Euler–Poincaré、标准曲面模型、离散Gauss–Bonnet、流形图册/逆函数/切空间及给定黎曼度量的长度。定义、主要定理条件、证明、例题和58题解答完整保留。

本册不宣称涵盖所有几何拓扑。未收入任意拓扑曲面的三角剖分及完整分类、完整奇异同调/上同调/对偶、一般维数理论、完整曲率测地线理论、Hopf–Rinow、Sard、Whitney与Morse。18.950完整几何主线适合另册。原版详细招生考纲PDF未重新获取的证据边界仍在书前保留；不将旧摘要升级为整份考纲已核实。

## 验证与历史

独立数学审稿的初审问题、修订复审和最终章SHA见`review/revision-math-*.md`，来源独立复核见`review/revision-source-review.md`。105页最终PDF均实际打开单页渲染检查，逐页记录在`review/revision-visual-*.json`；自动渲染本身不算视觉检查。目录/书签107项与实际目标标题匹配，177个PDF链接机械检查无问题。源码ZIP从干净目录解压并重新编译；与交付PDF逐页文本、链接、书签及可见图像比较，证据见`review/revision-clean-rebuild.json`。

未以旧审校记录冒充修订版验收：`review/FINAL_CHECKS.json`及不带revision前缀的旧记录绑定72页版，保留为历史证据。旧完整PDF和源码可从正常提交`fd08654b6a9bfb79de8473bbf2814015db4dd159`恢复。第1—7章字节不变，第8章只改流形可度量化的回指，见`review/revision-original-preservation.json`。不重写历史。

## 构建

```sh
cd subjects/topology
python3 tools/bootstrap_tex.py
export TEXMFHOME=/workspace/.local/texmf
export XDG_CACHE_HOME=/tmp/topology-cache
export PYTHONDONTWRITEBYTECODE=1
python3 vendor/math-latex-typesetting/scripts/validate.py main.tex --out build
python3 tools/audit_pdf.py build/main.pdf --out build/pdf-audit
python3 vendor/math-lecture-writing/scripts/audit_lecture.py main.tex --json
python3 vendor/math-lecture-writing/scripts/check_project.py . --main main.tex
python3 research/verify-sources.py
python3 tools/package_sources.py
```

XeLaTeX及Python渲染依赖需由构建环境提供，工具链依赖使用HTTPS与固定校验和。ZIP不捆绑字体、构建缓存、Git、凭据或页面PNG，解压后的`main.tex`是唯一编译入口；`chapters/01-*.tex`至`15-*.tex`是可编辑正文，`vendor/`保存实际模板及规则。排版自动PASS不替代数学或视觉审稿。

中文译编、重排、勘误与增补采用CC BY-NC-SA 4.0；OCW的Used with permission须按官方FAQ保留特别署名，不能等同All rights reserved。MIT与原作者不为本项目背书。本次只写`subjects/topology/`，其他学科与根主页由统筹者维护。
