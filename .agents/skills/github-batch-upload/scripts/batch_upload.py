#!/usr/bin/env python3
"""Manifest-driven, isolated Git batching. Dry-run by default; stdlib only.

No credentials are generated, read from files, printed, or configured here.
Existing Git/gh authorization is used. Publication needs task authorization;
respect existing denials. A supplied checkpoint freezes files across retries.
"""
from __future__ import annotations

import argparse
from contextvars import ContextVar
from contextlib import contextmanager, nullcontext
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import signal
import stat
import subprocess
import tempfile
import threading
import time
import random

RETRY = ContextVar("retry", default=(0, 1.0))
RETRY_EVENTS = ContextVar("retry_events", default=None)
DETECT_ONLY_LFS = ContextVar("detect_only_lfs", default=False)
VERIFY_ONLY = ContextVar("verify_only", default=False)


COMMAND_TIMEOUT = ContextVar("command_timeout", default=120.0)
UNSAFE_GIT_ENV = frozenset({
    "GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_NAMESPACE",
    "GIT_QUARANTINE_PATH", "GIT_SHALLOW_FILE", "GIT_CONFIG_PARAMETERS",
    "GIT_LFS_PROGRESS",
})


class Stop(Exception):
    def __init__(self, code, **details):
        self.code, self.details = code, details
        super().__init__(code)


def check_environment():
    # Fail closed rather than quietly redirecting the caller's repository/index.
    if any(key in os.environ for key in UNSAFE_GIT_ENV):
        raise Stop("UNSAFE_GIT_ENVIRONMENT")


def command_environment(env=None):
    check_environment()
    active = os.environ.copy()
    active.update(GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="never",
                  GIT_LFS_SKIP_SMUDGE="1")
    if env:
        active.update(env)
    return active


def kill_process(process):
    # Include filters, hooks and transport children in the timeout boundary.
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def run(args, cwd=None, data=None, env=None, timeout=None, allowed_returncodes=(0,)):
    # Do not expose raw stderr: platform authorization wrappers can mention secrets.
    active = command_environment(env)
    process = None
    try:
        process = subprocess.Popen(args, cwd=cwd, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   env=active, start_new_session=True)
        stdout, stderr = process.communicate(data, timeout=COMMAND_TIMEOUT.get() if timeout is None else timeout)
    except subprocess.TimeoutExpired:
        kill_process(process)
        process.communicate()
        raise Stop("COMMAND_TIMEOUT", program=Path(args[0]).name)
    except OSError:
        if process is not None:
            kill_process(process)
            process.communicate()
        raise Stop("COMMAND_UNAVAILABLE", program=Path(args[0]).name)
    except BaseException:
        if process is not None:
            kill_process(process)
            process.communicate()
        raise
    if process.returncode not in allowed_returncodes:
        msg = (stderr + stdout).lower()
        code = classify_failure(msg)
        details = {"program": Path(args[0]).name, "exit_code": process.returncode}
        if code == "REMOTE_RATE_LIMITED":
            match = re.search(rb"retry-after[: =]+([0-9]+)", msg)
            details["retry_after"] = int(match[1]) if match else 60
        raise Stop(code, **details)
    return stdout



def classify_failure(msg):
    msg = msg.lower()
    # Authentication, hooks, ref conflicts and explicit denials never become retryable.
    if re.search(rb"(?:http[^\n]{0,30}|error[^\n]{0,20}|status[: =]*)(?<![a-z0-9])(?:401|403)(?![a-z0-9])", msg) or any(x in msg for x in (b"authentication failed", b"could not read username", b"forbidden")):
        return "AUTH_DENIED"
    if any(x in msg for x in (b"hook declined", b"hook rejected", b"protected branch", b"permission denied", b"non-fast-forward", b"fetch first")):
        return "COMMAND_FAILED"
    if re.search(rb"(?:http[^\n]{0,30}|error[^\n]{0,20}|status[: =]*)(?:429)\b", msg) or b"too many requests" in msg:
        return "REMOTE_RATE_LIMITED"
    if re.search(rb"(?:http[^\n]{0,30}|error[^\n]{0,20}|status[: =]*)(?:500|502|503|504)\b", msg) or any(x in msg for x in (b"connection reset", b"connection timed out", b"remote end hung up", b"could not resolve host", b"failed to connect")):
        return "REMOTE_TRANSIENT_ERROR"
    return "COMMAND_FAILED"


TRANSIENT = {"COMMAND_TIMEOUT", "REMOTE_RATE_LIMITED", "REMOTE_TRANSIENT_ERROR"}


def backoff(error, attempt, scope):
    _, delay = RETRY.get()
    seconds = max(delay * 2 ** attempt + random.uniform(0, delay / 4), error.details.get("retry_after", 0))
    if seconds >= 60:
        raise Stop("RETRY_DEFERRED", retry_after_seconds=seconds, cause=error.code)
    events = RETRY_EVENTS.get()
    if events is not None:
        events.append({"scope": scope, "cause": error.code, "retry": attempt + 1, "wait_seconds": round(seconds, 3)})
    # Small waits remain interruptible; a long rate-limit wait is deferred to the caller.
    deadline = time.monotonic() + seconds
    while (remaining := deadline - time.monotonic()) > 0:
        time.sleep(min(remaining, 0.5))


def remote_read(operation, scope):
    for attempt in range(RETRY.get()[0] + 1):
        try:
            return operation()
        except Stop as error:
            if error.code not in TRANSIENT or attempt == RETRY.get()[0]:
                raise
            backoff(error, attempt, scope)


