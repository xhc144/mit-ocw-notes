# 习题课独立第二读者审查

审查者：exams组E，同模型独立会话；不是MIT官方审定或外部专家认证。

绑定正文 SHA-256：`30397a46683a41aadff404a7a07fb92efba1cad92219c237243ec1b6bd2ad64c`。此前修图前的作者单独PDF（历史实核证据保留） `/tmp/ode-rec-build/recitations-check.pdf`，31页，SHA-256 `3a2a88e84245dffe8ab03c7adc9db2f280750c12280fefd8c5ac0a9cedcc5f71`。

22次公开习题课，106主问题、147末级小问。6、12、20、26无公开单独题册，不编造题目。实际遍读22份源题、22份答案及全部中文题解；44份PDF SHA实际复核一致，全部原题标签唯一、清单题号与叶计数吻合。源题图像contact sheets全部实际查看，图问由题中明确方程或分段值定义；未发现另有第三方版权例外标记。

审查包括条件、初值、单位、题号、全部小问、代数、源答错漏与重绘图义。数值图只作示意，不作为数学证明。作者单独PDF的31页全部实际用view_image打开；最后p19裁切标签修正后重新实际查看闭合。全册重排后的页码与邻近段落仍由父任务作整册视觉审查。

## 关键论证与错误闭合

- Rec02Q7：正积分函数U可逐项求导；分部积分给U''=x²U，s=-U'/U>x。二解约化U(1+cJ)及J无界区分上侧有限爆破、下侧全局解，不能把等斜线y=x称为分界解。
- Rec02Q8：对U及J的渐近展开复核，得到下支y=-x+1/(2x)+O(x^-3)；漏斗边界-x与-√(x²-2)在x>√(8/3)向内。官方-x+1笔误明确补正。
- Rec03Q2：逐Euler区间的残差符号与比较论证成立，首段端点等号不妨碍结论。Rec03第二槽t=1才无盐的条件完整保留。
- Rec05负幂：z^-4确在上半平面，官方笼统下半平面错误已更正。
- Rec13Q6：负频率ω=-1消去例外及ω=0、1单频例外独立处理；其他频率由线性无关性证有理公度必要性。
- Rec15Q5：加入齐次解产生更多周期响应须频率公度；无公度时仅唯一周期特解，修正官方省略的条件。
- Rec23：八个参数点特征值、稳定性、旋转方向、亏损情形及显式Cayley–Hamilton通解逐行复算。
- Rec24Q1：Δ=0、迹负的常值方向及原点A²=0边界完整；零矩阵中性、有非零幂零矩阵产生线性增长，不能把整个原点无条件称中性稳定。
- Rec25Q3：V'=-(x-1)²，正象限紧子水平集、极限集不变性只留下(1,1)，全局收敛补证成立。
- Rec25Q4：曾反馈仅写e^Jt(c+o(1))不能保证c非零；作者补可逆实P变换与极坐标r'=-r/2+O(r²)、θ'=β+O(r)。r可积保证log r+t/2及θ-βt有有限极限，非零解C>0，主导率与伪周期完整成立；已独立复读闭合。
- Rec16Q1：最后PDF中“强度1”冲量标签曾被图框裁切；作者升高ymax，独立实看最终p19确认标签完整。

## 逐题结果

每一条“通过”对应实际读题、对照源条件及检查中文解答，非仅检索标签或编译。

