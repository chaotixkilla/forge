# Commits tell the why

A commit or PR message is read far more often than it is written — by a reviewer deciding whether to approve, by a bisect landing on it a year later, by whoever is paging through history to understand why the code is the way it is. The diff already shows *what* changed and *how*; the one thing it cannot show is *why*, and a message that restates the diff ("update handler", "change the loop") throws away the only information the reader can't reconstruct. This rule pins the near-universal core of a good message, the **house baseline format** integrate writes to (the default, overridable by an explicit or persisted preference), the trailers it does and does not attach, and how a caller-supplied message is handled.

## The settled core — pinned, always

Every message integrate writes carries these, because the authorities converge on them:

- **A short imperative-mood subject line** — "Fix the empty-batch guard", not "Fixed…" / "Fixes…" / "Fixing…". Keep it to roughly one line (~50 characters), a summary a reader scans in a log.
- **A blank line, then a body** (when the change needs more than the subject) — the body wrapped for readability (~72 columns).
- **The body explains the *why*, not the *how*** — the motivation for the change and, where useful, how the new behavior contrasts with the old. It does *not* narrate the diff line by line; the diff is right there. This is the load-bearing point: the reader needs the reason and the shape, not a prose transcript of the patch.

`(basis: these three points are convergent across independent authorities — Pro Git's commit guidelines (imperative subject; ~50-char summary + blank line + body; "include your motivation for the change and contrast its implementation with previous behavior"; git-scm.com §5.2), Google's "Writing good CL descriptions" ("reading source code may reveal what the software is doing but it may not reveal why it exists"; google.github.io/eng-practices), and the Git project's own SubmittingPatches. Convergence across independent sources is why this is pinned, always.)`

## The house baseline format — Conventional Commits (the default, overridable by preference)

integrate synthesizes messages to the **Conventional Commits** structure as its house baseline — the verbs, the breaking-change signaling, the semver mapping are codified here so a synthesized message is consistent across projects. It is the **default** integrate writes to, displaced only by an explicit or persisted preference, never silently by what recent history happens to look like (resolved below).

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

The `feat`/`fix` distinction and their semver mapping are the spec's only MUSTs; the rest of the set is the widely-used extension. The commit `type` describes *this commit* and is not the same axis as the run's landing type ([assess-the-change](../phases/01-assess-the-change.md)) — though they correlate (a feature landing is usually `feat`, a hotfix usually `fix`, a chore usually `chore`/`refactor`/`docs`).

**Breaking-change signaling** — a change that breaks an external contract is marked **both** ways it can be: a **`!`** after the type/scope (`feat(api)!: …`) **and** a **`BREAKING CHANGE:`** footer (uppercase) describing what breaks and the migration. → semver **MAJOR**. This ties the message to the reversibility read in [make-rollout-reversible](make-rollout-reversible.md): a contract break is both an *irreversible-if-wrong* tier signal and a MAJOR-version signal.

**Scope** — an optional parenthesized area (`fix(auth): …`) when the repo uses scopes; omit it rather than invent one.

`(basis: ratified by the maintainer, 2026-07-11 — Conventional Commits v1.0.0 (conventionalcommits.org) is the house baseline for synthesized commit messages, so the verbs, breaking-change signaling (`!` + `BREAKING CHANGE:` footer), and the fix→PATCH / feat→MINOR / breaking→MAJOR mapping are codified here rather than left per-repo. The spec's structure is RFC-2119-normative; the type set beyond feat/fix is its common extension. The baseline is the **default** integrate writes to, displaced only by an explicit or persisted preference per the resolution below; a differing repo history is surfaced and resolved with the user, not silently adopted — amended by the maintainer, 2026-07-22, superseding the earlier reading that a repo's established convention silently wins, which let a squash-and-merge history impose its message shape over the baseline without asking. Message format is the skill's own editorial default, so a real divergence is a question to the user, then persisted — unlike the merge-strategy and branch-model forks ([match-the-team-flow](match-the-team-flow.md)) and commit-object policy ([honor-commit-policy](honor-commit-policy.md)), which stay detect-and-follow because there the repo's own practice is the right answer.)`

**Resolving which format applies.** The message format is the skill's own editorial default, not a team fork — so it does **not** inherit [match-the-team-flow](match-the-team-flow.md)'s "surrounding repo convention wins" routing (that routing governs the merge-strategy and branch-model forks, where there is genuinely no right answer; a synthesized message format has a deliberate house default). Resolve it by this precedence, **first match wins**:

1. **An explicit or persisted preference wins outright.** In order: (i) a format the caller states in *this* invocation, else (ii) a format **preference persisted for this project** by a past run's step-3 resolution. Present → use it, and skip the step-3 detection question entirely. This is the "unless specified otherwise": the norm *is* overridable, but only by something that actually states the preference. (There is no message-format config key; a persisted preference lives in ambient project memory, not the project config.)
2. **Otherwise the house baseline (Conventional Commits) is the default.** It applies whenever step 1 is absent and step 3 finds no *consistent conflicting* convention — **including** when recent history is empty, or a roughly-even mix with no predominant style. The baseline is **not** displaced merely because recent history *looks* different: only a *consistent* convention that doesn't parse as CC (step 3) turns into a question; anything short of that — no history, or a no-dominant-style mix — just gets the baseline, silently.
3. **A consistent convention that does not parse as the baseline is surfaced, never silently followed.** Detection (in [assess-the-change](../phases/01-assess-the-change.md)) reads recent commit subjects and asks one mechanical question of each: **does it parse as Conventional Commits** (`<type>[(scope)][!]: <description>`)? Two thresholds decide:
   - **Consistent** — recent commits *predominantly* fall on one side of that parse (the same signal test [honor-commit-policy](honor-commit-policy.md) applies to signing history: a uniform recent history establishes a convention, a roughly-even mix establishes none and falls to step 2). A per-commit CC-parse check plus a predominance read — no finer grammar-clustering needed.
   - **Conflicting** — the predominant side **does not parse as Conventional Commits**: a fixed template (a `Subject (#NN)` squash-default shape), a bracketed or ticket-prefix tag (`[FEAT] …`, `JIRA-123 …`), *or a consistent free-form style* (`Add the rate limiter`, no type prefix — a real convention, not the absence of one). Conversely, a history that predominantly *does* parse as CC coincides with the baseline — no conflict, no question — and such a repo **conforms regardless of its verb set** (integrate writes the baseline vocabulary; a caller who wants the repo's own verbs kept states it for the run, step 1(i)).

   When the history is both consistent and conflicting, integrate does **not** adopt the convention on its own. When the message is written — and only if step 1 set no preference — it (a) **surfaces** the conflict, stating the baseline and the observed convention side by side; (b) **asks the user** which to use going forward — the baseline or the observed convention, or a third the user names; (c) **applies the chosen format to the commit(s) being written now** and **persists it for this project in ambient project memory** (the same store step 1(ii) reads back), so the next run resolves at step 1 and never re-asks.
   - **Non-interactive fallback.** When the run has no reachable user to answer (an unattended run), integrate falls back to the **baseline**, **records in the report** that a differing convention was detected but left unresolved, and persists nothing — it never resolves the conflict by silently following history.
   - **Under `--dry-run`** integrate *previews* the conflict as an open item and neither asks nor persists (a dry run writes nothing — [prepare-the-increment](../phases/02-prepare-the-increment.md)).

Whichever format resolves, a **synthesized** message must **conform** to it — a synthesized message that doesn't parse as the applicable format is a defect integrate fixes before landing, not a message it ships.

## Trailers — what integrate attaches, and what it never does

Footers/trailers are detect-and-apply from the repo's convention and config, never invented:

- **`Signed-off-by:` (DCO)** — add it when the repo requires a sign-off (its history carries the trailer, or a DCO check gates it). The DCO *check* itself is a gate concern ([green-before-land](green-before-land.md)); this rule just attaches the trailer the repo expects.
- **Ticket references** — `Refs: #NNN` / `Closes #NNN` (or the repo's form) when the change traces to a tracked item and the repo references them; the item is resolved through the project-mgmt capability where `--pr` links it ([open-for-review](../modules/open-for-review.md)).
- **`Co-authored-by:` for genuine human co-authors** — when the work was actually co-authored (pairing, a carried-over patch) and the repo uses the trailer.
- **`BREAKING CHANGE:`** — as above, whenever the change breaks a contract.

**Never attach a `Co-authored-by:` (or any trailer) that names Claude, an AI assistant, or the tooling.** `(basis: ratified by the maintainer, 2026-07-11, and consistent with the ratified clean-export bar — team-facing output is "the content and the decisions, never the machinery," carrying no internal tool/agent/process references. A commit records the change and its *human* authorship; an AI co-author trailer is exactly the machinery/branding that bar strips, leaking into the permanent record. Human co-authors and required trailers are attached; an AI-attribution trailer is not, ever — and if the working tree already carries one from an earlier step, integrate strips it before committing.)`

## Interaction with `--message=`

When the caller supplies `--message=` ([prepare-the-increment](../phases/02-prepare-the-increment.md) reads it), integrate uses that text **verbatim** for the wording — the caller owns what it says, and this rule does not rewrite it. But integrate still: (1) **flags** it if it doesn't conform to the applicable format (a warning in the report, not a silent rewrite — the caller may have a reason); (2) attaches the repo's **required** trailers (a DCO sign-off the repo mandates) that a bare `--message` omits; and (3) **strips** any AI-attribution trailer even from supplied text, since that bar is not the caller's to waive. A supplied message that merely restates the diff is noted in the report.
