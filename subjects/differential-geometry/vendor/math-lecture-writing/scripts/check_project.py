#!/usr/bin/env python3
"""Check audit records and current files; never infer mathematical/visual truth from records."""
from __future__ import annotations
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import sys
from urllib.parse import urlparse
from tex_scan import mask_noncode
from tex_project import expand_project
from artifact_records import verify_records

GATES = ("mathematics", "pedagogy", "sources", "visuals", "layout", "delivery")
HASH = re.compile(r"^[0-9a-f]{64}$")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def safe_file(root: Path, rel: str) -> Path:
    if not isinstance(rel, str) or not rel.strip() or "\x00" in rel:
        raise ValueError("路径必须是非空相对路径")
    p = PurePosixPath(rel.replace("\\", "/"))
    if p.is_absolute() or PureWindowsPath(rel).drive or ".." in p.parts:
        raise ValueError("不接受绝对路径、驱动器路径或上级目录")
    q = (root / Path(*p.parts)).resolve()
    if not q.is_relative_to(root.resolve()):
        raise ValueError("路径或符号链接逃出项目目录")
    if not q.is_file() or q.stat().st_size == 0:
        raise ValueError("文件不存在、不是文件或为空")
    return q


def web_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        p = urlparse(value)
        return p.scheme in ("https", "http") and bool(p.netloc)
    except ValueError:
        return False


