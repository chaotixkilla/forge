# review — usage

Critically read a finished change — a working-tree diff or a pull request — and return findings across correctness, craft, and risk, ranked so the author sees what matters first.

## When to use
- A change is written and you want a second pair of eyes before it lands: logic bugs, edge cases, error paths, concurrency, and a security lens, plus craft cleanups (reuse, simplification, efficiency, consistency).
- You want findings you can trust — each traced to a concrete failing scenario at file:line — not a vague list of concerns.
- You want to dial the rigor: a fast high-confidence pass for a small change, or a broad deep sweep for a risky one.
- You want the review to land where the work lives: returned locally, posted on the pull request, applied as fixes, or run as a CI gate that blocks a bad change.

## Not for / use instead
- Building the change and applying craft as you write it → **develop** (review reads a finished change; it does not build).
- A dedicated threat audit scoped to a named adversary or compliance standard → **security-review** (review carries a code-review-depth security lens, not a full threat model).
- Authoring or running tests to confirm behavior → **test**; driving the real running app to observe it → **verify** (review reads statically; it does not execute the code).
- Root-causing a specific known failure → **debug** (review hunts latent defects in a change; debug chases one that already bit).
- *Performing* a scoped refactor, dependency upgrade, or tech-debt paydown → **maintain** (maintain makes the change; review *judges* one). Reviewing a dependency-upgrade PR is squarely review's job — it fetches the dependency's API at the locked new version to judge the change even when that version isn't installed locally (see the gotcha below).

## Examples
`--effort=low` — a fast pass that reports only high-confidence findings; for a small or low-risk change.
`--effort=high` — broaden coverage and admit lower-confidence findings worth a look; for a risky or large change.
`--changed` — review the working-tree diff against the base (this is the default window when no source flag is given).
`--pr=142` — review pull request #142: its diff plus the description and context, fetched via the vcs capability.
`--lenses=security,concurrency` — comma-separate any subset of the declared lens domain; both the defect pass and the craft pass narrow to just the named lenses.
`--comment` — publish the findings back onto the change through the vcs capability instead of returning them locally.
`--comment --inline` — anchor each finding to its exact line as an inline annotation rather than one summary comment.
`--fix` — after triage, apply the accepted findings to the working tree as edits.
`--severity-min=high` — drop anything below high severity before delivery.
`--gate --severity-min=high` — run as a pass/fail check that exits non-zero if any high-or-above finding remains; for CI.

## Gotchas
- **Silence is a valid result.** Review surfaces the few findings that matter; it does not pad the list to look thorough. A clean change returns "no findings," not manufactured nits.
- **Correctness and craft stay separate.** Must-fix defects (a wrong result for some input) are reported apart from optional cleanups (same behavior, better form), so the author can tell a bug from a preference.
- **review needs no configuration of its own.** Reading the local diff and returning a report is ambient. The vcs capability — reached only by `--pr` (fetch a remote PR), `--comment`/`--inline` (post back), and `--gate` (post a status) — is delegated to the `vcs` skill, which owns the `tools.vcs` prerequisite. If vcs isn't configured, the `vcs` skill guides you through `init:vcs` (or blocks), and review degrades: `--pr` can't fetch, and `--comment` falls back to returning findings locally.
- **`--inline` needs `--comment`.** It modifies how comments attach; on its own it does nothing.
- **`--fix` edits, it does not build or run.** It applies the accepted findings to the tree and re-checks each fix at its site; end-to-end confirmation that the app still works is verify's job, not review's.
- **Effort is the primary dial.** It sets how broadly the passes hunt and how high the confidence bar sits — not merely how long the review takes. Reach for it before reaching for `--lenses`.
- **Review reads what the change set out to do.** Scope creep is flagged separately, not folded into the verdict; review judges the change against the surrounding code's conventions, not an external ideal.
- **Generated files and pure reformatting are set aside, not reviewed — unless they change a contract.** review excludes generator output (lockfiles, emitted schemas, bundles) and whitespace/EOL churn from the passes, reviewing the semantic diff; a generated file re-enters scope when its diff *drops or changes a contract* (a removed schema field), surfaced as a scope or correctness finding.
- **A dependency upgrade is reviewed against the new version's real API.** When the upgraded version isn't installed, review fetches its package source at the locked version rather than checking the change against the stale installed one.
- **`--pr` reviews the current remote head, materialized.** review checks the PR out at its head into an isolated worktree to read surrounding code, and cross-checks file counts against the PR metadata — so a force-pushed or stale branch doesn't yield a confident report of the wrong revision.
