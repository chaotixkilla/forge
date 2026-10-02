# Make it work, then make it right

Mid-slice, the pull is to write the code *well the first time* — the clean abstraction, the tuned data structure, the general shape — before you have ever seen it run. The judgment this rule governs is the *order* you spend effort in: working first, then structure, then speed. Left to taste it goes wrong in a specific way — one builder polishes the shape and tunes the performance of code that later turns out wrong or gets deleted, and that work is pure waste; another ships a rough slice that ran and then refactors it green.

## The discriminator

Sequence effort by **what has been proven to run**.

- **Not yet green?** Get the simplest thing that *runs and passes on the loop* — resist restructuring, generalizing, or optimizing.
- **Green but rough?** *Now* make it right: apply the craft standards, factor the shape, clear the debris — as a behavior-preserving pass in named moves, green after each ([refactoring-catalogue](../../../../craft/engineering/refactoring-catalogue.md)), not mixed into the working change ([separate-refactor-from-behavior-change](../../../../craft/engineering/separate-refactor-from-behavior-change.md)).
- **Right but slow?** Make it fast **only against a measured need** — a real budget or an observed hot path, not a guess.

Each stage is gated on the prior being *observed* green ([prove-the-path-actually-runs](prove-the-path-actually-runs.md), [verified-slice](../verified-slice.md)) — you do not skip "right" because "work" shipped.

(basis: Beck, "make it work, make it right, make it fast"; *Test-Driven Development: By Example*)

## The fork: test-first, or test-after

*Whether the slice's check is written before the code or after it* is a genuine, contested craft fork — encode it, don't pick a house winner:

- **Test-first (TDD).** Write the failing check first; it specifies the behavior and is red-before-green by construction. Cost: it presumes you can state the interface up front, which fights exploratory or interface-in-flux work. (basis: Beck, *Test-Driven Development: By Example*)
- **Test-after (self-testing code).** Build the slice to working, then write the check that pins it. Cost: a test you never watched fail can be vacuous, so it carries the hygiene rider below. (basis: Fowler, *SelfTestingCode*; *Software Engineering at Google*, ch. 11)

**Routing rule (non-gating): surrounding convention → house rule → maintainer.** If the module's existing tests read as specifications for units built in the same commits, follow test-first; if the repo states a testing discipline, follow it; absent both, either is acceptable and the choice is the builder's.

**The shared hygiene rider (not the hinge of the fork):** whichever pole, every check must be *seen to fail once* before its green is trusted, by the methods of [prove-the-test-can-fail](../../../../craft/engineering/prove-the-test-can-fail.md) in their order — a test never observed red proves little ([prove-the-path-actually-runs](prove-the-path-actually-runs.md)).

## The anchors

- *Good:* a thin slice wired end-to-end, run green on the loop, then refactored — extract the helper, tighten the names, flatten the nesting — as a second behavior-preserving pass. Working was proven before a minute went into polish.
- *Bad (reject):* a slice built as a configurable strategy with a cache and a fast path, hand-tuned for a load that was never measured — and it has never once been run. Half of it is deleted when the requirement clarifies; the tuning protected nothing. Effort spent ahead of proof, thrown away.
