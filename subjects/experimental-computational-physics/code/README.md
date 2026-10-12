# 计算复现条件

脚本以所在subject为根，不需要原作者账号或集群。模拟、材料模型输出和官方参考表分别标注；实际运行及输入/输出哈希见各QA报告。源码包不含字体、二进制或大型第三方库。

安装 `requirements.txt` 后，小模型运行 `python code/prelab_checks.py` 和 `python code/public_lab_checks.py`；原模型基准为 `experiments.py`，Au LJ为 `au_lj_lab.py`。吸附网格依次运行 `phase_diagram.py`、`phase_refinement.py`、`adsorption_extra_checks.py`。精化会追加绘图数据，不能在同一结果目录反复执行并把重复点当新样本。书中已有实际数据，不要求阅读时重跑扫描。

Quantum ESPRESSO本次为6.7MaX的 `pw.x`。MIT Lab2/3归档URL和SHA见 `research/archive-input-audit-v3.json`。解压原C、Co、Ba、Ti、O赝势，不执行归档的旧集群脚本。原UPF1可直接读取；本次UPF转换工具的 `l_local` 元数据不可靠，不使用转换副本计算。原/当前命名C、Co数值块比较及原UPF1直接回归另有记录。

各驱动的 `--help` 给精确参数，路径可由用户指定：

```sh
python code/qe_lab2.py --pw [pw.x] --pseudo [C.pz-vbc.UPF] --scratch [scratch-C] --workers 2
python code/qe_cobalt_lab3.py --pw [pw.x] --pseudo [Co.pz-nd-rrkjus.UPF] --scratch [scratch-Co] --workers 2
python code/qe_batio3_lab3.py --pw [pw.x] --pseudo [Lab3/pseudo] --scratch [scratch-BaTiO3] --workers 2
python code/qe_diamond_extras.py --help
```

保存的 `code/inputs` 使用相对pseudo和各任务scratch路径。不同编译器/并行实现可改变末位；总能只在同赝势和同胞定义下比较。

MOLDY上游为 `https://github.com/krefson/Moldy`，本次提交 `e6b5625b473edb2a2fc3a192f8082d7716b00e29`。主积分算法未改，GNU工具链/libtirpc构建。旧观察工具公共变量需 `-fcommon`；附 `moldy-reader-compat.patch` 是已实际使用的读取工具修复，只改ctype声明、POPEN宏和单物种dump头完整/探测判断。补丁遵循上游GPLv2，与讲义CC许可分开；上游SgInfo也有单列许可，不重新授权。补丁没有二进制。

在指定上游检出目录 `git apply [本包/code/moldy-reader-compat.patch]`，按上游说明配置本机tirpc并构建。原MIT Lab4输入由归档取得：

```sh
python code/moldy_kr_lab4.py --moldy [moldy] --inputs [Lab4/input_files] --scratch [scratch-Kr] --workers 3
```

原两相直接启动会碰撞。在独立准备目录复制 `Kr_SL.in` 与本包 `code/inputs/moldy-kr/two-phase-preparation.in`，运行 `moldy two-phase-preparation.in > preparation.log`；确认成功，将自身新生成的 `Kr-save` 通过 `--prepared-restart [Kr-save]` 传给驱动。不要改原2.12 restart版本头。准备改变了原几何，当前结果不构成已确认固液两相平衡熔点。使用匹配构建的msd工具提取轨道；本包未分发大型dump。

GULP许可二进制未取得，Au EAM、Ni三积分器、可选MOLDY修改成EAM未执行。保留完整题面、分析方法与原Ni参数，不用其他模型替代这些结果。
