#!/usr/bin/env python3
"""Verify this release's sources, navigation, and clean ZIP compilation.

Run from any directory. Requires PyMuPDF and XeLaTeX (same fonts as main.tex).
The SHA of the ZIP is recorded outside that ZIP to avoid a circular hash.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import zipfile

import fitz

SUBJECT = Path(__file__).resolve().parents[1]
REPO = SUBJECT.parents[1]
BASELINE = "8f7df4aa7b1464124b5344d7e5af7fa51b227850"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def pdf_info(path):
    document = fitz.open(path)
    assert len(document) == 79, (path, len(document))
    toc = document.get_toc()
    assert len(toc) == 38, len(toc)
    expected = {"课程大纲与课历": 2, **{f"{i+7} 作业 {i}": p for i, p in enumerate([62, 63, 66, 68, 70, 72, 75, 77], 1)}}
    for title, page in expected.items():
        matches = [e for e in toc if e[1] == title]
        assert len(matches) == 1 and matches[0][2] == page, (title, matches)
    links = []
    page_hashes = []
    for index, page in enumerate(document):
        for link in page.get_links():
            if link["kind"] in (fitz.LINK_GOTO, fitz.LINK_NAMED):
                assert 0 <= link["page"] < len(document), link
                entry = {"from_physical_page": index+1, "target_physical_page": link["page"]+1}
                if "nameddest" in link:
                    resolved = document.resolve_names()[link["nameddest"]]
                    assert resolved["page"] == link["page"]
                    entry["named_destination"] = link["nameddest"]
                links.append(entry)
            elif link["kind"] == fitz.LINK_URI:
                assert link["uri"].startswith(("https://", "http://")), link
                links.append({"from_physical_page": index+1, "uri": link["uri"]})
            else:
                raise AssertionError(f"Unexpected PDF link: {link}")
        pixmap = page.get_pixmap(matrix=fitz.Matrix(1.55, 1.55), alpha=False)
        page_hashes.append({"physical_page": index+1, "width": pixmap.width, "height": pixmap.height, "rgb_sha256": sha(pixmap.samples)})
    assert len(links) == 80, len(links)
    return {"pages": len(document), "sha256": sha(path.read_bytes()), "outline": toc, "links": links, "page_renders": page_hashes}


def source_checks():
    inventory = json.loads((SUBJECT/"assessment-inventory.json").read_text())
    assert inventory["problem_count"] == 33 and inventory["terminal_unit_count"] == 68
    assert len(inventory["assignments"]) == 8
    count = units = 0
    for index, assignment in enumerate(inventory["assignments"], 1):
        text = (SUBJECT/f"assessments/ps{index:02}.tex").read_text()
        labels = re.findall(r"\\label\{(ps\d+-q\d+)\}", text)
        assert labels == [p["tex_label"] for p in assignment["problems"]]
        assert text.count(r"\begin{exercise}") == assignment["numbered_problems"]
        assert text.count(r"\begin{solution}") == assignment["numbered_problems"]
        assert "AI 编写, 非官方答案" in text
        assert sum(len(p["parts"]) for p in assignment["problems"]) == assignment["terminal_units"]
        original = REPO/assignment["source_path"]
        assert sha(original.read_bytes()) == assignment["source_sha256"]
        assert len(fitz.open(original)) == 2
        count += assignment["numbered_problems"]
        units += assignment["terminal_units"]
    assert (count, units) == (33, 68)
    build = json.loads((SUBJECT/"qa/build-record.json").read_text())
    for item in build["inputs"]:
        assert sha((SUBJECT/item["path"]).read_bytes()) == item["sha256"], item["path"]
    for manifest in ["assessment-sources.json", "course-sources.json"]:
        for record in json.loads((SUBJECT/manifest).read_text()):
            path = REPO/record["archived_path"] if "archived_path" in record else REPO/"sources/18.330-spring-2012"/record["filename"]
            assert sha(path.read_bytes()) == record["sha256"]
            assert path.stat().st_size == record["bytes"]
    preserved = []
    for path in [*sorted((SUBJECT/"chapters").glob("*.tex")), SUBJECT/"figures/runge.tex"]:
        relative = path.relative_to(REPO).as_posix()
        old = subprocess.check_output(["git", "show", f"{BASELINE}:{relative}"], cwd=REPO)
        assert old == path.read_bytes(), relative
        preserved.append({"path": path.relative_to(SUBJECT).as_posix(), "sha256": sha(old)})
    old_main = subprocess.check_output(["git", "show", f"{BASELINE}:subjects/numerical-analysis/main.tex"], cwd=REPO).decode()
    main = (SUBJECT/"main.tex").read_text()
    pattern = r"% WZ-LOCKED-CLASS-BEGIN.*?% WZ-LOCKED-CLASS-END"
    locked = re.search(pattern, main, re.S).group()
    assert locked == re.search(pattern, old_main, re.S).group()
    return {"problems": count, "terminal_units": units, "baseline_commit": BASELINE, "preserved_inputs": preserved, "locked_class_sha256": sha(locked.encode()), "compiled_inputs": build["inputs"]}


def package():
    destination = SUBJECT/"dist/source.zip"
    exclusions = {destination, SUBJECT/"qa/release-verification.json"}
    files = [p for p in SUBJECT.rglob("*") if p.is_file() and p not in exclusions and "__pycache__" not in p.parts and p.suffix not in {".pyc", ".aux", ".log", ".toc", ".out", ".fls", ".fdb_latexmk"}]
    assert not any(p.name.endswith(".cls") for p in files), "Generated class must come from filecontents"
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(files):
            info = zipfile.ZipInfo(path.relative_to(SUBJECT).as_posix(), date_time=(2026,10,8,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    return len(files)


def clean_build(reference):
    with tempfile.TemporaryDirectory(prefix="numerical-clean-", dir="/tmp") as folder:
        root = Path(folder)
        archive_path = SUBJECT/"dist/source.zip"
        with zipfile.ZipFile(archive_path) as archive:
            assert archive.testzip() is None
            for name in archive.namelist():
                assert not name.startswith("/") and ".." not in Path(name).parts
            archive.extractall(root)
        for record in reference["compiled_inputs"]:
            assert sha((root/record["path"]).read_bytes()) == record["sha256"]
        env = dict(os.environ, SOURCE_DATE_EPOCH="1791417600", FORCE_SOURCE_DATE="1")
        for iteration in range(3):
            proc = subprocess.run(["xelatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", "main.tex"], cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            assert proc.returncode == 0, proc.stdout[-5000:]
        log = (root/"main.log").read_text()
        class_notice = "LaTeX Warning: Writing or overwriting file `elegantbook-original-adapter.cls'."
        warnings = [line for line in log.splitlines() if any(x in line for x in ["Overfull", "Underfull", "Missing character", "Warning:"]) and line != class_notice]
        assert not warnings, warnings
        rebuilt = pdf_info(root/"main.pdf")
        official = pdf_info(SUBJECT/"dist/main.pdf")
        assert rebuilt["outline"] == official["outline"]
        assert rebuilt["links"] == official["links"]
        assert rebuilt["page_renders"] == official["page_renders"]
        return {"status": "PASS", "passes": 3, "pages": rebuilt["pages"], "rebuilt_pdf_sha256": rebuilt["sha256"], "distributed_pdf_sha256": official["sha256"], "pdf_bytes_equal": rebuilt["sha256"] == official["sha256"], "all_page_pixels_equal": True, "navigation_equal": True, "all_compiled_input_hashes_equal": True, "log_warnings": warnings, "expected_class_generation_notice": class_notice}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", action="store_true")
    parser.add_argument("--clean-build", action="store_true")
    args = parser.parse_args()
    sources = source_checks()
    document = pdf_info(SUBJECT/"dist/main.pdf")
    write_json(SUBJECT/"qa/source-verification.json", sources)
    write_json(SUBJECT/"qa/page-render-hashes.json", {"pdf_sha256": document["sha256"], "dpi_equivalent": 111.6, "pages": document["page_renders"], "actual_visual_review": [{"reviewer": "primary AI editor", "physical_pages": [1,61]}, {"reviewer": "independent AI PS1-PS4 reviewer", "physical_pages": [62,70]}, {"reviewer": "independent AI PS5-PS8 reviewer", "physical_pages": [70,79]}]})
    write_json(SUBJECT/"qa/navigation-verification.json", {key:document[key] for key in ["pages", "sha256", "outline", "links"]})
    release = {"status": "PASS", "pages": document["pages"], "pdf_sha256": document["sha256"], "source_check": {"problems": sources["problems"], "terminal_units": sources["terminal_units"]}}
    if args.package:
        release["zip_file_count"] = package()
    if args.clean_build:
        release["clean_rebuild"] = clean_build(sources)
    archive = SUBJECT/"dist/source.zip"
    release["zip_sha256"] = sha(archive.read_bytes())
    release["zip_bytes"] = archive.stat().st_size
    write_json(SUBJECT/"qa/release-verification.json", release)
    print(json.dumps(release, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
