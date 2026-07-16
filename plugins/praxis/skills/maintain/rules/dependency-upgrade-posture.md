# Dependency-upgrade posture

A dependency upgrade is a maintenance change like any other — graded by the [change-risk-scale](change-risk-scale.md) on what it does to *your* code — but it carries two decisions the scale doesn't make: how tightly to constrain the version you depend on (**pin vs. float**), and how aggressively to move it (**the cadence**). Both have real authority on each side, so this rule encodes the fork and routes the house call rather than picking a winner.

## Reproducibility is settled: always commit the lockfile

Whatever the manifest posture, commit the resolved-version lockfile. A committed lockfile makes the build reproducible and makes "which upgrade introduced this?" answerable — regardless of whether the manifest pins or floats. This is *not* the fork; the ecosystems converge on it. The live fork is only about what the **manifest** records for your direct dependencies.

## The fork: pin exact vs. float ranges (in the manifest)

- **Pin exact** — record exact versions in the manifest. *Strength:* maximum reproducibility and supply-chain safety, precise attribution of which version introduced a change, no surprise from an in-range release. *Cost:* you stop receiving updates automatically and the project silently rots — pinning is only safe when **paired with an update-automation bot** that proposes the bumps.
- **Float ranges** — record a compatible range. *Strength:* patches and minors flow in automatically (fast security fixes, less manifest churn), and a *published library* avoids over-constraining its own downstream (a library's consumers see its range, not its lockfile). *Cost:* an in-range release can silently break the build; without the committed lockfile, builds are non-reproducible.

The axis the sources split on is **application vs. library**: an application pins exact and runs an update bot; a published library keeps ranges. That much is not in dispute.

`(basis: ratified by the maintainer, 2026-07-11 — when convention is silent, applications pin exact + run an update bot. Authority genuinely conflicts here, so the fork above stays encoded: established update-automation guidance argues pin-exact-even-with-a-committed-lockfile (visibility of exactly what runs in CI), while a 2025 empirical study argues float-with-lockfile (at least float-patch) is the better app tradeoff — the maintainer ratified the pin-exact side as the house default, and the routing below still lets a repo's own convention win first. The library→ranges and always-commit-the-lockfile calls were never in dispute.)`

## The cadence: map the increment to the risk tier

Treat the dependency's own version increment as a *prior* on how much adopting it will change your code, and take the matching [change-risk-scale](change-risk-scale.md) action:

- **patch** (backward-compatible fix) → **eligible for automatic adoption** after green checks + coverage (the [change-risk-scale](change-risk-scale.md) grades it, usually `contained`).
- **minor** (backward-compatible addition) → **eligible for automatic adoption** after green checks + coverage, with the changelog surfaced (the scan rides the automatic adoption; it is not a manual gate). Its tier is the [change-risk-scale](change-risk-scale.md)'s call — `contained` when your call sites take no adaptation, `bounded` when they must — *not* fixed by the increment.
- **major** (backward-incompatible) → **manual review** of the changelog / migration notes, never blind auto-adoption; take majors **in sequence** (one at a time, don't skip across several), because a breaking upgrade *is* a migration (graded `exposed`).
- **pre-release / pre-1.0 override** → any bump is high-risk regardless of the increment (a pre-1.0 dependency makes no compatibility promise) → **manual review**.

This is a *prior*, not the grade: the actual change the upgrade produces is still graded by the [change-risk-scale](change-risk-scale.md), and the increment→risk mapping holds **only if the upstream publisher actually adheres to versioning discipline** — which is why the safeguards below exist. The residual uncertainty they leave (you can't fully audit upstream) is *discharged* by these safeguards for a patch/minor — it does **not** resolve upward into `exposed` — while a major/pre-1.0 bump is an un-dischargeable uncertainty that does; this is the *Grading a dependency upgrade* rule in [change-risk-scale](change-risk-scale.md), and this cadence is its consumer.

## The safeguards — because versioning discipline varies

Upstream discipline is not guaranteed; minors and even patches do break in practice. So never auto-adopt un-gated:

- gate every automatic adoption behind real test coverage and a merge gate that requires green checks on the integration branch — so a bad bump *fails a check* rather than shipping unchecked. This is what makes patch/minor auto-adoption safe: the bot proposes and the checks gate; a **major or pre-1.0** bump additionally requires a human (the cadence above), while patch/minor may auto-adopt once green.
- prefer small, frequent updates over big batched jumps — staying close to current keeps the eventual urgent security patch cheap to take;
- apply a **release cooldown** — wait **~7–14 days** after a version's publish date before *automatically* adopting it, so a malicious or broken publish can be caught, with **security/advisory fixes exempt** so urgent patches still land immediately. Source the publish date from the dependency's published registry metadata (an ambient read); when it can't be determined, say so and treat the cooldown as advisory rather than manufacturing a block. The cooldown gates *unattended* adoption; an **explicitly-requested** upgrade instead surfaces the version's age as advice and proceeds. If a project policy hard-refuses adopting a version still inside the cooldown even on request, that is a refused gate → the run ends `blocked-and-reported` ([review-and-record](../phases/05-review-and-record.md)), reporting the age and the policy.

`(basis: ratified by the maintainer, 2026-07-11 — cooldown ~7–14 days, security/advisory fixes exempt. The cooldown length is a house rule, not standard-backed (authority says only "timely, risk-based"; the versioning standard is silent on cadence, and common practice ranges from a few days to two weeks); the maintainer ratified ~7–14 days. A per-repo "adopt patches within N days" SLA stays a project call where one is declared.)`

## Routing

A non-gating cascade: **(1) surrounding convention first** — does the repo already pin or float, is there a committed lockfile and an existing update-bot configuration (grouping, schedule)? Mirror it ([match-the-surrounding-code](match-the-surrounding-code.md)). **(2) the house rule** (ratified above: apps pin-exact + bot, cooldown ~7–14 days) when convention is silent. **(3) the maintainer** for anything still genuinely open on a given repo — a project-specific patch SLA, or an explicit choice to float an app against the house default.

`(basis: the increment→compatibility contract and the pre-1.0 exception are Semantic Versioning 2.0.0 (items 4, 6–8). Commit-the-lockfile-for-reproducibility is the converging guidance of the major package ecosystems. Pin-for-applications / ranges-for-libraries, and pair-pinning-with-an-update-bot, are from supply-chain hardening guidance (the pinned-dependencies criterion) and established dependency-update tooling guidance. "Update often / take majors in sequence / apply a cooldown" are from dependency-update-automation best practice; the ongoing-remediation duty is OWASP Top 10 A06 (vulnerable-and-outdated-components: remediate timely and risk-based) and NIST SSDF. The application pin-vs-float conflict is a documented recommendation-vs-empirical-study disagreement; the house default (apps pin-exact) and the cooldown length (~7–14 days) are the maintainer's ratified calls, 2026-07-11, since no authoritative number exists — checked the versioning standard, OWASP, and NIST SSDF.)`
