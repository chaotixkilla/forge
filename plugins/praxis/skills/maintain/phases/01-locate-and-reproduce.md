Maintenance acts on a *living* system, so the first move is to anchor the request to the real code and its current behavior — not to start editing from the description. A change described as "bump the parser dependency" or "clean up the auth helper" points at code you haven't located and behavior you haven't observed; touch it before you've pinned both and you're changing something you don't yet understand. This phase ends with two things in hand: the exact code that owns the behavior, and a reproduced baseline of how it behaves *now* — the anchor [verify-and-guard](04-verify-and-guard.md) will diff against, since maintenance usually has no upstream spec to check against.

## Gate: honor `--require-clean` before anything else

If `--require-clean` is set, run its precondition gate as the very first action — see [require-clean](../modules/require-clean.md). Do not read code for editing until it passes; a dirty tree that fails the gate stops the run here.

## Resolve the working set

Bind what this run may touch (a **rule** — the flags select a value, the phase always resolves one):

- **`--scope=<pattern>`** → the working set is the paths matching the glob; treat everything outside it as off-limits.
- **`--module=<name>`** → resolve the named subsystem to its concrete boundary — paths, entrypoints, and **ownership metadata** (owners) that [review-and-record](05-review-and-record.md) uses to route the record. Subsystem boundaries and ownership come from the repository; read them via the [repository](../../../agents/explorers/repository.md) explorer's lens (or inspect the project's own ownership/boundary files directly).
- **`--changed`** → the working set is the current version-control changes; read the working-tree/branch diff directly (an ambient local read — no configured backend needed) and target exactly what moved.
- **none of these** → the working set is the request's natural scope: the code that owns the named behavior, plus what phase 02 shows it reaches.

A needed change *outside* the resolved set is never made silently — it's surfaced as a follow-up in [review-and-record](05-review-and-record.md) ([leave-the-campsite-cleaner](../rules/leave-the-campsite-cleaner.md)).

## Locate the code that owns the behavior

Find the code that actually implements the behavior in question — the definition, not just a call site (**judgment**: the request names a symptom or a goal; you locate its owner). Read enough of the surrounding code to know the conventions you'll have to match ([match-the-surrounding-code](../rules/match-the-surrounding-code.md)) and to recognise anything puzzling. When the located code reads as dead, redundant, or arbitrary, or sits on a load-bearing path, recover its intent before planning any change — the Chesterton's-fence check in [decode-intent-from-history](../rules/decode-intent-from-history.md). Locate at the *cause*, not the first surface the symptom shows ([fix-the-cause-not-the-symptom](../rules/fix-the-cause-not-the-symptom.md)).

## Reproduce the current state — the verification anchor

**Checkpoint:** establish and record how the target behaves *now*, before changing it, because that baseline is what proves the change did what it intended. What "reproduce" means depends on the change's kind — pick the tightest available:

- **Fixing a defect** → reproduce the failure: a runnable demonstration (a failing test, a command, an input) that exhibits the wrong behavior. If it can't be reproduced, that is the first problem to solve — a fix you can't demonstrate is a fix you can't verify.
- **A refactor or cleanup** (behavior must not change) → capture the current observable behavior as the baseline so phase 04 can show it's unchanged. Prefer the relevant existing tests passing; where none exist, capture *representative current outputs* by **exercising the code** — drive it through its callers, or — when the target is directly callable — author a temporary throwaway harness that calls it with sample inputs, and record the outputs to diff against after the change. (A private, non-exported target isn't directly callable: use the caller route, or temporarily expose it as a baseline-only step you revert.) Cover the distinct input shapes its callers actually exercise, plus the obvious edges (empty, boundary); breadth beyond that is the executor's judgment (it varies with the subject). Only when the code genuinely cannot be exercised at all (no caller and no callable entry point) is the baseline unavailable — that single case is what phase 04 grades *inconclusive*, surfaced rather than worked around.
- **A dependency upgrade** → capture the current green state (the checks that pass now) so the upgrade's effect is a *delta* against a known-good baseline, not a guess.

Record the baseline explicitly; it is an input to [verify-and-guard](04-verify-and-guard.md)'s "done" test, not a throwaway.

## `--dry-run`

Under `--dry-run` the whole run plans and reports without mutating. This phase's contribution to that report is the located target and the reproduced baseline; carry them forward — phases 02–03 add the risk tier, blast radius, and intended edit, and the run stops before phase 03 writes anything.

## Reject out-of-scope requests with a redirect

Some requests aren't maintenance and shouldn't be forced through this skill (a **rule** — refuse with a redirect, don't half-do it):

- The request is **net-new behavior** (a feature, a new module) → route to **develop**; maintain changes existing code, it doesn't build new work.
- The request is **root-causing a specific failure that already bit** → route to **debug**; if the task is "find why this broke," debug owns the hunt (maintain performs upkeep and reproduces a baseline, but doesn't run the hypothesis-and-test investigation).

Redirect explicitly rather than producing a confident half-answer in the wrong shape.
