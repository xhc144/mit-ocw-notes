#!/bin/sh
# Compile the embedded fixed template without network access or shell escape.
set -eu
mkdir -p build
for pass in 1 2 3; do
    xelatex -no-shell-escape -interaction=nonstopmode \
        -halt-on-error -output-directory=build main.tex
done
printf '%s\n' 'Built build/main.pdf; inspect the PDF and final log before sharing.'
