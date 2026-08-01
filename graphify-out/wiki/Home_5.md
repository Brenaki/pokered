# Home 5

> 30 nodes · cohesion 0.10

## Key Concepts

- **wChannelSoundIDs** (21 connections) — `ram/wram.asm`
- **VBlank** (18 connections) — `home/vblank.asm`
- **home/vcopy.asm** (16 connections) — `home/vcopy.asm`
- **UpdateMusic6Times** (6 connections) — `home/audio.asm`
- **UpdateMovingBgTiles** (6 connections) — `home/vcopy.asm`
- **Audio1_UpdateMusic** (5 connections) — `audio/engine_1.asm`
- **Audio2_UpdateMusic** (5 connections) — `audio/engine_2.asm`
- **Audio3_UpdateMusic** (5 connections) — `audio/engine_3.asm`
- **engine/gfx/oam_dma.asm** (5 connections) — `engine/gfx/oam_dma.asm`
- **WriteDMACodeToHRAM** (3 connections) — `engine/gfx/oam_dma.asm`
- **FadeOutAudio** (3 connections) — `home/fade_audio.asm`
- **ClearBgMap** (3 connections) — `home/vcopy.asm`
- **FlowerTile1** (3 connections) — `home/vcopy.asm`
- **FlowerTile2** (3 connections) — `home/vcopy.asm`
- **FlowerTile3** (3 connections) — `home/vcopy.asm`
- **RedrawRowOrColumn** (3 connections) — `home/vcopy.asm`
- **VBlankCopyBgMap** (3 connections) — `home/vcopy.asm`
- **DMARoutine** (2 connections) — `engine/gfx/oam_dma.asm`
- **hDMARoutine** (2 connections) — `engine/gfx/oam_dma.asm`
- **ReadJoypad** (2 connections) — `home/joypad.asm`
- **AutoBgMapTransfer** (2 connections) — `home/vcopy.asm`
- **FillBgMapCommon** (2 connections) — `home/vcopy.asm`
- **GetRowColAddressBgMap** (2 connections) — `home/vcopy.asm`
- **TransferBgRows** (2 connections) — `home/vcopy.asm`
- **VBlankCopy** (2 connections) — `home/vcopy.asm`
- *... and 5 more nodes in this community*

## Relationships

- [Ram 3](Ram_3.md) (3 shared connections)
- [Home 2](Home_2.md) (1 shared connections)
- [Scripts 17](Scripts_17.md) (1 shared connections)
- [Audio Low Health Alarm.Asm](Audio_Low_Health_Alarm.Asm.md) (1 shared connections)
- [Engine Overworld 5](Engine_Overworld_5.md) (1 shared connections)
- [Engine Play Time.Asm](Engine_Play_Time.Asm.md) (1 shared connections)
- [Engine Overworld 2](Engine_Overworld_2.md) (1 shared connections)
- [Home](Home.md) (1 shared connections)
- [Bank VRAM](Bank_VRAM.md) (1 shared connections)

## Source Files

- `audio/engine_1.asm`
- `audio/engine_2.asm`
- `audio/engine_3.asm`
- `engine/gfx/oam_dma.asm`
- `home/audio.asm`
- `home/fade_audio.asm`
- `home/joypad.asm`
- `home/vblank.asm`
- `home/vcopy.asm`
- `ram/wram.asm`

## Audit Trail

- EXTRACTED: 55 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*