#!/usr/bin/env bash
set -euo pipefail
book_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
export TEXMFHOME="${TEXMFHOME:-$book_root/.runtime/texmf}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$book_root/.runtime/cache}"
export PYTHONDONTWRITEBYTECODE=1
python3 "$book_root/vendor/math-latex-typesetting/scripts/validate.py" "$book_root/main.tex" --out build
cp "$book_root/build/main.pdf" "$book_root/ordinary-differential-equations.pdf"
