# Engine Battle 13

> 14 nodes · cohesion 0.20

## Key Concepts

- **BTL-MOV** (7 connections)
- **AnyMoveToSelect** (6 connections) — `engine/battle/core.asm`
- **RecoilEffect_** (6 connections) — `engine/battle/move_effects/recoil.asm`
- **T_PP_003_STRUGGLE_RECOIL_IS_HALF_DAMAGE** (5 connections) — `rewrite/battle/contracts/cases/turn_status_pp.json`
- **move-catalog-and-pp** (5 connections) — `rewrite/battle/contracts/traceability.json`
- **engine/battle/move_effects/recoil.asm** (4 connections) — `engine/battle/move_effects/recoil.asm`
- **T_PP_001_LAST_USE_DECREMENTS_BATTLE_AND_PARTY_PP** (4 connections) — `rewrite/battle/contracts/cases/turn_status_pp.json`
- **T_PP_002_ALL_ZERO_SELECTS_STRUGGLE** (4 connections) — `rewrite/battle/contracts/cases/turn_status_pp.json`
- **T_PP_004_MULTI_TURN_CONTINUATION_DOES_NOT_DECREMENT_PP** (4 connections) — `rewrite/battle/contracts/cases/turn_status_pp.json`
- **T-PP-002** (3 connections)
- **NoMovesLeftText** (2 connections) — `engine/battle/core.asm`
- **HitWithRecoilText** (2 connections) — `engine/battle/move_effects/recoil.asm`
- **T-PP-001** (2 connections)
- **T-PP-003** (2 connections)

## Relationships

- [Scripts 2](Scripts_2.md) (2 shared connections)
- [Engine Battle 4](Engine_Battle_4.md) (2 shared connections)
- [Engine Battle](Engine_Battle.md) (1 shared connections)
- [Engine Battle 8](Engine_Battle_8.md) (1 shared connections)
- [Ram](Ram.md) (1 shared connections)
- [Rewrite](Rewrite.md) (1 shared connections)

## Source Files

- `engine/battle/core.asm`
- `engine/battle/move_effects/recoil.asm`
- `rewrite/battle/contracts/cases/turn_status_pp.json`
- `rewrite/battle/contracts/traceability.json`

## Audit Trail

- EXTRACTED: 26 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*