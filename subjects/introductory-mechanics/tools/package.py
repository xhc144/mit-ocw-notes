#!/usr/bin/env python3
"""Create the standalone source archive; never include build outputs or credentials."""
import hashlib
import json
from pathlib import Path
import zipfile

book = Path(__file__).resolve().parents[1]
repo = book.parents[1]
files = {}
for path in sorted(book.rglob("*")):
    if not path.is_file():
        continue
    rel = path.relative_to(book)
    if any(part in ("build", "__pycache__", ".git") for part in rel.parts):
        continue
    if path.suffix.lower() in (".pdf", ".zip", ".pyc") or path.name.endswith(".tmp.json"):
        continue
    # Review screenshots are in the repository; source rebuilding needs only the exam photo.
    if rel.parts[0] == "qa" and path.suffix.lower() not in (".json", ".md", ".txt"):
        continue
    # These receipts depend on the archive/commit and are published beside the package.
    if path.name in ("PACKAGE-MANIFEST.json", "zip-rebuild-verification.json", "publication-verification.json"):
        continue
    if path.suffix.lower() in (".tex", ".md", ".json", ".py", ".sh", ".txt", ".png") or path.name == ".gitignore":
        files[rel.as_posix()] = path.read_bytes()
frozen = repo / "manifests/introductory-mechanics-sources.json"
if not frozen.is_file():
    frozen = book / "source-manifest.json"
files["source-manifest.json"] = frozen.read_bytes()
inventory = {
    "schema_version": 1,
    "root": "introductory-mechanics/",
    "members": [{"path": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
                for name, data in sorted(files.items())],
    "build": "bash tools/build.sh",
    "note": "Fonts, original OCW PDF archive, generated PDF and external receipts are not bundled."
}
files["PACKAGE-MANIFEST.json"] = (json.dumps(inventory, ensure_ascii=False, indent=2) + "\n").encode()
archive = book / "introductory-mechanics-source.zip"
with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for name, data in sorted(files.items()):
        info = zipfile.ZipInfo("introductory-mechanics/" + name, (2026, 10, 11, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        z.writestr(info, data)
print(json.dumps({"archive": archive.name, "members": len(files), "bytes": archive.stat().st_size,
                  "sha256": hashlib.sha256(archive.read_bytes()).hexdigest()}))