def reject_secret_path(value):
    parts = PurePosixPath(value).parts
    denied = {".aws", ".ssh", ".netrc", "_netrc", ".git-credentials", ".npmrc", ".pypirc", "credentials", "credentials.json", "id_rsa", "id_ed25519"}
    if any(x.casefold() in denied or x.casefold() == ".env" or x.casefold().startswith(".env.") or x.casefold().endswith((".pem", ".key", ".p12", ".pfx")) for x in parts):
        raise Stop("CREDENTIAL_PATH_REJECTED", path=value)


SECRET_PATTERNS = (
    rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----",
    rb"(?:gh[pousr]_)[A-Za-z0-9]{20,}", rb"github_pat_[A-Za-z0-9_]{30,}",
    rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
    rb"(?i)authorization[ \t]*[:=][ \t]*[\"']?(?:bearer|basic)[ \t]+[A-Za-z0-9+/_.=-]{16,}",
    rb"(?i)(?:password|passwd|api[_-]?key|access[_-]?token|client[_-]?secret)[ \t]*[\"']?[ \t]*[:=][ \t]*[\"']([A-Za-z0-9+/_.=-]{16,})[\"']",
)


def scan_secret_bytes(chunk, path):
    if any(re.search(pattern, chunk) for pattern in SECRET_PATTERNS):
        raise Stop("SECRET_CONTENT_REJECTED", path=path)


def validate_snapshot(path, f):
    if path.is_symlink():
        raise Stop("CHECKPOINT_SYMLINK")
    digest, size, tail = hashlib.sha256(), 0, b""
    with path.open("rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise Stop("CHECKPOINT_NONREGULAR")
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk); size += len(chunk)
    if digest.hexdigest() != f["sha256"]:
        raise Stop("CHECKPOINT_HASH_MISMATCH", path=f["path"])
    f["snapshot"], f["size"] = path, size


def private_directory(path):
    path = Path(path).absolute()
    for parent in reversed((path, *path.parents)):
        if parent.is_symlink():
            raise Stop("CHECKPOINT_SYMLINK")
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    info = path.stat()
    if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) & 0o077:
        raise Stop("CHECKPOINT_NOT_PRIVATE")
    return path


