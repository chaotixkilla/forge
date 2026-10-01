The act file says which steps run, in what order, with which inputs; this phase carries that out without adding or dropping anything.

## Propose, then run

Before proposing, check that each step's skill is available and that the ports the act files and delivers through are configured, with a default artifacts destination set where the backend uses one. Show the user the act's steps from its act file, each with its skip condition, and ask once whether to run them as proposed. Fold into that one question anything the run can't proceed without: a step whose skill isn't available, an intent [open-the-task](02-open-the-task.md) couldn't find, each port the act needs that isn't configured — offered as "set it up now", through that capability's own setup in [init](../../init/SKILL.md), or "run without it", its channels then held or returned for hand delivery — and, for each step the act runs with a heavyweight flag, the cost question in [ask-before-a-heavyweight-run](../../gather/rules/ask-before-a-heavyweight-run.md)'s own words, where cancel removes that step. The user's answer settles that step's flag, so its skill doesn't ask again. A setup the answer chose runs right after it, interactively — the one exception to asking nothing after that question, since the user chose it in answering — before any deferred part of "Before the steps" and the first step. Running without a port is this task's choice: an act never records a capability as unused for the project. The user may remove steps; record each removal with the user's reason, in their own words if they give no other. Adding, reordering or re-inputting steps isn't offered. (basis: maintainer, 2026-09-30) (routed to maintainer: removal only, since a changed sequence is a different act.)

After that question, ask nothing before close-out. An input that asks for an action ([edits-change-intent-not-actions](../rules/edits-change-intent-not-actions.md)) is quoted in close-out's report for the user to answer, not acted on mid-run.

Then, when the act file has an "After approval" section, carry it out, and run the remaining steps in the act's order. Check a step's skip condition when its turn comes, against the results before it. Invoke the step's skill with exactly the inputs the act names for it ([form-your-own-view-first](../../../craft/evidence/form-your-own-view-first.md)). Never do a step's work in its skill's place, or restate its method here.

Run every step inline, in this context, unless the act file marks it isolated. An act marks a step isolated only when the step's inputs must exclude something this context already holds, and avoids that by withholding an input rather than reading it early. (basis: maintainer, 2026-09-30)

## Keep the record

After each step, record how it ended, on the act's checklist and in the act marker, using exactly the outcomes in [skip-only-with-a-reason](../rules/skip-only-with-a-reason.md): the marker's `outcome` becomes `ran`, `skipped-by-act` or `skipped-by-user`, and a skip's `reason` holds the act's condition or the user's reason. The act file says whether the run continues past a failed step. When the act stops early, every step it didn't reach is `skipped-by-act`, with the stop as its reason, and close-out still runs.

Then hand [document](../../document/SKILL.md) the task key, the task's memory entry, the step's result (for a skipped step, its outcome and reason), and every document filed for the task so far. After the first filing, write the task record's location that document returns into the entry's docs link. After every step, bring the entry's status, next step and commit up to date — the commit being the head the step left the task's work at — and its index line's status ([keep-the-task-memory-entry](../rules/keep-the-task-memory-entry.md)). Record the filing in the act marker: the step's `filed` becomes `true`, or, when document can't file the result, `false` with the reason in `unfiled`; keep the unfiled result in the run's report and say it wasn't filed.

Under `--dry-run`, see [dry-run](../modules/dry-run.md).

The output is every step's result and the completed checklist, for [close-out](04-close-out.md).
