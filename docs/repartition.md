# Work split — who does what, and when

How Clément and Paul share the work week by week. There is no hourly schedule: each week
both work in parallel, and the dependencies below say who waits for whom. Task IDs (T1–T20)
and estimates come from `report/project_specification.md`, Section 10; module owners from
`ai_governance/CONTRIBUTIONS.md`. Each task has one GitHub issue.

**Module owners:** M1 Paul · M2 Clément · M3 Paul · M4 Clément. When a task sits in the other
member's module, read `docs/ARCHITECTURE.md` and the decision records of that module first,
and let its owner review the PR.

## Week 1 — Definition (15 %)

Already merged: specification (T3), repository and tooling, governance files and
architecture documentation.

| Clément | Paul |
|---|---|
| **T2 · M3 (Paul's)** Chronological match split 70/15/15; frozen list of test `matchId`s committed in `configs/`; leakage tests. **Done when:** `make check` runs tests showing no `matchId` in two sets and every test date after every train date. | **T1 · M1 — first task of the project** Download raw Wyscout and PlayeRank files with a script; inventory (files, sizes, row counts); count player-match rows; build `data/processed/playerank_side_info.parquet`. **Done when:** `data/README.md` lists every file with a count produced by the script, and a test checks the quarantine table keys are unique. |
| **T21 · all** Organisation: this file and the GitHub issues. **Done when:** this file is merged and every task has an issue. | **T20 · all** Quality gate: reliable `make check` (it fails when a test fails, passes otherwise, under one minute) and `docs/PLAN.md` (tasks, owner, status, next step). **Done when:** `make check` is shown to fail on a deliberately failing test and `docs/PLAN.md` is merged. |

**Start:** the project work starts with Paul's T1 (raw data), the first pull request after
the set-up.

**Dependency:** Clément writes T2 on the synthetic fixture first, then runs it on the real
matches file only after Paul's T1 PR is merged.

**Reviews:** Clément reviews T1 and T20; Paul reviews T2 and T21.

**Sync point (end of week 1):** T1, T2, T20 and T21 merged on `main`; frozen test `matchId`s
on `main`.

## Week 2 — Data and baseline (25 %)

| Clément | Paul |
|---|---|
| **T5 · M1 (Paul's)** Recompute minutes and goals from line-ups, substitutions, red cards and goal events; join the target; schema tests; join-rate report; decision record on the quarantined columns. **Done when:** join rate in `results/` from a script, schema test in `make check`, record in `docs/decisions/`. | **T4 · M1** Aggregate events into `data/processed/player_match.parquet`, one row per (`matchId`, `playerId`); schema shown to Clément before coding. **Done when:** a test checks the unique key and column types; row count printed by the script. |
| **T8 · M3 (Paul's)** Metric functions (MAE, RMSE, R², within-match Spearman) and position-mean baseline. **Done when:** unit tests on hand-computed values pass. | **T7 · M2 (Clément's)** Feature engineering: rates, per-90 features, spatial shares. **Done when:** feature functions are tested on the fixture and fitted only inside the Pipeline. |
| **T6 · M2** Cleaning (missing values, duplicates, low-minute rule) and EDA notebook calling only `src/` functions. **Done when:** the notebook runs top to bottom and each rule has a decision record. | **T9 · M3** Ridge baseline (alpha chosen on validation only); `results/baseline_results.csv`; error analysis (MAE per position, 10 largest errors). **Done when:** the CSV is produced by one command given in the PR. |

**Dependencies:**
- Clément starts the **join** in T5 only after Paul's T4 PR is merged. Meanwhile he writes
  the minutes and goals recomputation on the raw events (from Paul's T1) and the T8 metric
  functions on the fixture.
- Clément starts T6 only after T5 is merged.
- Paul starts T7 only after T5 is merged. Meanwhile he prepares the Ridge Pipeline of T9 on
  the fixture.
- Paul runs T9 on real data only after T2, T7 and T8 are merged.

**Reviews:** Clément reviews T4, T7 and T9; Paul reviews T5, T6 and T8. Review within one
working day of the PR, so the waiting member is not blocked.

**Governance checkpoint:** Paul writes PROMPT_LOG entry 3 (M1 data preparation). Each of us writes at least one AI_AUDIT entry from a
real error caught so far (Clément may start from those caught in week 1). No entry is
written without a real error.

**Sync point (end of week 2):** T4–T9 merged; `results/baseline_results.csv` and the
baseline table in `report/` on `main`.

## Week 3 — Models and experiments (30 %)

| Clément | Paul |
|---|---|
| **T22 · all** Quality automation: automatic lint and format on every change, a review checklist applied before every PR, and a proposal for an automated PR review in CI (not activated). **Done when:** each part is tested on a small real task and documented. | Starts **T12** and the bootstrap function of T14 (see below) while T22 is in review. |
| **T10 · M4** Gradient boosting tuned with `GroupKFold` by match on train. **Done when:** one line per run in `results/experiments.csv` (config, seed, scores); search budget written in the config. | **T12 · M4 (Clément's)** Random Forest tuned with `GroupKFold`. **Done when:** same criterion as T10. |
| **T11 · M4** Feature importance (permutation, SHAP) and football sanity check per position; flag any feature that looks like leakage. **Done when:** figure and table in `results/`, comment in the PR. | **T13 · M4 (Clément's)** Position-aware model (one model per position, or interactions). **Done when:** same criterion as T10. |
| | **T14 · M4 (Clément's)** Comparison table with bootstrap 95 % CIs over test matches; the test set is used once, here. **Done when:** table in `results/` produced by one command. |

**Dependencies:**
- Clément starts T22 only after Paul's T9 PR (baseline) is merged, and T10 only after T22
  is merged.
- Paul does not wait for T22: he starts T12 and the T14 bootstrap function, then applies the
  T22 checks to his PR once T22 is merged.
- Clément starts T11 only after T10 is merged.
- Paul starts T14 only after T10, T12 and T13 are merged. Meanwhile he writes the bootstrap
  function and tests it on the fixture.

**Reviews:** Paul reviews T22, T10 and T11; Clément reviews T12, T13 and T14.

**Governance checkpoint:** Clément writes a PROMPT_LOG entry for T10, Paul one
for T13. Each of us adds an AI_AUDIT entry if a new real error was caught.

**Sync point (end of week 3):** T22 and T10–T14 merged; `results/experiments.csv` and the comparison
table on `main`.

## Week 4 — Report and defence (30 %)

| Clément | Paul |
|---|---|
| **T15** Report: introduction, data, methodology, interpretation. **Done when:** every number links to a file in `results/`. | **T16** Report: results, critical analysis, AI governance summary, conclusion. **Done when:** same criterion as T15. |
| **T17** Slides 1–5 and oral preparation on M2 and M4. | **T18** Slides 6–10 and oral preparation on M1 and M3. |
| **T19** (both) Final checks: `make check`, `make zip`, governance files complete; rehearsal. | **T19** (both) idem |

**Dependencies:** T16's results section waits for T14. T19 waits for T15–T18.

**Reviews:** each reviews the other's report part and slides.

**Sync point (end of week 4):** report PDF, slides and governance files merged; zip built
from `main`.

## Balance and governance targets

| | Clément | Paul |
|---|---|---|
| Tasks | T2, T5, T6, T8, T10, T11, T15, T17, T19, T21, T22 | T1, T4, T7, T9, T12, T13, T14, T16, T18, T19, T20 |
| Estimated load (spec, Section 10) | about 30 h + T21, T22 | about 31 h + T20 |
| PROMPT_LOG entries | 1, 2 (done), T10 | T4, T13 (and optionally T9) |
| AI_AUDIT entries | at least 1 (week 2 checkpoint) | at least 1 (week 2 checkpoint) |
