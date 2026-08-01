# Engine Overworld

> 76 nodes · cohesion 0.05

## Key Concepts

- **DelayFrames** (143 connections) — `home/delay.asm`
- **engine/overworld/player_animations.asm** (28 connections) — `engine/overworld/player_animations.asm`
- **GetPredefRegisters** (27 connections) — `home/predef.asm`
- **wPlayerName** (25 connections) — `ram/wram.asm`
- **EnterMapAnim** (24 connections) — `engine/overworld/player_animations.asm`
- **_LeaveMapAnim** (21 connections) — `engine/overworld/player_animations.asm`
- **FishingAnim** (19 connections) — `engine/overworld/player_animations.asm`
- **UpdateHPBar2** (17 connections) — `engine/gfx/hp_bar.asm`
- **engine/gfx/hp_bar.asm** (13 connections) — `engine/gfx/hp_bar.asm`
- **PrintSaveScreenText** (12 connections) — `engine/menus/main_menu.asm`
- **HealEffect_** (11 connections) — `engine/battle/move_effects/heal.asm`
- **DisplayContinueGameInfo** (10 connections) — `engine/menus/main_menu.asm`
- **DrainHPEffect_** (9 connections) — `engine/battle/move_effects/drain_hp.asm`
- **GetHPBarLength** (7 connections) — `engine/gfx/hp_bar.asm`
- **PrintNumBadges** (7 connections) — `engine/menus/main_menu.asm`
- **PrintNumOwnedMons** (7 connections) — `engine/menus/main_menu.asm`
- **DrawHP** (7 connections) — `engine/pokemon/status_screen.asm`
- **PrintPlayTime** (6 connections) — `engine/menus/main_menu.asm`
- **InitFacingDirectionList** (6 connections) — `engine/overworld/player_animations.asm`
- **PlayerSpinInPlace** (6 connections) — `engine/overworld/player_animations.asm`
- **engine/battle/move_effects/heal.asm** (6 connections) — `engine/battle/move_effects/heal.asm`
- **wFacingDirectionList** (6 connections) — `ram/wram.asm`
- **wHPBarOldHP** (6 connections) — `ram/wram.asm`
- **RecoilEffect_** (5 connections) — `engine/battle/move_effects/recoil.asm`
- **UpdateHPBar_PrintHPNumber** (5 connections) — `engine/gfx/hp_bar.asm`
- *... and 51 more nodes in this community*

## Relationships

- [Home](Home.md) (9 shared connections)
- [Bank VRAM](Bank_VRAM.md) (8 shared connections)
- [Engine Link](Engine_Link.md) (7 shared connections)
- [Bank WRAM0](Bank_WRAM0.md) (6 shared connections)
- [Scripts](Scripts.md) (6 shared connections)
- [Engine Battle 2](Engine_Battle_2.md) (5 shared connections)
- [Engine Battle](Engine_Battle.md) (4 shared connections)
- [Engine Movie 2](Engine_Movie_2.md) (4 shared connections)
- [Ram](Ram.md) (4 shared connections)
- [Scripts 5](Scripts_5.md) (4 shared connections)
- [Home 6](Home_6.md) (3 shared connections)
- [Home 2](Home_2.md) (2 shared connections)

## Source Files

- `data/tilesets/warp_pad_hole_tile_ids.asm`
- `engine/battle/animations.asm`
- `engine/battle/move_effects/drain_hp.asm`
- `engine/battle/move_effects/heal.asm`
- `engine/battle/move_effects/recoil.asm`
- `engine/gfx/hp_bar.asm`
- `engine/gfx/screen_effects.asm`
- `engine/menus/main_menu.asm`
- `engine/menus/swap_items.asm`
- `engine/overworld/player_animations.asm`
- `engine/pokemon/status_screen.asm`
- `home/delay.asm`
- `home/pokemon.asm`
- `home/predef.asm`
- `ram/wram.asm`

## Audit Trail

- EXTRACTED: 213 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*