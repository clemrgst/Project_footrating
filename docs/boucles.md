# Loops — where we are

How we run quality loops on this project, level by level. Each loop has a trigger,
a stop condition, a cap and a way to cut it.

| Level | Loop | Status | Task |
|---|---|---|---|
| 1 | The judge: `make check` | Done | T20 |
| 2 | Task loop on `docs/PLAN.md` | Done | T20 |
| 3–5 | Automatic lint and format, review checklist, PR review proposal | Not started | T22 |

## Level 1 — The judge (`make check`)

`make check` runs `lint` (ruff check + ruff format --check on `src`, `tests`, `scripts`)
then `test` (pytest on every file in `tests/`). It exits 0 only if both pass. CI runs the
same command on every pull request (`.github/workflows/ci.yml`).

- **Trigger:** by hand before every commit, and in CI on every pull request.
- **Stop condition:** exit code 0 = pass; any other code = fail. Lint runs first, so a lint
  error stops the run before the tests.
- **Cap:** one run; it must stay under one minute.
- **How to cut it:** Ctrl+C in the terminal; in CI, cancel the workflow run on GitHub.

**Reliability check (T20, 2026-11-26, branch `feat/loops-level-1-2`, GNU Make 4.4.1, Windows):**

| Case | Expected | Observed |
|---|---|---|
| Clean branch | exit 0 | exit 0, 6 passed, 3.9 s |
| Temporary failing test (`assert 1 + 1 == 3`) | exit ≠ 0 | exit 2, `1 failed, 6 passed` |
| Temporary lint error (unused import) | exit ≠ 0 | exit 2, ruff F401, tests not run |

The temporary files were deleted and `git status` was empty afterwards. Reproduce by adding
such a file to `tests/`, then running `make check; echo $LASTEXITCODE` (PowerShell) or
`make check; echo $?` (bash).

**Data schema and split leakage tests:** pytest collects everything in `tests/`
(`testpaths` in `pyproject.toml`), so these tests join the judge as soon as they are merged,
with no change to the `Makefile`. Today: the leakage tests (T2) and the player-match schema
test (T4) do not exist yet.

## Level 2 — Task loop on `docs/PLAN.md`

We work on one task of `docs/PLAN.md` until the judge passes, then update that task's row
(State, Next step) and note what blocks.

- **Trigger:** a teammate starts a task listed in `docs/PLAN.md`.
- **Stop condition:** `make check` exits 0 and the task's "Done when" from
  `docs/repartition.md` is met; or an existing test would have to change (we stop and
  discuss it with the module owner); or the cap is reached.
- **Cap:** 10 rounds; one round = one run of `make check`. Past the cap, we stop and
  discuss the task with the other teammate.
- **How to cut it:** Ctrl+C interrupts a running `make check`.

**Test run (T20, 2026-11-26):** a small real task, a minimal schema test on
`tests/fixtures/sample_player_match.csv` only (expected columns, unique `matchId` +
`playerId`), added `tests/test_fixture_schema.py` (two tests, no existing test changed);
round 1/10, `make check` exit 0, 8 passed. Limitation: the goal was met in round 1, so this
run did not exercise recovery from a failure or the 10-round cap.
