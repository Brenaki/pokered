# Battle characterization coverage policy

This gate exists before the first C production file. A requirement is `covered`
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
boundary. C implementation remains blocked by `test_c_rewrite_gate.py` until a
human reviews this milestone and intentionally replaces that gate with C/ASM
differential tests.
