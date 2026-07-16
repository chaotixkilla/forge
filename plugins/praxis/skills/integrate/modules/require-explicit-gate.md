# require-explicit-gate (`--gate`)

Activated by `--gate`, referenced from [run-the-gate](../phases/03-run-the-gate.md).

The pre-merge gate runs on the default path already; on some landing types the flow may run a reduced gate or soft-pass a non-required check (e.g. a chore that touches no runtime path). This module forces the gate to run in full and **hard-block** on any non-pass. Deletion test: remove this module and the base gate still runs — `--gate` removes the flow's leniency, so it is a module (an escalation), not the gate itself. `(basis: mirrors spec's --strict / strict-gate — an escalation flag that raises an always-on check from warn to hard block.)`

## The delta — force the gate, block on anything less than green

- **Run every check, skip nothing.** Where the default flow would narrow the gate to the affected checks (per the landing type in [assess-the-change](../phases/01-assess-the-change.md)) or soft-pass an advisory one, `--gate` runs the full check set and treats each as required.
- **Hard-block on non-pass.** Any result that is not a clean pass — a failure, a skip, a soft-pass, a hand-override — blocks the run under `--gate`. This flag does **not** redefine what a pass *is* (that is pinned in [green-before-land](../rules/green-before-land.md)); it removes the flow's permission to be lenient about a non-pass.
- **Overrides a lenient `--on-fail`.** With `--gate`, a failed gate blocks regardless of `--on-fail=continue`; `continue` cannot carry a red gate past the block ([failure-policy](failure-policy.md) and [green-before-land](../rules/green-before-land.md) both state this). `--on-fail`'s other values (ask / rollback / abort) still choose what happens *at* the block.

## When to reach for it

Use `--gate` on a path you don't trust to gate itself — an unattended run, a landing type whose default gate is reduced, or a repo whose CI is advisory-only — to guarantee the change is not landed on anything less than fully green. On the default attended path against a repo with a real required-checks gate, it is redundant with the base behavior.
