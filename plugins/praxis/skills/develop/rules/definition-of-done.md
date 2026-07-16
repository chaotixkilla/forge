# The definition of done

develop's whole promise is in one word — *finished* — and a promise that word can't cash is worthless. "Done" left to feel is develop's central failure mode: one builder calls a change done when it compiles, another when the tests pass, another when it's wired and reviewed, and the same work ships at three different standards. This rule pins what *done* means so two cold builders land the same change at the same bar, and so [land-the-change](../phases/06-land-the-change.md) has a checkable gate rather than a vibe. It is develop's marquee standard — the analogue of what the severity scale is to review.

A change is **done** only when **all five** criteria hold. They are conjunctive — the change is exactly as done as its weakest criterion — and each carries its own pass test so the judgment isn't re-invented per run.

`(basis: routed to maintainer, ratified 2026-07-10. Craft "done" has no single external authority the way a security severity has CVSS — the Scrum Guide (2020) makes Definition of Done a formal commitment but explicitly *team-defined*, with no universal set, which is exactly why these five criteria and their tightness are the maintainer's ratified house standard. Derived from: the Scrum-Guide DoD concept (a shared, checkable completion bar); the general agile/CI convention that "done" includes integrated-and-working, not merely written; and continuous-integration practice (green covers the whole change, actually run). The criteria set is fixed here; the *strictness* of criterion 3 is pinned below to the repo's existing checks, deliberately, so develop doesn't silently absorb `test`'s job.)`

## The five criteria

- **1 · Complete** — every acceptance criterion of the driving plan/spec (or, absent one, the stated intent) is satisfied, and nothing was silently deferred.
  - *Test:* each criterion maps to a demonstrated behavior in the change; any criterion not met is *explicitly surfaced* as deferred/out-of-scope, never dropped in silence.
- **2 · Integrated / reachable** — the new code is connected to a real entry point and exercised on a live path; no orphaned unit, no dead code.
  - *Test:* there is an invocation path from an entry point (caller, route, command, event) to the new behavior, and it has been run end-to-end at least once ([prove-the-path-actually-runs](verification/prove-the-path-actually-runs.md)).
- **3 · Verified-green** — the tightest per-slice loop *and* the repo's **existing** full local check (build + the suite the project already runs, plus its lint/type gates) pass over the whole change, each new behavior observed to actually run.
  - *Test:* the full local check is green over the complete change, not just the last slice; each new behavior was seen to run, not merely compile. develop does **not** gate on authoring *new* comprehensive coverage — that is `test`'s job; it stands up the verify loop and proves the existing bar green. `(basis: ratified 2026-07-10 — scoping "green" to the repo's existing checks, not new coverage, is the deliberate develop/test boundary; widening it here would make develop silently absorb comprehensive test design.)`
- **4 · Coherent** — the change matches the surrounding conventions, carries no debris, and is focused to the task.
  - *Test:* the phase-5 hostile self-review finds no scope creep ([keep-the-diff-focused](change-hygiene/keep-the-diff-focused.md)), no leftover debris ([leave-no-debris](change-hygiene/leave-no-debris.md)), and no unexplained break from local convention ([match-surrounding-conventions](change-hygiene/match-surrounding-conventions.md)).
- **5 · Landed-clean** — the working tree is in a clean, committable state, ready to hand off to review/integrate; local only.
  - *Test:* no half-staged or stray work; the change is committed as a coherent unit (a local, ambient commit — plain git, no backend). No push, PR, or ship — that is `integrate`.

## The anchors

- *Top of scale (unambiguously done):* a change whose new function is called from a real entry point and was run end-to-end; every spec/plan criterion demonstrated by that run; the full local check green over the whole diff; the diff contains only task-relevant lines in the local idiom with no debris; the tree is clean and committed. A cold reviewer picking it up finds nothing left to finish.
- *Bottom of scale (the false-done to reject):* a change that compiles and whose unit tests pass — but whose new path is never wired to any caller (criterion 2 fails: dead code), *or* where one acceptance criterion was quietly shelved to "later" (criterion 1 fails: silent deferral). It *looks* finished and isn't; this is the exact shape "done by feel" ships.

## When a required check can't be run locally

Criteria 2 and 3 require checks that actually *run* — an entry-point path exercised end-to-end, the full local check green over the change. Sometimes one genuinely can't run locally: a DB-resetting fixture unsafe against shared infra, an entry path needing a backend the local env lacks. That does **not** license claiming done, and it does **not** license silently skipping the check (the recurring failure — a required check left unexecuted and unmentioned). Surface it as a **required field — `{criterion, why-deferred, backstop}`** — naming which criterion is unmet, why it couldn't run locally, and what *will* run it (e.g. CI on the PR). And an unmet binary criterion makes the outcome **checkpointed** or **blocked**, never *landed* ([land-the-change](../phases/06-land-the-change.md)'s partition): a criterion-2 path never run end-to-end is *"not done — checkpointed against the backstop,"* not *"done, deferred."* A silent PR-checkbox a landing run walks past is exactly what this field replaces.

## Using the bar

Walk the five at landing; the change is done only if each passes its test, and a run that can't clear the bar reports **checkpointed** or **blocked**, never *landed* ([land-the-change](../phases/06-land-the-change.md)'s outcome partition). The criteria are develop's own bar for the author to clear before hand-off — passing it is not a substitute for `review`'s independent read, which judges the change cold on its own scales. Done means *ready to be reviewed and integrated*, not *already reviewed*.
