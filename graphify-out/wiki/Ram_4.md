# Ram 4

> 27 nodes · cohesion 0.19

## Key Concepts

- **LoadMainData** (21 connections) — `engine/menus/save.asm`
- **SaveMainData** (17 connections) — `engine/menus/save.asm`
- **LoadPartyAndDexData** (15 connections) — `engine/menus/save.asm`
- **SavePartyAndDexData** (13 connections) — `engine/menus/save.asm`
- **TryLoadSaveFile** (13 connections) — `engine/menus/save.asm`
- **LoadCurrentBoxData** (12 connections) — `engine/menus/save.asm`
- **CalcCheckSum** (11 connections) — `engine/menus/save.asm`
- **SaveCurrentBoxData** (9 connections) — `engine/menus/save.asm`
- **sGameData** (9 connections) — `ram/sram.asm`
- **sGameDataEnd** (9 connections) — `ram/sram.asm`
- **wBoxDataEnd** (9 connections) — `ram/wram.asm`
- **sMainData** (7 connections) — `ram/sram.asm`
- **wBoxDataStart** (7 connections) — `ram/wram.asm`
- **CheckPreviousSaveFile** (6 connections) — `engine/menus/save.asm`
- **sCurBoxData** (6 connections) — `ram/sram.asm`
- **wPokedexSeenEnd** (5 connections) — `ram/wram.asm`
- **wSpriteDataEnd** (5 connections) — `ram/wram.asm`
- **wSpriteDataStart** (5 connections) — `ram/wram.asm`
- **CheckSumFailed** (4 connections) — `engine/menus/save.asm`
- **GoodCheckSum** (4 connections) — `engine/menus/save.asm`
- **TryLoadSaveFileIgnoreChecksum** (4 connections) — `engine/menus/save.asm`
- **sPartyData** (4 connections) — `ram/sram.asm`
- **wMainDataEnd** (4 connections) — `ram/wram.asm`
- **wMainDataStart** (4 connections) — `ram/wram.asm`
- **wPartyDataEnd** (4 connections) — `ram/wram.asm`
- *... and 2 more nodes in this community*

## Relationships

- [Engine Pokemon](Engine_Pokemon.md) (8 shared connections)
- [Bank SRAM](Bank_SRAM.md) (4 shared connections)
- [Home](Home.md) (3 shared connections)
- [Engine Menus](Engine_Menus.md) (2 shared connections)
- [Home 2](Home_2.md) (1 shared connections)
- [Engine Link](Engine_Link.md) (1 shared connections)
- [Engine Movie](Engine_Movie.md) (1 shared connections)
- [Scripts](Scripts.md) (1 shared connections)

## Source Files

- `engine/menus/save.asm`
- `ram/sram.asm`
- `ram/wram.asm`

## Audit Trail

- EXTRACTED: 88 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*