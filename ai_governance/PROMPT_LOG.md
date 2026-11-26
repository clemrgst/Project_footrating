# Prompt Log

High-stakes prompts used with the AI assistant (target: 4 to 6 entries, at least one per team member).

## Entry 1 — Project definition and dataset selection

- **Date:** 2026-11-21
- **Author:** Clément
- **Module:** project definition (all modules; mainly M1 and M3)
- **Objective:** find a legal public dataset with per-player, per-match statistics and a per-match rating, then write the week-1 project specification.

**Exact prompt:**

```
[Paste prompt 0 exactly as sent, from "Nous sommes Clément et Paul, ESILV A4, majeure DIA (DIA 6)…" to "…voir le prompt 3 pour le format)."]
```

**Constraints imposed on the AI:**

- *Data schema:* one row = one player in one match; continuous target on the source's scale; features limited to in-match player statistics, minutes played and position.
- *Evidence:* nothing stated without seeing it on the page; unverifiable facts (licence, columns, size) marked "NOT VERIFIED"; at most 3 candidates with URL, licence, rows, matches, seasons, columns, target column and visible missing values.
- *Legality:* no dataset requiring scraping of a site whose terms forbid it.
- *Leakage guardrails:* no feature computed from or published with the target (e.g. man of the match, rating rank); split by match, chronological, 70/15/15; test set frozen and never used for model selection; scaler fitted on train only.
- *Process:* stop after the dataset step and wait for our choice; show the specification before saving; list assumptions at the end.

**Summary of the AI's answer:**

- Step 1: two valid candidates. (A) Wyscout public dataset + PlayeRank scores (figshare, 1,941 matches, target `playerankScore`); (B) Fantasy Premier League data (vaastav repository, target `total_points`). Four other sources rejected (season-level only, paywalled, or derived from WhoScored). StatsBomb Open Data + VAEP fallback described in 10 lines. Row counts and some licences marked NOT VERIFIED because downloads were blocked.
- Step 2: drafted `report/project_specification.md` with the 10 required sections, using the five 2017/18 leagues only, and a list of 9 assumptions.

**What we kept / rejected:**

- Kept: candidate A.
- Corrected: the AI marked the licence of `playerank.json` as NOT VERIFIED; we checked figshare and found CC BY 4.0. The AI took the documented 0–1 scale at face value at first; the figshare sample values (about −0.03 to 0.07, some negative) contradict it, so the specification describes the target on its raw observed scale.
- Changed after review: `minutesPlayed` and `goalScored` moved to a separate quarantine table until a week-2 decision; target kept on its raw scale; fixed module owners replaced by nominal owners plus a fixed task allocation per week (not based on our timetables) so both of us work on every module.
- [To complete by us: anything else.]

## Entry 2 — Git repository set-up

- **Date:** 2026-11-25
- **Author:** Clément
- **Module:** infrastructure (all modules; protects M1 data handling)
- **Objective:** turn the project folder into a reproducible two-person git repository with the layout defined in the specification and the Moodle structure (prompt 2): environment, Makefile, CI, contribution rules, no data in git.

**Exact prompt:**

```
[Paste prompt 2 exactly as sent.]
```

**Constraints imposed on the AI:**

- *Data schema:* follow the specification layout: raw files in `data/raw/`, processed tables in `data/processed/`, including the quarantine table `playerank_side_info.parquet` for `minutesPlayed` and `goalScored`, which must stay apart from the feature table.
- *Leakage and data guardrails:* no data, model or secret in git; the course PDF and personal planning files stay local.
- *Safety:* check first that the repository is not in a synced folder (OneDrive, Google Drive, Dropbox, iCloud); ask before creating a remote repository or pushing; never push to main, never force push.
- *Process:* deliverables in English; propose the PROMPT_LOG entry for our review before it is committed.

**Summary of the AI's answer:**

- Checked that the repository path (`C:\Users\cleme\dev\Projet_footrating`) is outside the OneDrive folder.
- Ran `git init -b main`; created `src/`, `tests/fixtures/`, `notebooks/`, `configs/`, `results/`, `docs/decisions/`, `data/raw/` and `data/processed/` (empty folders kept with `.gitkeep`), and `data/README.md` (sources, licences, quarantine table).
- Rewrote `.gitignore` so that everything in `data/` is ignored except the README and the two empty folders, plus models, `*.parquet`, `*.pkl`, `*.joblib`, secrets, `docs/planning/` and the course PDF. Checked with `git check-ignore -v` on dummy files.
- Commit `00e1632` on top of the existing GitHub `main` (`6ca1957`): specification, PROMPT_LOG entry 1, README, CLAUDE.md, prompts file and folder layout. `docs/guide/guide-demarrage-projet-ml.pdf` was already on GitHub; at our request it was removed from git and added to `.gitignore` (it remains in the history of the first commit).
- On branch `feat/repo-tooling` (commits `f02181a`, `453c517`, `a6be57c`): uv environment (Python 3.12, `uv.lock`, `requirements.txt` exported from it), Makefile (`install`, `format`, `lint`, `test`, `requirements`, `check`, `zip`), global seed in `configs/default.yaml`, smoke test on a small synthetic fixture, GitHub Actions running `make check` on each pull request, `CONTRIBUTING.md`, PR and issue templates, pre-commit (ruff, no commit to main), `.claude/settings.json` denying force pushes and pushes to main (syntax checked on the official Claude Code permissions page).
- Checked that `make check` exits 0 when tests pass and non-zero when a test fails, and runs in about 10 to 16 seconds; listed the content of the zip (31 files, no data, no model).
- Pushed `feat/repo-tooling` after our approval. The push to `main` was blocked by the AI's permission settings, so we pushed `main` ourselves.

**What we kept / rejected:**

- Kept: the folder layout, the `.gitignore` rules for data and models, the uv + Makefile + CI set-up, `make check` as the single quality gate, and the list of branch protections for `main` (we turned them on in GitHub).
- Corrected: the AI first read the task narrowly (init and first commit only); we pointed it to the full prompt 2.
- Corrected: the AI offered to create a new GitHub repository; one already existed (`Projet_footrating`), so it rebuilt its commits on top of the existing `main` instead of overwriting it.
- Corrected: the commands the AI gave us to check its work (`git log`, `mingw32-make check`) failed because they did not start with `cd` into the project folder.
- Changed: the start-up guide PDF was removed from git and ignored (the AI had kept it tracked and only excluded it from the zip); the zip is named `Group_footrating_DS_Project.zip` because we have no group number.
- [To check by us before the submission.]
