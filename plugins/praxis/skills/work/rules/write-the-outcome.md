# Write the outcome

A program that runs praxis, such as a hands-off host or a dashboard, needs to know how a run ended without parsing the memory entry's markdown. So every run of work that reaches a task ends by writing a small machine-readable outcome: what the entry and the act marker hold, and how the run ended. (basis: maintainer, 2026-10-20)

## When

As the run's last write, whatever ends it, such as:
- close-out's report, after any feedback ([feedback-on-praxis](feedback-on-praxis.md));
- an act's stop;
- a question a run that can't ask reports;
- another session's act marker it can't settle;
- a Close that failed;
- route 2's report on a wait.

A run that goes on into another act, such as a rework opened after a peer review, writes it again at that act's end, replacing the first. A `--dry-run` writes none. It is written every time, whatever the attendance signal.

## Where

`.claude/praxis/outcomes/<session-id>.json` in the main checkout, a sibling folder of the act markers' ([keep-the-act-marker](keep-the-act-marker.md)), replaced by the session's next run.

## What it holds

One JSON object, with these keys and no others:

    {"praxis_version": "<the installed version>", "updated": "2026-10-20T14:41:00Z", "session": "<session id>",
     "task": "PROJ-12", "title": "invoice export", "act": "developing", "round": "1.1",
     "status": "open · awaiting review on review requests 405, 406", "next": "<the entry's next step>",
     "ended": "delivered", "docs": "<the task record's location, or empty>",
     "delivered": [{"port": "vcs", "target": "review request 405", "part": "description", "where": "<link>"}],
     "held": [{"port": "communication", "target": "<target>", "part": "notice", "why": "<what's missing>"}],
     "questions": [], "feedback": null}

- `praxis_version`: the installed praxis's version, from `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`. `updated`: the UTC time of the write.
- `task` and `title`: the entry's task line, split into its key and its title without the ticket. `act`, `round`, `status`, `next` and `docs`: as the entry holds them after this run, `round` being its latest round line's number. A task whose entry waits on a question's answer takes the key and round its default would settle.
- `ended`, the first of these that applies:
  - `closed`: the task closed;
  - `declined`: the proposal was declined;
  - `waiting-on-answer`: a run that can't ask ended at a question;
  - `stopped`: the act stopped early, by the user or at a step;
  - `waiting`: route 2 reported a wait, filing no peer review;
  - `delivered`: close-out delivered at least one channel;
  - `filed`: close-out delivered nothing;
  - `reported`: the run ended at a report, running no act's steps and delivering nothing, as a failed Close, a closed task reported as closed, or a finding filed with no act does.
- `delivered`: each channel close-out recorded as `sent` or `sent-by-hand` in this run, a channel matched as already landed included, with where it went. They are read as close-out recorded them, before it removed the marker.
- `held`: each channel held or returned for hand delivery, with what's missing, read as `delivered` is.
- `questions`: for `waiting-on-answer`, one `{"item", "options", "default"}` per question item, as it would have been asked: `options` a list of strings, one per choice, the default among them, and `default` empty for an item that has none. Empty otherwise.
- `feedback`: the feedback file's path when developer mode wrote one, else `null`.

When a value isn't known, as a docs location before any filing landed, it is the empty string, or an empty list for a list. A write that fails is reported in a line after the report, and changes nothing else.
