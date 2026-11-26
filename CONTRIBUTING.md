# Contributing

Two contributors (Clément, Paul). Every change goes through a pull request reviewed by the other.

## Workflow

1. Start from an up-to-date `main`: `git switch main && git pull`.
2. One branch per task, named by type:
   - `feat/<short-name>`: new code or document (e.g. `feat/t1-download-raw-data`);
   - `fix/<short-name>`: bug fix;
   - `exp/<short-name>`: experiment (one config file, one line in `results/experiments.csv`).
3. Short, prefixed commits: `feat: ...`, `fix: ...`, `docs: ...`, `test: ...`, `chore: ...`, `exp: ...`.
4. Run `make check` locally (it must exit with code 0).
5. Open a pull request with the template (what changes, why, how to check).
6. The other teammate reviews; CI (`make check`) must be green.
7. **Squash merge** into `main`, then delete the branch.

## Forbidden

- Pushing directly to `main`.
- Force pushing (`git push --force`, `--force-with-lease`, `-f`).
- Committing secrets (`.env`, tokens, API keys): use `.env.example` for variable names only.
- Committing data (`data/`, `*.parquet`, raw JSON) or trained models (`models/`, `*.pkl`, `*.joblib`).
  Small synthetic samples for tests go in `tests/fixtures/`.

## Rules that protect the results

- No data leakage: split by match and chronologically; fit every transformation on the
  training set only, inside a scikit-learn `Pipeline`; never use the test set to choose a
  model, a feature or a hyperparameter.
- Every number in `docs/` or `report/` comes from a script in this repository and a file in
  `results/`; the pull request says which command reproduces it.
- Use the global seed from `configs/default.yaml` (`footrating.config.get_seed()`).
