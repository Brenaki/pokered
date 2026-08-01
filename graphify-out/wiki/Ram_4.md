# Ram 4

> 19 nodes · cohesion 0.12

## Key Concepts

- **LoadMapHeader** (20 connections) — `home/overworld.asm`
- **MarkTownVisitedAndLoadToggleableObjects** (8 connections) — `engine/overworld/toggleable_objects.asm`
- **IsSpriteOrSignInFrontOfPlayer** (7 connections) — `home/overworld.asm`
- **data/maps/toggleable_objects.asm** (5 connections) — `data/maps/toggleable_objects.asm`
- **wSignCoords** (4 connections) — `ram/wram.asm`
- **wSignTextIDs** (4 connections) — `ram/wram.asm`
- **ToggleableObjectMapPointers** (3 connections) — `data/maps/toggleable_objects.asm`
- **ToggleableObjectStates** (3 connections) — `data/maps/toggleable_objects.asm`
- **IsSpriteInFrontOfPlayer2** (3 connections) — `home/overworld.asm`
- **wCurMapHeader** (3 connections) — `ram/wram.asm`
- **wEastConnectionHeader** (3 connections) — `ram/wram.asm`
- **wMapBackgroundTile** (3 connections) — `ram/wram.asm`
- **wNorthConnectionHeader** (3 connections) — `ram/wram.asm`
- **wSouthConnectionHeader** (3 connections) — `ram/wram.asm`
- **wTilesetTalkingOverTiles** (3 connections) — `ram/wram.asm`
- **wTownVisitedFlag** (3 connections) — `ram/wram.asm`
- **wWestConnectionHeader** (3 connections) — `ram/wram.asm`
- **NoToggleData** (2 connections) — `data/maps/toggleable_objects.asm`
- **CopyMapConnectionHeader** (2 connections) — `home/overworld.asm`

## Relationships

- [Bank WRAM0](Bank_WRAM0.md) (1 shared connections)
- [Engine Battle 2](Engine_Battle_2.md) (1 shared connections)
- [Scripts 19](Scripts_19.md) (1 shared connections)
- [Scripts 5](Scripts_5.md) (1 shared connections)
- [Data Maps 6](Data_Maps_6.md) (1 shared connections)
- [Bank ROM0](Bank_ROM0.md) (1 shared connections)
- [Data Tilesets 2](Data_Tilesets_2.md) (1 shared connections)
- [Home](Home.md) (1 shared connections)
- [Home 5](Home_5.md) (1 shared connections)
- [Engine Overworld 4](Engine_Overworld_4.md) (1 shared connections)
- [Home 2](Home_2.md) (1 shared connections)

## Source Files

- `data/maps/toggleable_objects.asm`
- `engine/overworld/toggleable_objects.asm`
- `home/overworld.asm`
- `ram/wram.asm`

## Audit Trail

- EXTRACTED: 32 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*