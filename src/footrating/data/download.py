"""Download the raw Wyscout and PlayeRank files from figshare into data/raw/.

URLs, sizes and MD5 checksums were read from the figshare API
(https://api.figshare.com/v2/articles/<id>/files) on 2026-11-26.
"""

from __future__ import annotations

import hashlib
import zipfile
from dataclasses import dataclass
from pathlib import Path

import requests


@dataclass(frozen=True)
class RawFile:
    name: str
    article_id: int
    url: str
    md5: str


RAW_FILES = [
    RawFile("events.zip", 7770599, "https://ndownloader.figshare.com/files/14464685",
            "7c20e8647e7eda58d7838a0c7b1ec6ab"),
    RawFile("matches.zip", 7770422, "https://ndownloader.figshare.com/files/14464622",
            "51d80beb17480919f69a53a0152c2d71"),
    RawFile("players.json", 7765196, "https://ndownloader.figshare.com/files/15073721",
            "f28ddf6326281efeda6488b2169f5609"),
    RawFile("teams.json", 7765310, "https://ndownloader.figshare.com/files/15073697",
            "1381ff9449f21105090729cf0e086b5b"),
    RawFile("competitions.json", 7765316, "https://ndownloader.figshare.com/files/15073685",
            "3dc210a4805dda5337b0ff9f7eaa407a"),
    RawFile("playerank.json", 9361148, "https://ndownloader.figshare.com/files/16972010",
            "dbb3671e04eb37f30ef4006986748812"),
]  # fmt: skip


def md5sum(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download_file(raw: RawFile, raw_dir: Path) -> bool:
    """Download one file unless it is already present with the right MD5.

    Returns True if the file was downloaded, False if it was skipped.
    """
    dest = raw_dir / raw.name
    if dest.exists() and md5sum(dest) == raw.md5:
        return False
    tmp = dest.with_suffix(dest.suffix + ".part")
    with requests.get(raw.url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with tmp.open("wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 20):
                f.write(chunk)
    if md5sum(tmp) != raw.md5:
        tmp.unlink()
        raise ValueError(f"MD5 mismatch for {raw.name}")
    tmp.replace(dest)
    return True


def extract_zip(zip_path: Path, raw_dir: Path) -> list[str]:
    """Extract the members of a zip that are not already in raw_dir; return their names."""
    extracted = []
    with zipfile.ZipFile(zip_path) as z:
        for member in z.namelist():
            if member.endswith("/") or (raw_dir / member).exists():
                continue
            z.extract(member, raw_dir)
            extracted.append(member)
    return extracted


def download_all(raw_dir: Path) -> None:
    raw_dir.mkdir(parents=True, exist_ok=True)
    for raw in RAW_FILES:
        status = "downloaded" if download_file(raw, raw_dir) else "skipped (already present)"
        print(f"{raw.name}: {status}")
        if raw.name.endswith(".zip"):
            new = extract_zip(raw_dir / raw.name, raw_dir)
            print(f"  extracted {len(new)} new file(s)")
