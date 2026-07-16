# Judge against the surrounding code

A reviewer carries a mental picture of how code *should* look, and the trap is measuring the change against that picture instead of against the codebase it lives in. That produces findings that are technically defensible and practically wrong: flagging a pattern the whole module uses, demanding an abstraction the project deliberately avoids, imposing a naming style foreign to the file. The change's job is to be a good citizen of *this* system, not an exemplar of the reviewer's preferred one. This rule anchors every craft judgment to the local conventions, patterns, and abstractions already present.

## The standard is the neighborhood, not the ideal

Before flagging a craft issue, read enough of the surrounding code to know the local norm: how this module names things, how it handles errors, what abstractions it reaches for, how much indirection it tolerates. Then judge the change against *that*. A change that matches a strong local convention is correct even if you would have chosen differently; a change that breaks the local convention is a real finding even if what it does is defensible in the abstract, because inconsistency itself is a cost the next maintainer pays.

The discriminator for a craft finding: **does this diverge from a pattern the surrounding code actually establishes?** If the neighbors do it this way and the change doesn't, that's the finding. If the change simply isn't how *you* would do it, and the neighbors are silent on the question, that's taste — hold it ([weight-by-impact-not-count](weight-by-impact-not-count.md)).

## When the surrounding code is itself wrong

The local convention is the default standard, not an absolute one. Two cases override it, and naming which you're in keeps the finding honest:

- **A correctness defect is never excused by convention.** If the whole module dereferences without a null check and the change does too, the shared pattern is a shared bug — flag it, at the change's site, and note the pattern. Consistency is a craft bar, not a correctness one; [separate-correctness-from-taste](separate-correctness-from-taste.md) governs which you're applying.
- **A convention the project is actively moving away from** — if there's clear evidence (recent changes, a stated direction) that the local pattern is being replaced, judge against the *new* direction and say so. Absent that evidence, the existing convention wins; do not infer a migration from your own preference.

This is why [build-the-mental-model](../phases/02-build-the-mental-model.md) reads the surrounding code before the craft pass runs: you cannot judge conformance to a convention you haven't read.
