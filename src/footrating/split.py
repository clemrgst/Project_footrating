"""M3: chronological train / validation / test split by match.

All players of a match fall in the same set because the split assigns whole matches.
The result is frozen in configs/split_matches.csv by scripts/make_split.py; every other
module reads that file instead of recomputing the split.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from footrating.config import PROJECT_ROOT

LEAGUES = ("England", "France", "Germany", "Italy", "Spain")
FROZEN_SPLIT = PROJECT_ROOT / "configs" / "split_matches.csv"


def load_matches(raw_dir: Path) -> pd.DataFrame:
    """One row per match of the five leagues: matchId, dateutc, competition.

    World Cup and European Championship are left out (specification, assumption 3).
    """
    rows = []
    for league in LEAGUES:
        path = raw_dir / f"matches_{league}.json"
        for m in json.loads(path.read_text(encoding="utf-8")):
            rows.append({"matchId": m["wyId"], "dateutc": m["dateutc"], "competition": league})
    df = pd.DataFrame(rows)
    df["dateutc"] = pd.to_datetime(df["dateutc"])
    return df


def split_matches(matches: pd.DataFrame, fractions: dict[str, float]) -> pd.DataFrame:
    """Assign each match to "train", "validation" or "test" by kick-off date.

    Matches are sorted by (dateutc, matchId): the oldest `fractions["train"]` go to train,
    the next `fractions["validation"]` to validation, the rest to test. A cut that falls
    inside a group of matches with the same kick-off time is moved after that group, so
    every validation date is strictly later than every train date, and every test date
    strictly later than every validation date.

    Returns a copy sorted by date, with a "split" column.
    """
    if matches["matchId"].duplicated().any():
        raise ValueError("matchId must be unique: one row per match")
    df = matches.sort_values(["dateutc", "matchId"]).reset_index(drop=True)
    n = len(df)
    cuts = []
    for frac in (fractions["train"], fractions["train"] + fractions["validation"]):
        k = round(frac * n)
        while 0 < k < n and df.loc[k, "dateutc"] == df.loc[k - 1, "dateutc"]:
            k += 1
        cuts.append(k)
    df["split"] = np.select(
        [df.index < cuts[0], df.index < cuts[1]], ["train", "validation"], "test"
    )
    return df


def load_frozen_split(path: Path = FROZEN_SPLIT) -> pd.DataFrame:
    """Read the frozen split (matchId, dateutc, competition, split)."""
    return pd.read_csv(path, parse_dates=["dateutc"])
