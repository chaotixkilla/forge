# work — usage

Start or resume a piece of engineering work and carry it through its act: the right steps, in the right order, with the task's documentation and memory entry kept current, and the results delivered where they belong.

## When to use
- You're starting engineering work that should leave a trace. work routes it to one of ten acts:
  - **developing** — build or change behavior in your own code;
  - **fixing-a-bug** — find and remove the cause of a defect;
  - **reviewing** — judge someone else's change;
  - **shipping** — land finished work and roll it out;
  - **responding-to-an-incident** — restore a live production service;
  - **maintaining** — keep code healthy without changing its behavior;
  - **researching** — answer a question from outside sources;
  - **prototyping** — answer a feasibility question with throwaway code;
  - **auditing** — judge a whole system's security posture;
  - **learning** — understand an unfamiliar part of the system and document it.
- You're resuming a task from an earlier session and want it picked up where it stopped.
- You want an act's steps run in their proper order, with nothing skipped silently.

## Not for / use instead
- One specific step on its own (review this diff, debug this failure) → that step's skill directly.
- A quick question that produces nothing to review or keep → just ask it.

## Examples
- `work add rate limiting to the export endpoint (PROJ-88)` — routes to developing: spec, plan, decompose, then each unit built, tested, verified, reviewed and opened for review.
- `work review change 230` — routes to reviewing and runs its two passes.
- `work checkout is failing for EU users` — routes to responding-to-an-incident: triage, mitigate, diagnose, communicate.
- `work --task=review-230` — resumes that task where it stopped.
- `work --act=shipping --dry-run` — shows the steps it would propose and what it would record, without running or writing anything.

## Gotchas
- work never does a step's work itself: each step runs as its own skill, and document files the results.
- Every step on an act's checklist is run, skipped under the act's own condition, or skipped by you with a reason. It is never skipped silently.
- Steps never deliver; acts do, at close-out, and work does for a lone step it runs outside an act. Review requests, posts, published documents and work-items go out through the ports.
