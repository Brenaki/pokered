# Pokemon Red/Blue Rewrite

This tree contains the incremental rewrite work. The original RGBDS sources at
the repository root remain the executable specification.

The first milestone is intentionally test-only. No C implementation belongs in
this tree until the ASM battle characterization gate has been reviewed and
approved.

Current bounded context:

- [`battle/`](battle/README.md): battle rules and trainer battle AI.

Overworld actor movement, perception, pathfinding, and scripts remain outside
the battle context even when a trainer encounter eventually starts a battle.
