# Seam along change boundaries

A module boundary drawn in the wrong place taxes every future edit: a single change has to reach across the seam, touch both sides, and be tested through the interface between them. Drawn in the right place, the same change stays local — one module edited, its neighbors untouched. The trap is placing seams by what is easy to name (a technical layer, a noun) rather than by where change actually flows. This rule puts boundaries where change and ownership genuinely diverge, so future edits stay contained.

## Put the seam where things change separately

The load-bearing question for every boundary: **what changes together, and what changes independently?** Things that change for the same reason belong on the same side of a seam; things that change for different reasons, at different rates, or under different owners belong on opposite sides. Concretely:

- **Co-change.** Group behavior that a single requirement change would touch as a unit. If a feature edit predictably ripples across three "layers", the layer boundaries are cutting across the real change axis — the feature is the seam, not the layer.
- **Ownership.** A boundary that follows an ownership or team line turns a cross-cutting change into a coordinated one. Put the seam where handoffs already happen, so the interface is also the contract between owners.
- **Rate of change.** Isolate the volatile from the stable — a fast-churning policy behind an interface, a stable core it calls — so the thing that changes often does not drag the thing that rarely changes through review each time.

The discriminator against a bad seam: **does the boundary follow a technology/layer split while the real change axis runs perpendicular to it?** If a typical change crosses the boundary rather than staying inside it, the seam is misplaced.

## This rule places a seam; it does not decide there should be one

*Whether and when* to introduce the abstraction that a seam implies is governed by [justify-every-moving-part](justify-every-moving-part.md) — the ≥2-real-callers floor, the change-together discriminator, and the count fork. This rule assumes that gate has been passed and answers only *where the boundary goes*. Keeping the two separate is what stops them contradicting: justify decides the abstraction is warranted; seam decides its line. And a well-placed seam is what most often turns a one-way door into a two-way one — the thing behind an interface you own is reversible ([design-for-reversibility](design-for-reversibility.md)).

Cited by [specify-interfaces](../phases/03-specify-interfaces.md). Related: [justify-every-moving-part](justify-every-moving-part.md), [design-for-reversibility](design-for-reversibility.md), [follow-the-data](follow-the-data.md) (data ownership is often the truest seam).
