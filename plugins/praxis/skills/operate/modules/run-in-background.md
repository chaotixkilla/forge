# run-in-background (`--background`)

Activated by `--background`, referenced from the SKILL.md body — it changes the whole run's lifecycle, not one phase.

Base behavior: operate runs attached in a single session. This module detaches the loop so it continues across turns. Deletion test: remove it and operate still runs to a terminal outcome in one session; detaching across turns is additive — so it is a module.

## The delta — detach and re-engage on state change

Detach the operate loop so long-running waits — the [watch-until-stable](watch-until-stable.md) hold, a slow diagnosis, a mitigation baking in — continue across turns without holding the session open, re-engaging the operator only on a **state change or threshold breach**, not on a fixed clock. The re-engagement triggers:

- the watched signal reaches baseline and holds (→ resolve), or regresses (→ re-stabilize);
- the watch window times out unsettled (→ *indeterminate*, surface for a decision);
- severity changes (a mitigated incident worsens);
- a handed-off durable fix lands (→ verify).

**Delegate the detachment and scheduling to the harness's own long-running/loop capability — do not reimplement polling.** operate configures the re-engagement triggers and the interval; the harness owns the mechanism that suspends and re-invokes the run. `(basis: the harness provides the loop/schedule/detach primitives; a skill names what it needs re-engaged and when — a capability — and lets the harness effect it, the same way the skill layer names capabilities rather than tools. Reimplementing a poll loop inside the skill would be an invented mechanism competing with the harness's.)`

## Composition

- **With `--watch`** ([watch-until-stable](watch-until-stable.md)): the natural pairing — the sustained baseline watch is exactly the long wait worth detaching, so it continues in the background and re-engages when the signal settles or the window times out.
- **With `--notify`** ([notify-stakeholders](notify-stakeholders.md)): a backgrounded run still pushes its transition updates as they occur, so stakeholders are kept current even while the operator is detached.
