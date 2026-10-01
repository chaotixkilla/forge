An upgrade that starts without reading what changed in the dependency is a guess: the publisher's record of what moved is the one source that knows, and a model's memory of the library is exactly where an upgrade goes wrong silently. This phase pins down what moves, from which version to which, who uses it, and what the publisher says changes across that span, and captures how the project's checks stand now — the baseline [prove-it-green](04-prove-it-green.md) diffs against.

## Gate: honor `--require-clean` before anything else

If `--require-clean` is set, run its precondition gate as the very first action — see [require-clean](../modules/require-clean.md). Do not read code for editing until it passes; a dirty tree that fails the gate stops the run here.

## Resolve the working set

Bind what this run may touch (a **rule** — the flags select a value, the phase always resolves one):

- **`--scope=<pattern>`** → the working set is the paths matching the glob; treat everything outside it as off-limits.
- **`--module=<name>`** → resolve the named subsystem to its concrete boundary — paths, entrypoints, and **ownership metadata** (owners) returned with the change, so its record can be routed. Subsystem boundaries and ownership come from the repository; read them via the [repository](../../../agents/explorers/repository.md) explorer's lens (or inspect the project's own ownership/boundary files directly).
- **`--changed`** → the working set is the current version-control changes; read the working-tree/branch diff directly (an ambient local read) and target exactly what moved.
- **none of these** → the working set is the dependency's manifest and lockfile entries, plus its call sites.

A needed change *outside* the resolved set is never made silently — it's surfaced as a follow-up in [commit-and-hand-off](05-commit-and-hand-off.md) ([leave-the-campsite-cleaner](../../../craft/engineering/leave-the-campsite-cleaner.md)).

## Locate the dependency and who uses it

- **The versions.** The dependency, its currently resolved version (from the lockfile, not the manifest's range), and the target. The request names the target; without one, take the newest release the project's posture allows ([dependency-upgrade-posture](../rules/dependency-upgrade-posture.md)).
- **Its consumers.** Your own call sites, where a behavioral delta would land, and anything else that resolves the same copy — the reach [change-risk-scale](../../../craft/engineering/change-risk-scale.md) grades a dependency upgrade on.

Read enough of the call sites to know the conventions any adaptation will have to match ([match-the-surrounding-code](../../../craft/engineering/match-the-surrounding-code.md)).

## Read the upgrade path from its sources

Read the changelogs, release notes and migration guides for every version between the current one and the target through [gather](../../gather/SKILL.md), with its `official-documentation` lane. From them, take the breaking changes, deprecations, behavior changes, security fixes and migration steps that touch your call sites, each with its source. Note a span that is major or pre-1.0, or one with no scannable changelog: each shapes the grade in [grade-the-upgrade](02-grade-the-upgrade.md).

## Capture the green baseline — the verification anchor

**Checkpoint:** record the checks that pass now, before changing anything, so the upgrade's effect is a *delta* against a known-good baseline, not a guess. Prefer the project's own suite; where it has none for the call sites, capture representative current outputs by exercising them through their callers. Record the baseline explicitly; it is an input to [prove-it-green](04-prove-it-green.md)'s "done" test, not a throwaway.

## `--dry-run`

Under `--dry-run` the whole run plans and reports without mutating. This phase contributes the versions, the consumers, the upgrade path read from its sources, and the baseline; the run stops before phase 03 writes anything.

## Reject out-of-scope requests with a redirect

Some requests aren't upgrades and shouldn't be forced through this skill (a **rule** — refuse with a redirect, don't half-do it):

- The request changes code without moving a dependency → **refactor** when behavior must stay unchanged, **develop** otherwise.
- The request replaces a dependency with a different one → **develop**: a different library is new code, not a new version.
- The request finds why something broke → **debug**.
