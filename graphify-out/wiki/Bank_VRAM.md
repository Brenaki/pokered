# Bank VRAM

> 132 nodes · cohesion 0.03

## Key Concepts

- **DisplayTitleScreen** (47 connections) — `engine/movie/title.asm`
- **CopyVideoData** (36 connections) — `home/copy2.asm`
- **gfx/font.asm** (24 connections) — `gfx/font.asm`
- **LoadTextBoxTilePatterns** (24 connections) — `home/load_font.asm`
- **engine/movie/title.asm** (20 connections) — `engine/movie/title.asm`
- **LoadTradingGFXAndMonNames** (19 connections) — `engine/movie/trade.asm`
- **vChars2** (19 connections) — `ram/vram.asm`
- **ram/vram.asm** (17 connections) — `ram/vram.asm`
- **LoadHpBarAndStatusTilePatterns** (17 connections) — `home/load_font.asm`
- **vSprites** (17 connections) — `ram/vram.asm`
- **AnimationShakeEnemyHUD** (16 connections) — `engine/battle/animations.asm`
- **VRAM [VRAM]** (16 connections) — `ram/vram.asm`
- **vChars1** (13 connections) — `ram/vram.asm`
- **LoadHudTilePatterns** (12 connections) — `engine/battle/core.asm`
- **LoadMonBackPic** (12 connections) — `engine/battle/core.asm`
- **AnimateHealingMachine** (12 connections) — `engine/overworld/healing_machine.asm`
- **engine/overworld/cut.asm** (12 connections) — `engine/overworld/cut.asm`
- **vFrontPic** (12 connections) — `ram/vram.asm`
- **vBGMap0** (11 connections) — `ram/vram.asm`
- **gfx** (10 connections)
- **AnimationWavyScreen** (10 connections) — `engine/battle/animations.asm`
- **vBGMap1** (10 connections) — `ram/vram.asm`
- **DrawPlayerCharacter** (9 connections) — `engine/movie/title.asm`
- **engine/movie/title2.asm** (9 connections) — `engine/movie/title2.asm`
- **engine/overworld/dust_smoke.asm** (9 connections) — `engine/overworld/dust_smoke.asm`
- *... and 107 more nodes in this community*

## Relationships

- [Home 2](Home_2.md) (27 shared connections)
- [Engine Menus](Engine_Menus.md) (14 shared connections)
- [Engine Movie](Engine_Movie.md) (9 shared connections)
- [Home](Home.md) (9 shared connections)
- [Engine Pokemon](Engine_Pokemon.md) (7 shared connections)
- [Engine Menus 3](Engine_Menus_3.md) (6 shared connections)
- [Engine Menus 2](Engine_Menus_2.md) (4 shared connections)
- [Engine Battle 17](Engine_Battle_17.md) (3 shared connections)
- [Engine Link](Engine_Link.md) (3 shared connections)
- [Engine Battle 8](Engine_Battle_8.md) (2 shared connections)
- [Engine Battle 3](Engine_Battle_3.md) (2 shared connections)
- [Engine Battle 14](Engine_Battle_14.md) (2 shared connections)

## Source Files

- `.github/workflows/main.yml`
- `data/pokemon/title_mons.asm`
- `data/tilesets/cut_tree_blocks.asm`
- `engine/battle/animations.asm`
- `engine/battle/core.asm`
- `engine/battle/ghost_marowak_anim.asm`
- `engine/gfx/load_pokedex_tiles.asm`
- `engine/gfx/palettes.asm`
- `engine/movie/title.asm`
- `engine/movie/title2.asm`
- `engine/movie/trade.asm`
- `engine/overworld/cut.asm`
- `engine/overworld/dust_smoke.asm`
- `engine/overworld/healing_machine.asm`
- `gfx/font.asm`
- `gfx/trade.asm`
- `gfx/version.asm`
- `home/copy2.asm`
- `home/load_font.asm`
- `home/pics.asm`

## Audit Trail

- EXTRACTED: 341 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*