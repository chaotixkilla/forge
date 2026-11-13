# Audit report

A security audit's account of a system's posture, for the system's owners.

**Reader and question.** Decider and auditor: "what can an attacker do to this system now, and what do we fix first?"

**Page.** `own page`

## Membership

The security-review step's result in an auditing task ([reporting-findings](../../../security-review/phases/05-reporting-findings.md)). (basis: derived from the deliverable of the act that files it)

## Items

**Security finding `SEC`.**
- Fields: `severity` enum `critical`, `high`, `medium`, `low` ([severity-scale](../../../security-review/rules/severity-scale.md)); `certainty` enum `traced`, `inferred`, `unverified` ([results-and-certainty](../../../../craft/evidence/results-and-certainty.md)), with no `observed` because the audit executes nothing; `location` text; `adversary` text, who they are and what they control; `path` text, source to sink, the boundary crossed and the missing guard; `impact` text; `fix` text, the smallest change that breaks the path; `work item` text, its link when the request had it filed.
- Granularity: one reachable abuse. Several symptoms of one root cause are one finding with several locations.
- Change regime: `baseline`.
- Agreement: `none`.
- Live fields: `work item state` — project-mgmt: the filed work item's status.

A hardening note has no reachable abuse and no grade, so it is a line of prose, not an item.

## Sections

(basis: maintainer, 2026-10-02, for the order)

1. **What can an attacker do here?** Always. The posture line, then the verdict line, as [reporting-findings](../../../security-review/phases/05-reporting-findings.md) words them, empty cases included. When the top finding is restricted, the posture line gives only its id and severity, since the line would otherwise show its path. (basis: derived from [items-and-agreements](../items-and-agreements.md)' sensitivity)
2. **What was audited?** Always. The scope line: surface, breadth, framework and adversary, and what was excluded.
3. **What do we fix?** Always. The finding cards.
4. **What would harden it further?** When the review kept hardening notes. A list, unscored.
5. **Which controls does it cover?** When the audit ran against a standard. The coverage section as the review gives it.

## Checks

- *Computed:*
  - every `SEC` has `location`, `path` and `fix` (basis: security-review's fixed finding record);
  - the verdict line's counts equal the standing `SEC` on this page by severity, with the restricted ones counted in the line that says how many the page leaves out;
  - an empty verdict says which empty: nothing cleared the floor, or every finding was withheld below a severity filter.
- *Judgment:*
  - a finding graded by its weakness class rather than by exploitability and impact;
  - a hardening note promoted to a finding, or a finding demoted to hardening to soften the verdict;
  - a scope that doesn't say what was left out, so the report's silence reads as clean.

## Views

- **Finding cards** (section 3): `cards` of every `SEC`, sorted by `severity` then `certainty`, each descending: severity, certainty, location, adversary, path, impact, fix, `work item state`.

## Minimum form

The posture and verdict lines as the empty verdict, the scope line, and "no findings".
