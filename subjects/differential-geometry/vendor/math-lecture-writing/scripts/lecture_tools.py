#!/usr/bin/env python3
"""Local prepare/build/render/snapshot utilities. No network, installs or silent font fallback."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from tex_scan import mask_noncode

ROOT = Path(__file__).resolve().parent.parent
FONTS = {".ttf", ".otf", ".ttc", ".woff", ".woff2", ".pfb", ".pfa", ".tfm", ".afm", ".eot", ".otc", ".pfm", ".vf"}
SKIP = {".git", "__pycache__", ".build", "source-materials", "node_modules", ".venv"}
INPUT_EXTS = {".tex", ".bib", ".bst", ".sty", ".cls", ".clo", ".def", ".cfg", ".png", ".jpg", ".jpeg", ".pdf", ".svg", ".eps"}
BUNDLE_EXTS = INPUT_EXTS | {".md", ".txt", ".json", ".yaml", ".yml", ".csv", ".py"}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".write-", suffix=".json", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(value, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def escape_tex(value: str) -> str:
    chars = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
             "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(chars.get(c, c) for c in value)


def iter_project_files(project: Path, allowed: set[str]):
    for path in sorted(project.rglob("*")):
        rel = path.relative_to(project)
        if any(part in SKIP for part in rel.parts):
            continue
        if path.is_symlink():
            raise ValueError("不打包或编译通过符号链接引入的项目文件：" + str(rel))
        if path.is_file() and path.suffix.lower() not in FONTS and path.suffix.lower() in allowed:
            yield path


def prepare(body: Path, out_dir: Path, preview: bool = False, title: str = "", show_title: bool = False, force: bool = False) -> Path:
    if not body.is_file():
        raise ValueError("正文文件不存在")
    text = body.read_text(encoding="utf-8-sig").strip()
    if not text:
        raise ValueError("正文为空")
    if re.search(r"\\(?:documentclass\b|begin\{document\}|end\{document\})", mask_noncode(text)):
        raise ValueError("prepare 只接受正文片段；完整源码直接使用 build")
    template = (ROOT / "assets/yii-lecture-template.tex").read_text(encoding="utf-8")
    for marker in ("@@TITLE@@", "@@TITLEBLOCK@@", "@@BODY@@"):
        if template.count(marker) != 1:
            raise ValueError("模板占位符不唯一：" + marker)
    if preview:
        replacements = {
            r"\setmainfont{Palatino Linotype}": r"\setmainfont{Liberation Serif}",
            r"\setCJKmainfont{SimSun}[BoldFont=SimHei]": r"\setCJKmainfont{Noto Serif CJK SC}[BoldFont=Noto Sans CJK SC]",
            r"\setCJKsansfont{SimHei}": r"\setCJKsansfont{Noto Sans CJK SC}",
        }
        for original, replacement in replacements.items():
            if original not in template:
                raise ValueError("未找到预期字体指令；不能隐式替换未知模板")
            template = template.replace(original, replacement)
        template = "% PREVIEW: explicitly selected substitute fonts; not strict Yii rendering.\n" + template
    document = template.replace("@@TITLE@@", escape_tex(title)).replace("@@TITLEBLOCK@@", r"\maketitle" if show_title else "")
    document = document.replace("@@BODY@@", text)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / ("main.preview.tex" if preview else "main.tex")
    if target.exists() and not force:
        raise ValueError("目标文件已存在；使用其他目录或明确加 --force")
    target.write_text(document + "\n", encoding="utf-8")
    return target


def build(tex: Path, timeout: int = 120) -> Path:
    from build_utils import build as guarded_build
    return Path(guarded_build(tex, out=tex.resolve().parent, timeout=timeout)["pdf"])


def render(pdf: Path, dpi: int = 160) -> Path:
    from pdf_artifacts import render_pdf
    return render_pdf(pdf, dpi=dpi)


def snapshot(project: Path, target: Path) -> Path:
    project, target = project.resolve(), target.resolve()
    if not project.is_dir() or target.is_relative_to(project):
        raise ValueError("项目需存在，快照须保存在项目目录之外")
    if target.exists():
        raise ValueError("快照目标已存在；不覆盖原备份")
    paths = list(iter_project_files(project, BUNDLE_EXTS))
    if not paths:
        raise ValueError("没有可备份的项目文件")
    if any(p.relative_to(project).as_posix() == "SNAPSHOT_MANIFEST.json" for p in paths):
        raise ValueError("项目含保留名称 SNAPSHOT_MANIFEST.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".snapshot-", suffix=".zip", dir=str(target.parent))
    os.close(fd)
    tmp = Path(name)
    try:
        manifest = []
        with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for p in paths:
                payload = p.read_bytes()
                rel = p.relative_to(project).as_posix()
                zf.writestr(rel, payload)
                manifest.append({"path": rel, "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()})
            zf.writestr("SNAPSHOT_MANIFEST.json", json.dumps({"created_at": utc_now(), "files": manifest,
                "excluded": sorted(SKIP), "font_files_included": False}, ensure_ascii=False, indent=2))
        with zipfile.ZipFile(tmp) as zf:
            if zf.testzip() is not None:
                raise ValueError("ZIP 完整性检查失败")
        os.replace(tmp, target)
    finally:
        if tmp.exists():
            tmp.unlink()
    return target


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare", help="用内置 Yii 骨架包装正文；不编译")
    p.add_argument("body", type=Path)
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--preview", action="store_true")
    p.add_argument("--title", default="")
    p.add_argument("--show-title", action="store_true")
    p.add_argument("--force", action="store_true")
    p = sub.add_parser("build", help="实际运行 XeLaTeX；不自动替代字体")
    p.add_argument("tex", type=Path)
    p.add_argument("--timeout", type=int, default=120)
    p = sub.add_parser("render", help="渲染 PDF，检查需随后实际进行")
    p.add_argument("pdf", type=Path)
    p.add_argument("--dpi", type=int, default=160)
    p = sub.add_parser("snapshot", help="把项目可交付文件备份到项目外")
    p.add_argument("project", type=Path)
    p.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    try:
        if a.command == "prepare":
            result = prepare(a.body, a.out_dir, a.preview, a.title, a.show_title, a.force)
        elif a.command == "build":
            result = build(a.tex, a.timeout)
        elif a.command == "render":
            result = render(a.pdf, a.dpi)
        else:
            result = snapshot(a.project, a.out)
        print(result)
    except (OSError, ValueError, RuntimeError, UnicodeError, subprocess.TimeoutExpired) as exc:
        print("操作未完成：" + str(exc), file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
