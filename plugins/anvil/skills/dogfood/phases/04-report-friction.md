A dogfood run that ends in a verdict — "it works" / "it doesn't" — wastes everything the run and challenge phases captured. The point was never a grade; it was a list of specific things to fix, each pinned to the file that owns it. This phase turns the run logs and the critics' findings into that list: actionable findings, traced to slots, handed to the skills that can repair them. A finding the maintainer can't act on is noise, and a finding with no file pointer is an opinion.

## Fuse the three sources into findings

You hold three things now: the run logs (friction you hit), the cold-executor's findings (friction you'd have hit cold), and the standards-skeptic's findings (judgments a second run would have made differently). Merge them into a single ranked list of findings. Each finding is one defect in the plugin, stated concretely — not "the skill is confusing" but "step 3 names a capability with nothing behind it for the configured provider, so the run can't proceed." The craft of the conversion — separating a skill bug from a thin scenario, grading on the pinned blocker/friction/nit ladder, ranking by bite — lives in [reading-friction](../rules/reading-friction.md); apply it here, and hold every item to its four-part bar: defect, pointer, evidence, route. An item that can't complete all four parts is not yet a finding — read it further or let it dissolve.

## Tie every finding to a slot file

This is the non-negotiable part: every finding points at the specific file that owns the defect and, where possible, the line or step. *Which* slot kind owns *which* friction is the mapping in [reading-friction](../rules/reading-friction.md) — apply that table here; it is not restated in this phase.

The pointer is what makes the finding repairable. "The release skill is unsafe under dry-run" is a complaint; "phase 02 of release writes a version bump while `--dry-run` is set, contradicting the flag's declared meaning in frontmatter" is a work item. Always produce the second.

## Hand findings to the skills that fix them

Dogfood diagnoses; it does not repair. Route each finding to the authoring skill that owns its repair, so the loop closes:

- A step that stalls, guesses, or leaves a bar open → the skill that fills procedure: re-resolve the decision, pin the bar (or record why it stays open), re-phrase the step at the right altitude.
- A missing flag, module, adapter, or agent reference → the skill that adds components: wire the missing part.
- A structural gap — a slot that should exist and doesn't, a skill that should be split → the skill that lays out skeletons.

State the routing in the report ("phase 02 step → codify; missing module → add-component") so the maintainer sees not just what's broken but where the fix goes. Dogfood writes no fixes itself; its output is a worklist, not a patch.

## Emit findings in one fixed shape

Reports converge across runs only if their shape is pinned, so emit every finding in the same one-line-set shape — grade, defect, pointer, evidence, route:

> **[friction]** `<skill>/phases/02` step 3 — selects a default window without stating it; log: this run assumed the narrowest window, a second run could take the widest → route: codify, to pin the default or record why it's open.

Grades come from the ladder in [reading-friction](../rules/reading-friction.md), assigned by what a second cold run does at that point. Order the findings by bite per the rule's anchors, then close with the coverage notes (below) — never interleaved with the findings, so the worklist stays scannable.

## Honor `--report`

Return the findings inline by default — ranked, each in the fixed shape, prose back to the caller. Under `--report=artifact`, render the same content as a structured page via the configured artifacts backend (or a local file), so a longer self-hosting run has a durable, scannable log instead of a wall of inline text. The content is identical across formats; only the delivery changes. The example deliberately names the *capability* — the configured artifacts backend — not a concrete renderer: which backend produces the page is a wiring concern, not this phase's.

For example, the end of a `--self` run reports: three findings ranked by bite, each in the fixed shape with its grade, pointer, and fix-owner skill; a note that one scenario (the audit skill's untaken branch) was never exercised and should be added next pass; and, under `--report=artifact`, all of it rendered as a page. The maintainer reads it as a closed loop — what broke, where it lives, who fixes it.

Anti-pattern: a report that grades the plugin ("mostly works, minor issues") instead of itemizing. A verdict can't be assigned to a skill, can't be traced to a slot, and can't be re-checked next run. Itemize, point, and route — every time. And scope any summary claim by the sufficiency floor from the pick phase: a set that never chained the primary workflow may report on the paths it walked, never "the plugin works."

One more thing the report must carry: the scenarios that were *never run*. The pick phase closed the set; the challenge phase may have surfaced forks that set never touched. Those untaken paths are real coverage gaps — record them explicitly as "not yet exercised," so the next dogfood pass knows where to aim rather than re-walking the paths this one already cleared.
