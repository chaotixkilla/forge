# Decision record

One page per decision, holding plan's content contract ([record-rejected-alternatives](../../../plan/rules/record-rejected-alternatives.md)) and led by the decision and its status. (basis: maintainer, 2026-10-02) A part of the contract the result doesn't hold — the alternatives an author weighed, say — is stated as not recorded, never reconstructed ([preserve-the-why](../../../../craft/writing/preserve-the-why.md)). (basis: Nygard 2011, through plan's contract)

## Membership

A decision earns its own record when an approval would ratify it and it's a one-way door by the test in [design-for-reversibility](../../../../craft/engineering/design-for-reversibility.md). For a review, that means the one-way doors among the decisions its brief lists; the rest stay in the review record. A decision the requirement itself dictates — the ticket specified the format — is the requirement's, not a design decision: it earns no record, and the spec carries it. (routed to maintainer: one-way doors only, so the few that can't be walked back aren't buried.) In a review the decision is the author's, not the reviewer's: the record names who made it, links the change, and has the status `proposed` until the change lands. A task's own decision records file as `proposed` too, and its ship round's filing sets them to `accepted`, in place. (basis: maintainer, 2026-10-07)

Records are numbered in the task's filing order — `001`, `002`, … — each followed by a two-to-five-word slug of the decision, and a decision filed again keeps its number. (basis: derived from Nygard's numbered records)
