# What a verified slice is, and what "green" means

Slicing only works if "this slice is done" means the same thing every time. If "green" is left loose, one builder moves on when the code compiles, another when a test they never watched run reports pass, another when they've eyeballed it — and the guarantee slicing is supposed to buy (a failure is attributable to the handful of lines just written) evaporates, because an unverified slice can carry a latent break into the next. This rule pins the bar so [build-in-verified-slices](../phases/03-build-in-verified-slices.md) advances only on real green, and so `--until=slice`/`green`/`red` and `--checkpoint-commit` key off a defined state.

## The baseline the bar is measured against

"Green" is relative to a **baseline** established once, before the first slice: the set of checks that pass on the untouched code. [establish-the-feedback-loop](../phases/02-establish-the-feedback-loop.md) records it. Two cases, so "previously-green" is never ambiguous:

- **Baseline is clean** (the loop passes on the untouched tree) — the baseline-green set is "everything the loop covers," and every slice must keep all of it passing.
- **Baseline is already red** (a pre-existing failure the change didn't cause — common on a real codebase) — the baseline-green set is "everything that passed *before you started*," and the bar is *no regression against that set*, not "make the whole suite green." A pre-existing failure is **not develop's to fix** — record it as out-of-scope; only if it sits on the path the change must exercise is it a blocker (a `debug` hand-off), because then you cannot get a true signal on the slice. Never silently adopt a pre-existing failure as "your" red, and never fix unrelated pre-existing failures inside a develop run (that is `debug`/`maintain`).

## The bar: three conditions, all required

A slice is a **verified slice** — it is **green** — when all three hold:

- **Exercised, not merely built.** The slice's behavior was *run* on the loop from [establish-the-feedback-loop](../phases/02-establish-the-feedback-loop.md) — the code path actually executed. Compilation, type-checking, and a test that exists but never drove the changed path do **not** count ([prove-the-path-actually-runs](verification/prove-the-path-actually-runs.md)).
- **The loop passed.** Running it returned a clear pass for the behavior the slice adds.
- **No regression against the baseline.** The baseline-green set (above) plus every slice already verified is *still* green — the running check that covered them still passes. A slice that makes its own check pass while breaking an earlier one, or a pre-baseline-passing check, is not green; it is a red slice wearing a local pass.

`(basis: routed to maintainer, ratified 2026-07-10 — the three conditions are continuous-integration's "green build" made per-slice (the whole known-good set stays passing), Beck's red/green (a slice is green only when its check, having been able to fail, now passes), and develop's own prove-the-path-actually-runs (observed execution over compilation). Measuring "no regression" against a baseline captured at loop-setup — rather than an absolute "whole suite green" — is what lets develop run on a codebase that starts red without absorbing debug's job. No single external authority defines a "verified slice"; this is the house bar, kept identical to the *verified-green* criterion of the [definition of done](definition-of-done.md) so per-slice green and whole-change green are the same standard at two scales.)`

## The anchors

- *Green (verified):* the loop was clean on the untouched code; you added a slice, ran the loop, watched the new behavior execute and the loop pass, and re-ran the baseline set to confirm nothing regressed. The failure surface for anything that breaks next is now exactly the next slice.
- *Not green (reject as false-green):* the slice compiles and a unit test reports pass — but the test never exercised the new branch (it asserted on an unchanged path), *or* the slice's own check passes while a sibling slice's check now fails. Either is a red slice; treat it as red.

## What a red slice means, and when it hands off

A slice you cannot bring to green is a **red slice**. The hand-off discriminator is **fault localization, not effort**:

- **The fault is in this slice's own diff** — the cause is in the lines you just changed. Fix it and re-verify. This is normal build work, not a hand-off, however many attempts it takes.
- **The fault is not localizable to this slice's diff** — the failure points into code the slice didn't touch, or the mechanism cannot be pinned to the change in hand after you've read it. That is a **debug hand-off**, not a licence to thrash on your own change or to build the next slice on top of red. `--until=red` makes stopping-at-first-red an explicit request, and the run reports **blocked** ([land-the-change](../phases/06-land-the-change.md)'s outcome partition).

(Deliberately open: exactly *how long* to examine the diff before concluding the fault isn't in it is left to executor judgment against the change's size — a one-line slice localizes in seconds, a subtle concurrency slice takes longer. The pinned discriminator is *where the fault lives*, not a fixed attempt count; a bound on patience would be false precision.) Never advance to the next slice, checkpoint, or land on a red slice — an unverified slice in the history is the exact thing this bar exists to keep out.
