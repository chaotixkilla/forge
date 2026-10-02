## Write up the diagnosis

Whatever the outcome, produce the diagnosis record: the **mechanism** (the cause and the cause→symptom chain from [confirm-root-cause](05-confirm-root-cause.md)), its **certainty**, the **blast radius** (what else the cause can affect — other call sites, data already corrupted, related inputs that share the flaw), and the **reproduction** (the minimal trigger, so the reader can see the failure themselves). This is the content a hand-off carries; if it is routed onward to an incident record, a change request, or a published document through a capability port, it carries the findings and the reproduction — not debug's internal phase/critic/loop machinery.

## Route to one terminal outcome

The run's result is the diagnosis's, on the shared results scale ([results-and-certainty](../../../craft/evidence/results-and-certainty.md)), scoped to the reproduction it was shown on. Every run lands in exactly one of three. Walk the two questions in order — they partition the space:

1. **Did you reproduce the failure?** No → **not checked**, because the failure couldn't be reproduced: report the conditions tried and the evidence that would let someone reproduce it (from [reproduce-and-frame](01-reproduce-and-frame.md)). Stop — no fix is recommended for an unreproduced bug.
2. **Did the cause reach the diagnosis floor** ([root-cause certainty](../rules/root-cause-confidence.md))? No → **unsettled**: report the leading hypothesis, its certainty, and the specific evidence that would settle it or kill it. Yes → **holds**: the diagnosis, with its certainty and its recommended fix (below), is the deliverable. A reproduced behavior that turns out to match its contract — the expectation was wrong, not the code — is a diagnosis that holds too: its mechanism is the contract, and its recommendation is to correct the expectation or its documentation, with no code change. debug never edits the code it diagnoses; making the change is the recipient's.

A hypothesis its experiment refuted **fails**, and is reported among the eliminated rivals; it is never the run's result, so a run whose every candidate failed is **unsettled**. `(basis: derived by construction)`

## Recommend the fix at the cause

A diagnosis that holds carries the fix it recommends, held to the disciplines a fix owes:

- **Its altitude** — the layer that owns the violated invariant, not the first convenient call site ([fix-the-cause-not-the-symptom](../../../craft/evidence/fix-the-cause-not-the-symptom.md), *Place the fix where the invariant lives*).
- **Its guard** ([regression-guard-the-specific-failure](../../../craft/engineering/regression-guard-the-specific-failure.md)) — the test that would encode the reproduction, failing before the change and passing after, so the bug can't return silently.
- **Its size.** **Bounded** when the correct fix is a localized change at the fault's owning layer plus its guarding test, introducing no new design decision; **needs design work** when it requires a decision the author owns — a new abstraction, an interface or contract change that ripples across call sites, a cross-cutting refactor. `(basis: maintainer, 2026-07-10; after Hayes, WPShout, 2018)`

And keep asking whether the recommended fix addresses the mechanism or just hides the symptom: a change that would make the reproduction pass without touching the diagnosed cause is a symptom patch, not a fix.

## Under a declared incident

There is a standing tension in incident work between stopping the bleeding first and never fixing the symptom. In praxis it is settled by who does what: restoring service before the cause is known is mitigation, which runs before diagnosis and isn't debug's. debug resolves cause-only, always.

- **debug's own read of production state never licenses a mitigation.** Gathered telemetry showing a high error rate is *evidence for the diagnosis*, not authorization to patch the symptom.
- **A mitigation already applied is context, not the fix.** When the incident record shows one (a rollback, a feature-flag off, a rate-limit), record it in the diagnosis as *provisional* — the root-cause fix is still owed — and diagnose with it in place, keeping its effect apart from the failure's.

`(basis: Google SRE, Managing Incidents and Emergency Response; scientific debugging's cause-only default)`

## Before it goes out, read it as its reader

Put the finished report through [deliver-at-the-readers-register](../../../craft/writing/deliver-at-the-readers-register.md) before delivering it, applying its honesty floor item by item from the rule, not from memory.

## Boundary

debug diagnoses and recommends the fix; it doesn't make the change, confirm broad end-to-end health, or absorb feature-sized work. The diagnosis it returns is what the change, its guarding test and any wider confirmation are built from.
