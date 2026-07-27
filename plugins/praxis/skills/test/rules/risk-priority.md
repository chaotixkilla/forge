# The risk-priority scale

[design-the-cases](../phases/03-design-the-cases.md) always has more candidate cases than case budget, so it must order and prune them — and "prioritize by risk" with no defined scale means each executor ranks on a different axis: one by likelihood, one by blast radius, one by how easy the case is to write. The same candidate set then produces two different suites. This rule pins the scale so [coverage-adequacy](coverage-adequacy.md) has a defined notion of "the highest-risk behaviors" it requires covered.

Risk answers one question: **how likely is this behavior to break, and how bad is it if it does?** — likelihood × blast-radius. It is assigned in [design-the-cases](../phases/03-design-the-cases.md) and feeds [coverage-adequacy](coverage-adequacy.md) (a High-risk behavior left uncovered blocks "adequate").

## The three levels

`(basis: risk = likelihood × impact/blast-radius is the shared frame of every risk-based-testing authority — ISO/IEC/IEEE 29119 (risk-based testing); James Bach, "Heuristic Risk-Based Testing"; NIST SP 800-30 Rev.1. The 3-tier High/Medium/Low shape is 29119's "most common" scheme. The likelihood factors are Bach's Generic Risk List; the impact factors are the standard consequence axes. All treat the levels as qualitative/ordinal — a risk score is relative order, never an absolute measurement — 29119.)`

- **high** — a behavior that is both *likely to break* — it is new, complex, heavily changed, historically buggy, crosses many up/downstream dependencies, integrates third-party code, or was rushed (Bach's list) — **and** *high blast-radius* — failure corrupts data, breaches security / auth / payments, takes down a core flow, or is hard to reverse.
  - *Anchor (top of scale):* a rewritten auth-token validation on the login path — new code, security-critical, unrecoverable if wrong. Both factors maxed.
- **medium** — *either* factor high but not both, *or* a real failure mode on a non-core flow: a plausible break with bounded, recoverable blast radius, or a high-impact area touched by a small, isolated change.
  - *Anchor:* a changed pagination helper used by one feature — plausible to break, but the blast radius is one bounded, recoverable flow.
- **low** — *unlikely to break* **and** *bounded / recoverable* if it does: a small, isolated, mechanical change to non-critical code, or a well-covered pure function given a trivial tweak.
  - *Anchor (bottom of scale):* a user-facing copy-string change, or a rename the compiler enforces.

## The adjacent-level discriminators

- **high vs medium** — are *both* likelihood and blast-radius high? high. Is only one high (a likely break with trivial consequence, or a catastrophic consequence on a change unlikely to break)? medium. (the both-factors test)
- **medium vs low** — is there a *plausible, reachable input* on which the behavior breaks with a consequence a maintainer would care about? medium. Is a break both unlikely *and* trivially recoverable or cosmetic? low. (real-reachable-failure vs cosmetic / trivially-reversible)

Rank the kept candidates high → low and spend the case budget top-down: every High-risk behavior must be covered, Medium as budget allows, Low only when cheap. Prune a candidate only when a higher-or-equal-risk case already fails on the same defect (the discriminating-vs-redundant test in [design-the-cases](../phases/03-design-the-cases.md)). Any numbers are relative order only, never an absolute measurement.

`(basis: ratified by the maintainer, 2026-07-10. The three levels + anchors above are the house standard. The rung cut-points have no external anchor — ISO 29119 leaves the scale to the organization, Bach declines a fixed one ("no calculator"), and the standards that DO pin boundaries (NIST 800-30, MIL-STD-882E) anchor them in infosec-threat and system-safety domains (lives, dollars), not code change — so the boundaries are the maintainer's ratified call.)`
