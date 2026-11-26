"""Build the Moodle archive Group_<XX>_DS_Project.zip (LAB 5, page 5).

Only files tracked by git are included (commit first), so data/, models and
secrets never enter the archive; data/README.md is kept. Usage:

    uv run python scripts/make_zip.py --group XX
"""

from __future__ import annotations

import argparse
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PREFIXES = ("data/", "models/", ".claude/", "docs/planning/", "docs/guide/")
EXCLUDED_NAMES = {".env"}


def list_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "--cached"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    files = sorted(set(out.splitlines()))
    return [
        f
        for f in files
        if (f == "data/README.md" or not f.startswith(EXCLUDED_PREFIXES))
        and Path(f).name not in EXCLUDED_NAMES
        and not f.endswith(".zip")
        and (ROOT / f).is_file()
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--group", required=True, help="Group number, e.g. 06")
    args = parser.parse_args()
    top = f"Group_{args.group}_DS_Project"
    target = ROOT / f"{top}.zip"
    files = list_files()
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(ROOT / f, f"{top}/{f}")
    print(f"Wrote {target.name} with {len(files)} files")


if __name__ == "__main__":
    main()
