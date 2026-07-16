This is the pass the audit exists for: take the directed threat list and, for each threat, find the concrete reachable path that realizes it — or establish that none exists. The discipline that separates a real audit from a scanner run is here: hunt by *tracing tainted data to sinks* and *checking for the control that should exist*, not by grepping for dangerous function names. A keyword sweep flags the unreachable and misses the plainly-named sink that hostile data reaches; a traced hunt finds what an attacker would actually use.

## Sweep the threat classes deliberately

For each threat on the list from [modeling-the-threats](02-modeling-the-threats.md), work the two complementary methods, aimed at the boundary the threat targets:

- **Trace the tainted data** ([follow-the-tainted-data](../rules/follow-the-tainted-data.md)): from an adversary-controlled source, follow the value hop by hop to a dangerous sink, and check whether a sanitizer, parameterizer, or allow-list breaks the chain. Construct the hostile value first ([assume-the-input-is-hostile](../rules/assume-the-input-is-hostile.md)).
- **Check for the missing control** ([absence-is-a-finding](../rules/absence-is-a-finding.md)): for each boundary and sink, name the defense the surface owes — an authorization check, validation, a rate limit, output encoding — and confirm it is present, judged against how the project already defends itself ([match-the-projects-security-posture](../rules/match-the-projects-security-posture.md)).

The attack classes to carry across the surface — authn/authz, injection, secret handling, data exposure across a trust boundary, and supply-chain trust — are the recurring shapes the threat model points the hunt at. Breadth is set by `--exhaustive` (a phase input): the default works the high-likelihood classes the threat model prioritized; `--exhaustive` carries *every* class against *every* entry point, including the low-likelihood combinations.

## The attack-class taxonomy — a sourced default, a routed fork

Findings are named against a taxonomy so they are legible and comparable, and the taxonomy the sweep organizes by (and that `--standard` maps onto) has a sourced default and a routed fork. As with the framework, the authorities frame these as **complementary layers of different granularity, not rivals** — a finding pins to a specific CWE weakness, which rolls up into a broad OWASP Top 10 category; ASVS is a different axis (requirements to verify, not a label for a discovered bug). Route by **surrounding convention → house default → maintainer**, non-gating:

- **OWASP Top 10** *(the default)* — ~10 broad, widely-recognized application-risk categories. *Strength:* the recognized baseline; communicates a finding's class to any developer at a glance. *Cost:* coarse — a category, not a precise root cause.
- **CWE** — the exhaustive weakness dictionary (hundreds of specific types). *Strength:* precise root-cause identification and cross-tool correlation; a finding pins to a CWE ID. *Cost:* granular and large; overkill for coarse communication. Reach for it when a finding needs a precise, correlatable identifier.
- **ASVS** — a verification-requirements standard with assurance levels (L1/L2/L3). *Strength:* a testable pass/fail security bar. *Cost:* a *different axis* — a requirements checklist to verify against, not a label for a discovered vulnerability. Reach for it when the audit's job is to verify coverage against a defined bar rather than enumerate findings.

`(basis: default attack-class taxonomy = OWASP Top 10 (current edition) when --standard is unset and the project shows no established convention — ratified by the maintainer, 2026-07-10. Sourced from: OWASP's own framing of the Top 10 as the "standard awareness document" and "globally recognized first step" — the broadest-recognized category baseline, the right default for legible findings. CWE is the fine-grained ID beneath it, reached for precision; ASVS is a verification axis, reached via --standard when the job is coverage.)`

When `--standard=<framework>` is set, map each candidate onto that framework's controls as it is found and report coverage — see [standard-mapping](../modules/standard-mapping.md).

## Trace across the blast radius, and hunt with an adversary

A sink is judged in the context that reaches it, so carry each candidate out through the surface until you can state the full path from an entry point to the sink — recruit the **code explorer** to trace paths beyond the immediate file; without fan-out, trace them yourself before recording the candidate. Recruit the **security-auditor** critic as the primary threat lens (it reasons backward from abuse to sink), and at `--exhaustive` add the **adversary** critic for a general red-team pass over the same surface; without fan-out, apply both lenses yourself — for each threat, actively construct the attack rather than reading for confirmation the code is safe.

Record each candidate anchored to its `file:line` and its path (the source, the sink, and the boundary crossed) — an unanchored candidate cannot be triaged. Do **not** grade severity here; the output of this phase is a set of *candidate* findings, each a traced-or-suspected path, handed to [assessing-severity](04-assessing-severity.md) to confirm reachability, grade, and filter. A candidate you could not trace to a reachable path is carried as *suspected*, for that phase to confirm or drop — never silently kept or silently discarded.
