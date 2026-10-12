#!/usr/bin/env python3
"""Compatibility entry using the single guarded build implementation."""
import argparse
from pathlib import Path
from build_utils import build

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('main',type=Path); ap.add_argument('--out',type=Path,default=Path('build')); ap.add_argument('--timeout',type=int,default=120); a=ap.parse_args()
    out=a.out if a.out.is_absolute() else a.main.resolve().parent/a.out
    try: print(build(a.main,out,timeout=a.timeout)['pdf']); return 0
    except (OSError,ValueError,RuntimeError) as exc: print('BUILD FAILED:',exc); return 1
if __name__=='__main__': raise SystemExit(main())
