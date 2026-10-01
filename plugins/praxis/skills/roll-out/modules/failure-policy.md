# failure-policy (`--on-fail=<abort|continue|ask|rollback>`)

Activated by `--on-fail=`, referenced from the SKILL.md body (it spans the rollout and the health verdict) and consulted by [promote](../phases/02-promote.md) and [confirm-healthy](../phases/03-confirm-healthy.md).

Base behavior when a rollout fails or its verdict is needs-rollback: **stop and report**, leaving state recoverable. This module lets the caller override that terminal action per failure. Deletion test: remove this module and roll-out stops-and-reports on any failure; `--on-fail` selects a different action, so it is a module.

## The policy values — assignment test

`--on-fail` takes exactly one of four values; pick by this test, so two callers facing the same situation choose the same one:

- **`abort`** — halt at the failing step, report what failed and where, and leave the working state recoverable (no further step attempted, nothing undone). **This is the default** when `--on-fail` is not given. Assign it when the run is **unattended** or no more-specific policy fits — the safe stop.
- **`ask`** — surface the failure with its context and **wait for a human decision**. The decisions it offers are exactly the other three actions (so each maps to a resting-state member): **retry** the failed step, **roll back**, or **stop** (= abort); plus **continue** *only* when the failure is advisory. It offers no fifth "override" — accepting a hard failure as success is not on the menu, because that is `continue`, which is refused on a non-advisory failure. Assign `ask` when the run is **attended** and a human is present to make the call — the interactive policy. A watched run is not attended: under `--watch`, `ask` acts as `abort` ([watch-the-pipeline](watch-the-pipeline.md)), and so does a run that can't ask, such as a step another skill called ([ask-while-the-user-is-here](../../gather/rules/ask-while-the-user-is-here.md)). The outcome then lists the decisions `ask` would have offered.
- **`rollback`** — actively **undo the deployment**, returning the environment to its last-good state; the merge is never touched, and the run rests *not-rolled-out*. Where nothing deployed — a rollout that failed before promoting any stage — `rollback` is a **no-op**, reported as `abort` would leave it, never a pretend-reversal.
- **`continue`** — proceed past the failure to the next step. Assign it **only** for a **non-gating / advisory** failure (a soft check, an optional lint). A hard rollout failure — the deploy itself failed, or a sustained needs-rollback breach — is never advisory, so a `continue` requested on one is refused with that reason, not silently honored.

## Partition — every failure lands on exactly one action

The four values are exhaustive and mutually exclusive over "what to do at a failure": `continue` (advisory failures only) → `rollback` (a reverse exists) → `ask` (a human is present) → `abort` (everything else, the default). Applied to any failure, exactly one action fires: a rollout failure admits `abort`/`ask`/`rollback` always, and `continue` **only when that specific failure is itself advisory** (a soft canary signal the caller treats as non-blocking) — never when the deploy hard-failed. There is no failure for which no value applies (abort is the floor) and none for which two fire (a `continue` on a hard failure is refused). `(basis: maintainer, 2026-07-11)`
