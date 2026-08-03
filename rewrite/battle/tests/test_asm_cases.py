from __future__ import annotations

from pathlib import Path

import pytest

from battle_characterization.contracts import load_cases
from battle_characterization.expected import assert_expected
from battle_characterization.paths import CONTRACT_ROOT


CASE_FILES = sorted((CONTRACT_ROOT / "cases").glob("*.json"))


def all_cases() -> list[tuple[Path, object]]:
    return [(path, case) for path in CASE_FILES for case in load_cases(path)]


@pytest.mark.asm
@pytest.mark.parametrize(("case_file", "case"), all_cases(), ids=lambda value: getattr(value, "id", None))
def test_production_asm_matches_reviewed_contract(asm_runner, case_file: Path, case) -> None:
    del case_file
    if asm_runner.variant not in case.variants:
        pytest.skip(f"case does not apply to {asm_runner.variant}")
    result = asm_runner.run(case)
    assert_expected(case, result)
