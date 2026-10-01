## Find the task

With `--task=<key>`, resume that task: read its memory entry ([keep-the-task-memory-entry](../rules/keep-the-task-memory-entry.md)), take its act from there, and read the documentation it points to, fetched through the [artifacts](../../artifacts/SKILL.md) port by the location the entry records. When the entry's next step waits on a review request, read the request's state through [vcs](../../vcs/SKILL.md) first: an approval completes that unit, changes requested resume the act at its build step with the feedback as input, and a request still waiting is reported and leaves the task open. When the next step is a delivery rather than one of the act's steps, go straight to [close-out](04-close-out.md). A key with no entry is an error — say so and stop.

Without the flag, look through the task lines in the memory index for an open task that links the same change, ticket or branch as the request, and resume it if one does. Otherwise this is a new task. Its key names what it's about: for a review, the change (`review-pr-230` for a pull request, `review-<branch>` for a local branch); for other work, the ticket's identifier, else the branch name unless it's the integration line, else the date and a two-to-four-word slug of the request. (routed to maintainer: proposed in that order, each more stable than the next.) A closed task on the same change stays closed: the new task takes its key with the next round number, `review-pr-230-2`. If an entry already exists under the new key, resume it when it's open.

## Prepare the act

If the act file has a "Before the steps" section, carry it out now: it brings in what the rest of this phase reads, such as the change's branch name and head commit. When it needs a port that isn't configured, carry out what it can without the port, and the rest once the proposal's answer has set the port up ([run-the-act](03-run-the-act.md)).

## Gather the intent, locate the rationale

Classify each input by [form-your-own-view-first](../../../craft/evidence/form-your-own-view-first.md) as you meet it. Read the intent now — the ticket, a spec, an RFC, the requirement the work must meet, the conversation the request points at — fetching a tracker item through [project-mgmt](../../project-mgmt/SKILL.md) and a document through [knowledge](../../knowledge/SKILL.md); a file in the repository is read directly. Find its reference in the request, the change's branch name or the task's own record, never inside the rationale; when none of them names one, record that, and the proposal in [run-the-act](03-run-the-act.md) asks for it. Of the rationale, record only where it is, and don't open it here: every inline step inherits what this context has read, so a description read now would reach every step.

A ticket that also proposes a solution is read whole, and the task record notes that its proposal was seen. (routed to maintainer: an isolated reader passing on only the requirements would keep the proposal out, at the cost of a subagent per ticket.)

On resume, compare the intent as it stands now with the requirements and acceptance criteria the task record copied when the task opened. A change in what it requires — a requirement or acceptance criterion added, removed, or changed in meaning — runs the act again from its first step; a rewording that leaves every requirement the same is noted in the task record and changes nothing. (routed to maintainer: proposed.) Read other people's edits to the task's documents under [edits-change-intent-not-actions](../rules/edits-change-intent-not-actions.md).

## Create or update the entry

A new task's title comes from its ticket, else its branch name — never from the change's description or title, which are rationale. Creating the task writes its memory entry (status `open`, next: the act's first step, the commit it's working at, today's date) and its index line at once, so a run that stops mid-act can be resumed.

On resume, when the change's head has moved past the commit the entry records — which, since the entry records the act's own head after every step, means someone else's commits — the act runs again from its first step, from a fresh "Before the steps".

## Record the running act

Write the act marker the end-of-turn checks read, at `.claude/praxis-act.json`: the task key, the act, and the act's steps in order, each keyed by its row number and skill so two steps of one skill stay apart — `{"task": "review-pr-230", "act": "reviewing", "steps": [{"step": "1:understand", "outcome": "pending", "reason": "", "filed": false, "unfiled": ""}, …]}`. Keep it out of version control through the repository's local, unshared ignore list. (routed to maintainer: a file in the project's `.claude/`, as session bookkeeping, since the task's state lives in its documentation.) On resume, seed each step's outcome from the task record's "What was done", and continue at the entry's next step. Under `--dry-run`, write nothing ([dry-run](../modules/dry-run.md)).

The output is the open task — its key, its memory entry, the intent read, and where the rationale is — and the marker, for [run-the-act](03-run-the-act.md).
