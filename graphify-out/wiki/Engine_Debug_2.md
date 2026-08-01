# Engine Debug 2

> 21 nodes · cohesion 0.13

## Key Concepts

- **wNumBagItems** (17 connections) — `ram/wram.asm`
- **TossItem_** (12 connections) — `engine/items/item_effects.asm`
- **RemoveItemFromInventory** (11 connections) — `home/inventory.asm`
- **PrepareNewGameDebug** (10 connections) — `engine/debug/debug_party.asm`
- **ItemUseEvoStone** (9 connections) — `engine/items/item_effects.asm`
- **RemoveUsedItem** (8 connections) — `engine/items/item_effects.asm`
- **RemoveItemByID** (8 connections) — `engine/menus/pc.asm`
- **engine/debug/debug_party.asm** (8 connections) — `engine/debug/debug_party.asm`
- **OaksLabScript_RemoveParcel** (5 connections) — `scripts/OaksLab.asm`
- **SetDebugNewGameParty** (4 connections) — `engine/debug/debug_party.asm`
- **TossItem** (4 connections) — `home/item.asm`
- **wBagItems** (4 connections) — `ram/wram.asm`
- **DisplayPlayerBag** (3 connections) — `engine/battle/core.asm`
- **wRivalStarter** (3 connections) — `ram/wram.asm`
- **DebugNewGameItemsList** (2 connections) — `engine/debug/debug_party.asm`
- **DebugNewGameParty** (2 connections) — `engine/debug/debug_party.asm`
- **DebugSetPokedexEntries** (2 connections) — `engine/debug/debug_party.asm`
- **IsItOKToTossItemText** (2 connections) — `engine/items/item_effects.asm`
- **ThrewAwayItemText** (2 connections) — `engine/items/item_effects.asm`
- **TooImportantToTossText** (2 connections) — `engine/items/item_effects.asm`
- **DebugUnusedList** (1 connections) — `engine/debug/debug_party.asm`

## Relationships

- [Bank WRAM0](Bank_WRAM0.md) (7 shared connections)
- [Scripts](Scripts.md) (2 shared connections)
- [Home](Home.md) (2 shared connections)
- [Engine Menus 2](Engine_Menus_2.md) (1 shared connections)
- [Engine Items](Engine_Items.md) (1 shared connections)
- [Engine Items 3](Engine_Items_3.md) (1 shared connections)
- [Engine Pokemon 2](Engine_Pokemon_2.md) (1 shared connections)
- [Bank ROMX](Bank_ROMX.md) (1 shared connections)

## Source Files

- `engine/battle/core.asm`
- `engine/debug/debug_party.asm`
- `engine/items/item_effects.asm`
- `engine/menus/pc.asm`
- `home/inventory.asm`
- `home/item.asm`
- `ram/wram.asm`
- `scripts/OaksLab.asm`

## Audit Trail

- EXTRACTED: 44 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*