"""Command-line interface for executing and explicitly recording ASM cases."""

from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
import json
import sys

from .contracts import load_cases, validate_result
from .emulator import AsmRoutineRunner
from .paths import artifact_paths


def parser() -> ArgumentParser:
    result = ArgumentParser(prog="battle-asm")
    subcommands = result.add_subparsers(dest="command", required=True)
    for name in ("run", "record"):
        command = subcommands.add_parser(name)
        command.add_argument("case_file", type=Path)
        command.add_argument("--variant", choices=("red", "blue"), default="blue")
    return result


def execute(case_file: Path, variant: str) -> list[dict[str, object]]:
    rom, symbols = artifact_paths(variant)
    missing = [str(path) for path in (rom, symbols) if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing build artifacts: " + ", ".join(missing))
    runner = AsmRoutineRunner(rom, symbols, variant)
    results = []
    for case in load_cases(case_file):
        if variant not in case.variants:
            continue
        document = runner.run(case).to_dict()
        validate_result(document)
        results.append(document)
    return results


def main(argv: list[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    try:
        results = execute(arguments.case_file, arguments.variant)
    except Exception as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps({"protocol_version": 1, "results": results}, indent=2, sort_keys=True))
    if arguments.command == "record":
        print("record mode emits candidate results; review and apply them explicitly", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
