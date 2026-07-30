A design that isn't anchored to the real system is fiction — it reasons about an idealized codebase instead of the one the change lands in, and every abstract decision it makes has to be re-decided the moment it meets real code. This phase does the anchoring: locate where the change lives, learn what the existing architecture makes cheap versus expensive, and pull out the decisions the spec deliberately left open. Everything downstream designs against *this* system, not a clean-slate one.

## Locate the blast radius

Find the modules, services, and data the change will touch — directly and one hop out (the callers of what you change, the consumers of the data you reshape). This is a cross-lane investigation, so **delegate it to the `gather` skill** rather than reading in one dimension: `gather` recruits the fleet in parallel — the `code` lane for how the affected surfaces actually behave, `knowledge-base` for the documented architecture, invariants, and interfaces, and `repository` for the history (why it is this way, what was tried before, what got reverted). Take back its weighted, anchored picture; plan owns what to do with it, `gather` owns the fan-out, and its knowledge lane reads through the [knowledge](../../knowledge/SKILL.md) port, which owns the `tools.knowledge` prerequisite — which is why plan declares none.

## Read the local norms and the constraints they impose

From that picture, name what the current architecture makes **easy versus expensive** — the change that flows with the existing seams costs little; the one that cuts across them costs a lot, and that cost is a real design input, not an inconvenience to ignore. Read the conventions the design must be a citizen of ([match-existing-conventions](../rules/match-existing-conventions.md)): the layering, the error idiom, the abstractions the codebase reaches for. And characterize the **data** the change touches — its shape, volume, access pattern, and lifecycle — because those realities, not the control flow, will drive the structure ([follow-the-data](../rules/follow-the-data.md)).

## Pull out the open forks and the load-bearing assumptions

The spec settled the *what* and left the *how* open on purpose. Enumerate those open decisions explicitly — each is a fork the design must close, and together they are the candidate set [choosing-approach](02-choosing-approach.md) will work. As you map, state the load-bearing assumptions the mapping itself rests on ([surface-assumptions](../rules/surface-assumptions.md)) — "this service owns this data", "this call is synchronous", "volume here stays bounded" — so a wrong one surfaces now, in the map, rather than mid-build.

When invoked with `--from-spec`, the written spec at the given path is the locked, authoritative input: trust its requirements wholesale and re-derive only the system mapping, tracing the open forks back to the clauses that left them open ([from-spec](../modules/from-spec.md)).

The output is a system-anchored picture — blast radius, the easy-vs-expensive constraints, the local conventions and data realities, the open forks, and the load-bearing assumptions — that [choosing-approach](02-choosing-approach.md) closes.
