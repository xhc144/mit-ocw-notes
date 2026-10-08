#!/usr/bin/env python3
"""Verify archived source files against the frozen manifest; no network access."""
import hashlib
import json
from pathlib import Path
import subprocess


root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "research/source-manifest.json").read_text())
errors = []
pdf_pages = 0
for item in manifest["files"]:
    path = root / item["path"]
    if not path.is_file():
        errors.append(f"missing: {item['path']}")
        continue
    data = path.read_bytes()
    if len(data) != item["bytes"]:
        errors.append(f"byte count: {item['path']}")
    if hashlib.sha256(data).hexdigest() != item["sha256"]:
        errors.append(f"sha256: {item['path']}")
    if item["kind"] == "pdf":
        if not data.startswith(b"%PDF-"):
            errors.append(f"pdf signature: {item['path']}")
        info = subprocess.check_output(["pdfinfo", str(path)], text=True)
        fields = dict(line.split(":", 1) for line in info.splitlines() if ":" in line)
        pages = int(fields["Pages"])
        pdf_pages += pages
        if pages != item["pdf_pages"]:
            errors.append(f"pdf pages: {item['path']}")
    if "derived_from" in item and not (root / item["derived_from"]).is_file():
        errors.append(f"missing extraction origin: {item['path']}")

if pdf_pages != manifest["counts"]["all_pdf_pages"]:
    errors.append("total PDF page count")
if errors:
    raise SystemExit("\n".join(errors))
print(f"Verified {len(manifest['files'])} files; {sum(row['kind'] == 'pdf' for row in manifest['files'])} PDFs, {pdf_pages} pages.")
