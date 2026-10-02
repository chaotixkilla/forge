Take the directed threat list and, for each threat, find the concrete reachable path that realizes it — or establish that none exists. Hunt by *tracing tainted data to sinks* and *checking for the control that should exist*, not by grepping for dangerous function names.

## Sweep the threat classes deliberately

For each threat on the list from [modeling-the-threats](02-modeling-the-threats.md), work the two complementary methods, aimed at the boundary the threat targets:

- **Trace the tainted data** ([follow-the-tainted-data](../rules/follow-the-tainted-data.md)): from an adversary-controlled source, follow the value hop by hop to a dangerous sink, and check whether a sanitizer, parameterizer, or allow-list breaks the chain. Construct the hostile value first ([assume-the-input-is-hostile](../rules/assume-the-input-is-hostile.md)).
- **Check for the missing control** ([absence-is-a-finding](../rules/absence-is-a-finding.md)): for each boundary and sink, name the defense the surface owes — an authorization check, validation, a rate limit, output encoding — and confirm it is present, judged against how the project already defends itself ([match-the-projects-security-posture](../rules/match-the-projects-security-posture.md)).

The attack classes to carry across the surface — authn/authz, injection, secret handling, data exposure across a trust boundary, and supply-chain trust — are the recurring shapes the threat model points the hunt at. The hunt works the high-likelihood classes the threat model prioritized; [exhaustive](../modules/exhaustive.md) carries every class against every entry point.

## The attack-class taxonomy

Name each finding against the taxonomy [attack-class-taxonomy](../rules/attack-class-taxonomy.md) selects — its house default, or the project's convention or `--standard` where one applies.

When `--standard=<framework>` is set, map each candidate onto that framework's controls as it is found and report coverage — see [standard-mapping](../modules/standard-mapping.md).

## Trace across the blast radius, and hunt with an adversary

A sink is judged in the context that reaches it, so carry each candidate out through the surface until you can state the full path from an entry point to the sink — recruit the **code explorer** to trace paths beyond the immediate file; without fan-out, trace them yourself before recording the candidate. Recruit the **security-auditor** critic as the primary threat lens (it reasons backward from abuse to sink), plus the red-team pass under [exhaustive](../modules/exhaustive.md); without fan-out, apply the lens yourself — for each threat, actively construct the attack rather than reading for confirmation the code is safe.

Record each candidate anchored to its `file:line` and its path (the source, the sink, and the boundary crossed) — an unanchored candidate cannot be triaged. Do **not** grade severity here; the output of this phase is a set of *candidate* findings, each a traced-or-suspected path, handed to [assessing-severity](04-assessing-severity.md) to confirm reachability, grade, and filter. A candidate you could not trace to a reachable path is carried with its reachability unestablished, for that phase to place or drop — never silently kept or silently discarded.
