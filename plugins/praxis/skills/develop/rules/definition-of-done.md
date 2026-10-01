# The definition of done

"Done" left to feel is develop's central failure mode: one builder calls a change done when it compiles, another when the tests pass, another when it's wired and reviewed, and the same work ships at three different standards.

A change is **done** only when **all five** criteria hold, each by its own pass test.

`(basis: maintainer, 2026-07-10; derived from the Scrum Guide 2020 and CI practice)`

## The five criteria

- **1 · Complete** — every acceptance criterion of the driving plan/spec (or, absent one, the stated intent) is satisfied, and nothing was silently deferred.
  - *Test:* each criterion maps to a demonstrated behavior in the change; any criterion not met is *explicitly surfaced* as deferred/out-of-scope, never dropped in silence.
- **2 · Integrated / reachable** — the new code is connected to a real entry point and exercised on a live path; no orphaned unit, no dead code.
  - *Test:* there is an invocation path from an entry point (caller, route, command, event) to the new behavior, and it has been run end-to-end at least once ([prove-the-path-actually-runs](verification/prove-the-path-actually-runs.md)).
- **3 · Verified-green** — the tightest per-slice loop *and* the repo's **existing** full local check (build + the suite the project already runs, plus its lint/type gates) pass over the whole change, each new behavior observed to actually run.
  - *Test:* the full local check is green over the complete change, not just the last slice; each new behavior was seen to run, not merely compile. develop does **not** gate on authoring *new* comprehensive coverage — that is `test`'s job; it stands up the verify loop and proves the existing bar green. `(basis: maintainer, 2026-07-10)`
- **4 · Coherent** — the change matches the surrounding conventions, carries no debris, and is focused to the task.
  - *Test:* the phase-5 self-review finds no scope creep ([keep-the-diff-focused](../../../craft/engineering/keep-the-diff-focused.md)), no leftover debris ([leave-no-debris](../../../craft/engineering/leave-no-debris.md)), and no unexplained break from local convention ([match-the-surrounding-code](../../../craft/engineering/match-the-surrounding-code.md)).
- **5 · Landed-clean** — the working tree is in a clean, committable state, ready to hand off for review and landing; local only.
  - *Test:* no half-staged or stray work — a local backend's task documentation isn't stray: it stays out of the change ([document](../../document/SKILL.md) keeps it out); the change is committed as a coherent unit (a local, ambient commit — plain git, no backend). No push, PR, or ship: those belong to whoever delivers the change.

## The anchors

- *Top of scale (unambiguously done):* a change whose new function is called from a real entry point and was run end-to-end; every spec/plan criterion demonstrated by that run; the full local check green over the whole diff; the diff contains only task-relevant lines in the local idiom with no debris; the tree is clean and committed. A cold reviewer picking it up finds nothing left to finish.
- *Bottom of scale (the false-done to reject):* a change that compiles and whose unit tests pass — but whose new path is never wired to any caller (criterion 2 fails: dead code), *or* where one acceptance criterion was quietly shelved to "later" (criterion 1 fails: silent deferral). It *looks* finished and isn't; this is the exact shape "done by feel" ships.

## When a required check can't be run locally

Criteria 2 and 3 require checks that actually *run* — an entry-point path exercised end-to-end, the full local check green over the change. Sometimes one genuinely can't run locally: a DB-resetting fixture unsafe against shared infra, an entry path needing a backend the local env lacks. That does **not** license claiming done, and it does **not** license silently skipping the check (the recurring failure — a required check left unexecuted and unmentioned). Surface it as a **required field — `{criterion, why-deferred, backstop}`** — naming which criterion is unmet, why it couldn't run locally, and what *will* run it (e.g. CI on the PR). And an unmet binary criterion makes the outcome **checkpointed** or **blocked**, never *landed* ([land-the-change](../phases/06-land-the-change.md)'s partition): a criterion-2 path never run end-to-end is *"not done — checkpointed against the backstop,"* not *"done, deferred."*

## Using the bar

Walk the five at landing; a run that can't clear the bar reports **checkpointed** or **blocked**, never *landed* ([land-the-change](../phases/06-land-the-change.md)'s outcome partition). The criteria are develop's own bar for the author to clear before hand-off — passing it is not a substitute for `review`'s independent read, which judges the change cold on its own scales.
