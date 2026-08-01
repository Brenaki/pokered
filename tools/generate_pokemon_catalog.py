#!/usr/bin/env python3
"""Generate the controlled Pokemon Red/Blue species catalog from ASM data."""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs/002-2026-08-01-Informações_sobre_Pokemons.md"
SLOT_WEIGHTS = (51, 51, 39, 25, 25, 25, 13, 13, 11, 3)


@dataclass
class Evolution:
    method: str
    target: str
    level: int = 1
    item: str | None = None


@dataclass
class Species:
    number: int
    symbol: str
    name: str
    source: Path
    category: str = ""
    description: str = ""
    height_feet: int = 0
    height_inches: int = 0
    weight_tenths_lb: int = 0
    stats: tuple[int, int, int, int, int] = (0, 0, 0, 0, 0)
    types: tuple[str, str] = ("", "")
    catch_rate: int = 0
    base_exp: int = 0
    growth: str = ""
    initial_moves: list[str] = field(default_factory=list)
    level_moves: list[tuple[int, str]] = field(default_factory=list)
    tmhm_moves: list[str] = field(default_factory=list)
    evolutions: list[Evolution] = field(default_factory=list)
    evolves_from: list[tuple[str, Evolution]] = field(default_factory=list)


def read(path: str | Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def normalized(symbol: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", symbol.upper())


def title_words(value: str) -> str:
    return value.replace("_", " ").title()


def species_name(symbol: str) -> str:
    special = {
        "NIDORAN_F": "Nidoran♀",
        "NIDORAN_M": "Nidoran♂",
        "MR_MIME": "Mr. Mime",
        "FARFETCHD": "Farfetch'd",
    }
    return special.get(symbol, title_words(symbol))


def display_map_symbol(symbol: str) -> str:
    special = {
        "MT_MOON_1F": "Mt. Moon 1F",
        "MT_MOON_B1F": "Mt. Moon B1F",
        "MT_MOON_B2F": "Mt. Moon B2F",
    }
    if symbol in special:
        return special[symbol]
    words = symbol.split("_")
    result = []
    for word in words:
        if re.fullmatch(r"B?\d+F", word):
            result.append(word)
        elif word == "SS":
            result.append("S.S.")
        else:
            result.append(word.title())
    return " ".join(result).replace("Pokemon", "Pokémon")


def display_map_stem(stem: str) -> str:
    special = {
        "DiglettsCave": "Diglett's Cave",
        "MtMoon1F": "Mt. Moon 1F",
        "MtMoonB1F": "Mt. Moon B1F",
        "MtMoonB2F": "Mt. Moon B2F",
        "SeaRoutes": "Rotas 19 e 20",
    }
    if stem in special:
        return special[stem]
    value = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", stem)
    value = re.sub(r"(?<=[a-z])(?=\d+F?$)", " ", value)
    return value.replace("Pokemon", "Pokémon")


def format_number(value: float, decimals: int = 1) -> str:
    return f"{value:.{decimals}f}".replace(".", ",")


def current_commit() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def parse_roster() -> list[Species]:
    constants = read("constants/pokedex_constants.asm")
    symbols = re.findall(r"^\s*const DEX_([A-Z0-9_]+)\s+;", constants, re.MULTILINE)
    assert len(symbols) == 151, f"expected 151 Pokedex constants, got {len(symbols)}"

    includes = re.findall(
        r'^INCLUDE "(data/pokemon/base_stats/[^\"]+\.asm)"',
        read("data/pokemon/base_stats.asm"),
        re.MULTILINE,
    )
    includes.append("data/pokemon/base_stats/mew.asm")
    assert len(includes) == 151, f"expected 151 base-stat files, got {len(includes)}"

    result: list[Species] = []
    for number, (symbol, relative_path) in enumerate(zip(symbols, includes), start=1):
        path = ROOT / relative_path
        text = path.read_text(encoding="utf-8")
        dex_match = re.search(r"\bdb\s+DEX_([A-Z0-9_]+)\s*; pokedex id", text)
        assert dex_match and dex_match.group(1) == symbol, (
            f"Pokedex/base-stat order mismatch for {relative_path}: {symbol}"
        )

        stats_match = re.search(
            r"\bdb\s+(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\n"
            r"\s*;\s*hp\s+atk\s+def\s+spd\s+spc",
            text,
            re.IGNORECASE,
        )
        types_match = re.search(
            r"\bdb\s+([A-Z_]+)\s*,\s*([A-Z_]+)\s*; type", text
        )
        catch_match = re.search(r"\bdb\s+(\d+)\s*; catch rate", text)
        exp_match = re.search(r"\bdb\s+(\d+)\s*; base exp", text)
        initial_match = re.search(r"\bdb\s+([^\n;]+)\s*; level 1 learnset", text)
        growth_match = re.search(r"\bdb\s+(GROWTH_[A-Z_]+)\s*; growth rate", text)
        tmhm_match = re.search(r"\btmhm\s*(.*?)\n\s*; end", text, re.DOTALL)
        assert all(
            (
                stats_match,
                types_match,
                catch_match,
                exp_match,
                initial_match,
                growth_match,
                tmhm_match,
            )
        ), f"could not parse {relative_path}"

        initial = [
            move.strip()
            for move in initial_match.group(1).split(",")
            if move.strip() != "NO_MOVE"
        ]
        tmhm_raw = tmhm_match.group(1).replace("\\", " ")
        tmhm = [
            move.strip()
            for move in tmhm_raw.split(",")
            if move.strip() and move.strip() != "UNUSED"
        ]

        result.append(
            Species(
                number=number,
                symbol=symbol,
                name=species_name(symbol),
                source=Path(relative_path),
                stats=tuple(int(stats_match.group(i)) for i in range(1, 6)),
                types=(types_match.group(1), types_match.group(2)),
                catch_rate=int(catch_match.group(1)),
                base_exp=int(exp_match.group(1)),
                growth=growth_match.group(1),
                initial_moves=initial,
                tmhm_moves=tmhm,
            )
        )
    return result


def parse_move_names() -> tuple[dict[str, str], dict[str, str]]:
    constants_text = read("constants/move_constants.asm")
    constants_block = constants_text.split("DEF NUM_ATTACKS", 1)[0]
    constants = re.findall(r"^\s*const\s+([A-Z0-9_]+)\s+;", constants_block, re.MULTILINE)
    constants = [constant for constant in constants if constant != "NO_MOVE"]
    names = re.findall(r'^\s*li\s+"([^"]+)"', read("data/moves/names.asm"), re.MULTILINE)
    assert len(constants) == len(names) == 165, (
        f"move catalog mismatch: {len(constants)} constants, {len(names)} names"
    )
    move_names = {constant: name.title() for constant, name in zip(constants, names)}

    item_text = read("constants/item_constants.asm")
    teach_items: dict[str, str] = {}
    for index, move in enumerate(
        re.findall(r"^\s*add_tm\s+([A-Z0-9_]+)", item_text, re.MULTILINE), start=1
    ):
        teach_items[move] = f"TM{index:02d}"
    for index, move in enumerate(
        re.findall(r"^\s*add_hm\s+([A-Z0-9_]+)", item_text, re.MULTILINE), start=1
    ):
        teach_items[move] = f"HM{index:02d}"
    assert len(teach_items) == 55, f"expected 55 TM/HM mappings, got {len(teach_items)}"
    return move_names, teach_items


def parse_dex_entries(species: list[Species]) -> None:
    text = read("data/pokemon/dex_entries.asm")
    entries = {}
    pattern = re.compile(
        r"^([A-Za-z0-9]+)DexEntry:\s*\n"
        r"\s*db\s+\"([^\"]+)@\"\s*\n"
        r"\s*db\s+(\d+)\s*,\s*(\d+)\s*\n"
        r"\s*dw\s+(\d+)",
        re.MULTILINE,
    )
    for match in pattern.finditer(text):
        entries[normalized(match.group(1))] = (
            match.group(2),
            int(match.group(3)),
            int(match.group(4)),
            int(match.group(5)),
        )

    for mon in species:
        key = normalized(mon.symbol)
        assert key in entries, f"missing Pokedex entry for {mon.symbol}"
        mon.category, mon.height_feet, mon.height_inches, mon.weight_tenths_lb = entries[key]


def parse_dex_text(species: list[Species]) -> None:
    text = read("data/pokemon/dex_text.asm")
    matches = list(re.finditer(r"^_([A-Za-z0-9]+)DexEntry::\s*$", text, re.MULTILINE))
    entries = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.end() : end]
        fragments = re.findall(r'^\s*(?:text|next|page)\s+"([^"]*)"', block, re.MULTILINE)
        assert fragments, f"missing Pokedex text for {match.group(1)}"
        description = ""
        for fragment in fragments:
            if description.endswith("-"):
                description = description[:-1] + fragment
            else:
                description += (" " if description else "") + fragment
        entries[normalized(match.group(1))] = (
            description.replace("# BALL", "Poké Ball").replace("#MON", "Pokémon")
        )
    assert len(entries) == 151, f"expected 151 Pokedex texts, got {len(entries)}"
    for mon in species:
        key = normalized(mon.symbol)
        assert key in entries, f"missing Pokedex text for {mon.symbol}"
        mon.description = entries[key]


def parse_evolutions(species: list[Species]) -> None:
    text = read("data/pokemon/evos_moves.asm")
    species_by_key = {normalized(mon.symbol): mon for mon in species}
    matches = list(re.finditer(r"^([A-Za-z0-9]+)EvosMoves:\s*$", text, re.MULTILINE))
    blocks = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks[normalized(match.group(1))] = text[match.end() : end]

    for mon in species:
        block = blocks.get(normalized(mon.symbol))
        assert block is not None, f"missing evolution/move block for {mon.symbol}"
        evolution_text, learnset_text = block.split("; Learnset", 1)
        for line in evolution_text.splitlines():
            level_match = re.search(r"db\s+EVOLVE_LEVEL\s*,\s*(\d+)\s*,\s*([A-Z0-9_]+)", line)
            item_match = re.search(
                r"db\s+EVOLVE_ITEM\s*,\s*([A-Z0-9_]+)\s*,\s*(\d+)\s*,\s*([A-Z0-9_]+)",
                line,
            )
            trade_match = re.search(r"db\s+EVOLVE_TRADE\s*,\s*(\d+)\s*,\s*([A-Z0-9_]+)", line)
            if level_match:
                mon.evolutions.append(
                    Evolution("level", level_match.group(2), int(level_match.group(1)))
                )
            elif item_match:
                mon.evolutions.append(
                    Evolution(
                        "item", item_match.group(3), int(item_match.group(2)), item_match.group(1)
                    )
                )
            elif trade_match:
                mon.evolutions.append(
                    Evolution("trade", trade_match.group(2), int(trade_match.group(1)))
                )

        mon.level_moves = [
            (int(level), move)
            for level, move in re.findall(
                r"^\s*db\s+(\d+)\s*,\s*([A-Z0-9_]+)\s*$", learnset_text, re.MULTILINE
            )
        ]
        for evolution in mon.evolutions:
            assert normalized(evolution.target) in species_by_key, (
                f"unknown evolution target {evolution.target} for {mon.symbol}"
            )

    for mon in species:
        for evolution in mon.evolutions:
            species_by_key[normalized(evolution.target)].evolves_from.append((mon.symbol, evolution))


def preprocess_version(text: str, version: str) -> list[str]:
    active = True
    stack: list[tuple[bool, bool]] = []
    result = []
    for line in text.splitlines():
        match = re.match(r"\s*IF\s+DEF\((_RED|_BLUE)\)", line)
        if match:
            condition = match.group(1) == f"_{version.upper()}"
            stack.append((active, condition))
            active = active and condition
            continue
        if re.match(r"\s*ELSE\b", line):
            parent, condition = stack[-1]
            stack[-1] = (parent, not condition)
            active = parent and not condition
            continue
        if re.match(r"\s*ENDC\b", line):
            parent, _ = stack.pop()
            active = parent
            continue
        if active:
            result.append(line)
    assert not stack, "unbalanced IF/ENDC in versioned data"
    return result


def add_spawn(
    target: dict[str, list[str]], symbol: str, description: str
) -> None:
    if description not in target[symbol]:
        target[symbol].append(description)


def parse_wild_spawns(species: list[Species]) -> dict[str, dict[str, list[str]]]:
    valid = {mon.symbol for mon in species}
    result = {
        "red": defaultdict(list),
        "blue": defaultdict(list),
    }

    for version in ("red", "blue"):
        for path in sorted((ROOT / "data/wild/maps").glob("*.asm")):
            lines = preprocess_version(path.read_text(encoding="utf-8"), version)
            current_method = None
            current_rate = 0
            entries: list[tuple[int, str]] = []

            def finish_block() -> None:
                if current_rate == 0:
                    assert not entries, f"zero-rate table has entries in {path}"
                    return
                assert len(entries) == 10, (
                    f"expected 10 {current_method} slots in {path} ({version}), got {len(entries)}"
                )
                locations = (
                    ["Route 19", "Route 20"]
                    if path.stem == "SeaRoutes"
                    else [display_map_stem(path.stem)]
                )
                by_species: dict[str, dict[int, int]] = defaultdict(lambda: defaultdict(int))
                for slot, (level, symbol) in enumerate(entries):
                    assert symbol in valid, f"unknown wild species {symbol} in {path}"
                    by_species[symbol][level] += SLOT_WEIGHTS[slot]
                medium = "terrestre/caverna" if current_method == "grass" else "Surf"
                for location in locations:
                    for symbol, levels in by_species.items():
                        level_text = ", ".join(
                            f"Nv.{level} ({format_number(weight * 100 / 256)}%)"
                            for level, weight in sorted(levels.items())
                        )
                        add_spawn(
                            result[version],
                            symbol,
                            f"{location} - {medium}, limiar {current_rate}/256: {level_text}",
                        )

            for line in lines:
                start = re.search(r"def_(grass|water)_wildmons\s+(\d+)", line)
                if start:
                    current_method = start.group(1)
                    current_rate = int(start.group(2))
                    entries = []
                    continue
                if current_method and re.search(rf"end_{current_method}_wildmons", line):
                    finish_block()
                    current_method = None
                    current_rate = 0
                    entries = []
                    continue
                if current_method:
                    entry = re.search(r"^\s*db\s+(\d+)\s*,\s*([A-Z0-9_]+)", line)
                    if entry:
                        entries.append((int(entry.group(1)), entry.group(2)))

    # Static, catchable map objects encoded as species/level pairs.
    for path in sorted((ROOT / "data/maps/objects").glob("*.asm")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if "object_event" not in line:
                continue
            parts = [part.strip() for part in line.split(";", 1)[0].split(",")]
            if len(parts) < 2 or parts[-2] not in valid or not parts[-1].isdigit():
                continue
            symbol, level = parts[-2], int(parts[-1])
            description = f"{display_map_stem(path.stem)} - encontro estático capturável, Nv.{level}"
            for version in ("red", "blue"):
                add_spawn(result[version], symbol, description)

    for version in ("red", "blue"):
        add_spawn(result[version], "SNORLAX", "Route 12 - encontro estático capturável, Nv.30")
        add_spawn(result[version], "SNORLAX", "Route 16 - encontro estático capturável, Nv.30")

    add_fishing_spawns(result, valid)
    return result


def add_fishing_spawns(
    result: dict[str, dict[str, list[str]]], valid: set[str]
) -> None:
    common = {
        "MAGIKARP": "Old Rod - qualquer ponto de pesca válido, Nv.5; fisgada garantida",
        "GOLDEEN": "Good Rod - qualquer ponto de pesca válido, Nv.10; 25% por uso",
        "POLIWAG": "Good Rod - qualquer ponto de pesca válido, Nv.10; 25% por uso",
    }
    for version in ("red", "blue"):
        for symbol, description in common.items():
            add_spawn(result[version], symbol, description)

    text = read("data/wild/super_rod.asm")
    assignments: dict[str, list[str]] = defaultdict(list)
    for map_symbol, group in re.findall(
        r"^\s*dbw\s+([A-Z0-9_]+)\s*,\s*\.(Group\d+)", text, re.MULTILINE
    ):
        assignments[group].append(display_map_symbol(map_symbol))

    group_matches = list(re.finditer(r"^\.(Group\d+):\s*$", text, re.MULTILINE))
    for index, match in enumerate(group_matches):
        end = group_matches[index + 1].start() if index + 1 < len(group_matches) else len(text)
        block = text[match.end() : end]
        count_match = re.search(r"^\s*db\s+(\d+)\s*$", block, re.MULTILINE)
        assert count_match, f"missing Super Rod group size for {match.group(1)}"
        count = int(count_match.group(1))
        entries = re.findall(r"^\s*db\s+(\d+)\s*,\s*([A-Z0-9_]+)", block, re.MULTILINE)
        assert len(entries) == count, f"bad Super Rod group {match.group(1)}"
        chance = 50 / count
        maps = ", ".join(assignments[match.group(1)])
        for level, symbol in entries:
            assert symbol in valid, f"unknown fishing species {symbol}"
            description = (
                f"Super Rod - {maps}, Nv.{level}; {format_number(chance)}% por uso "
                "(50% sem fisgada)"
            )
            for version in ("red", "blue"):
                add_spawn(result[version], symbol, description)


def parse_special_acquisition(species: list[Species]) -> dict[str, dict[str, list[str]]]:
    result = {
        "red": defaultdict(list),
        "blue": defaultdict(list),
    }

    def add(versions: tuple[str, ...], symbol: str, description: str) -> None:
        for version in versions:
            add_spawn(result[version], symbol, description)

    both = ("red", "blue")
    for symbol in ("BULBASAUR", "CHARMANDER", "SQUIRTLE"):
        add(both, symbol, "Inicial no Oak's Lab, Nv.5; escolher apenas um dos três")
    add(both, "MAGIKARP", "Compra no Mt. Moon Pokécenter, Nv.5, por ₽500")
    add(both, "EEVEE", "Presente no Celadon Mansion Roof House, Nv.25")
    add(both, "LAPRAS", "Presente no Silph Co. 7F, Nv.15")
    add(both, "HITMONLEE", "Fighting Dojo, Nv.30; escolher Hitmonlee ou Hitmonchan")
    add(both, "HITMONCHAN", "Fighting Dojo, Nv.30; escolher Hitmonlee ou Hitmonchan")
    add(both, "OMANYTE", "Reviver Helix Fossil no Cinnabar Lab, Nv.30")
    add(both, "KABUTO", "Reviver Dome Fossil no Cinnabar Lab, Nv.30")
    add(both, "AERODACTYL", "Reviver Old Amber no Cinnabar Lab, Nv.30")
    add(both, "MEW", "Sem obtenção normal nesta ROM; exige distribuição/evento ou meio externo")

    red_prizes = (
        ("ABRA", 9, 180),
        ("CLEFAIRY", 8, 500),
        ("NIDORINA", 17, 1200),
        ("DRATINI", 18, 2800),
        ("SCYTHER", 25, 5500),
        ("PORYGON", 26, 9999),
    )
    blue_prizes = (
        ("ABRA", 6, 120),
        ("CLEFAIRY", 12, 750),
        ("NIDORINO", 17, 1200),
        ("PINSIR", 20, 2500),
        ("DRATINI", 24, 4600),
        ("PORYGON", 18, 6500),
    )
    for version, prizes in (("red", red_prizes), ("blue", blue_prizes)):
        for symbol, level, coins in prizes:
            add((version,), symbol, f"Celadon Game Corner Prize, Nv.{level}, por {coins} moedas")

    for symbol in ("SANDSHREW", "VULPIX", "MEOWTH", "BELLSPROUT", "MAGMAR", "PINSIR"):
        add(("red",), symbol, "Troca via link com uma partida de Pokémon Blue")
    for symbol in ("EKANS", "ODDISH", "MANKEY", "GROWLITHE", "SCYTHER", "ELECTABUZZ"):
        add(("blue",), symbol, "Troca via link com uma partida de Pokémon Red")

    valid = {mon.symbol for mon in species}
    trade_pattern = re.compile(
        r'^\s*npctrade\s+([A-Z0-9_]+)\s*,\s*([A-Z0-9_]+)\s*,[^\"]+\"([^\"]+)\"\s*;\s*(.+)$',
        re.MULTILINE,
    )
    for offered, received, nickname, comment in trade_pattern.findall(read("data/events/trades.asm")):
        if "unused" in comment.lower():
            continue
        assert offered in valid and received in valid
        location_match = re.search(r"used in\s+([A-Z0-9_]+)", comment)
        assert location_match, f"trade location missing: {comment}"
        location = display_map_symbol(location_match.group(1))
        add(
            both,
            received,
            f"Troca NPC em {location}: entregar {species_name(offered)}; "
            f"recebido no mesmo nível, apelido {nickname}",
        )
    return result


def stat_value(base: int, level: int, maximum: bool, hp: bool) -> int:
    dv = 15 if maximum else 0
    stat_exp_bonus = 63 if maximum else 0
    value = ((2 * (base + dv) + stat_exp_bonus) * level) // 100
    value += level + 10 if hp else 5
    return min(value, 999)


def capture_probability(catch_rate: int) -> float:
    # Normalized scenario: Poke Ball, no status, MaxHP=HP=100.
    hp_factor = ((100 * 255 // 12) // (100 // 4))
    second_test = (min(hp_factor, 255) + 1) / 256
    first_test_values = min(catch_rate + 1, 256)
    return first_test_values * second_test / 256 * 100


def capture_class(probability: float) -> str:
    if probability >= 30:
        return "muito favorável"
    if probability >= 20:
        return "favorável"
    if probability >= 10:
        return "intermediária"
    if probability >= 4:
        return "difícil"
    return "muito difícil"


def type_name(symbol: str) -> str:
    if symbol == "PSYCHIC_TYPE":
        return "Psychic"
    return title_words(symbol)


def growth_name(symbol: str) -> str:
    names = {
        "GROWTH_MEDIUM_FAST": "Medium Fast",
        "GROWTH_SLIGHTLY_FAST": "Slightly Fast",
        "GROWTH_SLIGHTLY_SLOW": "Slightly Slow",
        "GROWTH_MEDIUM_SLOW": "Medium Slow",
        "GROWTH_FAST": "Fast",
        "GROWTH_SLOW": "Slow",
    }
    return names[symbol]


def evolution_text(evolution: Evolution, species_by_key: dict[str, Species]) -> str:
    target = species_by_key[normalized(evolution.target)].name
    if evolution.method == "level":
        return f"{target} ao atingir Nv.{evolution.level} ou superior após ganho de nível"
    if evolution.method == "item":
        return f"{target} ao usar {title_words(evolution.item or '')}; nível mínimo {evolution.level}"
    return f"{target} por troca via link; nível mínimo {evolution.level}"


def source_list(paths: list[str]) -> str:
    return ", ".join(f"`{path}`" for path in paths)


def build_document(
    species: list[Species],
    move_names: dict[str, str],
    teach_items: dict[str, str],
    spawns: dict[str, dict[str, list[str]]],
    acquisitions: dict[str, dict[str, list[str]]],
) -> str:
    commit = current_commit()
    species_by_key = {normalized(mon.symbol): mon for mon in species}
    evolution_count = sum(len(mon.evolutions) for mon in species)
    species_with_evolution = sum(bool(mon.evolutions) for mon in species)
    red_wild = sum(bool(spawns["red"].get(mon.symbol)) for mon in species)
    blue_wild = sum(bool(spawns["blue"].get(mon.symbol)) for mon in species)

    lines = [
        "# Informações sobre os Pokémon de Pokémon Red/Blue",
        "",
        "## Controle do documento",
        "",
        "| Campo | Valor |",
        "|---|---|",
        "| Identificação | PKM-002 |",
        "| Arquivo | `002-2026-08-01-Informações_sobre_Pokemons.md` |",
        "| Revisão | 1.0 |",
        "| Data de emissão | 2026-08-01 |",
        "| Situação | Emitido para revisão e uso técnico interno |",
        "| Responsável pelo processo | Equipe de reescrita ASM para C |",
        "| Elaborado por | Gerador determinístico e verificação do código-fonte |",
        "| Aprovador | Pendente de designação |",
        f"| Baseline do código | commit `{commit}` |",
        "| Abrangência | 151 espécies válidas da Pokédex de Pokémon Red/Blue |",
        "| Classificação | Informação documentada interna |",
        "",
        "### Histórico de revisões",
        "",
        "| Revisão | Data | Alteração | Autor | Aprovação |",
        "|---|---|---|---|---|",
        "| 1.0 | 2026-08-01 | Emissão inicial do catálogo completo de espécies | Codex | Pendente |",
        "",
        "## 1. Finalidade e relação com a ISO 9001",
        "",
        "Este documento controla e torna rastreável o conhecimento sobre as espécies",
        "implementadas nesta ROM. Ele serve como fonte para análise do legado, contrato de",
        "compatibilidade da reescrita em C, entrada de testes e evidência de revisão.",
        "",
        "A organização adota abordagem de processo, pensamento baseado em risco, critérios",
        "de aceitação, rastreabilidade e controle de informação documentada inspirados na",
        "ISO 9001. Isso **não** declara certificação nem conformidade formal do software ou",
        "do repositório com a norma.",
        "",
        "Na data de emissão, a referência publicada é a",
        "[ISO 9001:2015/Amd 1:2024](https://www.iso.org/standard/88431.html). A sexta edição",
        "está em publicação, com [previsão da ISO para setembro de 2026](https://www.iso.org/standard/88464.html).",
        "O controle aplicado também considera a orientação oficial sobre",
        "[informação documentada](https://www.iso.org/files/live/sites/isoorg/files/archive/pdf/en/documented_information.pdf).",
        "",
        "## 2. Escopo",
        "",
        "### 2.1 Incluído",
        "",
        "- as 151 espécies numeradas por `DEX_BULBASAUR` a `DEX_MEW`;",
        "- nome, categoria, descrição da Pokédex, altura, peso, tipos, catch rate, EXP base e crescimento;",
        "- atributos base e resultados calculados nos níveis 0 e 99;",
        "- movimentos iniciais, movimentos por nível e compatibilidade TM/HM;",
        "- evolução direta, origem evolutiva e pré-requisitos;",
        "- encontros terrestres, em cavernas, por Surf, por pesca e estáticos;",
        "- diferenças de disponibilidade entre Red e Blue;",
        "- presentes, escolhas, fósseis, prêmios e trocas com NPC;",
        "- controles, riscos e testes necessários para a migração gradual para C.",
        "",
        "### 2.2 Excluído",
        "",
        "- índices `MISSINGNO.`, fósseis de exibição e o `RESTLESS_SOUL`;",
        "- equipes de treinadores, sprites, paletas e cries;",
        "- mecânicas inexistentes na Geração I, como abilities, natures, breeding, egg moves,",
        "  gênero mecânico e itens segurados;",
        "- dados de Pokémon Yellow ou gerações posteriores.",
        "",
        "## 3. Objetivos e critérios da qualidade",
        "",
        "| ID | Objetivo | Critério verificável |",
        "|---|---|---|",
        "| PKM-Q01 | Cobertura integral | Exatamente 151 espécies válidas, sem `MISSINGNO.`. |",
        "| PKM-Q02 | Fidelidade | Todo dado transcrito aponta para uma tabela ASM canônica. |",
        "| PKM-Q03 | Reprodutibilidade | O gerador produz o mesmo conteúdo para o mesmo commit. |",
        "| PKM-Q04 | Correção numérica | Fórmulas usam inteiros, pisos e limites iguais aos da ROM. |",
        "| PKM-Q05 | Distinção de versão | Encontros e prêmios Red/Blue não são fundidos indevidamente. |",
        "| PKM-Q06 | Manutenção | Alterações nas fontes exigem regeneração, testes e Graphify. |",
        "",
        "## 4. Fontes de verdade",
        "",
        "| Responsabilidade | Fonte |",
        "|---|---|",
        "| Ordem nacional e IDs | `constants/pokedex_constants.asm` |",
        "| Atributos, tipos, captura, EXP, golpes iniciais, crescimento e TM/HM | `data/pokemon/base_stats.asm`, `data/pokemon/base_stats/*.asm`, `data/pokemon/mew.asm` |",
        "| Altura, peso e categoria | `data/pokemon/dex_entries.asm` |",
        "| Descrição textual da Pokédex | `data/pokemon/dex_text.asm` |",
        "| Evoluções e golpes por nível | `data/pokemon/evos_moves.asm` |",
        "| Nomes de golpes | `constants/move_constants.asm`, `data/moves/names.asm` |",
        "| Numeração TM/HM | `constants/item_constants.asm`, `data/moves/tmhm_moves.asm` |",
        "| Encontros terrestres e Surf | `data/wild/grass_water.asm`, `data/wild/maps/*.asm` |",
        "| Probabilidade dos dez slots | `data/wild/probabilities.asm` |",
        "| Pesca | `engine/items/item_effects.asm`, `data/wild/good_rod.asm`, `data/wild/super_rod.asm` |",
        "| Encontros estáticos | `data/maps/objects/*.asm`, `scripts/Route12.asm`, `scripts/Route16.asm` |",
        "| Presentes, fósseis, prêmios e trocas | `scripts/OaksLab.asm`, `scripts/CeladonMansionRoofHouse.asm`, `scripts/SilphCo7F.asm`, `scripts/FightingDojo.asm`, `scripts/MtMoonPokecenter.asm`, `scripts/CinnabarLabFossilRoom.asm`, `data/events/prizes.asm`, `data/events/prize_mon_levels.asm`, `data/events/trades.asm` |",
        "| Cálculo de atributos | `home/move_mon.asm` (`CalcStats`, `CalcStat`) |",
        "| Evolução em execução | `engine/pokemon/evos_moves.asm` (`TryEvolvingMon`) |",
        "| Captura | `engine/items/item_effects.asm` (`ItemUseBall`) |",
        "",
        "## 5. Convenções e regras de interpretação",
        "",
        "As descrições da Pokédex permanecem em inglês, como armazenadas na ROM. O gerador",
        "une as linhas `text`/`next`/`page`, recompõe palavras hifenizadas apenas pela quebra",
        "de tela e expande o token de fonte `#` para \"Poké\".",
        "",
        "### 5.1 Atributos",
        "",
        "A Geração I possui cinco atributos armazenados: HP, Attack, Defense, Speed e Special.",
        "Não há Special Attack e Special Defense separados. `BST` neste documento é a soma",
        "dos cinco atributos base.",
        "",
        "Os atributos reais dependem do nível, DV e Stat Exp. Para tornar os valores de",
        "nível 99 verificáveis, cada célula apresenta a faixa **mínimo-máximo**:",
        "",
        "```text",
        "Min: DV=0 e Stat Exp=0",
        "Max: DV=15 e Stat Exp=65535; floor(ceil(sqrt(65535))/4)=63",
        "Não HP = floor(((2*(Base+DV)+BonusStatExp)*Nivel)/100)+5",
        "HP     = floor(((2*(Base+DV)+BonusStatExp)*Nivel)/100)+Nivel+10",
        "Resultado final limitado a 999",
        "```",
        "",
        "Nível 0 não é um nível normal de progressão (`MAX_LEVEL` é 100). Ele é incluído",
        "porque foi solicitado e representa a saída técnica da fórmula: HP=10 e os demais",
        "atributos=5 para toda espécie, independentemente de DV e Stat Exp. O catálogo usa",
        "nível 99, não 100, no segundo cenário.",
        "",
        "### 5.2 Captura e classificação",
        "",
        "`Catch rate` é o byte base da espécie. A chance efetiva também depende da Ball, HP",
        "atual/máximo, status e RNG. Para comparar espécies, a coluna de dificuldade usa um",
        "cenário normalizado: Poké Ball, sem status, HP=MaxHP=100. Nesse cenário, `W=85`,",
        "o segundo teste passa em `86/256` e:",
        "",
        "```text",
        "P = ((CatchRate + 1) / 256) * (86 / 256)",
        "```",
        "",
        "O primeiro fator é limitado a 256 resultados. As classes são critérios internos",
        "deste documento: muito difícil <4%; difícil <10%; intermediária <20%; favorável",
        "<30%; muito favorável >=30%. Para o algoritmo completo, usar",
        "`docs/001-2026-08-01-Sistema_de_Batalhas_Pokemon_Red_Blue.md`.",
        "",
        "### 5.3 Movimentos",
        "",
        "- **Iniciais:** até quatro bytes `BASE_MOVES`, descritos no fonte como learnset de nível 1.",
        "- **Por nível:** pares ordenados em `data/pokemon/evos_moves.asm`.",
        "- **TM/HM:** bits de compatibilidade; a ficha mostra número do item e nome do golpe.",
        "- Pokémon recebidos ou encontrados acima do nível 1 são montados pelo motor a partir",
        "  dessas tabelas e mantêm no máximo quatro movimentos.",
        "- Evolução preserva os golpes atuais. A nova espécie passa a usar seu próprio learnset",
        "  para níveis posteriores; não existe Move Reminder nesta ROM.",
        "",
        "### 5.4 Encontros",
        "",
        "Cada tabela terrestre/Surf tem um limiar de encontro e dez slots condicionais com",
        "pesos exatos `51, 51, 39, 25, 25, 25, 13, 13, 11, 3`, totalizando 256. A ficha",
        "agrega slots repetidos por espécie e nível. O percentual entre parênteses é a chance",
        "**condicional após ocorrer um encontro**; o limiar `N/256` é testado separadamente.",
        "",
        "Good Rod tem 50% de não fisgar e, quando fisga, escolhe Goldeen ou Poliwag igualmente:",
        "25% por uso para cada. Super Rod tem 50% de não fisgar e escolha uniforme dentro do",
        "grupo do mapa. Old Rod sempre produz Magikarp Nv.5 quando a pesca é permitida.",
        "",
        "### 5.5 Evolução e obtenção",
        "",
        "`EVOLVE_LEVEL` exige nível atual igual ou maior que o limiar durante a avaliação",
        "pós-batalha; `EVOLVE_ITEM` exige a pedra indicada e nível mínimo 1; `EVOLVE_TRADE`",
        "exige troca por link e nível mínimo 1. A rotina original contém o bug documentado",
        "em que encontros selvagens podem acionar evolução por pedra devido ao reuso de",
        "`wCurItem`; a reescrita deve preservá-lo somente em modo de compatibilidade.",
        "",
        "Trocas com NPC recebem o Pokémon no mesmo nível daquele entregue. Escolhas são",
        "mutuamente exclusivas quando indicado. Mew possui dados completos, mas não possui",
        "método normal de obtenção nesta ROM.",
        "",
        "## 6. Resumo de cobertura",
        "",
        "| Medida | Resultado |",
        "|---|---:|",
        f"| Espécies válidas | {len(species)} |",
        f"| Movimentos nomeados | {len(move_names)} |",
        f"| Compatibilidades TM/HM possíveis | {len(teach_items)} itens |",
        f"| Entradas diretas de evolução | {evolution_count} |",
        f"| Espécies com evolução direta | {species_with_evolution} |",
        f"| Espécies com algum encontro capturável em Red | {red_wild} |",
        f"| Espécies com algum encontro capturável em Blue | {blue_wild} |",
        "",
        "## 7. Catálogo controlado das 151 espécies",
        "",
        "As fichas seguem a ordem nacional. `Nenhum encontro` significa ausência nas tabelas",
        "aleatórias, pesca e encontros estáticos capturáveis; a espécie ainda pode ser obtida",
        "por evolução, presente, prêmio ou troca conforme as linhas seguintes.",
        "",
    ]

    def move_name(symbol: str) -> str:
        assert symbol in move_names, f"unknown move {symbol}"
        return move_names[symbol]

    for mon in species:
        hp, attack, defense, speed, special = mon.stats
        probability = capture_probability(mon.catch_rate)
        level_99 = []
        for index, (label, base) in enumerate(
            zip(("HP", "Atk", "Def", "Spd", "Spc"), mon.stats)
        ):
            minimum = stat_value(base, 99, False, index == 0)
            maximum = stat_value(base, 99, True, index == 0)
            level_99.append(f"{label} {minimum}-{maximum}")

        initial = ", ".join(move_name(move) for move in mon.initial_moves) or "Nenhum"
        level_moves = "; ".join(
            f"Nv.{level} {move_name(move)}" for level, move in mon.level_moves
        ) or "Nenhum"
        tmhm = "; ".join(
            f"{teach_items[move]} {move_name(move)}"
            for move in sorted(mon.tmhm_moves, key=lambda item: teach_items[item])
        ) or "Nenhum"
        evolutions = "; ".join(
            evolution_text(evolution, species_by_key) for evolution in mon.evolutions
        ) or "Não possui evolução direta nesta ROM"
        origins = "; ".join(
            f"{species_by_key[normalized(source)].name}: {evolution_text(evolution, species_by_key)}"
            for source, evolution in mon.evolves_from
        ) or "Não é resultado de evolução"

        red_spawns = "<br>".join(spawns["red"].get(mon.symbol, [])) or "Nenhum encontro"
        blue_spawns = "<br>".join(spawns["blue"].get(mon.symbol, [])) or "Nenhum encontro"
        red_acquisition = "<br>".join(acquisitions["red"].get(mon.symbol, [])) or "Nenhuma aquisição especial"
        blue_acquisition = "<br>".join(acquisitions["blue"].get(mon.symbol, [])) or "Nenhuma aquisição especial"

        type_values = [type_name(mon.types[0])]
        if mon.types[1] != mon.types[0]:
            type_values.append(type_name(mon.types[1]))
        height_inches = mon.height_feet * 12 + mon.height_inches
        height_m = height_inches * 0.0254
        weight_lb = mon.weight_tenths_lb / 10
        weight_kg = weight_lb * 0.45359237

        lines.extend(
            [
                f"### {mon.number:03d} {mon.name}",
                "",
                "| Campo | Valor |",
                "|---|---|",
                f"| Nome/espécie | {mon.name} (`DEX_{mon.symbol}`) |",
                f"| Categoria Pokédex | {mon.category.title()} |",
                f"| Descrição Pokédex | {mon.description} |",
                f"| Altura | {mon.height_feet}'{mon.height_inches:02d}\" ({format_number(height_m, 2)} m) |",
                f"| Peso | {format_number(weight_lb)} lb ({format_number(weight_kg)} kg) |",
                f"| Tipo | {' / '.join(type_values)} |",
                f"| Catch rate | {mon.catch_rate}; cenário normalizado: {format_number(probability, 2)}% ({capture_class(probability)}) |",
                f"| EXP base / crescimento | {mon.base_exp} / {growth_name(mon.growth)} |",
                f"| Atributos base | HP {hp}; Atk {attack}; Def {defense}; Spd {speed}; Spc {special}; BST {sum(mon.stats)} |",
                "| Atributos no Nv.0 técnico | HP 10; Atk 5; Def 5; Spd 5; Spc 5 |",
                f"| Atributos no Nv.99, mínimo-máximo | {'; '.join(level_99)} |",
                f"| Movimentos iniciais | {initial} |",
                f"| Movimentos aprendidos por nível | {level_moves} |",
                f"| Movimentos possíveis por TM/HM | {tmhm} |",
                f"| Evolução e pré-requisito | {evolutions} |",
                f"| Origem por evolução | {origins} |",
                f"| Spawns em Red | {red_spawns} |",
                f"| Spawns em Blue | {blue_spawns} |",
                f"| Aquisição especial em Red | {red_acquisition} |",
                f"| Aquisição especial em Blue | {blue_acquisition} |",
                f"| Fonte específica | `{mon.source.as_posix()}` |",
                "",
            ]
        )

    lines.extend(
        [
            "## 8. Controles de risco e não conformidades conhecidas",
            "",
            "| ID | Risco ou condição | Controle requerido na reescrita |",
            "|---|---|---|",
            "| PKM-R01 | Confundir índice interno com número da Pokédex. | Usar um tipo distinto para `PokemonIndex` e `PokedexNumber`; testar `IndexToPokedex`. |",
            "| PKM-R02 | Fundir dados Red e Blue. | Carregar `GameVersion` explicitamente e manter golden masters por versão. |",
            "| PKM-R03 | Tratar Special como dois atributos. | Modelo Gen I deve possuir um único `Special`. |",
            "| PKM-R04 | Calcular stats sem DV/Stat Exp ou com arredondamento real. | Reproduzir pisos intermediários e teto 999. |",
            "| PKM-R05 | Interpretar nível 0 como jogável. | Mantê-lo apenas como caso técnico de fronteira. |",
            "| PKM-R06 | Aplicar fórmula moderna de captura. | Usar o algoritmo de `ItemUseBall` e fixtures do documento de batalhas. |",
            "| PKM-R07 | Conceder todos os golpes listados ao mesmo tempo. | Limitar moveset ativo a quatro e separar catálogo de estado da instância. |",
            "| PKM-R08 | Ensinar TM/HM incompatível. | Validar o bitset de 55 posições da espécie. |",
            "| PKM-R08A | Interpretar o bit `UNUSED` de Mew como um 56º item ensinável. | Ignorar o bit de preenchimento na API de domínio e preservá-lo apenas na serialização compatível. |",
            "| PKM-R09 | Evoluir por pedra sem intenção. | Decidir e registrar modo compatível para o bug de `wCurItem`. |",
            "| PKM-R10 | Considerar Mew normalmente disponível. | Marcar obtenção externa como requisito, sem inventar spawn. |",
            "| PKM-R11 | Tratar chance de slot como chance total por passo. | Aplicar primeiro o limiar do mapa e depois o peso do slot. |",
            "| PKM-R12 | Omitir escolhas mutuamente exclusivas. | Modelar starter, Fighting Dojo e Dome/Helix como decisões persistentes. |",
            "",
            "## 9. Modelo de domínio para a reescrita em C",
            "",
            "### 9.1 Bounded contexts",
            "",
            "| Contexto | Responsabilidade |",
            "|---|---|",
            "| `SpeciesCatalog` | Dados imutáveis de espécie, tipos, base stats, crescimento e captura. |",
            "| `MoveLearning` | Golpes iniciais, por nível e compatibilidade TM/HM. |",
            "| `Evolution` | Regras, gatilhos, escolhas e resultado da transformação. |",
            "| `Encounter` | Tabelas por versão, método, mapa, slot e nível. |",
            "| `Acquisition` | Presentes, fósseis, prêmios e trocas NPC. |",
            "| `PokemonInstance` | Nível, DV, Stat Exp, EXP, HP, status e moveset atual. |",
            "",
            "### 9.2 SOLID e refatoração incremental",
            "",
            "- **SRP:** separar parser de dados, cálculo de stats, encontro, evolução e captura.",
            "- **OCP:** estratégias por `GameVersion` e método de encontro sem condicionais espalhadas.",
            "- **LSP:** implementações ASM-oracle e C devem obedecer aos mesmos contratos observáveis.",
            "- **ISP:** interfaces pequenas como `SpeciesRepository`, `StatCalculator` e `EncounterTable`.",
            "- **DIP:** serviços de domínio dependem dessas interfaces, não do layout binário da ROM.",
            "- Aplicar **Sprout Method/Class** e **Branch by Abstraction** para substituir uma regra",
            "  por vez, mantendo golden masters antes de cada mudança estrutural.",
            "",
            "## 10. Estratégia TDD e critérios de aceitação",
            "",
            "| ID | Teste | Resultado esperado |",
            "|---|---|---|",
            "| PKM-T001 | Carregar catálogo | 151 espécies únicas e números 1..151. |",
            "| PKM-T002 | Validar movimentos | Todo movimento referenciado pertence aos 165 IDs válidos. |",
            "| PKM-T003 | Validar TM/HM | Exatamente 55 posições e nenhuma compatibilidade fora do bitset. |",
            "| PKM-T004 | Validar evoluções | 72 entradas, alvos válidos e métodos/níveis preservados. |",
            "| PKM-T005 | Stats Nv.0 | Toda espécie resulta em HP 10 e demais atributos 5. |",
            "| PKM-T006 | Stats Nv.99 | Fixtures mínimas/máximas igualam `CalcStat`, inclusive teto 999. |",
            "| PKM-T007 | Slots selvagens | Cada tabela ativa tem 10 slots e soma de pesos 256. |",
            "| PKM-T008 | Versões | Exclusivos e níveis de prêmios correspondem a Red e Blue. |",
            "| PKM-T009 | Pesca | Old sempre Magikarp; Good e Super reproduzem chance de não fisgar. |",
            "| PKM-T010 | Captura por espécie | Catch rate carregado é idêntico ao cabeçalho base. |",
            "| PKM-T011 | Evolução por nível/item/troca | Limiares e pré-condições são exercitados nas bordas N-1/N. |",
            "| PKM-T012 | Golden master | Serialização C das 151 fichas é igual ao extrator ASM da mesma baseline. |",
            "",
            "Ciclo recomendado de Kent Beck: escrever primeiro um exemplo mínimo falho, fazê-lo",
            "passar com a menor implementação, refatorar sem alterar a saída e repetir por regra.",
            "",
            "## 11. Rastreabilidade de requisitos",
            "",
            "| Requisito | Evidência neste documento | Fonte principal | Testes |",
            "|---|---|---|---|",
            "| PKM-REQ-NOME | Nome e número | Seção 7 | `constants/pokedex_constants.asm` | PKM-T001 |",
            "| PKM-REQ-DIM | Categoria, descrição, altura e peso | Seção 7 | `data/pokemon/dex_entries.asm`, `data/pokemon/dex_text.asm` | PKM-T012 |",
            "| PKM-REQ-TIPO | Tipos | Seção 7 | `data/pokemon/base_stats/*.asm` | PKM-T012 |",
            "| PKM-REQ-MOVE | Movimentos aprendidos/possíveis | Seções 5.3 e 7 | `data/pokemon/evos_moves.asm`, bitset `tmhm` | PKM-T002/003 |",
            "| PKM-REQ-SPAWN | Local, nível, versão e chance | Seções 5.4 e 7 | `data/wild/**`, objetos e pesca | PKM-T007/008/009 |",
            "| PKM-REQ-CATCH | Dificuldade de captura | Seções 5.2 e 7 | `BASE_CATCH_RATE`, `ItemUseBall` | PKM-T010 |",
            "| PKM-REQ-EVO | Evolução e pré-requisitos | Seções 5.5 e 7 | `data/pokemon/evos_moves.asm` | PKM-T004/011 |",
            "| PKM-REQ-STAT | Base, nível 0 e nível 99 | Seções 5.1 e 7 | `CalcStat` | PKM-T005/006 |",
            "| PKM-REQ-ACQ | Presentes, prêmios e trocas | Seção 7 | scripts e `data/events/*` | PKM-T008/012 |",
            "",
            "## 12. Manutenção, aprovação e Graphify",
            "",
            "### 12.1 Regeneração",
            "",
            "```bash",
            "python3 tools/generate_pokemon_catalog.py",
            "python3 tools/graphify_rgbds.py .",
            "$(cat graphify-out/.graphify_python) -m graphify export html",
            "```",
            "",
            "Toda alteração nas fontes da Seção 4 exige: regenerar este arquivo, revisar o diff,",
            "executar as validações, atualizar `graphify-out/graph.json` e `graphify-out/graph.html`",
            "e registrar nova linha no histórico de revisão.",
            "",
            "### 12.2 Checklist de aprovação",
            "",
            "- [x] 151 espécies válidas presentes.",
            "- [x] Dados Red e Blue processados separadamente.",
            "- [x] Descrição, altura, peso, tipos, captura, stats, golpes e evolução rastreados.",
            "- [x] Encontros terrestres, Surf, pesca e estáticos contemplados.",
            "- [x] Aquisições especiais e indisponibilidade normal de Mew registradas.",
            "- [x] Fórmulas e pressupostos dos níveis 0 e 99 declarados.",
            "- [ ] Revisão técnica independente concluída.",
            "- [ ] Aprovador e data de aprovação registrados.",
            "",
            "## 13. Referências",
            "",
            "- Código-fonte desta baseline, conforme fontes da Seção 4.",
            "- `docs/001-2026-08-01-Sistema_de_Batalhas_Pokemon_Red_Blue.md`.",
            "- [ISO 9001:2015/Amd 1:2024](https://www.iso.org/standard/88431.html).",
            "- [ISO 9001 em publicação](https://www.iso.org/standard/88464.html).",
            "- [ISO: Guidance on documented information](https://www.iso.org/files/live/sites/isoorg/files/archive/pdf/en/documented_information.pdf).",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    output = args.output if args.output.is_absolute() else ROOT / args.output
    species = parse_roster()
    move_names, teach_items = parse_move_names()
    parse_dex_entries(species)
    parse_dex_text(species)
    parse_evolutions(species)
    spawns = parse_wild_spawns(species)
    acquisitions = parse_special_acquisition(species)

    for mon in species:
        for move in mon.initial_moves:
            assert move in move_names, f"unknown initial move {move} for {mon.symbol}"
        for _, move in mon.level_moves:
            assert move in move_names, f"unknown level move {move} for {mon.symbol}"
        for move in mon.tmhm_moves:
            assert move in teach_items, f"unknown TM/HM {move} for {mon.symbol}"

    document = build_document(
        species, move_names, teach_items, spawns, acquisitions
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")
    print(f"Generated {output.relative_to(ROOT)}")
    print(f"Species: {len(species)}; lines: {document.count(chr(10)) + 1}; words: {len(document.split())}")


if __name__ == "__main__":
    main()
