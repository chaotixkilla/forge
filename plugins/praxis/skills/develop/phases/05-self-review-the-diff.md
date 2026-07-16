# Self-review the diff

Read your own change the way a hostile reviewer would, before anyone else has to. This is the author's last pass — the cheapest place to catch scope creep, leftovers, and the edge case the spec named and the build missed, because you still have the whole change in your head. It is deliberately adversarial: you are not admiring that it works, you are trying to find what's wrong with it as a piece of work someone else will maintain.

## This is a pre-hand-off read, not the review skill

Draw the boundary sharply, because it is easy to blur: this phase applies the craft-library develop *built with* as a final check, and stops there. It does **not** re-author, duplicate, or stand in for `review`'s separate correctness/craft finding library — review is the independent second pair of eyes that reads the change cold, ranks findings on its own severity scale, and exists precisely so the author isn't the only judge. develop's self-review is the author catching their own obvious misses; review is the separate gate. If this phase starts growing its own severity ladder or defect taxonomy, it has drifted into review's territory — cut it back. What survives self-review still goes to review.

## The hostile checklist

Read the full diff (not the files — the *diff*) and hunt, each against the rule that pins it:

- **Scope creep.** Does the diff contain anything the task didn't need — a drive-by refactor, an unrelated fix, a tidy-up that widened the blast radius? ([keep-the-diff-focused](../rules/change-hygiene/keep-the-diff-focused.md); a genuinely-worth-it cleanup should have been a separate change — [separate-refactor-from-behavior-change](../rules/change-hygiene/separate-refactor-from-behavior-change.md).)
- **Debris.** Scaffolding, debug prints, commented-out code, dead branches, a TODO you meant to close, an unused import left by an earlier slice ([leave-no-debris](../rules/change-hygiene/leave-no-debris.md)).
- **Missed cases from the intent.** Walk the spec/plan's acceptance criteria against the diff — is each one demonstrably handled? The edge, empty, and failure inputs the happy path skips? A criterion silently deferred is the [definition of done](../rules/definition-of-done.md)'s *complete* criterion failing.
- **Names and comments that will mislead the next reader.** A name that now lies about what the code does ([avoid-misleading-names](../rules/naming/avoid-misleading-names.md)), a name that doesn't reveal intent at its call site ([name-for-the-reader](../rules/naming/name-for-the-reader.md)), a comment that the code drifted away from ([keep-comments-truthful](../rules/comments/keep-comments-truthful.md)), a comment restating the what where the why was needed ([comment-the-why-not-the-what](../rules/comments/comment-the-why-not-the-what.md)).

## Recruit the critics develop names

Recruit the two critics on develop's roster to attack the change from the two angles the author is worst at seeing:

- **simplicity-hawk** — what here isn't pulling its weight? Accidental complexity, an abstraction that earned nothing, code that could simply be deleted.
- **future-self** — read as the maintainer six months out with no context: the name that will mislead, the implicit dependency, the missing rationale, the 2am-debug trap, the change with no obvious way back.

Without fan-out, apply both lenses yourself, explicitly and separately — a simplicity pass, then a future-maintainer pass — rather than a single satisfied read. Fold the surviving findings back into the change before landing; a self-review that surfaces nothing on a non-trivial change is usually a self-review that wasn't hostile enough.

The output of this phase is a change the author has already tried to break and cleaned up — ready for [land-the-change](06-land-the-change.md) to bring to a clean, committable state and check against the definition of done.
