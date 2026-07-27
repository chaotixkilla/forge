# integrate — usage

Take a finished, reviewed change and get it safely into its integration target and out to production: stage coherent commits, reconcile with the latest target, pass the pre-merge gate, land it (by direct merge or a review request), roll it out to a target environment at a pace sized to its risk, and confirm it's healthy where it landed. The integration target defaults to the trunk but can be an epic/`develop` branch (via `--into`) for stacked-branch workflows.

## When to use
- A change is written, reviewed, and ready to land, and you want it committed, gated, merged, and shipped as one clean pass rather than driving each step by hand.
- You want the landing to match how this team actually works — its branch model and merge style — instead of a generic ritual imposed on the repo.
- You want the gate enforced honestly: the change reconciled against the *current* target before it's checked, and a red or skipped check treated as a stop, not a warning.
- You want the rollout to be reversible by default — shipped in a way that can be undone fast — and the outcome reported to the channel the team actually watches.

## Not for / use instead
- Building the change or applying craft as you write it → **develop** (integrate lands finished work; it does not build).
- Judging whether a change is correct before it lands → **review** (integrate carries the change through the gate; it does not perform the code review — run review first).
- Authoring or running the tests themselves → **test**; driving the running app to confirm behavior → **verify** (integrate *requires* the gate pass, it does not write the checks).
- Responding to a production incident — investigating telemetry, mitigating, running recurring ops → **operate** (integrate ships a planned change forward; operate responds when something is already burning).
- Writing a standalone status update, RFC, or announcement as a team document → **communicate** / **publish-artifact** (integrate reports its own ship outcome to a channel; it does not author long-form documents).

## Examples
`integrate` — the default path: assess, stage coherent commits, reconcile with the target, run the gate, land, and (if a target env is named) ship and confirm.
`--into=epic-checkout` — land the change into the `epic-checkout` branch instead of the trunk (a sub-branch integrating into its epic); the gate and reconcile run against that target, and no environment ship happens unless some environment is configured to deploy from `epic-checkout`.
`--commit` — stop after recording coherent local commits: stage and write them, push and open nothing. For work you want committed but not yet upstream.
`--pr` — land via a review request instead of a direct merge: assemble the description, link the originating work, and route to reviewers.
`--message="fix: guard against empty batch"` — use this text as the commit/PR message verbatim instead of synthesizing one from the diff.
`--target=staging` — after landing, promote to the `staging` environment, resolving its promotion path and any environment gating.
`--target=production --watch` — ship to production and stay attached: poll the run and post-ship signals until they settle, then report healthy or needs-rollback.
`--gate` — force the pre-merge gate to run and block on it even when the default flow would skip or soft-pass it.
`--on-fail=rollback` — if the gate or rollout fails, undo the last applied step rather than the default stop-and-report.
`--dry-run` — plan and report the whole path (commits, reconcile, gate, merge, rollout) without performing any mutation.

## Gotchas
- **integrate needs no configuration of its own.** It orchestrates; the backends live behind ports. Version-control operations (branch, push, PR, merge, conflict) go through the `vcs` skill, which owns `tools.vcs`; the pre-merge/pipeline checks and the deploy-promotion go through the `ci` skill, which owns `tools.ci`; the post-ship health read goes through `telemetry`, the channel report through `communication`, and the originating-work link (with `--pr`) through `project-mgmt` — each owns its own prerequisite. If a backend is unconfigured, that port guides you through its `init:<cap>` (or blocks), and integrate degrades on its side: no `tools.ci` → the hosted gate can't run and ship can't promote (fall back to local checks and report the hosted gate was not consulted); no `tools.telemetry` → land and ship still complete but post-ship health can't be judged; no `tools.communication`/`tools.project_mgmt` → the report/link is skipped and said so.
- **It lands finished work — it does not decide the work is good.** integrate assumes the change was already reviewed (run **review** first). It enforces that the *gate* is green; it does not re-judge the diff's correctness.
- **`--gate` is a floor, not the switch.** The gate runs on the default path already; `--gate` forces it to run and hard-block even where the flow would otherwise skip or soft-pass it. Reach for it on a path you don't trust to gate itself.
- **`--commit` truncates the run.** With `--commit`, the run stops after local commits — no push, no PR, no merge, no ship. The later flags (`--pr`, `--target`, `--watch`) are meaningless with it and are refused rather than silently ignored.
- **Reversible by default.** integrate prefers a rollout it can undo fast (small increments, staged exposure, or behind a switch) over an all-at-once cutover, sized to the change's assessed risk. `--target` names *where*; the risk assessment sets *how*.
- **Merge style and branch model follow the team; the commit-message format defaults to the house baseline.** Merge style and branch model are read from the repo's actual convention first, then any house rule, before anything is imposed — where they genuinely conflict, integrate surfaces the choice rather than picking one. The commit-message format is the opposite default: integrate writes its Conventional Commits baseline unless you state a preference or one is persisted, and where recent history *consistently* uses a different convention (a template, a tag scheme, or a plain free-form style) it surfaces the conflict and asks which to use (then remembers your answer), rather than silently adopting the history's shape.
- **The integration target defaults to the trunk but isn't always it.** integrate lands into the branch the work targets — resolved from durable records (an explicit `--into=<branch>`, else an open PR's base or a configured parent ref, else the default branch), never by guessing the fork parent. The gate, reconcile, and merge all run against *that* target, not an assumed `main`. Environment shipping is decided per `(target, env)`: a `--target=<env>` ships only if `<env>` is configured to **deploy from** the resolved target — so a Git Flow `develop` ships to `staging` (which deploys from it) but not `production` (which deploys from `main`), and an epic branch no env deploys from is land-only. A `--target` that doesn't deploy from the target is reported *deferred*, never silently dropped.
- **Landing default depends on collaboration posture.** With no landing flag, a collaboration repo (multiple contributors / a team roster / existing PR practice / branch protection) gets a review request; a solo repo is *asked* (direct-push vs PR), since solo landings are often not-yet-ready side-work. Branch protection always forces a PR. `--pr` forces the review-request path explicitly.
- **Green is a hard stop.** A failing or skipped required check blocks landing; integrate never lands on red and never silences a check to get through. `--on-fail` changes what happens *after* a failure (hold, ask, roll back), never whether a red gate blocks.
