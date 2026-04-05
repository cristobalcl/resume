# resume
CV generator in different formats.

## Install all dependencies

### 1) System dependencies

Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install -y \
  python3 python3-venv python3-pip \
  texlive texlive-binaries texlive-latex-recommended texlive-latex-extra texlive-fonts-extra \
  pandoc \
  nodejs npm
```

OpenSUSE:

```bash
sudo zypper install -y \
  python3 python3-pip \
  texlive texlive-moderncv \
  pandoc \
  nodejs npm
```

macOS (Homebrew):

```bash
brew install python pandoc node
brew install --cask mactex-no-gui
```

### 2) Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

# Required for RenderCV output pipeline
pip install "rendercv[full]"
```

### 3) JSON Resume tooling (resumed)

Choose one option:

```bash
# Global install
npm install -g resumed jsonresume-theme-even

# or local install in this repo
npm install --no-save resumed jsonresume-theme-even
```

The Makefile uses theme package `jsonresume-theme-even` by default.

## New JSON Resume + RenderCV workflow

This repository now supports a migration path to JSON Resume as the source data
format (authored in YAML), while keeping the legacy pipeline available.

- JSON Resume YAML source: `resume.jsonresume.yaml`
- JSON Resume canonical JSON output: `build/resume.json`
- RenderCV translated YAML output: `build/rendercv.yaml`

### Build targets

```bash
# Legacy templates + LaTeX/pandoc outputs
make legacy

# Convert JSON Resume YAML -> JSON and export HTML + PDF with resumed
make jsonresume

# Translate JSON Resume -> RenderCV and build PDF
make rendercv

# Run all pipelines
make all
```

### Tooling notes

- `make jsonresume` uses globally installed `resumed`, or local
  `node_modules/.bin/resumed` via `npx resumed`.
- Default JSON Resume theme is `jsonresume-theme-even` (override with
  `make jsonresume JSONRESUME_THEME=jsonresume-theme-professional`).
- `make rendercv` requires RenderCV installed (recommended:
  `pip install "rendercv[full]"`).

## Install dependencies

Ubuntu:

```bash
sudo apt-get install texlive texlive-binaries texlive-latex-recomended texlive-latex-extra virtualenv
virtualenv -p python3 .venv
source .venv/bin/activate.fish
pip install -r requirements.txt
```

OpenSuse:

```bash
sudo zypper install texlive texlive-moderncv python3
virtualenv -p python3 .venv
source .venv/bin/activate.fish
pip install -r requirements.txt
```

Download and install [Pandoc](http://pandoc.org/).

Mac:

```bash
sudo pip install virtualenv
brew cask install mactex-no-gui
brew install pandoc
virtualenv -p python3 .venv
source .venv/bin/activate.fish
pip install -r requirements.txt
```