@contextmanager
def process_lock(directory, key):
    import fcntl
    directory = private_directory(directory)
    fd = os.open(directory / key, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_nlink != 1:
            raise Stop("INVALID_LOCK_FILE")
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise Stop("WRITER_LOCKED") from None
        yield
    finally:
        os.close(fd)


class Checkpoint:
    def __init__(self, path, manifest, source_root, test_remote):
        self.path = private_directory(path)
        self.file = self.path / "state.json"
        self.identity = {"manifest": json.loads(json.dumps(manifest)), "source_root": str(source_root), "test_remote": str(test_remote) if test_remote else None}
        self.digest = hashlib.sha256(json.dumps(self.identity, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        if self.file.exists() or self.file.is_symlink():
            if self.file.is_symlink() or not self.file.is_file():
                raise Stop("CHECKPOINT_SYMLINK")
            try:
                self.state = json.loads(self.file.read_text())
            except (ValueError, OSError):
                raise Stop("INVALID_CHECKPOINT") from None
            if not isinstance(self.state, dict) or self.state.get("version") != 1 or self.state.get("manifest_id") != self.digest or self.state.get("identity") != self.identity:
                raise Stop("CHECKPOINT_TARGET_OR_MANIFEST_MISMATCH")
            if self.state.get("last_error") in {"AUTH_DENIED", "COMMAND_FAILED", "REPOSITORY_NOT_ACTIVE_PRIVATE", "PUSH_PERMISSION_UNCONFIRMED"}:
                raise Stop("CHECKPOINT_DENIAL_REQUIRES_REVIEW", cause=self.state["last_error"])
        else:
            self.state = {"version": 1, "manifest_id": self.digest, "identity": self.identity, "snapshots": []}
            self.save()

    def save(self, **values):
        self.state.update(values)
        fd, temporary_name = tempfile.mkstemp(prefix=".state-", dir=self.path)
        temporary = Path(temporary_name)
        with os.fdopen(fd, "w") as stream:
            json.dump(self.state, stream, ensure_ascii=False, sort_keys=True, indent=2)
            stream.flush(); os.fsync(stream.fileno())
        os.replace(temporary, self.file)
        fd = os.open(self.path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)

    def freeze(self, m, root, workers):
        snapshots = private_directory(self.path / "snapshots")
        def one(i, f):
            saved = snapshots / str(i)
            if saved.exists() or saved.is_symlink():
                validate_snapshot(saved, f)
                return i, True
            pending = snapshots / (str(i) + ".pending")
            if pending.exists() or pending.is_symlink():
                if pending.is_symlink():
                    raise Stop("CHECKPOINT_SYMLINK")
                shutil.rmtree(pending)
            pending.mkdir(mode=0o700)
            try:
                snapshot_sources({"files": [f]}, root, pending)
                os.replace(pending / "0", saved)
                f["snapshot"] = saved
            finally:
                shutil.rmtree(pending)
            return i, False
        reused = 0
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(one, i, f) for i, f in enumerate(m["files"])]
            for future in as_completed(futures):
                i, was_reused = future.result()
                reused += was_reused
                completed = set(self.state["snapshots"]); completed.add(i)
                self.save(snapshots=sorted(completed))
        return reused


@contextmanager
def phase(report, name):
    start = time.perf_counter()
    try:
        yield
    finally:
        report.setdefault("timings_seconds", {})[name] = round(time.perf_counter() - start, 6)


def git(cwd, *args, data=None):
    return run(["git", *args], cwd=cwd, data=data)


def safe_relative(value, kind):
    if not isinstance(value, str) or not value or "\\" in value:
        raise Stop("INVALID_PATH", kind=kind)
    parts = value.split("/")
    if (PurePosixPath(value).is_absolute() or any(p in ("", ".", "..") for p in parts)
            or any(ord(c) < 32 or ord(c) == 127 for c in value)
            or any(p.casefold() == ".git" for p in parts)):
        raise Stop("INVALID_PATH", kind=kind)
    if kind == "target" and any(p in (".gitattributes", ".lfsconfig", ".gitmodules") for p in parts):
        raise Stop("PROTECTED_RULE_FILE")
    return value


def load_manifest(path, validate_branch_git=True):
    def unique_pairs(pairs):
        result = {}
        for k, v in pairs:
            if k in result:
                raise Stop("DUPLICATE_JSON_KEY")
            result[k] = v
        return result
    try:
        m = json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique_pairs)
    except (ValueError, OSError):
        raise Stop("INVALID_MANIFEST_JSON")
    if not isinstance(m, dict) or set(m) != {"version", "repo", "branch", "expected_head", "files"} or type(m["version"]) is not int or m["version"] != 1:
        raise Stop("INVALID_MANIFEST_SCHEMA")
    if (not isinstance(m["repo"], str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-]+", m["repo"])
            or m["repo"].split("/")[-1] in (".", "..")):
        raise Stop("INVALID_REPO")
    if not isinstance(m["branch"], str) or m["branch"].startswith("-"):
        raise Stop("INVALID_BRANCH")
    if validate_branch_git:
        git(None, "check-ref-format", "refs/heads/" + m["branch"])
    elif (not m["branch"] or m["branch"] == "@" or ".." in m["branch"] or "@{" in m["branch"]
          or any(ord(c) <= 32 or ord(c) == 127 or c in "~^:?*[\\" for c in m["branch"])
          or any(not part or part.startswith(".") or part.endswith((".", ".lock")) for part in m["branch"].split("/"))):
        raise Stop("INVALID_BRANCH")
    if not isinstance(m["expected_head"], str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", m["expected_head"]):
        raise Stop("INVALID_EXPECTED_HEAD")
    if not isinstance(m["files"], list) or not m["files"]:
        raise Stop("EMPTY_MANIFEST")
    targets = set()
    for f in m["files"]:
        if not isinstance(f, dict) or set(f) != {"source", "path", "sha256"}:
            raise Stop("INVALID_FILE_SCHEMA")
        safe_relative(f["source"], "source")
        safe_relative(f["path"], "target")
        reject_secret_path(f["source"])
        reject_secret_path(f["path"])
        if not isinstance(f["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", f["sha256"]):
            raise Stop("INVALID_SHA256")
        if f["path"] in targets:
            raise Stop("DUPLICATE_TARGET")
        targets.add(f["path"])
    for p in targets:
        if any(str(parent) in targets for parent in PurePosixPath(p).parents if str(parent) != "."):
            raise Stop("TARGET_PREFIX_CONFLICT")
    return m


def non_symlink_path(root, relative):
    p = root
    for part in relative.split("/"):
        p = p / part
        if p.is_symlink():
            raise Stop("SYMLINK_PATH", path=relative)
    return p


def snapshot_sources(m, root, destination):
    # Copy from an opened regular file; validate the exact frozen bytes we stage.
    for i, f in enumerate(m["files"]):
        non_symlink_path(root, f["source"])
        try:
            # Open every directory relative to its already-open parent. A rename
            # or symlink swap cannot redirect this walk outside the source root.
            parent_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            try:
                parts = f["source"].split("/")
                for part in parts[:-1]:
                    child_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent_fd)
                    os.close(parent_fd)
                    parent_fd = child_fd
                fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent_fd)
            finally:
                os.close(parent_fd)
            with os.fdopen(fd, "rb") as src, open(destination / str(i), "xb") as dst:
                before = os.fstat(src.fileno())
                if not stat.S_ISREG(before.st_mode):
                    raise Stop("NONREGULAR_SOURCE", path=f["path"])
                digest = hashlib.sha256()
                tail = b""
                while chunk := src.read(1024 * 1024):
                    scan_secret_bytes(tail + chunk, f["path"])
                    tail = chunk[-8192:]
                    digest.update(chunk)
                    dst.write(chunk)
                after = os.fstat(src.fileno())
        except OSError:
            raise Stop("SOURCE_UNAVAILABLE", path=f["path"])
        if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
            raise Stop("SOURCE_CHANGED", path=f["path"])
        if digest.hexdigest() != f["sha256"]:
            raise Stop("SOURCE_HASH_MISMATCH", path=f["path"])
        f["snapshot"], f["size"] = destination / str(i), after.st_size


def check_private(m, test_remote=None, publish=False):
    if test_remote:
        # This exception is a local fixture, never a network/private assertion.
        remote = Path(test_remote)
        if not remote.is_absolute() or remote.is_symlink() or not remote.is_dir():
            raise Stop("INVALID_LOCAL_TEST_REMOTE")
        remote = remote.resolve()
        if git(remote, "rev-parse", "--is-bare-repository").strip() != b"true":
            raise Stop("TEST_REMOTE_NOT_BARE")
        return str(remote)
    response = remote_read(lambda: run(["gh", "api", "--hostname", "github.com", "repos/" + m["repo"]]), "metadata")
    try:
        metadata = json.loads(response)
    except ValueError:
        raise Stop("METADATA_INVALID")
    if not isinstance(metadata, dict) or not isinstance(metadata.get("full_name"), str):
        raise Stop("METADATA_INVALID")
    if (metadata.get("full_name", "").lower() != m["repo"].lower()
            or metadata.get("private") is not True or metadata.get("visibility") != "private"
            or metadata.get("archived") is not False):
        raise Stop("REPOSITORY_NOT_ACTIVE_PRIVATE")
    if publish and (not isinstance(metadata.get("permissions"), dict)
                    or metadata["permissions"].get("push") is not True):
        raise Stop("PUSH_PERMISSION_UNCONFIRMED")
    return "https://github.com/" + m["repo"] + ".git"


def remote_head(remote, branch):
    resolved = git(None, "ls-remote", "--get-url", remote).decode().strip()
    if resolved != remote:
        raise Stop("REMOTE_ROUTE_CHANGED")
    output = remote_read(lambda: git(None, "ls-remote", "--exit-code", remote, "refs/heads/" + branch), "head").decode()
    rows = output.strip().splitlines()
    if len(rows) != 1:
        raise Stop("BRANCH_MISSING_OR_AMBIGUOUS")
    sha, ref = rows[0].split("\t")
    if ref != "refs/heads/" + branch or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", sha):
        raise Stop("INVALID_REMOTE_REF")
    return sha


def checkout(directory, remote, branch, observed, selected=None):
    directory.mkdir()
    git(directory, "init", "--quiet")
    if (Path(git(directory, "rev-parse", "--absolute-git-dir").decode().strip()) != directory / ".git"
            or Path(git(directory, "rev-parse", "--show-toplevel").decode().strip()) != directory):
        raise Stop("WORKSPACE_REDIRECTED")
    git(directory, "remote", "add", "origin", remote)
    check_remote_route(directory, remote)
    fetch = ["fetch", "--quiet", "--depth=1", "--no-tags"]
    if selected is not None:
        fetch.append("--filter=blob:none")
    remote_read(lambda: git(directory, *fetch, "origin", "refs/heads/" + branch), "fetch")
    if git(directory, "rev-parse", "FETCH_HEAD").decode().strip() != observed:
        raise Stop("HEAD_CHANGED_DURING_FETCH")
    # Inspect attributes using the index before any checkout smudge can run,
    # including files outside the manifest. Existing hooks remain enabled.
    git(directory, "read-tree", observed)
    entries = tree(directory, observed)
    lfs_config = entries.get(".lfsconfig")
    if lfs_config and (lfs_config[0] not in ("100644", "100755") or lfs_config[1] != "blob"):
        raise Stop("NONREGULAR_LFS_CONFIG")
    all_filters = attributes(directory, [{"path": p} for p in entries], cached=True)
    if any(value not in ("unspecified", "unset", "lfs") for value in all_filters.values()):
        raise Stop("UNSUPPORTED_CHECKOUT_FILTER")
    if any(value == "lfs" for value in all_filters.values()):
        if DETECT_ONLY_LFS.get():
            raise Stop("LFS_DETECTED_REQUIRES_SEPARATE_WORKFLOW")
        check_lfs_route(directory, config_blob=lfs_config[2] if lfs_config else None)
    if selected is None:
        git(directory, "checkout-index", "--all")
    else:
        wanted = {f["path"] for f in selected} | {p for p in entries if PurePosixPath(p).name in {".gitattributes", ".lfsconfig"}}
        wanted &= entries.keys()
        omitted = entries.keys() - wanted
        if omitted:
            git(directory, "update-index", "--skip-worktree", "-z", "--stdin", data=b"".join(p.encode() + b"\0" for p in sorted(omitted)))
        if wanted:
            git(directory, "checkout-index", "-z", "--stdin", data=b"".join(p.encode() + b"\0" for p in sorted(wanted)))
    # Detach HEAD without invoking post-checkout hooks during a dry-run.
    # Commit and pre-push hooks still run on the actual publication commands.
    git(directory, "update-ref", "--no-deref", "HEAD", observed)
    if git(directory, "status", "--porcelain", "-z"):
        raise Stop("INITIAL_CHECKOUT_DIRTY")


def check_remote_route(cwd, remote):
    for args in (("--all",), ("--push", "--all")):
        urls = git(cwd, "remote", "get-url", *args, "origin").decode().splitlines()
        if urls != [remote]:
            raise Stop("REMOTE_ROUTE_CHANGED")


def tree(cwd, ref):
    result = {}
    for record in git(cwd, "ls-tree", "-r", "-z", ref).split(b"\0"):
        if record:
            metadata, name = record.split(b"\t", 1)
            mode, kind, oid = metadata.decode().split()
            result[name.decode("utf-8", "surrogateescape")] = (mode, kind, oid)
    return result


def blob_digests(cwd, entries, files):
    """Read all selected Git blobs through one streaming cat-file process."""
    result = {}
    process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=cwd,
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL, env=command_environment(),
                               start_new_session=True)
    expired = threading.Event()
    def expire():
        expired.set()
        kill_process(process)
    deadline = threading.Timer(COMMAND_TIMEOUT.get(), expire)
    deadline.daemon = True
    deadline.start()
    try:
        for f in files:
            p = f["path"]
            if p not in entries:
                continue
            mode, kind, oid = entries[p]
            if mode not in ("100644", "100755") or kind != "blob":
                raise Stop("NONREGULAR_TARGET", path=p)
            process.stdin.write((oid + "\n").encode())
            process.stdin.flush()
            header = process.stdout.readline().split()
            if len(header) != 3 or header[0].decode() != oid or header[1] != b"blob":
                raise Stop("BLOB_READ_FAILED", path=p)
            size = int(header[2]); remaining = size
            digest, small = hashlib.sha256(), bytearray()
            while remaining:
                chunk = process.stdout.read(min(remaining, 1024 * 1024))
                if not chunk:
                    raise Stop("BLOB_READ_FAILED", path=p)
                digest.update(chunk)
                if size <= 1024:
                    small.extend(chunk)
                remaining -= len(chunk)
            if process.stdout.read(1) != b"\n":
                raise Stop("BLOB_READ_FAILED", path=p)
            pointer = re.fullmatch(rb"version https://git-lfs.github.com/spec/v1\noid sha256:([0-9a-f]{64})\nsize ([0-9]+)\n", bytes(small))
            result[p] = {"raw_sha256": digest.hexdigest(), "size": size,
                         "pointer": (pointer[1].decode(), int(pointer[2])) if pointer else None}
    except (Stop, OSError, ValueError) as error:
        if expired.is_set():
            raise Stop("COMMAND_TIMEOUT", program="git") from None
        if isinstance(error, Stop):
            raise
        raise Stop("BLOB_READ_FAILED") from None
    finally:
        deadline.cancel()
        deadline.join()
        if process.poll() is None:
            kill_process(process)
        process.stdin.close()
        process.stdout.close()
        process.wait()
    if expired.is_set():
        raise Stop("COMMAND_TIMEOUT", program="git")
    return result


