# Engine Gfx 3

> 7 nodes · cohesion 0.33

## Key Concepts

- **PrepareOAMData** (5 connections) — `engine/gfx/sprite_oam.asm`
- **engine/gfx/sprite_oam.asm** (4 connections) — `engine/gfx/sprite_oam.asm`
- **data/sprites** (3 connections)
- **data/sprites/facings.asm** (3 connections) — `data/sprites/facings.asm`
- **HideSprites** (3 connections) — `home/clear_sprites.asm`
- **SpriteFacingAndAnimationTable** (2 connections) — `data/sprites/facings.asm`
- **GetSpriteScreenXY** (2 connections) — `engine/gfx/sprite_oam.asm`

## Relationships

- [Engine Overworld 5](Engine_Overworld_5.md) (1 shared connections)

## Source Files

- `data/sprites/facings.asm`
- `engine/gfx/sprite_oam.asm`
- `home/clear_sprites.asm`

## Audit Trail

- EXTRACTED: 8 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*