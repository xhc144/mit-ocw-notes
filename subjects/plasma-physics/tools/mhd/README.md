# 22.615 公开考核数值复核代码

来源：MIT OpenCourseWare，Jeffrey Freidberg，22.615 *MHD Theory of Fusion Systems*，Spring 2007 的公开期中、期中补充说明、期末及 HW4 第 3 题。课程入口：<https://ocw.mit.edu/courses/22-615-mhd-theory-of-fusion-systems-spring-2007/>。

这是中文讲义项目自行推导的参考实现，不是 MIT 官方解答。未重构作业中的商业教材引用题，也不包含原课程 PDF、课程图片、字体、凭据或下载器。许可与逐件来源例外以本主题的来源清单和仓库许可说明为准。

依赖：Python 3、NumPy、SciPy、Matplotlib。从仓库根运行：

```bash
python subjects/plasma-physics/tools/mhd/run_review.py
python subjects/plasma-physics/tools/mhd/hw4_ldx_reference.py
```

默认结果写到 `subjects/plasma-physics/qa/numerics/`。要在干净目录重现：

```bash
MHD_OUTPUT_DIR=/tmp/mhd-check python subjects/plasma-physics/tools/mhd/run_review.py
MHD_OUTPUT_DIR=/tmp/mhd-check python subjects/plasma-physics/tools/mhd/hw4_ldx_reference.py
```

`midterm_reference.py` 求五个弱矩与安培约束，按官方补充说明采用余弦权重和 `λ=0.2` 的磁通函数，并选择电流使离轴 `qmin=2`。它显式勘误 GS 压强项、采用 `p=2nT`，输出参数、扫描和磁面/电流数据。

`final_reference.py` 求高 beta 核心与零电流外环的平衡、安全因子和三谐波能量矩阵。保留从原始场分量积分的流体矩阵，并与解析矩阵交叉核验；真空谐波最多五个。等效壁严格按原试卷分支设置。

`run_review.py` 实际重新求解、进行加密核验、扫描 15,251 个平衡，分别保存真零特征值与整数共振壁切换，额外检查薄环序列的 `m=2,…,16`，并生成五份矢量 PDF 及审查 PNG。生成图片是原创数学绘图，没有原课程整页背景。

`hw4_ldx_reference.py` 独立核验公开第 3 题的磁场平衡、`γ=2` 的 `m=0,1` 稳定条件及有限壁修正。

参数、坐标、原件冲突、真实执行结果和范围限制见 [独立复核报告](../../qa/independent-mhd-review.md)。尤其：期中弱矩解不是逐点 GS 精确解；期末三谐波加等效壁模型的稳定点和候选上确界不等于真实装置的完整 MHD 稳定限。
