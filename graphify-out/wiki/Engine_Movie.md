# Engine Movie

> 64 nodes · cohesion 0.08

## Key Concepts

- **DelayFrames** (143 connections) — `home/delay.asm`
- **engine/movie/trade.asm** (51 connections) — `engine/movie/trade.asm`
- **DelayFrame** (51 connections) — `home/vblank.asm`
- **EvolveMon** (15 connections) — `engine/movie/evolution.asm`
- **Trade_AnimLeftToRight** (12 connections) — `engine/movie/trade.asm`
- **Trade_AnimRightToLeft** (12 connections) — `engine/movie/trade.asm`
- **Trade_ShowEnemyMon** (11 connections) — `engine/movie/trade.asm`
- **Trade_AnimateBallEnteringLinkCable** (10 connections) — `engine/movie/trade.asm`
- **Trade_DrawOpenEndOfLinkCable** (10 connections) — `engine/movie/trade.asm`
- **Trade_ShowPlayerMon** (10 connections) — `engine/movie/trade.asm`
- **Trade_DrawLeftGameboy** (9 connections) — `engine/movie/trade.asm`
- **Trade_DrawRightGameboy** (9 connections) — `engine/movie/trade.asm`
- **Trade_ClearTileMap** (8 connections) — `engine/movie/trade.asm`
- **engine/movie/evolution.asm** (8 connections) — `engine/movie/evolution.asm`
- **CopyScreenTileBufferToVRAM** (8 connections) — `home/copy2.asm`
- **Trade_Delay80** (7 connections) — `engine/movie/trade.asm`
- **Trade_LoadMonSprite** (7 connections) — `engine/movie/trade.asm`
- **WriteOAMBlock** (7 connections) — `home/oam.asm`
- **PrintTradeFarewellText** (6 connections) — `engine/movie/trade.asm`
- **Trade_AnimMonMoveVertical** (6 connections) — `engine/movie/trade.asm`
- **Trade_CopyCableTilesOffScreen** (6 connections) — `engine/movie/trade.asm`
- **Trade_CopyTileMapToVRAM** (6 connections) — `engine/movie/trade.asm`
- **Trade_InitGameboyTransferGfx** (6 connections) — `engine/movie/trade.asm`
- **Trade_SlideTextBoxOffScreen** (6 connections) — `engine/movie/trade.asm`
- **LoadFlippedFrontSpriteByMonIndex** (6 connections) — `home/pokemon.asm`
- *... and 39 more nodes in this community*

## Relationships

- [Home](Home.md) (9 shared connections)
- [Scripts 13](Scripts_13.md) (8 shared connections)
- [Engine Menus](Engine_Menus.md) (7 shared connections)
- [Bank VRAM](Bank_VRAM.md) (6 shared connections)
- [Scripts](Scripts.md) (5 shared connections)
- [Engine Link](Engine_Link.md) (5 shared connections)
- [Scripts 15](Scripts_15.md) (4 shared connections)
- [Engine Pokemon](Engine_Pokemon.md) (3 shared connections)
- [Engine Events 3](Engine_Events_3.md) (2 shared connections)
- [Engine Items 2](Engine_Items_2.md) (1 shared connections)
- [Engine Battle 7](Engine_Battle_7.md) (1 shared connections)
- [Scripts 2](Scripts_2.md) (1 shared connections)

## Source Files

- `engine/battle/animations.asm`
- `engine/battle/scroll_draw_trainer_pic.asm`
- `engine/movie/evolution.asm`
- `engine/movie/intro.asm`
- `engine/movie/trade.asm`
- `home/copy2.asm`
- `home/delay.asm`
- `home/oam.asm`
- `home/pokemon.asm`
- `home/vblank.asm`

## Audit Trail

- EXTRACTED: 209 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*