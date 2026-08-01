# Engine Debug

> 9 nodes · cohesion 0.33

## Key Concepts

- **PrepareNewGameDebug** (10 connections) — `engine/debug/debug_party.asm`
- **engine/debug/debug_party.asm** (8 connections) — `engine/debug/debug_party.asm`
- **SetDebugNewGameParty** (4 connections) — `engine/debug/debug_party.asm`
- **engine/debug** (3 connections)
- **wRivalStarter** (3 connections) — `ram/wram.asm`
- **DebugNewGameItemsList** (2 connections) — `engine/debug/debug_party.asm`
- **DebugNewGameParty** (2 connections) — `engine/debug/debug_party.asm`
- **DebugSetPokedexEntries** (2 connections) — `engine/debug/debug_party.asm`
- **DebugUnusedList** (1 connections) — `engine/debug/debug_party.asm`

## Relationships

- [Ram](Ram.md) (3 shared connections)
- [Engine Movie](Engine_Movie.md) (1 shared connections)
- [Engine Events 6](Engine_Events_6.md) (1 shared connections)
- [Scripts](Scripts.md) (1 shared connections)

## Source Files

- `engine/debug/debug_party.asm`
- `ram/wram.asm`

## Audit Trail

- EXTRACTED: 18 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*