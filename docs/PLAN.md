# Plan — task state

One row per task. Source of tasks, owners and dependencies: `docs/repartition.md`.
"Owner" is who does the task; "Module" is the module it belongs to (its owner reviews).
Whoever works on a task updates its State and Next step.
Last update: 2026-11-26 (T20).

States: To do · In progress · In review · Done.

| Task | Module | Owner | State | Next step |
|---|---|---|---|---|
| T1 Raw data download, inventory, quarantine table | M1 | Paul | Done (merged, `66d2bbc`) | — |
| T2 Chronological match split, frozen test `matchId`s, leakage tests | M3 | Clément | To do | Write split and leakage tests on the fixture, then run on real matches (T1 merged) |
| T3 Project specification | — | Both (`report/project_specification.md`, Section 10) | Done (repartition.md: "Already merged") | — |
| T4 Player-match table `player_match.parquet` | M1 | Paul | To do | Show the schema to Clément before coding |
| T5 Minutes and goals from events, target join, schema tests | M1 | Clément | To do | Recompute minutes and goals on raw events; join waits for T4 |
| T6 Cleaning and EDA notebook | M2 | Clément | To do | Waits for T5 |
| T7 Feature engineering | M2 | Paul | To do | Waits for T5 |
| T8 Metric functions and position-mean baseline | M3 | Clément | To do | Write metric functions with hand-computed tests on the fixture |
| T9 Ridge baseline and error analysis | M3 | Paul | To do | Prepare the Ridge Pipeline on the fixture; real data waits for T2, T7, T8 |
| T10 Gradient boosting with `GroupKFold` | M4 | Clément | To do | Waits for T22 |
| T11 Feature importance and sanity check | M4 | Clément | To do | Waits for T10 |
| T12 Random Forest with `GroupKFold` | M4 | Paul | To do | Week 3; starts while T22 is in review |
| T13 Position-aware model | M4 | Paul | To do | Week 3 |
| T14 Comparison table with bootstrap CIs (test set used once) | M4 | Paul | To do | Write the bootstrap function on the fixture; table waits for T10, T12, T13 |
| T15 Report: introduction, data, methodology, interpretation | — | Clément | To do | Week 4 |
| T16 Report: results, critical analysis, governance, conclusion | — | Paul | To do | Week 4; results section waits for T14 |
| T17 Slides 1–5, oral on M2 and M4 | — | Clément | To do | Week 4 |
| T18 Slides 6–10, oral on M1 and M3 | — | Paul | To do | Week 4 |
| T19 Final checks and rehearsal | — | Both | To do | Waits for T15–T18 |
| T20 Quality gate: `make check` and `docs/PLAN.md` | all | Paul | In progress | PROMPT_LOG entry → commit → pull request; Clément reviews |
| T21 Organisation: repartition.md and GitHub issues | all | Clément | Done for repartition.md (merged, PR #2); issues NOT VERIFIED | Check that every task has an issue |
| T22 Quality automation (lint/format, review checklist, PR review proposal) | all | Clément | To do | Waits for T9 |
