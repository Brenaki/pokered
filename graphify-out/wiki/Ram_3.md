# Ram 3

> 120 nodes · cohesion 0.04

## Key Concepts

- **AddNTimes** (71 connections) — `home/array.asm`
- **GetMonHeader** (39 connections) — `home/pokemon.asm`
- **GainExperience** (29 connections) — `engine/battle/experience.asm`
- **_AddPartyMon** (27 connections) — `engine/pokemon/add_mon.asm`
- **LoadEnemyMonData** (25 connections) — `engine/battle/core.asm`
- **_MoveMon** (18 connections) — `engine/pokemon/add_mon.asm`
- **engine/battle/draw_hud_pokeball_gfx.asm** (18 connections) — `engine/battle/draw_hud_pokeball_gfx.asm`
- **Moves** (15 connections) — `data/moves/moves.asm`
- **_AddEnemyMonToPlayerParty** (15 connections) — `engine/pokemon/add_mon.asm`
- **wPartyCount** (15 connections) — `ram/wram.asm`
- **LoadBattleMonFromParty** (14 connections) — `engine/battle/core.asm`
- **LoadEnemyMonFromParty** (14 connections) — `engine/battle/core.asm`
- **HealParty** (14 connections) — `engine/events/heal_party.asm`
- **_RemovePokemon** (14 connections) — `engine/pokemon/remove_mon.asm`
- **wPartyMonOT** (14 connections) — `ram/wram.asm`
- **wPartySpecies** (14 connections) — `ram/wram.asm`
- **GetCurrentMove** (13 connections) — `engine/battle/core.asm`
- **SendNewMonToBox** (13 connections) — `engine/items/item_effects.asm`
- **engine/battle/experience.asm** (12 connections) — `engine/battle/experience.asm`
- **wPartyMons** (12 connections) — `ram/wram.asm`
- **SwitchPartyMon_InitVarOrSwapData** (11 connections) — `engine/menus/start_sub_menus.asm`
- **WriteMonMoves** (11 connections) — `engine/pokemon/evos_moves.asm`
- **SkipFixedLengthTextEntries** (11 connections) — `home/array.asm`
- **FarCopyData** (11 connections) — `home/copy.asm`
- **CalcStats** (11 connections) — `home/move_mon.asm`
- *... and 95 more nodes in this community*

## Relationships

- [Engine Pokemon](Engine_Pokemon.md) (35 shared connections)
- [Home](Home.md) (5 shared connections)
- [Engine Battle 5](Engine_Battle_5.md) (5 shared connections)
- [Engine Menus 2](Engine_Menus_2.md) (5 shared connections)
- [Engine Battle 4](Engine_Battle_4.md) (4 shared connections)
- [Engine Menus](Engine_Menus.md) (4 shared connections)
- [Engine Link](Engine_Link.md) (4 shared connections)
- [Engine Items 2](Engine_Items_2.md) (3 shared connections)
- [Engine Battle 10](Engine_Battle_10.md) (3 shared connections)
- [Bank SRAM](Bank_SRAM.md) (3 shared connections)
- [Engine Battle 9](Engine_Battle_9.md) (2 shared connections)
- [Engine Battle 8](Engine_Battle_8.md) (2 shared connections)

## Source Files

- `data/items/names.asm`
- `data/moves/moves.asm`
- `data/pokemon/names.asm`
- `engine/battle/core.asm`
- `engine/battle/draw_hud_pokeball_gfx.asm`
- `engine/battle/experience.asm`
- `engine/battle/misc.asm`
- `engine/events/heal_party.asm`
- `engine/flag_action.asm`
- `engine/items/item_effects.asm`
- `engine/menus/start_sub_menus.asm`
- `engine/menus/text_box.asm`
- `engine/pokemon/add_mon.asm`
- `engine/pokemon/evos_moves.asm`
- `engine/pokemon/experience.asm`
- `engine/pokemon/load_mon_data.asm`
- `engine/pokemon/remove_mon.asm`
- `engine/pokemon/status_screen.asm`
- `gfx/battle/balls.2bpp`
- `home/array.asm`

## Audit Trail

- EXTRACTED: 372 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*