## Check the checklist

Every step must have ended in one of the outcomes of [skip-only-with-a-reason](../rules/skip-only-with-a-reason.md). A step whose result waits unfiled has ended: only its filing is owed, below. A step with none means the act isn't done: say which, and make running or skipping it the task's next step.

## File what waits and what no step produced

Before delivering, hand [document](../../document/SKILL.md), in one filing, every file waiting in the task's unfiled directory ([keep-the-act-marker](../rules/keep-the-act-marker.md)) and, when the act's Filed section names documentation no step produced — the system documentation of the part the task touched — the steps' results it's drawn from, to file as those types, unless a `closing.md` waiting there already holds it. Record it as [run-the-act](03-run-the-act.md) records a step's filing; when it fails, what document hands back for that documentation is written to `closing.md`.

## Deliver

Deliver what the act file says to deliver, through the port that owns each destination, by [deliver-through-the-ports](../rules/deliver-through-the-ports.md).

Before posting a review on a change, and before the question below, read the change's review feedback through [vcs](../../vcs/SKILL.md). Feedback already there from the account the port posts as may have landed before its session could record it. Only feedback posted on the commit this round reviewed, the entry's `at`, counts, so an earlier round's review is never taken for this one's. It's matched by content, never by stance:

- **The summary** matches when one contains the verdict and every finding this close-out would post, whatever else it adds, such as the link or folded questions. Record it `sent`, with the reference the read returns, and don't post it.
- **The inline feedback** matches question by question: an open question that a comment at its anchor, or a summary that matched, already contains is delivered. Post only the rest; when none is left, record the channel `sent` with the reference the read returns. (basis: derived from never delivering twice, and from a round's review being posted on the commit it reviewed)

Before anything goes out, settle in one question to the user whichever of these apply. Each part the answer leaves open takes its default, and when none applies, deliver without asking.

- **The record before the delivery.** A channel that delivers a step's result waits until that step is filed, and one that links the task's documentation waits until every step that ran is filed. When a step it waits on is still not filed, the user chooses between **hold delivery**, the default, which holds the channel with that filing as what's missing, and **deliver anyway**, recorded on the channel in their words. (basis: maintainer, 2026-10-02; every step for a link, and hold as the default, derived from a record that can't be rebuilt from what was delivered) Only an incident status update [right-sized-status-updates](../rules/right-sized-status-updates.md) schedules, at its cadence matrix's interval or at once on an impact change, never waits on a filing; every other channel does. (basis: derived from never going silent in that rule)
- **A link its readers can open.** What [deliver-through-the-ports](../rules/deliver-through-the-ports.md) asks by the record's reach before a link goes out.
- **A choice the act file leaves to the user**, such as the reviewing act's stance, with the proposal and default the act file gives. A choice for a channel that matched as landed above isn't asked. (basis: derived from a landed channel not being posted again)

Record each channel in the marker's `delivery` as it lands, and never deliver again a channel the marker records as delivered ([keep-the-act-marker](../rules/keep-the-act-marker.md)), as after a takeover. A channel held or returned for hand delivery becomes the task's next step. When the user later confirms it was delivered by hand — in answer to the report, or on resume — record the channel as `sent-by-hand`, and check the done-condition again. Then hand document every channel the marker's `delivery` records, with where it went — those an earlier run delivered and deliver-anyway choices included — to file with the rest and every file still waiting but a `delivery.md`, which this update stands in for ([keep-the-act-marker](../rules/keep-the-act-marker.md)), and record that filing in `delivery` as a step's filing is recorded. (basis: maintainer, 2026-10-02)

## Close the task, or leave it open

Check the act's done-condition, from its act file, against what the run produced and delivered. When it holds, the round closes once the filing below lands, and the task with it until a later review opens its next round ([open-the-task](02-open-the-task.md)): its entry's status becomes `closed`, its index line is removed ([keep-the-task-memory-entry](../rules/keep-the-task-memory-entry.md)), and the round's pages stop changing. When it doesn't hold, whatever it lacks becomes the task's next step and the task stays open.

Either way, bring the memory entry up to date and hand it to document — a closing status in what's handed, written to the memory only once the filing lands — with every file still waiting in the task's unfiled directory, and document brings the task record and the task log up to date. That filing fails when the task record's publish does. Then a task that was closing stays open instead — its status open, its index line kept, filing what waits its next step — the files stay waiting, and the report says so. It writes nothing to the unfiled directory of its own: what it adds is drawn from the memory entry, which keeps it for the next filing to rebuild from. (basis: derived from a closed round taking no more filings, [pages-belong-to-their-task](../../document/rules/pages-belong-to-their-task.md)) A task log the port couldn't update holds nothing back ([mirror-the-task-log](../../document/phases/04-mirror-the-task-log.md)). Discard what the act file says to discard, by the paths the marker records, such as its `copy`, and remove the act marker.

## Report

Tell the user briefly what the act concluded, what was delivered and where, what was recorded, and what's next, and quote each action an input asked for, for the user to answer. Deliver it at the reader's register ([deliver-at-the-readers-register](../../../craft/writing/deliver-at-the-readers-register.md)) and under the report-style settings ([report-style-settings](../../../craft/writing/report-style-settings.md)).

Under `--dry-run`, see [dry-run](../modules/dry-run.md).
