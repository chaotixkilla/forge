Before any work, ask whatever the run needs answered, all in one message ([ask-while-the-user-is-here](../../gather/rules/ask-while-the-user-is-here.md)); with `--deep` or `--critics=<n>`, that includes the cost question ([ask-before-a-heavyweight-run](../../gather/rules/ask-before-a-heavyweight-run.md)).

Anchor the design to the system the change lands in, not an idealized one: a decision reasoned against a clean slate has to be re-made the moment it meets real code.

## Locate the blast radius

Find the modules, services, and data the change will touch — directly and one hop out (the callers of what you change, the consumers of the data you reshape). This is a cross-lane investigation, so **delegate it to the `gather` skill** rather than reading in one dimension: `gather` recruits the fleet in parallel — the `code` lane for how the affected surfaces actually behave, `knowledge-base` for the documented architecture, invariants, and interfaces, and `repository` for the history (why it is this way, what was tried before, what got reverted). Take back its weighted, anchored picture and read the key files it names before designing against them; plan owns what to do with it, `gather` owns the fan-out, and its knowledge lane reads through the [knowledge](../../knowledge/SKILL.md) port, which owns the `tools.knowledge` prerequisite — which is why plan declares none. Recruit only as [fan-out-only-when-it-pays](../../gather/rules/fan-out-only-when-it-pays.md) allows.

When the caller hands you a map of the code the change touches — an understand run's result, its claims anchored and graded by certainty — start from it: what it establishes about the touched modules, their callers and the data's movement is taken as given, and gather is asked only for what it leaves open — the documented architecture and history the map didn't read, a consumer one hop out it doesn't reach, a claim the design will rest on that it carries only as *inferred* or *assumed-unverified*.

## Read the local norms and the constraints they impose

From that picture, name what the current architecture makes **easy versus expensive** — the change that flows with the existing seams costs little; the one that cuts across them costs a lot, and that cost is a design input. Read the conventions the design must be a citizen of ([match-the-surrounding-code](../../../craft/engineering/match-the-surrounding-code.md)): the layering, the error idiom, the abstractions the codebase reaches for. And characterize the **data** the change touches — its shape, volume, access pattern, and lifecycle — because those realities, not the control flow, will drive the structure ([follow-the-data](../../../craft/engineering/follow-the-data.md)).

## Pull out the open forks and the load-bearing assumptions

The spec settled the *what* and left the *how* open on purpose. Enumerate those open decisions explicitly — each is a fork the design must close, and together they are the candidate set [choosing-approach](02-choosing-approach.md) will work. As you map, state the load-bearing assumptions the mapping itself rests on ([surface-assumptions](../rules/surface-assumptions.md)) — "this service owns this data", "this call is synchronous", "volume here stays bounded" — so a wrong one surfaces now, in the map, rather than mid-build.

When invoked with `--from-spec`, the written spec at the given path is the locked, authoritative input: trust its requirements wholesale and re-derive only the system mapping, tracing the open forks back to the clauses that left them open ([from-spec](../modules/from-spec.md)).

The output is a system-anchored picture — blast radius, the easy-vs-expensive constraints, the local conventions and data realities, the open forks, and the load-bearing assumptions — that [choosing-approach](02-choosing-approach.md) closes.