def attributes(cwd, files, cached=False):
    paths = b"".join(f["path"].encode() + b"\0" for f in files)
    values = git(cwd, "check-attr", *(('--cached',) if cached else ()), "-z", "--stdin", "filter", data=paths).split(b"\0")
    result = {}
    for i in range(0, len(values) - 1, 3):
        p, _, v = values[i:i + 3]
        result[p.decode()] = v.decode()
    return result


def check_lfs_route(cwd, config_blob=None):
    # Do not introduce a custom host, transfer agent, or credential route.
    # Only default GitHub LFS endpoints (or the local test fixture) are supported.
    query = r"^(lfs\.(url|pushurl|storage|extension\..*|standalonetransferagent|customtransfer\..*)|remote\..*\.lfs(url|pushurl)|remote\.lfs(push)?default|url\..*\.(insteadof|pushinsteadof))$"
    config_sources = [()]
    if config_blob:
        config_sources.append(("--blob", config_blob))
    elif (cwd / ".lfsconfig").exists():
        config_sources.append(("--file", str(cwd / ".lfsconfig")))
    for source in config_sources:
        args = ["git", "config", *source, "--get-regexp", query]
        if run(args, cwd=cwd, allowed_returncodes=(0, 1)):
            raise Stop("CUSTOM_LFS_ROUTE_UNSUPPORTED")
    for key in ("lfs.remote.autodetect", "lfs.remote.searchall"):
        if run(["git", "config", "--bool", "--get", key], cwd=cwd,
               allowed_returncodes=(0, 1)).strip() == b"true":
            raise Stop("CUSTOM_LFS_ROUTE_UNSUPPORTED")
    commands = {}
    official = {"clean": b"git-lfs clean -- %f", "smudge": b"git-lfs smudge -- %f",
                "process": b"git-lfs filter-process"}
    for key in official:
        commands[key] = run(["git", "config", "--get", "filter.lfs." + key],
                            cwd=cwd, allowed_returncodes=(0, 1)).strip()
    if not commands["clean"] and not commands["process"]:
        raise Stop("LFS_FILTER_NOT_CONFIGURED")
    if any(value and value != official[key] for key, value in commands.items()):
        raise Stop("UNSUPPORTED_LFS_FILTER_COMMAND")


