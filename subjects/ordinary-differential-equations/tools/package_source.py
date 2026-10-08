#!/usr/bin/env python3
"""Package the clean editable Chinese book; English originals remain in sources/."""
import argparse, hashlib, json, zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, default=root / 'ordinary-differential-equations-source.zip')
args = parser.parse_args()
# Explicit compilation closure. Source archives and review caches stay in Git.
allowed_files = {'main.tex', 'LICENSE.md', 'SOURCES.md',
    'tools/build.sh', 'tools/bootstrap_tex.py',
    'vendor/math-latex-typesetting/requirements.txt',
    'vendor/math-latex-typesetting/templates/wangzhe_baiti_style.tex'}
needed_scripts = {'validate.py', 'build_utils.py', 'tex_guard.py', 'tex_project.py',
    'tex_scan.py', 'check_style.py', 'content_style_lint.py', 'log_audit.py',
    'validation_policy.py', 'wangzhe_pdf_audit.py', 'pdf_artifacts.py'}
allowed_files.update('vendor/math-latex-typesetting/scripts/' + n for n in needed_scripts)
allowed_files.update(p.relative_to(root).as_posix() for folder in ('chapters', 'coursework')
    for p in (root / folder).glob('*.tex'))
members = []
for name in sorted(allowed_files):
    path = root / name
    if path.is_symlink() or not path.is_file():
        raise SystemExit(f'Missing or symlink compilation input: {name}')
    members.append((name, path.read_bytes()))
readme = """# 常微分方程与动力系统：中文源码

此包仅包含中文原生 LaTeX 正文、锁定王者模板、必要构建代码及许可来源。
英文课程原件、网页、完整来源清单和审稿记录保留于仓库，不在此包内。
全部图形在 TeX 中以 TikZ/PGF 独立构造；重编无需下载或嵌入任何课程原件。

需要 Python 3.11+、XeLaTeX 与常规 TeX Live 宏包。先安装构建依赖：

```bash
python -m pip install -r vendor/math-latex-typesetting/requirements.txt
python tools/bootstrap_tex.py --texmf-dir .runtime/texmf --cache-dir .runtime/downloads
TEXMFHOME="$PWD/.runtime/texmf" bash tools/build.sh
```

已有 Fandol、CM Unicode 与 ctex 环境时可直接指定 TEXMFHOME 后执行构建。
字体与运行依赖不随包分发；引导脚本使用固定版本并验证下载哈希。
输出为 ordinary-differential-equations.pdf；main.tex 内含实际锁定类文件。
课程署名、编者补充和未公开教材题面边界见 SOURCES.md 与正文；许可见 LICENSE.md。
"""
members.append(('README.md', readme.encode()))
inventory = [{'path': n, 'bytes': len(d), 'sha256': hashlib.sha256(d).hexdigest()} for n,d in members]
members.append(('ZIP-CONTENTS.json', (json.dumps({'format':1,'members':inventory},ensure_ascii=False,indent=2)+'\n').encode()))
with zipfile.ZipFile(args.output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for name, data in members:
        info = zipfile.ZipInfo(name, date_time=(2026,10,8,0,0,0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, data)
print(json.dumps({'members':len(members),'bytes':args.output.stat().st_size,'sha256':hashlib.sha256(args.output.read_bytes()).hexdigest()}))
