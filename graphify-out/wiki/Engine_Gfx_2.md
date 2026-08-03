# Engine Gfx 2

> 23 nodes · cohesion 0.13

## Key Concepts

- **GetPredefRegisters** (27 connections) — `home/predef.asm`
- **UpdateHPBar2** (17 connections) — `engine/gfx/hp_bar.asm`
- **engine/gfx/hp_bar.asm** (13 connections) — `engine/gfx/hp_bar.asm`
- **engine/gfx** (8 connections)
- **DrawHP** (7 connections) — `engine/pokemon/status_screen.asm`
- **UpdateHPBar_PrintHPNumber** (5 connections) — `engine/gfx/hp_bar.asm`
- **PredefShakeScreenHorizontally** (5 connections) — `engine/gfx/screen_effects.asm`
- **engine/gfx/screen_effects.asm** (5 connections) — `engine/gfx/screen_effects.asm`
- **UpdateHPBar_AnimateHPBar** (4 connections) — `engine/gfx/hp_bar.asm`
- **UpdateHPBar_CalcOldNewHPBarPixels** (4 connections) — `engine/gfx/hp_bar.asm`
- **ChangeBGPalColor0_4Frames** (4 connections) — `engine/gfx/screen_effects.asm`
- **LoadMovePPs** (4 connections) — `engine/pokemon/add_mon.asm`
- **DrawHPBar** (4 connections) — `home/pokemon.asm`
- **DoRockSlideSpecialEffects** (3 connections) — `engine/battle/animations.asm`
- **HPBarLength** (3 connections) — `engine/gfx/hp_bar.asm`
- **PredefShakeScreenVertically** (3 connections) — `engine/gfx/screen_effects.asm`
- **Diploma_TextBoxBorder** (3 connections) — `engine/link/cable_club.asm`
- **DisplayPicCenteredOrUpperRight** (3 connections) — `engine/movie/oak_speech/oak_speech.asm`
- **DrawHP2** (3 connections) — `engine/pokemon/status_screen.asm`
- **engine/gfx/load_pokedex_tiles.asm** (3 connections) — `engine/gfx/load_pokedex_tiles.asm`
- **UpdateHPBar_CalcHPDifference** (2 connections) — `engine/gfx/hp_bar.asm`
- **UpdateHPBar_CompareNewHPToOldHP** (2 connections) — `engine/gfx/hp_bar.asm`
- **UpdateHPBar** (1 connections) — `engine/gfx/hp_bar.asm`

## Relationships

- [Bank VRAM](Bank_VRAM.md) (5 shared connections)
- [Ram](Ram.md) (3 shared connections)
- [Scripts 6](Scripts_6.md) (2 shared connections)
- [Engine Battle](Engine_Battle.md) (2 shared connections)
- [Bank WRAM0](Bank_WRAM0.md) (2 shared connections)
- [Engine Gfx](Engine_Gfx.md) (1 shared connections)
- [Data Sgb](Data_Sgb.md) (1 shared connections)
- [Engine Battle 3](Engine_Battle_3.md) (1 shared connections)
- [Engine Movie 2](Engine_Movie_2.md) (1 shared connections)
- [Engine Movie](Engine_Movie.md) (1 shared connections)

## Source Files

- `engine/battle/animations.asm`
- `engine/gfx/hp_bar.asm`
- `engine/gfx/load_pokedex_tiles.asm`
- `engine/gfx/screen_effects.asm`
- `engine/link/cable_club.asm`
- `engine/movie/oak_speech/oak_speech.asm`
- `engine/pokemon/add_mon.asm`
- `engine/pokemon/status_screen.asm`
- `home/pokemon.asm`
- `home/predef.asm`

## Audit Trail

- EXTRACTED: 52 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*