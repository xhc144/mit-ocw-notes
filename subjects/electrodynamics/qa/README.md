# 审校与交付证据

当前扩充版为73页、29章、110个考核题解单元；其中研究生十二套作业66道一级题已全部写入，原题模型和缺失教材图的限制在题旁注明。

- source-review.md与advanced-source-coverage.md：真实原件、许可证和十二套作业题面核对。
- theory-review.md、assessment-review.md、revision-review.md：首稿与首轮修订的数学/物理复核，作为历史记录。
- pedagogy-audit.md、expansion-review.md：扩充推导的教学缺口与修订检查。
- advanced-official-review-a.md、advanced-official-review-b.md：实际核对十二个命名官方解答文件及solution7错配。
- graduate-review-1-3.md、graduate-review-4-6.md、graduate-review-7-9.md、graduate-review-10-12.md：十二套66道一级题的独立计算和子问复核。
- revision-second-review.md：扩充稿缺项关闭、Frank–Tamm系数、圆孔球壳、规范解耦及强圆偏振波初态复核。
- typesetting-validation_report.json：固定模板、受控三遍XeLaTeX收敛和自动PASS，不认证数学或人工视觉质量。
- visual-review-second-primary.md：实际检查前半本1–37页；分页重编后18幅相同PNG保留已检查证据、19幅变化PNG实际重新打开。
- visual-review-second-independent.md：独立实际重新打开最终物理38–73页全部36页，图例和跨页问题修复后复核。最终报告均绑定同一PDF SHA256。
- release-structure.json：171个目录链接、174个内部链接、7个外部链接，命名目的地、页码与目标标题通过；再次核61份原件的SHA256及页数。
- release.json：成品PDF、源码ZIP确切哈希/大小及覆盖边界。

首版visual-review-primary.md、visual-review-independent.md及旧上传回执保留为历史，不能直接认证新版。typesetting-main.render.json记录实际生成73张130dpi单页图，自动字段仍诚实标为未人工检查；人工行为由上述视觉报告独立记录。临时PNG不作为附件交付，可从相同PDF重新渲染。

上传在最新远端main的隔离检出中仅复制冻结电动力学独占路径，普通提交/推送并核远端blob。仓库既有私有仓库专用上传器未改。首批原件提交1c87347db6d54b6cff69c7734b1acc5b7361faaa；本轮成品提交见second-upload-receipt.json及第二批审计回执。没有修改根README、公共索引或其他学科。

源码ZIP只打包可编辑正文、图数据、模板与内容/视觉审校证据；release.json和上传清单/回执留在仓库qa，避免ZIP自身哈希形成循环。独立编译不需原始英文PDF，来源/题面再核工具则应在完整仓库中执行。
