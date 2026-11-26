"""Quarantine table: minutesPlayed and goalScored, published with the target in playerank.json.

Never joined to the feature table by default (report/project_specification.md, Section 6).
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

KEYS = ["matchId", "playerId"]
COLUMNS = [*KEYS, "minutesPlayed", "goalScored"]


def build_side_info(playerank_path: Path) -> pd.DataFrame:
    """Return the quarantine table; raise ValueError if (matchId, playerId) is not unique."""
    df = pd.DataFrame(json.loads(playerank_path.read_text(encoding="utf-8")))[COLUMNS]
    n_dup = int(df.duplicated(subset=KEYS).sum())
    print(f"duplicate (matchId, playerId) keys in {playerank_path.name}: {n_dup}")
    if n_dup:
        raise ValueError(f"{n_dup} duplicate (matchId, playerId) keys in {playerank_path}")
    return df


def write_side_info(playerank_path: Path, out_path: Path) -> pd.DataFrame:
    df = build_side_info(playerank_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)
    return df
