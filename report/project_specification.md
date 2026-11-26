# Project Specification — Predicting Football Player Match Ratings from Match Statistics

*ESILV A4 — Machine Learning, LAB 5 (Full Project) — Week 1 milestone*

## 1. Project Title

**Predicting per-match football player ratings from in-match event statistics**

## 2. Team Members

| Member | Programme | Nominal module owner |
|---|---|---|
| Clément [surname] | ESILV A4, DIA major (DIA 6) | M2, M4 |
| Paul [surname] | ESILV A4, DIA major (DIA 6) | M1, M3 |

Both members work on every module through a fixed allocation of tasks per week (Section 10); the nominal owner is accountable for the module at the oral defence.

## 3. Context and Motivation

Player ratings summarise a footballer's contribution to a match in one number. Clubs, scouts, media and fantasy games use them, but most published ratings are proprietary and their logic is opaque. Being able to reproduce a rating from transparent statistics lets an analyst explain it ("which actions drove this score?") and apply it to matches the rating provider does not cover.

The project fits our Data & Artificial Intelligence (DIA) major because it covers the full data science pipeline on a real, messy and large dataset: turning millions of raw, timestamped events into a tabular dataset, designing leakage-free features, building a reproducible regression model with honest validation, and interpreting it. It also raises a question that is central to applied AI: when a model learns to imitate another algorithm's scores, how close can it get and where does it disagree?

## 4. Problem Statement

Given the statistics of one player in one match (event counts and rates, minutes played, position), predict that player's PlayeRank score for that match.

**Research question:** On the most recent 15% of matches of the 2017/18 season of the five major European leagues, how much can a supervised regression model reduce the mean absolute error (MAE) of the per-match PlayeRank score compared with a position-mean baseline, and does it rank the players of the same match correctly (within-match Spearman correlation)?

## 5. Project Objectives

All targets below are set before seeing the data and will be revised only through a documented decision (`docs/decisions/`).

1. **Data (M1):** build a player-match table with one row per (`matchId`, `playerId`), with at least 95% of the `playerank.json` records for the selected matches joined to event statistics; the join rate is reported.
2. **Baseline (M3):** the Ridge baseline reduces validation MAE by at least 30% relative to the position-mean baseline.
3. **Advanced models (M4):** at least one advanced model reduces test MAE by at least 10% relative to Ridge, with a bootstrap 95% confidence interval (over test matches) that excludes zero improvement.
4. **Ranking quality:** mean within-match Spearman correlation of at least 0.80 on the test set for the best model.
5. **Reproducibility:** every reported number is produced by a script in the repository and stored in `results/`; `make check` runs in under one minute.
6. **Interpretation:** identify the 10 most important features (permutation importance) and check that they make football sense per position.

## 6. Dataset Description

**Sources** (both licensed **CC BY 4.0**):

- *Soccer match event dataset* (Wyscout), Pappalardo et al., *Scientific Data* 6:236 (2019), DOI 10.1038/s41597-019-0247-7. Files on figshare: <https://figshare.com/collections/_/4415000> (events, matches, players, teams, competitions, coaches, referees, JSON).
- *PlayeRanks* scores, DOI 10.6084/m9.figshare.9361148, file `playerank.json` (5.95 MB): <https://figshare.com/articles/PlayeRanks/9361148>. Method: Pappalardo et al., *PlayeRank*, ACM TIST 10(5), article 59 (2019).

**Size (from the data paper, Table 1):** 1,941 matches, 3,251,294 events and 4,299 players over seven competitions: Spain, England, Italy, Germany and France first divisions (2017/18, 1,826 matches), FIFA World Cup 2018 (64) and UEFA Euro 2016 (51). We use the **five leagues only** (see Assumptions). The number of player-match rows is **not yet verified**; we expect roughly 50,000 (about 28 players per match), to be confirmed by M1.

**Unit of observation:** one player in one match.

**Target:** `playerankScore`, one value per player per match. The source describes it as ranging from 0 (very bad) to 1 (excellent), but the sample values displayed on figshare are much smaller (about −0.03 to 0.07) and some are negative. We therefore predict it **on the raw scale of the source**, and EDA (M2) will report its actual range and distribution, overall and per position.

**Features** (all computed by us from the Wyscout events and match files):

