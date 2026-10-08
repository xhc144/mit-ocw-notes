#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
export PYTHONDONTWRITEBYTECODE=1
if [[ -z "${TEXMFHOME:-}" && -d /workspace/.local/texmf ]]; then
  export TEXMFHOME=/workspace/.local/texmf
fi
if [[ -z "${XDG_CACHE_HOME:-}" ]]; then
  export XDG_CACHE_HOME="${TMPDIR:-/tmp}/differential-geometry-font-cache"
fi
mkdir -p -- "$XDG_CACHE_HOME"
python3 vendor/math-latex-typesetting/scripts/validate.py main.tex --out build --timeout 120
