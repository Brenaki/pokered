# Engine Overworld 5

> 20 nodes · cohesion 0.14

## Key Concepts

- **engine/overworld/map_sprites.asm** (9 connections) — `engine/overworld/map_sprites.asm`
- **LoadMapSpriteTilePatterns** (8 connections) — `engine/overworld/map_sprites.asm`
- **InitOutsideMapSprites** (7 connections) — `engine/overworld/map_sprites.asm`
- **PrepareOAMData** (5 connections) — `engine/gfx/sprite_oam.asm`
- **data/maps/sprite_sets.asm** (5 connections) — `data/maps/sprite_sets.asm`
- **GetSplitMapSpriteSetID** (4 connections) — `engine/overworld/map_sprites.asm`
- **engine/gfx/sprite_oam.asm** (4 connections) — `engine/gfx/sprite_oam.asm`
- **data/sprites** (3 connections)
- **data/sprites/facings.asm** (3 connections) — `data/sprites/facings.asm`
- **data/sprites/sprites.asm** (3 connections) — `data/sprites/sprites.asm`
- **HideSprites** (3 connections) — `home/clear_sprites.asm`
- **wSpriteSet** (3 connections) — `ram/wram.asm`
- **wXCoord** (3 connections) — `ram/wram.asm`
- **MapSpriteSets** (2 connections) — `data/maps/sprite_sets.asm`
- **SplitMapSpriteSets** (2 connections) — `data/maps/sprite_sets.asm`
- **SpriteSets** (2 connections) — `data/maps/sprite_sets.asm`
- **SpriteFacingAndAnimationTable** (2 connections) — `data/sprites/facings.asm`
- **SpriteSheetPointerTable** (2 connections) — `data/sprites/sprites.asm`
- **GetSpriteScreenXY** (2 connections) — `engine/gfx/sprite_oam.asm`
- **ReadSpriteSheetData** (2 connections) — `engine/overworld/map_sprites.asm`

## Relationships

- [Bank VRAM](Bank_VRAM.md) (2 shared connections)
- [Home](Home.md) (2 shared connections)
- [Engine Menus 3](Engine_Menus_3.md) (1 shared connections)

## Source Files

- `data/maps/sprite_sets.asm`
- `data/sprites/facings.asm`
- `data/sprites/sprites.asm`
- `engine/gfx/sprite_oam.asm`
- `engine/overworld/map_sprites.asm`
- `home/clear_sprites.asm`
- `ram/wram.asm`

## Audit Trail

- EXTRACTED: 32 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*