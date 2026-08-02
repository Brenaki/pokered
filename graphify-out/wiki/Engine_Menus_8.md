# Engine Menus 8

> 11 nodes · cohesion 0.29

## Key Concepts

- **CalcCheckSum** (11 connections) — `engine/menus/save.asm`
- **SaveCurrentBoxData** (9 connections) — `engine/menus/save.asm`
- **wBoxDataEnd** (9 connections) — `ram/wram.asm`
- **CopyBoxToOrFromSRAM** (7 connections) — `engine/menus/save.asm`
- **CalcIndividualBoxCheckSums** (6 connections) — `engine/menus/save.asm`
- **EmptySRAMBoxesInBank** (6 connections) — `engine/menus/save.asm`
- **sBank2AllBoxesChecksum** (4 connections) — `ram/sram.asm`
- **Saved Boxes 1 [SRAM]** (4 connections) — `ram/sram.asm`
- **EmptyAllSRAMBoxes** (3 connections) — `engine/menus/save.asm`
- **sBank2IndividualBoxChecksums** (3 connections) — `ram/sram.asm`
- **EmptySRAMBox** (2 connections) — `engine/menus/save.asm`

## Relationships

- [Bank SRAM](Bank_SRAM.md) (5 shared connections)
- [Engine Pokemon](Engine_Pokemon.md) (2 shared connections)

## Source Files

- `engine/menus/save.asm`
- `ram/sram.asm`
- `ram/wram.asm`

## Audit Trail

- EXTRACTED: 23 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*