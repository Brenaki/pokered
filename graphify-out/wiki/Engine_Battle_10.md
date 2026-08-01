# Engine Battle 10

> 12 nodes · cohesion 0.24

## Key Concepts

- **EndOfBattle** (21 connections) — `engine/battle/end_of_battle.asm`
- **AddBCDPredef** (14 connections) — `engine/math/bcd.asm`
- **engine/battle/end_of_battle.asm** (9 connections) — `engine/battle/end_of_battle.asm`
- **AddAmountSoldToMoney** (8 connections) — `home/inventory.asm`
- **PayDayEffect_** (7 connections) — `engine/battle/move_effects/pay_day.asm`
- **engine/battle/move_effects/pay_day.asm** (4 connections) — `engine/battle/move_effects/pay_day.asm`
- **EvolutionAfterBattle** (3 connections) — `engine/pokemon/evos_moves.asm`
- **DrawText** (2 connections) — `engine/battle/end_of_battle.asm`
- **PickUpPayDayMoneyText** (2 connections) — `engine/battle/end_of_battle.asm`
- **YouLoseText** (2 connections) — `engine/battle/end_of_battle.asm`
- **YouWinText** (2 connections) — `engine/battle/end_of_battle.asm`
- **CoinsScatteredText** (2 connections) — `engine/battle/move_effects/pay_day.asm`

## Relationships

- [Bank WRAM0](Bank_WRAM0.md) (5 shared connections)
- [Ram 2](Ram_2.md) (4 shared connections)
- [Engine Events](Engine_Events.md) (3 shared connections)
- [Ram](Ram.md) (2 shared connections)
- [Engine Events 3](Engine_Events_3.md) (2 shared connections)
- [Engine Menus](Engine_Menus.md) (2 shared connections)
- [Scripts](Scripts.md) (2 shared connections)
- [Engine Battle](Engine_Battle.md) (2 shared connections)
- [Engine Movie 5](Engine_Movie_5.md) (1 shared connections)

## Source Files

- `engine/battle/end_of_battle.asm`
- `engine/battle/move_effects/pay_day.asm`
- `engine/math/bcd.asm`
- `engine/pokemon/evos_moves.asm`
- `home/inventory.asm`

## Audit Trail

- EXTRACTED: 39 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*