"""Adapter from ASM-shaped characterization cases to the portable C domain API."""

from __future__ import annotations

from ctypes import (
    CFUNCTYPE,
    POINTER,
    Structure,
    byref,
    c_bool,
    c_int,
    c_uint8,
    c_uint16,
    c_void_p,
    cdll,
)
from pathlib import Path
from typing import Callable

from .case import BattleCase, BattleResult, MemoryValue, Stub
from .inventory import constant_values, move_rows
from .paths import REPO_ROOT, artifact_paths
from .symbols import SymbolTable


STATUS_OK = 0
GEN1_FIDELITY = 0


class RandomSource(Structure):
    pass


RandomCallback = CFUNCTYPE(c_bool, c_void_p, POINTER(c_uint8))
RandomSource._fields_ = [("next_u8", RandomCallback), ("context", c_void_p)]


class PokemonTypes(Structure):
    _fields_ = [("first", c_uint8), ("second", c_uint8)]


class DamageStatsInput(Structure):
    _fields_ = [
        ("current_attack", c_uint16),
        ("current_special", c_uint16),
        ("base_attack", c_uint16),
        ("base_special", c_uint16),
        ("current_defense", c_uint16),
        ("current_defender_special", c_uint16),
        ("base_defense", c_uint16),
        ("base_defender_special", c_uint16),
        ("move_power", c_uint8),
        ("move_type", c_uint8),
        ("level", c_uint8),
        ("critical", c_bool),
        ("reflect", c_bool),
        ("light_screen", c_bool),
    ]


class DamageStats(Structure):
    _fields_ = [
        ("attack", c_uint8),
        ("defense", c_uint8),
        ("power", c_uint8),
        ("level", c_uint8),
    ]


class BaseDamageInput(Structure):
    _fields_ = [
        ("attack", c_uint8),
        ("defense", c_uint8),
        ("power", c_uint8),
        ("level", c_uint8),
        ("move_effect", c_uint8),
        ("accumulated_damage", c_uint16),
    ]


class TypeDamageResult(Structure):
    _fields_ = [
        ("damage", c_uint16),
        ("damage_multipliers", c_uint8),
        ("stab", c_bool),
        ("immune_or_rounded_to_zero", c_bool),
    ]


class TrainerAiMove(Structure):
    _fields_ = [
        ("id", c_uint8),
        ("effect", c_uint8),
        ("power", c_uint8),
        ("type", c_uint8),
    ]


class TrainerAiMoveObservation(Structure):
    _fields_ = [
        ("moves", TrainerAiMove * 4),
        ("defender_types", PokemonTypes),
        ("defender_status", c_uint8),
        ("disabled_move_slot", c_uint8),
        ("layer2_encouragement", c_uint8),
        ("trainer_class", c_uint8),
    ]


class TrainerAiMoveScores(Structure):
    _fields_ = [("scores", c_uint8 * 4), ("candidates", c_uint8 * 4)]


class TrainerAiSpecialObservation(Structure):
    _fields_ = [
        ("mode", c_int),
        ("policy", c_int),
        ("random_roll", c_uint8),
        ("current_hp", c_uint16),
        ("max_hp", c_uint16),
        ("status", c_uint8),
        ("living_party_members", c_uint8),
    ]


class TrainerAiDecision(Structure):
    _fields_ = [
        ("action", c_int),
        ("move_slot", c_uint8),
        ("move_id", c_uint8),
        ("consumes_action_count", c_bool),
        ("remaining_action_count", c_uint8),
    ]


class SequenceRandom:
    def __init__(self, values: tuple[int, ...]) -> None:
        self.values = values
        self.consumed: list[int] = []

        @RandomCallback
        def next_u8(_context, output) -> bool:
            if len(self.consumed) >= len(self.values):
                return False
            value = self.values[len(self.consumed)]
            self.consumed.append(value)
            output[0] = value
            return True

        self.callback = next_u8
        self.source = RandomSource(self.callback, None)


class CaseMemory:
    def __init__(self, values: tuple[MemoryValue, ...]) -> None:
        self.values = {item.symbol: list(item.value) for item in values}

    def bytes(self, symbol: str, default: tuple[int, ...] = (0,)) -> list[int]:
        return list(self.values.get(symbol, default))

    def byte(self, symbol: str, default: int = 0) -> int:
        return self.bytes(symbol, (default,))[0]

    def word(self, symbol: str, default: int = 0) -> int:
        values = self.bytes(symbol, ((default >> 8) & 0xFF, default & 0xFF))
        return (values[0] << 8) | values[1]


