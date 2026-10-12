#!/usr/bin/env python3
"""Local UTF-8 prose linter. Risk hints only: NEVER certifies a mathematical proof."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys
from collections import Counter
from tex_scan import mask_noncode, document_body
from tex_project import expand_project

GAP = re.compile(r"显然|容易得到|不难证明|类似可得|标准论证|标准事实|众所周知|one can show|standard arguments?|well[- ]known|clearly", re.I)
PLACEHOLDER = re.compile(r"\b(?:TODO|FIXME|TBD)\b|证明待补|此处省略关键证明|证明略|待补证明", re.I)
GENERIC = re.compile(r"具有重要意义|起着至关重要的作用|不言而喻|为后续学习奠定坚实基础")
HEADING = re.compile(r"^\s*(?:#{1,6}\s+|\\(?:(?:sub)*section|originalchapter|originalsection)\*?\{)")
FIG = re.compile(r"\\includegraphics\b|!\[[^\]]*\]\(|\\begin\{(?:tikzpicture|figure|figure\*)\}|<img\b", re.I)
DRAW = re.compile(r"\\begin\{tikzpicture\}|<svg\b|\\begin\{pspicture\}", re.I)


def strip_tex_comments(text: str) -> str:
    """A percent is escaped iff preceded by an odd number of backslashes."""
    output = []
    for line in text.splitlines():
        end = len(line)
        for i, ch in enumerate(line):
            if ch != "%":
                continue
            n, j = 0, i - 1
            while j >= 0 and line[j] == "\\":
                n += 1
                j -= 1
            if n % 2 == 0:
                end = i
                break
        output.append(line[:end])
    return "\n".join(output)


def mask_code(text: str, tex: bool) -> str:
    """Preserve line numbers when suppressing code/verbatim blocks."""
    if tex:
        cleaned = mask_noncode(text)
        body, offset = document_body(text)
        if offset:
            return "\n" * text.count("\n", 0, offset) + body
        return cleaned
    rows, fence = [], None
    for line in text.splitlines():
        start = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence is None and start:
            fence = start.group(1)
            rows.append("")
        elif fence is not None:
            if re.match(r"^\s*" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*$", line):
                fence = None
            rows.append("")
        else:
            rows.append(line)
    return "\n".join(rows)


def audit_text(text: str, tex: bool = False) -> dict:
    clean = mask_code(text, tex)
    findings = []
    def add(code: str, line: int, message: str) -> None:
        findings.append({"code": code, "line": line, "message": message})
    for i, line in enumerate(clean.splitlines(), 1):
        for code, pat, message in [
            ("gap_phrase", GAP, "核对是否隐藏关键步骤；熟悉的直接推论不必展开"),
            ("placeholder", PLACEHOLDER, "检查是否为尚未补齐的证明，或只是在讨论坏样例"),
            ("generic_prose", GENERIC, "检查是否产生实际数学理解"),
        ]:
            if pat.search(line):
                add(code, i, message + "：" + line.strip()[:150])
    normalized = []
    for m in re.finditer(r"\S[\s\S]*?(?=\n\s*\n|\Z)", clean):
        p = re.sub(r"\s+", " ", m.group()).strip()
        if len(p) >= 100:
            normalized.append((p, clean.count("\n", 0, m.start()) + 1))
        if len(p) >= 500 and len(re.findall(r"因此|从而|于是|可得|所以|hence|therefore", p, re.I)) >= 3:
            add("proposition_cascade_candidate", clean.count("\n", 0, m.start()) + 1,
                "长段落含多次结论跃迁，逐句检查承重命题；这不是自动判错")
    counts = Counter(p for p, _ in normalized)
    emitted = set()
    for p, line in normalized:
        if counts[p] > 1 and p not in emitted:
            emitted.add(p)
            add("duplicate_paragraph", line, f"同一长段落出现 {counts[p]} 次，核对是否确有新用途")
    chars = len(clean)
    headings = sum(bool(HEADING.match(line)) for line in clean.splitlines())
    # Short examples and snippets must not be classified using unstable density ratios.
    if chars >= 1500 and headings >= 4 and headings * 10000 / chars > 18:
        add("heading_density", 1, "标题相对密集，人工核对是否碎片化；不设置全书标题配额")
    if DRAW.search(clean):
        add("self_drawn_qa", 1, "自绘图：按任务核对图源/绘制理由，并实际打开最终页面检查")
    if FIG.search(clean):
        add("figure_qa", 1, "所有图需核对原图与最终嵌入尺寸、标签、数学关系及来源")
    if re.search(r"\\begin\{proof\}\s*\\end\{proof\}", clean):
        add("empty_proof", 1, "空证明环境：核对是否误删正文")
    return {"kind": "heuristic_lint", "mathematical_verification": False,
            "characters": chars, "headings": headings, "findings": findings,
            "limitation": "无风险提示不等于没有错误；风险提示也不等于数学错误。"}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", type=Path)
    ap.add_argument("--json", action="store_true", help="输出 JSON；不写入原文件")
    args = ap.parse_args(argv)
    try:
        if not args.path.is_file():
            raise ValueError("输入不是已存在的文件")
        if args.path.stat().st_size > 20_000_000:
            raise ValueError("文件超过 20 MB，请按章节检查")
        if args.path.suffix.lower() == ".tex":
            project = expand_project(args.path)
            report = audit_text(project.text, True)
            for item in report["findings"]:
                item["file"], item["line"] = project.location(item["line"])
            report["files_checked"] = [p.relative_to(project.root).as_posix() for p in project.files]
        else:
            report = audit_text(args.path.read_text(encoding="utf-8-sig"), False)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"输入错误：{exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("启发式文本检查；不是数学验证器。")
        for item in report["findings"]:
            print(f"{item['code']} @ {item['line']}: {item['message']}")
        print(report["limitation"])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
