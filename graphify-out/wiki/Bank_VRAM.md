# Bank VRAM

> 109 nodes · cohesion 0.03

## Key Concepts

- **UpdateSprites** (71 connections) — `home/update_sprites.asm`
- **CopyVideoData** (36 connections) — `home/copy2.asm`
- **LoadTownMap_Fly** (25 connections) — `engine/items/town_map.asm`
- **PromptUserToPlaySlots** (25 connections) — `engine/slots/slot_machine.asm`
- **gfx/font.asm** (24 connections) — `gfx/font.asm`
- **LoadFontTilePatterns** (23 connections) — `home/load_font.asm`
- **LoadTextBoxTilePatterns** (23 connections) — `home/load_font.asm`
- **LoadTownMap** (22 connections) — `engine/items/town_map.asm`
- **DisplayDiploma** (21 connections) — `engine/events/diploma.asm`
- **LoadTradingGFXAndMonNames** (19 connections) — `engine/movie/trade.asm`
- **vChars2** (19 connections) — `ram/vram.asm`
- **ram/vram.asm** (18 connections) — `ram/vram.asm`
- **DisableLCD** (18 connections) — `home/lcd.asm`
- **SlidePlayerAndEnemySilhouettesOnScreen** (17 connections) — `engine/battle/core.asm`
- **LoadSlotMachineTiles** (17 connections) — `engine/slots/slot_machine.asm`
- **FarCopyData2** (17 connections) — `home/copy2.asm`
- **vSprites** (17 connections) — `ram/vram.asm`
- **EnableLCD** (16 connections) — `home/lcd.asm`
- **LoadHpBarAndStatusTilePatterns** (16 connections) — `home/load_font.asm`
- **LoadMapData** (16 connections) — `home/overworld.asm`
- **VRAM [VRAM]** (16 connections) — `ram/vram.asm`
- **ReloadMapData** (15 connections) — `home/reload_tiles.asm`
- **CloseTextDisplay** (13 connections) — `home/text_script.asm`
- **vChars1** (13 connections) — `ram/vram.asm`
- **LoadHudTilePatterns** (12 connections) — `engine/battle/core.asm`
- *... and 84 more nodes in this community*

## Relationships

- [Engine Menus](Engine_Menus.md) (28 shared connections)
- [Engine Movie 5](Engine_Movie_5.md) (12 shared connections)
- [Ram 2](Ram_2.md) (11 shared connections)
- [Engine Movie 3](Engine_Movie_3.md) (10 shared connections)
- [Engine Overworld 3](Engine_Overworld_3.md) (9 shared connections)
- [Engine Slots](Engine_Slots.md) (9 shared connections)
- [Ram](Ram.md) (8 shared connections)
- [Engine Movie](Engine_Movie.md) (7 shared connections)
- [Engine Battle](Engine_Battle.md) (6 shared connections)
- [Home 4](Home_4.md) (5 shared connections)
- [Engine Items 2](Engine_Items_2.md) (5 shared connections)
- [Bank WRAM0](Bank_WRAM0.md) (5 shared connections)

## Source Files

- `engine/battle/animations.asm`
- `engine/battle/core.asm`
- `engine/events/diploma.asm`
- `engine/events/hidden_events/town_map.asm`
- `engine/gfx/load_pokedex_tiles.asm`
- `engine/gfx/mon_icons.asm`
- `engine/items/town_map.asm`
- `engine/link/cable_club.asm`
- `engine/menus/display_text_id_init.asm`
- `engine/menus/naming_screen.asm`
- `engine/menus/party_menu.asm`
- `engine/menus/start_sub_menus.asm`
- `engine/movie/trade.asm`
- `engine/slots/slot_machine.asm`
- `gfx/font.asm`
- `gfx/slots/slots.tilemap`
- `gfx/trade.asm`
- `home/copy2.asm`
- `home/lcd.asm`
- `home/load_font.asm`

## Audit Trail

- EXTRACTED: 349 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*