# Validation record

| Field | Value |
|---|---|
| Date | 2026-08-01 |
| ASM baseline | `2b9f524537649e22d11bedaaee6eb81832fbbcb0` |
| RGBDS | `v1.0.2+hotfix` |
| PyBoy | `2.7.0` |
| Python | `3.13.11` |
| Variants | Red and Blue |
| Behavior profile | `GEN1_FIDELITY` |
| Result | `497 passed` |

Executed command:

```sh
BATTLE_TEST_VARIANTS=red,blue \
  uv run --project rewrite/battle --frozen --no-sync \
  pytest -q rewrite/battle/tests
```

The first local invocation attempted an unnecessary package rebuild and was
blocked by sandboxed network access. `--no-sync` reused the already locked and
synced environment; it did not change dependencies or test behavior.

This record is evidence for the pre-C characterization milestone. Human review
and approval remain pending.
