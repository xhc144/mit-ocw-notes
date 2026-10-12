# 交付与审校证据

自动检查、数学/教学审读、实际视觉查看、交付重编译和远端验证各有独立证据，不以题解文件或布尔覆盖字段代替核对。

- [冻结范围](scope-frozen.json)：8.323 Spring2023与8.324 Fall2010，明确无考试/缺第8套/书题指针边界。
- [逐文件来源完整性](source-integrity.json)：73PDF、435页、字节数/页数/哈希及可读文本全部实测。
- [自动编译终版报告](compilation-final.json)、[实际输入哈希](compilation-inputs.json)、[目录与链接检查](pdf-links.json)。自动PASS没有声称数学或视觉通过。
- [基础独审](independent-foundations.md)、[Dirac/QED独审](independent-dirac-qed.md)、[规范场/LSZ独审](independent-gauge-lsz.md)、[重整化/RG独审](independent-renorm-rg.md)：作者之外的模型实际全文阅读、复算并检查教学衔接，具体问题返修后复查。不是人类专家认证。
- [8.323前六套独审](independent-8323-early.md)、[后六套独审](independent-8323-late.md)、[8.324七套独审](independent-8324-assessments.md)：与实际原件全题面/子问对应。
- [有限公式抽检](formula-spotchecks.json)：数值积分、显式gamma矩阵迹、四组散射运动学及两场稳定矩阵，不冒称一般证明。
- [数学审读时的真实源码快照](semantic-reviewed-snapshot.zip)、[快照清单](semantic-reviewed-snapshot.json)、[机械排版映射](formatting-changes.json)、[公式换行语义复查](formatting-semantic-review.md)：源快照与最终排版版有明确对应。
- [积分哑变量专项修复](dummy-measure-correction.json)、[晚组修复对原件复查](dummy-measure-late-review.md)：后续源码核查定位并修正三处固定测度宏与k型被积量不一致，没有称作纯标点修改。
- `visual-pages-001-022.json`及其余六个`visual-pages-*.json/md`：全部148页均实际逐张打开全尺寸渲染图。原查看版PDF的哈希保留，未改成新版本假记录。
- [最终视觉迁移](final-visual-comparison.json)：修正后146页PNG字节与已看页面一致，物理页99/109改变并重新打开检查；终版记录绑定真实终版PDF。
- [源码ZIP成员哈希](source-zip.json)、[洁净解压重编译](standalone-rebuild.json)、[最终交付](release.json)。
- [可接管说明](handoff.md)及远端文件核验记录：限定目录发布、普通非强推、固定commit供父线程独立审查。

首次编译的控制字符错误、后续超宽公式失败分别保留在`compilation-attempt-1/2/3.json`。它们不是成功产物；真实修复后才运行终版检查。中途子集缺ctex.sty的尝试及缓存恢复在作者报告中保留。现成编译缓存路径与软件版本见[构建环境](build-environment.json)，未改锁定字体或版式。

构建缓存和全部页面PNG没有打包进源码ZIP或仓库。最终PDF可以重新渲染，像素SHA及查看范围是证据；每份记录都写明对应版本与检查范围。全册外部链接记录真实官方URL，不承诺未来永不变更。

最新题面忠实性补订：8.324 PS3原题4(d)补回官方第3页的长时间区间及提取寿命要求，解答不变。[修订核验](ps3-condition-correction.json)绑定新148页PDF；仅物理页135改变且已实际打开，其余147页像素与此前已审阅发布版一致。[本轮渲染](ps3-condition-render.json)、编译、链接及ZIP记录对应新版本，此前独审和视觉迁移记录仍保留其原哈希。

同一Library身份的替换及下载核验见[Library记录](ps3-condition-library-verification.json)。新上传来源PDF与新仓库产物一致；Library嵌入C2PA导致存储字节/hash不同，全部148页文字/80 dpi像素与书签相同。版本编号严格保留工具实际返回值。
