# Make it work, then make it right

Mid-slice, the pull is to write the code *well the first time* — the clean abstraction, the tuned data structure, the general shape — before you have ever seen it run. The judgment this rule governs is the *order* you spend effort in: working first, then structure, then speed. Left to taste it goes wrong in a specific way — one builder polishes the shape and tunes the performance of code that later turns out wrong or gets deleted, and that work is pure waste; another ships a rough slice that ran and then refactors it green. Same slice, two very different amounts of thrown-away effort.

## The discriminator

Sequence effort by **what has been proven to run**. Structure and performance work spent on code not yet observed working is speculative — you may be perfecting code that is wrong, or that the next slice deletes.

- **Not yet green?** Get the simplest thing that *runs and passes on the loop* — resist restructuring, generalizing, or optimizing. A working-but-rough slice you can then refactor beats a beautiful slice that never ran.
- **Green but rough?** *Now* make it right: apply the craft rules, factor the shape, clear the debris — as a behavior-preserving pass, not mixed into the working change ([separate-refactor-from-behavior-change](../change-hygiene/separate-refactor-from-behavior-change.md)). "Right" is gated on "works," never the reverse.
- **Right but slow?** Make it fast **only against a measured need** — a real budget or an observed hot path, not a guess. Premature optimization is polishing on spec; it buys nothing and obscures the code.

The hinge is proof-of-working, not perfectionism deferred forever: each stage is gated on the prior being *observed* green ([prove-the-path-actually-runs](prove-the-path-actually-runs.md), [verified-slice](../verified-slice.md)) — you do not skip "right" because "work" shipped.

(basis: Kent Beck — "make it work, make it right, make it fast" — the red/green/**refactor** cycle in *Test-Driven Development: By Example*: reach green first, improve structure only on green code.)

## The fork: test-first, or test-after

*Whether the slice's check is written before the code or after it* is a genuine, contested craft fork — encode it, don't pick a house winner:

- **Test-first (TDD).** Write the failing check first; it specifies the behavior and is red-before-green by construction. Cost: it presumes you can state the interface up front, which fights exploratory or interface-in-flux work. (basis: Beck, *Test-Driven Development: By Example* — the red/green/refactor cycle, the failing test specifies the behavior.)
- **Test-after (self-testing code).** Build the slice to working, then write the check that pins it. Cost: a test you never watched fail can be vacuous, so it carries the hygiene rider below. (basis: Fowler, *SelfTestingCode* — "the important point is that you have the tests, not how you got to them"; *Software Engineering at Google* Ch. 11 requires tests with changes but is deliberately methodology-agnostic.)

**Routing rule (non-gating): surrounding convention → house rule → maintainer.** If the module's existing tests read as specifications for units built in the same commits, follow test-first; if the repo states a testing discipline, follow it; absent both, either is acceptable and the choice is the builder's.

**The shared hygiene rider (not the hinge of the fork):** whichever pole, every check must be *seen to fail once* against broken/unfixed code before its green is trusted — a test never observed red proves little ([prove-the-path-actually-runs](prove-the-path-actually-runs.md)). This is TDD's red step repurposed as a validity check; it applies to test-after too, and is *not* what separates the two poles.

## The anchors

- *Good:* a thin slice wired end-to-end, run green on the loop, then refactored — extract the helper, tighten the names, flatten the nesting — as a second behavior-preserving pass. Working was proven before a minute went into polish.
- *Bad (reject):* a slice built as a configurable strategy with a cache and a fast path, hand-tuned for a load that was never measured — and it has never once been run. Half of it is deleted when the requirement clarifies; the tuning protected nothing. Effort spent ahead of proof, thrown away.
