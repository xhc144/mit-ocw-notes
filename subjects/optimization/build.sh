#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p build
for pass in 1 2 3; do
  xelatex -no-shell-escape -halt-on-error -file-line-error -interaction=nonstopmode -output-directory=build main.tex
done
