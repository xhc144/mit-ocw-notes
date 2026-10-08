#!/usr/bin/env bash
set -euo pipefail
TASK_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
export TEXMFHOME="${TEXMFHOME:-$TASK_ROOT/.runtime/texmf}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$TASK_ROOT/.runtime/cache}"
export PYTHONDONTWRITEBYTECODE=1
python "$TASK_ROOT/vendor/math-latex-typesetting/scripts/validate.py" "$TASK_ROOT/main.tex" --out build
cp "$TASK_ROOT/build/main.pdf" "$TASK_ROOT/complex-analysis.pdf"
