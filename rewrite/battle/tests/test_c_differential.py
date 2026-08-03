from __future__ import annotations

from pathlib import Path

import pytest

from battle_characterization.c_runner import CRoutineRunner
from battle_characterization.contracts import load_cases
from battle_characterization.expected import assert_expected
from battle_characterization.paths import CONTRACT_ROOT


CASE_FILES = sorted((CONTRACT_ROOT / "cases").glob("*.json"))


def supported_cases() -> list[tuple[Path, object]]:
    return [
        (path, case)
        for path in CASE_FILES
        for case in load_cases(path)
        if case.entry_symbol in CRoutineRunner.SUPPORTED_ENTRIES
    ]


@pytest.mark.parametrize(
    ("case_file", "case"), supported_cases(), ids=lambda value: getattr(value, "id", None)
)
def test_c_matches_reviewed_asm_contract(c_runner, case_file: Path, case) -> None:
    del case_file
    if c_runner.variant not in case.variants:
        pytest.skip(f"case does not apply to {c_runner.variant}")
    assert_expected(case, c_runner.run(case))


def test_differential_scope_includes_combat_math_and_trainer_ai() -> None:
    ids = {case.id for _, case in supported_cases()}
    required = {
        "T_ACC_002_MAXIMUM_ACCURACY_CAN_MISS",
        "T_CRT_002_FOCUS_ENERGY_REDUCES_CRITICAL_RATE",
        "T_DMG_001_NEUTRAL_DAMAGE",
        "T_TYP_002_DUAL_WEAKNESS_MULTIPLIES_TWICE",
        "AI_T05_DUAL_TYPE_USES_FIRST_TABLE_MATCH",
        "AI_T10_AGATHA_ROLL_128_DOES_NOT_ACT",
    }
    assert required <= ids
