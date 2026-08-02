# Engine Battle 11

> 22 nodes · cohesion 0.20

## Key Concepts

- **LoadPlayerBackPic** (12 connections) — `engine/battle/core.asm`
- **HoFLoadPlayerPics** (12 connections) — `engine/movie/hall_of_fame.asm`
- **sSpriteBuffer1** (12 connections) — `ram/sram.asm`
- **ScaleSpriteByTwo** (10 connections) — `engine/battle/scale_sprites.asm`
- **IntroDisplayPicCenteredOrUpperRight** (10 connections) — `engine/movie/oak_speech/oak_speech.asm`
- **home/pics.asm** (10 connections) — `home/pics.asm`
- **InterlaceMergeSpriteBuffers** (10 connections) — `home/pics.asm`
- **LoadUncompressedSpriteData** (9 connections) — `home/pics.asm`
- **sSpriteBuffer2** (8 connections) — `ram/sram.asm`
- **engine/battle/scale_sprites.asm** (7 connections) — `engine/battle/scale_sprites.asm`
- **UncompressSpriteFromDE** (7 connections) — `home/tilemap.asm`
- **sSpriteBuffer0** (7 connections) — `ram/sram.asm`
- **_LoadTrainerPic** (6 connections) — `engine/battle/core.asm`
- **Sprite Buffers [SRAM]** (6 connections) — `ram/sram.asm`
- **RedPicBack** (5 connections) — `gfx/pics.asm`
- **ScalePixelsByTwo** (4 connections) — `engine/battle/scale_sprites.asm`
- **ScaleFirstThreeSpriteColumnsByTwo** (3 connections) — `engine/battle/scale_sprites.asm`
- **ScaleLastSpriteColumnByTwo** (3 connections) — `engine/battle/scale_sprites.asm`
- **DuplicateBitsTable** (2 connections) — `engine/battle/scale_sprites.asm`
- **gfx/player/redb.pic** (2 connections) — `gfx/player/redb.pic`
- **AlignSpriteDataCentered** (2 connections) — `home/pics.asm`
- **ZeroSpriteBuffer** (2 connections) — `home/pics.asm`

## Relationships

- [Bank VRAM](Bank_VRAM.md) (6 shared connections)
- [Ram 8](Ram_8.md) (3 shared connections)
- [Engine Link](Engine_Link.md) (2 shared connections)
- [Engine Pokemon](Engine_Pokemon.md) (2 shared connections)
- [Gfx Pics.Asm 3](Gfx_Pics.Asm_3.md) (1 shared connections)
- [Engine Items 2](Engine_Items_2.md) (1 shared connections)
- [Home 6](Home_6.md) (1 shared connections)
- [Ram](Ram.md) (1 shared connections)
- [Bank SRAM](Bank_SRAM.md) (1 shared connections)
- [Engine Menus 5](Engine_Menus_5.md) (1 shared connections)

## Source Files

- `engine/battle/core.asm`
- `engine/battle/scale_sprites.asm`
- `engine/movie/hall_of_fame.asm`
- `engine/movie/oak_speech/oak_speech.asm`
- `gfx/pics.asm`
- `gfx/player/redb.pic`
- `home/pics.asm`
- `home/tilemap.asm`
- `ram/sram.asm`

## Audit Trail

- EXTRACTED: 66 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*