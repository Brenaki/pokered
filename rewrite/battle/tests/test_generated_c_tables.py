from __future__ import annotations

from battle_characterization.generate_c_tables import (
    COMBAT_OUTPUT,
    TRAINER_OUTPUT,
    combat_header,
    trainer_header,
)


def test_generated_combat_tables_match_rgbds_sources() -> None:
    assert COMBAT_OUTPUT.read_text(encoding="utf-8") == combat_header()


def test_generated_trainer_tables_match_rgbds_sources() -> None:
    assert TRAINER_OUTPUT.read_text(encoding="utf-8") == trainer_header()
