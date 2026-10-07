# Keep the act marker

While an act runs, a marker file records where it stands: the end-of-turn checks hold the run to it, and the edit guard lets code change only while this session has one whose proposal is answered. Each session keeps its own, so an act left behind by a session that ended never unlocks another session's edits, and two acts running at once never overwrite each other. (basis: maintainer, 2026-10-02)

## Where it lives

`.claude/praxis/acts/<session-id>.json`, under the session id praxis's session-start context states, or, when that context states none, the one praxis's note states once work is invoked in a session with no marker. Keep `.claude/praxis/` out of version control through the repository's local, unshared ignore list. (routed to maintainer: a directory in the project's `.claude/`, as session bookkeeping, since the task's state lives in its documentation.)

## What it holds

    {"updated": "2026-10-02T14:41:00Z", "task": "review-230", "act": "reviewing",
     "answered": "2026-10-02T14:12:00Z",
     "docs": {"location": "<the task record's location>", "reach": "private-until-shared", "share": "<the port's share line>"},
     "copy": "<the isolated working copy's path>",
     "steps": [{"step": "1:understand", "outcome": "pending", "reason": "", "filed": false, "unfiled": "", "failure": ""}, …],
     "delivery": {"channels": [], "filed": false, "unfiled": "", "failure": ""}}