def matches(f, blob, filters):
    if not blob:
        return False
    if filters[f["path"]] == "lfs":
        return blob["pointer"] == (f["sha256"], f["size"])
    return blob["raw_sha256"] == f["sha256"] and blob["size"] == f["size"]


def verify(cwd, ref, files, filters, fetch_lfs=False):
    blobs = blob_digests(cwd, tree(cwd, ref), files)
    for f in files:
        if not matches(f, blobs.get(f["path"]), filters):
            raise Stop("PUBLISHED_HASH_MISMATCH", path=f["path"])
    lfs = [f for f in files if filters[f["path"]] == "lfs"]
    if lfs and fetch_lfs:
        # Use official LFS transport, in a fresh repository; never accept just pointers.
        git(cwd, "lfs", "fetch", "--include=", "--exclude=", "origin", ref)
        for f in lfs:
            oid = f["sha256"]
            object_path = cwd / ".git" / "lfs" / "objects" / oid[:2] / oid[2:4] / oid
            try:
                with object_path.open("rb") as stream:
                    digest = hashlib.file_digest(stream, "sha256").hexdigest()
                if digest != oid or object_path.stat().st_size != f["size"]:
                    raise Stop("LFS_OBJECT_HASH_MISMATCH", path=f["path"])
            except OSError:
                raise Stop("LFS_OBJECT_UNAVAILABLE", path=f["path"])


