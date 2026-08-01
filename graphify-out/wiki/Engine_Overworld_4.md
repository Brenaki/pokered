# Engine Overworld 4

> 22 nodes · cohesion 0.16

## Key Concepts

- **wSpriteStateData1** (13 connections) — `ram/wram.asm`
- **engine/overworld/trainer_sight.asm** (12 connections) — `engine/overworld/trainer_sight.asm`
- **TrainerEngage** (9 connections) — `engine/overworld/trainer_sight.asm`
- **CalcPositionOfPlayerRelativeToNPC** (8 connections) — `engine/overworld/pathfinding.asm`
- **PalletTownOakWalksToPlayerScript** (8 connections) — `scripts/PalletTown.asm`
- **FindPathToPlayer** (6 connections) — `engine/overworld/pathfinding.asm`
- **TrainerWalkUpToPlayer** (6 connections) — `engine/overworld/trainer_sight.asm`
- **GetSpriteDataPointer** (5 connections) — `engine/overworld/trainer_sight.asm`
- **CalcDifference** (5 connections) — `home/pathfinding.asm`
- **_GetSpritePosition1** (4 connections) — `engine/overworld/trainer_sight.asm`
- **_GetSpritePosition2** (4 connections) — `engine/overworld/trainer_sight.asm`
- **ReadTrainerScreenPosition** (4 connections) — `engine/overworld/trainer_sight.asm`
- **_SetSpritePosition1** (4 connections) — `engine/overworld/trainer_sight.asm`
- **_SetSpritePosition2** (4 connections) — `engine/overworld/trainer_sight.asm`
- **CheckPlayerIsInFrontOfSprite** (3 connections) — `engine/overworld/trainer_sight.asm`
- **DivideBytes** (3 connections) — `home/pathfinding.asm`
- **hDividend2** (3 connections) — `ram/hram.asm`
- **hFindPathNumSteps** (3 connections) — `ram/hram.asm`
- **hNPCPlayerRelativePosFlags** (3 connections) — `ram/hram.asm`
- **hNPCPlayerYDistance** (3 connections) — `ram/hram.asm`
- **hQuotient2** (3 connections) — `ram/hram.asm`
- **CheckSpriteCanSeePlayer** (2 connections) — `engine/overworld/trainer_sight.asm`

## Relationships

- [Scripts 3](Scripts_3.md) (6 shared connections)
- [Home 2](Home_2.md) (2 shared connections)
- [Scripts 5](Scripts_5.md) (1 shared connections)
- [Engine Movie 3](Engine_Movie_3.md) (1 shared connections)

## Source Files

- `engine/overworld/pathfinding.asm`
- `engine/overworld/trainer_sight.asm`
- `home/pathfinding.asm`
- `ram/hram.asm`
- `ram/wram.asm`
- `scripts/PalletTown.asm`

## Audit Trail

- EXTRACTED: 48 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*