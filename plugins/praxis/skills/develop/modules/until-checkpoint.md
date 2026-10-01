# --until=<condition> — halt at a milestone, report state

`--until` turns a run that would carry the change all the way to landing into one that stops at a named milestone and reports state. A run that stops on `--until` ends in the **checkpointed** (or **blocked**, for `red`) terminal outcome, never *landed* — the stop is by request, so the run must say so rather than reporting a partial build as done ([land-the-change](../phases/06-land-the-change.md)'s outcome partition).

## The stop conditions

`--until` takes one of an enumerated set, one per kind of milestone — a unit boundary, a phase boundary, the first whole-change green, the first unrecoverable red — so a requested stop maps to exactly one. Each names a milestone the build reaches; the run stops the moment it is first reached and reports state:

- **`slice:<N|name>`** — stop after the Nth (or named) buildable unit is a verified slice ([verified-slice](../rules/verified-slice.md)). Assignment: the slice is green and no prior slice regressed; the *next* slice has not started. Reports which slices are done and what remains.
- **`phase:<N|name>`** — stop at the end of the named develop phase (e.g. `phase:3` = after build-in-verified-slices, before integrate-and-wire-up). Assignment: that phase's output is complete; the next phase has not begun. For running or resuming one phase's work in isolation.
- **`green`** — stop at the **first fully-green state**: the first point at which the full local check (not just a slice loop) passes over everything built so far. Assignment: a whole-change check has passed at least once. For getting to a demonstrable running state and pausing.
- **`red`** — stop at the **first red slice**: the first slice that cannot be made green. Assignment: a slice's loop fails and the failure is not resolved by the lines just written. This is the explicit hand-off-to-`debug` stop; the run reports **blocked** with the failing slice and its symptom.

`(basis: maintainer, 2026-07-10)`

When `--until` names a condition the run passes without ever satisfying exactly (e.g. `slice:5` on a four-slice change), the run reaches landing normally and reports that the condition was never triggered — it does not silently keep going past a real stop, nor invent a fifth slice.

## What "report state" means

On stopping, report: which outcome (checkpointed / blocked), what was built and verified so far, what remains to reach done, and — if `--checkpoint-commit` is active — the commit boundaries recorded. The report is what lets a human or a later develop run resume from exactly here.
