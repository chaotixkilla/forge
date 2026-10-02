# Keep the act marker

While an act runs, a marker file records where it stands: the end-of-turn checks hold the run to it, and the edit guard lets code change only while this session has one. Each session keeps its own, so an act left behind by a session that ended never unlocks another session's edits, and two acts running at once never overwrite each other. (basis: maintainer, 2026-10-02)

## Where it lives

`.claude/praxis/acts/<session-id>.json`, under the session id praxis's session-start context states, or, when that context states none, the one praxis's note states once work is invoked in a session with no marker. Keep `.claude/praxis/` out of version control through the repository's local, unshared ignore list. (routed to maintainer: a directory in the project's `.claude/`, as session bookkeeping, since the task's state lives in its documentation.)

## What it holds

    {"updated": "2026-10-02T14:41:00Z", "task": "review-230", "act": "reviewing",
     "docs": {"location": "<the task record's location>", "reach": "private-until-shared", "share": "<the port's share line>"},
     "copy": "<the isolated working copy's path>",
     "steps": [{"step": "1:understand", "outcome": "pending", "reason": "", "filed": false, "unfiled": ""}, …],
     "delivery": {"channels": [], "filed": false, "unfiled": ""}}

- `updated` is a UTC time in ISO 8601, set by every write.
- `docs` holds the task record's location, its reach and, for `private-until-shared`, the port's share line, as document last returned them. They stay empty until a filing returns them.
- `copy` holds the path of the isolated working copy the act's "Before the steps" made, or stays empty when it made none.
- `steps` lists the act's steps in order, each keyed by its row number and skill so two steps of one skill stay apart. `outcome` stays `pending` until the step ends in one of the outcomes in [skip-only-with-a-reason](skip-only-with-a-reason.md), and `reason` holds a skip's reason. `filed` becomes `true` once document has filed the step's result.
- `delivery.channels` gets one entry per channel as close-out delivers it. A channel is one submission a port makes, named by the port, the target reference it was handed, and the part, as the port's operation names it: a review summary and its inline feedback are two channels, since vcs posts them as two submissions.

      {"port": "vcs", "target": "review request 230", "part": "review summary",
       "disposition": "sent", "where": "<the reference the port returned, or what's missing>"}

  `disposition` is spelled `sent`, `held`, `degraded-return` or `sent-by-hand`, the four of [deliver-through-the-ports](deliver-through-the-ports.md). `sent` and `sent-by-hand` both count as delivered. A channel the user chose to deliver anyway also carries `"anyway": "<their words>"`. `delivery.filed` and `delivery.unfiled` record the record update after delivery, the way a step's own fields record its filing.

## Unfiled results

When document can't file a result, it hands back what that filing added, as it shaped it ([publish-and-link](../../document/phases/03-publish-and-link.md)). Write it at once to the task's unfiled directory, `.claude/praxis/unfiled/<task>/`, as one file: `<row>-<skill>.md` for a step's result, its step key with the colon as a hyphen, `delivery.md` for the record update after delivery, and `closing.md` for what close-out's own filing adds, the documentation no step produced. Two filings write nothing here when they fail: the one that closes a left-behind act ([open-the-task](../phases/02-open-the-task.md)), and the one that ends close-out, whose additions the memory entry keeps ([close-out](../phases/04-close-out.md)). The file holds the pieces in the order document handed them back, each opened by a line naming its type's slug, with `· section` for a section of a page:

    <!-- document: review-record -->
    …the review record as document shaped it…
    <!-- document: scratchpad · section -->
    …

Put that file's path, relative to the project, in the entry's `unfiled`, and keep `filed` `false`: a file waiting here never counts as filed. `closing.md` has no entry: the file waiting is its only record. The next filing for the task, in this session or a later one, hands document the content of every file waiting there, each under its file name, along with its own result, and document publishes them all in that one filing. When it lands, each file it carried is removed, and its entry's `filed` becomes `true` with `unfiled` cleared. When it fails, every file stays waiting, and the new result's file, when it has one, joins them. (basis: maintainer, 2026-10-02) A filing that carries the delivery hands document every channel `delivery` records, with where it went, so it stands in for a waiting `delivery.md` rather than carrying it: when it lands, that file is removed with the ones it carried, and when a failure writes a new `delivery.md`, it replaces the waiting one and loses nothing. (basis: derived from the marker holding every channel a waiting `delivery.md` holds)

## A marker its session left behind

A session that ends mid-act leaves its marker. Only [open-the-task](../phases/02-open-the-task.md) takes it over or closes it, when the task is resumed. praxis's session-start hook reports each other session's marker that has gone more than two hours without a write, with its task key. (basis: maintainer, 2026-10-02 — two hours, longer than one step usually runs, so a live act seldom reads as left behind, while an ended one is reported the same day.)

Cited by [open-the-task](../phases/02-open-the-task.md), [run-the-act](../phases/03-run-the-act.md), [close-out](../phases/04-close-out.md), the [reviewing](../acts/reviewing.md) act, and document's [find-the-task-documentation](../../document/phases/01-find-the-task-documentation.md) and [publish-and-link](../../document/phases/03-publish-and-link.md).
