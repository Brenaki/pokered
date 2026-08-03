# Bank ROM0

> 46 nodes · cohesion 0.08

## Key Concepts

- **home/header.asm** (20 connections) — `home/header.asm`
- **CableClubNPC** (19 connections) — `engine/link/cable_club_npc.asm`
- **ROM0** (17 connections)
- **home/serial.asm** (14 connections) — `home/serial.asm`
- **engine/link/cable_club_npc.asm** (12 connections) — `engine/link/cable_club_npc.asm`
- **Serial_SyncAndExchangeNybble** (10 connections) — `home/serial.asm`
- **Serial_ExchangeByte** (8 connections) — `home/serial.asm`
- **Serial_ExchangeLinkMenuSelection** (6 connections) — `home/serial.asm`
- **Serial_PrintWaitingTextAndSyncAndExchangeNybble** (6 connections) — `home/serial.asm`
- **wUnknownSerialCounter** (6 connections) — `ram/wram.asm`
- **CloseLinkConnection** (4 connections) — `engine/link/cable_club_npc.asm`
- **IsUnknownCounterZero** (4 connections) — `home/serial.asm`
- **Serial_SendZeroByte** (4 connections) — `home/serial.asm`
- **NULL** (3 connections) — `home.asm`
- **NULL [ROM0]** (3 connections) — `home.asm`
- **Start** (3 connections) — `home/header.asm`
- **Header [ROM0]** (3 connections) — `home/header.asm`
- **Serial_ExchangeBytes** (3 connections) — `home/serial.asm`
- **Serial_ExchangeNybble** (3 connections) — `home/serial.asm`
- **SetUnknownCounterToFFFF** (3 connections) — `home/serial.asm`
- **_Start** (3 connections) — `home/start.asm`
- **CableClubNPCAreaReservedFor2FriendsLinkedByCableText** (2 connections) — `engine/link/cable_club_npc.asm`
- **CableClubNPCLinkClosedBecauseOfInactivityText** (2 connections) — `engine/link/cable_club_npc.asm`
- **CableClubNPCMakingPreparationsText** (2 connections) — `engine/link/cable_club_npc.asm`
- **CableClubNPCPleaseApplyHereHaveToSaveText** (2 connections) — `engine/link/cable_club_npc.asm`
- *... and 21 more nodes in this community*

## Relationships

- [Engine Movie 2](Engine_Movie_2.md) (4 shared connections)
- [Engine Battle](Engine_Battle.md) (3 shared connections)
- [Bank VRAM](Bank_VRAM.md) (2 shared connections)
- [Scripts 2](Scripts_2.md) (2 shared connections)
- [Ram](Ram.md) (2 shared connections)
- [Engine Pokemon 2](Engine_Pokemon_2.md) (1 shared connections)
- [Engine Overworld](Engine_Overworld.md) (1 shared connections)
- [Home 4](Home_4.md) (1 shared connections)
- [Scripts 5](Scripts_5.md) (1 shared connections)
- [Bank WRAM0](Bank_WRAM0.md) (1 shared connections)

## Source Files

- `engine/link/cable_club_npc.asm`
- `home.asm`
- `home/header.asm`
- `home/serial.asm`
- `home/start.asm`
- `home/timer.asm`
- `ram/wram.asm`

## Audit Trail

- EXTRACTED: 99 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*