# 中文 LaTeX 工具链记录

状态: **用户金标准样张编译和官方机械检查通过; 全书完成状态另见 PROGRESS.md**. 工具链检查不代替全书数学及页面审查.

## 授权版式来源

用户上传 `数学LaTeX排版_Skill_v4.0.zip`, SHA256 为 `8590d369c7a5294a9a951b683fd80ae05313d0a5db77ab5bb53dbd71822f4630`. 已检查 ZIP 内路径、符号链接与解包大小. 所需主 SKILL.md、完整 references、完整金标准模板、官方 scripts、原样张及原测试保存于 `vendor/math-latex-typesetting/`; 没有复制字体或旧编译缓存. 各原件哈希记录在其 `SOURCE.json`.

此前 skill 子资源接口无法读取, 经 MCP 根资源的授权 bundle 恢复原文本后, 又与真实上传 ZIP 逐字节比较; 全部 24 份同名文本完全一致. 当前以真实 ZIP 原件为主来源, 不使用凭记忆重写的类.

固定类区 `WZ-LOCKED-CLASS-BEGIN/END` 不作修改. 模板使用 letterpaper 612×792bp, 10pt, Fandol 中文字体, CM Unicode OpenType 西文字体, FandolKai 页眉. 配色、几何参数、行段距、章/节与数学环境均来自金标准.

## 安装及来源

宿主为 Debian 13 (trixie), XeTeX 为 TeX Live 2025/dev/Debian, LaTeX2e 为 2024-11-01, 系统 l3kernel 为 2025-01-18. 原环境没有 xeCJK 和 ctex. 没有用最新 CTAN 宏包覆盖系统内核.

通过 Debian 官方 `https://deb.debian.org/debian` 的签名 InRelease / Packages 索引取得下列匹配包, 经索引 SHA256 验证后本地提取至 `/workspace/.local/texmf`. 不需要 sudo, 不改系统 TeX.

| 包 | 版本 | SHA256 |
| --- | --- | --- |
| texlive-lang-chinese | 2024.20250309-1 | `583cd26483b79d32191a8d0a198e80546415d6eca4f23a4bedd253ebdb661291` |
| texlive-lang-cjk | 2024.20250309-1 | `56c795c17b392766c66132f469aab024c374eb92848685ab1d66072a14115b66` |

Debian 包页面: <https://packages.debian.org/trixie/texlive-lang-chinese>, <https://packages.debian.org/trixie/texlive-lang-cjk>. 宏包许可证随包保存. 包中指向可选独立 Arphic 字体依赖的失效符号链接不复制; 固定模板用的是 Fandol.

固定西文字体要求实际 `cmunrm.otf`, `cmunbx.otf`, `cmunti.otf`, `cmunbi.otf`. Debian fonts-cmu 提供 TTF, 因而没有以重命名 TTF 代替固定 OTF. 使用官方 TeX Live `cm-unicode` 0.7.0, revision 58661 的 OpenType 字体包, 下载 <https://mirrors.ctan.org/systems/texlive/tlnet/archive/cm-unicode.tar.xz>, 与官方 `texlive.tlpdb` 的 `containerchecksum` SHA512 核对相符:

```text
5d6cce2e396ffa0dc887e839f4ef57865db9eda3dcdf6a62737008b53837c40ee1498d97ab06eab8f0802e745787fa5c107c0738a8dedd4e65f6996aee555c48
```

CM Unicode 许可为 OFL. 字体与字体许可仅在运行时 `/workspace/.local/texmf` 依赖缓存中, 字体不纳入仓库或源码交付包. `tools/bootstrap_tex.py` 用固定 URL 和以上已核对校验值复现; 保留 HTTPS / CA 验证, 校验失败即停止, 不安装新 l3kernel.

```sh
cd /workspace/mit-ocw-notes/subjects/topology
python3 tools/bootstrap_tex.py
export TEXMFHOME=/workspace/.local/texmf
export XDG_CACHE_HOME=/workspace/.cache
kpsewhich xeCJK.sty
kpsewhich cmunrm.otf
```

## 已实际执行的样张检查