| 原题标签 | 源页 | 末级小问 | 结果 |
|---|---|---|---|
| cw:rec01-1 | 1 | root | 通过 |
| cw:rec01-2 | 1 | root | 通过 |
| cw:rec01-3 | 1 | root | 通过 |
| cw:rec01-4 | 1 | root | 通过 |
| cw:rec01-5 | 1 | root | 通过 |
| cw:rec01-6 | 1 | root | 通过 |
| cw:rec02-1 | 1 | root | 通过 |
| cw:rec02-2 | 1 | root | 通过 |
| cw:rec02-3 | 1 | root | 通过 |
| cw:rec02-4 | 1 | root | 通过 |
| cw:rec02-5 | 1 | root | 通过 |
| cw:rec02-6 | 1 | root | 通过 |
| cw:rec02-7 | 1 | root | 通过 |
| cw:rec02-8 | 2 | root | 通过 |
| cw:rec03-1 | 1 | root | 通过 |
| cw:rec03-2 | 1 | root | 通过 |
| cw:rec03-3 | 1 | root | 通过 |
| cw:rec03-4 | 1 | root | 通过 |
| cw:rec03-5 | 1 | root | 通过 |
| cw:rec03-6 | 1 | root | 通过 |
| cw:rec04-1 | 1 | a,b,c,d | 通过 |
| cw:rec04-2 | 1 | root | 通过 |
| cw:rec04-3 | 1 | root | 通过 |
| cw:rec05-1 | 1 | root | 通过 |
| cw:rec05-2 | 1 | root | 通过 |
| cw:rec05-3 | 1 | a,b,c | 通过 |
| cw:rec05-4 | 1 | root | 通过 |
| cw:rec05-5 | 1 | root | 通过 |
| cw:rec07-1 | 1 | root | 通过 |
| cw:rec07-2 | 1 | root | 通过 |
| cw:rec07-3 | 1 | root | 通过 |
| cw:rec07-4 | 1 | root | 通过 |
| cw:rec07-5 | 1 | root | 通过 |
| cw:rec07-6 | 1 | root | 通过 |
| cw:rec08-1 | 1 | root | 通过 |
| cw:rec08-2 | 1 | a,b,c,d | 通过 |
| cw:rec08-3 | 1 | root | 通过 |
| cw:rec08-4 | 1 | root | 通过 |
| cw:rec08-5 | 2 | root | 通过 |
| cw:rec09-1 | 1 | root | 通过 |
| cw:rec09-2 | 1 | root | 通过 |
| cw:rec09-3 | 1 | root | 通过 |
| cw:rec09-4 | 1 | root | 通过 |
| cw:rec09-5 | 1 | root | 通过 |
| cw:rec10-1 | 1 | root | 通过 |
| cw:rec10-2 | 1 | root | 通过 |
| cw:rec10-3 | 1 | root | 通过 |
| cw:rec10-4 | 1 | root | 通过 |
| cw:rec10-5 | 1 | root | 通过 |
| cw:rec11-1 | 1 | root | 通过 |
| cw:rec11-2 | 1 | root | 通过 |
| cw:rec11-3 | 1 | root | 通过 |
| cw:rec11-4 | 1 | root | 通过 |
| cw:rec11-5 | 1 | root | 通过 |
| cw:rec11-6 | 1 | root | 通过 |
| cw:rec13-1 | 1 | root | 通过 |
| cw:rec13-2 | 1 | root | 通过 |
| cw:rec13-3 | 1 | root | 通过 |
| cw:rec13-4 | 1 | root | 通过 |
| cw:rec13-5 | 1 | root | 通过 |
| cw:rec13-6 | 1 | root | 通过 |
| cw:rec14-1 | 1 | a,b,c | 通过 |
| cw:rec14-2 | 1 | root | 通过 |
| cw:rec14-3 | 1 | root | 通过 |
| cw:rec14-4 | 1 | root | 通过 |
| cw:rec14-5 | 2 | root | 通过 |
| cw:rec15-1 | 1 | root | 通过 |
| cw:rec15-2 | 1 | root | 通过 |
| cw:rec15-3 | 1 | root | 通过 |
| cw:rec15-4 | 1 | root | 通过 |
| cw:rec15-5 | 1 | root | 通过 |
| cw:rec16-1 | 1 | a,b,c,d | 通过 |
| cw:rec16-2 | 1 | root | 通过 |
| cw:rec16-3 | 1 | root | 通过 |
| cw:rec16-4 | 1 | root | 通过 |
| cw:rec17-1 | 1 | a,b | 通过 |
| cw:rec17-2 | 1 | root | 通过 |
| cw:rec17-3 | 1 | a,b | 通过 |
| cw:rec17-4 | 1 | a,b,c | 通过 |
| cw:rec18-1 | 1 | root | 通过 |
| cw:rec18-2 | 1 | root | 通过 |
| cw:rec18-3 | 1 | i,ii,iii | 通过 |
| cw:rec18-4 | 1 | root | 通过 |
| cw:rec18-5 | 1 | root | 通过 |
| cw:rec19-1 | 1 | root | 通过 |
| cw:rec19-2 | 1 | root | 通过 |
| cw:rec19-3 | 1 | root | 通过 |
| cw:rec19-4 | 1 | a,b | 通过 |
| cw:rec21-1 | 1 | i,ii,iii,iv | 通过 |
| cw:rec21-2 | 1 | i,ii,iii,iv,v | 通过 |
| cw:rec21-3 | 1 | root | 通过 |
| cw:rec21-4 | 1 | root | 通过 |
| cw:rec22-1 | 1 | a,b,c,d,e | 通过 |
| cw:rec22-2 | 1 | a,b,c,d,e | 通过 |
| cw:rec23-1 | 1 | root | 通过 |
| cw:rec23-2 | 1 | root | 通过 |
| cw:rec23-3 | 1 | root | 通过 |
| cw:rec23-4 | 1 | root | 通过 |
| cw:rec24-1 | 1 | root | 通过 |
| cw:rec24-2 | 1 | a,b,c,d | 通过 |
| cw:rec24-3 | 1,2 | a,b,c,d | 通过 |
| cw:rec25-1 | 1 | root | 通过 |
| cw:rec25-2 | 1 | root | 通过 |
| cw:rec25-3 | 1 | root | 通过 |
| cw:rec25-4 | 1 | root | 通过 |
| cw:rec25-5 | 1 | root | 通过 |

