# Battle Characterization

This directory defines the executable compatibility contract for the Pokemon
Red/Blue battle rewrite. The contract is derived from the production RGBDS ROM,
not from a second implementation of the formulas.

## Quality gate

Before any battle C source is added:

1. build Red and Blue with RGBDS `v1.0.2+hotfix` and debug symbols;
2. run source-table, contract, and ASM behavior tests;
3. verify every controlled requirement has traceable evidence;
4. review changes to golden results explicitly;
5. keep `GEN1_FIDELITY` behavior, including documented Generation I defects.

Pixel output, animation timing, text, and audio are presentation concerns and
are not part of this semantic gate.

## Commands

```sh
uv sync --project rewrite/battle --frozen --extra test
make DEBUG=1 pokered.gbc pokeblue.gbc
BATTLE_TEST_VARIANTS=red,blue \
  uv run --project rewrite/battle --frozen pytest rewrite/battle/tests
uv run --project rewrite/battle battle-asm run \
  rewrite/battle/contracts/cases/combat_math.json
```

Set `BATTLE_RED_ROM`, `BATTLE_RED_SYM`, `BATTLE_BLUE_ROM`, or
`BATTLE_BLUE_SYM` to override the default root build artifacts.

Golden files are never updated by the normal test command. Use the explicit
`battle-asm record` command, inspect the diff, and record the approving reviewer
in the controlled documents.

The suite contains reviewed JSON examples, exhaustive reads of all 165 move
records, and ASM property enumerations. See `contracts/traceability.json` for the
owner and evidence method of every controlled ID. Full battle-end, intentional
divide-by-zero, Counter history, and transformed-capture save mutation remain
isolated in `contracts/compatibility_hazards.md`.

## Design boundaries

The future implementation will use the bounded contexts `Battle`,
`CombatMath`, `Conditions`, `Items`, `Capture`, `TrainerAI`, and `Progression`.
The language-neutral JSON case/result protocol is the compatibility boundary.
The ASM runner is its first adapter; the C runner will be a later adapter.
