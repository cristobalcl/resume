# AGENTS.md

Instructions for coding agents working in this repository.
Scope: entire repo.

## Repository Overview

- Main generator script: `render.py`.
- Input data: `resume.yaml`.
- Templates: `templates/markdown.mako`, `templates/latex.mako`, `templates/hugo.mako`.
- Build entrypoint: `Makefile` (`all` target).
- CI: `.github/workflows/build.yml`.
- Generated artifacts are written under `output/`.

## Environment and Dependencies

- Python 3 runtime.
- Python packages from `requirements.txt`:
  - `Mako==1.1.0`
  - `MarkupSafe==1.1.1`
  - `PyYAML==5.1.2`
- External build tools used by `make all`:
  - `lualatex`
  - `pandoc`

## Setup Commands

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Build / Lint / Test Commands

### Build

- Full build (recommended):

```bash
make all
```

- Render templates only (without LaTeX/pandoc pipeline):

```bash
python3 render.py -t build
```

- Render with debug output:

```bash
python3 render.py -t build -v
```

### Lint and Formatting

- There is no configured linter or formatter in this repo.
- No `pyproject.toml`, `ruff`, `black`, `flake8`, or `pylint` config detected.
- Keep style consistent manually when editing.

### Tests

- There is no committed automated test suite yet (`tests/` not found).
- If you add tests, use `pytest` naming (`test_*.py`) and the commands below.

```bash
# all tests
pytest

# single file
pytest tests/test_render.py

# single test (important)
pytest tests/test_render.py::test_renders_markdown

# single parameterized case
pytest tests/test_render.py::test_renders_markdown[case_name]
```

## CI Behavior

The workflow in `.github/workflows/build.yml` does the following:

- installs dependencies
- runs `python3 render.py -t /github/workspace/build`
- compiles LaTeX via `dante-ev/latex-action`
- copies generated Hugo output to `output/cv.md`
- may commit generated changes when output differs

When changing generation logic, run `make all` locally first.

## Code Style Guidelines

### Python

- Follow PEP 8 for new or modified code.
- Prefer `snake_case` for functions, variables, and helpers.
- Use `UPPER_SNAKE_CASE` for constants.
- Keep functions small and focused.
- Prefer explicit behavior over clever shortcuts.
- Use `with open(...)` for file I/O.
- Prefer explicit encodings for text file operations.

### Imports

- Group imports in this order:
  1. standard library
  2. third-party
  3. local
- Keep one import per line unless there is a strong reason.
- Remove unused imports.
- Do not use wildcard imports.

### Formatting

- Use 4 spaces in Python files.
- Avoid formatting-only churn unrelated to the task.
- Keep line length readable; wrap long calls and literals.
- Keep existing quote style unless touching a whole block consistently.

### Types

- Typing is not enforced in current project.
- Add lightweight type hints for new public functions when useful.
- Avoid broad typing refactors unless explicitly requested.

### Naming Conventions

- Python identifiers: descriptive and intention-revealing.
- Template variables should match keys in `resume.yaml`.
- Preserve output file names (`resume.md`, `resume.tex`, `resume.hugo`).

### Error Handling

- Fail fast on invalid input or missing required files.
- Raise clear exceptions with actionable context.
- Do not silently swallow exceptions.
- CLI paths should return non-zero on failure.

### YAML and Templates

- Keep `resume.yaml` schema backward-compatible with templates.
- If YAML keys change, update all affected templates in same change.
- Keep template output deterministic.
- Reuse escaping helpers in templates when rendering user-provided text.
- Keep heavy logic out of templates; prefer Python-side processing.

## Cursor and Copilot Rules

Checked and not found:

- `.cursorrules`
- `.cursor/rules/`
- `.github/copilot-instructions.md`

If any of these files are added later, treat them as higher-priority guidance
and update this AGENTS.md to reference their key rules.

## Agent Working Rules

- Keep diffs focused to the request and avoid unrelated refactors.
- Preserve existing behavior unless the change request requires behavior changes.
- Describe verification steps in your handoff.
