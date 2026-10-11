#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
if ! kpsewhich ctex.sty >/dev/null 2>&1 && [[ -f /workspace/.local/texmf/tex/latex/ctex/ctex.sty ]]; then
  export TEXMFHOME=/workspace/.local/texmf
fi
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-/tmp/introductory-electromagnetism-cache}"
mkdir -p "$XDG_CACHE_HOME"
python vendor/math-latex-typesetting/scripts/validate.py main.tex --out build
