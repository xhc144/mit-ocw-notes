#!/usr/bin/env bash
set -euo pipefail
STATISTICS_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
cd -- "$STATISTICS_DIR"
export TEXMFHOME=${TEXMFHOME:-/workspace/.local/texmf}
export SOURCE_DATE_EPOCH=1791417600
export FORCE_SOURCE_DATE=1
STATISTICS_BUILD=$(mktemp -d /tmp/mit-statistics-build.XXXXXX)
trap 'rm -rf -- "$STATISTICS_BUILD"' EXIT
cp main.tex references.tex course-information.tex "$STATISTICS_BUILD/"
cp -R chapters assignments "$STATISTICS_BUILD/"
cd -- "$STATISTICS_BUILD"
for STATISTICS_PASS in 1 2 3; do
  xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex > "pass-${STATISTICS_PASS}.txt"
done
if rg 'Undefined control sequence|LaTeX Error|Missing character|There were undefined references|multiply defined' main.log; then
  exit 1
fi
mkdir -p -- "$STATISTICS_DIR/dist"
cp main.pdf "$STATISTICS_DIR/dist/main.pdf"
printf 'Built %s\n' "$STATISTICS_DIR/dist/main.pdf"
