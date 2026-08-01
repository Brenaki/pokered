# Engine Battle 4

> 44 nodes · cohesion 0.11

## Key Concepts

- **CheckEnemyStatusConditions** (40 connections) — `engine/battle/core.asm`
- **CheckPlayerStatusConditions** (35 connections) — `engine/battle/core.asm`
- **Divide** (25 connections) — `home/math.asm`
- **wDamage** (19 connections) — `ram/wram.asm`
- **EnemyCalcMoveDamage** (14 connections) — `engine/battle/core.asm`
- **GetMoveName** (14 connections) — `home/names.asm`
- **PlayerCalcMoveDamage** (13 connections) — `engine/battle/core.asm`
- **PlayMoveAnimation** (12 connections) — `engine/battle/core.asm`
- **HandleSelfConfusionDamage** (11 connections) — `engine/battle/core.asm`
- **CalculateDamage** (10 connections) — `engine/battle/core.asm`
- **CriticalHitTest** (10 connections) — `engine/battle/core.asm`
- **PlayPlayerMoveAnimation** (10 connections) — `engine/battle/core.asm`
- **HandleCounterMove** (9 connections) — `engine/battle/core.asm`
- **PrintMoveIsDisabledText** (9 connections) — `engine/battle/core.asm`
- **AdjustDamageForMoveType** (8 connections) — `engine/battle/core.asm`
- **GetDamageVarsForEnemyAttack** (8 connections) — `engine/battle/core.asm`
- **wPlayerSelectedMove** (8 connections) — `ram/wram.asm`
- **EnemyCheckIfFlyOrChargeEffect** (7 connections) — `engine/battle/core.asm`
- **GetDamageVarsForPlayerAttack** (7 connections) — `engine/battle/core.asm`
- **RandomizeDamage** (7 connections) — `engine/battle/core.asm`
- **GetEnemyMonStat** (6 connections) — `engine/battle/core.asm`
- **HandleIfEnemyMoveMissed** (6 connections) — `engine/battle/core.asm`
- **HandleIfPlayerMoveMissed** (6 connections) — `engine/battle/core.asm`
- **PlayerCheckIfFlyOrChargeEffect** (6 connections) — `engine/battle/core.asm`
- **SwapPlayerAndEnemyLevels** (6 connections) — `engine/battle/core.asm`
- *... and 19 more nodes in this community*

## Relationships

- [Engine Battle 2](Engine_Battle_2.md) (14 shared connections)
- [Engine Battle 6](Engine_Battle_6.md) (13 shared connections)
- [Engine Pokemon](Engine_Pokemon.md) (10 shared connections)
- [Engine Battle](Engine_Battle.md) (6 shared connections)
- [Ram](Ram.md) (5 shared connections)
- [Scripts 2](Scripts_2.md) (4 shared connections)
- [Engine Battle 16](Engine_Battle_16.md) (4 shared connections)
- [Engine Battle 11](Engine_Battle_11.md) (3 shared connections)
- [Bank HRAM](Bank_HRAM.md) (2 shared connections)
- [Engine Battle 10](Engine_Battle_10.md) (2 shared connections)
- [Engine Movie](Engine_Movie.md) (2 shared connections)
- [Engine Battle 13](Engine_Battle_13.md) (2 shared connections)

## Source Files

- `data/battle/set_damage_effects.asm`
- `engine/battle/core.asm`
- `home/math.asm`
- `home/names.asm`
- `ram/wram.asm`

## Audit Trail

- EXTRACTED: 173 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*