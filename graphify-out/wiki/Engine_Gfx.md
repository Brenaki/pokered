# Engine Gfx

> 64 nodes · cohesion 0.05

## Key Concepts

- **DisplayNamingScreen** (34 connections) — `engine/menus/naming_screen.asm`
- **engine/gfx/mon_icons.asm** (25 connections) — `engine/gfx/mon_icons.asm`
- **engine/menus/naming_screen.asm** (20 connections) — `engine/menus/naming_screen.asm`
- **AskName** (15 connections) — `engine/menus/naming_screen.asm`
- **wStringBuffer** (14 connections) — `ram/wram.asm`
- **PrintNamingText** (9 connections) — `engine/menus/naming_screen.asm`
- **_GivePokemon** (8 connections) — `engine/events/give_pokemon.asm`
- **SetPokedexOwnedFlag** (8 connections) — `engine/events/give_pokemon.asm`
- **GetAnimationSpeed** (8 connections) — `engine/gfx/mon_icons.asm`
- **WriteMonPartySpriteOAM** (8 connections) — `engine/gfx/mon_icons.asm`
- **PrintNicknameAndUnderscores** (7 connections) — `engine/menus/naming_screen.asm`
- **engine/events/give_pokemon.asm** (7 connections) — `engine/events/give_pokemon.asm`
- **EraseMenuCursor** (7 connections) — `home/window.asm`
- **GetPartyMonSpriteID** (6 connections) — `engine/gfx/mon_icons.asm`
- **LoadMonPartySpriteGfxWithLCDDisabled** (6 connections) — `engine/gfx/mon_icons.asm`
- **UnusedPartyMonSpriteFunction** (6 connections) — `engine/gfx/mon_icons.asm`
- **WriteMonPartySpriteOAMBySpecies** (6 connections) — `engine/gfx/mon_icons.asm`
- **PrintAlphabet** (6 connections) — `engine/menus/naming_screen.asm`
- **WriteMonPartySpriteOAMByPartyIndex** (5 connections) — `engine/gfx/mon_icons.asm`
- **CalcStringLength** (5 connections) — `engine/menus/naming_screen.asm`
- **LoadEDTile** (5 connections) — `engine/menus/naming_screen.asm`
- **MonPartySpritePointers** (4 connections) — `data/icon_pointers.asm`
- **DakutensAndHandakutens** (4 connections) — `engine/menus/naming_screen.asm`
- **data/icon_pointers.asm** (4 connections) — `data/icon_pointers.asm`
- **data/text/alphabets.asm** (4 connections) — `data/text/alphabets.asm`
- *... and 39 more nodes in this community*

## Relationships

- [Engine Menus](Engine_Menus.md) (13 shared connections)
- [Home](Home.md) (9 shared connections)
- [Engine Pokemon](Engine_Pokemon.md) (8 shared connections)
- [Engine Link](Engine_Link.md) (7 shared connections)
- [Ram](Ram.md) (5 shared connections)
- [Bank VRAM](Bank_VRAM.md) (4 shared connections)
- [Scripts 2](Scripts_2.md) (3 shared connections)
- [Engine Items 2](Engine_Items_2.md) (3 shared connections)
- [Engine Menus 2](Engine_Menus_2.md) (2 shared connections)
- [Ram 3](Ram_3.md) (2 shared connections)
- [Engine Battle 10](Engine_Battle_10.md) (1 shared connections)
- [Scripts](Scripts.md) (1 shared connections)

## Source Files

- `data/icon_pointers.asm`
- `data/pokemon/menu_icons.asm`
- `data/text/alphabets.asm`
- `data/text/dakutens.asm`
- `engine/events/give_pokemon.asm`
- `engine/gfx/mon_icons.asm`
- `engine/items/town_map.asm`
- `engine/menus/naming_screen.asm`
- `gfx/font/ED.1bpp`
- `gfx/icons/bug.2bpp`
- `gfx/icons/plant.2bpp`
- `gfx/icons/quadruped.2bpp`
- `gfx/icons/snake.2bpp`
- `gfx/trade/bubble.2bpp`
- `home/window.asm`
- `ram/wram.asm`

## Audit Trail

- EXTRACTED: 171 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*