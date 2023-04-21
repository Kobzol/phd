#!/bin/bash

find thesis/chapters -name "*.tex" -exec latexindent -m -o {} {} \; > /dev/null
latexindent -m -o thesis/main.tex thesis/main.tex \; > /dev/null
find thesis -name indent.log -exec rm {} \;
