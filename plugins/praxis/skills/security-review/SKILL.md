---
name: security-review
description: Audit a change or subject through a threat lens — authn/authz, injection, secret handling, data exposure, supply chain — scoped to a named adversary, and emit substantiated, severity-ranked findings, optionally a machine-readable findings document or a CI gate. The dedicated threat audit, distinct from review's code-review-depth security lens.
metadata:
  flags:
    --changed: narrow the surface to the working-tree diff and its blast radius (touched code plus what newly reaches it), instead of the whole subject
    --threat-model=<framework>: bias the hunt toward a named threat-modeling framework or adversary, weighting which threats to prioritize
    --standard=<framework>: map the findings onto a named standard/compliance framework's control taxonomy and report coverage against it (activates standard-mapping)
    --severity-min=<level>: drop findings below this severity from the report before delivery
    --exhaustive: trade speed for completeness — enumerate every entry point and every threat class rather than the high-likelihood subset
    --sarif=<path>: emit findings as a machine-readable findings document at the path, in addition to the human report (activates sarif-output)
    --gate: reduce the run to a pass/fail verdict for CI — fail when a finding meets the configured severity bar (activates gate-decision)
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

security-review owns no backend of its own. It reads the subject — and, under `--changed`, the local working-tree diff and its base — **ambiently**, needing no configured backend, exactly as review reads a local diff. (A change *hosted* on a version-control host would be a vcs-capability delegation to the `vcs` skill, which owns `tools.vcs` under doer-owns-prerequisites — but this skill takes no hosted-change flag.) Emitting a findings document (`--sarif`) is a local file write and the gate verdict (`--gate`) is a local exit status. So it declares **no `config_requires`**.

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

1. Scope the surface: resolve what is under audit and map its trust boundaries, entry points, assets, and the attacker's reachable surface  — see [phases/01-scoping-the-surface.md](phases/01-scoping-the-surface.md)
2. Model the threats: derive who the adversary is, what they want, and which attack classes the architecture actually exposes  — see [phases/02-modeling-the-threats.md](phases/02-modeling-the-threats.md)
3. Hunt vulnerabilities: trace tainted input to dangerous sinks across the surface, probing each threat class deliberately rather than pattern-matching keywords  — see [phases/03-hunting-vulnerabilities.md](phases/03-hunting-vulnerabilities.md)
4. Assess severity: for each candidate, establish exploitability and impact, confirm reachability, and discard what is unreachable or already mitigated  — see [phases/04-assessing-severity.md](phases/04-assessing-severity.md)
5. Report the findings: write each confirmed finding as attacker-path + impact + concrete remediation, ordered by severity, with enough evidence to act on  — see [phases/05-reporting-findings.md](phases/05-reporting-findings.md)
