export SHELL:=/bin/bash
export SHELLOPTS:=$(if $(SHELLOPTS),$(SHELLOPTS):)pipefail:errexit

.ONESHELL:

OUTFILE := $(shell grep outfile resume.yaml | head -n 1 | awk '{print $$2}')

all:
	$(eval TMP := $(shell mktemp -d))

	trap "rm -rf $(TMP)" EXIT

	./render.py -t $(TMP)

	lualatex -output-directory=$(TMP) $(TMP)/resume.tex

	cp $(TMP)/resume.pdf output/$(OUTFILE).pdf

	pandoc $(TMP)/resume.md -o output/$(OUTFILE).odt
	pandoc $(TMP)/resume.md -o output/$(OUTFILE).docx
	cp $(TMP)/resume.hugo output/cv.md
