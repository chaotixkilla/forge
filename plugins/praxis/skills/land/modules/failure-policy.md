# failure-policy (`--on-fail=<abort|continue|ask|rollback>`)

Activated by `--on-fail=`, referenced from the SKILL.md body (it spans the gate and the merge) and consulted by [run-the-gate](../phases/03-run-the-gate.md) and [merge](../phases/04-merge.md).

Base behavior when the gate, a reconcile or the merge fails — an advisory check included: **stop and report**, leaving state recoverable. This module lets the caller override that terminal action per failure. Deletion test: remove this module and land stops-and-reports on any failure; `--on-fail` selects a different action, so it is a module.

## The policy values — assignment test

`--on-fail` takes exactly one of four values; pick by this test, so two callers facing the same situation choose the same one:

- **`abort`** — halt at the failing step, report what failed and where, and leave the working state recoverable (no further step attempted, nothing undone). **This is the default** when `--on-fail` is not given. Assign it when the run is **unattended** or no more-specific policy fits — the safe stop.
- **`ask`** — surface the failure with its context and **wait for a human decision**. The decisions it offers are exactly the other three actions (so each maps to a resting-state member): **retry** the failed step, **roll back**, or **stop** (= abort); plus **continue** *only* when the failure is advisory. It offers no fifth "override" — accepting a hard failure as success is not on the menu, because that is `continue`, which is refused on a non-advisory failure. Assign `ask` when the run is **attended** and a human is present to make the call — the interactive policy. Where the run can't ask — a step another skill called, a background run — `ask` acts as `abort`, and the outcome lists the decisions `ask` would have offered ([ask-while-the-user-is-here](../../gather/rules/ask-while-the-user-is-here.md)).
- **`rollback`** — actively **undo the effect of the stage that failed**, returning to the last-good state: a failed reconcile is undone, restoring the branch to its pre-reconcile commit. It reverses only the failing stage's own effect, never an earlier good step. Where that stage applied **nothing** to reverse — a gate failure, with nothing merged — `rollback` is a **no-op**, reported as `abort` would leave it, never a pretend-reversal. Either way the change rests *stopped-on-failure*. land runs no check after merging, so there is no merge to revert.
- **`continue`** — proceed past the failure to the next step. Assign it **only** for an **advisory** failure ([green-before-land](../rules/green-before-land.md) says which checks are required). It can **never** carry a failed *required* gate past the block — [green-before-land](../rules/green-before-land.md) is a hard stop, and `--gate` ([require-explicit-gate](require-explicit-gate.md)) forces the block regardless of this value. A `continue` requested on a required-gate failure is refused with that reason, not silently honored.

## Partition — every failure lands on exactly one action

The caller picks the value, and each applies only where its own condition holds, falling to `abort` otherwise: `continue` needs an advisory failure, `rollback` needs a failed stage that applied something to reverse, and `ask` needs a human present. A required-gate failure can therefore only `abort`, `ask`, or `rollback`-as-abort; `continue` there is refused, by the green-before-land stop. So on any failure exactly one action fires, and `abort` is the floor. `(basis: maintainer, 2026-07-11)`

## Interaction with the hard stop

`--on-fail` governs the action *at* a failure; it never redefines *what fails*. A required gate that is red **blocks** under every value — `abort`/`ask`/`rollback` choose what happens at the block, and `continue` is refused there. This is the one place the module defers wholly to [green-before-land](../rules/green-before-land.md): the stop is not negotiable, only the response to it is.
