# 核验范围

自动排版报告、实际逐页目检与数学复核分开保存。`automated-validation-report.json` 保留工具原始结论，自动化工具明确没有评估数学、教学和视觉质量；本项目没有把这些字段改成通过。

- 使用锁定的仓库 `elegantbook-original-adapter` 模板；XeLaTeX 两遍编译，目录、公式交叉引用和书签均在生成 PDF 内。
- 全页 130 dpi 渲染；编者逐页查看标题、公式、表格、图、图注、页眉页脚及留白。`visual-audit.json` 对应最终 PDF 哈希及每页渲染哈希。相同像素哈希的最终页沿用实际看过的页面；改版页重新查看。
- 无未定义引用、缺字或 overfull 报错。仅有 underfull 提示；已查看对应来源表/图注。目录末页和书目留白是自然分页，没有空白占位章。
- `compilation-record.json` 记录编译输入哈希；`all-pages-render-record.json` 记录所有页。渲染缓存 PNG 不加入公开仓库。
- 源码 ZIP 解压到全新临时目录，实际再次 XeLaTeX 编译并核对页数、PDF 提取文本、ZIP CRC 和所有输入文件哈希；见 `clean-rebuild.json`。构建机补齐 TeX Live 的 ctex、xeCJK、Fandol 与 CMU 依赖，字体文件不再分发。

数学与题面核对：

`numerical_and_plots.py` 复算 Na 有效振子寿命、饱和强度、黄光/红外光阱功率与散射率、Rydberg 腔尺度/真空 Rabi、Stark 淬灭和单 2P 近似的双光子寿命，生成13个光场状态矢量图和 Schmidt 阈值曲线。其他推导在正文给出：Breit–Rabi 的二维块、频率与宽度约定、相干/压缩态矩、光力及相关函数。原题不足以唯一确定的量明确保留几何或分布参数。

重点检查更正：LOCC 与秩、Schmidt 固定阈值、双臂损耗、Yurke 系数、单环境与 Markov 极限、短时展开条件。未声称经独立 Agent 审校或已证明全部 AMO 多体结果。

原件与出版边界见 `../SOURCES.md` 和 `../LICENSE.md`；正式包不含原版 PDF、原页截图、OCR文本、商业教材或外部字体。

修订版补入Welton领先对数、Casimir模式和、Mollow相干/非相干谱及权重/半宽、缀饰力噪声与Sisyphus循环、蒸发效率与runaway、愈合长度/TF/耗尽/Mott平均场、Cooper与BCS、Cirac–Zoller三脉冲。revision-math-results.json 核验固定B/P端口正号、严格阈值边界、耗尽积分、平均场尖点及离子CZ脉冲；考试所需两组能级/跃迁图和光散射虚态图实际绘制。严格QED、多体临界及硬件噪声不在这些有限检查的证明范围。新版独立数学接收仍由父任务抽查。
