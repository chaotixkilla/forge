A refactor restructures code and leaves its behavior exactly as it was. When the job is retiring a feature flag or toggle, [retire-the-switches](../../../craft/engineering/retire-the-switches.md) gives its steps: removing a switch that has held one value for its whole exposure changes no behavior, so it is a refactor.

Anchor the request to the real code and its current behavior before editing anything: a change described as "split the billing module" or "clean up the auth helper" points at code you haven't located and behavior you haven't observed. The phase ends with two things in hand: the exact code that owns the behavior, and a reproduced baseline of how it behaves *now*, the anchor [prove-it-unchanged](04-prove-it-unchanged.md) diffs against.

## Gate: honor `--require-clean` before anything else

If `--require-clean` is set, run its precondition gate as the very first action — see [require-clean](../modules/require-clean.md). Do not read code for editing until it passes; a dirty tree that fails the gate stops the run here.

## Resolve the working set

Bind what this run may touch (a **rule** — the flags select a value, the phase always resolves one):

- **`--scope=<pattern>`** → the working set is the paths matching the glob; treat everything outside it as off-limits.
- **`--module=<name>`** → resolve the named subsystem to its concrete boundary — paths, entrypoints, and **ownership metadata** (owners) returned with the change, so its record can be routed. Subsystem boundaries and ownership come from the repository; read them via the [repository](../../../agents/explorers/repository.md) explorer's lens (or inspect the project's own ownership/boundary files directly).
- **`--changed`** → the working set is the current version-control changes; read the working-tree/branch diff directly (an ambient local read — no configured backend needed) and target exactly what moved.
- **none of these** → the working set is the request's natural scope: the code that owns the named behavior, plus what phase 02 shows it reaches.

A needed change *outside* the resolved set is never made silently — it's surfaced as a follow-up in [commit-and-hand-off](05-commit-and-hand-off.md) ([leave-the-campsite-cleaner](../../../craft/engineering/leave-the-campsite-cleaner.md)).

## Locate the code that owns the behavior

Find the code that actually implements the behavior in question — the definition, not just a call site (**judgment**: the request names a symptom or a goal; you locate its owner). Read enough of the surrounding code to know the conventions you'll have to match ([match-the-surrounding-code](../../../craft/engineering/match-the-surrounding-code.md)) and to recognise anything puzzling. When the located code reads as dead, redundant, or arbitrary, or sits on a load-bearing path, recover its intent before planning any change — the Chesterton's-fence check in [decode-intent-from-history](../../../craft/engineering/decode-intent-from-history.md).

## Reproduce the current state — the verification anchor

**Checkpoint:** establish and record how the target behaves *now*, before changing it, because that baseline is what proves the behavior didn't change. Prefer the relevant existing tests passing; where none exist, characterize the code first ([refactoring-catalogue](../../../craft/engineering/refactoring-catalogue.md), *Untested code*) and capture *representative current outputs* by **exercising the code** — drive it through its callers, or — when the target is directly callable — author a temporary throwaway harness that calls it with sample inputs, and record the outputs to diff against after the change. (A private, non-exported target isn't directly callable: use the caller route, or temporarily expose it as a baseline-only step you revert.) Cover the distinct input shapes its callers actually exercise, plus the obvious edges (empty, boundary); breadth beyond that is the executor's judgment (it varies with the subject). Only when the code genuinely cannot be exercised at all (no caller and no callable entry point) is the baseline unavailable — that single case is what phase 04 grades *inconclusive*, surfaced rather than worked around.

Record the baseline explicitly; it is an input to [prove-it-unchanged](04-prove-it-unchanged.md)'s "done" test, not a throwaway.

## `--dry-run`

Under `--dry-run` the whole run plans and reports without mutating. This phase's contribution to that report is the located target and the reproduced baseline; carry them forward — phases 02–03 add the risk tier, blast radius, and intended edit, and the run stops before phase 03 writes anything.

## Reject out-of-scope requests with a redirect

Some requests aren't refactors and shouldn't be forced through this skill (a **rule** — refuse with a redirect, don't half-do it):

- The request **changes behavior** — new behavior, a feature, a deliberate contract change → route to **develop**; a refactor leaves behavior exactly as it was.
- The request moves **a dependency to a new version** → route to **upgrade**, which reads the dependency's changelogs and migration guides.
- The request **fixes a defect, or finds why something broke** → route to **debug**; fixing a defect changes behavior on purpose, which a refactor never does.
