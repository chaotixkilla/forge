# Preserve the evidence

A failure you can only reproduce once is destroyed the moment your first probe changes the conditions that produced it — and a rare or production-only failure may not come back for days. Debugging that mutates state before capturing it can erase the very thing being investigated, leaving you worse off than before you touched it. This rule is the discipline of capturing the failing state before you start poking.

## Snapshot before you mutate

Before the first experiment, capture what the failure needs to be re-examined: the **inputs** that triggered it, the **state** at the point of failure (variables, data, the relevant store contents), the **stack** or trace, and the **environment** (versions, config, timing conditions). The rarer and less reproducible the failure, the more this matters — for a one-shot production failure, the capture may be the only witness you ever get, and a probe that clears it is irreversible.

## Keep an audit trail as you go

Record each change you make and what happened after it — the experiments run, the values observed, the branches eliminated. This is what makes the elimination auditable, keeps [change-one-thing-at-a-time](change-one-thing-at-a-time.md) honest (you can see what's been varied and reverted), and stops you re-running a test whose answer you already have. A session without a trail re-treads its own ground and loses the thread of what's been ruled out.

## The discriminator: capture first, or regenerate later?

Not everything needs preserving — capturing is not free, and over-capturing buries the signal. The test: **would losing this state cost you the failure or a hard-won observation?** Capture first when the state is *expensive or impossible to regenerate* — a rare trigger, a production-only condition, a timing window, a corrupted store you're about to overwrite. Skip the ceremony when the state is *cheap to reproduce on demand* — a deterministic local failure you can re-trigger in seconds needs no snapshot, just re-run it.

`(basis: Agans' Rule 6, "Keep an Audit Trail" — Debugging: The 9 Indispensable Rules (2002): "write down what you did, in what order, and what happened." Reinforced by incident-response practice (Google SRE, Managing Incidents: "preserve the evidence for root-causing"). The capture-first-vs-regenerate discriminator, keyed to cost-of-regeneration, is the maintainer's house rule to keep the practice proportionate.)`
