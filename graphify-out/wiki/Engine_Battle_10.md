# Engine Battle 10

> 27 nodes · cohesion 0.12

## Key Concepts

- **UpdateStatDone** (18 connections) — `engine/battle/effects.asm`
- **wBuffer** (18 connections) — `ram/wram.asm`
- **GetCurrentMove** (13 connections) — `engine/battle/core.asm`
- **MetronomePickMove** (10 connections) — `engine/battle/core.asm`
- **MirrorMoveCopyMove** (10 connections) — `engine/battle/core.asm`
- **Moves** (9 connections) — `data/moves/moves.asm`
- **ReloadMoveData** (9 connections) — `engine/battle/core.asm`
- **UpdateLoweredStatDone** (9 connections) — `engine/battle/effects.asm`
- **ReadMove** (8 connections) — `engine/battle/trainer_ai.asm`
- **wEnemyMoveNum** (8 connections) — `ram/wram.asm`
- **wPlayerMoveNum** (8 connections) — `ram/wram.asm`
- **wEnemySelectedMove** (7 connections) — `ram/wram.asm`
- **PrintStatText** (6 connections) — `engine/battle/effects.asm`
- **AIMoveChoiceModification1** (6 connections) — `engine/battle/trainer_ai.asm`
- **AIMoveChoiceModificationFunctionPointers** (6 connections) — `engine/battle/trainer_ai.asm`
- **HalveAttackDueToBurn** (5 connections) — `engine/battle/core.asm`
- **QuarterSpeedDueToParalysis** (5 connections) — `engine/battle/core.asm`
- **ApplyBadgeStatBoosts** (4 connections) — `engine/battle/core.asm`
- **ApplyBurnAndParalysisPenalties** (4 connections) — `engine/battle/core.asm`
- **AIEnemyTrainerChooseMoves** (4 connections) — `engine/battle/trainer_ai.asm`
- **AIMoveChoiceModification2** (4 connections) — `engine/battle/trainer_ai.asm`
- **AIMoveChoiceModification3** (4 connections) — `engine/battle/trainer_ai.asm`
- **ApplyBurnAndParalysisPenaltiesToPlayer** (3 connections) — `engine/battle/core.asm`
- **IncrementMovePP** (3 connections) — `engine/battle/core.asm`
- **data/battle/stat_mod_names.asm** (3 connections) — `data/battle/stat_mod_names.asm`
- *... and 2 more nodes in this community*

## Relationships

- [Engine Pokemon](Engine_Pokemon.md) (13 shared connections)
- [Engine Battle 2](Engine_Battle_2.md) (5 shared connections)
- [Engine Battle 4](Engine_Battle_4.md) (4 shared connections)
- [Scripts 2](Scripts_2.md) (3 shared connections)
- [Engine Battle 8](Engine_Battle_8.md) (2 shared connections)
- [Engine Battle 16](Engine_Battle_16.md) (2 shared connections)
- [Ram](Ram.md) (2 shared connections)
- [Engine Battle 9](Engine_Battle_9.md) (2 shared connections)
- [Home 2](Home_2.md) (1 shared connections)
- [Data Trainers 2](Data_Trainers_2.md) (1 shared connections)
- [Engine Battle 6](Engine_Battle_6.md) (1 shared connections)

## Source Files

- `data/battle/stat_mod_names.asm`
- `data/moves/moves.asm`
- `engine/battle/core.asm`
- `engine/battle/effects.asm`
- `engine/battle/trainer_ai.asm`
- `ram/wram.asm`

## Audit Trail

- EXTRACTED: 78 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*