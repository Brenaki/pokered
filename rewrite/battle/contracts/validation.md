# Validation record

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| ASM baseline | `2b9f524537649e22d11bedaaee6eb81832fbbcb0` |
| RGBDS | `v1.0.2+hotfix` |
| PyBoy | `2.7.0` |
| Python | `3.13.11` |
| C | C17, GCC 16.1.1, ASan and UBSan |
| Variants | Red and Blue |
| Behavior profile | `GEN1_FIDELITY` |
| Result | `656 passed`; native C checks passed; ROM hashes unchanged |

Executed command:

```sh
BATTLE_TEST_VARIANTS=red,blue \
  uv run --project rewrite/battle --frozen --no-sync \
  pytest -q rewrite/battle/tests
```

Additional commands:

```sh
make -C rewrite/battle check
python -m battle_characterization.generate_c_tables --check
make DEBUG=1 RGBDS=/tmp/rgbds-v1.0.2-hotfix/ -j4 compare
```

The first local invocation attempted an unnecessary package rebuild and was
blocked by sandboxed network access. `--no-sync` reused the already locked and
synced environment; it did not change dependencies or test behavior.

This record is evidence for the approved first C milestone. It covers portable
`CombatMath`, battle `TrainerAI`, generated RGBDS tables, native sanitizer tests,
and Red/Blue C/ASM differential contracts. Contexts listed as remaining in
`traceability.json` are not claimed as implemented.
