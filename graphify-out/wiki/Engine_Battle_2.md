# Engine Battle 2

> 159 nodes · cohesion 0.03

## Key Concepts

- **engine/battle/effects.asm** (100 connections) — `engine/battle/effects.asm`
- **MoveEffectPointerTable** (38 connections) — `data/moves/effects_pointers.asm`
- **BattleRandom** (35 connections) — `engine/battle/core.asm`
- **Divide** (25 connections) — `home/math.asm`
- **wEnemyBattleStatus1** (23 connections) — `ram/wram.asm`
- **wEnemyBattleStatus2** (22 connections) — `ram/wram.asm`
- **wPlayerBattleStatus2** (22 connections) — `ram/wram.asm`
- **StatModifierDownEffect** (21 connections) — `engine/battle/effects.asm`
- **MoveHitTest** (20 connections) — `engine/battle/core.asm`
- **TransformEffect_** (20 connections) — `engine/battle/move_effects/transform.asm`
- **PoisonEffect** (18 connections) — `engine/battle/effects.asm`
- **UpdateStatDone** (18 connections) — `engine/battle/effects.asm`
- **Multiply** (18 connections) — `home/math.asm`
- **StatModifierUpEffect** (17 connections) — `engine/battle/effects.asm`
- **HazeEffect_** (16 connections) — `engine/battle/move_effects/haze.asm`
- **SwitchAndTeleportEffect** (14 connections) — `engine/battle/effects.asm`
- **wEnemyMoveEffect** (14 connections) — `ram/wram.asm`
- **FreezeBurnParalyzeEffect** (13 connections) — `engine/battle/effects.asm`
- **wPlayerMoveEffect** (13 connections) — `ram/wram.asm`
- **HideSubstituteShowMonAnim** (12 connections) — `engine/battle/animations.asm`
- **HandleBuildingRage** (12 connections) — `engine/battle/core.asm`
- **DisableEffect** (12 connections) — `engine/battle/effects.asm`
- **MimicEffect** (12 connections) — `engine/battle/effects.asm`
- **ReflectLightScreenEffect_** (12 connections) — `engine/battle/move_effects/reflect_light_screen.asm`
- **ConfusionSideEffectSuccess** (11 connections) — `engine/battle/effects.asm`
- *... and 134 more nodes in this community*

## Relationships

- [Engine Battle](Engine_Battle.md) (24 shared connections)
- [Scripts](Scripts.md) (23 shared connections)
- [Bank WRAM0](Bank_WRAM0.md) (12 shared connections)
- [Ram](Ram.md) (9 shared connections)
- [Engine Battle 7](Engine_Battle_7.md) (6 shared connections)
- [Engine Overworld](Engine_Overworld.md) (5 shared connections)
- [Home](Home.md) (3 shared connections)
- [Engine Battle 12](Engine_Battle_12.md) (2 shared connections)
- [Bank ROM0](Bank_ROM0.md) (1 shared connections)
- [Engine Slots](Engine_Slots.md) (1 shared connections)
- [Ram 5](Ram_5.md) (1 shared connections)
- [Home 7](Home_7.md) (1 shared connections)

## Source Files

- `data/battle/stat_mod_names.asm`
- `data/battle/stat_modifiers.asm`
- `data/growth_rates.asm`
- `data/moves/effects_pointers.asm`
- `engine/battle/animations.asm`
- `engine/battle/core.asm`
- `engine/battle/effects.asm`
- `engine/battle/move_effects/conversion.asm`
- `engine/battle/move_effects/haze.asm`
- `engine/battle/move_effects/mist.asm`
- `engine/battle/move_effects/reflect_light_screen.asm`
- `engine/battle/move_effects/transform.asm`
- `engine/pokemon/experience.asm`
- `home/math.asm`
- `ram/wram.asm`

## Audit Trail

- EXTRACTED: 495 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*