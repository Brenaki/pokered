"""Repository and build artifact discovery."""

from __future__ import annotations

from pathlib import Path
import os


REPO_ROOT = Path(__file__).resolve().parents[3]
CONTRACT_ROOT = REPO_ROOT / "rewrite" / "battle" / "contracts"


def artifact_paths(variant: str) -> tuple[Path, Path]:
    upper = variant.upper()
    rom = Path(os.environ.get(f"BATTLE_{upper}_ROM", REPO_ROOT / f"poke{variant}.gbc"))
    sym = Path(os.environ.get(f"BATTLE_{upper}_SYM", REPO_ROOT / f"poke{variant}.sym"))
    return rom, sym
