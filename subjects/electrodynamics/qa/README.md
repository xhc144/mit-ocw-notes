# 审校与交付证据

中文成品为37页、17章、44项考核题解。各证据职责不同：

- `source-review.md`：实际原件、元数据和许可证的独立审查。
- `theory-review.md`、`assessment-review.md`：初稿数学/物理与题面复核、具体修订项。
- `revision-review.md`：修订后复核和8.311三道期末题的独立计算。
- `typesetting-validation_report.json`：固定模板及受控三次XeLaTeX编译，自动PASS，不认证内容。
- `visual-review-primary.md`：实际打开物理第1–19页。
- `visual-review-independent.md`：独立实际打开物理第20–37页。两报告绑定同一PDF SHA256。
- `release-structure.json`：75个目录链接、78个内部链接、7个外部链接，命名目的地、页码与标题检查；再次核61份源PDF哈希/页数。
- `release.json`：成品PDF及源码ZIP的确切哈希、大小和覆盖边界。

编译产物重新变化后，旧报告不能自动认证新文件。`typesetting-main.render.json`是本地实际生成每页图像的记录，图像临时目录不作为交付附件；人工审查报告记载实际查看行为。读者可从同一PDF重新渲染。

上传使用授权公开仓库的普通Git，冻结精确路径和SHA256，独立检出远端main，只加电动力学路径，正常推送并核验远端blob。仓库既有私有仓库专用上传器没有改动。首批源文件实提交`1c87347db6d54b6cff69c7734b1acc5b7361faaa`；最终成品提交见批量回执。未改根README、公共索引或其他学科。
