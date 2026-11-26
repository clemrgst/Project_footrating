"""T2 (M3): compute the chronological split of the five leagues and freeze it in
configs/split_matches.csv.

    uv run python scripts/make_split.py

The file is frozen: if it already exists with a different content, the script stops
instead of overwriting it.
"""

from footrating.config import PROJECT_ROOT, load_config
from footrating.split import FROZEN_SPLIT, load_matches, split_matches


def main() -> None:
    config = load_config()
    matches = load_matches(PROJECT_ROOT / config["paths"]["raw"])
    split = split_matches(matches, config["split"])
    text = split.to_csv(index=False, lineterminator="\n", date_format="%Y-%m-%d %H:%M:%S")

    if FROZEN_SPLIT.exists():
        if FROZEN_SPLIT.read_text(encoding="utf-8") != text:
            raise SystemExit(f"{FROZEN_SPLIT.name} already exists and differs: it is frozen.")
        print(f"{FROZEN_SPLIT.name} unchanged")
    else:
        FROZEN_SPLIT.write_text(text, encoding="utf-8")
        print(f"{FROZEN_SPLIT.name} written")

    print(f"{len(split):,} matches")
    summary = split.groupby("split", sort=False).agg(
        matches=("matchId", "size"), first=("dateutc", "min"), last=("dateutc", "max")
    )
    summary["share"] = (summary["matches"] / len(split)).round(3)
    print(summary.to_string())
    print(
        split.pivot_table(
            index="competition", columns="split", values="matchId", aggfunc="size", fill_value=0
        )[["train", "validation", "test"]]
    )


if __name__ == "__main__":
    main()
