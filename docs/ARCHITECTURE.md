# Architecture

What the project does, where each piece lives, and how data flows from raw events to a
predicted rating. Read this before changing a part of the code; update it in the same pull
request when the structure changes. Choices are justified in `docs/decisions/`.

Status: planned layout. Parts marked *(planned)* do not exist yet.

## Data flow

```
 Wyscout events (JSON)        matches, players (JSON)        playerank.json
 data/raw/                     data/raw/                       data/raw/
        │                            │                              │
        └──────────────┬─────────────┘                              │
                       ▼                                            │
 M1  aggregate events per (matchId, playerId);                      │
     recompute minutes and goals                                    │
                       │                                            │
                       ▼                                            ▼
     data/processed/player_match.parquet  ◄── join target ── playerankScore
                       │                     (minutesPlayed, goalScored go to
                       │                      data/processed/playerank_side_info.parquet,
                       │                      never joined by default)
                       ▼
 M2  cleaning, low-minute rule, rates, per-90 features
                       │
                       ▼
 M3  chronological split by match 70 / 15 / 15  (test matchIds frozen)
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
        train      validation      test (used once, at the end)
          │            │
          ▼            ▼
 M3/M4  sklearn Pipeline (imputer, scaler, encoder fitted on train only) + model
                       │
                       ▼
     predicted rating  →  metrics (MAE, RMSE, R², within-match Spearman)  →  results/
```

## Folders

| Folder | Role | Tracked by git |
|---|---|---|
| `src/footrating/` | Python package: all reusable code. `config.py` loads `configs/default.yaml` and the global seed. `data/` downloads the raw files (`download.py`), writes the inventory (`inventory.py`) and builds the quarantine table (`side_info.py`). `features/`, `split.py`, `models/`, `evaluation/` *(planned)* | yes |
| `scripts/` | Command-line utilities: synthetic fixture (`make_fixture.py`), Moodle archive (`make_zip.py`), raw data download, inventory and quarantine table (`download_raw_data.py`, T1) | yes |
| `tests/` | pytest suite run by `make check`; `tests/fixtures/` holds a small synthetic sample | yes |
| `notebooks/` | Exploration notebooks; they only call functions from `src/` and use relative paths | yes |
| `configs/` | YAML configs; `default.yaml` holds the seed, split fractions and paths | yes |
| `data/raw/`, `data/processed/` | Downloaded files and tables built by scripts | no (only `data/README.md`) |
| `results/` | Metrics and tables written by scripts; every number in the report comes from here | yes |
| `report/` | Project specification and final report | yes |
| `ai_governance/` | `CONTRIBUTIONS.md`, `PROMPT_LOG.md`, `AI_AUDIT.md` | yes |
| `docs/` | This file, `decisions/` (one record per choice), `journal.md` (hand-over notes), `PLAN.md` (task state), `boucles.md` (loops) | yes |
| `.github/` | CI (`make check` on each pull request), PR and issue templates | yes |

## Guardrails built into the layout

- The split is by match and chronological; tests check that no `matchId` is in two sets and
  that test dates come after train dates *(planned, M3)*.
- Every transformation is fitted inside a scikit-learn `Pipeline` on the training set only.
- Columns published with the target (`minutesPlayed`, `goalScored`) live in a separate
  quarantine table until a written decision allows them.
