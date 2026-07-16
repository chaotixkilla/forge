# Read at the definition and call sites

Reading a file top to bottom is how you spend an afternoon learning things the question never asked. A symbol's behavior is pinned by two things: what its definition does, and how its real callers actually use it — the arguments they pass, the return they depend on, the order they call it in. Anchoring at both, then following only the usages the question turns on, is what makes an investigation converge instead of sprawl.

## Anchor at the definition plus the real usages
For each symbol the question turns on, read its definition (what it *can* do) and its call sites (what it is *asked* to do — the concrete arguments passed and the returns callers depend on). The definition alone tells you the full behavior; the call sites tell you which slice of it actually matters, and that slice is usually narrow. A function that handles ten cases but is only ever called with one has one relevant behavior — read for that one.

## Follow only the paths that bear on the question
From the call sites, follow outward only along the usages a claim the question must answer depends on — the "which paths matter" test in [stop-when-answered](stop-when-answered.md). A definition has callers, and callers have callers; the discipline is to walk the ones the answer turns on and note-but-not-chase the rest. This is the standard reachability decomposition — definition, callers, callees, the invariants they share — bounded by the question, not by what is nearby.

Cited from [locate-the-surfaces](../phases/02-locate-the-surfaces.md) (what to anchor on) and [trace-the-behavior](../phases/03-trace-the-behavior.md) (how far to follow).
