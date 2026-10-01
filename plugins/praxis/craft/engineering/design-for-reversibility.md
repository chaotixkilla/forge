# Design for reversibility

A design decision's cost is dominated by how hard it is to undo when it's wrong. A decision one deploy can reverse can be made fast and corrected later; one baked into a persisted format or a public contract must be right the first time. The failure is giving both the same weight: deliberating endlessly over a reversible call, or casually shipping an irreversible one.

## The two classes

`(basis: Bezos's 2015–16 shareholder letters; Booch 2006; Fowler 2003; maintainer, 2026-07-05)`

- **One-Way Door (Type 1).** The decision is **both** (a) *consequential* — it shapes the system, with lasting blast radius — **and** (b) *irreversible, or reversible only at high cost/coordination given the team's actual tooling*: you cannot cheaply reopen the door and walk back. Handle it deliberately; decide it near the last responsible moment, with consultation. *Anchor (clearly one-way):* a published API / on-the-wire or persisted **data format** that external, uncontrolled consumers depend on — you cannot migrate the callers, so reversal breaks third parties; or a destructive one-way data migration over production data.
- **Two-Way Door (Type 2).** Reversible at low cost within your own control — revert with a deploy, no external party to coordinate. Decide it fast, at ~70% of the information you wish you had; do not gate it behind heavyweight review. *Anchor (clearly two-way):* an implementation choice hidden behind an interface you fully own — swap the library or algorithm behind the port and revert in one deploy.

## The assignment test reads tooling as it is now

Reversibility is **not** purely intrinsic to an artifact — it is partly a function of the tooling and practice you actually have. A database schema is a one-way door with no migration tooling and a two-way door with it. So classify by the cost to reverse *given the team's real tooling as of now*, not by the artifact's reputation. `(basis: Fowler, "Who Needs an Architect?", 2003)` The competing reading — treat reversibility as near-intrinsic and classify conservatively — is safer against a missing-tooling surprise but pushes more decisions into the slow Type 1 process; where the codebase's convention already settles this (does it treat schema/contracts as fixed or as migratable?), follow it. `(routed to maintainer: a numeric threshold that tips a decision into Type 1; no authority sets one)`

**When the repository can't show who consumes a format or an interface** — the CSV a finance team imports, an endpoint another system calls — treat it as having consumers you can't move until shown otherwise: a one-way door by default, since breaking a consumer you can't see is exactly the cost the class exists to avoid. `(basis: derived from the class's own reason)`

**Standing directive:** where a Type 1 decision can be *converted* into a Type 2 one cheaply — a version negotiation, an abstraction you own, a reversible migration path — prefer designing that in over deliberating the irreversible choice.

Related: [justify-every-moving-part](justify-every-moving-part.md) (a reversible part is a cheaper bet), [preserve-the-why](../writing/preserve-the-why.md) (a one-way decision most needs its rationale recorded).
