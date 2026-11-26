"""Leakage tests for the chronological split by match (T2, M3).

The first tests use the SYNTHETIC fixture and hand-made dates; the last ones check the
frozen split committed in configs/split_matches.csv (real matchIds, no raw data needed).
"""

from pathlib import Path

import pandas as pd
import pytest

from footrating.config import load_config
from footrating.split import LEAGUES, load_frozen_split, split_matches

FIXTURE = Path(__file__).parent / "fixtures" / "sample_player_match.csv"
FRACTIONS = load_config()["split"]


def assert_no_leakage(split: pd.DataFrame) -> None:
    """No matchId in two sets; train < validation < test dates, strictly."""
    assert not split["matchId"].duplicated().any()
    dates = split.groupby("split")["dateutc"]
    assert dates.max()["train"] < dates.min()["validation"]
    assert dates.max()["validation"] < dates.min()["test"]


def fixture_matches() -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = pd.read_csv(FIXTURE, parse_dates=["dateutc"])
    return rows, rows[["matchId", "dateutc"]].drop_duplicates()


def test_fixture_split_has_no_leakage():
    _, matches = fixture_matches()
    split = split_matches(matches, FRACTIONS)
    assert_no_leakage(split)
    # 6 matches: round(0.70 * 6) = 4 train, round(0.85 * 6) = 5, so 1 validation, 1 test
    assert split["split"].value_counts().to_dict() == {"train": 4, "validation": 1, "test": 1}


def test_all_players_of_a_match_in_the_same_set():
    rows, matches = fixture_matches()
    split = split_matches(matches, FRACTIONS)
    merged = rows.merge(split[["matchId", "split"]], on="matchId", validate="many_to_one")
    assert len(merged) == len(rows)
    assert merged.groupby("matchId")["split"].nunique().eq(1).all()


def test_same_kickoff_is_never_cut():
    # 20 matches on 20 days, except matches 13, 14 and 15 (0-based) which share a kick-off.
    # The train cut round(0.70 * 20) = 14 falls inside that group, so it moves to 16.
    days = [*range(1, 14), 14, 14, 14, *range(15, 19)]
    dates = pd.to_datetime([f"2018-01-{d:02d} 20:00" for d in days])
    matches = pd.DataFrame({"matchId": range(20), "dateutc": dates})
    split = split_matches(matches, FRACTIONS)
    assert_no_leakage(split)
    assert split["split"].value_counts().to_dict() == {"train": 16, "test": 3, "validation": 1}


def test_split_does_not_depend_on_row_order():
    _, matches = fixture_matches()
    a = split_matches(matches, FRACTIONS)
    b = split_matches(matches.sample(frac=1, random_state=0), FRACTIONS)
    pd.testing.assert_frame_equal(a, b)


def test_duplicate_matchid_raises():
    _, matches = fixture_matches()
    with pytest.raises(ValueError, match="unique"):
        split_matches(pd.concat([matches, matches.head(1)]), FRACTIONS)


def test_frozen_split_has_no_leakage():
    split = load_frozen_split()
    assert_no_leakage(split)
    assert set(split["competition"]) == set(LEAGUES)
    assert len(split) == 380 * 4 + 306  # data/README.md: four leagues of 380, Germany 306


def test_frozen_split_fractions_match_config():
    shares = load_frozen_split()["split"].value_counts(normalize=True)
    for name, frac in FRACTIONS.items():
        assert shares[name] == pytest.approx(frac, abs=0.01)
