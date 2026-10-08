# 数值线性代数

67页 · [下载PDF](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/numerical-linear-algebra/dist/main.pdf) · [源码ZIP](https://github.com/xhc144/mit-ocw-notes/raw/main/subjects/numerical-linear-algebra/dist/source.zip) · [版本历史](https://github.com/xhc144/mit-ocw-notes/commits/main/subjects/numerical-linear-algebra/dist/main.pdf)

MIT 18.335J Introduction to Numerical Methods, Spring 2019 的相关主题中文整理与自编补充，12章、来源附录与参考文献，最终PDF67页。

## 阅读范围

浮点误差与范数、条件数及后向误差、SVD与最小二乘/PCA/GSVD、Gram–Schmidt与Householder/Givens QR、LU与Cholesky、数据移动、Schur/Hessenberg/幂法与QR特征值迭代、Arnoldi/Lanczos及重启、GMRES、CG/PCG与双共轭方法、稀疏填充/排序与复杂度、综合实验。

数学公式为原生可编辑LaTeX，未用整页截图替代；目录与交叉引用可点击。模板锁定区使用用户提供的王者百题排版，未另建样式或捆绑字体。

## 来源与改编

主要课程作者Steven G. Johnson；SVD/GSVD两讲由Alan Edelman客座讲授；若干手册作者Per-Olof Persson。官方入口：

- https://ocw.mit.edu/courses/18-335j-introduction-to-numerical-methods-spring-2019/pages/resource-index/
- https://ocw.mit.edu/courses/18-335j-introduction-to-numerical-methods-spring-2019/resources/lecture-notes/

27份全课程手册共261页，不是完整数值代数课稿。核心12份59页、性能补充3份16页；本册以L2–5及L7–24为主线。无完整手册的主题、额外证明及例题已标明自编补充。ODE、优化、积分与FFT全文未混进本册。未复制或下载Trefethen/Bau版权教材全文。

OCW默认CC BY-NC-SA 4.0，特殊署名与权利例外仍适用。另见LICENSE.md与source-manifest.json。Julia-intro的Project Jupyter图像及L25优化概览的Springer图像明确排除CC：原PDF只本地核对，默认原件上传包排除这两件，本册不复制这些图像。

## 编译

使用XeLaTeX，至少两轮。需要ctex/Fandol、Computer Modern Unicode字体与模板使用的宏包。不要更换锁定字体或页面来掩盖缺依赖。

在已配置上述依赖的项目根执行：

    sh build.sh

脚本执行三轮XeLaTeX，将生成结果放在build/main.pdf。dist/main.pdf为已完成核验的发布PDF，不由本脚本覆盖。

主文件通过静态input引用chapters/，所有路径按项目根解析。user提供的math-latex-typesetting Skill可进一步执行validate.py进行模板、日志、PDF和渲染核验。

## 检查边界

- 固定模板完整锁定区比对、依赖检查及XeLaTeX编译通过；最终无未解析引用、缺字、真实盒溢出。
- 67页均已渲染并逐页视觉检查；最后一处中文措辞修订只改变物理页64，其余页图像哈希未变，页64已重看。
- 一位独立作者审查前7章数学条件并提出4项修订，已落实。四个迭代/稀疏章节由作者自检，主编另读其证明与算例。
- 27项选定算例/有限维恒等式的NumPy数值核验通过；不代表所有数学定理由计算机证明。
- Julia标准库API名称已对照官方文档；环境没有Julia，随附nla_experiments.jl未实机运行，不冒称性能测量已完成。
- 行内矩阵高度等自动提醒已按实际页面复核，未发现截断或重叠；自动PASS不是数学或教学质量的自动认证。

详细来源覆盖、构建哈希和检查记录在source-coverage.json与qa/中保存。最终PDF以交付清单中的SHA-256为准。
