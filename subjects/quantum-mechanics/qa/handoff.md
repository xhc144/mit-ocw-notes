# 量子力学增补终稿交付证据

主成品仍是同一路径 `quantum-mechanics-zh.pdf`：153 页的一本连续中文学习册。完整源码 `quantum-mechanics-source.zip` 为 98 成员独立包。19 章理论、39 份作业/测试/期末文档、227 道可用大题的全部小问；本次 20 份作业新增 115 道大题及三份理论来源的遗漏内容。10 道只有商业教材题号的引用不编造题面，两张公式表不计考核。课程题面中文转述与 AI 独立解答分明，没有取得官方解答。

实际恢复远端到 `7c60074a8dbd90065ca82bccd0674ffc608f7d81`；原内容 `52c25d2e8c234575e49dced68d80c2d54c931ae0` 与验收 `14188feaa07dd935962f1a2ee20bb086a057bf71` 在历史内。原作者停止后冻结恢复提交 `e781803cdd8492474b6a303ad92c9a80d688b0f6` 普通合并为 `26c79f98c04dac40947656e7e131b6cc77ce12e7`。新增源码与独审先保存为 `21a45a5`，并普通合并其他学科的远端提交后上传阶段提交 `de114663`；该阶段的旧 89 页 PDF/ZIP 尚未代表新增稿，现已由本记录绑定的新成品替换。没有与停止作者并发写入，没有改写 Git 历史或权限；本次自己编写的变更仅限三个授权量子路径，其他学科及根 README 的并行提交按正常合并保留。

原 17 章理论、19 份考核正文逐字节保留；第 8 章仅在原文前增加线代输入行，见 `baseline-preservation.json`。公开原件 78 份 / 874 页逐文件 SHA、字节、页数及全部页文本读取再次通过。此前 23 份整体暂缓已逐件复核并恢复；来源映射、改编信用、只有题号的对象及官方未提供的材料各自列明，见 `coverage.json`、`additions-coverage.md` 和来源清单。此前撤下和恢复的历史证据继续保留。

原新增稿四组数学独审PASS，115题、新理论与17个自主图表完成返修。父审随后收敛到七处题面条件/请求与W04首次定义，已按实际原PDF限定补全；三组增量数学独审PASS并绑定全部7个变动源。82个TeX输入及所有数值图表未改。精确定位与源/成品哈希见 `parent-review-revisions.json`。没有扩大为整本重写。

本轮XeLaTeX三轮收敛，固定模板自动PASS，无字体缺失或公式溢出。153页联系页及13个修订/关联页实际查看，明确范围见 `visual-parent-revisions.md`；旧 `visual-additions-final.md`按151页历史版本保留。353内部链接、350书签实际目的页/标题PASS，91外链记录。

ZIP 在新目录解压，98 成员 CRC/路径/哈希核对通过；全部 89 个 TeX 输入一致，独立编译三轮生成 153 页，全部页 72 dpi 渲染逐字节匹配交付版。重建 PDF 与交付 PDF 因构建元数据不同而文件 SHA 不同，页面像素相同；不声称二进制可复现。详见 `source-zip.json`、`standalone-rebuild.json`。

交付 PDF SHA256：`a9255bb6e04739df64fc2a9f70dd1a5254d56d819bf1b1f7dae563afb183fd80`。

源码 ZIP SHA256：`783004b992f746a0ff04d2a4fe1a717e5e5c7b396ddf02aaf22504314d14e17d`。

准确终稿输入、独审报告与证据哈希见 `release.json`。远端正常推送后的公开文件 SHA 核验记入 `publication-verification.json`，其记录绑定内容提交，不把早期上传记录用于当前产物。无本次增补阻塞；官方缺失 8.06 第 5 章、两场考试、课纲末周作业以及纯教材题号对象保持清楚边界。

文件用途：`main.tex` 嵌入固定适配类并合成全册；`course-info.tex` 为卷首与课历；`chapters/ch01–17.tex` 是保留理论正文；`linear-algebra-support.tex`、`spectrum-variational-support.tex`、`time-dependent-support.tex` 是本次理论增补；39 个 assessment 文件是考核题解；figure/table 文件是自主图表数值坐标；`source-map.tex` 是逐项来源与边界。`tools/build.py` 隔离编译、禁止 shell escape 并检查源输入未变；`check_pdf.py` 验真实目的页；两个 numerics 脚本重算图形；`package_source.py` 生成完整独立包，`build_coverage.py` 同步覆盖清单与清单中的逐题状态。
