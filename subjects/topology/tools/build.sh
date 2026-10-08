#!/usr/bin/env bash
# Use the user's fixed-template validator and its isolated, guarded build.
set -euo pipefail
TOP_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd -- "$TOP_DIR"
SOURCE_FILE=${1:-main.tex}
OUTPUT_DIR=${2:-build}
if [[ ! -f "$SOURCE_FILE" ]]; then
  printf 'Missing LaTeX source: %s\n' "$SOURCE_FILE" >&2
  exit 2
fi
export TEXMFHOME=${TEXMFHOME:-/workspace/.local/texmf}
export XDG_CACHE_HOME=${XDG_CACHE_HOME:-/workspace/.cache}
export PYTHONDONTWRITEBYTECODE=1
mkdir -p -- "$XDG_CACHE_HOME/fontconfig" "$OUTPUT_DIR"
if ! kpsewhich xeCJK.sty > /dev/null || ! kpsewhich cmunrm.otf > /dev/null; then
  printf 'Fixed-template dependencies are missing. Run python3 tools/bootstrap_tex.py first.\n' >&2
  exit 2
fi
python3 vendor/math-latex-typesetting/scripts/validate.py "$SOURCE_FILE" --out "$OUTPUT_DIR"