def execute(manifest_path, source_root, publish=False, test_remote=None,
            message="Batch upload verified manifest", before_publish=None, after_head_check=None,
            command_timeout=120, checkpoint=None, retries=0, retry_delay=1.0,
            workers=2, lfs_detect_only=False, verify_only=False):
    if (isinstance(command_timeout, bool) or not isinstance(command_timeout, (int, float))
            or not math.isfinite(command_timeout) or command_timeout <= 0
            or command_timeout > threading.TIMEOUT_MAX):
        raise Stop("INVALID_COMMAND_TIMEOUT")
    if type(retries) is not int or not 0 <= retries <= 5 or type(workers) is not int or not 1 <= workers <= 4 or isinstance(retry_delay, bool) or not isinstance(retry_delay, (int, float)) or not math.isfinite(retry_delay) or not 0 <= retry_delay <= 30:
        raise Stop("INVALID_RETRY_OR_WORKER_POLICY")
    if verify_only and publish:
        raise Stop("VERIFY_ONLY_CANNOT_PUBLISH")
    if os.name != "posix" or not hasattr(os, "O_NOFOLLOW"):
        raise Stop("NATIVE_RUNTIME_REQUIRES_POSIX")
    tokens = [(COMMAND_TIMEOUT, COMMAND_TIMEOUT.set(float(command_timeout))),
              (RETRY, RETRY.set((retries, float(retry_delay)))),
              (RETRY_EVENTS, RETRY_EVENTS.set([])),
              (DETECT_ONLY_LFS, DETECT_ONLY_LFS.set(lfs_detect_only)),
              (VERIFY_ONLY, VERIFY_ONLY.set(verify_only))]
    started = time.perf_counter()
    cp = None
    try:
        check_environment()
        m = load_manifest(manifest_path)
        root = Path(source_root).resolve(strict=not bool(checkpoint))
        if (root.exists() and not root.is_dir()) or (not checkpoint and not root.is_dir()):
            raise Stop("SOURCE_ROOT_NOT_DIRECTORY")
        # One local writer for all branches of a target repository.
        key = hashlib.sha256((m["repo"].casefold() + "|" + str(test_remote or "github.com")).encode()).hexdigest()
        lock_root = Path(tempfile.gettempdir()) / ("github-batch-upload-locks-" + str(os.getuid()))
        with process_lock(lock_root, key):
            with process_lock(checkpoint, "checkpoint.lock") if checkpoint else nullcontext():
                if checkpoint:
                    cp = Checkpoint(checkpoint, m, root, test_remote)
                try:
                    report = _execute(manifest_path, source_root, publish, test_remote, message,
                                      before_publish, after_head_check, m=m, root=root, cp=cp, workers=workers)
                    report["timings_seconds"]["total"] = round(time.perf_counter() - started, 6)
                    if cp:
                        cp.save(last_error=None, receipt=report)
                    return report
                except Stop as error:
                    error.details.setdefault("timings_seconds", {})["total"] = round(time.perf_counter() - started, 6)
                    if cp:
                        cp.save(last_error=error.code, receipt={"status": "STOPPED", "code": error.code, **error.details})
                    raise
    finally:
        for variable, token in reversed(tokens):
            variable.reset(token)


def push_candidate(work, remote, m, candidate, observed, report, test_remote):
    for attempt in range(RETRY.get()[0] + 1):
        try:
            git(work, "push", "--porcelain", "origin", candidate + ":refs/heads/" + m["branch"])
            report["git_push_returned_success"] = True
            return
        except Stop as error:
            if error.code not in TRANSIENT or RETRY.get()[0] == 0:
                raise
            # Always inspect the actual ref before considering a write retry.
            now = remote_head(remote, m["branch"])
            if now == candidate:
                report["remote_confirmed_after_transient"] = True
                return
            if now != observed:
                raise Stop("HEAD_CONFLICT_DURING_RETRY", observed_head=now) from None
            if attempt == RETRY.get()[0]:
                raise
            backoff(error, attempt, "push")
            check_private(m, test_remote, publish=True)
            check_remote_route(work, remote)
            if remote_head(remote, m["branch"]) != observed:
                raise Stop("HEAD_CONFLICT_BEFORE_RETRY")
            report["automatic_write_retry"] = True


