# Separate the finding from the noise

A security report is trusted in proportion to its signal. Pad it with hardening suggestions dressed as findings and the reader can no longer tell the reachable breach from the nice-to-have — the critical issue is *diluted* by the dozen defense-in-depth notes around it, and a report that cries wolf gets triaged like one. This rule draws the line security review lives or dies on: an **exploitable finding** (a reachable adversary gains something concrete) is ranked and reported; a **hardening nit** (a robustness improvement with no reachable abuse) is kept separate, unranked.

## The line: what the attacker gains, today

The discriminator is a single question: **can you name the adversary, the reachable path, and the concrete thing they gain — a read, a write, an execution, an exfiltration, a privilege they shouldn't have?**

- **Yes → an exploitable finding.** It goes in the ranked list, graded on [severity-scale](severity-scale.md), anchored to its path. "An attacker gains X" is the shape.
- **No → a hardening observation.** "This would be more robust," "defense-in-depth," "best practice would add Y" — a real improvement that reduces risk but grants no reachable abuse *today*. It is worth surfacing, but it does not compete with the exploitable findings for the reader's attention.

The fuzzy edge is a *low-severity real vuln* versus a *hardening nit*, and the tie-breaker is reachability, not size: if a reachable adversary gains anything at all, however small, it is a low finding (it has an attacker and a path); if no adversary gains anything today, it is hardening, no matter how sound the advice. When you cannot construct the abuse, it is hardening — resolve the doubt toward the separate section, because a wrongly-ranked nit costs more trust than a rightly-separated one.

## Where the hardening notes go

Keep hardening observations in their own section of the report, **not scored and not ranked** with the exploitable findings ([reporting-findings](../phases/05-reporting-findings.md)) — surfaced for the author's judgement, explicitly outside the severity ladder. Do not inflate a nit's severity to justify keeping it in the main list, and do not manufacture hardening notes to look thorough: a short, high-signal report is the goal, and silence on a clean surface is a valid result.

`(basis: pentest-report convention corroborated across ~6 independent 2024–2026 sources — informational/hardening items go in a separate section, unscored, "not security vulnerabilities on their own," and padding them into the ranked list dilutes the real findings; consistent with CVSS scoring vulnerabilities rather than best-practice recommendations. The low-vuln-vs-hardening boundary is the one practitioners call genuinely fuzzy; the reachable-abuse tie-breaker is the pin. The separate-unscored placement (vs. an "info" fifth rung) is ratified in [severity-scale](severity-scale.md).)`
