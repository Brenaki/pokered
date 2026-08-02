# Bank VRAM

> 83 nodes · cohesion 0.04

## Key Concepts

- **PlayCry** (43 connections) — `home/pokemon.asm`
- **5. Visao arquitetural** (42 connections) — `docs/004-2026-08-01-Audio_Musicas_Efeitos_Sonoros_e_Sprites.md`
- **ram/vram.asm** (20 connections) — `ram/vram.asm`
- **LoadTradingGFXAndMonNames** (19 connections) — `engine/movie/trade.asm`
- **VBlank** (19 connections) — `home/vblank.asm`
- **home/vcopy.asm** (18 connections) — `home/vcopy.asm`
- **DisableLCD** (18 connections) — `home/lcd.asm`
- **vSprites** (18 connections) — `ram/vram.asm`
- **SlidePlayerAndEnemySilhouettesOnScreen** (17 connections) — `engine/battle/core.asm`
- **LoadSlotMachineTiles** (17 connections) — `engine/slots/slot_machine.asm`
- **AnimationShakeEnemyHUD** (16 connections) — `engine/battle/animations.asm`
- **LoadMapData** (16 connections) — `home/overworld.asm`
- **vFrontPic** (16 connections) — `ram/vram.asm`
- **VRAM [VRAM]** (16 connections) — `ram/vram.asm`
- **8.1 Estado logico, viewport e VRAM** (14 connections) — `docs/004-2026-08-01-Audio_Musicas_Efeitos_Sonoros_e_Sprites.md`
- **vChars1** (13 connections) — `ram/vram.asm`
- **LoadMonBackPic** (12 connections) — `engine/battle/core.asm`
- **GetCryData** (11 connections) — `home/pokemon.asm`
- **vBGMap0** (11 connections) — `ram/vram.asm`
- **vBackPic** (10 connections) — `ram/vram.asm`
- **engine/gfx** (8 connections)
- **CopyGfxToSuperNintendoVRAM** (8 connections) — `engine/gfx/palettes.asm`
- **PrepareOAMData** (8 connections) — `engine/gfx/sprite_oam.asm`
- **MarowakAnim** (7 connections) — `engine/battle/ghost_marowak_anim.asm`
- **home/vblank.asm** (7 connections) — `home/vblank.asm`
- *... and 58 more nodes in this community*

## Relationships

- [Engine Menus](Engine_Menus.md) (13 shared connections)
- [Engine Link](Engine_Link.md) (10 shared connections)
- [Home](Home.md) (10 shared connections)
- [Scripts 11](Scripts_11.md) (9 shared connections)
- [Engine Slots](Engine_Slots.md) (8 shared connections)
- [Engine Battle](Engine_Battle.md) (7 shared connections)
- [Engine Movie 3](Engine_Movie_3.md) (6 shared connections)
- [Engine Pokemon](Engine_Pokemon.md) (6 shared connections)
- [Engine Battle 11](Engine_Battle_11.md) (5 shared connections)
- [Data Sgb](Data_Sgb.md) (5 shared connections)
- [Bank WRAM0](Bank_WRAM0.md) (4 shared connections)
- [Engine Items 2](Engine_Items_2.md) (4 shared connections)

## Source Files

- `data/pokemon/cries.asm`
- `docs/004-2026-08-01-Audio_Musicas_Efeitos_Sonoros_e_Sprites.md`
- `engine/battle/animations.asm`
- `engine/battle/core.asm`
- `engine/battle/ghost_marowak_anim.asm`
- `engine/gfx/load_pokedex_tiles.asm`
- `engine/gfx/oam_dma.asm`
- `engine/gfx/palettes.asm`
- `engine/gfx/sprite_oam.asm`
- `engine/movie/trade.asm`
- `engine/slots/slot_machine.asm`
- `gfx/slots/blue_slots_2.2bpp`
- `gfx/slots/red_slots_2.2bpp`
- `gfx/tilesets/flower/flower1.2bpp`
- `gfx/tilesets/flower/flower2.2bpp`
- `gfx/tilesets/flower/flower3.2bpp`
- `gfx/trade.asm`
- `gfx/trade/cable_ball.2bpp`
- `gfx/trade/game_boy.2bpp`
- `gfx/trade/link_cable.2bpp`

## Audit Trail

- EXTRACTED: 283 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*