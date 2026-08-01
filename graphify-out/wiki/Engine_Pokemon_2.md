# Engine Pokemon 2

> 13 nodes · cohesion 0.21

## Key Concepts

- **PlaySoundWaitForCurrent** (30 connections) — `home/delay.asm`
- **engine/pokemon/learn_move.asm** (16 connections) — `engine/pokemon/learn_move.asm`
- **AbandonLearning** (7 connections) — `engine/pokemon/learn_move.asm`
- **OneTwoAndText** (4 connections) — `engine/pokemon/learn_move.asm`
- **PrintLearnedMove** (4 connections) — `engine/pokemon/learn_move.asm`
- **AbandonLearningText** (2 connections) — `engine/pokemon/learn_move.asm`
- **DidNotLearnText** (2 connections) — `engine/pokemon/learn_move.asm`
- **HMCantDeleteText** (2 connections) — `engine/pokemon/learn_move.asm`
- **LearnedMove1Text** (2 connections) — `engine/pokemon/learn_move.asm`
- **PoofText** (2 connections) — `engine/pokemon/learn_move.asm`
- **TryingToLearnText** (2 connections) — `engine/pokemon/learn_move.asm`
- **WhichMoveToForgetText** (2 connections) — `engine/pokemon/learn_move.asm`
- **ForgotAndText** (1 connections) — `engine/pokemon/learn_move.asm`

## Relationships

- [Bank WRAM0](Bank_WRAM0.md) (3 shared connections)
- [Scripts](Scripts.md) (3 shared connections)
- [Home](Home.md) (2 shared connections)
- [Scripts 5](Scripts_5.md) (1 shared connections)

## Source Files

- `engine/pokemon/learn_move.asm`
- `home/delay.asm`

## Audit Trail

- EXTRACTED: 25 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*