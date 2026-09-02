State the verdict against the framed claim — not "the suite is green" — attach a reproduction for every genuine failure, and surface what was *not* verified. This is test's whole deliverable, and its value is that the caller can trust it: a verdict that reports green while the risky path went unexercised is worse than no verdict.

## State the verdict against the framed claim

Measure the verdict against the pass condition stated in [frame-what-to-verify](01-frame-what-to-verify.md), not against a green suite. The verdict is one of three values — they partition the space, so every run lands on exactly one:

- **PASS** — every part of the framed claim's pass condition is met by a discriminating case that was seen able to fail ([prove-the-test-can-fail](../rules/prove-the-test-can-fail.md)), **and** coverage is **adequate**, or **partial** with every gap named as accepted residual risk ([coverage-adequacy](../rules/coverage-adequacy.md)). The change is established to do what it should, to the depth the coverage reaches.
  - *Anchor:* the discount change's over-100% and empty-cart criteria each have a discriminating case seen red first, all now green, and every High/Medium-risk behavior is covered — PASS.
- **FAIL** — at least one **genuine failure** ([failure-classification](../rules/failure-classification.md)) that is **in-claim** (the scope test below): the change is demonstrably wrong on a reachable input. Such a failure dominates — it makes the verdict FAIL regardless of coverage. An **out-of-claim** genuine failure does **not** set the verdict — it is a real finding, reported separately (see below), not this change's FAIL.
  - *Anchor:* `computeTotal` returns `NaN` for a valid cart on every run — a genuine failure contradicting the claim — FAIL.
- **INCONCLUSIVE** — no genuine failure contradicts the claim, **but coverage is inadequate** to establish it: the risky behaviors were not exercised by discriminating cases, or the cases that ran do not discriminate. The change is neither shown right nor shown wrong. This is the honest verdict for a green suite that never exercised the risky path — reported as such, never rounded up to PASS.
  - *Anchor:* the suite is green, but its only case asserts `computeTotal` "returns a number" and the over-100% rejection was never exercised — INCONCLUSIVE, not PASS.

Resolve mechanically, in order: **an in-claim genuine failure → FAIL**; else **coverage adequate (or partial with gaps named) → PASS**; else **INCONCLUSIVE**. The discriminators: FAIL-vs-rest is the presence of an in-claim genuine failure (scope test below); PASS-vs-INCONCLUSIVE is whether coverage clears [coverage-adequacy](../rules/coverage-adequacy.md) (adequate/partial-named = PASS; inadequate = INCONCLUSIVE).

## In-claim vs out-of-claim — the scope test for a genuine failure

Whether a genuine failure sets the verdict turns on one pinned test, not on where the failing code sits. A genuine failure is **in-claim** (FAIL-eligible) iff **either (a)** the failing behavior is one the framed pass condition names; **or (b)** the failure is *caused by the change*. Evaluate (b) by the shape of the behavior:

- a behavior the change **introduces** (absent before the change) is change-caused **by construction** — it exists only because of the change, so any failure of it is in-claim;
- a behavior the change **alters** is change-caused iff its failure does **not** reproduce on the **pre-change revision** — same case, same expected-vs-actual (a red there merely because the behavior is *absent* pre-change is not a reproduction), the pre-change test in [failure-classification](../rules/failure-classification.md);
- when there is **no pre-change revision** to test (a non-version-controlled tree, or nothing changed — [frame-what-to-verify](01-frame-what-to-verify.md)), only the **altered**-behavior sub-case above is unevaluable (it is the one that needs the baseline): the **introduced**-behavior sub-case still holds — introduced-ness is read from the change itself, not from a baseline — so an introduced-behavior failure stays in-claim. For an *altered* behavior with no baseline to test, fall back to **(a) alone** and surface every such genuine failure prominently as one whose change-attribution could not be established — never silently dropped.

