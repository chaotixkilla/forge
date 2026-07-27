A batch of changes has landed across a plugin; before calling the run done, prove the resulting diff holds, then report the whole change set. Verify and report are **one phase** because no decision sits between them: the author who confirms the merge is sound is the one who reports it, and splitting them would invent a checkpoint where there is none. This is a **checkpoint** phase — the run does not complete until the diff passes — because a bad edit shipped here propagates into the plugin every downstream consumer loads.

## Verify on the diff, with the concern-matched critics and audits

Verify **the diff**, not the whole layer — recruit the reviewers the touched **surface** calls for (not one reviewer per item), so verification scales to what changed and no further. Selection is **surface-primary**: a single change can touch more than one surface and draw more than one reviewer, and the sizing tier chose the *engine* in phase 04 — it does not narrow *which* reviewers run here. In particular, a T3/T4 addition whose authored body introduces method or a grading bar touches the *added-structure* surface **and** the *method/bar* surface, so it draws the earns-its-place check **and** the bar-closure checks, not the former alone. The surface→reviewer selection:

- **method / a bar / step-order changed** (a T2 codify edit, or the authored body of a T3/T4 addition) → the **[cold-executor](../../../agents/critics/cold-executor.md)** (does the step converge?) and **[standards-skeptic](../../../agents/critics/standards-skeptic.md)** (is every bar closed?).
- **wiring / frontmatter / a flag-module pairing changed** (a T1 edit or a T3 wire-up) → the **[contract-skeptic](../../../agents/critics/contract-skeptic.md)**.
- **any skill-layer prose changed** → the **[leak-hunter](../../../agents/critics/leak-hunter.md)** (re-run the capability-not-tool swap test on the touched prose).
- **structure was added** (a T3 component, or a T4 build the maintainer ran) → the **[scaffolding-skeptic](../../../agents/critics/scaffolding-skeptic.md)** — the anti-bloat acceptance check: did each addition earn its place, and was it truly the **lowest tier** that would reach the finding's resolved-state ([intervention-tiers](../rules/intervention-tiers.md))? This is the self-check that would have caught the founding incident, now run on revise's own output.
- **file placement / catalog / packaging changed** → the **[boundary-keeper](../../../agents/critics/boundary-keeper.md)**.

`(basis: derived — the map assigns each touched surface to the reviewer whose declared charter owns it (read each critic's description in agents/critics/); it is the first concern-to-critic selection map in the kit, so the maintainer may narrow or widen it, but the assignment itself is derived from the critics' own lenses, not a house preference.)` Alongside the critics, re-gate the relevant **audits in full over the changed files** — audit-contract for any wiring/frontmatter change, audit-tool-leaks (detection only) for any prose change, audit-packaging for any placement change — mirroring the release preflight's conjunction. Note: audit-tool-leaks' repair mode is **not** dispatched per finding here; it scans the whole layer and takes no per-item input, so a leaked tool name is a T2 method edit routed to codify, and the audit runs here only as a read-only re-gate. Critics challenge read-only; **revise decides and re-edits** what they surface. Without fan-out, apply each selected reviewer's lens yourself — read the linked agent's method and run it inline over the diff before proceeding — rather than skipping the check.

## Loop until clean, bounded

A fix can open a new finding, so re-run the selected checks after each round of edits and **loop until a pass raises nothing** — a fix that leaves the next scan dirty is not a fix. The loop is **bounded**: after **two** attempts on the same unconverging span, stop editing it and **route it to the maintainer** with what the two attempts tried and why they didn't converge. (Two is pinned, not a flag: a span that resists two honest attempts is a design question, not an edit to keep retrying — and if real batches routinely need more, that is a finding revise sizes on itself, not a speculative rounds flag added now.)

## Optional: prove a large batch with a benchmark

The checks above verify the diff is *sound* — it converges, closes its bars, leaks nothing, earns its structure. They do not prove it is *better* than the version before it, and on a batch large enough to trade one behavior for another they can't: a change that repairs one scenario while quietly breaking another passes every static check and still ships a regression. When the batch is that large, escalate past the checkpoint to [benchmark](../../benchmark/SKILL.md) — the heavyweight A/B-with-repeats tier — to prove the change is a net improvement, not a silent trade. This is an **opt-in escalation, not part of the checkpoint**: the run still completes on a clean static pass, and benchmark is the maintainer's call when regression risk earns its cost. A `net-regression` verdict comes back as a fresh findings batch this same skill can take in turn — the diagnose-fix-prove loop closing on itself. When a batch meets this bar and benchmark is *not* run, surface that in the report — flag the large-batch, regression-risk condition under *routed to the maintainer* and recommend the benchmark — so the maintainer's call is put in front of them rather than left to notice.

## Report the change set

Report the whole run as one auditable handoff, so the maintainer sees exactly what moved and what didn't:

- **applied** — each change, mapped to the item (and its originating finding) that justified it, with its tier.
- **deferred**, **won't-do**, **dropped**, **held** — each with the reason recorded in triage, so a non-change is as accountable as a change.
- **diverged routes** — any item whose dispatch differed from its provisional route, with why.
- **routed to the maintainer** — every T4 structural recommendation, and any span the verify loop could not converge.

A run that changed nothing (an all-drop/defer batch, or a `--dry-run`) still reports — the disposition of every item is the record, whether or not it produced a diff.
