# Engine Slots

> 88 nodes · cohesion 0.05

## Key Concepts

- **engine/slots/slot_machine.asm** (60 connections) — `engine/slots/slot_machine.asm`
- **MainSlotMachineLoop** (29 connections) — `engine/slots/slot_machine.asm`
- **SlotMachine_CheckForMatches** (27 connections) — `engine/slots/slot_machine.asm`
- **LoadSlotMachineTiles** (17 connections) — `engine/slots/slot_machine.asm`
- **SlotMachine_PayCoinsToPlayer** (10 connections) — `engine/slots/slot_machine.asm`
- **SlotMachine_SpinWheels** (10 connections) — `engine/slots/slot_machine.asm`
- **SlotRewardPointers** (10 connections) — `engine/slots/slot_machine.asm`
- **SlotMachine_HandleInputWhileWheelsSpin** (8 connections) — `engine/slots/slot_machine.asm`
- **SlotMachine_AnimWheel1** (7 connections) — `engine/slots/slot_machine.asm`
- **SlotMachine_AnimWheel2** (7 connections) — `engine/slots/slot_machine.asm`
- **SlotMachine_AnimWheel3** (7 connections) — `engine/slots/slot_machine.asm`
- **SlotMachine_PrintPayoutCoins** (6 connections) — `engine/slots/slot_machine.asm`
- **SlotMachine_StopOrAnimWheel1** (6 connections) — `engine/slots/slot_machine.asm`
- **SlotMachine_StopOrAnimWheel2** (6 connections) — `engine/slots/slot_machine.asm`
- **SlotReward300Func** (6 connections) — `engine/slots/slot_machine.asm`
- **wSlotMachineWheel1BottomTile** (6 connections) — `ram/wram.asm`
- **wSlotMachineWheel1SlipCounter** (6 connections) — `ram/wram.asm`
- **SlotMachine_GetWheel2Tiles** (5 connections) — `engine/slots/slot_machine.asm`
- **SlotMachine_GetWheel3Tiles** (5 connections) — `engine/slots/slot_machine.asm`
- **SlotMachine_PrintCreditCoins** (5 connections) — `engine/slots/slot_machine.asm`
- **SlotMachine_StopWheel1Early** (5 connections) — `engine/slots/slot_machine.asm`
- **SlotMachine_SubtractBetFromPlayerCoins** (5 connections) — `engine/slots/slot_machine.asm`
- **data/events/slot_machine_wheels.asm** (5 connections) — `data/events/slot_machine_wheels.asm`
- **wPayoutCoins** (5 connections) — `ram/wram.asm`
- **wSlotMachineWheel1Offset** (5 connections) — `ram/wram.asm`
- *... and 63 more nodes in this community*

## Relationships

- [Bank WRAM0](Bank_WRAM0.md) (6 shared connections)
- [Bank VRAM](Bank_VRAM.md) (6 shared connections)
- [Scripts 6](Scripts_6.md) (5 shared connections)
- [Scripts 46](Scripts_46.md) (5 shared connections)
- [Scripts 2](Scripts_2.md) (4 shared connections)
- [Engine Menus](Engine_Menus.md) (3 shared connections)
- [Engine Battle](Engine_Battle.md) (3 shared connections)
- [Engine Pokemon](Engine_Pokemon.md) (2 shared connections)
- [Engine Pokemon 2](Engine_Pokemon_2.md) (2 shared connections)
- [Engine Items 2](Engine_Items_2.md) (2 shared connections)
- [Engine Movie 2](Engine_Movie_2.md) (2 shared connections)
- [Engine Items 4](Engine_Items_4.md) (2 shared connections)

## Source Files

- `data/events/slot_machine_wheels.asm`
- `engine/battle/animations.asm`
- `engine/slots/slot_machine.asm`
- `gfx/slots/blue_slots_1.2bpp`
- `gfx/slots/blue_slots_2.2bpp`
- `gfx/slots/red_slots_1.2bpp`
- `gfx/slots/red_slots_2.2bpp`
- `gfx/slots/slots.tilemap`
- `ram/wram.asm`

## Audit Trail

- EXTRACTED: 219 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*