# Favor disposability

Write prototype code to be deleted. Don't invest in the structure, naming, abstraction, tests, or error handling you'd want in production — every hour spent making a spike durable is an hour spent on code whose whole purpose is to be thrown away once it has yielded its verdict. The subtler cost is the pull the other way: a spike that looks half-decent invites *keeping* it, and a kept spike quietly becomes production code that was never designed — the learning-optimized shortcuts become load-bearing. Resist hardening the spike in place. The deliverable is the verdict and the learnings ([verdict-scale](verdict-scale.md), [record-dead-ends](record-dead-ends.md)), not the code.

This rule is cited from [build-the-spike](../phases/04-build-the-spike.md) (build disposably) and [capture-and-discard](../phases/06-capture-and-discard.md) (discard, don't graft into production); it also drives the "reuse throwaway prior art over crafting fresh" discriminator in [pick-the-cheapest-probe](../phases/03-pick-the-cheapest-probe.md).

## The fork — throwaway spike vs tracer bullet / evolutionary

Disposability is a genuine fork in the literature, not a settled law:

- **Throwaway spike** — build the smallest thing that answers the question, then discard the code and keep only the learning. Pays a re-implementation cost (the real thing is built fresh) to buy a clean, unconstrained production design and the fastest possible disposable learning. Don't cite Brooks's "plan to throw one away" for it: Brooks recanted it in the 1995 anniversary edition, and his throwaway was an entire pilot system, not a small probe. `(basis: Cunningham's XP spike solution; Beck, Extreme Programming Explained; McConnell, Rapid Development ch. 38)`
- **Tracer bullet / evolutionary** — build a thin end-to-end skeleton and *keep* it, growing it into the real system. Pays the cost of living with early structural decisions to buy no-throwaway: the code you learned on becomes the code you ship. `(basis: Hunt and Thomas, The Pragmatic Programmer, "Tracer Bullets"; McConnell ch. 21; Cockburn's walking skeleton)`

**The branch condition — which mode the question calls for:** throw away when the question is *"does this one piece work at all?"* (a feasibility unknown a disposable probe settles); keep-and-grow when the question is *"do the pieces fit together?"* (an integration/architecture question a kept skeleton answers). `(basis: Hunt and Thomas, via artima)`

**The routing rule (non-gating):** prototype's default posture is **throwaway**. By the branch condition, prototype's questions are the *"does this piece work"* kind. Override toward keep-and-grow only when the question is really the *"do the pieces fit"* kind, or the *surrounding work already commits to a tracer-bullet/evolutionary approach*, or a *declared house rule* or the *maintainer* directs it (surrounding convention → house rule → maintainer, in that order). But note the boundary: keep-and-grow is a *different deliverable* — building the real thing incrementally — which is `develop`'s or `plan`'s territory, not a spike's.
