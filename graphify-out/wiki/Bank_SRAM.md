# Bank SRAM

> 72 nodes · cohesion 0.07

## Key Concepts

- **engine/menus/save.asm** (41 connections) — `engine/menus/save.asm`
- **ram/sram.asm** (24 connections) — `ram/sram.asm`
- **ChangeBox** (21 connections) — `engine/menus/save.asm`
- **LoadMainData** (21 connections) — `engine/menus/save.asm`
- **SaveMainData** (17 connections) — `engine/menus/save.asm`
- **SaveMenu** (16 connections) — `engine/menus/save.asm`
- **LoadPartyAndDexData** (15 connections) — `engine/menus/save.asm`
- **SavePartyAndDexData** (13 connections) — `engine/menus/save.asm`
- **TryLoadSaveFile** (13 connections) — `engine/menus/save.asm`
- **LoadCurrentBoxData** (12 connections) — `engine/menus/save.asm`
- **PrepareOakSpeech** (12 connections) — `engine/movie/oak_speech/oak_speech.asm`
- **CalcCheckSum** (11 connections) — `engine/menus/save.asm`
- **DisplayChangeBoxMenu** (11 connections) — `engine/menus/save.asm`
- **Save Data [SRAM]** (11 connections) — `ram/sram.asm`
- **SaveCurrentBoxData** (9 connections) — `engine/menus/save.asm`
- **sGameData** (9 connections) — `ram/sram.asm`
- **sGameDataEnd** (9 connections) — `ram/sram.asm`
- **wBoxDataEnd** (9 connections) — `ram/wram.asm`
- **CopyBoxToOrFromSRAM** (7 connections) — `engine/menus/save.asm`
- **SaveGameData** (7 connections) — `engine/menus/save.asm`
- **sMainData** (7 connections) — `ram/sram.asm`
- **wBoxDataStart** (7 connections) — `ram/wram.asm`
- **CalcIndividualBoxCheckSums** (6 connections) — `engine/menus/save.asm`
- **CheckPreviousSaveFile** (6 connections) — `engine/menus/save.asm`
- **EmptySRAMBoxesInBank** (6 connections) — `engine/menus/save.asm`
- *... and 47 more nodes in this community*

## Relationships

- [Bank WRAM0](Bank_WRAM0.md) (14 shared connections)
- [Scripts](Scripts.md) (8 shared connections)
- [Home](Home.md) (7 shared connections)
- [Engine Overworld](Engine_Overworld.md) (6 shared connections)
- [Ram](Ram.md) (4 shared connections)
- [Engine Movie](Engine_Movie.md) (4 shared connections)
- [Bank VRAM](Bank_VRAM.md) (4 shared connections)
- [Engine Pokemon 2](Engine_Pokemon_2.md) (2 shared connections)
- [Bank HRAM](Bank_HRAM.md) (2 shared connections)
- [Engine Link](Engine_Link.md) (2 shared connections)
- [Bank ROM0](Bank_ROM0.md) (1 shared connections)
- [Engine Movie 2](Engine_Movie_2.md) (1 shared connections)

## Source Files

- `engine/menus/main_menu.asm`
- `engine/menus/save.asm`
- `engine/movie/oak_speech/oak_speech.asm`
- `home/predef_text.asm`
- `ram/sram.asm`
- `ram/wram.asm`

## Audit Trail

- EXTRACTED: 244 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*