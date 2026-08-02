"""Run one production ASM routine with deterministic ports and observations."""

from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import Any

from .case import BattleCase, BattleResult, MemoryValue, Stub
from .symbols import Symbol, SymbolTable


REGISTER_NAMES = {"A", "F", "B", "C", "D", "E", "HL", "SP", "PC", "BC", "DE"}
START_HOOK = 0x0100
STACK_START = 0xDFFE
ROM0_RETURN_TRAP = 0x3FFF
ROMX_RETURN_TRAP = 0x7FFF


class AsmExecutionError(RuntimeError):
    """Raised when a characterization case cannot complete deterministically."""


class AsmRoutineRunner:
    def __init__(self, rom: Path, symbols: Path, variant: str) -> None:
        self.rom = rom
        self.symbol_path = symbols
        self.variant = variant
        self.symbols = SymbolTable.load(symbols)

    def run(self, case: BattleCase) -> BattleResult:
        try:
            from pyboy import PyBoy
        except ImportError as error:
            raise AsmExecutionError("PyBoy is required; run `uv sync --extra test`") from error

        pyboy = PyBoy(
            str(self.rom),
            symbols=str(self.symbol_path),
            window="null",
            no_input=True,
            sound_emulated=False,
            log_level="ERROR",
        )
        pyboy.set_emulation_speed(0)
        done = {"value": False}
        events: list[dict[str, Any]] = []
        rng_values = deque(case.rng)
        rng_consumed: list[int] = []
        frames = 0
        captured: dict[str, Any] = {}

        try:
            self._boot_cartridge(pyboy, case.max_frames)
            target, return_trap = self._initialize(pyboy, case)

            def finish(_: object) -> None:
                captured["registers"] = {
                    name: self._get_register(pyboy, name) for name in case.observe_registers
                }
                captured["memory"] = {
                    reference: self._read_reference(pyboy, reference) for reference in case.observe_memory
                }
                done["value"] = True
                pyboy.stop(save=False)

            pyboy.hook_register(return_trap.bank, return_trap.address, finish, None)

            if case.rng and case.rng_symbol != case.entry_symbol:
                self._register_rng_hook(pyboy, case.rng_symbol, rng_values, rng_consumed, events)

            for stub in case.stubs:
                self._register_stub(pyboy, stub, events)

            while not done["value"] and frames < case.max_frames:
                pyboy.tick(1, render=False, sound=False)
                frames += 1

            if not done["value"]:
                raise AsmExecutionError(
                    f"{case.id} did not return from {case.entry_symbol} within {case.max_frames} frames "
                    f"(PC=0x{pyboy.register_file.PC:04x}, SP=0x{pyboy.register_file.SP:04x})"
                )
            if rng_values:
                raise AsmExecutionError(f"{case.id} left {len(rng_values)} configured RNG bytes unused")

            return BattleResult(
                case_id=case.id,
                variant=self.variant,
                termination="returned",
                registers=captured["registers"],
                memory=captured["memory"],
                events=tuple(events),
                rng_consumed=tuple(rng_consumed),
                frames=frames,
            )
        finally:
            if not done["value"]:
                pyboy.stop(save=False)

    @staticmethod
    def _boot_cartridge(pyboy: Any, max_frames: int) -> None:
        reached_entry = {"value": False}

        def mark_entry(context: dict[str, bool]) -> None:
            context["value"] = True

        pyboy.hook_register(0, START_HOOK, mark_entry, reached_entry)
        frames = 0
        while not reached_entry["value"] and frames < max_frames:
            pyboy.tick(1, render=False, sound=False)
            frames += 1
        if not reached_entry["value"]:
            raise AsmExecutionError("cartridge did not finish the boot ROM within the frame budget")

    def _initialize(self, pyboy: Any, case: BattleCase) -> tuple[Symbol, Symbol]:
        target = self.symbols.resolve(case.entry_symbol)
        trap_address = ROMX_RETURN_TRAP if target.address >= 0x4000 else ROM0_RETURN_TRAP
        trap_bank = target.bank if target.address >= 0x4000 else 0
        return_trap = Symbol(trap_bank, trap_address, "characterization_return_trap")
        # Routine cases are not frame-loop tests. Mask hardware interrupts so
        # VBlank cannot preempt a synthetic call with an uninitialized stack.
        pyboy.memory[0xFFFF] = 0
        pyboy.memory[0xFF0F] = 0
        if 0x4000 <= target.address < 0x8000:
            pyboy.memory[0x2000] = target.bank
            loaded_bank = self.symbols.resolve("hLoadedROMBank")
            pyboy.memory[loaded_bank.address] = target.bank
        for item in case.memory:
            self._write_memory_value(pyboy, item)
        for name, value in case.registers.items():
            self._set_register(pyboy, name, value)
        pyboy.memory[STACK_START] = return_trap.address & 0xFF
        pyboy.memory[STACK_START + 1] = return_trap.address >> 8
        pyboy.register_file.SP = STACK_START
        pyboy.register_file.PC = target.address
        return target, return_trap

    def _register_rng_hook(
        self,
        pyboy: Any,
        symbol_name: str,
        values: deque[int],
        consumed: list[int],
        events: list[dict[str, Any]],
    ) -> None:
        symbol = self.symbols.resolve(symbol_name)

        def provide(_: object) -> None:
            if not values:
                raise AsmExecutionError(f"unexpected call to {symbol_name}; RNG fixture exhausted")
            value = values.popleft()
            consumed.append(value)
            pyboy.register_file.A = value
            events.append({"type": "rng", "source": symbol_name, "value": value})
            self._emulate_return(pyboy)

        pyboy.hook_register(symbol.bank, symbol.address, provide, None)

    def _register_stub(self, pyboy: Any, stub: Stub, events: list[dict[str, Any]]) -> None:
        symbol = self.symbols.resolve(stub.symbol)

        def invoke(_: object) -> None:
            for item in stub.memory:
                self._write_memory_value(pyboy, item)
            for name, value in stub.registers.items():
                self._set_register(pyboy, name, value)
            if stub.event:
                events.append({"type": "stub", "name": stub.event, "symbol": stub.symbol})
            self._emulate_return(pyboy)

        pyboy.hook_register(symbol.bank, symbol.address, invoke, None)

    @staticmethod
    def _emulate_return(pyboy: Any) -> None:
        sp = pyboy.register_file.SP
        low = pyboy.memory[sp]
        high = pyboy.memory[(sp + 1) & 0xFFFF]
        pyboy.register_file.SP = (sp + 2) & 0xFFFF
        pyboy.register_file.PC = low | (high << 8)

    def _write_memory_value(self, pyboy: Any, item: MemoryValue) -> None:
        symbol = self.symbols.resolve(item.symbol)
        for offset, value in enumerate(item.value):
            pyboy.memory[(symbol.address + offset) & 0xFFFF] = value

    def _read_reference(self, pyboy: Any, reference: str) -> list[int]:
        if ":" in reference:
            symbol_name, raw_length = reference.rsplit(":", 1)
            length = int(raw_length, 0)
        else:
            symbol_name = reference
            length = 1
        symbol = self.symbols.resolve(symbol_name)
        return [pyboy.memory[(symbol.address + offset) & 0xFFFF] for offset in range(length)]

    @staticmethod
    def _set_register(pyboy: Any, name: str, value: int) -> None:
        normalized = name.upper()
        if normalized not in REGISTER_NAMES:
            raise AsmExecutionError(f"unsupported register: {name}")
        if normalized == "BC":
            pyboy.register_file.B = (value >> 8) & 0xFF
            pyboy.register_file.C = value & 0xFF
        elif normalized == "DE":
            pyboy.register_file.D = (value >> 8) & 0xFF
            pyboy.register_file.E = value & 0xFF
        else:
            setattr(pyboy.register_file, normalized, value)

    @staticmethod
    def _get_register(pyboy: Any, name: str) -> int:
        normalized = name.upper()
        if normalized == "BC":
            return (pyboy.register_file.B << 8) | pyboy.register_file.C
        if normalized == "DE":
            return (pyboy.register_file.D << 8) | pyboy.register_file.E
        if normalized not in REGISTER_NAMES:
            raise AsmExecutionError(f"unsupported register: {name}")
        return int(getattr(pyboy.register_file, normalized))
