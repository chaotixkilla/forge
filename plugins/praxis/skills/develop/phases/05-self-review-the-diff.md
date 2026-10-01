# Self-review the diff

Check your own change before it's handed on — the author's last pass is the cheapest place to catch what the build missed, because you still have the whole change in your head, and the checks the [definition of done](../rules/definition-of-done.md) needs are about what the change was supposed to be.

## The author's checks, not the review

This pass checks the change against its own task and stops there. Judging it cold — its correctness and its craft, ranked on review's own scales by a reader who didn't write it — is `review`'s, which every act that runs develop runs after it; a run on its own hands the change to review for that. If this pass starts growing a severity ladder or a defect taxonomy, it has drifted into review's territory: cut it back. What survives self-review still goes to review.

Read the full diff (not the files — the *diff*) for:

- **Scope creep.** Anything the task didn't need — a drive-by refactor, an unrelated fix, a tidy-up that widened the blast radius ([keep-the-diff-focused](../../../craft/engineering/keep-the-diff-focused.md); a cleanup worth doing should have been a separate change — [separate-refactor-from-behavior-change](../../../craft/engineering/separate-refactor-from-behavior-change.md)).
- **Debris.** Scaffolding, debug prints, commented-out code, dead branches, a TODO you meant to close, an unused import an earlier slice left ([leave-no-debris](../../../craft/engineering/leave-no-debris.md)).
- **Missed acceptance criteria.** Walk the spec's or plan's acceptance criteria against the diff: is each one demonstrably handled, its edge, empty and failure inputs included? A criterion silently deferred is the definition of done's *complete* criterion failing.
- **A break from local convention you can't explain.** The change reads in the surrounding code's dialect, or the divergence has a reason the diff states ([match-the-surrounding-code](../../../craft/engineering/match-the-surrounding-code.md)).
- **A name or comment the change made false.** A name that now lies about what the code does ([avoid-misleading-names](../../../craft/engineering/avoid-misleading-names.md)), a comment the code moved away from ([keep-comments-truthful](../../../craft/engineering/keep-comments-truthful.md)).

## The future maintainer's read

Recruit the **future-self** critic to read the change as the maintainer six months out who holds none of your context: the implicit dependency, the missing rationale, the 2am-debug trap, the change with no obvious way back. It's the one read the author can't give their own change, and no later step gives it. Without fan-out, apply that lens yourself, as a separate pass after the checks above rather than folded into them. A finding survives when it names a concrete future misreading or trap this change creates — a scenario, not a style preference. Fold a surviving finding into the change when its fix lies inside the change's footprint; otherwise list it among the run's follow-ups, so it reaches review and the reader instead of being dropped.

The output of this phase is a change checked against its task and read as its future maintainer will meet it — ready for [land-the-change](06-land-the-change.md) to bring to a clean, committable state and check against the definition of done.
