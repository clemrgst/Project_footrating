from footrating.config import get_seed, load_config


def test_seed_is_an_int():
    assert isinstance(get_seed(), int)


def test_split_fractions_sum_to_one():
    split = load_config()["split"]
    assert abs(split["train"] + split["validation"] + split["test"] - 1.0) < 1e-9
