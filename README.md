# Projet_footrating — Football Player Match Rating (ML)

ESILV A4 Machine Learning project (LAB 5 – Full Project), by Clément and Paul.

**Goal:** predict the per-match rating (PlayeRank score) of each football player from the
statistics of that player in that match. See `report/project_specification.md`.

## Install

Requirements: [uv](https://docs.astral.sh/uv/) and GNU make (on Windows, `mingw32-make`
works; replace `make` by `mingw32-make` below).

```bash
make install        # uv sync --frozen + pre-commit hooks
```

Without uv: `python -m venv .venv`, activate it, then `pip install -r requirements.txt`
(Python 3.12).

## Download the data

Sources (both CC BY 4.0): the Wyscout soccer match event dataset (Pappalardo et al., 2019,
<https://figshare.com/collections/_/4415000>) and PlayeRank scores
(<https://figshare.com/articles/PlayeRanks/9361148>). Files go in `data/raw/`, which git
ignores. The download script is added in task T1 (module M1); see `data/README.md`.

## Reproduce the results

Not available yet: the commands that produce each file in `results/` will be listed here as
the modules are delivered.

## Commands

| Command | What it does |
|---|---|
| `make install` | Create `.venv` from `uv.lock`, install pre-commit hooks |
| `make format` | Format code and fix imports (ruff) |
| `make lint` | Lint and check formatting, without changes |
| `make test` | Run pytest |
| `make check` | Lint + tests; exits 0 only if everything passes (under one minute) |
| `make requirements` | Regenerate `requirements.txt` from `uv.lock` |
| `make zip` | Build `Group_footrating_DS_Project.zip` for Moodle, without data or models |

## Layout

```
pyproject.toml, uv.lock   environment (uv); requirements.txt is exported from uv.lock
src/footrating/           data, features, models, evaluation code
scripts/                  utility scripts (fixture generation, Moodle zip)
tests/                    automated tests; tests/fixtures/ holds a small synthetic sample
notebooks/                exploration notebooks (relative paths only)
configs/                  configs, including the global random seed (default.yaml)
results/                  metrics and tables produced by scripts (tracked)
report/                   specification and final report
ai_governance/            CONTRIBUTIONS.md, PROMPT_LOG.md, AI_AUDIT.md
docs/                     architecture, decisions (docs/decisions/)
data/                     raw/ and processed/ data (not tracked, see data/README.md)
```

Contribution rules: `CONTRIBUTING.md`.