class CRoutineRunner:
    """Run the characterized pure battle routines through the C implementation."""

    SUPPORTED_ENTRIES = frozenset(
        {
            "CalcHitChance",
            "MoveHitTest",
            "RandomizeDamage",
            "AdjustDamageForMoveType",
            "CriticalHitTest",
            "CalculateDamage",
            "GetDamageVarsForPlayerAttack",
            "AIGetTypeEffectiveness",
            "AIEnemyTrainerChooseMoves",
            "SelectEnemyMove.chooseRandomMove",
            "JugglerAI",
            "BlackbeltAI",
            "GiovanniAI",
            "CooltrainerMAI",
            "BlaineAI",
            "CooltrainerFAI",
            "BrockAI",
            "MistyAI",
            "LtSurgeAI",
            "ErikaAI",
            "KogaAI",
            "SabrinaAI",
            "Rival2AI",
            "Rival3AI",
            "LoreleiAI",
            "BrunoAI",
            "AgathaAI",
            "LanceAI",
            "AISwitchIfEnoughMons",
            "DecrementAICount",
        }
    )

    SPECIAL_POLICIES = {
        "JugglerAI": 1,
        "BlackbeltAI": 2,
        "GiovanniAI": 3,
        "CooltrainerMAI": 4,
        "CooltrainerFAI": 5,
        "BrockAI": 6,
        "MistyAI": 7,
        "LtSurgeAI": 8,
        "ErikaAI": 9,
        "KogaAI": 10,
        "BlaineAI": 11,
        "SabrinaAI": 12,
        "Rival2AI": 13,
        "Rival3AI": 14,
        "LoreleiAI": 15,
        "BrunoAI": 16,
        "AgathaAI": 17,
        "LanceAI": 18,
    }

    ACTION_EVENTS = {
        2: "switch",
        3: "use_potion",
        4: "use_super_potion",
        5: "use_hyper_potion",
        6: "use_full_restore",
        7: "use_full_heal",
        8: "use_x_attack",
        9: "use_x_defend",
        10: "use_x_speed",
        11: "use_guard_spec",
    }

    def __init__(self, library: Path, variant: str) -> None:
        self.variant = variant
        self.library = cdll.LoadLibrary(str(library))
        _, symbol_path = artifact_paths(variant)
        self.symbols = SymbolTable.load(symbol_path)
        self.moves = self._load_moves()
        self._configure_abi()

    def _configure_abi(self) -> None:
        library = self.library
        library.combat_math_scale_accuracy.argtypes = [c_uint8, c_uint8, c_uint8]
        library.combat_math_scale_accuracy.restype = c_uint8
        library.combat_math_roll_hit.argtypes = [
            c_uint8,
            c_uint8,
            c_uint8,
            c_bool,
            POINTER(RandomSource),
            POINTER(c_bool),
            POINTER(c_uint8),
        ]
        library.combat_math_roll_hit.restype = c_uint8
        library.combat_math_roll_critical.argtypes = [
            c_uint8,
            c_uint8,
            c_bool,
            c_bool,
            POINTER(RandomSource),
            POINTER(c_bool),
        ]
        library.combat_math_roll_critical.restype = c_uint8
        library.combat_math_is_high_critical_move.argtypes = [c_uint8]
        library.combat_math_is_high_critical_move.restype = c_bool
        library.combat_math_select_damage_stats.argtypes = [
            POINTER(DamageStatsInput),
            POINTER(DamageStats),
        ]
        library.combat_math_select_damage_stats.restype = c_uint8
        library.combat_math_calculate_base_damage.argtypes = [
            POINTER(BaseDamageInput),
            POINTER(c_uint16),
        ]
        library.combat_math_calculate_base_damage.restype = c_uint8
        library.combat_math_apply_type_modifiers.argtypes = [
            c_uint16,
            PokemonTypes,
            PokemonTypes,
            c_uint8,
            POINTER(TypeDamageResult),
        ]
        library.combat_math_apply_type_modifiers.restype = c_uint8
        library.combat_math_ai_type_effectiveness.argtypes = [c_uint8, PokemonTypes]
        library.combat_math_ai_type_effectiveness.restype = c_uint8
        library.combat_math_randomize_damage.argtypes = [
            c_uint16,
            POINTER(RandomSource),
            POINTER(c_uint16),
        ]
        library.combat_math_randomize_damage.restype = c_uint8
        library.trainer_ai_score_moves.argtypes = [
            POINTER(TrainerAiMoveObservation),
            POINTER(TrainerAiMoveScores),
        ]
        library.trainer_ai_score_moves.restype = c_uint8
        library.trainer_ai_choose_move.argtypes = [
            POINTER(TrainerAiMoveScores),
            c_uint8,
            POINTER(RandomSource),
            POINTER(TrainerAiDecision),
        ]
        library.trainer_ai_choose_move.restype = c_uint8
        library.trainer_ai_choose_special_action.argtypes = [
            POINTER(TrainerAiSpecialObservation),
            POINTER(TrainerAiDecision),
        ]
        library.trainer_ai_choose_special_action.restype = c_uint8
        library.trainer_ai_decrement_action_count.argtypes = [c_uint8]
        library.trainer_ai_decrement_action_count.restype = c_uint8

    @staticmethod
    def _load_moves() -> dict[int, TrainerAiMove]:
        effects = constant_values(REPO_ROOT / "constants" / "move_effect_constants.asm")
        types = constant_values(REPO_ROOT / "constants" / "type_constants.asm")
        catalog: dict[int, TrainerAiMove] = {}
        for move_id, row in enumerate(move_rows(), 1):
            catalog[move_id] = TrainerAiMove(
                move_id,
                effects[row.effect],
                int(row.power, 0),
                types[row.type],
            )
        return catalog

    def run(self, case: BattleCase) -> BattleResult:
        if case.entry_symbol not in self.SUPPORTED_ENTRIES:
            raise ValueError(f"C runner does not support {case.entry_symbol}")
        memory = CaseMemory(case.memory)
        random = SequenceRandom(case.rng)
        registers: dict[str, int] = {}
        observed = {
            symbol: memory.bytes(symbol.split(":", 1)[0])
            for symbol in case.observe_memory
        }
        events: list[dict[str, str]] = []

        if case.entry_symbol in self.SPECIAL_POLICIES:
            self._run_special(
                case.entry_symbol, case, memory, registers, observed, events
            )
        else:
            method_name = f"_run_{case.entry_symbol.replace('.', '_')}"
            handler: Callable[..., None] = getattr(self, method_name)
            handler(case, memory, random, registers, observed, events)
        return BattleResult(
            case_id=case.id,
            variant=self.variant,
            termination="returned",
            registers=registers,
            memory=observed,
            events=tuple(events),
            rng_consumed=tuple(random.consumed),
            frames=0,
        )

    @staticmethod
    def _set_word(observed: dict[str, list[int]], symbol: str, value: int) -> None:
        observed[symbol] = [(value >> 8) & 0xFF, value & 0xFF]

    @staticmethod
    def _stub_memory(case: BattleCase, symbol: str) -> CaseMemory:
        stub = next((item for item in case.stubs if item.symbol == symbol), None)
        return CaseMemory(stub.memory if stub is not None else ())

    def _run_CalcHitChance(self, case, memory, random, registers, observed, events) -> None:
        del case, random, registers, events
        scaled = self.library.combat_math_scale_accuracy(
            memory.byte("wPlayerMoveAccuracy"),
            memory.byte("wPlayerMonAccuracyMod"),
            memory.byte("wEnemyMonEvasionMod"),
        )
        observed["wPlayerMoveAccuracy"] = [scaled]

    def _run_MoveHitTest(self, case, memory, random, registers, observed, events) -> None:
        del case, registers, events
        hit = c_bool()
        scaled = c_uint8()
        status = self.library.combat_math_roll_hit(
            memory.byte("wPlayerMoveAccuracy"),
            memory.byte("wPlayerMonAccuracyMod"),
            memory.byte("wEnemyMonEvasionMod"),
            memory.byte("wPlayerMoveEffect") == 0x11,
            byref(random.source),
            byref(hit),
            byref(scaled),
        )
        self._require_ok(status)
        if "wPlayerMoveAccuracy" in observed:
            observed["wPlayerMoveAccuracy"] = [scaled.value]
        observed["wMoveMissed"] = [0 if hit.value else 1]
        if not hit.value:
            observed["wDamage:2"] = [0, 0]

    def _run_RandomizeDamage(self, case, memory, random, registers, observed, events) -> None:
        del case, registers, events
        result = c_uint16()
        self._require_ok(
            self.library.combat_math_randomize_damage(
                memory.word("wDamage"), byref(random.source), byref(result)
            )
        )
        self._set_word(observed, "wDamage:2", result.value)

    def _run_AdjustDamageForMoveType(self, case, memory, random, registers, observed, events) -> None:
        del case, random, registers, events
        result = TypeDamageResult()
        self._require_ok(
            self.library.combat_math_apply_type_modifiers(
                memory.word("wDamage"),
                PokemonTypes(*memory.bytes("wBattleMonType")),
                PokemonTypes(*memory.bytes("wEnemyMonType")),
                memory.byte("wPlayerMoveType"),
                byref(result),
            )
        )
        self._set_word(observed, "wDamage:2", result.damage)
        observed["wDamageMultipliers"] = [result.damage_multipliers]
        observed["wMoveMissed"] = [1 if result.immune_or_rounded_to_zero else 0]

    def _run_CriticalHitTest(self, case, memory, random, registers, observed, events) -> None:
        del registers, events
        move_id = memory.bytes("wPlayerMoveNum")[0]
        move_power = memory.bytes("wPlayerMoveNum")[2]
        base_speed = self._stub_memory(case, "GetMonHeader").byte("wMonHBaseSpeed")
        critical = c_bool()
        self._require_ok(
            self.library.combat_math_roll_critical(
                base_speed,
                move_power,
                self.library.combat_math_is_high_critical_move(move_id),
                (memory.byte("wPlayerBattleStatus2") & 0x04) != 0,
                byref(random.source),
                byref(critical),
            )
        )
        observed["wCriticalHitOrOHKO"] = [1 if critical.value else 0]

    def _run_CalculateDamage(self, case, memory, random, registers, observed, events) -> None:
        del random, events
        inputs = BaseDamageInput(
            registers.get("B", case.registers.get("B", 0)),
            registers.get("C", case.registers.get("C", 0)),
            registers.get("D", case.registers.get("D", 0)),
            registers.get("E", case.registers.get("E", 0)),
            memory.byte("wPlayerMoveEffect"),
            memory.word("wDamage"),
        )
        result = c_uint16()
        self._require_ok(
            self.library.combat_math_calculate_base_damage(byref(inputs), byref(result))
        )
        self._set_word(observed, "wDamage:2", result.value)

    def _run_GetDamageVarsForPlayerAttack(self, case, memory, random, registers, observed, events) -> None:
        del random, observed, events
        critical = memory.byte("wCriticalHitOrOHKO") != 0
        base_attack = memory.word("wPartyMon1Attack", memory.word("wBattleMonAttack"))
        base_special = memory.word("wPartyMon1Special", memory.word("wBattleMonSpecial"))
        enemy_base = self._stub_memory(case, "GetEnemyMonStat").word(
            "hProduct+2",
            memory.word("wEnemyMonDefense"),
        )
        inputs = DamageStatsInput(
            memory.word("wBattleMonAttack"),
            memory.word("wBattleMonSpecial"),
            base_attack,
            base_special,
            memory.word("wEnemyMonDefense"),
            memory.word("wEnemyMonSpecial"),
            enemy_base,
            enemy_base,
            memory.byte("wPlayerMovePower"),
            memory.byte("wPlayerMoveType"),
            memory.byte("wBattleMonLevel"),
            critical,
            (memory.byte("wEnemyBattleStatus3") & 0x01) != 0,
            (memory.byte("wEnemyBattleStatus3") & 0x02) != 0,
        )
        result = DamageStats()
        self._require_ok(
            self.library.combat_math_select_damage_stats(byref(inputs), byref(result))
        )
        registers.update(B=result.attack, C=result.defense, D=result.power, E=result.level)

    def _run_AIGetTypeEffectiveness(self, case, memory, random, registers, observed, events) -> None:
        del case, random, registers, events
        result = self.library.combat_math_ai_type_effectiveness(
            memory.byte("wEnemyMoveType"),
            PokemonTypes(*memory.bytes("wBattleMonType")),
        )
        observed["wTypeEffectiveness"] = [result]

    def _run_AIEnemyTrainerChooseMoves(self, case, memory, random, registers, observed, events) -> None:
        del random, events
        move_ids = memory.bytes("wEnemyMonMoves", (0, 0, 0, 0))
        moves = (TrainerAiMove * 4)(
            *(self.moves[move_id] if move_id else TrainerAiMove() for move_id in move_ids)
        )
        disabled = (memory.byte("wEnemyDisabledMove") >> 4) & 0x0F
        observation = TrainerAiMoveObservation(
            moves,
            PokemonTypes(*memory.bytes("wBattleMonType", (0, 0))),
            memory.byte("wBattleMonStatus"),
            disabled,
            memory.byte("wAILayer2Encouragement"),
            memory.byte("wTrainerClass"),
        )
        result = TrainerAiMoveScores()
        self._require_ok(self.library.trainer_ai_score_moves(byref(observation), byref(result)))
        no_layers = observation.trainer_class in (1, 16)
        observed["wBuffer:4"] = (
            list(result.scores) if no_layers else list(result.candidates)
        )
        if "HL" in case.observe_registers:
            symbol = "wEnemyMonMoves" if no_layers else "wBuffer"
            registers["HL"] = self.symbols.resolve(symbol).address

    def _run_SelectEnemyMove_chooseRandomMove(
        self, case, memory, random, registers, observed, events
    ) -> None:
        del case, registers, events
        scores = TrainerAiMoveScores()
        for index, move_id in enumerate(memory.bytes("wBuffer", (0, 0, 0, 0))):
            scores.candidates[index] = move_id
        decision = TrainerAiDecision()
        disabled = (memory.byte("wEnemyDisabledMove") >> 4) & 0x0F
        self._require_ok(
            self.library.trainer_ai_choose_move(
                byref(scores), disabled, byref(random.source), byref(decision)
            )
        )
        observed["wEnemyMoveListIndex"] = [decision.move_slot]
        observed["wEnemySelectedMove"] = [decision.move_id]

    def _run_special(self, entry, case, memory, registers, observed, events) -> None:
        observation = TrainerAiSpecialObservation(
            GEN1_FIDELITY,
            self.SPECIAL_POLICIES[entry],
            case.registers.get("A", 0),
            memory.word("wEnemyMonHP", 1),
            memory.word("wEnemyMonMaxHP", 1),
            memory.byte("wEnemyMonStatus"),
            2,
        )
        decision = TrainerAiDecision()
        self._require_ok(
            self.library.trainer_ai_choose_special_action(byref(observation), byref(decision))
        )
        if decision.action != 0:
            name = self.ACTION_EVENTS[decision.action]
            symbol = next(
                stub.symbol for stub in case.stubs if stub.event == name
            )
            events.append({"type": "stub", "name": name, "symbol": symbol})

    def _run_AISwitchIfEnoughMons(self, case, memory, random, registers, observed, events) -> None:
        del random, registers, observed
        count = memory.byte("wEnemyPartyCount")
        living = sum(
            memory.word("wEnemyMon1HP" if index == 0 else f"wEnemyMon1HP+{44 * index}")
            != 0
            for index in range(count)
        )
        observation = TrainerAiSpecialObservation(
            GEN1_FIDELITY,
            1,
            0,
            1,
            1,
            0,
            living,
        )
        decision = TrainerAiDecision()
        self._require_ok(
            self.library.trainer_ai_choose_special_action(byref(observation), byref(decision))
        )
        if decision.action == 2:
            stub: Stub = next(item for item in case.stubs if item.event == "switch")
            events.append({"type": "stub", "name": "switch", "symbol": stub.symbol})

    def _run_DecrementAICount(self, case, memory, random, registers, observed, events) -> None:
        del case, random, registers, events
        observed["wAICount"] = [
            self.library.trainer_ai_decrement_action_count(memory.byte("wAICount"))
        ]

    @staticmethod
    def _require_ok(status: int) -> None:
        if status != STATUS_OK:
            raise RuntimeError(f"C battle routine returned status {status}")
