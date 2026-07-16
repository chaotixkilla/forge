# Establish the feedback loop

This is develop's leverage, and the phase most often skipped. Before building the change, stand up the tightest loop that gives a true pass/fail signal on it — so every slice in phase 3 is proven in seconds, not discovered broken at the end. A build without a fast loop degrades predictably: changes accumulate unverified, the first run surfaces a tangle of failures at once, and localizing any one of them costs more than the loop would have. Stand the loop up *first*, on purpose, as its own step.

## Find the tightest loop that actually exercises the change

The loop is whatever runs the change's behavior and returns a clear verdict fastest. Reach in this order, stopping at the tightest that genuinely exercises the code you're about to write:

- an existing unit/integration test target you can run scoped to the change,
- a scratch harness or a single new test that drives the specific behavior,
- a REPL / one-shot script that calls the unit directly,
- the running app driven to the one path the change affects.

The discriminator for "tightest loop" is not "fastest command" — it is **the fastest signal that actually exercises the behavior under change**. A millisecond unit test that doesn't touch the changed path is not a loop, it's a false green; a 30-second app run that does exercise it beats a 5-second test that doesn't. Match the loop's *level* to where the change's risk lives: pure logic → a unit-level driver; a wiring/boundary change → an integration-level driver that crosses the seam; a change only observable in the running system → drive the app ([prove-the-path-actually-runs](../rules/verification/prove-the-path-actually-runs.md) is why compilation and an unexercised assertion don't count).

**How hard to work to stand a loop up** (the effort bar, so two builders don't diverge on building-a-harness-vs-a-proxy): build the real loop when a test seam exists **or can be created within the change's own scope** — a harness, a fixture, a driver proportionate to the change you're already making. Fall back to a proxy *only* when a true loop would require infrastructure the change doesn't itself need (a test framework the repo lacks, a whole environment to stand up) — that is a genuine testability finding, surfaced now, not a licence to build blind: note it, fall back to the tightest available proxy, and flag the untested surface for phase 5 and for `test`. The line is whether the loop-building effort is bounded by *this change's* surface or is a project of its own.

**Capture the baseline.** Before the first slice, run the loop (and the repo's checks) on the **untouched** code and record what passes — this is the baseline [verified-slice](../rules/verified-slice.md)'s "no regression" bar is measured against. If the baseline is already red (a pre-existing failure the change didn't cause), that failure is *not develop's to fix* (it is `debug`/`maintain`): record it out-of-scope and hold every currently-passing check green. Only if the pre-existing failure sits on the path this change must exercise is it a blocker — you can't get a clean signal — and that is a `debug` hand-off, not silent absorption.

**Loop, not coverage — the develop/test line.** The loop is the *minimal* check that proves **this slice's** behavior actually ran green; it is not the change's test suite. Designing the discriminating case set — the edges, boundaries, failure modes, and counter-examples that should *not* pass — is `test`'s job, not develop's ([definition-of-done](../rules/definition-of-done.md) criterion 3 scopes develop to the repo's existing bar, not authoring new coverage). The test for whether a case you're about to write is still "the loop": are you writing it to *prove this slice runs* (loop — keep it), or to *cover the behavior's input space* (that is `test` — hand it off)? A slice may need one or a few loop cases; the moment you're enumerating the space, you've crossed into test's work.

## Test-first or test-after — decided once, at loop-setup

The loop's check is where the **test-first vs. test-after** fork actually bites, because the loop *is* the check you're standing up — so decide it here, once, and hold it across the build. develop does not pick a house winner: the two poles, their costs, and the routing rule (surrounding convention → house → maintainer) are **owned by [make-it-work-then-make-it-right](../rules/verification/make-it-work-then-make-it-right.md)** — read it and route accordingly, don't re-decide per slice. At loop-setup the only local consequence is *ordering*: test-first means the loop's failing check comes before the first slice; test-after means the slice comes first and the check pins it. Either way, every check must be **seen to fail once** before its green is trusted ([prove-the-path-actually-runs](../rules/verification/prove-the-path-actually-runs.md)) — a shared validity rider, not the hinge of the fork.

## Fold in the lens's check

When `--lens=<value>` is set, the loop is where the lens stops being advisory: add the lens's own fast check so each slice is verified against it as it's built, not deferred to review — a benchmark or profile for `performance`, a contrast/keyboard check for `accessibility`, the relevant guard test for `security`. See [lens](../modules/lens.md) for how the lens reshapes each phase; here, its concrete obligation is a check in the loop, so the lens is part of "green" from the first slice.

The output of this phase is a standing loop you (or a cold executor) can invoke by a named command or steps, with its level and what it exercises stated — carried into phase 3, where every slice is run against it.
