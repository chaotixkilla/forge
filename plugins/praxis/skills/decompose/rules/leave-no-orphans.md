# Leave no orphans

A decomposition is a claim: *these units, together, are all of the work in the source, and no part of the source is done twice.* That claim is easy to break silently. A requirement in the plan quietly has no unit that delivers it (an orphan — discovered mid-build as "wait, who was doing auth?"), or two units both claim the same outcome (an overlap — discovered as a merge conflict and a wasted effort). Neither shows up unless you check the unit set *against the source*, deliberately. This rule pins that check as a coverage proof. It is cited by [check-coverage-and-handoff](../phases/05-check-coverage-and-handoff.md).

## The discriminator: every source element maps to exactly one owning unit

Enumerate the source's elements — the plan's units or the spec's requirements and acceptance criteria — and for each, find its owner among your units. The proof has two directions, and both must hold:

- **No orphans (the source → units direction):** every element of the source is delivered by *at least one* unit. An element with no owning unit is dropped work; either a unit is missing, or the element is deliberately out of scope and must be recorded as such ([carry-just-enough-context](carry-just-enough-context.md)'s explicit-boundary), never silently absent.
- **No overlaps (the units → source direction):** every element is owned by *at most one* unit. Two units delivering the same outcome is double-ownership — decide which owns it and cut the outcome from the other, or merge them ([unit-size-scale](unit-size-scale.md)). A shared *dependency* is not an overlap (that is an explicit link, [make-dependencies-explicit](make-dependencies-explicit.md)); an overlap is two units both claiming to *produce* the same result.
- **Together they are a partition:** exactly-one owner per element — exhaustive (no orphan) and mutually exclusive (no overlap). A unit that maps to *no* source element is its own signal: either it is invented scope to cut, or the source was incomplete and that gap goes back to plan/spec.

## Method: prove it, don't eyeball it

Walk the source list explicitly and mark each element with its owning unit; the unmarked elements are the orphans and the doubly-marked are the overlaps. Recruit the **completeness-auditor** critic to attack the source→units direction (what did you drop?) and the **adversary** critic to attack the units→source direction (where do two units collide, where is a claimed owner not actually delivering it?); without fan-out, run both passes yourself — once reading source-to-units for gaps, once units-to-source for collisions — before declaring coverage. The coverage proof always runs: by fan-out where it is available, by the inline two-direction self-pass otherwise — there is no effort or size gate on *whether* it runs, only on *how* ([check-coverage-and-handoff](../phases/05-check-coverage-and-handoff.md) recruits the same two critics on the same terms).

`(basis: house craft rule; the exactly-one-owner partition is the coverage-and-closure discipline the completeness-auditor critic embodies — exhaustive and mutually exclusive against the source. No external authority; the two-direction check above is the proof procedure.)`

## Anchors

- *Orphan:* the plan specifies rate-limiting on the public API, but no unit mentions it — caught by the source→units walk, added as a unit (or recorded out-of-scope with a reason).
- *Overlap:* two units, "add the audit log writer" and "log admin actions," both write the same audit entries — caught by the units→source walk, merged into one owning unit.
