# The severity scale

Every finding security-review keeps carries a severity, and severity is what lets the owner triage: block the release, fix it this sprint, or note it. Leave the scale undefined and each reviewer invents a ladder — one calls a reachable injection "high," another "critical," and the same audit yields two incompatible verdicts, one of which fails a CI gate the other passes. Unlike code-review severity — which has no single external authority, so review's scale is a maintainer house standard — **security severity has an authority: CVSS.** This scale is sourced from CVSS's qualitative bands.

Severity answers one question: **how bad is the consequence, and how easily can a reachable attacker cause it?** It is assigned in [assessing-severity](../phases/04-assessing-severity.md), consumed by [reporting-findings](../phases/05-reporting-findings.md) (the `--severity-min` floor and the ranking) and by [gate-decision](../modules/gate-decision.md) (the pass/fail floor). It rides beside confidence ([confirm-reachability-before-flagging](confirm-reachability-before-flagging.md)) without merging into it — *how bad and how exploitable* versus *how sure the path is real*. And it applies **only after the reachability floor is cleared**: an unreachable sink is dropped, not graded (see [exploit-then-impact](exploit-then-impact.md)).

## The four levels

`(basis: CVSS qualitative severity rating bands — FIRST.org, CVSS v3.1 spec §5 Table 14 and v4.0 spec §7 Table 22, which define identical bands: Critical 9.0–10.0, High 7.0–8.9, Medium 4.0–6.9, Low 0.1–3.9, None 0.0. The rungs and boundaries are CVSS's, not the maintainer's; the per-level prose below maps CVSS's exploitability×impact decomposition (§2) onto a reasoning reviewer's qualitative call, since this skill reasons about severity rather than computing a vector.)`

- **critical** *(CVSS 9.0–10.0)* — a reachable adversary achieves an unrecoverable, wide-blast outcome with little standing in their way: remote code execution, a full authentication bypass, mass exfiltration of sensitive or cross-tenant data, or total compromise — and exploitation needs no privilege, no user interaction, and low complexity.
  - *Anchor (top of scale):* unsanitized request input concatenated into a query on the unauthenticated login path — a remote attacker bypasses auth and reads every user's data.
- **high** *(7.0–8.9)* — a reachable adversary achieves serious impact (significant data exposure, privilege escalation, injection with real consequence, integrity loss on a core flow), but one real precondition bounds it: authentication is required, or a specific configuration, or the blast is one tenant/flow rather than all.
  - *Anchor:* a stored injection that runs in another user's session, reachable only by an already-authenticated account.
- **medium** *(4.0–6.9)* — a real, reachable weakness whose exploitation is meaningfully constrained (needs high privilege, significant user interaction, or an unlikely-but-possible precondition) **or** whose impact is bounded (limited information disclosure, a denial of service on one non-core flow, tampering with low-value state).
  - *Anchor:* a denial-of-service reachable by an authenticated user sending an oversized but bounded payload to one endpoint.
- **low** *(0.1–3.9)* — a reachable weakness where the attacker gains something real but marginal: a minor information leak with no sensitive content, a verbose error exposing a framework version, a weakness exploitable only under conditions that barely qualify as reachable.
  - *Anchor (bottom of scale):* an error response returning a stack trace that reveals the framework and version to any caller — an attacker gains reconnaissance, nothing more.

There is **no "informational" rung** in this scale: CVSS bottoms at Low (its "None"/0.0 is "not a vulnerability," not a severity). A no-impact hardening observation is not a low finding — it has no reachable abuse, so it is not ranked here at all; it goes to the separate hardening section ([separate-finding-from-noise](separate-finding-from-noise.md)). `(basis: keep hardening observations in a separate, unscored section rather than adding an "info" fifth rung — ratified by the maintainer, 2026-07-10. The dominant pentest-report convention, and consistent with CVSS scoring vulnerabilities rather than best-practice notes; CVSS bottoms at Low (its "None"/0.0 is not-a-vulnerability), OWASP Risk Rating's lowest is "Note", and vendor "Info" tiers map to CVSS 0.0 — no authority establishes an informational severity distinct from a low vulnerability. The minority practice models Info as the lowest rung of one scale.)`

## The adjacent-level discriminators

Assign by walking down until a level fits; the boundary tests are what stop a finding sliding between rungs, and each turns on the two axes **exploitability × impact** ([exploit-then-impact](exploit-then-impact.md)):

- **critical vs high** — is exploitation *unconstrained* (remote, no auth, no interaction) *and* the impact *unrecoverable or wide* (RCE, auth bypass, mass/cross-tenant breach)? Critical. Does a real precondition gate it, or is the blast bounded to one flow/tenant? High. (exploitability + blast radius)
- **high vs medium** — does a *plausible* attacker reach serious impact with a *modest* precondition? High. Does it need *high privilege, heavy user interaction, or an unlikely precondition*, or is the impact *bounded/low-value*? Medium. (precondition weight + impact size)
- **medium vs low** — does the attacker gain something of *real consequence* (usable data, a foothold, a working DoS)? Medium. Is the gain *marginal* (version disclosure, a trivial leak) though still a reachable abuse? Low. (impact materiality)
- **low vs not-a-finding** — is there a *reachable adversary who gains anything at all*? Low. Is there *no reachable abuse* (a hardening improvement only)? Not on this scale — it is a hardening note ([separate-finding-from-noise](separate-finding-from-noise.md)).

When two levels both seem to fit, the higher wins only if you can name the attacker, the path, and the impact that justify it; absent that, drop a level. A severity you cannot tie to a concrete reachable consequence is a confidence problem wearing a severity's clothes — re-check it against [confirm-reachability-before-flagging](confirm-reachability-before-flagging.md).

## The severity-authority fork

CVSS is the default authority here, but it is not the only one, and it genuinely does not fit every project — encode the fork rather than pretend it does. Route by: **the project's own security posture and rating convention → the house default (CVSS) → the maintainer**, non-gating.

- **CVSS** — a standardized, technical, intrinsic severity (exploitability × impact of the vulnerability itself). *Strength:* comparable across projects, authoritative, the default. *Cost:* context-blind — its Base score ignores this deployment's likelihood, data sensitivity, and compensating controls, so it can over- or under-state real risk for *this* system.
- **OWASP Risk Rating** — likelihood × impact, with business/technical impact factors the rater fills in. *Strength:* contextual, tuned to the project's actual exposure and data. *Cost:* more subjective, less comparable, needs inputs a code audit may not have. Reach for it when the project rates risk this way or when CVSS's context-blindness distorts the call.
- **The project's own posture** — a bespoke scale keyed to the project's risk appetite and asset classes. *Strength:* matches how the team already triages. *Cost:* not portable, only as good as the project's own rubric. Use it when the surrounding convention ([match-the-projects-security-posture](match-the-projects-security-posture.md)) establishes one.

When an authority other than CVSS governs, say which and grade on it; do not silently swap the anchors. `(basis: CVSS context-blindness is a documented limitation — FIRST positions Base scores as intrinsic, with Environmental metrics for context; OWASP Risk Rating is likelihood×impact per the OWASP methodology. The fork is real; CVSS is the default, not the only, authority.)`
