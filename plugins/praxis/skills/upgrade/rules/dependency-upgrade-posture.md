# Dependency-upgrade posture

A dependency upgrade is a maintenance change like any other — graded by the [change-risk-scale](../../../craft/engineering/change-risk-scale.md) on what it does to *your* code — but it carries two decisions the scale doesn't make: how tightly to constrain the version you depend on (**pin vs. float**), and how aggressively to move it (**the cadence**).

## Reproducibility is settled: always commit the lockfile

Whatever the manifest posture, commit the resolved-version lockfile. A committed lockfile makes the build reproducible and makes "which upgrade introduced this?" answerable. This is *not* the fork; the ecosystems converge on it. The live fork is only about what the **manifest** records for your direct dependencies.

## The fork: pin exact vs. float ranges (in the manifest)

- **Pin exact** — record exact versions in the manifest. *Strength:* maximum reproducibility and supply-chain safety, precise attribution of which version introduced a change, no surprise from an in-range release. *Cost:* you stop receiving updates automatically and the project silently rots — pinning is only safe when **paired with an update-automation bot** that proposes the bumps.
- **Float ranges** — record a compatible range. *Strength:* patches and minors flow in automatically (fast security fixes, less manifest churn), and a *published library* avoids over-constraining its own downstream (a library's consumers see its range, not its lockfile). *Cost:* an in-range release can silently break the build; without the committed lockfile, builds are non-reproducible.

The axis the sources split on is **application vs. library**. A published library keeps ranges, and that isn't in dispute. For an application they conflict: update-automation guidance pins exact even with a committed lockfile, while a 2025 empirical study finds a floating manifest range with a committed lockfile (at least for patches) the better tradeoff. So when convention is silent, the house default decides: an application pins exact and runs an update bot. `(basis: maintainer, 2026-07-11)`

## The cadence: map the increment to the risk tier

Treat the dependency's own version increment as a *prior* on how much adopting it will change your code, and take the matching [change-risk-scale](../../../craft/engineering/change-risk-scale.md) action:

- **patch** (backward-compatible fix) → **eligible for automatic adoption** after green checks + coverage (the [change-risk-scale](../../../craft/engineering/change-risk-scale.md) grades it, usually `contained`).
- **minor** (backward-compatible addition) → **eligible for automatic adoption** after green checks + coverage, with the changelog surfaced (the scan rides the automatic adoption; it is not a manual gate). Its tier is the [change-risk-scale](../../../craft/engineering/change-risk-scale.md)'s call — `contained` when your call sites take no adaptation, `bounded` when they must — *not* fixed by the increment.
- **major** (backward-incompatible) → **manual review** of the changelog / migration notes, never blind auto-adoption; take majors **in sequence** (one at a time, don't skip across several), because a breaking upgrade *is* a migration (graded `exposed`).
- **pre-release / pre-1.0 override** → any bump is high-risk regardless of the increment (a pre-1.0 dependency makes no compatibility promise) → **manual review**.

This is a *prior*, not the grade: the change the upgrade actually produces is graded by *Grading a dependency upgrade* in [change-risk-scale](../../../craft/engineering/change-risk-scale.md), which this cadence consumes, and the increment→risk mapping holds **only if the upstream publisher actually adheres to versioning discipline**, which is why the safeguards below exist.

## The safeguards — because versioning discipline varies

Minors and even patches do break in practice, so never auto-adopt un-gated:

- gate every automatic adoption behind real test coverage and a merge gate that requires green checks on the integration branch, so a bad bump *fails a check* rather than shipping unchecked: the bot proposes and the checks gate.
- prefer small, frequent updates over big batched jumps — staying close to current keeps the eventual urgent security patch cheap to take;
- apply a **release cooldown** — wait **7 days** after a version's publish date before *automatically* adopting it (routed to maintainer: 7 days, the low end of the common 7–14, as the default), so a malicious or broken publish can be caught, with **security/advisory fixes exempt** so urgent patches still land immediately. Source the publish date from the dependency's published registry metadata (an ambient read); when it can't be determined, say so and treat the cooldown as advisory rather than manufacturing a block. The cooldown gates *unattended* adoption; an **explicitly-requested** upgrade instead surfaces the version's age as advice and proceeds. If a project policy hard-refuses adopting a version still inside the cooldown even on request, that is a refused gate → the run ends `blocked-and-reported` ([commit-and-hand-off](../phases/05-commit-and-hand-off.md)), reporting the age and the policy.

`(basis: maintainer, 2026-07-11, for the posture; the cooldown's length is routed above)`

## Routing

A non-gating cascade: **(1) surrounding convention first** — does the repo already pin or float, is there a committed lockfile and an existing update-bot configuration (grouping, schedule)? Mirror it ([match-the-surrounding-code](../../../craft/engineering/match-the-surrounding-code.md)). **(2) the house rule** (above: apps pin-exact + bot, a 7-day cooldown) when convention is silent. **(3) the maintainer** for anything still genuinely open on a given repo — a project-specific patch SLA, or an explicit choice to float an app against the house default.

`(basis: SemVer 2.0.0, items 4 and 6–8; supply-chain hardening's pinned-dependencies criterion; dependency-update tooling guidance; OWASP Top 10 A06; NIST SSDF)`
