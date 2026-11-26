"""Smoke test: a Ridge pipeline runs end to end on the synthetic fixture.

It checks the tooling, not model quality. The split is by match and chronological,
and the scaler and encoder are fitted on the training matches only.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from footrating.config import get_seed

FIXTURE = Path(__file__).parent / "fixtures" / "sample_player_match.csv"
NUMERIC = ["minutes", "passes", "accurate_passes", "shots"]


def test_ridge_pipeline_on_fixture():
    df = pd.read_csv(FIXTURE, parse_dates=["dateutc"])
    matches = df.drop_duplicates("matchId").sort_values("dateutc")["matchId"].tolist()
    train_ids, test_ids = matches[:4], matches[4:]
    train = df[df["matchId"].isin(train_ids)]
    test = df[df["matchId"].isin(test_ids)]
    assert set(train["matchId"]).isdisjoint(test["matchId"])
    assert train["dateutc"].max() < test["dateutc"].min()

    model = Pipeline(
        [
            (
                "prep",
                ColumnTransformer(
                    [
                        ("num", StandardScaler(), NUMERIC),
                        ("pos", OneHotEncoder(handle_unknown="ignore"), ["position"]),
                    ]
                ),
            ),
            ("ridge", Ridge(alpha=1.0, random_state=get_seed())),
        ]
    )
    model.fit(train, train["playerankScore"])
    pred = model.predict(test)
    assert pred.shape == (len(test),)
    assert np.isfinite(pred).all()
