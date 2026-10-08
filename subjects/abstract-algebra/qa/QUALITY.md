# 质量检查记录

2026-10-08。合册 **58个实际页面**：书前6页，原教学正文与参考文献41页（PDF第7–47页），独立附录11页（PDF第48–58页）。数学定义、定理、证明、例题及题解全部中文；附录英文只为版权/许可证原文。编译、数学、视觉、重编和传输分别验证。

## 数学与题目覆盖

`core-review-a.md`、`core-review-b.md` 独立重建第1–7、8–14章，初审问题A1–A5、B1–B10均关闭，绑定正文SHA。`assessment-independent.md` 全量独立核对45个公开作业题号（69小问）、24个模拟卷题号（47小问）、81个原外书定位，非抽样。旧正文和覆盖清单未因此次附录修改，旧审读绑定继续有效；69个MIT公开题号去重为68题，116明确小问解答为编者独立答案，不冒充官方答案。

`judson-independent.md` 独立读取两历史PDF实际原页，先求解后回读中文稿；新增4题8任务全部通过，正方形表64格、海森堡矩阵公理及准循环群所有子群分类完整核对。新版数学载荷与通过的旧快照逐字节相同，Needspace位于题组之外。新版权页和完整许可证另绑定SHA，不以数学通过替代许可材料/传输。该报告作为GFDL附录补充文件，许可和全文随包保留。

合册解答73个来源题号（72个不同题），计116个原明确小问加8项新增任务；不把新增题说成MIT重印题。J#49两版冲突，未替换课程原题；仍未恢复77个外书定位（76个不同定位）。分别见 `../assessment-map.json`、`../judson-assessment-map.json`。未覆盖范围见README和第17章。

## 编译、模板与许可证文本

固定模板内嵌类与 `subjects/probability/main.tex` 完全一致。三轮XeLaTeX、no-shell-escape；`validation/validation_report.json` 自动PASS，日志无超宽、缺字、未定义引用或重复标签。自动工具不判断数学或视觉。

```sh
TEXMFHOME=/workspace/.local/texmf XDG_CACHE_HOME=/tmp/abstract-algebra-fontcache \
python /tmp/abstract-algebra-style/math-latex-typesetting/scripts/validate.py \
/workspace/mit-ocw-notes/subjects/abstract-algebra/main.tex \
--out /workspace/mit-ocw-notes/subjects/abstract-algebra/qa/validation \
--template /workspace/mit-ocw-notes/subjects/probability/main.tex
```

绝对路径只记录执行环境；完整TeX Live环境运行包内build.sh即可。GNU官方HTML→72块JSON→TXT→TeX全部非空白字符由独立审读核对，章节0–10、修改条款A–O及How to use全部保留。`license-pdf-check.json`另核最终PDF第52–58页许可证的全部16303个字母/数字与官方文本一致（NFKC并去空白、标点及换行断词格式）。版权页原著英文notice、致谢与修改版声明保留；不称律师核准。

## 实际逐页视觉与链接

主编实际查看全部58页的29幅可读双页渲染，每页1.45倍PDF尺寸，检查文字、公式、表、页眉页脚、密度、截断与重叠；见 `page-pairs/` 与逐页绑定哈希的 `visual-review.json`。不是以渲染成功或小缩略图代替实际查看。

唯一TikZ域格图在PDF第27页，边、节点、标签无重叠；第9章行内2×2矩阵提醒在PDF第21页实际查看无碰撞。第50页64格表和第51页矩阵均可读、完整，矩阵题题面/矩阵同页。第48–49页为独立版权/历史/致谢页，第52–58页为完整许可证。新增附录曾使末目录页只有一行，去掉参考文献非必要目录行后恢复三页目录，参考文献正文与锁定模板未改。

`pdf-navigation.json`：89个目录条目与89个目录链接，对应标题均在目标页查到；121个总链接全部解析。内部页有效且有文字，外链为明确来源/许可；原著历史网络位置保留原HTTP，其余HTTPS。不替阅读器自身作显示保证。

## 自足源码ZIP与来源

`package_and_rebuild.py` 明确白名单：全部中文数学输入、内嵌模板、构建脚本、说明、覆盖/来源清单、四份完整数学审读及附录必要版权/许可证。英文教材/讲义PDF、原书/官方TeX ZIP、字体、凭据、生成PDF、缓存和构建产物不进包。英文GFDL.txt与许可证TeX是版权附件。源码图由TikZ生成，不依赖其他科目。

干净空目录三轮实际重编已通过，最终包的全部58页文字/72dpi渲染/目录比较及成员SHA见 `clean-rebuild.json`；不声称PDF字节一致，元数据时间可不同。

MIT41资源：39PDF共545页、2官方TeX ZIP，逐件页数、URL、署名、SHA和许可标记见 `../source-manifest.json`。另有作者官网Judson历史PDF442+444页、作者官网与GNU许可HTML/TXT，见 `sources/abstract-algebra/judson-manifest.json` 及归档inventory。合计43资源、41PDF1431页、2TeX ZIP，不称逐页全译。学生笔记未经教师核准；没有未标注权属保证，不复用原图，Herstein未获取。

## 许可与发布

PDF第1–47页原教学主体（前言至参考文献，含第1–17章）保持CC BY-NC-SA 4.0；PDF第48–58页独立附录、对应三个TeX输入和四题审读补充采用GFDL 1.2-or-later。署名、原版权与许可、修改版声明、历史、致谢与完整许可证保留；汇编不向GFDL部分添加非商业限制。详见LICENSE.md。

完成本地关卡后冻结独占文件，不改根README、全局清单、其他科或.agents。原私库阶段使用现有v2.0.1；仓库后续实际为Public，由用户授权普通Git路径提交，未升级/绕过私库上传器安全限制、未生成凭据或改可见性/权限。发布核最新HEAD，正常快进提交/推送，保留并行历史，不force。完整远端路径/字节/SHA、PDF页数和ZIP成员均实际读取核对，最终结果见不可变提交对应交付回执；本地报告不提前声称远端成功。
