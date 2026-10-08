# 度量空间与基础拓扑

状态：整册编写与审校进行中，尚未完成 PDF 和逐页核验。不要将本阶段标为完整交付。

主源为 MIT OCW 18.S190 Introduction to Metric Spaces, January IAP 2023（Paige Bright）。中文按概念重新编排，补齐论证与勘误；一般拓扑、Picard、Baire 及函数空间紧性等标明编者补充。详细新领军考纲原 PDF 本次未能重新获取；已核最新版官方简章及考纲发布通知，证据边界见 `research/syllabus-verification.md` 和书前说明。

## 文件

- `main.tex`：一本书的编译入口，原样保留用户固定模板的锁定类，按章 `input`。
- `frontmatter.tex`、`references.tex`：读者范围、章节映射、署名和许可。
- `chapters/01-*.tex` 至 `08-*.tex`：可编辑的分章原生 LaTeX。
- `sources/`：授权归档的主课 PDF、官方 TeX、原习题与选读补充，逐课程有 `SOURCE.json`。
- `research/`：来源完整性、原稿勘误、逐页阅读记录、考纲核实与范围边界。
- `review/`：作者及交叉数学审校证据；不能替代整册 PDF 页面检查。
- `vendor/math-latex-typesetting/`：用户上传 v4.0.0 的原模板、规则与官方验证器，模板不是另行设计的主题；不捆绑字体。
- `tools/`：本地 TeX 依赖引导、编译与 PDF 链接核查。

## 构建

```sh
cd /workspace/mit-ocw-notes/subjects/topology
python3 tools/bootstrap_tex.py
export TEXMFHOME=/workspace/.local/texmf
export XDG_CACHE_HOME=/workspace/.cache
export PYTHONDONTWRITEBYTECODE=1
python3 vendor/math-latex-typesetting/scripts/validate.py main.tex --out build
python3 tools/audit_pdf.py build/main.pdf --out build/pdf-audit
python3 vendor/math-lecture-writing/scripts/audit_lecture.py main.tex --json
python3 vendor/math-lecture-writing/scripts/check_project.py . --main main.tex
python3 research/verify-sources.py
```

依赖下载保持 HTTPS 与固定校验和验证。`build/` 是本机临时编译与渲染证据，不加入 Git；发布后的最终 PDF 和源 ZIP 将放本目录根。各个数学/机械/视觉检查分别记录，模板验证器不会自动证明数学正确。

## 来源和许可

中文译编、重排、修正与增补采用 **CC BY-NC-SA 4.0**；原课作者、学期、官网链接、原件校验和与第三方例外见 `sources/ATTRIBUTION.md`。原习题没有公开官方答案，本书自编练习和题解不冒称 OCW 答案。MIT 和原作者不为本项目背书。固定 Skill 的源码/模板按用户提供的包用于本项目，字体从正规运行时依赖安装而不分发。

本次工作只提交 `subjects/topology/`；未编辑其他学科或全局清单。
