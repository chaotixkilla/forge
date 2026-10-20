# Match the team flow

A change lands into a repository that already has a way of doing things — a merge style, a branch model, a release cadence — and imposing a generic ritual over it produces friction at best and a broken history at worst (a rebase where the team merges, a direct commit where the team reviews). Two of these choices are genuine, authority-confirmed **forks** with no single right answer; land does not pick a house winner, it detects what the team already does and follows it.

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

Where the host exposes squash as an axis separate from merge-commit, treat squash-vs-not and merge-commit-vs-linear as two decisions, not one three-way pick. `(basis: Pro Git §3.6; the hosting providers' own merge-method documentation; practitioner experience)`

**The rebase golden rule — the one hard constraint inside this fork:** never rebase (or force-push a rebase of) commits that have been pushed and that others may have based work on — it rewrites shared history and destroys collaborators' work. Prefer a lease-guarded (compare-and-swap) force-push over an unconditional one if a shared-branch rebase is unavoidable. `(basis: Pro Git §3.6, "The Perils of Rebasing"; practitioner reports of lost work)` This constrains rebasing *shared feature branches locally*; a host's server-side rebase onto the target tip at merge time is a different operation and is not what the golden rule forbids.

## Fork 2 — branch / trunk model

The model is an **applicability fork keyed on the release model**, not a better/worse choice:

- **trunk-based** (including the review-before-merge variant: short-lived branches opened as review requests off `main`) — a single long-lived line (`main`/trunk) with short-lived branches integrated frequently. Fits **continuous-delivery** software (one production version). 
- **Git Flow** — permanent `main` + `develop` with `release/*` and `hotfix/*` branches. Fits **explicitly-versioned** software or **multiple versions supported in production at once**.

Integration *frequency* is not a fork: follow the team's branch model, but where the team is choosing, bias toward short-lived branches and frequent integration — across models, the evidence correlates ≤3 active branches, merging to trunk at least daily, and branch lifetimes under a day with higher delivery performance. `(basis: Driessen's Git Flow scope note; DORA, "Trunk-based development"; Fowler)`

## Updating a branch against its target

Bringing a branch to its target's head is a third choice, apart from the land strategy. (basis: maintainer, 2026-10-19)

- **The convention.** What the repository's instruction files or contribution guide say about updating a branch decides it. History isn't read for it, since a rebased branch and one never updated look alike there. (basis: maintainer, 2026-10-20)
- **With no convention, it depends on who updates the branch.**
  - land's own reconcile merges the target into a pushed branch, and rebases one never pushed.
  - work's update of a review request's branch, in a revision or a rework, **rebases** it, keeping it free of merge commits. (basis: maintainer, 2026-10-20 — rebase where praxis updates a review request; land keeps merging, since its gate runs between the update and the push)
  - A stated rebase convention makes land rebase a pushed branch too, as the bullets below say.
- **The golden rule caps every rebase.** This test is what "others may have based work on" means here.
  - A branch is rebased only when every commit the rebase rewrites is the task's own: on the branch past the target, authored by the configured git identity, and, in work, not among the commits any of the task's `outside:` results record.
  - A pushed branch is rebased only when the remote's head for it is in its local history. That head is read from the remote itself, never from a remote-tracking ref.
  - A pushed branch whose route can't push with a lease is merged into. A route can lease when its adapter's push names one, or when a learned map was shown to keep the lease.
  - Any other branch is merged into.
- **Every merge into a pushed branch** whose remote holds commits it lacks takes the remote's head first, then the target.
- **Pushing it back.** A rebased branch that was pushed goes back right after the update, before anything else runs or is committed on it, with the vcs lease on the remote head read before the rebase. A refused lease means someone pushed meanwhile. The branch then goes back to its head before the rebase, losing nothing, and is merged into instead: the remote's head, then the target. It is pushed plainly, at once. In work, the commits that arrived are recorded as outside, not as the round's. In a revision, open-the-task's reconciliation runs again, and the running revision's number moves past the outside revision, as Another's commits says. In a rework, they are an `outside:` result of the round, unnumbered and not checked by praxis.
- **A stack** is rebased only when the golden rule allows every branch in it, else every branch in it is merged into. It goes base-most first, each branch rebased and pushed before the next. Each branch above replays only its own commits, from the old head of the branch below, onto the updated one. A refused lease at one branch merges it, and every branch above it, as above, leaving the ones below as pushed. Propagating a rebuilt unit upward stays a merge, as the review request rule says.
- **After a rebase,** a compare link from a commit the rebase removed from the head's history is noted unavailable, naming the new head by its full commit id. A rebase whose result is the entry's `at` or an ancestor of it is praxis's. A commit it rewrote is counted as the one it copies when its message and author match, in order, its change allowed to differ by the conflict's resolution. A copy made outside praxis also needs its change to match.
- **Saying which.** The run states the method, and which of these settled it.

## Detecting the repo's convention (so step 1 of the routing rule is runnable)

Read the repository's history and configuration to infer what it already does:

- **Merge strategy:** merge commits present in the history (commits with ≥2 parents) → merge-commit. Linear history, one commit per change, subjects often tagged with the change number → squash. Linear history, multiple commits per change retained, rewritten committer/dates → rebase.
- **Branch model:** a `develop` branch alongside `main`/`master`, plus `release/*`/`hotfix/*` names → Git Flow. A single long-lived branch with feature branches via review requests, no `develop` → trunk-based (the review-request variant); very short branch lifetimes and near-daily integration confirm trunk-based.
- **Landing constraint:** whether the resolved **integration target** (the trunk, or an epic/`develop` branch per `--into`/derivation) *requires* a review request (a protected target) or permits a direct merge — read through the **vcs capability** for that target (a landing-constraint read; the vcs port serves it, extended as consumers need). Resolve this *up front* so [merge](../phases/04-merge.md) chooses its landing path from a known fact, never by attempting a direct merge and reacting to a rejection.
- **Cadence and naming:** branch-name patterns, tag/release patterns, and review expectations (are changes reviewed before merge?) are read the same way and followed, not overridden.

State which convention you detected and by which precedence step you resolved each fork, so the landing is legible and a wrong inference is correctable.
