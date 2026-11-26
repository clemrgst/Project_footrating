## What changes

<!-- Task ID (e.g. T4), module (M1–M4), files touched. -->

## Why

<!-- The problem solved or the decision applied (link to docs/decisions/ if any). -->

## How to check

<!-- Exact commands to run and what the reviewer should see. -->

- [ ] `make check` passes locally
- [ ] No data, model or secret committed
- [ ] No leakage: transformations fitted on train only; test set not used for selection
- [ ] Every new number comes from a script and a file in `results/`
