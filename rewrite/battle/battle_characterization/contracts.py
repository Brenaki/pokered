"""Load and validate the versioned case/result protocol."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import json

from jsonschema import Draft202012Validator

from .case import BattleCase
from .paths import CONTRACT_ROOT


def schema(name: str) -> dict[str, Any]:
    return json.loads((CONTRACT_ROOT / "schema" / name).read_text(encoding="utf-8"))


def load_case_document(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator(schema("case.schema.json")).validate(document)
    return document


def load_cases(path: Path) -> list[BattleCase]:
    document = load_case_document(path)
    return [BattleCase.from_dict(item) for item in document["cases"]]


def validate_result(result: dict[str, Any]) -> None:
    Draft202012Validator(schema("result.schema.json")).validate(result)
