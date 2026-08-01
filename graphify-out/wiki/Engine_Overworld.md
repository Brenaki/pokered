# Engine Overworld

> 71 nodes · cohesion 0.04

## Key Concepts

- **engine/overworld** (30 connections)
- **data/tilesets** (16 connections)
- **LoadSpecialWarpData** (14 connections) — `engine/overworld/special_warps.asm`
- **engine/overworld/cut.asm** (12 connections) — `engine/overworld/cut.asm`
- **data/maps/special_warps.asm** (10 connections) — `data/maps/special_warps.asm`
- **LoadTilesetHeader** (9 connections) — `engine/overworld/tilesets.asm`
- **engine/overworld/dust_smoke.asm** (9 connections) — `engine/overworld/dust_smoke.asm`
- **LoadSpinnerArrowTiles** (8 connections) — `engine/overworld/spinners.asm`
- **engine/overworld/ledges.asm** (8 connections) — `engine/overworld/ledges.asm`
- **InitCutAnimOAM** (7 connections) — `engine/overworld/cut.asm`
- **LoadHoppingShadowOAM** (7 connections) — `engine/overworld/ledges.asm`
- **AnimateBoulderDust** (6 connections) — `engine/overworld/dust_smoke.asm`
- **IsPlayerStandingOnDoorTileOrWarpTile** (6 connections) — `engine/overworld/player_state.asm`
- **engine/overworld/spinners.asm** (6 connections) — `engine/overworld/spinners.asm`
- **wCurrentTileBlockMapViewPointer** (6 connections) — `ram/wram.asm`
- **PlayerStepOutFromDoor** (5 connections) — `engine/overworld/auto_movement.asm`
- **WriteCutOrBoulderDustAnimationOAMBlock** (5 connections) — `engine/overworld/cut.asm`
- **IsPlayerStandingOnDoorTile** (5 connections) — `engine/overworld/doors.asm`
- **LoadSmokeTileFourTimes** (5 connections) — `engine/overworld/dust_smoke.asm`
- **data/tilesets/spinner_tiles.asm** (5 connections) — `data/tilesets/spinner_tiles.asm`
- **engine/overworld/special_warps.asm** (5 connections) — `engine/overworld/special_warps.asm`
- **engine/overworld/tilesets.asm** (5 connections) — `engine/overworld/tilesets.asm`
- **GetCutOrBoulderDustAnimationOffsets** (4 connections) — `engine/overworld/cut.asm`
- **LoadCutGrassAnimationTilePattern** (4 connections) — `engine/overworld/cut.asm`
- **LoadSmokeTile** (4 connections) — `engine/overworld/dust_smoke.asm`
- *... and 46 more nodes in this community*

## Relationships

- [Home](Home.md) (10 shared connections)
- [Bank VRAM](Bank_VRAM.md) (9 shared connections)
- [Engine Overworld 3](Engine_Overworld_3.md) (4 shared connections)
- [Scripts 6](Scripts_6.md) (3 shared connections)
- [Engine Movie 3](Engine_Movie_3.md) (3 shared connections)
- [Engine Overworld 2](Engine_Overworld_2.md) (3 shared connections)
- [Engine Battle](Engine_Battle.md) (3 shared connections)
- [Engine Movie 5](Engine_Movie_5.md) (2 shared connections)
- [Scripts 2](Scripts_2.md) (2 shared connections)
- [Engine Menus](Engine_Menus.md) (2 shared connections)
- [Scripts 5](Scripts_5.md) (1 shared connections)
- [Data Tilesets](Data_Tilesets.md) (1 shared connections)

## Source Files

- `data/maps/special_warps.asm`
- `data/tilesets/cut_tree_blocks.asm`
- `data/tilesets/door_tile_ids.asm`
- `data/tilesets/dungeon_tilesets.asm`
- `data/tilesets/ledge_tiles.asm`
- `data/tilesets/spinner_tiles.asm`
- `data/tilesets/tileset_headers.asm`
- `data/tilesets/warp_tile_ids.asm`
- `engine/overworld/auto_movement.asm`
- `engine/overworld/clear_variables.asm`
- `engine/overworld/cut.asm`
- `engine/overworld/doors.asm`
- `engine/overworld/dust_smoke.asm`
- `engine/overworld/is_player_just_outside_map.asm`
- `engine/overworld/ledges.asm`
- `engine/overworld/player_state.asm`
- `engine/overworld/special_warps.asm`
- `engine/overworld/spinners.asm`
- `engine/overworld/tilesets.asm`
- `home/overworld.asm`

## Audit Trail

- EXTRACTED: 164 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*