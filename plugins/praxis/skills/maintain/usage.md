# maintain — usage

Perform a scoped, reversible change to living code — a dependency upgrade, a refactor, a deprecation, tech-debt paydown, or security/compliance hardening — sized to its blast radius, verified and regression-guarded, and left as a clean diff someone can review and attribute.

## When to use
- The code works (or works well enough) and you want to keep it healthy: bump a dependency, refactor for clarity, retire a deprecated path, pay down debt, or harden a weak spot — without changing what the system is *for*.
- You want the change done *safely*: located against the real code, its reach understood before editing, staged behind a guard when it's risky, and reversible if it goes wrong.
- You want the result to land reviewable — a self-explaining diff, the rationale, a regression guard for anything it fixes, and the record the project expects.
- You want to bound the work to a subset — a path glob, a named subsystem, or just what already moved — and treat everything outside that bound as a follow-up, not a silent extra.

## Not for / use instead
- Root-causing a specific failure that has already bitten → **debug**. Both reproduce a current state and leave a regression guard, but debug chases *one failure* from symptom to confirmed mechanism; maintain performs *scoped upkeep* on code that isn't necessarily failing. If the task is "find why this broke," that's debug; "improve/upgrade this safely" is maintain.
- Building new work — a feature, a new module, net-new behavior → **develop**. Both edit to the surrounding convention, but develop *adds* capability the system didn't have; maintain *changes existing* code without expanding what it does. New behavior is develop even when it touches old files.
- Judging a change someone wrote — correctness, craft, risk → **review**. review *reads and judges* a finished change and returns findings; maintain *makes* the change. Reach for review to evaluate a diff, maintain to produce one.
- Landing a change into a shared line — merge, resolve conflicts, sequence the integration → **integrate**. integrate *moves finished work* into the trunk; maintain *changes the work itself*. Once the maintenance diff is clean, handing it onward to land is integrate's job.
- Authoring or running the test suite as the deliverable → **test**. test *designs and runs* coverage and reports a verdict; maintain adds the *one regression guard* for the specific failure it fixed and runs the existing checks, then **delegates broader test design** to test rather than duplicating it. If the deliverable is coverage itself, that's test.
- A dedicated threat audit scoped to a named adversary or compliance standard → **security-review**. maintain's `--security` gates the change on a security pass and hands the audit to that skill; it does not itself own the full threat model.

## Examples
`--scope='src/api/**'` — constrain every read, edit, and check to the API tree; anything needed outside it is surfaced as a follow-up, not changed silently.
`--module=billing` — resolve the billing subsystem's boundary (paths, entrypoints, owners) and operate within it, routing review/notification by its ownership.
`--changed` — target only what already moved in the working tree — upkeep, verification, and review scoped to that diff.
`--dry-run` — plan the change and report it (located target, risk tier, blast radius, intended edit) without touching the tree; the safe preview before committing to an edit.
`--checkpoint-commit` — commit at safe milestones so progress is recoverable and the change reads as a reviewable sequence.
`--changelog` — additionally emit a user-facing changelog / release-note entry matching the project's format.
`--require-clean` — refuse to start on a dirty tree, so the maintenance diff stays attributable.
`--security` — layer a gating security/compliance pass over the change and block completion on disqualifying findings.
`--module=auth --security` — harden the auth subsystem and gate completion on the security pass.

## Gotchas
- **maintain needs no configuration of its own.** Making a scoped edit, reading the local working tree — status, diff, and history — and **committing locally** are all ambient plain git (like reading any file; `--changed` derives its set this way and needs no configuration; maintain never pushes, so there is no version-control *host* to reach). The *external* touches it delegates are confirming checks, the security audit, and any ticket/notification records — to the skills that own them. If a delegated capability isn't configured, the owning skill guides setup (or blocks/degrades) and maintain degrades accordingly — e.g. `--security` can't complete its audit without the security capability.
- **Scope is a fence, not a suggestion.** Under `--scope`/`--module`, a needed change *outside* the bound is surfaced as a follow-up, never made silently — the diff stays about the one thing it set out to do.
- **`--require-clean` refuses; it does not stash.** It hard-stops on a dirty tree so your maintenance change can't get entangled with pre-existing uncommitted work; it will not move that work aside for you.
- **maintain adds the guard, not the suite.** It captures the specific failure it fixed as a regression check and runs the existing checks; designing broader coverage is test's job, and driving the running app to observe it is verify's.
- **`--security` gates, it doesn't just advise.** With the flag set, disqualifying security findings block completion rather than landing as notes — the change isn't done until they're resolved or the bar is explicitly lowered.
- **maintain stops at a clean, reviewable diff.** Judging that diff is review; landing it into a shared line is integrate. maintain produces the change and the record; it does not review or merge its own work.
