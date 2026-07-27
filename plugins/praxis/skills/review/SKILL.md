---
name: review
description: Critically read a diff or PR for correctness, craft, and risk at a chosen effort level; surface findings ranked by severity and confidence — optionally as comments, applied fixes, or a CI gate.
metadata:
  flags:
    --effort=<low|medium|high|max>: rigor dial — how broadly to hunt and how high to set the confidence bar
    --changed: scope to the working-tree diff against the base (the default window)
    --pr=<number>: review a remote pull request's diff + description via the vcs capability
    --comment: publish findings back through the vcs capability instead of returning them locally
    --inline: with --comment, anchor each finding to its exact line rather than one summary comment
    --fix: apply the accepted findings to the working tree as edits
    --lenses=<list>: restrict the defect and craft passes to a named subset of these eleven — correctness: logic, boundary, error-paths, concurrency, security, resource-safety, data-integrity; craft: reuse, simplification, efficiency, altitude
    --severity-min=<level>: drop findings below this severity before delivery
    --gate: turn the review into a pass/fail check that exits non-zero on findings at or above the floor
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

1. Scope the review: resolve what's under review and load enough surrounding code to judge it  — see [phases/01-scope-the-review.md](phases/01-scope-the-review.md)
2. Build the mental model: understand what the change is trying to do before judging it  — see [phases/02-build-the-mental-model.md](phases/02-build-the-mental-model.md)
3. Hunt for defects: pass over the change for correctness bugs, sized to the effort level  — see [phases/03-hunt-for-defects.md](phases/03-hunt-for-defects.md)
4. Assess craft: a separate pass for reuse, simplification, efficiency, and consistency  — see [phases/04-assess-craft.md](phases/04-assess-craft.md)
5. Triage and rank: validate each candidate, assign severity and confidence, drop below the bar, order by what matters  — see [phases/05-triage-and-rank.md](phases/05-triage-and-rank.md)
6. Deliver the findings: render the survivors to the chosen sink, anchored to file:line  — see [phases/06-deliver-findings.md](phases/06-deliver-findings.md)
