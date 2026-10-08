# Round record

What one round of a change did and decided, frozen when the round closes, so a reader can see why the change is as the current state describes it.

## Membership

One page per round of an act that authors a change — developing, fixing a bug, maintaining — when the round decided something: an owner's call (a choice between alternatives, or a decline or deferral of a comment, that the owner's answer to the proposal names; a go-ahead isn't one), a decision record, or a spec or plan the round filed in place of an earlier round's. It is filed once, by the filing that files the round's peer review and closes it, linking what the round's scratchpad holds; round 1 of a task its peer review approves files none, a task done in one round having only its Iterations entry and its task history section. A round that decided nothing has only its section in the [task history](task-history.md) and its entry in the [task record](task-record.md)'s Iterations. It keeps only what the review host doesn't hold; the comments and the diff stay on the host, linked. The round's working notes stay in its [scratchpad](scratchpad.md), which the record links. (basis: maintainer, 2026-10-07)

## Sections

In this order, each present even when empty; an empty section says so in a line. A section is named by what it holds, never by who did the work, and who did it is a field.

1. **Trigger** — what opened the round: the request, for a build; the peer review it answers, linked, for a rework after peer review; the finding or request, for follow-ups.
2. **Changes** — what the round changed, unit by unit, each with its commits, a link to the round's diff on each review request it worked on, the compare link the round's peer review hands for it, and the changes no comment asked for, with their intent.
3. **Decisions** — each owner's call, with the owner and the reason; each review comment declined or deferred, with why and, for a deferral, where it went; each decision record the round filed, linked.
4. **Evidence** — what showed the changes work: the round's test and verify results, each linked to its scratchpad section, and what was left unsettled.
5. **Self-review** — the check before the review request went out: the review step's verdict and its open findings, and the record check's verdict, each linked to the scratchpad section that holds it, with a Reviewer field naming the owner, for whom the review step ran.
6. **Peer review** — each reviewer's verdict, with a link to each of their comments, written when the review comes back.

(basis: maintainer, 2026-10-07)