def validate(root: Path, data: dict) -> dict:
    errors, warnings = [], []
    if not isinstance(data, dict):
        return {"mechanical_checks_passed": False, "errors": ["顶层必须为 JSON 对象"], "warnings": [], "mathematical_verification": False}
    def error(message: str) -> None:
        errors.append(message)
    def items(key: str) -> list[dict]:
        value = data.get(key)
        if not isinstance(value, list) or not all(isinstance(x, dict) for x in value):
            error(f"{key} 必须为对象数组")
            return []
        return value
    def bound_file(entry: dict, context: str) -> Path | None:
        try:
            path = safe_file(root, entry.get("path", ""))
            digest = entry.get("sha256", "")
            if not isinstance(digest, str) or not HASH.fullmatch(digest) or sha256(path) != digest:
                error(context + "：哈希缺失或已过期")
            return path
        except (ValueError, OSError) as exc:
            error(context + "：" + str(exc))
            return None
    def unique(entries: list[dict], context: str) -> dict:
        index = {}
        for entry in entries:
            ident = entry.get("id")
            if not isinstance(ident, str) or not ident:
                error(context + "：缺少字符串 id")
            elif ident in index:
                error(context + "：重复 id " + ident)
            else:
                index[ident] = entry
        return index
    if type(data.get("schema_version")) is not int or data.get("schema_version") not in (1, 2):
        error("不支持的 schema_version")
    scope = data.get("scope", {})
    if not isinstance(scope, dict):
        scope = {}
    if scope.get("status") != "complete" or not scope.get("topic") or not scope.get("audience"):
        error("范围尚未完成，或缺少主题/读者")
    units = scope.get("units", [])
    if not isinstance(units, list) or not units or not all(isinstance(x, dict) for x in units):
        error("必须记录实际教学单元")
        units = []
    unique(units, "教学单元")
    for unit in units:
        if unit.get("status") != "complete" or not unit.get("goal"):
            error("未完成教学单元：" + str(unit.get("id")))
    bindings = items("review_snapshot")
    if not bindings:
        error("缺少审核时文件快照")
    snapshots = {}
    for entry in bindings:
        path = bound_file(entry, "审核快照")
        if path:
            if path in snapshots:
                error("审核快照存在重复路径")
            snapshots[path] = entry.get("sha256")
    def require_snapshot(path: Path | None, context: str) -> None:
        if path and path not in snapshots:
            error(context + "：未纳入审核快照")
    sources = unique(items("sources"), "来源")
    for ident, source in sources.items():
        if not source.get("title") or not source.get("authors"):
            error("来源元数据不完整：" + ident)
        if not web_url(source.get("url")) and not source.get("path") and not source.get("publication"):
            error("来源缺少网页、本地原件或完整出版信息：" + ident)
        if source.get("path"):
            try:
                safe_file(root, source["path"])
            except (ValueError, OSError) as exc:
                error("本地来源无效：" + ident + ": " + str(exc))
        if not source.get("accessed_on") or not source.get("locator"):
            error("来源缺少核验日期或所读位置：" + ident)
    claims = unique(items("claims"), "命题")
    if not claims:
        warnings.append("没有登记命题；人工确认该任务确实不含须审计的核心结论")
    indegree, outgoing = {k: 0 for k in claims}, {k: [] for k in claims}
    for ident, claim in claims.items():
        if not claim.get("statement") or not isinstance(claim.get("central"), bool):
            error("命题缺少陈述或 central 布尔值：" + ident)
        deps = claim.get("dependencies", [])
        if not isinstance(deps, list) or not all(isinstance(d, str) for d in deps):
            error("依赖必须是字符串数组：" + ident)
            deps = []
        for dep in set(deps):
            if dep not in claims:
                error(f"未知依赖：{ident} -> {dep}")
            else:
                indegree[ident] += 1
                outgoing[dep].append(ident)
        support = claim.get("support", {})
        if not isinstance(support, dict):
            support = {}
        kind = support.get("kind")
        if kind not in ("local_proof", "earlier_proof", "prerequisite", "external"):
            error("命题缺少有效支持：" + ident)
        proof_required = claim.get("proof_required", claim.get("central") is True)
        if not isinstance(proof_required, bool):
            error("proof_required 必须是布尔值：" + ident)
        if proof_required is True and kind not in ("local_proof", "earlier_proof"):
            error("当前目标要求证明，不能只外引或声明为先修：" + ident)
        if claim.get("central") is True and proof_required is False and not claim.get("proof_scope_reason"):
            error("核心结论采用引用版须说明实际任务/先修依据：" + ident)
        if claim.get("central") is True and not claim.get("bottleneck"):
            error("核心命题未描述具体理解重点：" + ident)
        if kind in ("local_proof", "earlier_proof"):
            try:
                path = safe_file(root, support.get("path", ""))
                require_snapshot(path, "命题 " + ident)
                marker = support.get("marker", "")
                text = path.read_text(encoding="utf-8-sig")
                if path.suffix.lower() == ".tex":
                    text = mask_noncode(text)
                if not isinstance(marker, str) or not marker or marker not in text:
                    error("证明定位标记缺失：" + ident)
            except (ValueError, OSError, UnicodeError) as exc:
                error("命题 " + ident + "：" + str(exc))
        elif kind == "external":
            source_id = support.get("source_id")
            source = sources.get(source_id) if isinstance(source_id, str) else None
            if not source or source.get("read_level") not in ("relevant_sections", "full_text"):
                error("外部命题缺少已读相关正文的来源：" + ident)
            if not support.get("hypotheses_checked") or not support.get("locator"):
                error("外部命题未记录版本条件对齐：" + ident)
        elif kind == "prerequisite" and not support.get("reader_basis"):
            error("先修声明缺少读者依据：" + ident)
        review = claim.get("review", {})
        if not isinstance(review, dict) or review.get("status") != "pass" or not review.get("note"):
            error("命题尚无具体复核记录：" + ident)
    queue = deque(k for k, value in indegree.items() if value == 0)
    visited = 0
    while queue:
        key = queue.popleft()
        visited += 1
        for nxt in outgoing[key]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    if visited != len(claims):
        error("证明依赖图含循环")
    figures = unique(items("figures"), "图片")
    for ident, figure in figures.items():
        path = bound_file(figure, "图片 " + ident)
        require_snapshot(path, "图片 " + ident)
        origin = figure.get("origin")
        if origin not in ("external", "self_drawn", "user_supplied"):
            error("图片 origin 无效：" + ident)
        if origin != "user_supplied" and not figure.get("search_record"):
            error("图片缺少先搜原图/能力限制的记录：" + ident)
        if origin == "external" and (not web_url(figure.get("source_url")) or not figure.get("source_locator")):
            error("外部图片缺少原始来源/原页定位：" + ident)
        if origin == "self_drawn" and not figure.get("fallback_reason"):
            error("自绘图片未解释原图为何不适合：" + ident)
        if figure.get("reuse_status") not in ("allowed", "permission_obtained", "user_provided", "original") or not figure.get("reuse_note"):
            error("图片复用状态未解决或未说明：" + ident)
        page = figure.get("final_page")
        if not isinstance(page, int) or isinstance(page, bool) or page < 1:
            error("图片最终页码无效：" + ident)
        rendered = {"path": figure.get("render_path"), "sha256": figure.get("render_sha256")}
        require_snapshot(bound_file(rendered, "图片最终渲染 " + ident), "图片最终渲染 " + ident)
        if figure.get("inspected") is not True or not figure.get("review_note"):
            error("图片未记录实际视觉审核：" + ident)
    reviews = data.get("reviews", {})
    if not isinstance(reviews, dict):
        reviews = {}
    for key in GATES:
        review = reviews.get(key, {})
        if not isinstance(review, dict):
            review = {}
        status = review.get("status")
        if status not in ("pass", "not_applicable") or not review.get("note") or not review.get("reviewer"):
            error("验收项缺少实际审核记录：" + key)
        if status == "not_applicable" and (key in ("mathematics", "pedagogy", "delivery") or (key == "visuals" and figures)):
            error("不能把必要验收项标为不适用：" + key)
    deliverables = items("deliverables")
    if not deliverables:
        error("没有交付文件")
    has_pdf = False
    document_pdfs = []
    delivered_paths = set()
    for entry in deliverables:
        path = bound_file(entry, "交付文件")
        require_snapshot(path, "交付文件")
        if path:
            delivered_paths.add(path)
        if path and path.suffix.lower() == ".pdf":
            if entry.get("role") != "asset":
                has_pdf = True
                document_pdfs.append(path)
            with path.open("rb") as stream:
                if stream.read(5) != b"%PDF-":
                    error("扩展名为 PDF，但没有 PDF 文件头")
    if has_pdf:
        if len(document_pdfs) != 1:
            error("每份项目记录只核验一份主 PDF；分册请分别建立记录")
        build_ref = data.get("build_record")
        try:
            record_path = safe_file(root, build_ref)
            require_snapshot(record_path, "编译记录")
            record = json.loads(record_path.read_text(encoding="utf-8"))
            if not isinstance(record, dict) or record.get("status") != "built":
                error("PDF 未有成功编译记录")
                record = {}
            pdf = record.get("pdf", {})
            if isinstance(pdf, dict):
                pdf_path = bound_file(pdf, "编译产物")
                if pdf_path not in document_pdfs:
                    error("编译记录指向的 PDF 不在主文档交付清单中")
            else:
                error("编译 PDF 记录无效")
            inputs = record.get("inputs", [])
            if not isinstance(inputs, list) or not inputs:
                error("编译记录未绑定输入源码")
                inputs = []
            for item in inputs:
                if isinstance(item, dict):
                    require_snapshot(bound_file(item, "编译输入"), "编译输入")
                else:
                    error("无效编译输入")
        except (ValueError, TypeError, OSError, json.JSONDecodeError) as exc:
            error("PDF 编译记录错误：" + str(exc))
        layout = reviews.get("layout", {})
        if not isinstance(layout, dict) or layout.get("status") != "pass":
            error("PDF 排版没有实际审核通过记录")
        try:
            render_path = safe_file(root, data.get("render_record"))
            require_snapshot(render_path, "渲染记录")
            rendering = json.loads(render_path.read_text(encoding="utf-8"))
            if not isinstance(rendering, dict):
                raise ValueError("渲染记录必须为对象")
            render_pdf = rendering.get("pdf", {})
            if not isinstance(render_pdf, dict):
                raise ValueError("渲染 PDF 绑定无效")
            actual_pdf = bound_file(render_pdf, "渲染所用 PDF")
            if actual_pdf not in document_pdfs:
                error("渲染记录与主文档 PDF 不一致")
            pages = rendering.get("pages", [])
            if not isinstance(pages, list) or not pages:
                raise ValueError("渲染记录缺少页面")
            page_map = {}
            for page in pages:
                if not isinstance(page, dict):
                    error("无效渲染页面记录")
                    continue
                number = page.get("page")
                if not isinstance(number, int) or isinstance(number, bool) or number < 1 or number in page_map:
                    error("渲染页码无效或重复")
                    continue
                page_file = bound_file(page, "渲染页面")
                require_snapshot(page_file, "渲染页面")
                page_map[number] = page_file
            if sorted(page_map) != list(range(1, len(page_map) + 1)):
                error("渲染页序不连续")
            for ident, figure in figures.items():
                number = figure.get("final_page")
                if isinstance(number, int) and not isinstance(number, bool):
                    expected = page_map.get(number)
                else:
                    expected = None
                try:
                    inspected_page = safe_file(root, figure.get("render_path", ""))
                    if expected is None or inspected_page != expected:
                        error("图片审核所用页面不匹配当前 PDF 渲染页：" + ident)
                except (ValueError, OSError) as exc:
                    error("图片审核页面无效：" + ident + ": " + str(exc))
        except (ValueError, TypeError, OSError, json.JSONDecodeError) as exc:
            error("PDF 渲染记录错误：" + str(exc))
    if has_pdf:
        actual = verify_records(root, data.get("build_record"), data.get("render_record"), require_render=True)
        errors.extend(actual["errors"])
        warnings.extend(actual["warnings"])
    warnings.append("记录一致不等于内容正确；脚本不能证明语义判断或视觉检查实际发生。")
    return {"mechanical_checks_passed": not errors, "mathematical_verification": False,
            "errors": errors, "warnings": warnings}