It is **out-of-claim** iff neither (a) nor (b) holds — two instances qualify, both surfaced separately and neither setting the verdict: **(i)** a **pre-existing bug** — not named in the pass condition and it reproduces on the pre-change revision in a *behavior* the change did not functionally alter (even if that behavior sits inside code the change rewrote), which the run merely surfaced; and **(ii)** an **attribution-unestablished** failure — an *altered*-behavior failure on a tree with no baseline to test (the no-pre-change case above), not named in the pass condition, so (b) is unevaluable and (a) does not hold. Label case (ii) *change-attribution unestablished* so the reader knows the classification was forced by a missing baseline, not by evidence the change is innocent.

- *Worked:* a change rewrites the discount path; the run surfaces a negative-discount bug that reproduces on the pre-change revision and is not named in the pass condition → **out-of-claim** (surfaced separately, not this change's FAIL) even though it sits inside the rewritten function. The over-100% rejection breaking *only* after the change → change-caused → **in-claim** → FAIL.

This is distinct from the **coverage universe**: [design-the-cases](03-design-the-cases.md) and [coverage-adequacy](../rules/coverage-adequacy.md) design and grade cases over *every behavior the change introduces or alters* (change-scoped), while this scope test decides only whether a *genuine failure* moves the verdict. The two answer different questions — "what must be covered" vs "what a failure counts against" — and do not conflict.

## Attach a reproduction for every genuine failure

For each genuine failure, attach a reproduction ([make-failures-diagnostic](../rules/make-failures-diagnostic.md)): the input and conditions, the expected-vs-actual, and where it failed — enough that someone who wasn't at the run can reproduce it. Report flakes and environment noise **separately**, each classified, so they are not mistaken for the verdict. Report an **out-of-claim** genuine failure (by the scope test above — a pre-existing bug, or an *attribution-unestablished* failure the missing baseline could not attribute) separately too — it is a real finding worth surfacing, but it does not set this change's verdict value; do not hide it, and do not let it flip the change's verdict to FAIL.

## Surface coverage gaps and residual risk

State the [coverage-adequacy](../rules/coverage-adequacy.md) level and name every gap: the behaviors left unverified and their [risk-priority](../rules/risk-priority.md), so the caller knows what the verdict does and does not cover. The coverage level is reported **independently of the verdict value**: a **FAIL** can carry **adequate** coverage (a discriminating case found the bug — coverage did its job; the failure sets the verdict), and a **PASS** can carry **partial** coverage (with its gaps named). Do not lower the coverage grade because the verdict is FAIL, or raise it because the verdict is PASS — they answer different questions. Under `--from-spec`, report per-criterion status — which acceptance criteria are verified, which are not.

## The verdict shape

Two cold runs must produce a report of the same character. The verdict carries: the framed claim and its pass condition; the verdict value against it (PASS / FAIL / INCONCLUSIVE); each in-claim genuine failure with its reproduction; out-of-claim genuine failures (pre-existing / attribution-unestablished) listed separately; flakes and environment noise listed separately; the coverage-adequacy level with its named gaps and residual risk; and — under `--from-spec` — per-criterion status. `(basis: a pinned report shape is what makes two cold runs' verdicts comparable — the recurring output-shape lesson from review's phase-06 and prototype's verdict output.)`

## Before it goes out, read it as its reader

Put the finished report through [deliver-at-the-readers-register](../../communicate/rules/deliver-at-the-readers-register.md) before delivering it: take from that rule the obligations this phase has not already settled for itself, and apply its honesty floor to the result. A run with no register to write to falls back on the only vocabulary it has loaded — this procedure's own — which is how a report comes out accurate and unreadable. Read the floor from the rule item by item rather than from memory — the passages it protects are exactly the ones that read as padding to anyone not checking whether the claim is true — and let its carve-out for named levels and verdict values hold the graded rungs and status names this skill defines and reports on.

## Output

The verdict — test's whole deliverable. test **does not fix** (a genuine failure hands off to develop or debug) and **does not drive the live app** (that is [verify](../../verify/SKILL.md)); it returns the verdict to its caller.
