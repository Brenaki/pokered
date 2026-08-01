# Engine Battle 9

> 21 nodes · cohesion 0.21

## Key Concepts

- **LoadPlayerBackPic** (12 connections) — `engine/battle/core.asm`
- **HoFLoadPlayerPics** (12 connections) — `engine/movie/hall_of_fame.asm`
- **sSpriteBuffer1** (12 connections) — `ram/sram.asm`
- **IntroDisplayPicCenteredOrUpperRight** (10 connections) — `engine/movie/oak_speech/oak_speech.asm`
- **InterlaceMergeSpriteBuffers** (10 connections) — `home/pics.asm`
- **ScaleSpriteByTwo** (9 connections) — `engine/battle/scale_sprites.asm`
- **home/pics.asm** (8 connections) — `home/pics.asm`
- **LoadUncompressedSpriteData** (8 connections) — `home/pics.asm`
- **sSpriteBuffer2** (8 connections) — `ram/sram.asm`
- **engine/battle/scale_sprites.asm** (7 connections) — `engine/battle/scale_sprites.asm`
- **UncompressSpriteFromDE** (7 connections) — `home/tilemap.asm`
- **sSpriteBuffer0** (7 connections) — `ram/sram.asm`
- **Sprite Buffers [SRAM]** (6 connections) — `ram/sram.asm`
- **RedPicBack** (5 connections) — `gfx/pics.asm`
- **ScalePixelsByTwo** (4 connections) — `engine/battle/scale_sprites.asm`
- **ScaleFirstThreeSpriteColumnsByTwo** (3 connections) — `engine/battle/scale_sprites.asm`
- **ScaleLastSpriteColumnByTwo** (3 connections) — `engine/battle/scale_sprites.asm`
- **DuplicateBitsTable** (2 connections) — `engine/battle/scale_sprites.asm`
- **gfx/player/redb.pic** (2 connections) — `gfx/pics.asm`
- **AlignSpriteDataCentered** (2 connections) — `home/pics.asm`
- **ZeroSpriteBuffer** (2 connections) — `home/pics.asm`

## Relationships

- [Bank VRAM](Bank_VRAM.md) (6 shared connections)
- [Home](Home.md) (3 shared connections)
- [Engine Pokemon](Engine_Pokemon.md) (2 shared connections)
- [Gfx Pics.Asm 4](Gfx_Pics.Asm_4.md) (1 shared connections)
- [Engine Battle 7](Engine_Battle_7.md) (1 shared connections)
- [Engine Movie 3](Engine_Movie_3.md) (1 shared connections)
- [Home 6](Home_6.md) (1 shared connections)
- [Ram](Ram.md) (1 shared connections)
- [Bank SRAM](Bank_SRAM.md) (1 shared connections)
- [Engine Menus](Engine_Menus.md) (1 shared connections)

## Source Files

- `engine/battle/core.asm`
- `engine/battle/scale_sprites.asm`
- `engine/movie/hall_of_fame.asm`
- `engine/movie/oak_speech/oak_speech.asm`
- `gfx/pics.asm`
- `home/pics.asm`
- `home/tilemap.asm`
- `ram/sram.asm`

## Audit Trail

- EXTRACTED: 63 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*