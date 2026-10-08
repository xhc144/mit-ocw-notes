#!/usr/bin/env python3
"""Incrementally archive explicitly approved OCW files, or verify local copies.

This script is not a crawler. A researcher must populate manifests/files.json
with verified URLs, attribution, and licensing before --download is used.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler


ALLOWED_HOSTS = frozenset({"ocw.mit.edu"})


def official_url(url: str) -> bool:
    parsed = urlparse(url)
    return (parsed.scheme == "https" and parsed.hostname in ALLOWED_HOSTS
            and parsed.username is None and parsed.password is None
            and parsed.port in (None, 443))


class OfficialRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not official_url(newurl):
            raise ValueError("redirect outside the approved OCW host; review the source")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def local_path(root: Path, value: str) -> Path:
    raw = Path(value)
    if not value or raw.is_absolute() or ".." in raw.parts:
        raise ValueError("manifest path must be a nonempty, safe relative path")
    result = (root / raw).resolve()
    if result == root or not result.is_relative_to(root):
        raise ValueError("manifest path escapes the archive root")
    return result


def digest(path: Path) -> tuple[str, int]:
    hasher = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            hasher.update(block)
            size += len(block)
    return hasher.hexdigest(), size


def verify(entry: dict[str, Any], root: Path) -> dict[str, Any]:
    result = dict(entry)
    path = local_path(root, entry["path"])
    expected = entry.get("sha256")
    if not path.is_file():
        result.update(status="missing", verification="missing")
        return result
    actual, size = digest(path)
    result["observed_sha256"] = actual
    result["observed_bytes"] = size
    if not expected:
        result.update(verification="unrecorded-checksum")
    elif actual != expected:
        result.update(status="checksum-mismatch", verification="failed")
    elif entry.get("bytes") is not None and size != entry["bytes"]:
        result.update(status="size-mismatch", verification="failed")
    else:
        result.update(status="downloaded", verification="passed")
    return result


def archive(entry: dict[str, Any], root: Path, max_bytes: int) -> dict[str, Any]:
    result = dict(entry)
    if entry.get("archive_allowed") is not True:
        result.update(status="held", error="archive permission not yet verified")
        return result
    required = ("url", "course_id", "course_url", "attribution", "license")
    if any(not entry.get(key) for key in required):
        result.update(status="held", error="source or licensing metadata is incomplete")
        return result
    if not official_url(entry["url"]):
        result.update(status="held", error="source URL is outside the approved OCW host")
        return result
    path = local_path(root, entry["path"])
    if path.exists():
        # Never silently replace an existing original or retroactively certify it.
        checked = verify(entry, root)
        if checked.get("verification") != "passed":
            checked["error"] = "existing file needs review; no overwrite attempted"
        return checked
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".part")
    if temporary.exists():
        result.update(status="held", error="partial file already exists; review before retry")
        return result
    opener = build_opener(OfficialRedirects())
    request = Request(entry["url"], headers={"User-Agent": "MIT-OCW-personal-archive/1.0"})
    try:
        with opener.open(request, timeout=60) as response:
            length = response.headers.get("Content-Length")
            if length and int(length) > max_bytes:
                raise ValueError("file exceeds configured size limit; no LFS purchase attempted")
            hasher = hashlib.sha256()
            total = 0
            with temporary.open("xb") as output:
                while block := response.read(1024 * 1024):
                    total += len(block)
                    if total > max_bytes:
                        raise ValueError("file exceeds configured size limit")
                    output.write(block)
                    hasher.update(block)
            if length and total != int(length):
                raise ValueError("incomplete download: Content-Length mismatch")
            actual = hasher.hexdigest()
            if entry.get("sha256") and actual != entry["sha256"]:
                raise ValueError("downloaded checksum differs from the recorded checksum")
            if entry.get("bytes") is not None and total != entry["bytes"]:
                raise ValueError("downloaded size differs from the recorded size")
            # Hard-link publication cannot overwrite a concurrently-created file.
            os.link(temporary, path)
            temporary.unlink()
            result.update(status="downloaded", sha256=actual, bytes=total,
                          verification="passed", final_url=response.geturl(),
                          downloaded_at=datetime.now(timezone.utc).isoformat())
            result.pop("error", None)
    except Exception as exc:
        # Leave a partial download as explicit evidence; never retry a denial.
        result.update(status="failed", error=f"{type(exc).__name__}: {exc}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--manifest", type=Path, default=Path("manifests/files.json"))
    parser.add_argument("--download", action="store_true",
                        help="download planned, licensing-approved missing files")
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--max-mib", type=int, default=90)
    parser.add_argument("--write-manifest", action="store_true",
                        help="atomically save observed results into the same manifest")
    args = parser.parse_args()
    if not 1 <= args.jobs <= 8 or args.max_mib < 1:
        parser.error("jobs must be 1–8 and max-mib must be positive")
    root = args.root.resolve()
    manifest = args.manifest if args.manifest.is_absolute() else root / args.manifest
    document = json.loads(manifest.read_text(encoding="utf-8"))
    entries = document["files"]
    paths = [entry["path"] for entry in entries]
    if len(paths) != len(set(paths)):
        parser.error("duplicate manifest paths must be resolved before execution")
    # Preflight every path before any network or file mutation occurs.
    for path in paths:
        local_path(root, path)
    results: list[dict[str, Any] | None] = [None] * len(entries)
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {
            pool.submit(archive if args.download else verify, entry, root,
                        *([args.max_mib * 1024 * 1024] if args.download else [])): index
            for index, entry in enumerate(entries)
        }
        for future in as_completed(futures):
            index = futures[future]
            try:
                results[index] = future.result()
            except Exception as exc:
                results[index] = {**entries[index], "status": "failed",
                                  "error": f"{type(exc).__name__}: {exc}"}
    report = {"schema_version": document.get("schema_version", 1), "files": results}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.write_manifest:
        document["files"] = results
        document["checked_at"] = datetime.now(timezone.utc).isoformat()
        temporary = manifest.with_name(manifest.name + ".tmp")
        temporary.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")
        temporary.replace(manifest)
    return 0 if all(e.get("verification") == "passed" for e in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
