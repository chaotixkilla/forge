# Put shared code at the right home

You've decided two callers genuinely share knowledge and the helper should be extracted ([dry-vs-incidental-duplication](dry-vs-incidental-duplication.md)). The next judgment is *where it lives* — and the reflex is to drop it wherever is convenient: next to the caller you happened to be editing, or in whatever grab-bag "utils" module is already imported. That reflex quietly wires the dependency graph the wrong way, and two builders left to taste put the same helper in two incompatible homes — one creates an upward dependency, the other a cycle.

## The discriminator

The right home is the **lowest layer both callers already legitimately depend on, reached without adding a new upward or cyclic dependency.**

- **Sink it, don't hoist it.** Shared code belongs *below* its callers, in something stable that both already point down at. If the natural home would have to start depending on a *higher* layer to do its job, that is the wrong home — you're hoisting the helper up to meet convenient code instead of sinking it down to stable code.
- **No new edge upward, no cycle.** Test the extraction by the arrow it creates: caller → home must point down the dependency graph. If placing the helper in module A forces A to import from B while B still imports from A, you've made a cycle — pick a lower shared home, or split the helper so each half sinks cleanly.
- **No clean common home is a signal, not an obstacle.** If the only shared home you can find sits awkwardly high, or would need a brand-new module invented only to hold this one thing, reconsider whether the duplication was shared knowledge at all — a forced home often means the similarity was incidental ([dry-vs-incidental-duplication](dry-vs-incidental-duplication.md)), and two small copies beat one badly-placed abstraction ([right-altitude-abstraction](../abstraction/right-altitude-abstraction.md)).

(basis: the Stable-Dependencies Principle and the dependency-direction rule — Martin, *Clean Architecture* / *Agile Software Development* — depend in the direction of stability; shared code should sink to a stable lower layer that volatile callers point down at, and dependencies must not form cycles. The lowest-common-legitimate-dependency test operationalizes this at the moment of extraction.)

## The anchors

- *Good:* two feature modules both need the same money-rounding rule; it sinks into the existing low-level numeric/domain layer both already import, adding no new edges — a clean downward arrow from each feature to shared code.
- *Bad (reject):* the rounding helper is dropped into feature-module A because that's where you were typing, then feature-module B imports it — now B depends on A's whole feature surface for one helper, and when A later needs something from B you have a cycle. Convenient home, corrupted graph.
