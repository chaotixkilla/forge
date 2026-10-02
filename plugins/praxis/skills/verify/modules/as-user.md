# as-user (`--as-user=<persona>[,<persona>…]`)

Activated by `--as-user`, referenced from [exercise-the-flows](../phases/03-exercise-the-flows.md). The flag takes **one or more persona names, comma-separated**; each name is resolved on its own and each yields its own drive, its own record, and its own units per [verdict-scale](../rules/verdict-scale.md)'s composition order. A comma-separated value is never resolved as a single persona whose name contains a comma.

The base run drives each flow as an operator who knows the system — who knows where things are, what the next step is, and what a healthy response looks like. This module re-drives the same flows in one named user's shoes and reports what *that* user encounters, under that user's constraints, through the access path that user actually arrives by.

## The delta

Re-drive each flow the run already framed, holding the persona's constraint for the entire drive rather than sampling it at the interesting steps — a constraint dropped halfway through produces a record of a user who does not exist. Where the persona is a user of assistive technology, the flow is exercised **through that access path**, and what is reported is what is perceivable and operable that way: what was presented or announced at each step, what was reachable, what could be operated with the input that user has, and where the flow stalled. This is not an audit of the markup or of a structural checklist — a surface can satisfy every structural rule and still leave this user unable to finish, and it can violate one and still be completable.

Record each step as three things: the persona constraint in play, the step, and what was observed through that access path. Findings stay **scoped to that persona's path** — a fact about how that user's route behaves, never a claim about every user — and two personas are two drives with two records, never averaged into a single "the user" result, because the whole reason to name a persona is that their path is not the general one.

**Deletion test:** without the flag, [exercise-the-flows](../phases/03-exercise-the-flows.md) drives each framed flow once from the operator's vantage and records the functional observation; the persona re-drive, the constraint it imposes on the access path, and the persona-scoped findings are the added behavior. Remove the module and no framed flow goes undriven — it is only driven by one kind of user.

## What a persona must supply before the pass can run

The persona domain is **open by design** — the value is the project's own vocabulary for its own users. What *is* pinned is what each name has to resolve to before a drive is possible — two things:

- **The constraints the persona operates under** — what they can perceive, what they can operate and with which input, what they already know about the system, and the access path they arrive by.
- **The goal they came to accomplish** — what completing the flow means *for them*, since a persona whose goal is unstated cannot be observed failing to reach it.

`(basis: derived from what a persona-constrained drive needs)`

Resolve both from the project's own material — its spec, design notes, prior user research, whatever the codebase already says about its users — per named persona, and where several are named a persona that resolves is driven whether or not its neighbours do. **Error case:** if a named persona cannot be resolved to constraints and a goal from that material, do not invent them from a stereotype; that manufactures findings about a user who may not exist and dresses them as observations. Report that persona's pass as **requested and not performed**, name the persona given, and name what would resolve it (the material that would have to exist, or the constraints the caller can state directly). The framed flows are still driven by the base run, so the functional pass is unaffected — only the persona vantage is missing, and it is reported missing.

## The discipline that separates this from guesswork

Before writing each line, apply the discriminator defined in [observation-over-inference](../../../craft/evidence/observation-over-inference.md) and label the line `observed` or, on the inference side, with the certainty it reaches on the scale in [results-and-certainty](../../../craft/evidence/results-and-certainty.md) — traced, inferred or unverified; this module is where the temptation to conflate observation and inference is strongest.

The specific failure mode: a claim about a user whose path you did not exercise. *"A user relying on announced output would be lost at this step"*, written after looking at the surface rather than driving it through that access path, is an inference — a defensible one, sometimes, but it is not a persona finding and it does not go in the persona record. A persona finding requires all three of the recorded elements above: the constraint in play, the named step, and what was observed **through that access path**. A line missing any one of the three is labelled with the certainty it reaches, never `observed`, and never counts as evidence about that user.

## What the pass yields

Sort each thing the persona hit into one of two kinds, because they travel differently:

- **A completion failure on that access path** — the persona could not complete a step, or could not complete the flow, through the path they use, while the operator's drive completed it. This is a behavioral observation about a real path, not a preference, so it returns into the observation record [exercise-the-flows](../phases/03-exercise-the-flows.md) hands onward and is classified there like any other malfunction — with the persona and access path attached, so the defect reads as scoped to that path rather than as a general break.
- **Friction on that access path** — the persona completed the step, but at a cost: the extra attempts, the state they could not interpret, the information they had to hold themselves. These are friction findings and clear the same bar every friction finding in the run answers to — anchored to a step that was driven, an expectation grounded in something outside the driver's own preference, an observed consequence, and no proposal attached — with the persona's stated constraint doing the grounding work, which is what makes a persona finding the easiest kind to ground and the easiest kind to fake.

`(routed to maintainer: a persona-path completion failure is a functional observation, and friction short of it a finding, since a change that works only for users who don't need that path hasn't done what was claimed; alternative: a defect only where the project commits to supporting that path)`

## Degraded case

The pass depends on being able to exercise the persona's access path. Where it cannot be exercised — the run has no way to drive the flow through that path, or no way to observe what is presented on it — the pass is **reported as not performed**, with the path named and the reason stated, and the run's scope is described as narrowed: the flows were observed from the operator's vantage only.

Do not substitute a reading. Inspecting the code, the markup, or the interface definition to say what that user *would* encounter produces an inference about an unexercised path, and reporting it in place of the pass is worse than reporting nothing, because it looks like evidence about that user and is not. Where the path can be exercised for some flows and not others, drive the ones it can and name the rest as unobserved on that path — an unexercised path yields no persona result, clean or otherwise. In every degraded shape, the functional verdicts the base run assigned stand untouched.
