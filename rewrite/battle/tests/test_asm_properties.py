from __future__ import annotations

import pytest

from battle_characterization.case import BattleCase, MemoryValue, Stub


BASELINE = "2b9f524537649e22d11bedaaee6eb81832fbbcb0"


def memory(symbol: str, *values: int) -> MemoryValue:
    return MemoryValue(symbol, values)


@pytest.mark.asm
def test_sleep_counters_one_through_seven_decrement_before_action(asm_runner) -> None:
    for counter in range(1, 8):
        case = BattleCase(
            id=f"T_STA_SLEEP_COUNTER_{counter}",
            requirements=("T-STA-001",),
            variants=("red", "blue"),
            entry_symbol="CheckPlayerStatusConditions",
            registers={},
            memory=(memory("wBattleMonStatus", counter), memory("wPlayerUsedMove", 33)),
            observe_memory=("wBattleMonStatus", "wPlayerUsedMove"),
            observe_registers=("A",),
            rng=(),
            rng_symbol="BattleRandom",
            stubs=(Stub("PrintText"), Stub("PlayMoveAnimation")),
            max_frames=120,
            expected=None,
            provenance={"source": "engine/battle/core.asm:CheckPlayerStatusConditions", "baseline": BASELINE},
        )

        result = asm_runner.run(case)

        assert result.registers["A"] == 0
        assert result.memory["wBattleMonStatus"] == [counter - 1]
        assert result.memory["wPlayerUsedMove"] == [0]


@pytest.mark.asm
def test_section_17_7_capture_probability_is_71_of_151_rand1_values(asm_runner) -> None:
    captured = 0
    for rand1 in range(151):
        case = BattleCase(
            id=f"T_CAP_SECTION_17_7_RAND1_{rand1}",
            requirements=("T-CAP-001",),
            variants=("red", "blue"),
            entry_symbol="ItemUseBall.checkForAilments",
            registers={"B": rand1},
            memory=(
                memory("wCurItem", 2),
                memory("wEnemyMonStatus", 1),
                memory("wEnemyMonActualCatchRate", 45),
                memory("wEnemyMonHP", 0, 25),
                memory("wEnemyMonMaxHP", 0, 100),
            ),
            observe_memory=(),
            observe_registers=(),
            rng=(),
            rng_symbol="Random",
            stubs=(
                Stub("ItemUseBall.captured", event="captured"),
                Stub("ItemUseBall.failedToCapture", event="failed"),
            ),
            max_frames=120,
            expected=None,
            provenance={"source": "engine/items/item_effects.asm:ItemUseBall", "baseline": BASELINE},
        )

        result = asm_runner.run(case)
        captured += result.events[0]["name"] == "captured"

    assert captured == 71

