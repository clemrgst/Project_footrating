"""Minimal schema test on the SYNTHETIC player-match fixture (the real table is T4)."""

from pathlib import Path

import pandas as pd

FIXTURE = Path(__file__).parent / "fixtures" / "sample_player_match.csv"
COLUMNS = [
    "matchId",
    "playerId",
    "dateutc",
    "position",
    "minutes",
    "passes",
    "accurate_passes",
    "shots",
    "playerankScore",
]


def test_fixture_columns():
    df = pd.read_csv(FIXTURE)
    assert list(df.columns) == COLUMNS


def test_fixture_key_is_unique():
    df = pd.read_csv(FIXTURE)
    assert not df.duplicated(subset=["matchId", "playerId"]).any()
