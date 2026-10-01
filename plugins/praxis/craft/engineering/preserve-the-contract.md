# Preserve the contract

When you change existing code — a signature, a return shape, a default, an error mode — the code in front of you can be perfectly correct and still ship a regression, because something you can't see on screen depends on it the old way. Some of what a change touches is private and some is a promise, and a promise broken incidentally does its damage somewhere you can't see, on a schedule you don't control: a caller two modules away passing an argument that no longer exists, a client pinned to the old shape, data already written in the old format. Left to taste it goes wrong by tunnel vision — the local change works, the edited file is green, and it gets called done.

## Is this a caller-facing change?

A change to anything a caller could depend on — a **signature** (parameters, order, types), a **return shape**, an **invariant** the code guaranteed, an **error mode** (what it throws or returns on failure), a **default**, or an observable behavior a consumer relies on — reaches every caller. A change to purely internal implementation, with all of that identical, has no blast radius beyond itself.

When it is caller-facing, sort the callers by one property: **can you move them under your control?**

- **Movable — every caller is code you can change and ship together**, even a large in-repository set migrated over several diffs. Read the full blast radius: find *every* caller (a usage search across the repository, a reverse-dependency read) and either **migrate** it to the new form or **confirm** it's unaffected — not a sample, not the ones you remember: all of them. The migrated callers are required lines in the diff, not scope creep. This is a `bounded` change by [change-risk-scale](change-risk-scale.md).
- **Not movable — a contract.** A promise to a consumer you **cannot move under your control** — external code, a non-enumerable or unknown set, or anything across a deploy or version boundary: an exported symbol other repositories import, a wire, serialization or on-disk format, a database schema, an endpoint's request and response shape, a config key, observable timing or ordering something depends on. A change to a contract is an `exposed`-tier change, and it owes a migration path (below). The tell is movability, not diff count.

**A caller you can't migrate now means the change isn't ready.** One you can't reach or can't safely update is a blocker, never something left broken and noted for later: keep the old form working alongside the new (a compatibility path), or the change stops until the caller can move.

`(basis: derived from reading a change in its blast radius, and caller-migration practice)`

## The fork: how much migration or notice a contract change owes

Authorities and house policies genuinely differ on what a contract change owes its consumers; encode the fork rather than pick one, and route it.

- **Break with a major version + migration guide.** Bump the major version (semver's signal that consumers must act), document the change, and let the version boundary carry the break. *Strength:* honest and simple when consumers can choose when to adopt. *Cost:* consumers on the old version get no runtime transition — they break at upgrade time if they miss the guide.
- **Expand–contract (parallel change) with a deprecation window.** Add the new form alongside the old, migrate consumers, then remove the old after a notice period. *Strength:* no flag-day break; consumers move incrementally. *Cost:* a period of carrying both, and the discipline to actually complete the contract step.
- **Same-diff (or staged) update — the boundary case.** When the full consumer set turns out enumerable and movable under your control, the surface is not an exposed contract after all — it's a `bounded` change: update every consumer in one diff, or migrate them over a staged in-repo rollout you own. *Strength:* no migration machinery for a set you fully control. *Cost:* valid only when *none* of the set crosses a deploy or version boundary — if any consumer ships independently or lives outside your reach, it's `exposed` and owes a real migration path.

**Routing (non-gating):** the *surrounding convention* wins first — a project's declared deprecation/versioning policy or its semver commitment; absent that, the *house rule* below; absent that, the *maintainer*.

**The house rule** scales the migration to the consumer set: a same-diff or staged update when the set is movable under your control; expand–contract with a deprecation window when any consumer is external, non-enumerable, or independently deploying; a clean major-version break only when a deprecation window is infeasible. `(basis: maintainer, 2026-07-11)` The window's *length* is deliberately left open, because no single length is right across projects: it routes to the project's deprecation or versioning policy, else to that repo's maintainer, and never blocks the run.

## Never change a contract incidentally

The defect this rule exists to stop is the *silent* contract change — a refactor that renames an exported symbol, a "cleanup" that tightens a tolerated input, a serialization tweak that old data can't read. If the blast-radius map says a surface is a contract, changing it is a decision made on purpose with one of the paths above, recorded with the change — never a side effect of an edit aimed at something else.

## Anchors

- *Good:* you add a required parameter to a widely-called function, run a usage search, find all eleven call sites, and update each in the same change — the diff carries the signature change and its full blast radius, green everywhere.
- *Bad:* you change a function's return from a value to a wrapped result, fix the one caller you were thinking about, and ship — the other four callers still unwrap the old shape and fail at runtime, a regression that looked "done" because the edited file was green.
