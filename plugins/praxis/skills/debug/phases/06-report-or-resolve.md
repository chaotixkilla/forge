Debug's value is realized here: the investigation becomes either a diagnosis someone can act on or a fix that closes the defect. This phase writes up what was found and routes the run to exactly one terminal outcome — and it holds the line that separates a cause fix from a symptom patch, and a bounded fix from a design change debug should not absorb.

## Write up the diagnosis

Whatever the outcome, produce the diagnosis record: the **mechanism** (the cause and the cause→symptom chain from [confirm-root-cause](05-confirm-root-cause.md)), its **confidence rung**, the **blast radius** (what else the cause can affect — other call sites, data already corrupted, related inputs that share the flaw), and the **reproduction** (the minimal trigger, so the reader can see the failure themselves). This is the content a hand-off carries; if it is routed onward to an incident record, a change request, or a published document through a capability port, it carries the findings and the reproduction — not debug's internal phase/critic/loop machinery.

## Route to one terminal outcome

Every run lands in exactly one of five outcomes. Walk the three questions in order — they partition the space:

1. **Did you reproduce the failure?** No → **not-reproduced**: report the conditions tried and the evidence that would let someone reproduce it (from [reproduce-and-frame](01-reproduce-and-frame.md)). Stop — no fix on an unreproduced bug.
2. **Did you confirm a cause to a defensible rung** (at least *probable* with an observed link)? No → **inconclusive**: report the leading hypothesis and the specific evidence that would confirm or kill it. Stop.
3. **Was `--fix` requested, and is the fix bounded?** For a confirmed cause, split on the flag first, then on the change:
   - **no `--fix`** → **confirmed-diagnosis**: the diagnosis (with any recommended fix altitude) is the deliverable; making the change is the recipient's to do. debug never edits without `--fix`, so a no-`--fix` run always lands here regardless of who will act on it.
   - **`--fix`, and the correct change is bounded** (below) → **resolved**: change made at the cause + a guarding test, original reproduction no longer triggers.
   - **`--fix`, but the correct change needs design work debug should not absorb** (below) → **handed-off**: diagnosis + recommended fix altitude routed to plan/develop, not fixed here.

`(basis: derived. The five outcomes partition every run. Questions 1–2 split on facts of the investigation: reproduced-or-not (not-reproduced is the branch a "we found it" binary drops) and confirmed-or-not (inconclusive is the reproduced-but-unproven run a binary also drops). Question 3 splits the confirmed runs on a single axis — was `--fix` requested, and if so is the change bounded — giving confirmed-diagnosis (no `--fix`), resolved (`--fix` + bounded), or handed-off (`--fix` + design-work). Mutually exclusive: a confirmed run either carries `--fix` or not, and if it does the correct change is either bounded or not — never two branches at once; hand-off is specifically the `--fix` design-work case, not a form of the no-`--fix` diagnosis, so the earlier overlap ("fix deferred to another owner") is gone. Exhaustive: every run answers all three questions and each answer routes to exactly one branch and stops.)`

## Fix at the cause, not the symptom — and know when to hand off

Under `--fix`, the [apply-fix](../modules/apply-fix.md) module extends the run past diagnosis; it owns the smallest-correct-change bar, the confidence gate, and the guarding-test requirement. Two disciplines this phase enforces on any fix:

- **Place it at the right altitude** ([fix-at-the-right-altitude](../rules/fix-at-the-right-altitude.md)) — the layer that owns the violated invariant, not the first convenient call site. A guard bolted onto one caller while the invariant stays breakable elsewhere is a symptom patch wearing a fix's clothes.
- **Guard it against regression** ([guard-against-regression](../rules/guard-against-regression.md)) — encode the reproduction as a test that fails before the change and passes after, so the bug cannot return silently.

And keep asking whether the "fix" addresses the mechanism or just hides the symptom ([distinguish-cause-from-symptom](../rules/distinguish-cause-from-symptom.md)); a change that makes the reproduction pass without touching the confirmed cause is the failure this whole skill exists to prevent.

## The mitigation-vs-root-cause fork

There is a genuine, standing tension in how to *resolve* — and debug encodes it rather than picking a side:

- **Stop the bleeding first** — under a live incident, incident-response practice holds that restoring service comes before understanding: a mitigation (a rollback, a feature-flag off, a rate-limit) that stops the harm now is the right first move, because minimizing time-to-recovery outweighs elegance while users are hurting.
- **Never fix the symptom** — debug's default: a change that suppresses the symptom without addressing the mechanism leaves the cause live, and the bug returns — often worse, now masked.

The tradeoff in a line: a mitigation buys restored service now at the cost of a still-live cause (recurrence risk); a root-cause fix buys durability at the cost of time-to-restore.

**Routing rule.** The mitigate-then-diagnose branch is entered only under a **declared incident** — and that is one crisp check, deliberately kept separate from any judgment about how bad things look:

- **The trigger is a discrete incident-authority signal** — an emitted artifact from an accountable party: `--from-incident`, a declared incident, an on-call/pager activation, or a formal severity declaration. This is a binary presence check; the executor may recognize a further artifact *of this same emitted kind* (the enumeration cannot be exhaustive), which keeps the set open without loosening what counts as the trigger.
- **debug's own read of production state never self-licenses a mitigation.** Gathered telemetry showing a high error rate is *evidence for the diagnosis*, not authorization to patch the symptom — a run may not enter the mitigate branch because *it* judges the live impact severe. Absent a discrete incident signal, the default holds: resolve at the confirmed cause only, and a symptomatic patch is not an acceptable outcome.

When the trigger is present, mitigate-then-diagnose is legitimate: apply the mitigation, record it explicitly as *provisional*, and keep the root-cause fix owed as a follow-up (the mitigation is not the resolution). This fork is non-gating — it routes the resolution, it does not block the run.

`(basis: a fork between two accountable positions — incident-response practice (Google SRE, Managing Incidents / Emergency Response: mitigate to restore service and minimize MTTR before root-causing) and scientific debugging's cause-only default (fix the mechanism, not the symptom). Neither wins globally, so the fork is encoded, non-gating, per the kit's fork-don't-side discipline. The trigger is decomposed into one binary check — a discrete incident-authority signal — because "production pressure" conflated two dimensions that a single fuzzy test let diverge: an emitted authority artifact vs. debug's own read of live impact. Resolving debug's-own-read to never self-license a mitigation is derived from SRE's own framing, where mitigation is an incident-response action taken under a declared incident, not something the debugging agent authorizes from ambient telemetry; it also keeps the cause-only default from being bypassable on the agent's own say-so.)`

## Before it goes out, read it as its reader

Put the finished report through [deliver-at-the-readers-register](../../communicate/rules/deliver-at-the-readers-register.md) before delivering it: take from that rule the obligations this phase has not already settled for itself, and apply its honesty floor to the result. A run with no register to write to falls back on the only vocabulary it has loaded — this procedure's own — which is how a report comes out accurate and unreadable. Read the floor from the rule item by item rather than from memory — the passages it protects are exactly the ones that read as padding to anyone not checking whether the claim is true — and let its carve-out for named levels and verdict values hold the graded rungs and status names this skill defines and reports on.

## Boundary

debug diagnoses, and under `--fix` makes the smallest correct change plus its guarding test — it does not confirm broad end-to-end health (that is test's job, and [verify](../../verify/SKILL.md)'s) and does not absorb feature-sized work (that hands off to plan/develop). A fix that needs the app exercised across flows to be trusted, or a change large enough to need its own plan, is a hand-off, not a step this phase completes.
