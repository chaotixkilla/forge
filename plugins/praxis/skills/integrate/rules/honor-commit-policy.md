# Honor the repo's commit policy

A repo often enforces policy on the commit *object* itself — hooks that must run, a signature that must be present — and the failure mode is quiet: integrate commits in a way that bypasses the hook or omits the signature, the commit lands, and a later check (or an auditor) rejects it, or worse, a secret a pre-commit scan would have caught is now in history. This rule pins that integrate **follows** the repo's enforced commit policy and never cheats it. It is detect-and-follow, not a house default: most repos require neither, some require both, and integrate reads which before it commits — it does not impose signing or hooks a repo doesn't use, nor skip ones it does.

## Pre-commit hooks — run them, never bypass them

- **Let the hooks run.** Committing normally fires the repo's commit-time hooks (formatters, staged-file linters, secret-scanners, message linters). integrate commits normally so they run; it **never** takes the skip-verification shortcut to force a commit past a hook.
- **A hook failure is a stop, not a warning.** If a hook rejects the commit — a formatter rewrote files, a secret was detected, the message failed a linter — integrate **stops**, surfaces what the hook reported, and resolves it (re-stage the formatter's changes, remove the secret, fix the message) before committing, rather than forcing the commit through. A secret-scan hit in particular is a hard stop: never commit past it.
- **This composes with the gate, doesn't duplicate it.** Hooks run at *commit* time (here, in [prepare-the-increment](../phases/02-prepare-the-increment.md)); the pre-merge gate ([run-the-gate](../phases/03-run-the-gate.md)) runs later against the merged result. A hook is not a substitute for the gate or vice-versa — integrate honors both, and bypassing the hook to "let the gate catch it" is exactly the cheat this rule forbids.

## Commit signing — sign when the repo requires it

- **Detect the signing requirement.** Read whether the repo/team requires signed commits — its configuration (a sign-by-default / required-signature setting) or a history of signed commits. This is not assumed: an unsigned-history repo is not signed by integrate, and a signed-history/required-signature repo is. The **config signal is authoritative** (it, not history, drives the required-but-unable stop below); a **history signal alone** establishes a requirement only when it is *consistent* (recent commits are signed) — a **mixed** signed/unsigned history with no config signal establishes **no** requirement, so integrate treats signing as not-required there (it does not guess from a 50/50 split).
- **Sign when required; stop when required-but-unable.** Where signing is required, integrate produces signed commits per the repo's configured signing method. Where signing is required but integrate **cannot** sign (no signing key configured/available), it **stops and reports** the missing signing setup rather than landing unsigned commits that a signature check will later reject — an unsigned commit into a signed-required line is the quiet failure this prevents.

`(basis: detect-and-follow, not a house default — signing and hooks are repo-specific policy (most repos enforce neither; some enforce both), so integrate reads the repo's actual policy and matches it, the same routing every other team-flow fact uses ([match-the-team-flow](match-the-team-flow.md)). The never-bypass and stop-on-hook-failure discipline is the commit-time analog of [green-before-land](green-before-land.md)'s hard stop: a check that exists to guard the line is not silenced to get a commit through. Corroborated by the widely-reported failure mode of bypassing commit hooks — shipping a secret or a broken format past a hook that would have caught it.)`

## Cited from

[prepare-the-increment](../phases/02-prepare-the-increment.md) — the phase that records commits, where hooks fire and signing is applied.
