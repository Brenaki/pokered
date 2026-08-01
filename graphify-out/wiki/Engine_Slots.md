# Engine Slots

> 76 nodes · cohesion 0.06

## Key Concepts

- **engine/slots/slot_machine.asm** (60 connections) — `engine/slots/slot_machine.asm`
- **MainSlotMachineLoop** (29 connections) — `engine/slots/slot_machine.asm`
- **SlotMachine_CheckForMatches** (27 connections) — `engine/slots/slot_machine.asm`
- **Random** (24 connections) — `home/random.asm`
- **InitPlayerData2** (15 connections) — `engine/movie/oak_speech/init_player_data.asm`
- **JoypadLowSensitivity** (14 connections) — `home/joypad2.asm`
- **SlotMachine_PayCoinsToPlayer** (10 connections) — `engine/slots/slot_machine.asm`
- **SlotMachine_SpinWheels** (10 connections) — `engine/slots/slot_machine.asm`
- **SlotRewardPointers** (10 connections) — `engine/slots/slot_machine.asm`
- **SlotMachine_HandleInputWhileWheelsSpin** (8 connections) — `engine/slots/slot_machine.asm`
- **SlotMachine_AnimWheel1** (7 connections) — `engine/slots/slot_machine.asm`
- **SlotMachine_AnimWheel2** (7 connections) — `engine/slots/slot_machine.asm`
- **SlotMachine_AnimWheel3** (7 connections) — `engine/slots/slot_machine.asm`
- **wNumBoxItems** (7 connections) — `ram/wram.asm`
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
- *... and 51 more nodes in this community*

## Relationships

- [Bank WRAM0](Bank_WRAM0.md) (13 shared connections)
- [Ram 2](Ram_2.md) (9 shared connections)
- [Engine Events](Engine_Events.md) (7 shared connections)
- [Ram](Ram.md) (5 shared connections)
- [Scripts 2](Scripts_2.md) (5 shared connections)
- [Scripts](Scripts.md) (4 shared connections)
- [Bank VRAM](Bank_VRAM.md) (4 shared connections)
- [Engine Events 3](Engine_Events_3.md) (2 shared connections)
- [Engine Menus](Engine_Menus.md) (2 shared connections)
- [Engine Movie 3](Engine_Movie_3.md) (2 shared connections)
- [Scripts 4](Scripts_4.md) (1 shared connections)
- [Engine Movie 2](Engine_Movie_2.md) (1 shared connections)

## Source Files

- `data/events/slot_machine_wheels.asm`
- `engine/movie/oak_speech/init_player_data.asm`
- `engine/slots/slot_machine.asm`
- `home/joypad2.asm`
- `home/random.asm`
- `ram/wram.asm`

## Audit Trail

- EXTRACTED: 217 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*