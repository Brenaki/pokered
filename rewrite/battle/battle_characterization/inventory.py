"""Deterministic parsers for battle data tables in the RGBDS sources."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from .paths import REPO_ROOT


COMMENT_RE = re.compile(r";.*$")
CONST_RE = re.compile(r"^\s*const\s+([A-Za-z_][A-Za-z0-9_]*)")
CONST_DEF_RE = re.compile(r"^\s*const_def(?:\s+([^,\s]+))?")
CONST_NEXT_RE = re.compile(r"^\s*const_next\s+([^,\s]+)")
CONST_SKIP_RE = re.compile(r"^\s*const_skip(?:\s+([^,\s]+))?")
MOVE_RE = re.compile(r"^\s*move\s+(.+)$")
POINTER_RE = re.compile(r"^\s*dw\s+([A-Za-z_.$][A-Za-z0-9_.$]*)")
TYPE_ROW_RE = re.compile(r"^\s*db\s+([^,]+),\s*([^,]+),\s*([^,;]+)")
CONTROLLED_ID_RE = re.compile(
    r"\b(?:T-[A-Z]{2,4}-\d{3}|AI-T\d{2}|NC-\d{2}|AI-R\d{2}|AI-REQ-\d{3}|BTL-[A-Z]{3})\b"
)


def _number(raw: str) -> int:
    value = raw.strip()
    if value.startswith("$"):
        return int(value[1:], 16)
    if value.startswith("%"):
        return int(value[1:], 2)
    return int(value, 0)


def constant_values(path: Path) -> dict[str, int]:
    values: dict[str, int] = {}
    current = 0
    increment = 1
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = COMMENT_RE.sub("", raw_line).strip()
        if not line:
            continue
        if match := CONST_DEF_RE.match(line):
            current = _number(match.group(1)) if match.group(1) else 0
            increment = 1
            continue
        if match := CONST_NEXT_RE.match(line):
            current = _number(match.group(1))
            continue
        if match := CONST_SKIP_RE.match(line):
            current += increment * (_number(match.group(1)) if match.group(1) else 1)
            continue
        if match := CONST_RE.match(line):
            values[match.group(1)] = current
            current += increment
    return values


@dataclass(frozen=True)
class MoveRow:
    name: str
    effect: str
    power: str
    type: str
    accuracy: str
    pp: str


def move_rows(path: Path | None = None) -> list[MoveRow]:
    source = path or REPO_ROOT / "data" / "moves" / "moves.asm"
    rows: list[MoveRow] = []
    for raw_line in source.read_text(encoding="utf-8").splitlines():
        line = COMMENT_RE.sub("", raw_line)
        match = MOVE_RE.match(line)
        if not match:
            continue
        fields = [field.strip() for field in match.group(1).split(",")]
        if len(fields) != 6:
            raise ValueError(f"invalid move row: {raw_line}")
        rows.append(MoveRow(*fields))
    return rows


def effect_pointers(path: Path | None = None) -> list[str]:
    source = path or REPO_ROOT / "data" / "moves" / "effects_pointers.asm"
    return [
        match.group(1)
        for line in source.read_text(encoding="utf-8").splitlines()
        if (match := POINTER_RE.match(COMMENT_RE.sub("", line)))
    ]


def type_rows(path: Path | None = None) -> list[tuple[str, str, str]]:
    source = path or REPO_ROOT / "data" / "types" / "type_matchups.asm"
    rows: list[tuple[str, str, str]] = []
    for line in source.read_text(encoding="utf-8").splitlines():
        if match := TYPE_ROW_RE.match(COMMENT_RE.sub("", line)):
            rows.append(tuple(field.strip() for field in match.groups()))
    return rows


def trainer_move_choice_rows(path: Path | None = None) -> list[tuple[int, ...]]:
    source = path or REPO_ROOT / "data" / "trainers" / "move_choices.asm"
    rows: list[tuple[int, ...]] = []
    in_table = False
    for raw_line in source.read_text(encoding="utf-8").splitlines():
        line = COMMENT_RE.sub("", raw_line).strip()
        if line == "TrainerClassMoveChoiceModifications:":
            in_table = True
            continue
        if in_table and line.startswith("assert "):
            break
        if in_table and line.startswith("move_choices"):
            raw = line.removeprefix("move_choices").strip()
            rows.append(tuple(int(value.strip()) for value in raw.split(",") if value.strip()))
    return rows


def trainer_ai_pointer_rows(path: Path | None = None) -> list[tuple[int, str]]:
    source = path or REPO_ROOT / "data" / "trainers" / "ai_pointers.asm"
    rows: list[tuple[int, str]] = []
    for raw_line in source.read_text(encoding="utf-8").splitlines():
        line = COMMENT_RE.sub("", raw_line).strip()
        match = re.match(r"dbw\s+(\d+)\s*,\s*([A-Za-z_][A-Za-z0-9_]*)", line)
        if match:
            rows.append((int(match.group(1)), match.group(2)))
    return rows


def controlled_ids() -> set[str]:
    documents = (
        REPO_ROOT / "docs" / "001-2026-08-01-Sistema_de_Batalhas_Pokemon_Red_Blue.md",
        REPO_ROOT / "docs" / "003-2026-08-01-Funcionamento-das-IAs-Pokemon.md",
    )
    return {
        match.group(0)
        for document in documents
        for match in CONTROLLED_ID_RE.finditer(document.read_text(encoding="utf-8"))
    }
