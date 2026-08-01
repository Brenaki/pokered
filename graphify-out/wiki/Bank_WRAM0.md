# Bank WRAM0

> 256 nodes · cohesion 0.02

## Key Concepts

- **CopyData** (113 connections) — `home/copy.asm`
- **AddNTimes** (71 connections) — `home/array.asm`
- **ItemUseMedicine** (39 connections) — `engine/items/item_effects.asm`
- **GetMonHeader** (39 connections) — `home/pokemon.asm`
- **TradeCenter_Trade** (38 connections) — `engine/link/cable_club.asm`
- **Evolution_PartyMonLoop** (36 connections) — `engine/pokemon/evos_moves.asm`
- **wNameBuffer** (35 connections) — `ram/wram.asm`
- **GainExperience** (29 connections) — `engine/battle/experience.asm`
- **RedrawPartyMenu_** (27 connections) — `engine/menus/party_menu.asm`
- **_AddPartyMon** (27 connections) — `engine/pokemon/add_mon.asm`
- **DaycareGentlemanText** (27 connections) — `scripts/Daycare.asm`
- **wPartyMonNicks** (26 connections) — `ram/wram.asm`
- **LoadEnemyMonData** (25 connections) — `engine/battle/core.asm`
- **FlagActionPredef** (25 connections) — `engine/flag_action.asm`
- **GetMonName** (25 connections) — `home/names.asm`
- **DoInGameTradeDialogue** (24 connections) — `engine/events/in_game_trades.asm`
- **DisplayListMenuIDLoop** (22 connections) — `home/list_menu.asm`
- **PrintListMenuEntries** (20 connections) — `home/list_menu.asm`
- **GetItemName** (20 connections) — `home/names.asm`
- **wBuffer** (20 connections) — `ram/wram.asm`
- **IndexToPokedex** (18 connections) — `engine/menus/pokedex.asm`
- **_MoveMon** (18 connections) — `engine/pokemon/add_mon.asm`
- **engine/battle/draw_hud_pokeball_gfx.asm** (18 connections) — `engine/battle/draw_hud_pokeball_gfx.asm`
- **engine/pokemon/evos_moves.asm** (18 connections) — `engine/pokemon/evos_moves.asm`
- **CopyToStringBuffer** (18 connections) — `home/copy_string.asm`
- *... and 231 more nodes in this community*

## Relationships

- [Home](Home.md) (54 shared connections)
- [Ram](Ram.md) (33 shared connections)
- [Scripts](Scripts.md) (25 shared connections)
- [Engine Link](Engine_Link.md) (21 shared connections)
- [Engine Overworld](Engine_Overworld.md) (20 shared connections)
- [Engine Battle](Engine_Battle.md) (17 shared connections)
- [Engine Battle 2](Engine_Battle_2.md) (16 shared connections)
- [Data Sgb](Data_Sgb.md) (8 shared connections)
- [Engine Pokemon 2](Engine_Pokemon_2.md) (7 shared connections)
- [Bank VRAM](Bank_VRAM.md) (7 shared connections)
- [Engine Battle 3](Engine_Battle_3.md) (7 shared connections)
- [Engine Items](Engine_Items.md) (6 shared connections)

## Source Files

- `data/battle/stat_names.asm`
- `data/items/names.asm`
- `data/items/prices.asm`
- `data/moves/moves.asm`
- `data/pokemon/base_stats.asm`
- `data/pokemon/names.asm`
- `data/sgb/sgb_packets.asm`
- `data/trainers/special_moves.asm`
- `docs/002-2026-08-01-Informações_sobre_Pokemons.md`
- `docs/003-2026-08-01-Funcionamento-das-IAs-Pokemon.md`
- `engine/battle/animations.asm`
- `engine/battle/core.asm`
- `engine/battle/draw_hud_pokeball_gfx.asm`
- `engine/battle/experience.asm`
- `engine/battle/get_trainer_name.asm`
- `engine/battle/misc.asm`
- `engine/battle/read_trainer_party.asm`
- `engine/battle/trainer_ai.asm`
- `engine/events/cinnabar_lab.asm`
- `engine/events/display_pokedex.asm`

## Audit Trail

- EXTRACTED: 1006 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*