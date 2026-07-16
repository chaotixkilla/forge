# Find the source of truth

Every source that *describes* a system can be wrong about it. A comment describes the code as it was two refactors ago; a doc describes the contract the author intended, not the one they shipped; a name promises what the body never delivers; a commit message explains a change a later commit undid. understand's whole value is a map of what the system *actually does* — so when sources disagree, the skill needs a fixed rule for which one it obeys, or two investigators resolve the same conflict differently and the map is only as reliable as who ran it. This rule pins that ordering.

## The ordering: behavior over description

`(basis: the follow-execution ethos — [follow-execution-not-names](follow-execution-not-names.md) — that names understand's reason for existing, plus the gather sourcing-model rule that project reality diverging from a norm is a finding, not a tie to average away ([gather](../../gather/SKILL.md), ratified 2026-07-03). The two-tier split and the surface-don't-reconcile discipline are principled from that ethos, not a house preference — ratified by the maintainer as a principled pin, not a fork, 2026-07-09.)`

Sources split into two tiers by *what they are evidence of*:

- **Tier 1 — evidence of what the code does.** Runtime behavior you observed; a test you watched exercise the path and pass; the traced code path itself. These *are* the behavior, or a direct execution of it.
- **Tier 2 — claims about what the code does.** Official docs, comments, commit messages, human/tribal knowledge, and the symbol names themselves. Each is someone's description of the behavior, which may or may not still match it.

The rule, for any question about **what the system does**: **Tier 1 wins.** Believe the code's actual behavior over any description of it. Names, comments, and docs are the author's *intent*; the thing you are mapping is exactly where intent and behavior diverge.

When the system under study is *declarative* rather than executable — a config, a schema, an IaC manifest, a skill — its own **operative text is Tier 1** (the artifact *is* what the interpreter obeys), while comments and docs *about* it stay Tier 2; the "behavior" you weigh against is how the interpreter consumes that text ([separate-fact-from-inference](separate-fact-from-inference.md), "when the system is declarative").

When you cannot reach Tier 1 (the path is unobservable and unread) and must rely on Tier 2, rank the Tier-2 sources by the sourcing model gather returns (which already tiers official-docs as authoritative, code/repository as ground truth, community as anecdotal, knowledge-base as recorded-intent-with-staleness). Ranking picks *which description to relay*; it does not raise how *certain* the claim is. The certainty rung is the scale's call, and its owner is [separate-fact-from-inference](separate-fact-from-inference.md): a behavior claim resting only on a description, with no first-hand read of the code, is **assumed-unverified** until you check it — however authoritative the source that described it. (Ranking a doc above a comment makes the doc the one you relay; it does not make the claim traced.)

## A divergence is a finding, not a tie to break

When a Tier-2 claim contradicts Tier-1 evidence — the doc says the endpoint rejects negative amounts, the code accepts them — do **not** silently pick one and move on. The divergence is itself a finding in the map: a **bug** when the code violates a contract that is a real requirement, a **stale/wrong description** when the code is right and the doc lags, or an **open divergence** when which is authoritative isn't yours to decide. (basis: gather's surface-conflicts-not-consensus — project reality vs. norm is reported, never averaged.) Reconciling it silently hides exactly the discrepancy a reader most needs to see.

## What this rule is not
It does not rank the Tier-2 sources against each other from scratch — that cross-lane weighing is gather's sourcing model, which understand consumes in [corroborate-against-reality](../phases/04-corroborate-against-reality.md). This rule owns only the behavior-over-description ordering and the surface-the-divergence discipline. Cited from [corroborate-against-reality](../phases/04-corroborate-against-reality.md) and [synthesize-the-answer](../phases/05-synthesize-the-answer.md).
