#!/usr/bin/env python3
"""Record offline tests and stable source hashes, never production upload timing."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
import unittest


def flattened(suite):
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            yield from flattened(test)
        else:
            yield test.id()


def hashes(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*.py')) if '__pycache__' not in p.parts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    package = Path(__file__).resolve().parents[1]
    parser.add_argument('--tests', type=Path, default=package / 'tests')
    parser.add_argument('--source-root', type=Path, default=package)
    parser.add_argument('--output', type=Path, default=package / 'references' / 'validation.json')
    args = parser.parse_args()
    test_root = args.tests.resolve()
    sys.path.insert(0, str(test_root))
    before = hashes(args.source_root)
    start_utc = datetime.now(timezone.utc).isoformat()
    started = time.perf_counter()
    suite = unittest.defaultTestLoader.discover(str(test_root), pattern='test_*.py')
    test_ids = list(flattened(suite))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.with_suffix('.txt').open('w') as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    elapsed = time.perf_counter() - started
    after = hashes(args.source_root)
    report = {'baseline_commit': 'a170d65a5646eafb0798f12c741f1cc9b7efbbba',
              'started_utc': start_utc, 'finished_utc': datetime.now(timezone.utc).isoformat(),
              'python': platform.python_version(), 'platform': platform.platform(),
              'git': subprocess.check_output(['git', '--version'], text=True).strip(),
              'tests_run': result.testsRun, 'failures': len(result.failures),
              'errors': len(result.errors), 'skipped': len(result.skipped),
              'successful': result.wasSuccessful() and before == after,
              'elapsed_seconds': round(elapsed, 3), 'sources_unchanged_during_run': before == after,
              'source_sha256': before, 'test_ids': test_ids,
              'scope': 'Synthetic local bare Git remotes, original security/LFS regressions, persistent recovery, target binding, retry/denial, secret/path gates, repo installer and offline connector planning. No production GitHub upload, byte-range continuation or universal-platform validation.'}
    args.output.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('tests_run', 'failures', 'errors', 'skipped', 'successful', 'elapsed_seconds', 'sources_unchanged_during_run')}, indent=2))
    return 0 if report['successful'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
