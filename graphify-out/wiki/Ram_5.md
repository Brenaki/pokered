# Ram 5

> 24 nodes · cohesion 0.12

## Key Concepts

- **Audio RAM [WRAM0]** (44 connections) — `ram/wram.asm`
- **wChannelDutyCyclePatterns** (11 connections) — `ram/wram.asm`
- **wChannelNoteSpeeds** (11 connections) — `ram/wram.asm`
- **Audio1_note_type** (9 connections) — `audio/engine_1.asm`
- **Audio2_note_type** (9 connections) — `audio/engine_2.asm`
- **Audio3_note_type** (9 connections) — `audio/engine_3.asm`
- **wChannelVolumes** (8 connections) — `ram/wram.asm`
- **wMusicWaveInstrument** (8 connections) — `ram/wram.asm`
- **wSfxWaveInstrument** (8 connections) — `ram/wram.asm`
- **wChannelNoteDelayCountersFractionalPart** (5 connections) — `ram/wram.asm`
- **wAudioROMBank** (2 connections) — `ram/wram.asm`
- **wAudioSavedROMBank** (2 connections) — `ram/wram.asm`
- **wDisableChannelOutputWhenSfxEnds** (2 connections) — `ram/wram.asm`
- **wFrequencyModifier** (2 connections) — `ram/wram.asm`
- **wMusicTempo** (2 connections) — `ram/wram.asm`
- **wMuteAudioAndPauseMusic** (2 connections) — `ram/wram.asm`
- **wNewSoundID** (2 connections) — `ram/wram.asm`
- **wSavedVolume** (2 connections) — `ram/wram.asm`
- **wSfxHeaderPointer** (2 connections) — `ram/wram.asm`
- **wSfxTempo** (2 connections) — `ram/wram.asm`
- **wSoundID** (2 connections) — `ram/wram.asm`
- **wStereoPanning** (2 connections) — `ram/wram.asm`
- **wTempoModifier** (2 connections) — `ram/wram.asm`
- **wUnusedMusicByte** (2 connections) — `ram/wram.asm`

## Relationships

- [Ram 3](Ram_3.md) (16 shared connections)
- [Audio Engine 2.Asm](Audio_Engine_2.Asm.md) (7 shared connections)
- [Audio Engine 3.Asm](Audio_Engine_3.Asm.md) (4 shared connections)
- [Audio Engine 1.Asm](Audio_Engine_1.Asm.md) (3 shared connections)
- [Bank WRAM0](Bank_WRAM0.md) (1 shared connections)
- [Home 5](Home_5.md) (1 shared connections)

## Source Files

- `audio/engine_1.asm`
- `audio/engine_2.asm`
- `audio/engine_3.asm`
- `ram/wram.asm`

## Audit Trail

- EXTRACTED: 64 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*