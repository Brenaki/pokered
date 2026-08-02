from __future__ import annotations

from battle_characterization.inventory import (
    constant_values,
    effect_pointers,
    move_rows,
    trainer_ai_pointer_rows,
    trainer_move_choice_rows,
    type_rows,
)
from battle_characterization.paths import REPO_ROOT


def test_all_165_moves_match_the_move_constant_order() -> None:
    moves = move_rows()
    constants = constant_values(REPO_ROOT / "constants" / "move_constants.asm")
    ordered = [
        name
        for name, value in sorted(constants.items(), key=lambda item: item[1])
        if 1 <= value <= 165
    ]
    assert len(moves) == 165
    assert [move.name for move in moves] == ordered
    assert all(0 <= int(move.pp) <= 40 for move in moves)


def test_every_move_effect_has_a_valid_dispatch_contract() -> None:
    moves = move_rows()
    effects = constant_values(REPO_ROOT / "constants" / "move_effect_constants.asm")
    pointers = effect_pointers()
    assert effects["DISABLE_EFFECT"] == 0x56
    assert len(pointers) == 0x56
    assert all(move.effect in effects for move in moves)
    assert all(0 <= effects[move.effect] <= len(pointers) for move in moves)

    asm_labels = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (REPO_ROOT / "engine" / "battle").rglob("*.asm")
    )
    assert all(pointer == "NULL" or f"{pointer}:" in asm_labels for pointer in set(pointers))


def test_type_matchups_are_complete_and_use_only_gen1_factors() -> None:
    rows = type_rows()
    assert len(rows) == 82
    assert len(rows) == len(set(rows))
    assert {factor for _, _, factor in rows} == {"SUPER_EFFECTIVE", "NOT_VERY_EFFECTIVE", "NO_EFFECT"}
    assert ("GHOST", "PSYCHIC_TYPE", "NO_EFFECT") in rows


def test_every_trainer_class_has_move_layers_and_an_action_policy() -> None:
    choices = trainer_move_choice_rows()
    pointers = trainer_ai_pointer_rows()
    assert len(choices) == 47
    assert len(pointers) == 47
    assert all(set(layers) <= {1, 2, 3, 4} for layers in choices)
    assert all(1 <= limit <= 5 for limit, _ in pointers)
    assert pointers[31] == (1, "CooltrainerFAI")
    assert pointers[45] == (2, "AgathaAI")


def test_trainer_battle_ai_is_table_driven_and_not_a_perceptron() -> None:
    sources = "\n".join(
        (REPO_ROOT / path).read_text(encoding="utf-8")
        for path in (
            "engine/battle/trainer_ai.asm",
            "data/trainers/move_choices.asm",
            "data/trainers/ai_pointers.asm",
        )
    ).lower()
    assert "trainerclassmovechoicemodifications:" in sources
    assert "traineraipointers:" in sources
    assert "perceptron" not in sources
    assert "neural" not in sources


def test_non_link_enemy_move_execution_has_no_pp_decrement() -> None:
    core = (REPO_ROOT / "engine" / "battle" / "core.asm").read_text(encoding="utf-8")
    enemy_execution = core.split("ExecuteEnemyMove:", 1)[1].split("ExecuteEnemyMoveDone:", 1)[0]
    player_execution = core.split("ExecutePlayerMove:", 1)[1].split("ExecutePlayerMoveDone:", 1)[0]
    assert "DecrementPP" not in enemy_execution
    assert "DecrementPP" in player_execution


def test_end_of_battle_and_residual_faint_paths_remain_explicit() -> None:
    core = (REPO_ROOT / "engine" / "battle" / "core.asm").read_text(encoding="utf-8")
    end = (REPO_ROOT / "engine" / "battle" / "end_of_battle.asm").read_text(encoding="utf-8")
    assert "call HandlePoisonBurnLeechSeed" in core
    assert "jp z, HandleEnemyMonFainted" in core
    assert "jp z, HandlePlayerMonFainted" in core
    assert "EndOfBattle:" in end
    assert "wBattleResult" in end


def test_isolated_compatibility_hazards_remain_locatable() -> None:
    core = (REPO_ROOT / "engine" / "battle" / "core.asm").read_text(encoding="utf-8")
    items = (REPO_ROOT / "engine" / "items" / "item_effects.asm").read_text(encoding="utf-8")
    substitute = (REPO_ROOT / "engine" / "battle" / "move_effects" / "substitute.asm").read_text(encoding="utf-8")
    assert "defensive stat can actually end up as 0" in core
    counter = core.split("HandleCounterMove:", 1)[1].split("GetDamageVarsForPlayerAttack:", 1)[0]
    assert "wPlayerSelectedMove" in counter
    assert "wDamage" in counter
    assert "bug: since it only branches on carry" in substitute
    assert "wEnemyMonSpecies2" in items
    assert "wTransformedEnemyMonOriginalDVs" in items