已完整读取固定 skill 主文件、STYLE_SPEC、ENVIRONMENTS、MATH_LAYOUT、EDITORIAL_RULES、VALIDATION 与完整模板. 官方 `scripts/validate.py` 对原样张实际得到 `AUTOMATED PASS`; source、compile、log、pdf 阶段全通过, 3 页全渲染, 无错误或提醒. 已逐页打开可读尺寸页面: 字体、颜色、目录、行间式、数学环境与空心 QED 正常. 此结果只证明原样张工具链与版式机械检查, 不是全书审查.

另实际用 `--texmf-dir /tmp/topology-toolchain/fresh-texmf` 从空的 TEXMF 树重跑 bootstrap, 两份 Debian 包和 CM Unicode OTF 均从下载缓存重新校验、提取成功. 设置该新树为 TEXMFHOME 后, 同一原样张再次通过官方 `validate.py` 的 source、compile、log、pdf 检查. 这验证本机从缓存重建依赖, 不声称已在另一台云实例复现.

此前通用中文烟雾稿也成功编译, 并核对 2 个书签与 5 个内部链接; 正式书稿以固定样张和最终全书证据为准.

运行时工具为 Python 3.12, XeLaTeX, latexmk 4.86, pdftotext/pdfinfo, PyMuPDF 1.26.6, Pillow 12.3.0. 样张最终日志用的是系统 l3kernel; 系统 expl3.sty SHA256 为 `1841b4d9b33cfd2826939618eb53739cd9360dbef9b7b0e51008e74a2815fa98`.

## 正式全书构建

```sh
cd /workspace/mit-ocw-notes/subjects/topology
bash tools/build.sh main.tex build
python3 tools/audit_pdf.py build/main.pdf --out build/pdf-audit
PYTHONDONTWRITEBYTECODE=1 python3 tools/audit_tex_source.py main.tex --out build/static-source-audit.json
```

`build.sh` 调用原 skill 官方 `validate.py`, 在隔离临时目录构建, 禁用 shell escape, 核对锁定区、环境、最终日志、PDF 尺寸, 并渲染所有页面. 实际输入和最终 PDF SHA256 绑定在 `main.build.json`, 渲染记录在 `main.render.json`; 检查报告保持数学/教学/视觉未自动验证的诚实边界.

`audit_pdf.py` 另核对书签和内部链接是否指向有效页, 保存 PDF SHA256 与每页图片. 所有最终页面必须另行实际打开检查; 数学内容修改后重新构建, 不以旧 PDF 代替新源码.

`audit_tex_source.py` 复用原 skill 的静态输入解析、环境/数学分隔符检查和锁定区比对, 并核对字面标签、引用与书目键. 报告绑定当前全部输入 SHA256; 动态 TeX 和最终 PDF 链接仍需真实编译检查. 最终冻结稿已重跑为 PASS: 11 个输入、168 个唯一标签、32 个引用目标、6 个书目键, 0 错误及 0 提醒, 无重复或未解析目标. `review/source-static-audit.json` 保存该冻结稿证据. 内容变化后需重跑, 不把旧报告视为当前稿证据.

## 内容槽与环境

- 元数据为 `BookTitle`, `BookAuthor`, `BookDate`, `PDFTitle`, `PDFAuthor`. 作者/日期没有提供时留空. 模板不会自动打印标题, 标题文字属于正文内容槽.
- 正文用 `originalchapter{章名}`, `originalsection{节名}`, `originalpreface`, `originalcontents`; 正文从 `mainmatter` 后开始, 可分章 `input`.
- `definition`, `theorem`, `lemma`, `proposition`, `corollary` 共享章内计数器; 定理类可带可选名称. `example`, `exercise` 独立按章编号, 其可选题名会被固定样式丢弃, 不使用方法副标题.
- `remark` 不编号. `proof`, `solution` 自动空心 QED; 须与陈述环境分开. 末尾无编号显示式按实际结构用 `qedhere`, 不手写重复方框.
- 数学内容使用原定记号或添加不冲突的数学记号宏. 不重定义固定类、页眉、字体、章/节、证明或颜色.
