With the sub-questions framed, planning decides where each is likely to be answered and how much parallel search to throw at it. The judgment is allocation: match each sub-question to the lanes whose sources would actually settle it, and set a fan-out wide enough to triangulate but not so wide it buries the signal in restatement.

## Map each sub-question to source lanes

Choose, per sub-question, the lanes whose sources would answer it — by fit, not one-of-each:

- **official-documentation** — an authoritative, version-matched contract (what an API guarantees, a config's real defaults). The lane for "what does X officially do."
- **authoritative-literature** — papers, standards, and books; the strongest tier for a settled-knowledge or methodological question.
- **community-practices** — how practitioners actually solved it and the pitfalls they hit; the lane for "does this hold up in practice."
- **knowledge-base** — org-internal prior art: prior research, RFCs, runbooks, and the history and decisions behind a feature (what, when, who). Reached through the [gather](../../gather/SKILL.md) port *when a knowledge backend is configured* — gather owns `tools.knowledge`. Often the highest-value lane for a question about your own systems; when no backend is set, gather drops the lane with a note, so its absence degrades the run, never blocks it.

Lead each sub-question with the lane that would yield its strongest source ([weight-by-source-strength](../rules/weight-by-source-strength.md)): a guaranteed-behavior question leads with official-documentation; a "scales in practice" question pairs authoritative-literature with community-practices.

## Set the fan-out strategy

The default is **a single broad pass**: recruit the fitting lanes once, in parallel, then chase leads until the answer stops moving ([know-when-to-stop](../rules/know-when-to-stop.md)). (basis: single-pass breadth is what a caller who names no depth wants — enough to triangulate the load-bearing claims without a multi-round spend; the escalations are opt-in.) The flags reshape it: [deep-mode](../modules/deep-mode.md) (`--deep`) widens the lane set and the rounds; [budget-discipline](../modules/budget-discipline.md) (`--budget`) bounds the spend and allocates it across sub-questions by importance; [timeboxing](../modules/timeboxing.md) (`--timebox`) caps wall-clock and forces early prioritization.

Sequence the sub-questions so a lead-rich one — whose answer reshapes the others — runs first ([follow-the-leads](../rules/follow-the-leads.md)), rather than in the order the ask happened to list them.

The output is the recruitment plan: which lanes serve which sub-questions, the parallelism and round expectation, and any spend bound — ready for gather-evidence to execute.
