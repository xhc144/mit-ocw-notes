# 验证记录

- coverage-freeze.sha256：编写前冻结的全课程来源清单。
- assessment-inventory.json：原题编号、合编计数及无法取得项；全文清单与实写解答核对，选做小问保留。
- numerical-checks.json：物理数值、样本尺寸、收敛/有限精度边界；tools/physics_checks.py可重算。该证据不能证明一般分类或无限体系相变。
- render-and-links.json：每个物理页的PNG哈希、实际查看状态、181个内链及144个书签目标检查，锁定模板与既有热统卷逐字节比较。图片只存在临时审阅目录，不增加公开仓库体积。此次为同一编者的逐页检查；不冒称独立读者审查。
- standalone-build.json：最终TeX输入哈希、XeLaTeX轮数、PDF哈希。禁shell escape，交叉引用收敛，无未定义引用、数学模式非法命令、盒溢出或缺字。
- archive-validation.json：已实际解包源码ZIP并从独立干净路径重新编译，ZIP CRC、输入数、PDF页数及哈希比较。
- remote-validation.json：提交后按不可变提交URL下载PDF/ZIP，核对哈希、物理页数、ZIP CRC及远端ZIP的干净复编。该文件在产物上传成功后另提交，不预写成功。

数学范围复核：检查响应符号和傅里叶归一化、环链费米宇称、开链一般边界量子化、横场自旋倾斜基、Friedel分支和电荷积分、原题疑似误植以及Bott/LSM使用条件。原教材图比较缺口保留。一般理论的证明范围见正文，不把抽样或图像检查说成数学证明。
