# Engine Movie 2

> 63 nodes · cohesion 0.05

## Key Concepts

- **engine/movie/intro.asm** (35 connections) — `engine/movie/intro.asm`
- **engine/movie/splash.asm** (19 connections) — `engine/movie/splash.asm`
- **PlayIntroScene** (16 connections) — `engine/movie/intro.asm`
- **PlayShootingStar** (15 connections) — `engine/movie/intro.asm`
- **LoadIntroGraphics** (12 connections) — `engine/movie/intro.asm`
- **LoadShootingStarGraphics** (12 connections) — `engine/movie/splash.asm`
- **AnimateShootingStar** (11 connections) — `engine/movie/splash.asm`
- **CheckForUserInterruption** (8 connections) — `home/overworld.asm`
- **PlayIntro** (7 connections) — `engine/movie/intro.asm`
- **SmallStarsWaveCoordsPointerTable** (7 connections) — `engine/movie/splash.asm`
- **IntroDrawBlackBars** (5 connections) — `engine/movie/intro.asm`
- **MoveAnimationTiles1** (4 connections) — `engine/battle/animations.asm`
- **AnimateIntroNidorino** (4 connections) — `engine/movie/intro.asm`
- **FightIntroFrontMon** (4 connections) — `engine/movie/intro.asm`
- **GameFreakIntro** (4 connections) — `engine/movie/intro.asm`
- **IntroClearScreen** (4 connections) — `engine/movie/intro.asm`
- **IntroMoveMon** (4 connections) — `engine/movie/intro.asm`
- **UpdateIntroNidorinoOAM** (4 connections) — `engine/movie/intro.asm`
- **FightIntroBackMon** (3 connections) — `engine/movie/intro.asm`
- **FightIntroFrontMon2** (3 connections) — `engine/movie/intro.asm`
- **FightIntroFrontMon3** (3 connections) — `engine/movie/intro.asm`
- **InitIntroNidorinoOAM** (3 connections) — `engine/movie/intro.asm`
- **FallingStar** (3 connections) — `engine/movie/splash.asm`
- **MoveDownSmallStars** (3 connections) — `engine/movie/splash.asm`
- **FightIntroBackMonEnd** (2 connections) — `engine/movie/intro.asm`
- *... and 38 more nodes in this community*

## Relationships

- [Engine Items 2](Engine_Items_2.md) (5 shared connections)
- [Engine Movie 3](Engine_Movie_3.md) (5 shared connections)
- [Engine Menus](Engine_Menus.md) (5 shared connections)
- [Bank VRAM](Bank_VRAM.md) (4 shared connections)
- [Engine Battle](Engine_Battle.md) (3 shared connections)
- [Scripts 11](Scripts_11.md) (3 shared connections)
- [Engine Link](Engine_Link.md) (2 shared connections)
- [Home](Home.md) (2 shared connections)
- [Engine Pokemon](Engine_Pokemon.md) (2 shared connections)
- [Engine Menus 3](Engine_Menus_3.md) (1 shared connections)
- [Engine Menus 2](Engine_Menus_2.md) (1 shared connections)
- [Engine Movie](Engine_Movie.md) (1 shared connections)

## Source Files

- `engine/battle/animations.asm`
- `engine/movie/intro.asm`
- `engine/movie/splash.asm`
- `gfx/battle/move_anim_1.2bpp`
- `gfx/intro/blue_jigglypuff_1.2bpp`
- `gfx/intro/blue_jigglypuff_2.2bpp`
- `gfx/intro/blue_jigglypuff_3.2bpp`
- `gfx/intro/gengar.2bpp`
- `gfx/intro/red_nidorino_1.2bpp`
- `gfx/intro/red_nidorino_2.2bpp`
- `gfx/intro/red_nidorino_3.2bpp`
- `gfx/splash/falling_star.2bpp`
- `gfx/splash/gamefreak_logo.2bpp`
- `gfx/splash/gamefreak_presents.2bpp`
- `home/overworld.asm`

## Audit Trail

- EXTRACTED: 141 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*