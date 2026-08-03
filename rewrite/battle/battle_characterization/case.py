"""Language-neutral case and result models for differential battle tests."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import json


def parse_int(value: int | str) -> int:
    if isinstance(value, int):
        return value
    return int(value, 0)


@dataclass(frozen=True)
class MemoryValue:
    symbol: str
    value: tuple[int, ...]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MemoryValue":
        raw = data["value"]
        values = raw if isinstance(raw, list) else [raw]
        return cls(data["symbol"], tuple(parse_int(value) for value in values))

    def to_dict(self) -> dict[str, Any]:
        value: int | list[int]
        value = self.value[0] if len(self.value) == 1 else list(self.value)
        return {"symbol": self.symbol, "value": value}


@dataclass(frozen=True)
class Stub:
    symbol: str
    registers: dict[str, int] = field(default_factory=dict)
    memory: tuple[MemoryValue, ...] = ()
    event: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Stub":
        return cls(
            symbol=data["symbol"],
            registers={key: parse_int(value) for key, value in data.get("registers", {}).items()},
            memory=tuple(MemoryValue.from_dict(item) for item in data.get("memory", [])),
            event=data.get("event"),
        )


@dataclass(frozen=True)
class BattleCase:
    id: str
    requirements: tuple[str, ...]
    variants: tuple[str, ...]
    entry_symbol: str
    registers: dict[str, int]
    memory: tuple[MemoryValue, ...]
    observe_memory: tuple[str, ...]
    observe_registers: tuple[str, ...]
    rng: tuple[int, ...]
    rng_symbol: str
    stubs: tuple[Stub, ...]
    max_frames: int
    expected: dict[str, Any] | None
    provenance: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BattleCase":
        initial = data.get("initial", {})
        observe = data.get("observe", {})
        return cls(
            id=data["id"],
            requirements=tuple(data["requirements"]),
            variants=tuple(data.get("variants", ["red", "blue"])),
            entry_symbol=data["entry_symbol"],
            registers={key: parse_int(value) for key, value in initial.get("registers", {}).items()},
            memory=tuple(MemoryValue.from_dict(item) for item in initial.get("memory", [])),
            observe_memory=tuple(observe.get("memory", [])),
            observe_registers=tuple(observe.get("registers", [])),
            rng=tuple(parse_int(value) for value in data.get("rng", [])),
            rng_symbol=data.get("rng_symbol", "BattleRandom"),
            stubs=tuple(Stub.from_dict(item) for item in data.get("stubs", [])),
            max_frames=int(data.get("max_frames", 120)),
            expected=data.get("expected"),
            provenance=data["provenance"],
        )


@dataclass(frozen=True)
class BattleResult:
    case_id: str
    variant: str
    termination: str
    registers: dict[str, int]
    memory: dict[str, list[int]]
    events: tuple[dict[str, Any], ...]
    rng_consumed: tuple[int, ...]
    frames: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "variant": self.variant,
            "termination": self.termination,
            "registers": self.registers,
            "memory": self.memory,
            "events": list(self.events),
            "rng_consumed": list(self.rng_consumed),
            "frames": self.frames,
        }


def load_case(path: Path) -> BattleCase:
    return BattleCase.from_dict(json.loads(path.read_text(encoding="utf-8")))
