# 本轮构建与核查

最终PDF为126页，SHA-256：`d065a5cc3f6d2ea022eec10d4994d080330da8601780e47444a8bded0afa5d04`。源码ZIP含65份文件，SHA-256：`e72f565560d3ec4f9aaf02cd271b4177cf3e196da81ac2116036a4a3ca7de288`。交付清单见 [release-manifest.json](release-manifest.json)。

- 原13章正文保留，仅增加两处例题引用标签及一处系数与全1向量之间的薄空格；原66页交付及其PDF/ZIP保留Git历史。
- 新增97主问题、308第一层块，逐题中文题面和解答成对核对通过。两个独立读者分别完成6.253的31题及15.053的66题数学、转录及全部作答要求审读；发现的条件、对偶证书、逻辑、数据和作图问题均返修复查。
- 九份工作簿的30张表实际读取，含真实XLS/XLSX/XLSB格式。实际运行LP、精确主元、整数枚举和原/对偶证书检查；1765对XOR与84775组三条件逻辑验证通过。当前没有专用spreadsheet skill，未声称调用不存在的技能。
- 固定模板锁定区一致，实际编译引用收敛，自动PASS、0错误。保留1条Underfull疏排提醒，经相应整页视觉检查可读；没有缺字、未解析引用或溢出错误。
- 全126页均以130dpi原尺寸实际打开检查。修改页重新打开；最终未变页以PNG字节哈希相同承接已完成检查。接触图未替代单页检查。最终逐页绑定见 [visual-review-v2.json](review/visual-review-v2.json)。
- 新增15.053全部15幅TikZ另由数学读者独立实际看图。正文公式原生TeX，PDF内0个栅格图片；120项目录书签、325个链接，全部内部目的地有效。
- 63份原始资源实际字节哈希全匹配。13份文件仅保留官方链接与哈希，其中12份含外书背景行文；完整数学数据和任务已独立重述。Rec10已删除的版权插画未恢复。
- 最终源码ZIP在全新临时目录实际解包，开始时没有生成类或build缓存；用关闭shell-escape的标准XeLaTeX三轮重编。全文提取一致，126页在130dpi的全部像素与交付PDF相同。二进制PDF因时间戳/ID不同可有不同哈希，两者分别记录，未冒称同字节。

详细证据见 [final-qa-v2.json](review/final-qa-v2.json)、[clean-rebuild-v2.json](review/clean-rebuild-v2.json)、[pdf-link-audit.json](review/pdf-link-audit.json)及两个`*-final-reader.json`。`review/final-qa.json`、`review/clean-rebuild.json`与原来源元数据记录的是66页基线；源审计里最初缺ctex的尝试不是当前整册构建状态。

两处非阻断观感保留：原正文39页首有短续句；104–105页初始基元组跨页，但等式两端及含义清楚。以上检查限定已核范围，同模型独立代理审读不是外部专家认证，也不是全书零数学错误的保证。

15.053实际期中和七份小测试卷不在已核公开库存，未猜补；公开综合练习和三份考试范围指南的身份已明确。远端PDF、ZIP及清单的实际逐字节验证在推送后记录于 [remote-verification.json](review/remote-verification.json)。