- `updated` is a UTC time in ISO 8601, set by every write.
- `answered` is the UTC time the act's proposal was settled ([run-the-act](../phases/03-run-the-act.md)): the user's answer when it asked a question, else the moment its steps were shown. It is read from the clock at the write that records it, never estimated, and stays empty until then. While it's empty no step runs and no code changes: the edit guard and the end-of-turn checks read it. (basis: maintainer, 2026-10-07) A marker seeded on resume, or taken over, that has no `answered` gets the time of that write when it holds an outcome for any step of this act, from the task record's current round, a file waiting in the unfiled directory or the taken-over marker itself. Otherwise it stays empty. A taken-over marker that records `answered` gets the take-over write's time in its place, so none of this session's earlier work counts against it. (basis: derived — no step runs before the answer; the clock, derived from the end-of-turn check's transcript timestamps)
- `docs` holds the task record's location, its reach and, for `private-until-shared`, the port's share line, as document last returned them. They stay empty until a filing returns them.
- `copy` holds the path of the isolated working copy the act's "Before the steps" made, or stays empty when it made none.
- `steps` lists the act's steps in order, each keyed by its row number and skill so two steps of one skill stay apart. `outcome` stays `pending` until the step ends in one of the outcomes in [skip-only-with-a-reason](skip-only-with-a-reason.md), and `reason` holds a skip's reason. `filed` becomes `true` once document has filed the step's result. `unfiled` and `failure` are set together, only when a filing fails (below). An entry seeded or taken over with an `unfiled` file and no `failure` gets `failure` saying the file waits from an earlier session. (basis: derived — the waiting file doesn't keep the port's outcome)
- `delivery.channels` gets one entry per channel as close-out delivers it. A channel is one submission a port makes, named by the port, the target reference it was handed, and the part, as the port's operation names it: a review summary and its inline feedback are two channels, since vcs posts them as two submissions. A ship round's report names in its part the requests it covers and what each reached ([shipping](../acts/shipping.md)).

      {"port": "vcs", "target": "review request 230", "part": "review summary",
       "disposition": "sent", "where": "<the reference the port returned, or what's missing>"}

  `disposition` is spelled `sent`, `held`, `degraded-return` or `sent-by-hand`, the four of [deliver-through-the-ports](deliver-through-the-ports.md). `sent` and `sent-by-hand` both count as delivered. A channel the user chose to deliver anyway also carries `"anyway": "<their words>"`. `delivery.filed`, `delivery.unfiled` and `delivery.failure` record the record update after delivery, the way a step's own fields record its filing.

## Unfiled results

When a filing fails, document hands back what that filing added, as it shaped it, with the outcome the artifacts port returned ([publish-and-link](../../document/phases/03-publish-and-link.md)). Only then, write it at once to the task's unfiled directory, `.claude/praxis/unfiled/<task>/`, as one file: `<row>-<skill>.md` for a step's result, its step key with the colon as a hyphen, `delivery.md` for the record update after delivery, `closing.md` for what close-out's own filing adds, the documentation no step produced, and `finding.md` for the pieces of a finding filed outside the steps that came with no step key, and for everything a finding filed while no act runs hands back ([open-the-task](../phases/02-open-the-task.md)), a later one appended to it. Four filings write nothing here when they fail, since the memory entry or the review host keeps what each adds: the filing of a round's peer review ([close-out](../phases/04-close-out.md)), the opening filing ([run-the-act](../phases/03-run-the-act.md)), the one that closes a left-behind act ([open-the-task](../phases/02-open-the-task.md)), and the one that ends close-out ([close-out](../phases/04-close-out.md)). A finding or a proposal's dispositions the opening filing carried are the exception: their pieces go to `finding.md`. The file holds the pieces in the order document handed them back, each opened by a line naming its type's slug, with `· section` for a section of a page, the step key the piece came with, or `no step`, what the step ran for when it came with one, and `· held` for a piece a reader's comment held:

    <!-- document: review-record · 4:review -->
    …the review record as document shaped it…
    <!-- document: scratchpad · section · 5:develop · unit 2 -->
    …
    <!-- document: scratchpad · section · no step -->
    …

The key decides where a waiting piece lands when it is filed ([publish-and-link](../../document/phases/03-publish-and-link.md)), so a correction that waited still replaces the claim it corrects. (basis: maintainer, 2026-10-07)

Put that file's path, relative to the project, in the entry's `unfiled` and the port's outcome in its `failure`, and keep `filed` `false`: a file waiting here never counts as filed. Pieces a filing hands back because a reader's comment held their page are written to the step's file the same way, the hold as their `failure`, while the step's `filed` stays `true` for the pages that landed; seeding on resume keeps it so. A file written without a failed filing is a filing skipped, and the end-of-turn check reads an `unfiled` with no `failure` as unrecorded. (basis: maintainer, 2026-10-07) `closing.md` and `finding.md` have no entry: the file waiting is their only record. The next filing for the task, in this session or a later one, hands document the content of every file waiting there, each under its file name, along with its own result, and document publishes them all in that one filing. When it lands, each file it carried is removed, and its entry's `filed` becomes `true` with `unfiled` and `failure` cleared. When it fails, every file stays waiting, and the new result's pieces are written to its file: appended to a step's waiting file, replacing the pieces it holds for what the new result ran for, and those naming nothing it ran for under the same type and section heading, or all of them for a step that runs once, as a loop back's rerun or a correction does. (basis: maintainer, 2026-10-02) A filing that carries the delivery hands document every channel `delivery` records, with where it went, so it stands in for a waiting `delivery.md` rather than carrying it: when it lands, that file is removed with the ones it carried, and when a failure writes a new `delivery.md`, it replaces the waiting one and loses nothing. (basis: derived from the marker holding every channel a waiting `delivery.md` holds)

## A marker its session left behind

A session that ends mid-act leaves its marker. Only [open-the-task](../phases/02-open-the-task.md) takes it over or closes it, when the task is resumed. praxis's session-start hook reports each other session's marker that has gone more than the marker idle time, two hours, without a write, with its task key. (basis: maintainer, 2026-10-02 — two hours, longer than one step usually runs, so a live act seldom reads as left behind, while an ended one is reported the same day.)

Cited by [open-the-task](../phases/02-open-the-task.md), [run-the-act](../phases/03-run-the-act.md), [close-out](../phases/04-close-out.md), the [reviewing](../acts/reviewing.md) act, and document's [find-the-task-documentation](../../document/phases/01-find-the-task-documentation.md) and [publish-and-link](../../document/phases/03-publish-and-link.md).
