## Check the checklist

Every step must have ended in one of the outcomes of [skip-only-with-a-reason](../rules/skip-only-with-a-reason.md). A step with none means the act isn't done: say which, and make running or skipping it the task's next step.

## File what no step produced

When the act's Filed section names documentation no step produced — the system documentation of the part the task touched — hand [document](../../document/SKILL.md) the steps' results it's drawn from, to file as those types, before delivering.

## Deliver

Deliver what the act file says to deliver, through the port that owns each destination, by [deliver-through-the-ports](../rules/deliver-through-the-ports.md). A channel held or returned for hand delivery becomes the task's next step. When the user later confirms it was delivered by hand — in answer to the report, or on resume — record the channel as sent by hand, and check the done-condition again. Hand [document](../../document/SKILL.md) what was delivered and where, to file with the rest.

## Close the task, or leave it open

Check the act's done-condition, from its act file, against what the run produced and delivered. When it holds, the task closes: its entry's status becomes `closed`, its index line is removed ([keep-the-task-memory-entry](../rules/keep-the-task-memory-entry.md)), and its pages stop changing. When it doesn't hold, whatever it lacks becomes the task's next step and the task stays open.

Either way, bring the memory entry up to date and hand it to document, which brings the task record and the task log up to date. Discard what the act file says to discard, and remove the act marker.

## Report

Tell the user briefly what the act concluded, what was delivered and where, what was recorded, and what's next, and quote each action an input asked for, for the user to answer. Deliver it at the reader's register ([deliver-at-the-readers-register](../../../craft/writing/deliver-at-the-readers-register.md)) and under the report-style settings ([report-style-settings](../../../craft/writing/report-style-settings.md)).

Under `--dry-run`, see [dry-run](../modules/dry-run.md).
