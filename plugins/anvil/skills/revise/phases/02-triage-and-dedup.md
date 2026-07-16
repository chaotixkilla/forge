The intake worklist is a flat list of actionable items, and some of them are the same defect wearing different clothes while others don't warrant acting on at all. This phase collapses the duplicates and decides, for each survivor, *whether and when* to act — before any sizing or dispatch happens, so the engines downstream only ever see work that is genuinely distinct and genuinely worth doing. The failure this prevents is the one that motivated the skill: N symptoms of one root cause turned into N separate changes, and preference-only noise actioned as if it were a defect.

## Dedup by root cause

Cluster items that trace to the **same underlying defect** — the same wrong or missing thing — into one work item that carries its several locations, not several items. Cluster by the *defect*, not by the eventual fix (which sizing hasn't chosen yet, so a fix-shaped test would be circular): two items are the same defect when correcting the one thing they both name would resolve both, however many sites witness it and whatever shape that correction later takes. (A single judgment left unpinned across three phases is *one* item with three witnessing locations; three genuinely different missing defaults are *three* items.) Rank the resulting clusters by the **grade** each item carries from [01-intake](01-intake.md) — dogfood items carry theirs, and intake assigned one to the un-graded inputs on the same ladder — and **order by it, don't re-grade**: grading happened in intake, this phase only sorts.

## Assign a disposition

Every surviving cluster gets exactly one disposition:

- **act** — a real, unblocked, in-scope defect; proceeds to sizing. This is the **default**: revise acts on every such item and does not thin the worklist by guessing what is "worth this pass."
- **hold** — real and worth fixing, but **blocked on a cross-cutting maintainer decision it cannot be sized until** (a design fork, a ratification the fix depends on). Held with the blocking question named — never silently deferred.
- **defer** — real and **will be acted on**, just not in this pass: the maintainer directs the timing, or it belongs to a different plugin/scope than this batch. Never a priority guess. Recorded so it is not lost.
- **won't-do** — a real, in-scope defect that will **not** be acted on at all: it contradicts a ratified decision, or the maintainer declines it. Rationale recorded; never a silent decline.
- **drop** — not a work item: preference-only, already-demoted, or subsumed by another cluster. Recorded with the one-line reason.

## The disposition enum is a closed partition

`(basis: derived — the five values are proven exhaustive and mutually exclusive by construction, so every triaged cluster lands in exactly one. Walk the space: an item either warrants acting (→ **act**, unless a maintainer decision blocks sizing → **hold**, or it's a tracked-later → **defer**) or does not (→ **won't-do** when a real item is declined with cause, **drop** when it isn't a work item at all). The load-bearing discriminators, at the seams cold runs split on: **hold vs defer** — is the item *blocked on a maintainer decision the fix needs* (hold) or merely *timed for a later pass* (defer)? **defer vs won't-do** — will it be *acted on eventually* (defer) or *not at all* (won't-do)? **won't-do vs drop** — is it a *real defect we decline* (won't-do, owes a rationale) or *not a defect* (drop, owes only the reason it isn't one)? The indeterminate case a binary would drop — "real, but can't be sized yet" — is exactly what **hold** names, so no cluster falls between act and won't-do.)`

Every disposition except **act** ends the item's journey here, with its reason recorded for the phase-05 report. Only **act** items continue to [03-size-intervention](03-size-intervention.md).
