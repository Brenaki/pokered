# Engine Battle 3

> 64 nodes · cohesion 0.04

## Key Concepts

- **engine/battle** (40 connections)
- **EndOfBattle** (21 connections) — `engine/battle/end_of_battle.asm`
- **SubstituteEffect_** (13 connections) — `engine/battle/move_effects/substitute.asm`
- **engine/battle/experience.asm** (12 connections) — `engine/battle/experience.asm`
- **engine/battle/end_of_battle.asm** (9 connections) — `engine/battle/end_of_battle.asm`
- **PrintSafariZoneBattleText** (8 connections) — `engine/battle/safari_zone.asm`
- **ItemUseBait** (8 connections) — `engine/items/item_effects.asm`
- **engine/battle/safari_zone.asm** (8 connections) — `engine/battle/safari_zone.asm`
- **LeechSeedEffect_** (7 connections) — `engine/battle/move_effects/leech_seed.asm`
- **PayDayEffect_** (7 connections) — `engine/battle/move_effects/pay_day.asm`
- **PrintMonType** (7 connections) — `engine/battle/print_type.asm`
- **engine/battle/print_type.asm** (7 connections) — `engine/battle/print_type.asm`
- **FocusEnergyEffect_** (6 connections) — `engine/battle/move_effects/focus_energy.asm`
- **engine/battle/move_effects/substitute.asm** (6 connections) — `engine/battle/move_effects/substitute.asm`
- **GainedText** (5 connections) — `engine/battle/experience.asm`
- **BaitRockCommon** (5 connections) — `engine/items/item_effects.asm`
- **engine/battle/move_effects/leech_seed.asm** (5 connections) — `engine/battle/move_effects/leech_seed.asm`
- **wPartyAndBillsPCSavedMenuItem** (5 connections) — `ram/wram.asm`
- **wSafariBaitFactor** (5 connections) — `ram/wram.asm`
- **DivideExpDataByNumMonsGainingExp** (4 connections) — `engine/battle/experience.asm`
- **InitBattleVariables** (4 connections) — `engine/battle/init_battle_variables.asm`
- **ParalyzeEffect_** (4 connections) — `engine/battle/move_effects/paralyze.asm`
- **PrintType** (4 connections) — `engine/battle/print_type.asm`
- **SaveTrainerName** (4 connections) — `engine/battle/save_trainer_name.asm`
- **_ScrollTrainerPicAfterBattle** (4 connections) — `engine/battle/scroll_draw_trainer_pic.asm`
- *... and 39 more nodes in this community*

## Relationships

- [Engine Battle 2](Engine_Battle_2.md) (15 shared connections)
- [Bank WRAM0](Bank_WRAM0.md) (12 shared connections)
- [Engine Overworld](Engine_Overworld.md) (11 shared connections)
- [Engine Battle](Engine_Battle.md) (8 shared connections)
- [Scripts](Scripts.md) (8 shared connections)
- [Ram](Ram.md) (6 shared connections)
- [Home](Home.md) (5 shared connections)
- [Engine Link](Engine_Link.md) (4 shared connections)
- [Bank ROMX](Bank_ROMX.md) (2 shared connections)
- [Scripts 8](Scripts_8.md) (2 shared connections)
- [Engine Battle 4](Engine_Battle_4.md) (1 shared connections)
- [Engine Battle 6](Engine_Battle_6.md) (1 shared connections)

## Source Files

- `data/trainers/name_pointers.asm`
- `data/types/names.asm`
- `engine/battle/end_of_battle.asm`
- `engine/battle/experience.asm`
- `engine/battle/get_trainer_name.asm`
- `engine/battle/init_battle_variables.asm`
- `engine/battle/link_battle_versus_text.asm`
- `engine/battle/move_effects/focus_energy.asm`
- `engine/battle/move_effects/leech_seed.asm`
- `engine/battle/move_effects/one_hit_ko.asm`
- `engine/battle/move_effects/paralyze.asm`
- `engine/battle/move_effects/pay_day.asm`
- `engine/battle/move_effects/substitute.asm`
- `engine/battle/print_type.asm`
- `engine/battle/safari_zone.asm`
- `engine/battle/save_trainer_name.asm`
- `engine/battle/scroll_draw_trainer_pic.asm`
- `engine/items/item_effects.asm`
- `engine/pokemon/evos_moves.asm`
- `ram/wram.asm`

## Audit Trail

- EXTRACTED: 173 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*