def _execute(manifest_path, source_root, publish=False, test_remote=None,
             message="Batch upload verified manifest", before_publish=None, after_head_check=None,
             m=None, root=None, cp=None, workers=2):
    report = {"repo": m["repo"], "branch": m["branch"], "expected_head": m["expected_head"],
              "mode": "publish" if publish else "dry-run", "test_fixture": bool(test_remote),
              "remote_write_attempted": False, "file_count": len(m["files"]),
              "automatic_write_retry": False, "retry_events": RETRY_EVENTS.get(),
              "timings_seconds": {}, "checkpoint_enabled": bool(cp)}
    try:
        with tempfile.TemporaryDirectory(prefix="github-manifest-batch-") as temporary:
            base = Path(temporary)
            with phase(report, "freeze"):
                if cp:
                    report["reused_snapshots"] = cp.freeze(m, root, workers)
                    report["manifest_id"] = cp.digest
                else:
                    snapshots = base / "snapshots"; snapshots.mkdir()
                    snapshot_sources(m, root, snapshots)
            with phase(report, "preflight"):
                remote = check_private(m, test_remote, publish=publish)
                observed = remote_head(remote, m["branch"])
                report["observed_head"] = observed
            with phase(report, "checkout"):
                reusable = cp and cp.state.get("work_ready") and observed in {cp.state.get("base_head"), cp.state.get("candidate_commit")}
                work = cp.path / "work" if cp and (reusable or not cp.state.get("work_ready")) else base / "work"
                if work.is_symlink() or (work / ".git").is_symlink():
                    raise Stop("CHECKPOINT_SYMLINK")
                if reusable:
                    check_remote_route(work, remote)
                    if Path(git(work, "rev-parse", "--absolute-git-dir").decode().strip()) != work / ".git":
                        raise Stop("WORKSPACE_REDIRECTED")
                    cached_head = git(work, "rev-parse", "HEAD").decode().strip()
                    if cached_head not in {cp.state.get("base_head"), cp.state.get("candidate_commit")}:
                        # Recover a commit accepted locally before the checkpoint write was interrupted.
                        if (cp.state.get("staged_tree") and git(work, "rev-parse", "HEAD^").decode().strip() == cp.state["base_head"]
                                and git(work, "rev-parse", "HEAD^{tree}").decode().strip() == cp.state["staged_tree"]
                                and not git(work, "status", "--porcelain", "-z")):
                            cp.save(candidate_commit=cached_head)
                        else:
                            raise Stop("CHECKPOINT_WORK_HEAD_MISMATCH")
                    # Reinspect cached attributes; checkpoint content is never implicitly trusted.
                    all_filters = attributes(work, [{"path": p} for p in tree(work, "HEAD")], cached=True)
                    if any(v not in {"unspecified", "unset", "lfs"} for v in all_filters.values()):
                        raise Stop("UNSUPPORTED_CHECKOUT_FILTER")
                    if DETECT_ONLY_LFS.get() and "lfs" in all_filters.values():
                        raise Stop("LFS_DETECTED_REQUIRES_SEPARATE_WORKFLOW")
                    report["reused_work"] = True
                else:
                    if work.exists():
                        shutil.rmtree(work)
                    if cp:
                        checkout(work, remote, m["branch"], observed, selected=m["files"])
                    else:
                        checkout(work, remote, m["branch"], observed)
                    report["reused_work"] = False
                    if cp and work == cp.path / "work":
                        cp.save(work_ready=True, base_head=observed)
            original = tree(work, observed)
            filters = attributes(work, m["files"], cached=bool(cp))
            for f in m["files"]:
                filter_name = filters[f["path"]]
                if filter_name not in ("unspecified", "unset", "lfs"):
                    raise Stop("UNSUPPORTED_FILTER", path=f["path"])
                if filter_name != "lfs" and f["size"] > 100 * 1024 * 1024:
                    raise Stop("NEEDS_EXPLICIT_LFS_RULE", path=f["path"])
            if any(value == "lfs" for value in filters.values()):
                if DETECT_ONLY_LFS.get():
                    raise Stop("LFS_DETECTED_REQUIRES_SEPARATE_WORKFLOW")
                check_lfs_route(work)
            with phase(report, "compare"):
                current = blob_digests(work, original, m["files"])
            changed = [f for f in m["files"] if not matches(f, current.get(f["path"]), filters)]
            report.update(changed=[f["path"] for f in changed],
                          skipped=[f["path"] for f in m["files"] if f not in changed],
                          lfs_files=[f["path"] for f in m["files"] if filters[f["path"]] == "lfs"],
                          large_normal_files=[f["path"] for f in m["files"] if filters[f["path"]] != "lfs" and f["size"] > 50 * 1024 * 1024])
            report["changed_source_bytes"] = sum(f["size"] for f in changed)
            # Bound uncompressed normal payload conservatively below GitHub's 2 GiB push cap.
            if sum(f["size"] for f in changed if filters[f["path"]] != "lfs") > 1024 ** 3:
                raise Stop("NEEDS_SMALLER_EXPLICIT_BATCH")
            if not changed:
                with phase(report, "verify"):
                    if report["reused_work"]:
                        fresh = base / "verification"
                        checkout(fresh, remote, m["branch"], observed, selected=m["files"])
                        verify(fresh, "HEAD", m["files"], attributes(fresh, m["files"], cached=True), fetch_lfs=True)
                    else:
                        verify(work, "HEAD", m["files"], filters, fetch_lfs=True)
                if remote_head(remote, m["branch"]) != observed:
                    raise Stop("HEAD_CHANGED_DURING_VERIFICATION")
                report.update(status="NOOP_VERIFIED", verified_head=observed,
                              verified_files=len(m["files"]))
                return report
            if VERIFY_ONLY.get():
                raise Stop("REMOTE_CONTENT_NOT_COMPLETE")
            if observed != m["expected_head"]:
                raise Stop("HEAD_CONFLICT", observed_head=observed)
            stage_started = time.perf_counter()
            report["reused_staged_files"] = 0
            for f in changed:
                dst = non_symlink_path(work, f["path"])
                if dst.exists() and not dst.is_file():
                    raise Stop("NONREGULAR_TARGET", path=f["path"])
                dst.parent.mkdir(parents=True, exist_ok=True)
                reusable_bytes = False
                if cp and dst.is_file() and dst.stat().st_size == f["size"]:
                    with dst.open("rb") as stream:
                        reusable_bytes = hashlib.file_digest(stream, "sha256").hexdigest() == f["sha256"]
                if reusable_bytes:
                    report["reused_staged_files"] += 1
                else:
                    shutil.copyfile(f["snapshot"], dst)
                os.chmod(dst, 0o755 if original.get(f["path"], (None,))[0] == "100755" else 0o644)
            paths = b"".join(f["path"].encode() + b"\0" for f in changed)
            git(work, "--literal-pathspecs", "add", "--pathspec-from-file=-", "--pathspec-file-nul", data=paths)
            staged_tree = git(work, "write-tree").decode().strip()
            staged = tree(work, staged_tree)
            allowed = {f["path"] for f in changed}
            actual = {p for p in original.keys() | staged.keys() if original.get(p) != staged.get(p)}
            if actual != allowed:
                raise Stop("UNEXPECTED_TREE_CHANGE")
            verify(work, staged_tree, m["files"], filters)
            report["staged_tree"] = staged_tree
            if cp:
                cp.save(staged_tree=staged_tree)
            report["timings_seconds"]["stage"] = round(time.perf_counter() - stage_started, 6)
            if not publish:
                if remote_head(remote, m["branch"]) != observed:
                    raise Stop("HEAD_CHANGED_DURING_DRY_RUN")
                report.update(status="DRY_RUN_VERIFIED", verified_files=len(m["files"]),
                              planned_commits=1, planned_git_pushes=1,
                              lfs_payload_verified=False if report["lfs_files"] else None)
                return report
            # Normal hooks/signing rules remain active; failures stop, never bypass.
            with phase(report, "commit"):
                previous = cp.state.get("candidate_commit") if cp else None
                if previous:
                    candidate = git(work, "rev-parse", "HEAD").decode().strip()
                    if candidate != previous:
                        raise Stop("CHECKPOINT_CANDIDATE_MISMATCH")
                    report["reused_candidate"] = True
                else:
                    git(work, "commit", "--quiet", "-m", message)
                    candidate = git(work, "rev-parse", "HEAD").decode().strip()
            report["candidate_commit"] = candidate
            if (git(work, "rev-parse", "HEAD^").decode().strip() != observed
                    or git(work, "rev-parse", "HEAD^{tree}").decode().strip() != staged_tree
                    or git(work, "status", "--porcelain", "-z")):
                raise Stop("COMMIT_OR_HOOK_CHANGED_REVIEWED_CONTENT")
            if cp:
                cp.save(candidate_commit=candidate, staged_tree=staged_tree)
            if before_publish:  # Test injection only, never exposed as a CLI shell hook.
                before_publish(candidate)
            check_private(m, test_remote, publish=True)
            check_remote_route(work, remote)
            if remote_head(remote, m["branch"]) != observed:
                raise Stop("HEAD_CONFLICT_BEFORE_PUSH")
            if after_head_check:
                after_head_check(candidate)
            if report["lfs_files"]:
                report["remote_write_attempted"] = True
                git(work, "lfs", "push", "origin", candidate)
                if remote_head(remote, m["branch"]) != observed:
                    raise Stop("HEAD_CONFLICT_AFTER_LFS_UPLOAD")
            report["remote_write_attempted"] = True
            # Exactly one explicit branch, no force/lease/+, no rebase/merge/reset.
            with phase(report, "push"):
                push_candidate(work, remote, m, candidate, observed, report, test_remote)
            final_head = remote_head(remote, m["branch"])
            if final_head != candidate:
                raise Stop("HEAD_CHANGED_AFTER_PUSH", observed_head=final_head)
            verification = base / "verification"
            with phase(report, "verify"):
                if cp:
                    checkout(verification, remote, m["branch"], candidate, selected=m["files"])
                else:
                    checkout(verification, remote, m["branch"], candidate)
                verified_filters = attributes(verification, m["files"], cached=bool(cp))
                if verified_filters != filters:
                    raise Stop("ATTRIBUTES_CHANGED")
                verify(verification, "HEAD", m["files"], verified_filters, fetch_lfs=True)
            if remote_head(remote, m["branch"]) != candidate:
                raise Stop("HEAD_CHANGED_DURING_VERIFICATION")
            report.update(status="PUBLISHED_VERIFIED", verified_head=candidate,
                          verified_files=len(m["files"]), lfs_payload_verified=bool(report["lfs_files"]))
            return report
    except Stop as error:
        error.details = {**report, **error.details,
                         "publication_may_have_occurred": report["remote_write_attempted"],
                         "automatic_write_retry": report["automatic_write_retry"]}
        raise
    except KeyboardInterrupt:
        raise Stop("INTERRUPTED", **report,
                   publication_may_have_occurred=report["remote_write_attempted"],
                   ) from None
    except (OSError, ValueError, TypeError, KeyError):
        raise Stop("LOCAL_INPUT_OR_IO_ERROR", **report,
                   publication_may_have_occurred=report["remote_write_attempted"],
                   )


