#!/usr/bin/env bash

outfile=`grep outfile resume.yaml | head -n 1 | awk '{print $2}'`

tmp=`mktemp -d`
trap "rm -rf $tmp" EXIT

./render.py -t $tmp

pdflatex -output-directory=$tmp $tmp/resume.tex

tools/shrinkpdf2 $tmp/resume.pdf output/${outfile}.pdf

pandoc $tmp/resume.md -o output/${outfile}.odt
pandoc $tmp/resume.md -o output/${outfile}.docx
