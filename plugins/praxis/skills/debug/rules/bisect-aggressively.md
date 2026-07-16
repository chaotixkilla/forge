# Bisect aggressively

Reading a failure linearly from the top spends attention proportional to the size of the search space; binary search crosses that space in a logarithm of its size. On a space of a thousand commits, that is five or six probes instead of a thousand reads. But bisection is not free to apply — used where its preconditions don't hold, it returns a confident *wrong* answer, which is worse than a slow correct one. This rule is both the method for halving the space and the test for when halving beats reading.

## Halve the space, across whichever axis the failure offers

The move is always the same: split the suspect space in two, determine which half still contains the fault, discard the other, repeat. Three axes are usually available:

- **The input** — reduce the failing input toward the smallest one that still triggers the failure, discarding what doesn't change the outcome (the delta-debugging move). A minimal trigger is a smaller space to reason about and names the cause by what it retains.
- **The code path** — probe a point midway between the last-known-good state and the symptom and ask which side the state first goes wrong on; that halves the code under suspicion each probe.
- **The version-control history** — when the failure is a regression, bisect the history between a known-good and a known-bad revision to find the change that introduced it.

## The discriminator: when to bisect, when to read instead

Because the cost is roughly log₂(N) probes, **the size of the space barely matters — the binding constraint is the cost and reliability of one probe.** Bisect when all three hold; read or trace linearly when any fails:

- **Large space, no location hypothesis.** If you can already localize by reading or observability, bisection is wasted motion — narrow directly. Bisect is for when you genuinely don't know where to look.
- **An orderable space with a monotone good→bad boundary.** Bisection assumes that once the space turns "bad" it stays bad along the axis (a single introducing point). A bug that comes and goes along the axis — or a history with broken intermediate states that fail for *other* reasons — violates this, and the search's answer is meaningless.
- **A cheap, reliable, unambiguous per-step oracle.** Each probe must yield a trustworthy good/bad in little time. A slow probe makes even log₂(N) steps expensive; a *flaky* probe is the dangerous one — one mismarked step sends the whole search to the wrong culprit.

## When the oracle is flaky or the history is dirty

If the per-step test is intermittent, make it reliable *before* bisecting: amplify the failure to a high reproduction rate ([reproduce-before-fixing](reproduce-before-fixing.md)), run several trials per step and take the majority, and mark a genuinely-untestable step as *skip*, never as *bad*. If intermediate states are broken for unrelated reasons, the space isn't cleanly orderable — reading the changes directly may beat bisecting them.

`(basis: delta debugging's ddmin for input minimization — Zeller & Hildebrandt, "Simplifying and Isolating Failure-Inducing Input," IEEE TSE 28(2), 2002, which also warns a minimized input is 1-minimal, not globally minimal; the good-anchor / bad-anchor / reliable-classifier contract of bisect-over-history from git's own documentation; and Agans' Rule 4, "Divide and Conquer" (Debugging: The 9 Indispensable Rules, 2002). The three-condition discriminator and the "cost is log₂(N), so per-step oracle cost binds, not space size" framing are the practitioner reconciliation of the bisect-as-default vs. bisect-as-last-resort divergence; the monotone-boundary premise is bisection's implicit assumption — documented in git's design notes and practitioner writeups rather than the reference page — stated here explicitly as the house articulation.)`