def check_files(root: Path, main: str = "main.tex") -> dict:
    root = root.resolve()
    project = expand_project(safe_file(root, main))
    evidence_root = project.main.parent
    build_candidates = [evidence_root / project.main.with_suffix(".build.json").name, evidence_root / "build" / project.main.with_suffix(".build.json").name]
    build_path = next((p for p in build_candidates if p.is_file()), None)
    render_path = build_path.with_name(build_path.name.replace(".build.json", ".render.json")) if build_path else None
    result = verify_records(evidence_root, build_path.relative_to(evidence_root).as_posix() if build_path else None,
        render_path.relative_to(evidence_root).as_posix() if render_path and render_path.is_file() else None,
        require_render=False)
    result.update(mechanical_checks_passed=not result["errors"], review_status="not_provided",
        files_checked=[p.relative_to(root).as_posix() for p in project.files],
        limitation="仅检查文件、依赖和已有构建证据；未提供语义审核记录，不能声明数学/教学已通过。")
    return result


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("root", type=Path)
    ap.add_argument("--record", default=None)
    ap.add_argument("--main", default="main.tex")
    args = ap.parse_args(argv)
    try:
        record = args.record or ("project-review.json" if (args.root / "project-review.json").is_file() else None)
        if record:
            path = safe_file(args.root.resolve(), record)
            if path.stat().st_size > 10_000_000:
                raise ValueError("审核记录过大，请拆分项目")
            data = json.loads(path.read_text(encoding="utf-8-sig"))
            report = validate(args.root.resolve(), data)
        else:
            report = check_files(args.root, args.main)
    except (OSError, ValueError, TypeError, ImportError) as exc:
        print(json.dumps({"mechanical_checks_passed": False, "errors": [str(exc)]}, ensure_ascii=False))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["mechanical_checks_passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
