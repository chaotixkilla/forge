The hunt produces *candidates* — some are reachable breaches, some are sinks nothing hostile reaches, some are hardening nits, some are suspicions not yet traced. Turn that pile into the trustworthy, ranked list the owner acts on.

## Confirm reachability — the floor, not a downgrade

Take each candidate and clear the reachability bar before anything else ([confirm-reachability-before-flagging](../rules/confirm-reachability-before-flagging.md)): can you name an adversary-controlled source, a real entry point, a traced path to the sink, and the absence of a neutralizing guard? Recruit the **adversary** critic with the inverted lens — "assume this is a false positive: argue the path is unreachable or already guarded" — and keep only the candidates that survive; without fan-out, argue the opposing case yourself for each before letting it stand.

A candidate that fails the floor is **dropped, not graded low** — or, where a missing second layer is worth improving, carried as a hardening note ([confirm-reachability-before-flagging](../rules/confirm-reachability-before-flagging.md)) — never a graded finding: an unreachable sink is noise, and reporting it is exactly what burns the audit's credibility. A candidate whose reachability you cannot establish either way is not dropped and not asserted: it survives at **unverified** certainty, labelled, for the report to carry honestly.

## Grade the survivors — severity and certainty, separately

For each survivor that cleared the floor, assign two independent grades:

- **Severity** — how bad and how exploitable, on the four bands (critical / high / medium / low) and their assignment tests defined in [severity-scale](../rules/severity-scale.md), assigned by decomposing the finding into exploitability × impact ([exploit-then-impact](../rules/exploit-then-impact.md)) — never by the weakness class in the abstract.
- **Certainty** — how sure the path is real, on the certainty scale of [results-and-certainty](../../../craft/evidence/results-and-certainty.md) (traced / inferred / unverified), placed per [confirm-reachability-before-flagging](../rules/confirm-reachability-before-flagging.md) from how much of the attack path you actually traced.

Keep them orthogonal: a version leak traced as reachable is low severity / traced certainty; a suspected remote-code-execution sink you traced no path to is critical severity / unverified certainty — and honest labelling of the second is more valuable than either dropping it or dressing it as certain.

## Separate the hardening notes, then apply the floor

Pull the hardening observations out of the ranked set ([separate-finding-from-noise](../rules/separate-finding-from-noise.md)): a candidate with no reachable abuse — a defense-in-depth improvement, a best-practice suggestion — is real but is **not** a graded finding. Hold it for the separate, unscored hardening section in [reporting-findings](05-reporting-findings.md); do not inflate its severity to keep it in the main list, and do not manufacture such notes to look thorough.

Then apply `--severity-min` when the caller set one: it is a **reporting filter over the graded list**, not a hunting limit — you graded everything that cleared the floor; you deliver only what also clears `--severity-min`. Merge duplicates — three symptoms of one root cause are one finding with three locations, never three findings — and resist raising a finding's severity to justify keeping it above the floor. The hardening section is unscored, so `--severity-min` doesn't filter it.

When `--severity-min` removed every graded finding, the result is not a clean one: report how many were withheld below the filter and the highest severity among them. If nothing survived the floor itself, that is the result: a surface whose trust holds returns **no reachable abuse found for the adversary modeled**, and saying so — explicitly, with the surface that was audited — is a valid and valuable audit. The output is a validated, graded, floored, ranked list plus a separate hardening set, ready for [reporting-findings](05-reporting-findings.md) to render.
