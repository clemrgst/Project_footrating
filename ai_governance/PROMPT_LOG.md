# Prompt Log

High-stakes prompts used with the AI assistant (target: 4 to 6 entries, at least one per team member).

## Entry template

Copy this block for each new entry, numbered in order.

```markdown
## Entry N — <short title>

- **Date:** YYYY-MM-DD
- **Author:** Clément / Paul
- **Module:** M1 / M2 / M3 / M4 / project-wide
- **Objective:** what we wanted from the AI, in one sentence.

**Exact prompt:**

    <the prompt exactly as sent>

**Constraints imposed on the AI:**

- *Data schema:* …
- *Assumptions:* …
- *Leakage guardrails:* …

**Summary of the AI's answer:**

- …

**What we kept / rejected:**

- Kept: …
- Rejected or corrected: … (and why)
```

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

## Entry 3 — Loop engineering, levels 1 and 2

- **Date:** 2026-11-26
- **Author:** Paul
- **Module:** project-wide (infrastructure; quality gate for all modules)
- **Objective:** make sure `make check` is a reliable, fast judge, then build a goal-driven loop (`/boucle` skill + `docs/PLAN.md`) that works on one task until `make check` exits 0, with a cap and a documented way to stop it (prompt 5, T20).

**Exact prompt:**

```
Mets en place notre loop engineering, niveaux 1 et 2. Arrête-toi après chaque niveau pour me montrer ce que tu as fait et attendre mon accord. Note dans docs/boucles.md où nous en sommes.

Niveau 1, le juge : vérifie que `make check` est fiable (il échoue quand un test échoue, passe sinon) et rapide. Il doit inclure les tests de schéma des données et de non-fuite du split dès qu'ils existent.

Niveau 2, la boucle par objectif : crée docs/PLAN.md (tâches, module, propriétaire, état, prochain pas) et un skill /boucle qui prend une tâche, travaille jusqu'à ce que `make check` renvoie 0, s'arrête après 10 tours, met à jour docs/PLAN.md et résume ce qui bloque. /boucle ne modifie jamais un test pour le faire passer sans me le signaler.

Pour chaque boucle, écris dans docs/boucles.md : déclencheur, condition d'arrêt, plafond, comment la couper. Vérifie la syntaxe dans la documentation officielle, et teste chaque niveau sur une petite tâche réelle.

Avant de coder, donne-moi un plan étape → vérification et attends mon accord. Montre-moi chaque document avant de l'enregistrer. Ne fais aucun commit et ne touche pas au miroir.
```

**Constraints imposed on the AI:**

- *Process:* give a `step → verify` plan and wait for our OK before coding; stop after each level; show every document before saving it; no commit; do not touch the mirror repository; stop before the real `/boucle` test so that we type `/boucle` ourselves.
- *Evidence:* check the skill syntax in the official documentation and cite the exact page; do not use a frontmatter field that is not on that page; do not add a task to `docs/PLAN.md` without a source.
- *Leakage guardrails:* `make check` must include the data schema tests and the split leakage tests as soon as they exist; `/boucle` never modifies an existing test to make it pass without telling us.
- *Loop limits:* one round = one run of `make check`, cap of 10 rounds; the real test is a minimal schema test on the synthetic fixture only (the real player-match table is T4).

**Summary of the AI's answer:**

- Level 1: no change to the `Makefile`. On the clean branch `make check` exited 0 in 3.9 s (6 passed); with a temporary failing test it exited 2 (`1 failed, 6 passed`); with a temporary lint error (unused import) it exited 2 before the tests ran. The temporary files were deleted and `git status` was shown empty. Pytest collects all of `tests/`, so future schema and leakage tests join the judge with no change.
- Level 2: `docs/PLAN.md` (state of tasks T1–T22 from `docs/repartition.md`, Section 10 of the specification and `git log`); `.claude/skills/boucle/SKILL.md` (manual trigger only, optional sub-goal after the task ID, cap of 10 rounds, stop before changing an existing test, never edit the judge); `docs/boucles.md` (trigger, stop condition, cap, how to cut it, for each level); one line added to `docs/ARCHITECTURE.md`. Skill syntax checked on https://code.claude.com/docs/en/skills and stop keys on https://code.claude.com/docs/en/interactive-mode.
- Real test: `/boucle T20 minimal schema test on tests/fixtures/sample_player_match.csv only …` created `tests/test_fixture_schema.py` (column list and unique `matchId` + `playerId`); round 1/10, `make check` exit 0, 8 passed.
- Errors the AI caught itself: it first ran `mingw32-make`, which is not installed on this PC, then used GNU `make`; its first temporary failing test (`assert False`) was stopped by ruff (B011) before pytest ran, so it repeated the test with a lint-clean failing assertion.
- No commit yet (files left uncommitted for our review).

**What we kept / rejected:**

- Kept: the unchanged `Makefile`; the "do not bend the judge" rule in `/boucle` (no edits to the `Makefile`, CI, ruff or pytest settings, no `# noqa`), which the AI added beyond our request; the T22 row in `docs/PLAN.md` (source: `docs/repartition.md:70`).
- Corrected: the stop rule "stop before any change in `tests/`" was too broad and would have blocked the real test; we limited it to changing an existing test to make it pass (new test files stay allowed).
- Corrected: the reproduce command `make check; echo $?` is wrong in PowerShell (`$?` is True/False); we asked for `echo $LASTEXITCODE` (PowerShell) or `echo $?` (bash).
- Corrected: the owner of T3 was marked NOT VERIFIED; Section 10 of `report/project_specification.md` gives "Both".
- Corrected: `/boucle T20` would have read T20's own "Done when" and looped on itself; we added an optional sub-goal after the task ID, which replaces the "Done when" for that loop.
- Added: a limitation in `docs/boucles.md`: the goal was met in round 1, so the run did not exercise recovery from a failure or the 10-round cap.
