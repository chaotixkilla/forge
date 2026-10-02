Two failure modes bracket the choice of probe. Over-build — a probe with error handling, structure, and polish — and you've spent the spike's budget on code you're about to throw away. Under-build — a probe so minimal it stubs the very thing in doubt — and you get a fast, cheap signal that answers nothing (a guaranteed *not checked*).

## The cheapest-probe selection basis

Choose the probe that reaches a trustworthy pass/fail signal on the framed unknown for the least build effort. **"Cheapest" means least effort to a *trustworthy* signal — not least code in the absolute, and not fastest to *any* signal.** Cut cost on breadth — features, polish, final architecture — never on the thing under question. A probe is a candidate only if it actually exercises the framed unknown; among those, cheaper wins. Order candidates by these discriminators, in priority:

1. **Exercises the real risk (a gate, not a preference).** The probe must run the actual thing in doubt under conditions faithful to the question — never a stub, mock, or toy substitute *of the unknown itself* (stubbing everything *else* is not just allowed but required — see below). A probe that fakes the thing under test is disqualified no matter how cheap: a double encodes *your* assumption about the thing in doubt, so a green result confirms the assumption, not the world, and the probe can only ever return *not checked* ([verdict-scale](../rules/verdict-scale.md)). The cheapest probe to *build* is often the one that dodges the risk. `(basis: derived from Meszaros, xUnit Test Patterns; Freeman and Pryce, GOOS ch. 8; Fowler, "Mocks Aren't Stubs")`
2. **Isolates the single unknown.** Among probes that clear the gate, prefer the one that varies only the framed unknown and stubs, mocks, or hardcodes everything else ([change-one-thing-at-a-time](../../../craft/evidence/change-one-thing-at-a-time.md)) — fewer confounds means a signal you can actually attribute. `(basis: the controlled-experiment rule; Zeller, delta debugging and Why Programs Fail)`
3. **Reaches a clear signal fastest.** Prefer the probe with the shortest path to an unambiguous pass/fail ([make-failure-fast-and-loud](../rules/make-failure-fast-and-loud.md)) over one that needs more scaffolding to read.
4. **Reuses scouted prior art over fresh build.** Prefer seeding from what [scout-prior-art](02-scout-prior-art.md) found — a reference implementation, an example, a library's own test — over writing from scratch ([favor-disposability](../rules/favor-disposability.md): borrow throwaway code rather than craft it).

Tie-break when two candidates are otherwise equal: fewer components touched, less code to write. `(basis: maintainer, 2026-07-09; after Freeman and Pryce's GOOS, Cockburn's walking skeleton and Cunningham on "the simplest thing that could possibly work")`

## Under `--max-agents` — pick N candidate approaches

When racing is enabled, this phase selects not one probe but up to *n* candidate *approaches* to the same question — each a **distinct mechanism or strategy**, not the same approach re-parameterized (the axis of difference is pinned in [parallel-fan-out](../modules/parallel-fan-out.md); a parameter sweep is one approach, not a race). Each still obeys the basis above (each must exercise the real risk). How they are compared and selected is [parallel-fan-out](../modules/parallel-fan-out.md).

The output of this phase: the chosen probe (or the N candidate approaches), stated as *what it will exercise* and *what it will stub* — the build plan [build-the-spike](04-build-the-spike.md) executes.
