# Battle characterization coverage policy

This gate was established before the first C production file. A requirement is `covered`
when its source location and expected compatibility policy are reviewable through
one of these evidence methods:

- `asm`: production Red and Blue ROM routines execute with controlled state;
- `asm+structural`: executable cases are paired with table or control-flow checks;
- `structural`: immutable catalog/dispatch completeness is checked from RGBDS data;
- `isolated-hazard`: executing the path would require UI orchestration, persistent
  save mutation, link hardware, or an intentional hang; source assertions and a
  documented isolation decision are mandatory.

`covered` does not mean that every combination of a state machine has been
enumerated. It means the migration has a named oracle or an explicit hazard
boundary. The human review was recorded on 2026-08-03. C implementation is now
allowed only for IDs claimed by `c_milestone` in `traceability.json`, with native
C tests and C/ASM differential evidence. Unclaimed contexts remain
characterization-only.
