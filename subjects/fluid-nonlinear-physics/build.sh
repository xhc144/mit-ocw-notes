#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
mkdir -p build
latexmk -xelatex -interaction=nonstopmode -halt-on-error -no-shell-escape -outdir=build main.tex
mkdir -p dist
cp build/main.pdf dist/fluid-nonlinear-physics-zh.pdf
