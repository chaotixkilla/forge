Frame a question, not a topic. "See if the new queue library is any good" points at everything and settles nothing — you cannot tell when you're done, and you cannot tell what the result means. "Can this library hold message ordering under 5k concurrent producers, because if it can't we stay on the current one" names exactly what to build, what would end the spike, and what turns on the answer.

## Frame the three parts

State the spike as a question with three required parts:

- **The specific unknown** — the one thing in doubt, named concretely enough to build an experiment around: not "is the library good" but "does it sustain the write throughput we need on our data shape."
- **The decision it unblocks** — the choice that is waiting on this answer (which library, whether this architecture is viable, whether to commit to this approach). A spike with no decision behind it is curiosity, not de-risking — and burns budget on an answer nobody needs.
- **The observation that would change course** — the concrete result that would answer or refute it, stated *before* building: "sustains ≥10k/sec → we adopt it; below → we don't." This is the success test the verdict is later read against, and naming it now is what stops you rationalizing whatever the spike happens to produce.

`(basis: the riskiest-assumption test and hypothesis-driven structure)`

## Checkpoint: one decision-bearing, quantified question — or don't spike yet

This is a gate. Every later phase scopes to the frame — the probe in [pick-the-cheapest-probe](03-pick-the-cheapest-probe.md) is built to exercise *this* unknown, and the verdict in [evaluate-against-the-question](05-evaluate-against-the-question.md) is read against *this* success test — so a defect here corrupts the whole run. Run the two stages in order — first reduce the ask to a single *first spike*, then check *that* frame — and do **not** proceed on a frame that fails a check.

**Stage 1 — reduce the ask to one first spike.**
- **If the ask is a topic** (points at no specific unknown) — narrow it with the caller, or split it into the sub-questions you'd actually spike; don't fan out on a topic. Recruit only as [fan-out-only-when-it-pays](../../gather/rules/fan-out-only-when-it-pays.md) allows.
- **If the ask braids more than one co-equal unknown** — e.g. *"does this locking pattern keep at-least-once delivery under crashes, **and** can the store sustain our throughput"* joins a correctness unknown to a performance one — do not spike them as one; their probes, verdicts, and findings don't compose ([change-one-thing-at-a-time](../../../craft/evidence/change-one-thing-at-a-time.md)). Spike **one at a time**, ordered by *precedence*:
  - **spike the precedent unknown first.** *X precedes Y when Y's result would be meaningless until X is settled* — measuring Y on an approach whose X is unresolved (or already refuted) measures the wrong thing. In practice a **functional or quality unknown** (does it work at all / is it correct / is it accurate enough) precedes a **performance unknown** (is it fast or scalable enough): the throughput of a queue that doesn't reliably deliver, or the latency of a retriever that misses half its targets, is a number about a system you would never ship. So correctness/quality is spiked before performance *even when each unknown would independently kill the decision* — precedence, not "which also kills the decision," breaks the tie. The category is a heuristic for the test, not the test: two unknowns on separate components, where neither's result changes what the other's means, have no precedence whatever their kinds, and the next bullet routes them. `(basis: "make it work, make it right, then make it fast", commonly attributed to Kent Beck)`
  - **route the ranking to the caller only when no precedence holds** — the unknowns are genuinely independent, neither's result changing what the other's means (two separate functional questions, or two performance axes with no ordering between them).
  The unknown you pick is **the first spike**; the rest become **deferred follow-on spikes** — each a separate re-invocation, framed and checked on its own when it runs.

**Stage 2 — check the first spike's frame** (the one you're about to run — *not* the original braided ask; a threshold or decision that belongs to a *deferred* unknown is sourced when that follow-on spike runs, not now):
- **The success test isn't quantified** — the first spike's success test says *"fast enough"* / *"at our throughput"* with no number. Source the threshold from the **caller** or a **stated constraint** (an SLO, a budget, a measurement the caller supplies), and **do not invent it**: prototype is config-less and has no telemetry channel to read "our throughput" from, so an unsourceable threshold is a halt-and-ask, never a guess. A made-up threshold silently flips the load-bearing verdict — the same run is *answered* against a low bar and *refuted* against a high one ([verdict-scale](../rules/verdict-scale.md)).
- **No decision waits on the first spike's answer** — stop and say so.
- **The unknown can be settled by reading, not building** — wrong skill: route to **understand** (existing behavior) or **gather**/**deep-research** (open-world synthesis). A spike builds something new to observe; building to learn what a read would tell you is wasted effort.

The output of this phase: that framed question (unknown + decision + quantified success test), the deferred follow-on unknowns (if any), and the constraints the answer must respect — the frame every later phase executes against.
