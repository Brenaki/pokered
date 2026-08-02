"""Executable traceability matrix for the controlled battle documents."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import json

from .paths import CONTRACT_ROOT, REPO_ROOT


ALLOWED_METHODS = {"asm", "asm+structural", "structural", "isolated-hazard"}


def load_traceability() -> dict[str, Any]:
    return json.loads((CONTRACT_ROOT / "traceability.json").read_text(encoding="utf-8"))


def evidence_paths(matrix: dict[str, Any]) -> list[Path]:
    return [REPO_ROOT / path for group in matrix["groups"] for path in group["evidence"]]
