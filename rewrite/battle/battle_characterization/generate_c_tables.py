"""Generate typed C initializers from the authoritative RGBDS battle tables."""

from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
import re

from .inventory import (
    COMMENT_RE,
    constant_values,
    trainer_ai_pointer_rows,
    trainer_move_choice_rows,
    type_rows,
)
from .paths import REPO_ROOT


BATTLE_ROOT = REPO_ROOT / "rewrite" / "battle"
COMBAT_OUTPUT = BATTLE_ROOT / "src" / "gen1_combat_tables.generated.h"
TRAINER_OUTPUT = BATTLE_ROOT / "src" / "gen1_trainer_tables.generated.h"

MULTIPLIERS = {
    "SUPER_EFFECTIVE": 20,
    "NOT_VERY_EFFECTIVE": 5,
    "NO_EFFECT": 0,
}

POLICIES = {
    "GenericAI": "TRAINER_AI_POLICY_GENERIC",
    "JugglerAI": "TRAINER_AI_POLICY_JUGGLER",
    "BlackbeltAI": "TRAINER_AI_POLICY_BLACKBELT",
    "GiovanniAI": "TRAINER_AI_POLICY_GIOVANNI",
    "CooltrainerMAI": "TRAINER_AI_POLICY_COOLTRAINER_M",
    "CooltrainerFAI": "TRAINER_AI_POLICY_COOLTRAINER_F",
    "BrockAI": "TRAINER_AI_POLICY_BROCK",
    "MistyAI": "TRAINER_AI_POLICY_MISTY",
    "LtSurgeAI": "TRAINER_AI_POLICY_LT_SURGE",
    "ErikaAI": "TRAINER_AI_POLICY_ERIKA",
    "KogaAI": "TRAINER_AI_POLICY_KOGA",
    "BlaineAI": "TRAINER_AI_POLICY_BLAINE",
    "SabrinaAI": "TRAINER_AI_POLICY_SABRINA",
    "Rival2AI": "TRAINER_AI_POLICY_RIVAL2",
    "Rival3AI": "TRAINER_AI_POLICY_RIVAL3",
    "LoreleiAI": "TRAINER_AI_POLICY_LORELEI",
    "BrunoAI": "TRAINER_AI_POLICY_BRUNO",
    "AgathaAI": "TRAINER_AI_POLICY_AGATHA",
    "LanceAI": "TRAINER_AI_POLICY_LANCE",
}


def stat_ratios() -> list[tuple[int, int]]:
    source = REPO_ROOT / "data" / "battle" / "stat_modifiers.asm"
    ratios: list[tuple[int, int]] = []
    for raw_line in source.read_text(encoding="utf-8").splitlines():
        line = COMMENT_RE.sub("", raw_line)
        match = re.match(r"\s*db\s+(\d+)\s*,\s*(\d+)\s*$", line)
        if match:
            ratios.append((int(match.group(1)), int(match.group(2))))
    return ratios


def high_critical_moves() -> list[int]:
    source = REPO_ROOT / "data" / "battle" / "critical_hit_moves.asm"
    move_constants = constant_values(REPO_ROOT / "constants" / "move_constants.asm")
    moves: list[int] = []
    for raw_line in source.read_text(encoding="utf-8").splitlines():
        line = COMMENT_RE.sub("", raw_line).strip()
        match = re.match(r"db\s+([A-Z][A-Z0-9_]*)$", line)
        if match:
            moves.append(move_constants[match.group(1)])
    return moves


def combat_header() -> str:
    types = constant_values(REPO_ROOT / "constants" / "type_constants.asm")
    ratio_lines = "\n".join(f"    {{{a}, {b}}}," for a, b in stat_ratios())
    type_lines = "\n".join(
        f"    {{{types[attacker]}, {types[defender]}, {MULTIPLIERS[multiplier]}}},"
        for attacker, defender, multiplier in type_rows()
    )
    critical_lines = ", ".join(str(value) for value in high_critical_moves())
    return f"""/* Generated from RGBDS battle tables. Do not edit by hand. */
static const StatRatio STAT_RATIOS[] = {{
{ratio_lines}
}};

static const TypeEffect TYPE_EFFECTS[] = {{
{type_lines}
}};

static const uint8_t HIGH_CRITICAL_MOVES[] = {{{critical_lines}}};
"""


def trainer_header() -> str:
    layers = trainer_move_choice_rows()
    pointers = trainer_ai_pointer_rows()
    if len(layers) != len(pointers):
        raise ValueError("trainer move layers and policy tables have different lengths")
    rows = []
    for layer_values, (maximum_uses, handler) in zip(layers, pointers, strict=True):
        mask = sum(1 << (value - 1) for value in layer_values)
        rows.append(f"    {{{mask}, {POLICIES[handler]}, {maximum_uses}}},")
    return """/* Generated from RGBDS trainer tables. Do not edit by hand. */
static const TrainerClassPolicy TRAINER_CLASSES[GEN1_TRAINER_CLASS_COUNT] = {
""" + "\n".join(rows) + "\n};\n"


def update(path: Path, content: str, check: bool) -> bool:
    if check:
        return path.is_file() and path.read_text(encoding="utf-8") == content
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = (
        update(COMBAT_OUTPUT, combat_header(), args.check),
        update(TRAINER_OUTPUT, trainer_header(), args.check),
    )
    if not all(outputs):
        print("generated C battle tables are stale")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
