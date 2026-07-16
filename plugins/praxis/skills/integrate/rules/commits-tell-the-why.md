# Commits tell the why

A commit or PR message is read far more often than it is written — by a reviewer deciding whether to approve, by a bisect landing on it a year later, by whoever is paging through history to understand why the code is the way it is. The diff already shows *what* changed and *how*; the one thing it cannot show is *why*, and a message that restates the diff ("update handler", "change the loop") throws away the only information the reader can't reconstruct. This rule pins the near-universal core of a good message, the **house baseline format** integrate writes to (overridable per-repo), the trailers it does and does not attach, and how a caller-supplied message is handled.

## The settled core — pinned, always

Every message integrate writes carries these, because the authorities converge on them:

- **A short imperative-mood subject line** — "Fix the empty-batch guard", not "Fixed…" / "Fixes…" / "Fixing…". Keep it to roughly one line (~50 characters), a summary a reader scans in a log.
- **A blank line, then a body** (when the change needs more than the subject) — the body wrapped for readability (~72 columns).
- **The body explains the *why*, not the *how*** — the motivation for the change and, where useful, how the new behavior contrasts with the old. It does *not* narrate the diff line by line; the diff is right there. This is the load-bearing point: the reader needs the reason and the shape, not a prose transcript of the patch.

`(basis: these three points are convergent across independent authorities — Pro Git's commit guidelines (imperative subject; ~50-char summary + blank line + body; "include your motivation for the change and contrast its implementation with previous behavior"; git-scm.com §5.2), Google's "Writing good CL descriptions" ("reading source code may reveal what the software is doing but it may not reveal why it exists"; google.github.io/eng-practices), and the Git project's own SubmittingPatches. Convergence across independent sources is why this is pinned, always.)`

## The house baseline format — Conventional Commits (overridable per-repo)

integrate synthesizes messages to the **Conventional Commits** structure as its house baseline — the verbs, the breaking-change signaling, the semver mapping are codified here so a synthesized message is consistent across projects, and a repo overrides it only where its own convention differs.

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

`(basis: ratified by the maintainer, 2026-07-11 — Conventional Commits v1.0.0 (conventionalcommits.org) is the house baseline for synthesized commit messages, so the verbs, breaking-change signaling (`!` + `BREAKING CHANGE:` footer), and the fix→PATCH / feat→MINOR / breaking→MAJOR mapping are codified here rather than left per-repo. The spec's structure is RFC-2119-normative; the type set beyond feat/fix is its common extension. Overridable per the routing below — a repo's own established convention wins, and the baseline applies where the repo has none.)`

**Override + enforcement.** Detect the repo's actual convention first (read recent history: do messages carry a `type:` prefix? a different house template? free-form?). Resolve by [match-the-team-flow](match-the-team-flow.md)'s routing — **surrounding repo convention → house rule → this baseline**: a repo with an established different convention wins (follow it, don't impose Conventional Commits on a settled free-form history); a repo with no clear convention gets the baseline. Whichever format applies, a **synthesized** message must **conform** to it — a synthesized message that doesn't parse as the applicable format is a defect integrate fixes before landing, not a message it ships.

## Trailers — what integrate attaches, and what it never does

Footers/trailers are detect-and-apply from the repo's convention and config, never invented:

- **`Signed-off-by:` (DCO)** — add it when the repo requires a sign-off (its history carries the trailer, or a DCO check gates it). The DCO *check* itself is a gate concern ([green-before-land](green-before-land.md)); this rule just attaches the trailer the repo expects.
- **Ticket references** — `Refs: #NNN` / `Closes #NNN` (or the repo's form) when the change traces to a tracked item and the repo references them; the item is resolved through the project-mgmt capability where `--pr` links it ([open-for-review](../modules/open-for-review.md)).
- **`Co-authored-by:` for genuine human co-authors** — when the work was actually co-authored (pairing, a carried-over patch) and the repo uses the trailer.
- **`BREAKING CHANGE:`** — as above, whenever the change breaks a contract.

**Never attach a `Co-authored-by:` (or any trailer) that names Claude, an AI assistant, or the tooling.** `(basis: ratified by the maintainer, 2026-07-11, and consistent with the ratified clean-export bar (USING-ANVIL-ON-PRAXIS.md §2) — team-facing output is "the content and the decisions, never the machinery," carrying no internal tool/agent/process references. A commit records the change and its *human* authorship; an AI co-author trailer is exactly the machinery/branding that bar strips, leaking into the permanent record. Human co-authors and required trailers are attached; an AI-attribution trailer is not, ever — and if the working tree already carries one from an earlier step, integrate strips it before committing.)`

## Interaction with `--message=`

When the caller supplies `--message=` ([prepare-the-increment](../phases/02-prepare-the-increment.md) reads it), integrate uses that text **verbatim** for the wording — the caller owns what it says, and this rule does not rewrite it. But integrate still: (1) **flags** it if it doesn't conform to the applicable format (a warning in the report, not a silent rewrite — the caller may have a reason); (2) attaches the repo's **required** trailers (a DCO sign-off the repo mandates) that a bare `--message` omits; and (3) **strips** any AI-attribution trailer even from supplied text, since that bar is not the caller's to waive. A supplied message that merely restates the diff is noted in the report.
