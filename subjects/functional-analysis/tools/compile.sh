#!/usr/bin/env bash
set -euo pipefail
book_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
export PYTHONDONTWRITEBYTECODE=1
python3 "$book_dir/vendor/math-latex-typesetting/scripts/validate.py" "$book_dir/main.tex" --out build
