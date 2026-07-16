A structured requirement can still be unbuildable: "users can share documents" has a home in the functional bucket and no way to tell, at acceptance, whether it was met. This phase turns each requirement into something a build is held to and a test passes or fails on — acceptance criteria, examples, an explicit scope boundary, and surfaced assumptions. It is where the skill's thesis ([testable-or-its-not-a-requirement](../rules/testable-or-its-not-a-requirement.md)) is enforced on every requirement, not just asserted.

## Write acceptance criteria, not descriptions

A requirement's description says what it *is*; its acceptance criteria say how you will *know it is met* — and the criteria are the real spec, the description is context. Write each requirement's criteria in a form a verification method returns pass/fail on. The format is a fork, chosen per requirement by its shape — [prefer-examples-over-prose](../rules/prefer-examples-over-prose.md) carries the per-case discriminator, [match-existing-spec-conventions](../rules/match-existing-spec-conventions.md) the routing:

- a **single behavior with context** → Given/When/Then (the house default);
- **one rule with many discrete cases** (pricing tiers, eligibility matrices) → an example/decision table, keyed to equivalence classes, not every combination;
- a **continuous range or quality attribute** → a bounded, measurable assertion.

`(basis: Given/When/Then is the house acceptance-criteria default — the existing spec skill's phase-04 convention, standard BDD practice; the per-shape fork is routed through match-existing-spec-conventions.)`

## Add examples and counter-examples

A criterion pinned with a concrete input→output pair, plus the counter-example that must be *rejected*, is far harder to build wrong than one pinned with prose ([prefer-examples-over-prose](../rules/prefer-examples-over-prose.md)). Always include what must **not** work: the negative example fences the boundary the positive one leaves open. "$120 order, Gold tier → $12 off" needs its partner "fraud-flagged account → discount refused" to be unambiguous.

## State what is explicitly out of scope

Saying what the spec will not do prevents the later argument. The discriminator for what to state *explicitly* rather than omit silently: **would a reasonable reader assume it is in?** If yes, exclude it out loud; if no one would expect it, silence is fine. "Sharing does not support external, non-account recipients in this version" is worth stating because a reader would assume it might be included; "sharing does not modify the billing system" is not. An out-of-scope line is a decision recorded ([make-the-unsaid-explicit](../rules/make-the-unsaid-explicit.md)), not an admission of a gap.

## Surface assumptions and open questions

Write every inference down so it can be challenged, and flag every genuine unknown instead of guessing — [make-the-unsaid-explicit](../rules/make-the-unsaid-explicit.md) carries the discriminator between an assumption (a defensible default you took and labeled) and an open question (a fork only a stakeholder can settle). This surfaced list is exactly what `--strict` acts on.

## Hold the testability bar, and challenge for gaps

Two closing moves. **First, the baseline check** — hold every requirement to [testable-or-its-not-a-requirement](../rules/testable-or-its-not-a-requirement.md): verifiable, unambiguous, singular. A requirement below the bar is surfaced as a **warning** delivered with the spec; under `--strict` that warning becomes a hard block ([strict-gate](../modules/strict-gate.md)). The check runs the same either way — only the consequence differs.

**Second, challenge the spec for what is missing and whom it fails** — recruit the **completeness-auditor** critic ([completeness-auditor](../../../agents/critics/completeness-auditor.md)), whose lens is "what requirement, state, or case is absent?", and the **user-advocate** critic ([user-advocate](../../../agents/critics/user-advocate.md)), whose lens is "whose need does this leave unserved?" — and fold their findings in. Without fan-out, apply both lenses yourself: walk the buckets once asking what is missing, then walk them again as each actor asking what they still cannot do, before finalizing.

The output is the concrete spec — every requirement testable, exemplified, scoped, and its assumptions surfaced — ready to be sequenced and sized in [sequencing-and-sizing](05-sequencing-and-sizing.md).
