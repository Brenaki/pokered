# Bank SRAM

> 31 nodes · cohesion 0.16

## Key Concepts

- **ram/sram.asm** (24 connections) — `ram/sram.asm`
- **LoadMainData** (21 connections) — `engine/menus/save.asm`
- **SaveMainData** (17 connections) — `engine/menus/save.asm`
- **LoadPartyAndDexData** (15 connections) — `engine/menus/save.asm`
- **SavePartyAndDexData** (13 connections) — `engine/menus/save.asm`
- **LoadCurrentBoxData** (12 connections) — `engine/menus/save.asm`
- **Save Data [SRAM]** (11 connections) — `ram/sram.asm`
- **sGameData** (9 connections) — `ram/sram.asm`
- **sGameDataEnd** (9 connections) — `ram/sram.asm`
- **sMainData** (7 connections) — `ram/sram.asm`
- **wBoxDataStart** (7 connections) — `ram/wram.asm`
- **CheckPreviousSaveFile** (6 connections) — `engine/menus/save.asm`
- **sCurBoxData** (6 connections) — `ram/sram.asm`
- **sPlayerName** (5 connections) — `ram/sram.asm`
- **wPokedexSeenEnd** (5 connections) — `ram/wram.asm`
- **SRAM** (4 connections)
- **CheckSumFailed** (4 connections) — `engine/menus/save.asm`
- **GoodCheckSum** (4 connections) — `engine/menus/save.asm`
- **TryLoadSaveFileIgnoreChecksum** (4 connections) — `engine/menus/save.asm`
- **sPartyData** (4 connections) — `ram/sram.asm`
- **sSpriteData** (4 connections) — `ram/sram.asm`
- **Saved Boxes 2 [SRAM]** (4 connections) — `ram/sram.asm`
- **wCurMapTileset** (4 connections) — `ram/wram.asm`
- **wMainDataEnd** (4 connections) — `ram/wram.asm`
- **wMainDataStart** (4 connections) — `ram/wram.asm`
- *... and 6 more nodes in this community*

## Relationships

- [Engine Menus 8](Engine_Menus_8.md) (12 shared connections)
- [Engine Pokemon](Engine_Pokemon.md) (5 shared connections)
- [Engine Menus 2](Engine_Menus_2.md) (4 shared connections)
- [Bank WRAM0](Bank_WRAM0.md) (4 shared connections)
- [Engine Battle 11](Engine_Battle_11.md) (4 shared connections)
- [Engine Menus 5](Engine_Menus_5.md) (1 shared connections)

## Source Files

- `engine/menus/save.asm`
- `ram/sram.asm`
- `ram/wram.asm`

## Audit Trail

- EXTRACTED: 105 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*