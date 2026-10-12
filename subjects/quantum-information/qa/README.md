# 核验范围

自动排版报告、实际逐页目检与数学复核分开保存。`automated-validation-report.json` 保留工具原始结论，自动化工具明确没有评估数学、教学和视觉质量；本项目没有把这些字段改成通过。

- 使用锁定的仓库 `elegantbook-original-adapter` 模板；XeLaTeX 两遍编译，目录、公式交叉引用和书签均在生成 PDF 内。
- 全页 130 dpi 渲染；编者逐页查看标题、公式、表格、图、图注、页眉页脚及留白。`visual-audit.json` 对应最终 PDF 哈希及每页渲染哈希。相同像素哈希的最终页沿用实际看过的页面；改版页重新查看。
- 无未定义引用、缺字或 overfull 报错。仅有 underfull 提示；已查看对应来源表/图注。目录末页和书目留白是自然分页，没有空白占位章。
- `compilation-record.json` 记录编译输入哈希；`all-pages-render-record.json` 记录所有页。渲染缓存 PNG 不加入公开仓库。
- 源码 ZIP 解压到全新临时目录，实际再次 XeLaTeX 编译并核对页数、PDF 提取文本、ZIP CRC 和所有输入文件哈希；见 `clean-rebuild.json`。构建机补齐 TeX Live 的 ctex、xeCJK、Fandol 与 CMU 依赖，字体文件不再分发。

数学与题面核对：

`numerical_and_circuits.py` 逐矩阵验证 Fredkin 六个 Pauli 共轭像、原页 PS8 的两同号 X 旋转及准确 CNOT 补门；对 N=4,10,100,143,1024 核验相位匹配搜索。Shor 恢复使用512维编码、256正交综合征与全部512阻尼 Kraus，对26个阻尼强度检查恢复基正交和逻辑信道保迹，画四种输入的精确有限和曲线。它不证明所有恢复器或全体输入的最坏保真度。

典型串数以精确整数求得，98位、概率0.6185752077；Bayes 反馈固定种子143保留50次实测模拟记录；78节点QFT资源图保留逐边和测量顺序 JSON，不报未经证明的最小值。

旧 PDF 的错误文字编码另以原页检查：主 HW3 同号搜索相位、HW5 根号与概率、Quiz1 SWAP Hamiltonian，附加 PS1–10 全部原页。更正 PS2 的 Y/X、AC/B 寄存器和 bra contraction，PS8 同号负 X 旋转，PS5.4 的置换相似错误。主 HW4.5 的原页本身没有可恢复边线；solutions4 第4页明确推迟该解答，保持部分完成。

一般 HSW/解耦/绝热等价/非Abel算法和最优性证明的边界见 coverage.json，不把有限实例检查列为它们的一般证明。没有独立 Agent 数学审校。

原件与出版边界见 `../SOURCES.md` 和 `../LICENSE.md`；正式包不含原版 PDF、原页截图、OCR文本、商业教材或外部字体。
