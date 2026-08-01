# Engine Battle 13

> 22 nodes · cohesion 0.14

## Key Concepts

- **DrawPlayerHUDAndHPBar** (19 connections) — `engine/battle/core.asm`
- **DrawEnemyHUDAndHPBar** (17 connections) — `engine/battle/core.asm`
- **UpdateHPBar2** (17 connections) — `engine/gfx/hp_bar.asm`
- **engine/gfx/hp_bar.asm** (11 connections) — `engine/gfx/hp_bar.asm`
- **DrainHPEffect_** (9 connections) — `engine/battle/move_effects/drain_hp.asm`
- **RecoilEffect_** (5 connections) — `engine/battle/move_effects/recoil.asm`
- **GetHPBarLength** (5 connections) — `engine/gfx/hp_bar.asm`
- **UpdateHPBar_PrintHPNumber** (5 connections) — `engine/gfx/hp_bar.asm`
- **engine/battle/move_effects/drain_hp.asm** (5 connections) — `engine/battle/move_effects/drain_hp.asm`
- **wBattleMonNick** (5 connections) — `ram/wram.asm`
- **UpdateHPBar_AnimateHPBar** (4 connections) — `engine/gfx/hp_bar.asm`
- **UpdateHPBar_CalcOldNewHPBarPixels** (4 connections) — `engine/gfx/hp_bar.asm`
- **engine/battle/move_effects/recoil.asm** (4 connections) — `engine/battle/move_effects/recoil.asm`
- **DrawHPBar** (4 connections) — `home/pokemon.asm`
- **PrintStatusConditionNotFainted** (4 connections) — `home/pokemon.asm`
- **CenterMonName** (3 connections) — `engine/battle/core.asm`
- **DreamWasEatenText** (2 connections) — `engine/battle/move_effects/drain_hp.asm`
- **SuckedHealthText** (2 connections) — `engine/battle/move_effects/drain_hp.asm`
- **HitWithRecoilText** (2 connections) — `engine/battle/move_effects/recoil.asm`
- **UpdateHPBar_CalcHPDifference** (2 connections) — `engine/gfx/hp_bar.asm`
- **UpdateHPBar_CompareNewHPToOldHP** (2 connections) — `engine/gfx/hp_bar.asm`
- **UpdateHPBar** (1 connections) — `engine/gfx/hp_bar.asm`

## Relationships

- [Engine Pokemon](Engine_Pokemon.md) (6 shared connections)
- [Ram](Ram.md) (6 shared connections)
- [Home 2](Home_2.md) (3 shared connections)
- [Engine Battle 4](Engine_Battle_4.md) (3 shared connections)
- [Engine Menus 2](Engine_Menus_2.md) (3 shared connections)
- [Engine Battle 11](Engine_Battle_11.md) (2 shared connections)
- [Engine Menus](Engine_Menus.md) (2 shared connections)
- [Engine Battle](Engine_Battle.md) (2 shared connections)
- [Scripts 2](Scripts_2.md) (2 shared connections)
- [Engine Movie](Engine_Movie.md) (2 shared connections)
- [Ram 7](Ram_7.md) (1 shared connections)
- [Bank HRAM](Bank_HRAM.md) (1 shared connections)

## Source Files

- `engine/battle/core.asm`
- `engine/battle/move_effects/drain_hp.asm`
- `engine/battle/move_effects/recoil.asm`
- `engine/gfx/hp_bar.asm`
- `home/pokemon.asm`
- `ram/wram.asm`

## Audit Trail

- EXTRACTED: 66 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*