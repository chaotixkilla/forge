# Match the team flow

A change lands into a repository that already has a way of doing things — a merge style, a branch model, a release cadence — and imposing a generic ritual over it produces friction at best and a broken history at worst (a rebase where the team merges, a direct commit where the team reviews). Two of these choices are genuine, authority-confirmed **forks** with no single right answer; integrate does not pick a house winner, it detects what the team already does and follows it, routing the call up only when the repo is silent. This rule pins the two forks, the routing rule that resolves them, and how to read the repo's convention so the routing is runnable rather than aspirational.

## The routing rule (applies to both forks)

Resolve each fork by this precedence, non-gating — never block the run on it, follow the first source that answers:

1. **Surrounding repo convention** — what the repository already does (detected as below). This wins; a repo's lived convention outranks any default.
2. **House rule** — an explicit project/team configuration or documented standard, when the repo itself is ambiguous.
3. **Maintainer** — when neither the repo nor a house rule settles it, surface the choice with the tradeoff and let the maintainer decide; do not silently pick.

## Fork 1 — merge strategy

The three strategies are all first-class, and the authority is explicit that there is **no correct answer** — the axis is *fidelity of history* (preserve exactly what happened) vs. *legibility of history* (a clean linear log):

- **merge-commit** — every branch commit is kept and a merge commit records the integration (≥2 parents, branchy history). *Fidelity:* preserves the branch topology and answers "which integration introduced this?"; a merge commit is a landmark for bisect. *Cost:* a noisier, non-linear log.
- **squash** — the branch's commits collapse into one commit on the base (linear, one commit per change). *Legibility:* a clean per-change history. *Cost:* loses intra-change commit granularity — bisect lands on the whole change, not the one line, and the author's step-by-step reasoning is gone.
- **rebase** — the branch's commits replay onto the base individually, no merge commit (linear, all commits kept, but SHAs/committer rewritten). *Legibility + granularity:* linear yet per-commit. *Cost:* rewritten SHAs, and it is bound by the rebase golden rule below.

`(basis: Pro Git states outright there is no right answer — "every team and every project is different … it's up to you to decide which one is best" (git-scm.com, §3.6 Rebasing). GitHub ships all three merge methods as first-class (docs.github.com, "About merge methods"); GitLab exposes squash as an axis orthogonal to merge-commit (docs.gitlab.com, "Merge methods") — so where the host separates them, treat squash-vs-not and merge-commit-vs-linear as two decisions, not one three-way pick. The fidelity-vs-legibility framing and the bisect/granularity costs are corroborated by practitioner experience.)`

**The rebase golden rule — the one hard constraint inside this fork:** never rebase (or force-push a rebase of) commits that have been pushed and that others may have based work on — it rewrites shared history and destroys collaborators' work. Prefer a lease-guarded (compare-and-swap) force-push over an unconditional one if a shared-branch rebase is unavoidable. `(basis: Pro Git, §3.6, "The Perils of Rebasing" — stated as an absolute rule; corroborated by widespread practitioner reports of lost work from force-pushing shared branches.)` This constrains rebasing *shared feature branches locally*; a host's server-side "rebase-and-merge" onto the target tip is a different operation and is not what the golden rule forbids.

## Fork 2 — branch / trunk model

The model is an **applicability fork keyed on the release model**, not a better/worse choice:

- **trunk-based** (including the review-before-merge variant: short-lived branches opened as review requests off `main`) — a single long-lived line (`main`/trunk) with short-lived branches integrated frequently. Fits **continuous-delivery** software (one production version). 
- **Git Flow** — permanent `main` + `develop` with `release/*` and `hotfix/*` branches. Fits **explicitly-versioned** software or **multiple versions supported in production at once**.

`(basis: the fork keys on release model per the Git Flow author's own scope note — Vincent Driessen redirects continuous-delivery teams to a simpler flow and keeps Git Flow for explicitly-versioned / multi-version software (nvie.com). What is NOT a fork and is evidence-backed: integration *frequency* — DORA's research correlates ≤3 active branches, merging to trunk at least daily, and branch lifetimes under a day with higher delivery performance (dora.dev, "Trunk-based development"; echoed by Fowler). So follow the team's branch model, but where the team is choosing, bias toward short-lived branches and frequent integration, which the evidence supports across models.)`

## Detecting the repo's convention (so step 1 of the routing rule is runnable)

Read the repository's history and configuration to infer what it already does:

- **Merge strategy:** merge commits present in the history (commits with ≥2 parents) → merge-commit. Linear history, one commit per change, subjects often tagged with the change number → squash. Linear history, multiple commits per change retained, rewritten committer/dates → rebase. Also read the host's configured merge method where available — it is the most direct signal.
- **Branch model:** a `develop` branch alongside `main`/`master`, plus `release/*`/`hotfix/*` names → Git Flow. A single long-lived branch with feature branches via review requests, no `develop` → trunk-based (the review-request variant); very short branch lifetimes and near-daily integration confirm trunk-based.
- **Landing constraint:** whether the resolved **integration target** (the trunk, or an epic/`develop` branch per `--into`/derivation) *requires* a review request (branch protection / required review) or permits a direct merge — read through the **vcs capability** for that target (a landing-constraint read; the vcs port serves it, extended as consumers need). Resolve this *up front* so [land-it](../phases/04-land-it.md) chooses its landing path from a known fact, never by attempting a direct merge and reacting to a rejection.
- **Cadence and naming:** branch-name patterns, tag/release patterns, and review expectations (are changes reviewed before merge?) are read the same way and followed, not overridden.

State which convention you detected and by which precedence step you resolved each fork, so the landing is legible and a wrong inference is correctable.
