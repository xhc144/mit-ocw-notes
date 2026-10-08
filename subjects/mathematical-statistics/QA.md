# 数理统计整书交付核验

本卷保留原有十章并增加原课程信息与11章官方作业中文完整题解，唯一整书PDF为110个物理页（前置7页、正文与参考文献103页）。讲义按当前内容页10份PDF、第1–24讲、292源页；作业按官方Assignments页11份PDF、42源页。共21个源PDF334页，20份317页归档，PCA17页整份hold。旧Lecture6、Old17–18排除；新版矩估计15页、Bayesian18页。全部可归档原件的大小、SHA256及实际页数逐一核验，见review/final-source-audit.json。

新增作业包括34主问题、203个原印层级节点、181编号末级问及12个无编号要求；保留原编号与原截止日期，PS11七分布逐一解答。译题与AI独立推导的详细解答分别完整展开，原印错误及必要补充条件明确区分。MIT明确没有官方作业答案；未发现可纳入的公开考试PDF，不虚构考卷。无外部教材缺失题干或外部数据待补项。逐问来源定位与独立复算见review/assignment-inventory.json、两个ps*independent-review.md。两位独立任务代理实际全文审读、复算并复看最终修改，报告绑定全部11.tex最终哈希；这不是外部专家保证。卷首事实另经独立来源审读，网页与Intro的评分/先修差异分别保留。

十章.tex与已交付66页基线逐字节一致。固定锁定类与subjects/numerical-analysis/main.tex完全一致，字体、页边距、颜色、语义环境未重设计。最终source/compile/log/pdf机械验证PASS；无未解析引用、缺字或盒溢出。机械检查不代替数学或视觉审查。QED提示、PS8行内矩阵和目录尾页空白均经实际页面检查。

每个最终物理页具有视觉证据：60页与此前已逐页查看的66页基线RGB像素完全一致，其余新增/变化页逐张实际打开查看；最终版再按PNG字节等值映射承接审看结果，变化的卷首页重新查看。证据链绑定在review/visual-final.json、final-page-evidence.json与base-volume-evidence.json，三份assessment-visual报告明确只签实际查看的草稿快照，未自动重签新PDF。原生文字及公式可选取；自绘箱线图为TikZ矢量。PS7五幅原QQ图本为JPEG，必要PDF裁切保留原图像字节和原图号/坐标文字；不称全部图形纯矢量，也未把新随机图冒充原题。五幅图像字节哈希均与官方PS7原件完全一致。

目录与PDF书签目标按实际annotation、named destination及目标页文字核验，92书签、92内部链接、23外部链接均合法，见review/pdf-links.json；未声称模拟鼠标点击。三组Python实验脚本真实运行成功，含likelihood数值极值、Fisher积分、有限样本区间、KS/Spearman实际50000次模拟、GLS矩阵恒等式、非参数风险、后验积分与指数族归一化。R代码已阅读，R未安装/未运行；模拟不替代证明。

源码包按白名单生成，含main、course-information、十章、十一份作业、参考文献、build.sh、数值脚本与来源/许可/审校记录，及两份必要QQ图裁切；没有字体、官方完整PDF、PCA受限素材、旧成品或编译缓存。包内脚本在独立干净临时目录关闭shell escape三遍重编，结果与整书逐字节对比，见review/clean-rebuild.json。复现只针对本环境已核依赖，不声称跨操作系统字节相同。

改编按CC BY-NC-SA4.0署名；第三方例外按材料核验而非按仓库可见性推定。正常Git保留同路径历史与并行学科提交，无force、无新LFS、安全/网络/凭据修改。上传后的独立克隆与远端文件哈希证据见review/remote-delivery.json。
