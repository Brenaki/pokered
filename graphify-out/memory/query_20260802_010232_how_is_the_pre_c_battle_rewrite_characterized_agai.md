---
type: "query"
date: "2026-08-02T01:02:32.081640+00:00"
question: "How is the pre-C battle rewrite characterized against the ASM oracle, including trainer AI?"
contributor: "graphify"
outcome: "useful"
source_nodes: ["rewrite/battle/contracts/traceability.json", "rewrite/battle/battle_characterization/emulator.py", "BattleRandom", "CriticalHitTest", "trainer-battle-ai", "capture-and-safari"]
---

# Q: How is the pre-C battle rewrite characterized against the ASM oracle, including trainer AI?

## Answer

Expanded from graph vocabulary: battle characterization asm_runner BattleRandom CriticalHitTest capture-and-safari trainer-battle-ai traceability. The graph links rewrite/battle/contracts/traceability.json groups to controlled requirement nodes, links JSON cases to production ASM entry symbols, and places the PyBoy emulator adapter beside BattleRandom, damage, critical, capture, status, PP, and trainer AI sources. This confirms the rewrite milestone is a test-only compatibility boundary over the production ROMs; isolated hazards remain separately controlled.

## Outcome

- Signal: useful

## Source Nodes

- rewrite/battle/contracts/traceability.json
- rewrite/battle/battle_characterization/emulator.py
- BattleRandom
- CriticalHitTest
- trainer-battle-ai
- capture-and-safari