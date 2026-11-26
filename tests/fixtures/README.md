# Test fixtures

`sample_player_match.csv` is a small **synthetic** sample (random values, not real
Wyscout or PlayeRank data) with the shape of the future player-match table. It is used by
the smoke test in `make check`. Regenerate it with `uv run python scripts/make_fixture.py`.
