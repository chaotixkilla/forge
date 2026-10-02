# prior-pass (`--prior=<review>`)

Activated by `--prior=<review>`, referenced from [scope-the-review](../phases/01-scope-the-review.md).

The base review hunts the change from scratch. This module builds on a prior pass over the same change, typically one that held the author's rationale back ([hold-rationale](hold-rationale.md)). The prior result is the starting list, and this pass reads the rationale against it. Deletion test: remove it and review still runs as a fresh pass; starting from a prior result is what the flag turns on.

## The delta

- **Read the prior pass.** Handed its report, use it; handed where it was filed, read it back through the [artifacts](../../artifacts/SKILL.md) port's fetch, by that location. If it can't be read — the fetch comes back not-found or unavailable, or a handed report is unreadable — stop and say so, as [hosted-change](hosted-change.md) does; under `--gate` the status is could-not-review.
- **Confirm it's the same change.** The prior review's scope line names the commit it read. If that isn't the change's current head, the change has moved: say so, and review it afresh rather than trust findings about code that's gone.
- **Run on the prior result instead of from scratch.** [scope-the-review](../phases/01-scope-the-review.md) fetches the rationale; [build-the-mental-model](../phases/02-build-the-mental-model.md) reads it against the prior pass's model; the hunt and craft passes run only where the rationale points at something the prior pass didn't look at; [triage-and-rank](../phases/05-triage-and-rank.md) re-triages only what this pass changed. Everything else stands as the prior pass judged it.
- **Settle each item the prior pass left.** An author's stated reason counts once it's checked against the code; a reason that isn't checked settles nothing.
  - A **question** the checked rationale answers is closed, citing where; one it doesn't answer stands ([questions-for-the-author](../rules/questions-for-the-author.md)).
  - A **finding** the checked rationale shows is intended and correct is withdrawn, with why. One the rationale explains but doesn't clear keeps its grade and carries the author's reason.
  - A **decision** in the brief gains the author's alternative and reasoning, where the rationale gives them; a decision the rationale reveals that the prior pass missed is added.
- **Where the rationale and the evidence disagree,** [build-the-mental-model](../phases/02-build-the-mental-model.md)'s divergence rule applies. Where the evidence the prior pass gathered, such as an official source or a test result, doesn't settle which is right, it's a question.
- **The report carries every standing item, with its mark,** so a reader sees what the rationale did. A finding or decision ends with `· withdrawn: <why>`, `· author: <their reason>`, `· new` or `· regraded from <grade>`, and a closed question reads `file:line — the question — answered: <where>`.

(basis: maintainer, 2026-09-30)
