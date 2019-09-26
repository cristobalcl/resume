# resume
CV generator in different formats.

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
