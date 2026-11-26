"""T1 (M1): download raw files, write the inventory into data/README.md, build the
quarantine table data/processed/playerank_side_info.parquet.

    uv run python scripts/download_raw_data.py            # everything
    uv run python scripts/download_raw_data.py --dry-run  # print the inventory, do not write README
"""

import argparse

from footrating.config import PROJECT_ROOT, load_config
from footrating.data.download import download_all
from footrating.data.inventory import (
    build_inventory,
    count_player_match,
    coverage_by_competition,
    render_inventory,
    write_inventory,
)
from footrating.data.side_info import write_side_info


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="do not write data/README.md")
    args = parser.parse_args()

    paths = load_config()["paths"]
    raw_dir = PROJECT_ROOT / paths["raw"]
    out = PROJECT_ROOT / paths["processed"] / "playerank_side_info.parquet"

    download_all(raw_dir)

    block = render_inventory(
        build_inventory(raw_dir),
        count_player_match(raw_dir / "playerank.json"),
        coverage_by_competition(raw_dir),
    )
    print(block)
    if not args.dry_run:
        write_inventory(PROJECT_ROOT / "data" / "README.md", block)
        print("inventory written to data/README.md")

    side = write_side_info(raw_dir / "playerank.json", out)
    print(f"{out.relative_to(PROJECT_ROOT)}: {len(side):,} rows, columns {list(side.columns)}")


if __name__ == "__main__":
    main()