全部106主问题、147末级小问通过；发现事项均闭合，无未解决数学或题目覆盖阻塞。源码冻结后如发生内容变更须重新绑定复核。

## 仅图排版变更后的绑定复核

本次从已全量数学复核的 `6dd2a7d2128c6daee3bfd18fb70b4595e4f13d993b50539a6bf44396754f7b0d` 到 `3bd6636ff77d58d7962c3ca2e3015cc0d5599bf579732e634eeda2ce252fb751`，对照 `/tmp/ode-visual-before-fixes-20261008/recitations.tex` 的精确diff。仅有11处3.8cm高局部相图宽度由0.3改0.28正文宽、7处相邻图间增加0.035正文宽间隔，以及Rec05Q1的z^-3标签和引线起点移至上方。引线终点仍是(-1/8,0)；所有曲线采样坐标、方向箭头坐标、矩阵、题面、公式、证明和解答均未改。

将这四类排版替换反向还原后，与旧正文全文逐字符一致，独立验证记录为 `review/visual-layout-diff-independent-check.json`。因此原106主问题/147末级小问及44源SHA的数学审查继续成立，无需重复未改数学。新合册图排版效果仍须实际重新查看受影响页；历史31页实看与原源题实核证据保留，不将diff验证宣称为新PDF视觉通过。

### 第二次标签锚点复核

从 `3bd6636ff77d58d7962c3ca2e3015cc0d5599bf579732e634eeda2ce252fb751` 到 `ba41c5349cd4596f82723237d00e5e6728154da35aefbfa067557e7b2f906e8c`，唯一新增差异为Rec05Q1的z^-3节点锚点由 `[above]` 改为 `[above left]`。将这唯一替换反向还原后，正文SHA严格回到前一已审稿SHA；标签坐标、引线起终点、全部数学及曲线/箭头数据均未变。原全量数学审查继续成立。新版145页仍待实际render复看，不能据源码差异宣称视觉碰撞已消除。

### 负幂图左侧留白的最终差异复核

从 `ba41c5349cd4596f82723237d00e5e6728154da35aefbfa067557e7b2f906e8c` 到 `30397a46683a41aadff404a7a07fb92efba1cad92219c237243ec1b6bd2ad64c`，唯一新增差异为Rec05Q1负幂图的可视域下界xmin由-0.3扩为-0.45。精确反向该替换，正文SHA回到上一已审稿SHA；所有点、引线端点、标签内容、公式、矩阵、证明与方向箭头均未变，因此全量数学审查继续成立。原尺寸孤立预览已由独立读者实际查看，z^-3完整且与纵轴0.2刻度分离；正式合册145页的最终视觉状态由独立视觉JSON记录，不再改变本数学审稿。
