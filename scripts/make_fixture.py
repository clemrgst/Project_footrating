"""Write the small SYNTHETIC player-match sample used by the smoke test.

The values are random, not real Wyscout or PlayeRank data. They only mimic the
shape of the future table (one row per matchId, playerId). Run once:

    uv run python scripts/make_fixture.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "sample_player_match.csv"


def main(seed: int = 42) -> None:
    rng = np.random.default_rng(seed)
    rows = []
    positions = ["GK", "DEF", "MID", "FWD"]
    for m in range(6):
        for p in range(10):
            minutes = int(rng.integers(10, 91))
            passes = int(rng.poisson(minutes / 2))
            accurate = int(rng.binomial(passes, 0.8))
            shots = int(rng.poisson(1))
            rows.append(
                {
                    "matchId": 1000 + m,
                    "playerId": 100 * m + p,
                    "dateutc": f"2018-01-{m + 1:02d} 20:00:00",
                    "position": positions[p % 4],
                    "minutes": minutes,
                    "passes": passes,
                    "accurate_passes": accurate,
                    "shots": shots,
                    "playerankScore": round(
                        0.0004 * accurate + 0.003 * shots + rng.normal(0, 0.005), 6
                    ),
                }
            )
    pd.DataFrame(rows).to_csv(OUT, index=False)


if __name__ == "__main__":
    main()
