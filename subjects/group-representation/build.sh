#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p build dist
for pass in 1 2 3; do
  xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build main.tex > "build/pass-${pass}.txt"
done
cp build/main.pdf dist/main.pdf
