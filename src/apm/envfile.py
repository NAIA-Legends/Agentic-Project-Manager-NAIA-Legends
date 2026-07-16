"""Optional .env loading for local runs — real environment variables always win.

Looked up automatically by the CLI: <this repo>/.env first, then the project
root's .env. Values are applied with setdefault, never logged, never required
— CI keeps injecting real env vars and ignores all of this.
"""

from __future__ import annotations

import os
from pathlib import Path

from .config import REPO_ROOT


def load_env_files(*paths: str | Path) -> list[str]:
    """Apply KEY=VALUE lines from existing .env files; return the keys set.

    Lines starting with '#' and blank lines are skipped; surrounding single or
    double quotes on values are stripped. Existing env vars are never
    overridden (so a shell-exported value beats the file).
    """
    candidates = (
        [Path(p) for p in paths]
        if paths
        else [REPO_ROOT / ".env", REPO_ROOT.parent / ".env"]
    )
    applied: list[str] = []
    for path in candidates:
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'\"")
            if key and key not in os.environ:
                os.environ[key] = value
                applied.append(key)
    return applied
