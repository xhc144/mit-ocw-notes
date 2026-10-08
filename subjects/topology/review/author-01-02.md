# 第1--2章作者交接

状态: 两章完整正文已保存, 作者数学复查已进行, 已交独立章节审读. 本记录不把全书或最终 PDF 标为完成. 最终全书构建、链接、逐页视觉及来源许可总核验由主任务继续.

## 写入范围

仅编辑 `chapters/01-metrics.tex`、`chapters/02-sequences-topology.tex` 与本文件, 没有修改其他任务的正文, 没有自行提交.

## 实际读到的来源

- Paige Bright, MIT OCW 18.S190 Introduction to Metric Spaces, IAP 2023, 第1讲原始 TeX 全文与 PDF 提取文本全文, 正文印刷页1--7（末尾另有 OCW 许可页）.
- 同课程第2讲原始 TeX 全文与 PDF 提取文本全文, 正文印刷页1--7（末尾另有 OCW 许可页）.
- 原始文件保存在 `sources/18.s190-iap2023/{tex,text,pdf}/`；正文开头注明主要来源与改编范围, 没有声称逐字全译. 来源 TeX 明示 Creative Commons BY-NC-SA, 具体授权版本和全书许可文字由主任务的来源账本与许可页核验保留.
- 已完整读 math-lecture-writing 主 Skill. 最初 skills.read 对四份 references 返回不可读, 后从已恢复的 vendor/math-lecture-writing/references 实际完整读完 writing-and-proof.md、review-gates.md、research-and-sources.md、latex-and-delivery.md, 该限制已消除.
- 已完整读固定 math-latex-typesetting Skill、STYLE_SPEC、ENVIRONMENTS、MATH_LAYOUT、EDITORIAL_RULES、VALIDATION 与完整 wangzhe_baiti_style.tex; 使用原生语义环境与 originalchapter/originalsection, 没有新增样式. 所有例题题面和完整解答已分离, 使用简体中文及半角英文标点.

## 第1章覆盖与证明

从度量公理、反三角不等式、球及子空间进入范数, 完整证明有限维 Cauchy--Schwarz 与三个常用范数的三角不等式, 给出范数比较与二维球形计算. 继续处理离散度量、有限空间的最小距离、C([a,b]) 上确界度量及 L1 积分度量、C1 范数与微分算子估计. 球面部分区分弦长与测地距离, 证明角度三角不等式, 以分割弦长和说明球面最短路径. 章末5题均附完整解答.

明确声明一元分析先修: 实数完备性, 闭区间连续实函数的有界性、最大值与一致连续性, Riemann 积分和微积分基本定理. 球面路径的一致连续性已通过三个坐标函数解释, 不循环调用后文一般紧域定理. 没有无证明调用一般 p 的 Minkowski 不等式; 此阶段只用1、2、无穷三个范数版本.

## 第2章覆盖与证明

完整给出收敛定义、唯一性、有界性、子序列与距离极限, Cauchy 的三条基本性质与两条 Cauchy 序列间距离的收敛. 给出开闭集运算、开闭球、有限集闭、相对开闭性, 内部/闭包/边界/稠密/聚点/孤立点及运算. 邻域最终包含、闭包与闭集序列判据、聚点互异序列判据均有完整证明. 连续性有 epsilon-delta、序列、邻域逆像与全局开闭逆像版本; 接着证明距离函数 Lipschitz、零点等于闭包, 比较同拓扑度量、双边常数估计与完备性. 反正切拉回度量给出同拓扑而不同完备性的完整反例. 章末6题均附完整解答.

## 修正与审读重点

1. 原讲义L1 Example18把球面路径称在unit ball上; 已明确采用单位球面 S2, 并说明实心球的内部直线路径区别.
2. 原讲义L2 Theorem27的not否定词错误; 已改为序列最终在每个邻域中, 并完整证明.
3. 原讲义的函数积分正定性略去; 已证明连续非零值在正长度小区间上给出严格正积分.
4. 原讲义子序列证明下标容易混淆; 改用 n_k>=k 的直接证明.
5. 独立审读指出02定义后1/n的首项不属于(0,1); 已改为1/(n+1), 审读者实际重读修正段.
6. 对闭集也可能无最近点的陈述, 已补完整离散空间反例并逐项验证度量、闭性与未达到下确界.

独立审读由 chapters_5_6 agent 实际完成, 数学证据另见其 `review/math-01-02.md`. 同模型独立 Agent 审读不冒充跨模型专家. 01末尾有限度量习题只追加 qedhere 作版面调整, 数学内容未变, 已发送新哈希要求绑定.

## 当前稳定源码 SHA256

- `chapters/01-metrics.tex`: `6768ebf6e5888330e7cc306490e2c787ff7c38d101c352abe0568fe5aa4d4856`
- `chapters/02-sequences-topology.tex`: `0104f6262208a9bae70a74c57518cf172c931100d2bae269721c66c0c75c35e7`

## 临时机械与版面检查

在 `/tmp/topology-author-01-02-tvmfj05j/` 用原完整固定模板及两章当前同内容副本构建, 不改正式主文件. 系统默认缺少 ctex 时, 按主任务工具链记录设 TEXMFHOME=/workspace/.local/texmf、XDG_CACHE_HOME=/workspace/.cache 后实际编译成功. 正式源码的环境栈与标签重复检查通过; 没有中文全角标点.

固定 Skill 官方 validate.py 实际返回 AUTOMATED PASS, 两章加测试目录共23页, 所有页已机械渲染. 最终日志无Overfull/Underfull、缺字或未解析引用. 仍有固定模板 FandolKai 粗体与 FandolSong 斜体字形回退提醒, 未通过改样式压制.

实际打开临时最终PDF第10页检查末题QED, 将原另占一行的方框通过 qedhere 放到最后无编号公式右侧后重新构建、重新查看正常. 临时PDF不是整本交付文件; 没有据此宣称全书逐页看过、目录最终通过或最终产物已完成. 正式书稿合并后应重新构建, 并核对所有最终页、链接和许可.
