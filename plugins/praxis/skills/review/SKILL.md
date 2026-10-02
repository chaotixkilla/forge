---
name: review
description: Critically read a diff or a hosted change for correctness, craft, and risk at a chosen rigor level; surface findings ranked by severity and certainty — optionally as a CI gate.
metadata:
  flags:
    --rigor=<low|medium|high|max>: how broadly to hunt and how high to set the certainty bar — praxis's own dial, independent of the model's effort setting; `max` asks before starting
    --changed: scope to the working-tree diff against the base (the default window)
    --change=<ref>: review a hosted change (a review request) — its diff + description via the vcs capability; --pr=<number> is accepted as an alias (activates hosted-change)
    --hold-rationale: judge the change against the intent its caller supplies, reading none of the author's rationale — description, commit messages, linked threads — so a later pass can read it last (activates the hold-rationale module)
    --prior=<review>: build on a prior pass over the same change — its report, or where it was filed — reading the author's rationale against it instead of hunting afresh (activates the prior-pass module)
    --lenses=<list>: restrict the defect and craft passes to a named subset of these twelve — correctness: logic, boundary, error-paths, concurrency, security, resource-safety, data-integrity; craft: reuse, simplification, efficiency, altitude, comments
    --severity-min=<level>: drop findings below this severity before delivery
    --typed: also emit the findings to the harness's typed finding channel as structured records, alongside the report (activates typed-findings)
    --gate: turn the review into a check whose result fails on a traced or observed finding at or above the floor, holds when none remains, or is not checked when the review halted (activates gate-mode)
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

1. Scope the review: resolve what's under review and load enough surrounding code to judge it  — see [phases/01-scope-the-review.md](phases/01-scope-the-review.md)
2. Build the mental model: understand what the change is trying to do before judging it  — see [phases/02-build-the-mental-model.md](phases/02-build-the-mental-model.md)
3. Hunt for defects: pass over the change for correctness bugs, sized to the rigor level  — see [phases/03-hunt-for-defects.md](phases/03-hunt-for-defects.md)
4. Assess craft: a separate pass for reuse, simplification, efficiency, and consistency  — see [phases/04-assess-craft.md](phases/04-assess-craft.md)
5. Triage and rank: validate each candidate, assign severity and certainty, drop below the bar, order by what matters  — see [phases/05-triage-and-rank.md](phases/05-triage-and-rank.md)
6. Deliver the findings: render the survivors to the chosen sink, anchored to file:line  — see [phases/06-deliver-findings.md](phases/06-deliver-findings.md)
