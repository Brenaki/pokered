# Isolated Generation I compatibility hazards

Baseline: `2b9f524537649e22d11bedaaee6eb81832fbbcb0`.

The executable contracts preserve normal and boundary behavior. The following
paths remain isolated during the pre-C milestone because unconstrained execution
can hang, mutate persistent capture data, or require full link/UI orchestration.

| IDs | Source | Isolation decision |
|---|---|---|
| `NC-08` | `ApplyBadgeStatBoosts`, stat effect handlers | Keep source assertion now; add a sequence golden master before porting stat-stage effects. |
| `NC-09` | `HandleCounterMove` | Preserve selected-move and shared-damage inputs in the future domain event; add cursor-history replay before porting Counter. |
| `NC-13` | `GetDamageVarsFor*`, `CalculateDamage` | Do not execute the known divide-by-zero hang in CI. The C compatibility profile must report this state without hanging the process. |
| `NC-14` | successful tail of `ItemUseBall` | Capture arithmetic executes now; transformed-species save mutation stays isolated until a disposable save-state fixture exists. |
| `T-END-001` | `Handle*Fainted`, `EndOfBattle` | Residual branches and result writes are structurally pinned. Add a full-battle savestate replay before replacing orchestration in C. |

Other named nonconformities have direct ASM evidence in the case files or property
tests. These isolation decisions are compatibility controls, not permission to
silently normalize the behavior in C.