- Event counts per player and match, by event and sub-event type (passes, accurate passes, key passes, crosses, shots, shots on target, goals, assists, duels and duels won, aerial duels, tackles, interceptions, clearances, dribbles, fouls, cards, saves for goalkeepers…), using Wyscout tags (e.g. accurate / not accurate).
- Success rates (e.g. pass accuracy) and per-90-minute versions where relevant.
- Simple spatial aggregates from event positions (e.g. share of actions in the final third).
- Minutes played and goals, recomputed by us from line-ups, substitutions, red cards and goal events in the Wyscout files.
- Position (goalkeeper, defender, midfielder, forward) from the players file (field name **not yet verified**).

**Forbidden columns (leakage):** `roleCluster` (computed by PlayeRank). No match outcome, team score or cross-match aggregate (e.g. season averages) is used as a feature.

**Quarantined columns:** `minutesPlayed` and `goalScored` are published in the same file as the target. M1 stores them, with the keys (`matchId`, `playerId`), in a separate table (`data/processed/playerank_side_info.parquet`) that is never joined to the feature table by default. In week 2 we compare them with our own values recomputed from the Wyscout files (line-ups, substitutions, red cards, goal events) and decide, in a written decision record (`docs/decisions/`), whether they may be used. Until then, features use only our recomputed minutes and goals.

**Limitations:**

- The target is algorithmic, not a human rating: PlayeRank is computed from the same Wyscout events with learned weights. A very high R² would partly mean we re-learned a formula; this is discussed, not hidden.
- One season only, so chronological validation happens within 2017/18 and says little about drift across seasons.
- Event data ignore off-ball work (positioning, pressing without contact), which affects defenders and goalkeepers.
- Missing values and data errors are not documented by the source; M2 will quantify them.

## 7. Machine Learning Task

- **Type:** supervised regression.
- **Input:** a vector of in-match statistics for one player (numerical), minutes played (numerical), position (categorical, one-hot encoded).
- **Output:** a continuous predicted `playerankScore` on the source's scale.
- **Models:** baselines in week 2; in week 3, Random Forest, gradient boosting (LightGBM or XGBoost) and a position-aware model (one model per position, or position × statistics interactions).

## 8. Baseline Strategy

1. **Position mean:** predict the mean target of the player's position, computed on the training set. It shows how much of the score is explained by role alone and is the floor every model must beat.
2. **Ridge regression:** linear model on standardised features and one-hot position. The scaler and encoder are fitted on the training set only, inside a scikit-learn `Pipeline`. The regularisation strength `alpha` is chosen on the validation set only. Ridge is appropriate because many count features are correlated (e.g. passes and accurate passes) and because PlayeRank itself is built from weighted event features, so a linear model is a strong and interpretable reference.

## 9. Evaluation Strategy

**Split:** by match, chronological, 70 / 15 / 15. All matches of the five leagues are sorted by kick-off date (`dateutc`); the oldest 70% of matches form the training set, the next 15% the validation set, the most recent 15% the test set. All players of a match fall in the same set. The test set is fixed in week 1 by a script that writes the list of test `matchId`s to the repository, and it is never used to select a model, a feature or a hyperparameter. Automated tests check that no `matchId` appears in two sets and that every test date is later than every training date.

**Validation for model selection:** validation set for the baselines; in week 3, `GroupKFold` cross-validation grouped by match on the training set, then a check on the validation set. Final scores are reported once on the test set.

**Metrics:**

- **MAE** (primary metric), on the target's scale.
- **RMSE**, to expose large errors.
- **R²**, for comparison with a constant predictor.
- **Within-match Spearman correlation:** for each match, Spearman correlation between predicted and true scores of its players, averaged over matches. It answers "does the model rank the players of a match correctly?".

Results are reported for validation and test, with bootstrap 95% confidence intervals over test matches, and broken down by position.

## 10. Initial Work Plan

**Modules and nominal owners** (the course requires one owner per module; the owner answers for it at the oral, but both members contribute to all four):

