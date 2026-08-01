# Ram 4

> 27 nodes · cohesion 0.19

## Key Concepts

- **LoadMainData** (21 connections) — `engine/menus/save.asm`
- **SaveMainData** (17 connections) — `engine/menus/save.asm`
- **LoadPartyAndDexData** (15 connections) — `engine/menus/save.asm`
- **SavePartyAndDexData** (13 connections) — `engine/menus/save.asm`
- **LoadCurrentBoxData** (12 connections) — `engine/menus/save.asm`
- **CalcCheckSum** (11 connections) — `engine/menus/save.asm`
- **SaveCurrentBoxData** (9 connections) — `engine/menus/save.asm`
- **sGameData** (9 connections) — `ram/sram.asm`
- **sGameDataEnd** (9 connections) — `ram/sram.asm`
- **wBoxDataEnd** (9 connections) — `ram/wram.asm`
- **CopyBoxToOrFromSRAM** (7 connections) — `engine/menus/save.asm`
- **sMainData** (7 connections) — `ram/sram.asm`
- **wBoxDataStart** (7 connections) — `ram/wram.asm`
- **CalcIndividualBoxCheckSums** (6 connections) — `engine/menus/save.asm`
- **CheckPreviousSaveFile** (6 connections) — `engine/menus/save.asm`
- **sCurBoxData** (6 connections) — `ram/sram.asm`
- **wPokedexSeenEnd** (5 connections) — `ram/wram.asm`
- **wSpriteDataEnd** (5 connections) — `ram/wram.asm`
- **wSpriteDataStart** (5 connections) — `ram/wram.asm`
- **CheckSumFailed** (4 connections) — `engine/menus/save.asm`
- **GoodCheckSum** (4 connections) — `engine/menus/save.asm`
- **TryLoadSaveFileIgnoreChecksum** (4 connections) — `engine/menus/save.asm`
- **wCurMapTileset** (4 connections) — `ram/wram.asm`
- **wMainDataEnd** (4 connections) — `ram/wram.asm`
- **wMainDataStart** (4 connections) — `ram/wram.asm`
- *... and 2 more nodes in this community*

## Relationships

- [Bank SRAM](Bank_SRAM.md) (7 shared connections)
- [Engine Pokemon](Engine_Pokemon.md) (7 shared connections)
- [Engine Menus](Engine_Menus.md) (2 shared connections)
- [Engine Menus 2](Engine_Menus_2.md) (2 shared connections)
- [Engine Menus 4](Engine_Menus_4.md) (1 shared connections)

## Source Files

- `engine/menus/save.asm`
- `ram/sram.asm`
- `ram/wram.asm`

## Audit Trail

- EXTRACTED: 86 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*