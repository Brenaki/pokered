"""Parser for RGBDS `.sym` files emitted by `rgblink`."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


SYMBOL_RE = re.compile(r"^([0-9A-Fa-f]{2}):([0-9A-Fa-f]{4})\s+([^\s;]+)")
REFERENCE_RE = re.compile(r"^([^+\-]+?)(?:([+\-])(.+))?$")


@dataclass(frozen=True)
class Symbol:
    bank: int
    address: int
    name: str


class SymbolTable:
    def __init__(self, symbols: dict[str, Symbol]) -> None:
        self._symbols = symbols

    @classmethod
    def load(cls, path: Path) -> "SymbolTable":
        symbols: dict[str, Symbol] = {}
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            match = SYMBOL_RE.match(line)
            if not match:
                continue
            bank, address, name = match.groups()
            symbol = Symbol(int(bank, 16), int(address, 16), name)
            previous = symbols.get(name)
            if previous is not None and previous != symbol:
                raise ValueError(f"duplicate symbol {name!r} at {path}:{line_number}")
            symbols[name] = symbol
        if not symbols:
            raise ValueError(f"no RGBDS symbols found in {path}")
        return cls(symbols)

    def resolve(self, reference: str) -> Symbol:
        match = REFERENCE_RE.match(reference.replace(" ", ""))
        if not match:
            raise KeyError(f"invalid symbol reference: {reference!r}")
        name, operator, raw_offset = match.groups()
        try:
            base = self._symbols[name]
        except KeyError as error:
            raise KeyError(f"symbol not found: {name}") from error
        offset = int(raw_offset, 0) if raw_offset else 0
        if operator == "-":
            offset = -offset
        return Symbol(base.bank, (base.address + offset) & 0xFFFF, reference)

    def __contains__(self, name: str) -> bool:
        return name in self._symbols

    def __len__(self) -> int:
        return len(self._symbols)
