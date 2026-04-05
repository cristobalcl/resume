export SHELL:=/bin/bash
export SHELLOPTS:=$(if $(SHELLOPTS),$(SHELLOPTS):)pipefail:errexit

.ONESHELL:

OUTFILE := $(shell grep outfile resume.yaml | head -n 1 | awk '{print $$2}')
BUILD_DIR := build
JSONRESUME_YAML := resume.jsonresume.yaml
JSONRESUME_JSON := $(BUILD_DIR)/resume.json
RENDERCV_YAML := $(BUILD_DIR)/rendercv.yaml

JSONRESUME_THEME ?= jsonresume-theme-even
JSONRESUME_THEME_PACKAGE ?= $(JSONRESUME_THEME)
JSONRESUME_PUPPETEER_ARGS ?= --puppeteer-arg=--no-sandbox --puppeteer-arg=--disable-setuid-sandbox

JSONRESUME_HTML := output/$(OUTFILE)-jsonresume.html
JSONRESUME_PDF := output/$(OUTFILE)-jsonresume.pdf
RENDERCV_PDF := output/$(OUTFILE)-rendercv.pdf

all: legacy jsonresume rendercv

legacy:
	$(eval TMP := $(shell mktemp -d))

	trap "rm -rf $(TMP)" EXIT

	./render.py -t $(TMP)

	lualatex -output-directory=$(TMP) $(TMP)/resume.tex

	cp $(TMP)/resume.pdf output/$(OUTFILE).pdf

	pandoc $(TMP)/resume.md -o output/$(OUTFILE).odt
	pandoc $(TMP)/resume.md -o output/$(OUTFILE).docx
	cp $(TMP)/resume.hugo output/cv.md

jsonresume: jsonresume-export

jsonresume-build:
	mkdir -p $(BUILD_DIR)
	python3 scripts/jsonresume_yaml_to_json.py --input $(JSONRESUME_YAML) --output $(JSONRESUME_JSON)

jsonresume-export: jsonresume-build
	mkdir -p output
	if command -v resumed >/dev/null 2>&1; then
		RESUMED_BIN="resumed"
	elif [ -x ./node_modules/.bin/resumed ]; then
		RESUMED_BIN="npx resumed"
	else
		echo "resumed is required. Install it with: npm install -g resumed $(JSONRESUME_THEME_PACKAGE)"
		echo "Or locally: npm install --no-save resumed $(JSONRESUME_THEME_PACKAGE)"
		exit 1
	fi
	$$RESUMED_BIN render $(JSONRESUME_JSON) -o $(JSONRESUME_HTML) -t $(JSONRESUME_THEME)
	$$RESUMED_BIN export $(JSONRESUME_JSON) -o $(JSONRESUME_PDF) -t $(JSONRESUME_THEME) $(JSONRESUME_PUPPETEER_ARGS)

rendercv: rendercv-export

rendercv-build: jsonresume-build
	mkdir -p $(BUILD_DIR)
	python3 scripts/jsonresume_to_rendercv.py --input $(JSONRESUME_JSON) --output $(RENDERCV_YAML) --theme moderncv

rendercv-export: rendercv-build
	mkdir -p output
	if command -v rendercv >/dev/null 2>&1; then
		rendercv render $(RENDERCV_YAML) --pdf-path ../$(RENDERCV_PDF) -nomd -nohtml -nopng
	elif python3 -m rendercv --version >/dev/null 2>&1; then
		python3 -m rendercv render $(RENDERCV_YAML) --pdf-path ../$(RENDERCV_PDF) -nomd -nohtml -nopng
	else
		echo "RenderCV is required. Install it with: pip install \"rendercv[full]\""
		exit 1
	fi
	rm -f $(BUILD_DIR)/rendercv_output/*.typ
	rmdir $(BUILD_DIR)/rendercv_output 2>/dev/null || true

.PHONY: all legacy jsonresume jsonresume-build jsonresume-export rendercv rendercv-build rendercv-export
