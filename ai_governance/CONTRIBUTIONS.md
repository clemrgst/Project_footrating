# Contributions

Team: Clément and Paul (ESILV A4). Each module has one nominal owner, who answers for it at
the oral defence, and one reviewer. Both members work on every module through the task
allocation in `report/project_specification.md`, Section 10.

## Module matrix

| Module | Content | Owner | Reviewer | Files concerned |
|---|---|---|---|---|
| **M1** Data acquisition and player-match table | Download raw files, aggregate events, recompute minutes and goals, quarantine table, join the target, schema tests | Paul | Clément | `src/footrating/data/`, `data/README.md`, `tests/test_data_*.py` |
| **M2** Cleaning, EDA, features | Missing values, duplicates, low-minute rule, target distribution, correlations, per-90 features | Clément | Paul | `notebooks/01_eda.ipynb`, `src/footrating/features/`, `tests/test_features*.py` |
| **M3** Split, baselines, evaluation | Chronological match split, leakage tests, position-mean and Ridge baselines, metrics, error analysis | Paul | Clément | `src/footrating/split.py`, `src/footrating/models/`, `src/footrating/evaluation/`, `tests/test_split*.py`, `results/baseline_results.csv` |
| **M4** Advanced models and analysis | Random Forest, gradient boosting, position-aware model, grouped CV, bootstrap CIs, feature importance | Clément | Paul | `src/footrating/models/`, `configs/`, `results/experiments.csv` |

Shared files (both members): `README.md`, `CONTRIBUTING.md`, `Makefile`, `pyproject.toml`,
`report/`, `ai_governance/`, `docs/`.

## Task allocation

Task-level allocation (who does, who reviews, estimate) is in
`report/project_specification.md`, Section 10, and its status in `docs/PLAN.md`.

The file paths above are the planned layout; they are updated in the same pull request when
the code is written.
