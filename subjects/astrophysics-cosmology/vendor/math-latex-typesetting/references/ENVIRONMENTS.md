# 固定语义环境

## 原生与预设的区别

`amsmath` 提供数学排版环境；`amsthm` 原生提供 `proof` 和 `\newtheorem` 等定义接口。`lemma`、`theorem` 等具体名称不是 `amsthm` 自动全部提供的。本包已经在锁定适配类里一次性注册，不要求也不允许每次生成书稿再设计。

旧包仅有 `originalchapter/originalsection/originalexample/originalsolution` 四个宏，未注册定理类环境。本版保留章节宏，将题目和解答迁移到语义环境。不得再次使用旧版手工编号宏。

## 直接可用

| 内容 | 环境 | 固定排版与编号 |
| --- | --- | --- |
| 定理 | `theorem` | 紫红粗体标签，楷体陈述 |
| 引理 | `lemma` | 同定理，不能手写“引理”冒充 |
| 命题 | `proposition` | 同定理 |
| 推论 | `corollary` | 同定理 |
| 定义 | `definition` | 紫红粗体标签，宋体正文 |
| 例题 | `example` | 紫色题号，宋体题面；自动按章编号 |
| 习题 | `exercise` | 紫色题号，宋体题面；独立按章编号 |
| 注 | `remark` | 不编号；黑色粗体“注”与宋体正文 |
| 证明 | `proof` | 黑色粗体“证明”、宋体正体、自动空心方框 |
| 解答 | `solution` | 原生 `proof` 的固定包装，标签为“解答” |

定义、定理、引理、命题、推论共享章内连续计数器，如定义 1.1、引理 1.2、定理 1.3，避免同一章中多个“1.1”难以检索。例题和习题各有独立计数器。前言中不得放带章编号的环境；模板会拦截第 0 章中的数学编号。交叉引用用 `\label`、`\ref` 和 `\eqref`，不要手打。

题面先结束 `example`，再开始 `solution`；不要把完整解答塞在题面环境里。引理先陈述、结束，再单独写证明。环境选择对应内容作者已经确定的语义，不决定内容的讲解方式。

```tex
\begin{lemma}\label{lem:key}
设 $V$ 为实内积空间. 若 $x\perp y$, 则
$\|x+y\|^2=\|x\|^2+\|y\|^2$.
\end{lemma}
\begin{proof}
按内积的双线性展开, 混合项为零.
\end{proof}

\begin{example}\label{ex:one}
设 $a,b>0$. 证明 $a/b+b/a\ge2$.
\end{example}
\begin{solution}
由 $(a-b)^2\ge0$ 得 $a^2+b^2\ge2ab$, 再除以 $ab$ 即可.
\end{solution}
```

## 证毕符号与分段

保持 `amsthm` 的 `pushQED/popQED` 机制，不另写 `myproof`，也不手动 `\hfill $\square$`。正文结束于最后一个有意义的数学句子；自动方框是边界标记，不是额外的总结段。

证明以普通句子结束时，直接 `\end{proof}`；最后一个段落和 `\end{proof}` 之间不要额外空行。若以无编号行间式结束，把 `\qedhere` 放在最后一行：

```tex
\begin{proof}
由假设,
\begin{align*}
F(x)&=G(x)+H(x)\\
    &\ge G(x).\qedhere
\end{align*}
\end{proof}
```

末尾公式需要右侧编号、含 `split/aligned` 或多重嵌套时，不机械塞 `\qedhere`，以免公式编号与方框冲突。优先在公式后写真实的最后一句推论；或者在测试过的顶层无编号环境结束。若以列表结束，方框放在最后一项的末尾。任何情形都须看 PDF 实际位置。

段落数量与证明详略由内容作者决定。模板保留正文行距和首行缩进，以固定块间距区分相邻环境；不用额外空行或临时样式重造证明版式。

## 已有数学排版环境

单式用 `equation` 或 `equation*`/`\[...\]`；成组推导用 `align/align*`；单个长公式用 `multline/multline*`；需要一个编号而分行的等式用 `equation` 内的 `split`；局部对齐用 `aligned`；分段函数用 `cases`；矩阵用 `matrix/pmatrix/bmatrix/vmatrix` 等。`split/aligned/cases/矩阵` 不是可以在普通正文里裸用的显示环境，必须放在合适数学模式内。

并列条件用 `enumerate`，需要表格时用标准 `tabular`（长表按实际需求最小扩展）。书目使用预设 `thebibliography`。额外包只服务内容，不得覆盖字体、段距、章节或环境样式。
