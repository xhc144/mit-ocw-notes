# 凸分析与最优化

66页 · [下载PDF](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/optimization/dist/main.pdf) · [源码ZIP](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/optimization/dist/source.zip) · [版本历史](https://github.com/xhc144/mit-ocw-notes/commits/main/subjects/optimization/dist/main.pdf)

[阅读完整PDF](dist/main.pdf) · [下载可编辑LaTeX源码ZIP](dist/source.zip)

以Dimitri P. Bertsekas的MIT 6.253 Spring 2012完整讲义为主源, 加入James Orlin与Ebrahim Nasrabadi的15.053 Spring 2013指定线性规划补充, 重构为一册简体中文讲义. 学科主题包含凸集/函数、最优解存在性、分离、共轭、扰动对偶、次梯度、锥规划、罚函数、次梯度、内外多面体近似、近端/束方法、增广拉格朗日、内点、增量、一阶复杂度与加速、Bregman/熵镜像下降, 以及LP建模、单纯形、Phase I、防循环与灵敏度.

- 最终成果: [dist/main.pdf](dist/main.pdf), 一份PDF, 不按单讲拆分成品
- 源码入口: [main.tex](main.tex)及[chapters/](chapters/), 按章input, 公式原生TeX, 数学示意图TikZ
- 覆盖: 6.253全部25讲的数学教学内容, 原PDF第2--339页; 第25讲复习内容回指前章
- LP补充: 15.053 L2--6/L9与Tutorials 1/2/4/5/6/7, 12资源共377原页, 跨源重复知识合并
- 教学重构不是原作者逐字中文译文; 补充证明与修正说明由整理稿负责

## 原资料与许可

署名MIT OpenCourseWare及原课程教师. 中文改编文本按CC BY-NC-SA 4.0提供. MIT及教师未为改编背书. 原PDF第1页的Athena Scientific图形授权说明原样保留; 这些出版图不在本稿复制, 不能重新宣称它们均为CC素材. 外部书籍、图像和题面有逐项权利例外. 明示All rights reserved的外书题面不逐字复制或重译, 相关知识用通用模型和独立推导保留.

- 6.253来源与SHA-256: source-metadata.json
- 6.253逐页数学覆盖: coverage.json及COVERAGE.md
- 15.053已冻结来源清单: sources/15.053/manifest.json
- 可归档8份原PDF清单: sources/15.053/eligible-manifest.json
- 仅本地保留、归档源链接的4份: sources/15.053/hold-manifest.json

原件资格检查为全部可提取文本版权标注检索及复杂数据页视觉抽查, 不是每一幅嵌入图像的独立权利清理. 原资源页可供读者直接核对.

## 编译

需要XeLaTeX、ctex/Fandol、CM Unicode字体及常规TeX Live宏包, 含amsmath、amsthm、hyperref、TikZ. 不捆绑字体. 在源码目录运行bash build.sh可用关闭shell-escape的标准引擎编译. 本轮固定王者模板的独立验证报告与PDF哈希见交付清单.

## 核查边界

构建检查模板锁定区、全部input依赖、实际编译日志、缺字、引用、溢出、PDF页尺寸与全部页面渲染. 实际视觉审查单独记录. 数学审读重点核对核心对偶/分离/次微分、防循环与算法收敛条件, 精确有理数计算另核对生产/饮食/排班证书及循环表. 高级EMP向量和闭性对偶工具在文中明示为引用工具, 未把论文级证明冒充已经全部重建. 自动PASS不等于全书数学零错误的保证.
