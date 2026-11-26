"""Load the shared project configuration and the global random seed."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "configs" / "default.yaml"


def load_config(path: Path | str = DEFAULT_CONFIG) -> dict[str, Any]:
    """Read a YAML config file; relative paths are resolved from the project root."""
    path = Path(path)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_seed(config: dict[str, Any] | None = None) -> int:
    """Return the global random seed used everywhere in the project."""
    config = config if config is not None else load_config()
    return int(config["seed"])
