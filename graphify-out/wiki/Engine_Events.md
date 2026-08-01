# Engine Events

> 80 nodes · cohesion 0.04

## Key Concepts

- **VendingMachineMenu** (24 connections) — `engine/events/vending_machine.asm`
- **HandlePrizeChoice** (21 connections) — `engine/events/prize_menu.asm`
- **engine/events/prize_menu.asm** (19 connections) — `engine/events/prize_menu.asm`
- **wPlayerMoney** (19 connections) — `ram/wram.asm`
- **wPlayerCoins** (17 connections) — `ram/wram.asm`
- **CeladonPrizeMenu** (14 connections) — `engine/events/prize_menu.asm`
- **GameCornerClerk1Text** (14 connections) — `scripts/GameCorner.asm`
- **engine/math/bcd.asm** (13 connections) — `engine/math/bcd.asm`
- **Museum1FScientist1Text** (13 connections) — `scripts/Museum1F.asm`
- **engine/events/vending_machine.asm** (12 connections) — `engine/events/vending_machine.asm`
- **HiddenCoins** (11 connections) — `engine/events/hidden_items.asm`
- **SubBCDPredef** (11 connections) — `engine/math/bcd.asm`
- **engine/events/hidden_items.asm** (11 connections) — `engine/events/hidden_items.asm`
- **HasEnoughMoney** (11 connections) — `home/money.asm`
- **engine/items** (10 connections)
- **FoundHiddenItemText** (10 connections) — `engine/events/hidden_items.asm`
- **MtMoonPokecenterMagikarpSalesmanText** (10 connections) — `scripts/MtMoonPokecenter.asm`
- **SafariZoneGateSafariZoneWorker1WouldYouLikeToJoinText** (10 connections) — `scripts/SafariZoneGate.asm`
- **hCoins** (9 connections) — `ram/hram.asm`
- **hMoney** (9 connections) — `ram/hram.asm`
- **PrintPrizePrice** (8 connections) — `engine/events/prize_menu.asm`
- **StringCmp** (8 connections) — `home/compare.asm`
- **HiddenItems** (7 connections) — `engine/events/hidden_items.asm`
- **HiddenItemNear** (7 connections) — `engine/items/itemfinder.asm`
- **SubtractAmountPaidFromMoney_** (6 connections) — `engine/items/subtract_paid_money.asm`
- *... and 55 more nodes in this community*

## Relationships

- [Scripts](Scripts.md) (29 shared connections)
- [Ram](Ram.md) (10 shared connections)
- [Engine Menus](Engine_Menus.md) (9 shared connections)
- [Ram 2](Ram_2.md) (8 shared connections)
- [Engine Battle](Engine_Battle.md) (6 shared connections)
- [Bank VRAM](Bank_VRAM.md) (4 shared connections)
- [Engine Battle 10](Engine_Battle_10.md) (3 shared connections)
- [Scripts 5](Scripts_5.md) (3 shared connections)
- [Engine Events 3](Engine_Events_3.md) (2 shared connections)
- [Bank WRAM0](Bank_WRAM0.md) (2 shared connections)
- [Bank HRAM](Bank_HRAM.md) (2 shared connections)
- [Engine Events 6](Engine_Events_6.md) (1 shared connections)

## Source Files

- `data/events/hidden_coins.asm`
- `data/events/hidden_item_coords.asm`
- `data/events/prize_mon_levels.asm`
- `data/items/vending_prices.asm`
- `engine/events/black_out.asm`
- `engine/events/hidden_items.asm`
- `engine/events/prize_menu.asm`
- `engine/events/vending_machine.asm`
- `engine/items/get_bag_item_quantity.asm`
- `engine/items/itemfinder.asm`
- `engine/items/subtract_paid_money.asm`
- `engine/items/tmhm.asm`
- `engine/math/bcd.asm`
- `home/array2.asm`
- `home/compare.asm`
- `home/map_objects.asm`
- `home/money.asm`
- `ram/hram.asm`
- `ram/wram.asm`
- `scripts/GameCorner.asm`

## Audit Trail

- EXTRACTED: 227 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*