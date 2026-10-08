# 质量检查记录

检查日期：2026-10-08。最终中文 PDF 为 **47 个实际页面**，含书前 6 页及正文 41 页。自动编译、独立数学审读、逐页视觉和远端传输是不同检查，以下分别给证据。

## 数学与题目覆盖

两位独立审读者逐段重建第 1–7 章和第 8–14 章的数学论证，初审问题 A1–A5、B1–B10 修订后全部关闭。报告保留发现、返修和最后源文件 SHA256，见 `core-review-a.md`、`core-review-b.md`。这不代表原教师核准。

第三位审读者独立推导并逐题核对全部 45 个公开作业题号（69 小问）和 24 个模拟卷题号（47 小问），并把 81 个只给教材定位的原题号全部与官方 PDF 核对，见 `assessment-independent.md`。覆盖不是抽样。清单为 `../assessment-map.json`，69 个公开原题号经重复映射后为 68 个不同题。两份 Sylow 有限阶排除表的 31、67 行已全部检查，剩余阶数另证；交叉引用与交错群单性依赖无循环。解答均为编者独立答案，官网未提供所选题目的官方解答。

## 编译与模板

`validation/validation_report.json` 自动状态 PASS，正文输入哈希与独立审读快照一致。锁定模板类与 `subjects/probability/main.tex` 完全一致；没有自行重设计字体、页面、语义环境。三轮 XeLaTeX 使用 no-shell-escape，最终日志无超宽、缺字、未定义引用或重复标签。自动工具不判断数学正确性，也不冒充人工视觉。

验证命令使用已有本地 TeX 树：

```sh
TEXMFHOME=/workspace/.local/texmf XDG_CACHE_HOME=/tmp/abstract-algebra-fontcache \
python /tmp/abstract-algebra-style/math-latex-typesetting/scripts/validate.py \
/workspace/mit-ocw-notes/subjects/abstract-algebra/main.tex \
--out /workspace/mit-ocw-notes/subjects/abstract-algebra/qa/validation \
--template /workspace/mit-ocw-notes/subjects/probability/main.tex
```

上述绝对路径记录本次执行环境，不是源码包依赖；常规完整 TeX Live 环境可直接运行包内 `build.sh`。

## 实际逐页视觉与链接

主编实际查看全部 47 页的可读渲染（双页图像，每页 1.45 倍 PDF 尺寸），检查正文、页眉页脚、公式、表格、分段与密度。图像为 `page-pairs/`，每页检查记录、图像哈希及最终 PDF 哈希为 `visual-review.json`。没有用渲染成功或小缩略图代替逐页查看。

唯一 TikZ 域格图在 PDF 第 27 页，边、节点与标签已单独查看，无重叠。自动工具对第 9 章一个行内 2×2 矩阵给出高度提醒，PDF 第 21 页实际查看无碰撞；保留原式。原 48 页版本最后目录页过疏，删除来源说明的三个非必要节级目录项后成为 47 页，说明文字未删。

`pdf-navigation.json` 记录 89 个目录条目与 89 个实际目录链接；对应标题全部在目标页查到。113 个总链接全部解析，内部跳转均在有效页且有文字，外部链接为明确 HTTPS 原始来源/条款。此检查验证 PDF 目标解析，浏览器阅读器自身的显示差异不在范围内。

## 自足源码包

`package_and_rebuild.py` 只打包明确白名单：中文 `main.tex`、全部章节、内嵌模板、构建脚本、说明/许可、两个来源与覆盖清单、三份数学审读及本记录。没有英文原 PDF、官方英文 TeX ZIP、字体、凭据、生成 PDF、图片缓存或构建产物。所有文字输入都在包内，TikZ 图形从源码生成。

包在 `/tmp` 的新空目录解压并以三轮 XeLaTeX 实际重编，47 页的文字和 72 dpi 渲染逐页与最终 PDF 相同，目录相同，日志无上述问题。证据为 `clean-rebuild.json`，它绑定最终 ZIP/PDF 的 SHA256 与每个包成员。PDF 元数据时间可能不同，因此不声称两个 PDF 字节完全相同。

## 来源与发布边界

`../source-manifest.json` 记录 41 个官方资源文件，其中 39 PDF 共 545 页、2 个官方 TeX ZIP；每件原始 URL、页数、作者、许可检查和成员哈希均留存。原件只进入 `sources/abstract-algebra/`。默认 CC BY-NC-SA 4.0，单件第三方例外优先；未发现额外明确限制标记不等于保证所有未标注权属。未获取外部教材，不复用原图，未公开题面只登记引用。

本地检查通过后才冻结提交白名单；提交只允许 `subjects/abstract-algebra/` 与 `sources/abstract-algebra/`。发布使用仓库已有 v2.0.1 批量工具，沿用当前私库、安全设置和并行历史。具体远端 commit、完整文件哈希验证及最终 HEAD 以批量工具回执和交付消息为准，不在本地检查阶段预称发布成功。
