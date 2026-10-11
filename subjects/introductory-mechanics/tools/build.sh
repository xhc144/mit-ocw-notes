#!/usr/bin/env bash
set -euo pipefail
book_dir=$(cd -- "$(dirname -- "$0")/.." && pwd)
cd "$book_dir"
python3 tools/numerics.py > build-numerics.tmp.json
python3 vendor/math-latex-typesetting/scripts/validate.py main.tex --out build
cp build/main.pdf introductory-mechanics.pdf
rm -f build-numerics.tmp.json
