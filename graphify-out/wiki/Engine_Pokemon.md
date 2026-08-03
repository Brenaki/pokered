# Engine Pokemon

> 97 nodes · cohesion 0.05

## Key Concepts

- **CopyData** (113 connections) — `home/copy.asm`
- **AddNTimes** (71 connections) — `home/array.asm`
- **GetMonHeader** (39 connections) — `home/pokemon.asm`
- **Evolution_PartyMonLoop** (36 connections) — `engine/pokemon/evos_moves.asm`
- **wNameBuffer** (35 connections) — `ram/wram.asm`
- **GainExperience** (29 connections) — `engine/battle/experience.asm`
- **LoadEnemyMonData** (25 connections) — `engine/battle/core.asm`
- **ItemUsePPRestore** (25 connections) — `engine/items/item_effects.asm`
- **GetMonName** (25 connections) — `home/names.asm`
- **DoInGameTradeDialogue** (24 connections) — `engine/events/in_game_trades.asm`
- **GetItemName** (20 connections) — `home/names.asm`
- **engine/pokemon/evos_moves.asm** (18 connections) — `engine/pokemon/evos_moves.asm`
- **TryingToLearn** (17 connections) — `engine/pokemon/learn_move.asm`
- **engine/pokemon/learn_move.asm** (16 connections) — `engine/pokemon/learn_move.asm`
- **GetName** (15 connections) — `home/names2.asm`
- **LoadEnemyMonFromParty** (14 connections) — `engine/battle/core.asm`
- **HealParty** (14 connections) — `engine/events/heal_party.asm`
- **GiveFossilToCinnabarLab** (13 connections) — `engine/events/cinnabar_lab.asm`
- **DontAbandonLearning** (13 connections) — `engine/pokemon/learn_move.asm`
- **engine/battle/experience.asm** (12 connections) — `engine/battle/experience.asm`
- **home/names.asm** (12 connections) — `home/names.asm`
- **engine/pokemon** (11 connections)
- **WriteMonMoves** (11 connections) — `engine/pokemon/evos_moves.asm`
- **FarCopyData** (11 connections) — `home/copy.asm`
- **GetMaxPP** (9 connections) — `engine/items/item_effects.asm`
- *... and 72 more nodes in this community*

## Relationships

- [Bank WRAM0](Bank_WRAM0.md) (46 shared connections)
- [Engine Battle](Engine_Battle.md) (36 shared connections)
- [Scripts 2](Scripts_2.md) (22 shared connections)
- [Ram](Ram.md) (20 shared connections)
- [Engine Menus](Engine_Menus.md) (8 shared connections)
- [Engine Items](Engine_Items.md) (7 shared connections)
- [Engine Gfx 2](Engine_Gfx_2.md) (4 shared connections)
- [Engine Battle 5](Engine_Battle_5.md) (4 shared connections)
- [Data Pokemon](Data_Pokemon.md) (4 shared connections)
- [Engine Battle 2](Engine_Battle_2.md) (3 shared connections)
- [Bank VRAM](Bank_VRAM.md) (3 shared connections)
- [Scripts 4](Scripts_4.md) (3 shared connections)

## Source Files

- `data/growth_rates.asm`
- `data/pokemon/base_stats.asm`
- `engine/battle/core.asm`
- `engine/battle/experience.asm`
- `engine/battle/get_trainer_name.asm`
- `engine/battle/misc.asm`
- `engine/events/cinnabar_lab.asm`
- `engine/events/heal_party.asm`
- `engine/events/in_game_trades.asm`
- `engine/items/item_effects.asm`
- `engine/pokemon/add_mon.asm`
- `engine/pokemon/evos_moves.asm`
- `engine/pokemon/experience.asm`
- `engine/pokemon/learn_move.asm`
- `engine/pokemon/load_mon_data.asm`
- `engine/pokemon/remove_mon.asm`
- `engine/pokemon/set_types.asm`
- `home/array.asm`
- `home/copy.asm`
- `home/names.asm`

## Audit Trail

- EXTRACTED: 402 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*