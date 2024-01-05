#!/bin/bash

find thesis/chapters ! -name 'publications-generated.tex' -name "*.tex" -exec latexindent -m -o {} {} \; > /dev/null
latexindent -m -o thesis/main.tex thesis/main.tex \; > /dev/null
find thesis -name indent.log -exec rm {} \;
