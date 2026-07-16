# Keep the real thing in view

Track which shortcuts would not survive contact with production scale, data, or constraints, so the result isn't read as more than it is. A spike buys its speed with shortcuts — hardcoded values, stubbed dependencies, a tenth of the real data, none of the concurrency — and every shortcut is a gap between what the spike showed and what production demands. Left unnamed, those gaps let a caller read "it worked in the spike" as "it will work in production," which is exactly the over-claim a throwaway experiment cannot support.

This rule is distinct from [ground-claims-in-a-run](ground-claims-in-a-run.md): that one asks *"is this claim real?"* (did something run and show it); this one asks *"how far does a real claim generalize?"* (what did the spike's conditions leave untested). A verdict can be honestly *answered* on the spike's terms and still not transfer — the spike hit the throughput target on 100 records, but production runs 100 million. Name that gap explicitly in the verdict's caveats so the boundary between demonstrated and assumed is visible.

Cited from [evaluate-against-the-question](../phases/05-evaluate-against-the-question.md) (caveat how far the verdict generalizes) and [capture-and-discard](../phases/06-capture-and-discard.md) (the caveats travel in the findings).