def main():
    def interrupt(signum, frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, interrupt)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--source-root", required=True, type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Default: stage/review locally, never commit or push")
    mode.add_argument("--verify-only", action="store_true", help="Read-only recovery: require all remote manifest bytes to match")
    mode.add_argument("--publish", action="store_true", help="Publish within authorized task scope, respecting existing denials")
    parser.add_argument("--message", default="Batch upload verified manifest")
    parser.add_argument("--command-timeout", type=float, default=120,
                        help="Positive seconds per external command/blob stream")
    parser.add_argument("--checkpoint", type=Path, help="Private persistent directory; same manifest/target resumes frozen files")
    parser.add_argument("--retries", type=int, default=2, help="Bounded transient retries; each push retry inspects the remote first")
    parser.add_argument("--retry-delay", type=float, default=1, help="Exponential base delay; Retry-After is honored or deferred")
    parser.add_argument("--workers", type=int, default=2, help="1-4 source snapshot workers; Git/ref writes are serial")
    parser.add_argument("--test-only-local-remote", type=Path, help="Absolute local bare fixture only; never a URL")
    args = parser.parse_args()
    try:
        report = execute(args.manifest, args.source_root, publish=args.publish,
                         test_remote=args.test_only_local_remote, message=args.message,
                         command_timeout=args.command_timeout, checkpoint=args.checkpoint,
                         retries=args.retries, retry_delay=args.retry_delay, workers=args.workers,
                         lfs_detect_only=True, verify_only=args.verify_only)
        print(json.dumps(report, ensure_ascii=False, indent=2))
    except Stop as error:
        print(json.dumps({"status": "STOPPED", "code": error.code, **error.details}, ensure_ascii=False, indent=2))
        return 2
    except (OSError, ValueError, TypeError, KeyError):
        print(json.dumps({"status": "STOPPED", "code": "LOCAL_INPUT_OR_IO_ERROR", "automatic_write_retry": False}))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
