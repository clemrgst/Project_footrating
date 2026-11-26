"""Quarantine table built from a SYNTHETIC playerank.json sample (no real data, no network)."""

import json
from pathlib import Path

import pytest

from footrating.data.side_info import COLUMNS, KEYS, build_side_info

FIXTURE = Path(__file__).parent / "fixtures" / "playerank_sample.json"


def test_side_info_keys_are_unique():
    df = build_side_info(FIXTURE)
    assert list(df.columns) == COLUMNS
    assert len(df) == 6
    assert not df.duplicated(subset=KEYS).any()


def test_side_info_excludes_target_and_role():
    df = build_side_info(FIXTURE)
    assert "playerankScore" not in df.columns
    assert "roleCluster" not in df.columns


def test_duplicate_keys_raise(tmp_path):
    records = json.loads(FIXTURE.read_text(encoding="utf-8"))
    path = tmp_path / "playerank.json"
    path.write_text(json.dumps([*records, records[0]]), encoding="utf-8")
    with pytest.raises(ValueError, match="1 duplicate"):
        build_side_info(path)
