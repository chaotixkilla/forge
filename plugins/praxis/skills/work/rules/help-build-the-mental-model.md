# Help build the mental model

A task goes wrong quietly when the person doing it, or praxis, works from a picture of the area that nobody checked. Experiment follows experiment before anyone asks how the thing actually works. praxis helps at three points, with no setting, and keeps the rule that nothing is asked between the proposal and close-out. `(basis: maintainer, 2026-10-14)`

## Show the map of an unfamiliar area

When the act's first step is [understand](../../understand/SKILL.md), the proposal says its map will be shown if the user has no commits in the area it maps. When the step ends, run the test against the repository's history: no commit by the user's version-control name under the paths the map anchors. If it passes, show the map, as well as filing it as usual. Showing is not asking: the run goes on. `(basis: maintainer, 2026-10-14; shown when step 1 ends, derived — the map exists only once it has run)`

## Research when stuck

Research the blocking question without asking when either of these holds:

- **Two attempts have failed.** An attempt is one pass of the act's loop back: develop's steps 5 to 8 for a unit, or fixing-a-bug's fix-and-check pass. The research runs before the act's stop after the second failed pass. If it settles the question, the unit gets exactly one more pass, and a failure on that pass stops the act as before. `(basis: maintainer, 2026-10-14)`
- **A decision rests on unverified behaviour.** A step's result is about to record a decision — a plan's decision, a diagnosis's choice between hypotheses, a design choice develop records — that rests on how a library, service, host or protocol behaves. No source in the task has established it: no read of its code or documentation, and no run that showed it.

Keep the research bounded:

- **Scope.** It covers only that question.
- **Frequency.** It runs once per question per round.
- **No questions.** Each skill runs as a run that can't ask, taking its defaults.
- **Order.** Take the smallest kind first:
  1. a map of the code involved, the dependency's own source included, through [understand](../../understand/SKILL.md);
  2. its documentation, through [gather](../../gather/SKILL.md);
  3. external research, through [deep-research](../../deep-research/SKILL.md) at its standard depth, never a heavyweight run.
- **When to climb.** Move to the next kind only while the answer is short of `holds` or `fails` on [results-and-certainty](../../../craft/evidence/results-and-certainty.md)'s scale.
- **If it stays open.** When the last kind leaves it `unsettled`, the step goes on with the assumption stated as unsettled, and a heavyweight run becomes a close-out suggestion.

File the result as a result of its own, labelled `research:` with the question, its kind, and how many skill runs it took, by [run-the-act](../phases/03-run-the-act.md)'s rules for findings. Then carry on with the step from what it established. `(basis: maintainer, 2026-10-14)`

## Suggest research at key moments

Suggest research the user could run only at three moments:

- in the proposal, at most one;
- at close-out;
- when a message of the user's shows a gap without asking for the research itself: it states a belief the record contradicts, or works from a wrong picture of something the task depends on. A request for the research is side work ([side-work-asks-once](side-work-asks-once.md)).

Make at most two suggestions per task. Each says what it would settle and what it costs: its kind, and whether it is a heavyweight run. Suggest only what would change the task's outcome or the user's grasp of the area, never research for its own sake.

Each suggestion goes into the record with the filing that follows it, labelled `suggestion:` with its answer:

- a suggestion in the proposal goes with the opening filing;
- a mid-run suggestion goes with the next step's filing;
- a close-out suggestion goes with the closing filing.

An unanswered suggestion counts as declined. A declined suggestion is not made again in the task for the same question or the same paths, and a resumed task reads that from its history. `(basis: maintainer, 2026-10-14 — key moments only, so suggestions stay rare enough to be read)`

Cited by [run-the-act](../phases/03-run-the-act.md), [close-out](../phases/04-close-out.md) and the [developing](../acts/developing.md) and [fixing-a-bug](../acts/fixing-a-bug.md) acts.