| Module | Content | Nominal owner |
|---|---|---|
| **M1** Data acquisition and player-match table | Download raw files; aggregate events into `data/processed/player_match.parquet`; recompute minutes and goals; quarantine table; join the target; schema tests; join-rate report | Paul |
| **M2** Cleaning, EDA, features | Missing values, duplicates, low-minute exclusion rule, target distribution per position, feature–target correlations, per-90 features | Clément |
| **M3** Split, baselines, evaluation | Chronological match split and leakage tests; position-mean and Ridge baselines; metric functions; error analysis | Paul |
| **M4** Advanced models and analysis | Random Forest, gradient boosting, position-aware model; grouped CV; bootstrap CIs; feature importance; critical analysis | Clément |

**Fixed task allocation.** Each task has one person who does it and is reviewed by the other through a pull request. Durations are estimates; the allocation does not depend on individual timetables.

| Week | ID | Module | Task | Done by | Reviewed by | Est. |
|---|---|---|---|---|---|---|
| 1 (15%) | T1 | M1 | Download raw files; inventory; count player-match rows; quarantine table for `minutesPlayed` and `goalScored` | Clément | Paul | 3 h |
| 1 | T2 | M3 | Chronological match split script; frozen list of test `matchId`s; leakage tests | Paul | Clément | 3 h |
| 1 | T3 | — | Project specification | Both | Both | 2 h each |
| 2 (25%) | T4 | M1 | Aggregate events into the player-match table | Paul | Clément | 5 h |
| 2 | T5 | M1 | Recompute minutes and goals; join the target; schema tests; join-rate report | Clément | Paul | 3 h |
| 2 | T6 | M2 | Cleaning (missing values, duplicates, low-minute rule) and EDA notebook | Clément | Paul | 4 h |
| 2 | T7 | M2 | Feature engineering (rates, per-90 features, spatial shares) | Paul | Clément | 2 h |
| 2 | T8 | M3 | Metric functions (MAE, RMSE, R², within-match Spearman); position-mean baseline | Clément | Paul | 2 h |
| 2 | T9 | M3 | Ridge baseline (alpha on validation); results table; error analysis | Paul | Clément | 3 h |
| 3 (30%) | T10 | M4 | Gradient boosting with `GroupKFold` tuning | Clément | Paul | 5 h |
| 3 | T11 | M4 | Feature importance (permutation, SHAP) and football sanity check | Clément | Paul | 3 h |
| 3 | T12 | M4 | Random Forest with `GroupKFold` tuning | Paul | Clément | 3 h |
| 3 | T13 | M4 | Position-aware model (per position or interactions) | Paul | Clément | 3 h |
| 3 | T14 | M4 | Comparison table with bootstrap 95% CIs over test matches | Paul | Clément | 2 h |
| 4 (30%) | T15 | — | Report: introduction, data, methodology, interpretation | Clément | Paul | 4 h |
| 4 | T16 | — | Report: results, critical analysis, AI governance, conclusion | Paul | Clément | 4 h |
| 4 | T17 | — | Slides 1–5 and oral preparation on M2 and M4 | Clément | Paul | 2 h |
| 4 | T18 | — | Slides 6–10 and oral preparation on M1 and M3 | Paul | Clément | 2 h |
| 4 | T19 | — | Final checks (`make check`, `make zip`, governance files) and rehearsal | Both | Both | 2 h each |

Estimated load: Clément about 30 h, Paul about 31 h. The status of each task is tracked in `docs/PLAN.md` and GitHub issues.

## Assumptions made in this document

1. Team members' surnames are unknown and left as placeholders; "DIA 6" is read as the group/class label.
2. Nominal module ownership (Clément: M2, M4; Paul: M1, M3) with a fixed task allocation in which both members work on every module is our reading of "1 owner per student" for a team of two; to confirm with the instructor.
3. World Cup 2018 and Euro 2016 are excluded from the main split: national-team tournaments differ from club leagues, and a chronological split would put the whole World Cup in the test set. They may be used as a separate out-of-distribution check.
4. `minutesPlayed` and `goalScored` from `playerank.json` are kept in a separate quarantine table until a week-2 decision; features use our own recomputed values meanwhile.
5. `playerank.json` contains one record per player per match for the five leagues; the record count and coverage are not yet verified.
6. The players file contains a position field usable as GK/DEF/MID/FWD; not yet verified.
7. All numeric objectives in Section 5 are targets chosen before seeing the data.
8. Events can be attributed to a player through `playerId`; events with no player (e.g. some ball-out events) are ignored.
9. Match outcome and team-level statistics are excluded from the features, to keep strictly to "the player's statistics in the match".
