# Commits tell the why

A commit or PR message is read far more often than it is written — by a reviewer deciding whether to approve, by a bisect landing on it a year later, by whoever is paging through history to understand why the code is the way it is. The diff already shows *what* changed and *how*; the one thing it cannot show is *why*, and a message that restates the diff ("update handler", "change the loop") throws away the only information the reader can't reconstruct.

## The settled core — pinned, always

Every commit message carries these, because the authorities converge on them:

- **A short imperative-mood subject line** — "Fix the empty-batch guard", not "Fixed…" / "Fixes…" / "Fixing…". Keep it to roughly one line (~50 characters), a summary a reader scans in a log.
- **A blank line, then a body** (when the change needs more than the subject) — the body wrapped for readability (~72 columns).
- **The body explains the *why*, not the *how*** — the motivation for the change and, where useful, how the new behavior contrasts with the old. It does *not* narrate the diff line by line; the diff is right there.

`(basis: Pro Git §5.2; Google's "Writing good CL descriptions"; the Git project's SubmittingPatches)`

## The house baseline format — Conventional Commits (the default, overridable by preference)

A message written for a change follows the **Conventional Commits** structure as the house baseline — the verbs, the breaking-change signaling, the semver mapping are codified here so a written message is consistent across projects.

**Structure:** `<type>[(scope)][!]: <description>`, then the settled-core body, then footers.

**The type vocabulary** (the verb that leads the subject):

- **`feat`** — a new user-facing capability. → semver **MINOR**.
- **`fix`** — a bug fix. → semver **PATCH**.
- **`refactor`** — a behavior-preserving restructuring (no feature, no fix).
- **`perf`** — a change made for performance.
- **`docs`** — documentation only.
- **`test`** — adding or correcting tests only.
- **`build`** — the build system or dependencies.
- **`ci`** — CI/pipeline configuration.
- **`style`** — formatting/whitespace only, no logic change.
- **`chore`** — other maintenance with no src/test behavior change.
- **`revert`** — reverts a prior commit (name it in the body).

The `feat`/`fix` distinction and their semver mapping are the spec's only MUSTs; the rest of the set is the widely-used extension. The commit `type` describes *this commit*, which isn't the same axis as how the change as a whole lands — though they correlate (a feature is usually `feat`, a hotfix usually `fix`, a chore usually `chore`/`refactor`/`docs`).

**Breaking-change signaling** — a change that breaks an external contract is marked **both** ways it can be: a **`!`** after the type/scope (`feat(api)!: …`) **and** a **`BREAKING CHANGE:`** footer (uppercase) describing what breaks and the migration. → semver **MAJOR**. A contract break is both a rollout that can't simply be reverted and a MAJOR-version signal, and the message carries the second.

**Scope** — an optional parenthesized area (`fix(auth): …`) when the repo uses scopes; omit it rather than invent one.

`(basis: maintainer, 2026-07-11, amended 2026-07-22; Conventional Commits v1.0.0)`

**Resolving which format applies.** The message format is an editorial default, not a team fork — so it does **not** inherit the "surrounding convention wins" routing that a merge strategy or a branch model follows, where there is genuinely no right answer; a written message format has a deliberate house default. Commit-object policy ([honor-commit-policy](honor-commit-policy.md)) stays detect-and-follow, because there the repo's own practice is the right answer. Resolve the format by this precedence, **first match wins**:

1. **An explicit or persisted preference wins outright.** In order: (i) a format the caller states in *this* invocation, else (ii) a format **preference persisted for this project** by a past run's step-3 resolution. Present → use it, and skip the step-3 detection question entirely. (There is no message-format config key; a persisted preference lives in ambient project memory, not the project config.)
2. **Otherwise the house baseline (Conventional Commits) is the default.** It applies silently, with no question, whenever step 1 is absent and step 3 finds no *consistent conflicting* convention — **including** when recent history is empty, or a roughly-even mix with no predominant style.
3. **A consistent convention that does not parse as the baseline is surfaced, never silently followed.** Detection reads recent commit subjects and asks one mechanical question of each: **does it parse as Conventional Commits** (`<type>[(scope)][!]: <description>`)? Two thresholds decide:
   - **Consistent** — recent commits *predominantly* fall on one side of that parse (the same signal test commit signing applies to its history: a uniform recent history establishes a convention, a roughly-even mix establishes none and falls to step 2). A per-commit CC-parse check plus a predominance read — no finer grammar-clustering needed.
   - **Conflicting** — the predominant side **does not parse as Conventional Commits**: a fixed template (a `Subject (#NN)` squash-default shape), a bracketed or ticket-prefix tag (`[FEAT] …`, `JIRA-123 …`), *or a consistent free-form style* (`Add the rate limiter`, no type prefix — a real convention, not the absence of one). Conversely, a history that predominantly *does* parse as CC coincides with the baseline — no conflict, no question — and such a repo **conforms regardless of its verb set** (the baseline vocabulary is written; a caller who wants the repo's own verbs kept states it for the run, step 1(i)).

   When the history is both consistent and conflicting, the convention is **not** adopted on its own. When the message is written — and only if step 1 set no preference — (a) **surface** the conflict, stating the baseline and the observed convention side by side; (b) **ask the user** which to use going forward — the baseline or the observed convention, or a third the user names; (c) **apply the chosen format to the commit(s) being written now** and **persist it for this project in ambient project memory** (the same store step 1(ii) reads back), so the next run resolves at step 1 and never re-asks.
   - **Non-interactive fallback.** When the run has no reachable user to answer — an unattended run, or a step another skill invoked, which asks nothing mid-run — fall back to the **baseline**, **record in the report** that a differing convention was detected but left unresolved, and persist nothing: never resolve the conflict by silently following history.
   - **Under a dry run**, *preview* the conflict as an open item and neither ask nor persist, since a dry run writes nothing.

Whichever format resolves, a **written** message must **conform** to it — one that doesn't parse as the applicable format is a defect fixed before committing, not a message to ship.

## Trailers — what a commit carries, and what it never does

Footers/trailers are detect-and-apply from the repo's convention and config, never invented:

- **`Signed-off-by:` (DCO)** — add it when the repo requires a sign-off (its history carries the trailer, or a DCO check gates it). The DCO *check* itself is the gate's concern; this standard just attaches the trailer the repo expects.
- **Ticket references** — `Refs: #NNN` / `Closes #NNN` (or the repo's form) when the change traces to a tracked item and the repo references them; the item is resolved through the project-mgmt capability.
- **`Co-authored-by:` for genuine human co-authors** — when the work was actually co-authored (pairing, a carried-over patch) and the repo uses the trailer.
- **`BREAKING CHANGE:`** — as above, whenever the change breaks a contract.

**Never attach a `Co-authored-by:` (or any trailer) that names Claude, an AI assistant, or the tooling**, and if the working tree already carries one from an earlier step, strip it before committing: a commit records the change and its *human* authorship, and an AI-attribution trailer is machinery leaking into the permanent record. `(basis: maintainer, 2026-07-11; the clean-export bar)`
