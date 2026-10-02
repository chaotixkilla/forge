# dry-run (`--dry-run`)

Activated by `--dry-run`, referenced from [SKILL.md](../SKILL.md).

The base run routes the work, opens the task, runs the act and delivers. This module runs the routing and planning in full but stops short of every side effect, so the user sees what the act would do before it does it. Deletion test: remove it and work always runs and writes; computing and showing without acting is what the flag turns on.

## The delta

- **Route in full** ([route-the-work](../phases/01-route-the-work.md)) and resolve the task key, without creating the task or its memory entry ([open-the-task](../phases/02-open-the-task.md)).
- **For a lone step** ([route-the-work](../phases/01-route-the-work.md)), show the step it would invoke, what it would deliver, and any missing port it would ask about; ask nothing and invoke nothing.
- **Show the act's steps and the inputs each would receive** ([run-the-act](../phases/03-run-the-act.md)); invoke no step.
- **Show what would be delivered and recorded** ([close-out](../phases/04-close-out.md)); write nothing — no act marker, no memory entry, no documentation, no comment on the change.
