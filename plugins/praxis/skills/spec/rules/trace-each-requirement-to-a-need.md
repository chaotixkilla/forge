# Trace each requirement to a need

Every requirement in a spec should answer to someone's stated goal or a real constraint. A requirement that answers to neither is an *orphan*, and an orphan is one of two problems wearing a requirement's clothes: **scope creep** — gold-plating nobody asked for, a feature the specifier thought would be nice — or a **hidden assumption** — a need that is real but was never stated, so the requirement floats free of the reasoning that justifies it. Either way the orphan costs build effort no stakeholder is paying for, or it smuggles in an unexamined belief. This rule requires each requirement to carry its lineage, so the spec contains what is needed and only what is needed, and so time pressure cuts by need rather than by whim.

## The discriminator: whose need dies if this is dropped?

The test for every requirement: **name the actor and the goal it serves, or the explicit constraint it satisfies.**

- **Nameable** — it traces to an actor from the interrogation ([interrogating-prompts](../phases/01-interrogating-prompts.md)) pursuing a stated goal ("as an admin, revoke a user's access so a departed employee loses it"), or to a real constraint (a compliance rule, a performance budget, a behavioral invariant). Keep it — traced.
- **Not nameable** — no actor's goal and no constraint requires it. It is an orphan. Resolve it, don't ship it: if it's **scope creep**, cut it (and record the cut as an out-of-scope note so the decision is visible); if it's a **hidden assumption** (the need is real but unstated), surface the need as an explicit line and *then* the requirement traces to it ([make-the-unsaid-explicit](make-the-unsaid-explicit.md)).

The question that forces the call: *whose need dies if this requirement is dropped?* If you can name the stakeholder and what they lose, the requirement earns its place. If dropping it costs no one anything nameable, it was never a requirement.

## Method

As you structure the requirements ([requirement-structuring](../phases/03-requirement-structuring.md)), link each back to the actor-goal list built during interrogation, or to the constraint that demands it. A requirement seeded from a tracker item or a discussion traces to its source ([ingest-from-issue](../modules/ingest-from-issue.md), [ingest-from-discussion](../modules/ingest-from-discussion.md)) — the originating need, attributed. The traceability is not bureaucratic ceremony: it is the mechanism that makes the priority call in [sequencing-and-sizing](../phases/05-sequencing-and-sizing.md) honest, because a requirement whose need you can name can be weighed, and one whose need you can't should not be in the list to weigh.

## The boundary: derived requirements

Some requirements trace to *another requirement* rather than directly to an actor — a non-functional requirement implied by a functional one ("if users upload files, the system must scan them for malware"), or an interface requirement implied by a data one. That is legitimate lineage, not an orphan: the chain still terminates at a need, one hop removed. The test is whether the chain *terminates* at an actor goal or a constraint — a requirement that traces only to another requirement that itself traces to nothing is still an orphan, just one link further down.
