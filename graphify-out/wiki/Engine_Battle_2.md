# Engine Battle 2

> 178 nodes · cohesion 0.03

## Key Concepts

- **engine/battle/effects.asm** (100 connections) — `engine/battle/effects.asm`
- **engine/battle** (40 connections)
- **MoveEffectPointerTable** (38 connections) — `data/moves/effects_pointers.asm`
- **BattleRandom** (33 connections) — `engine/battle/core.asm`
- **wEnemyBattleStatus1** (23 connections) — `ram/wram.asm`
- **wPlayerBattleStatus1** (23 connections) — `ram/wram.asm`
- **wEnemyBattleStatus2** (22 connections) — `ram/wram.asm`
- **wPlayerBattleStatus2** (22 connections) — `ram/wram.asm`
- **StatModifierDownEffect** (21 connections) — `engine/battle/effects.asm`
- **MoveHitTest** (20 connections) — `engine/battle/core.asm`
- **TransformEffect_** (20 connections) — `engine/battle/move_effects/transform.asm`
- **PoisonEffect** (18 connections) — `engine/battle/effects.asm`
- **UpdateStatDone** (18 connections) — `engine/battle/effects.asm`
- **Bankswitch** (18 connections) — `home/bankswitch.asm`
- **StatModifierUpEffect** (17 connections) — `engine/battle/effects.asm`
- **HazeEffect_** (16 connections) — `engine/battle/move_effects/haze.asm`
- **SwitchAndTeleportEffect** (14 connections) — `engine/battle/effects.asm`
- **wEnemyMoveEffect** (14 connections) — `ram/wram.asm`
- **FreezeBurnParalyzeEffect** (13 connections) — `engine/battle/effects.asm`
- **SubstituteEffect_** (13 connections) — `engine/battle/move_effects/substitute.asm`
- **wPlayerMoveEffect** (13 connections) — `ram/wram.asm`
- **HideSubstituteShowMonAnim** (12 connections) — `engine/battle/animations.asm`
- **HandleBuildingRage** (12 connections) — `engine/battle/core.asm`
- **DisableEffect** (12 connections) — `engine/battle/effects.asm`
- **MimicEffect** (12 connections) — `engine/battle/effects.asm`
- *... and 153 more nodes in this community*

## Relationships

- [Scripts](Scripts.md) (27 shared connections)
- [Engine Battle](Engine_Battle.md) (20 shared connections)
- [Ram 2](Ram_2.md) (16 shared connections)
- [Bank WRAM0](Bank_WRAM0.md) (15 shared connections)
- [Engine Battle 3](Engine_Battle_3.md) (13 shared connections)
- [Ram](Ram.md) (10 shared connections)
- [Engine Battle 10](Engine_Battle_10.md) (2 shared connections)
- [Home 3](Home_3.md) (1 shared connections)
- [Engine Battle 4](Engine_Battle_4.md) (1 shared connections)
- [Engine Battle 7](Engine_Battle_7.md) (1 shared connections)
- [Engine Battle 11](Engine_Battle_11.md) (1 shared connections)
- [Engine Battle 8](Engine_Battle_8.md) (1 shared connections)

## Source Files

- `data/battle/stat_mod_names.asm`
- `data/battle/stat_modifiers.asm`
- `data/moves/effects_pointers.asm`
- `engine/battle/animations.asm`
- `engine/battle/core.asm`
- `engine/battle/effects.asm`
- `engine/battle/get_trainer_name.asm`
- `engine/battle/init_battle_variables.asm`
- `engine/battle/link_battle_versus_text.asm`
- `engine/battle/move_effects/conversion.asm`
- `engine/battle/move_effects/focus_energy.asm`
- `engine/battle/move_effects/haze.asm`
- `engine/battle/move_effects/heal.asm`
- `engine/battle/move_effects/leech_seed.asm`
- `engine/battle/move_effects/mist.asm`
- `engine/battle/move_effects/one_hit_ko.asm`
- `engine/battle/move_effects/paralyze.asm`
- `engine/battle/move_effects/reflect_light_screen.asm`
- `engine/battle/move_effects/substitute.asm`
- `engine/battle/move_effects/transform.asm`

## Audit Trail

- EXTRACTED: 568 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*