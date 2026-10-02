# Auditing

**Entry condition.** The request is to judge the security posture of a whole system or component: no change under review, no author. A security review of one change goes to the [security-review](../../security-review/SKILL.md) skill directly, with `--changed`, as one step's outcome, whoever wrote the change — the reviewing act runs no security pass. security-review reads the local tree, so a hosted change is first materialized through [vcs](../../vcs/SKILL.md)'s *materialize a change* and reviewed in that copy. (basis: maintainer, 2026-09-30)

**Done when** the audit report is filed and its findings have reached the system's owners. (basis: derived from the steps' outcomes)

## Steps

(basis: maintainer, 2026-09-30)

| # | step | inputs | skipped by the act when |
|---|---|---|---|
| 1 | [understand](../../understand/SKILL.md) | the system or component the request names | never |
| 2 | [security-review](../../security-review/SKILL.md), with `--exhaustive` when the request asks for it | the subject, and step 1's map | never |
| 3 | [communicate](../../communicate/SKILL.md) | step 2's findings and posture, for the system's owners | never |

## Filed

Step 1's map files as a section of the task's scratchpad, and step 2's result as the audit report. (basis: derived from the document types' membership tests)

## Delivered

Step 3's message reaches the system's owners per [deliver-through-the-ports](../rules/deliver-through-the-ports.md), linking the audit report, which is published first. When the request asks for it, each finding at or above high is filed as a work-item through [project-mgmt](../../project-mgmt/SKILL.md), with its severity. (routed to maintainer: findings filed as work-items only when the request asks, since filing unasked fills a shared tracker with items nobody triaged.)
