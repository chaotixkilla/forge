The change is made and verified; this phase makes it *reviewable and attributable*, then stops. Maintenance that lands as an opaque diff with no rationale is maintenance the next person can't trust or safely build on. The deliverable is a clean, self-explaining diff, the reasoning behind it, a regression guard already in place from [phase 04](04-verify-and-guard.md), and whatever record the project expects — no more. maintain does not judge its own change (that's [review](../../review/SKILL.md)) or land it into a shared line (that's [integrate](../../integrate/SKILL.md)); it produces the change and the record and hands off.

## Make the diff self-explaining

Read your own change as a hostile reviewer before recording it (**judgment**): is the diff about the one thing it set out to do, or has unrelated cleanup crept in? Are there leftovers — debug prints, dead scaffolding, a half-applied rename? Does each hunk explain itself, or does it need a comment the change should carry? Fold in nothing that fails the [leave-the-campsite-cleaner](../rules/leave-the-campsite-cleaner.md) line; strip what doesn't belong.

## Record what the project expects

First, **commit the change locally** — a local commit done directly (ambient plain git, no delegation and no backend; maintain never pushes), honoring the project's commit-message convention. **Stage only the paths this change's edits actually modified** — not the whole working set (a `--scope`/`--module` bound can contain files this change never touched) — and leave *all* other uncommitted work untouched, whether unrelated or merely in-scope-but-unedited, so the commit is attributable to this change and nothing else. If `--checkpoint-commit` was set the milestone commits already exist; this is the final attributable commit. Never push unless asked.

Then compose the *record* and delegate each part to the skill that owns it (a **delegating step** — state the fallback inline):
- **The work-item / ticket update** → the [project-mgmt](../../project-mgmt/SKILL.md) skill. **A human notification** → the [communication](../../communication/SKILL.md) skill, **when the change warrants one**: notify on an `exposed`-tier change (its reach extends past the team, so affected owners/consumers need warning) or when the caller explicitly asked; a `contained` or `bounded` internal change warrants none. Route *who* to notify by the `--module` **ownership metadata** from [phase 01](01-locate-and-reproduce.md) when set. `(basis: the notify-whether threshold is keyed to the risk tier — an exposed change reaches beyond the team — plus explicit caller request; derived and tied to change-risk-scale so the two stay consistent.)`
- **Fallback:** where a record capability isn't configured, don't drop the record silently — leave the clean diff and the written rationale locally and state plainly which records couldn't be written, so the maintainer can complete them. The owning skill's `if_missing` posture governs.

## `--changelog`

When `--changelog` is set, additionally emit a user-facing changelog / release-note entry — see [changelog-entry](../modules/changelog-entry.md). Like any record written for a human audience, it's a clean export: the change and why it matters, none of maintain's internal machinery.

## Surface the follow-ups

Record the out-of-scope needs the change deliberately did *not* fold in ([leave-the-campsite-cleaner](../rules/leave-the-campsite-cleaner.md)) — the deferred cleanups, the labeled stopgaps from [fix-the-cause-not-the-symptom](../rules/fix-the-cause-not-the-symptom.md), and coverage the *change itself made necessary* — new behavior or branches it introduced that the [phase-01](01-locate-and-reproduce.md) baseline does not cover. Those are the change-made-necessary work **Q2** turns on. The tell is *is the coverage gap new*, not *is the code new*: a behavior-preserving refactor's extracted or relocated code is covered by the same baseline, so its lack of dedicated tests is a **pre-existing** gap — a **routine hygiene note** surfaced as advice for [test](../../test/SKILL.md) that does **not** make the run partial (it stays *recorded*). A surfaced follow-up is captured work; a dropped one is lost.

## The disposition — a decided partition

Every run ends in exactly one of three dispositions. Decide it with two questions, **in order** — this decision procedure is what keeps the three values exhaustive and mutually exclusive, so a novel case still lands in exactly one:

**Q1 — did the in-scope change land?** (get made, reach a trustworthy verdict, and get its record written.) A run does **not** land when a gate refused it, for *any* cause:
- `--require-clean` refused a dirty tree ([phase 01](01-locate-and-reproduce.md));
- the `--security` bar blocked ([phase 04](04-verify-and-guard.md));
- the verify verdict was **not-verified** or **inconclusive** *and* the correction lies outside this change's scope ([phase 04](04-verify-and-guard.md)) — an *in-scope* failure instead loops back to [make-the-change](03-make-the-change.md) and is not terminal;
- the change is `exposed` and no migration path can be built within scope ([phase 03](03-make-the-change.md)) — including a dependency bump that moves a separately-deploying consumer with no in-scope way to migrate it.

Any of these → **blocked-and-reported**: report what blocked and what would unblock it (including *whom to coordinate with* — e.g. the owners of a consumer a shared-resolved bump would move). Nothing is recorded as landed. This disposition is defined by its *cause* — a gate refused — not by a fixed list, so a novel refusal still lands here rather than escaping the partition.

**Q2 — if it landed, did the change surface out-of-scope WORK that still must be done?** — a needed change outside the working set, a labeled stopgap's real cause-fix, a co-consumer a shared fix motivates bumping ([leave-the-campsite-cleaner](../rules/leave-the-campsite-cleaner.md)).
- **Yes** → **partial-with-surfaced-followups**: the in-scope change landed and reached a verdict; the deferred work is recorded so it isn't lost.
- **No** → **recorded**: the normal landing. A *routine hygiene note* — "this area is thinly tested," a pre-existing gap the change did not create — is **not** the deferred work that makes a run partial; it's surfaced as advice and the run is still **recorded**. Partial is for work *the change itself* makes necessary, not for every observation — otherwise every no-tests refactor would read as "partial" and the distinction would carry no information.

The two questions partition every run: it either landed (Q1) or it didn't; if it landed, it either carries change-made-necessary follow-up work (Q2) or it doesn't.

## Stop at the handoff

The clean, recorded diff is the end of maintain's mandate. Judging it is [review](../../review/SKILL.md)'s job; landing it into the trunk is [integrate](../../integrate/SKILL.md)'s. Do not review or merge your own work here.
