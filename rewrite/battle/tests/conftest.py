from __future__ import annotations

from pathlib import Path
import os
import subprocess

import pytest

from battle_characterization.emulator import AsmRoutineRunner
from battle_characterization.c_runner import CRoutineRunner
from battle_characterization.paths import REPO_ROOT, artifact_paths


def selected_variants() -> tuple[str, ...]:
    raw = os.environ.get("BATTLE_TEST_VARIANTS", "blue")
    variants = tuple(item.strip() for item in raw.split(",") if item.strip())
    invalid = set(variants) - {"red", "blue"}
    if invalid:
        raise pytest.UsageError(f"invalid BATTLE_TEST_VARIANTS: {sorted(invalid)}")
    return variants


@pytest.fixture(scope="session", params=selected_variants())
def asm_runner(request: pytest.FixtureRequest) -> AsmRoutineRunner:
    variant = str(request.param)
    rom, symbols = artifact_paths(variant)
    missing = [path for path in (rom, symbols) if not path.is_file()]
    if missing:
        pytest.fail(
            "missing ASM artifacts: " + ", ".join(str(path) for path in missing) +
            "; build with `make DEBUG=1 pokered.gbc pokeblue.gbc`"
        )
    return AsmRoutineRunner(rom, symbols, variant)


@pytest.fixture(scope="session", params=selected_variants())
def c_runner(request: pytest.FixtureRequest) -> CRoutineRunner:
    variant = str(request.param)
    battle_root = REPO_ROOT / "rewrite" / "battle"
    subprocess.run(["make", "shared"], cwd=battle_root, check=True)
    return CRoutineRunner(battle_root / "build" / "libpokered_battle.so", variant)
