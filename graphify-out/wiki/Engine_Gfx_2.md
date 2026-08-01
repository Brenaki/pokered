# Engine Gfx 2

> 9 nodes · cohesion 0.47

## Key Concepts

- **SetPalFunctions** (16 connections) — `engine/gfx/palettes.asm`
- **SetPal_Battle** (8 connections) — `engine/gfx/palettes.asm`
- **SetPal_Pokedex** (7 connections) — `engine/gfx/palettes.asm`
- **SetPal_PokemonWholeScreen** (7 connections) — `engine/gfx/palettes.asm`
- **SetPal_StatusScreen** (7 connections) — `engine/gfx/palettes.asm`
- **wPalPacket** (7 connections) — `ram/wram.asm`
- **DeterminePaletteIDOutOfBattle** (6 connections) — `engine/gfx/palettes.asm`
- **SetPal_Overworld** (6 connections) — `engine/gfx/palettes.asm`
- **PalPacket_Empty** (5 connections) — `data/sgb/sgb_packets.asm`

## Relationships

- [Data Sgb](Data_Sgb.md) (16 shared connections)
- [Ram](Ram.md) (6 shared connections)
- [Bank WRAM0](Bank_WRAM0.md) (1 shared connections)
- [Engine Menus](Engine_Menus.md) (1 shared connections)

## Source Files

- `data/sgb/sgb_packets.asm`
- `engine/gfx/palettes.asm`
- `ram/wram.asm`

## Audit Trail

- EXTRACTED: 41 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*