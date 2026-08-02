from __future__ import annotations

import pytest

from battle_characterization.case import BattleCase
from battle_characterization.inventory import constant_values, move_rows
from battle_characterization.paths import REPO_ROOT


BASELINE = "2b9f524537649e22d11bedaaee6eb81832fbbcb0"
MOVES = move_rows()
MOVE_IDS = constant_values(REPO_ROOT / "constants" / "move_constants.asm")
EFFECTS = constant_values(REPO_ROOT / "constants" / "move_effect_constants.asm")
TYPES = constant_values(REPO_ROOT / "constants" / "type_constants.asm")


def encoded_accuracy(percent: str) -> int:
    return int(percent) * 255 // 100


@pytest.mark.asm
@pytest.mark.parametrize("move", MOVES, ids=lambda move: move.name)
def test_each_move_row_is_read_from_the_production_rom(asm_runner, move) -> None:
    move_id = MOVE_IDS[move.name]
    expected = [
        move_id,
        EFFECTS[move.effect],
        int(move.power),
        TYPES[move.type],
        encoded_accuracy(move.accuracy),
        int(move.pp),
    ]
    case = BattleCase(
        id=f"MOVE_CATALOG_{move.name}",
        requirements=("BTL-MOV",),
        variants=("red", "blue"),
        entry_symbol="ReadMove",
        registers={"A": move_id},
        memory=(),
        observe_memory=("wEnemyMoveNum:6",),
        observe_registers=(),
        rng=(),
        rng_symbol="BattleRandom",
        stubs=(),
        max_frames=120,
        expected=None,
        provenance={"source": "data/moves/moves.asm:Moves", "baseline": BASELINE},
    )

    result = asm_runner.run(case)

    assert result.memory["wEnemyMoveNum:6"] == expected
