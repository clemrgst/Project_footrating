# 0001 — Chronological split by match, frozen in configs/split_matches.csv

- **Date / author / module:** 2026-11-26 · Clément · M3
- **Status:** proposed
- **Context:** the specification (Section 9) asks for a split by match, chronological,
  70 / 15 / 15, with the test set frozen in week 1. The five leagues hold 1,826 matches
  (`data/README.md`, from `scripts/download_raw_data.py`). Several matches share the same
  kick-off time (up to 10 at once), and both cuts fall inside such a group: at match 1,278
  (2018-02-28 18:30) and at match 1,552 (2018-04-14 18:45) (`scripts/make_split.py`).
- **Choice:** sort the matches by (`dateutc`, `matchId`), cut at 70 % and 85 %, and move a
  cut that falls inside a group of identical kick-off times to the end of that group.
  Freeze the three sets (`matchId`, `dateutc`, `competition`, `split`) in
  `configs/split_matches.csv`; every module reads this file.
- **Alternatives rejected:**
  - Freeze only the test `matchId`s: the train/validation cut would be recomputed by each
    task and could move (for example if cleaning drops matches), so validation scores of
    T9 and T10 would not be comparable; the CI test could only check the test set.
  - Cut exactly at 70 % / 85 % of the matches: matches played at the same time would fall
    in two sets, so "every test date after every train date" would not hold strictly.
  - Split each league separately: the test set would no longer be "the most recent
    matches" overall.
- **Consequences:** 1,279 train (70.0 %), 275 validation (15.1 %), 272 test (14.9 %)
  matches. Train ends 2018-02-28 18:30, validation runs 2018-02-28 20:30 to 2018-04-14
  18:45, test 2018-04-15 10:00 to 2018-05-20 18:45. The Bundesliga ends a week earlier
  than the other leagues, so it has the fewest test matches (39, against 49 to 66).
- **Leakage check:** the split uses only kick-off dates and `matchId`, never the target or
  any feature. Whole matches are assigned, so all players of a match are in the same set.
- **How to verify:** `uv run python scripts/make_split.py` prints the counts above and
  "split_matches.csv unchanged"; `make check` runs `tests/test_split.py` (no `matchId` in
  two sets, train < validation < test dates, fractions within 1 point of the config).
- **Files:** `src/footrating/split.py`, `scripts/make_split.py`, `configs/split_matches.csv`,
  `tests/test_split.py`.
