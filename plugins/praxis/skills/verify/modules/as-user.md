# as-user (`--as-user=<persona>[,<persona>…]`)

Activated by `--as-user`, referenced from [exercise-the-flows](../phases/03-exercise-the-flows.md). The flag takes **one or more persona names, comma-separated**; each name is resolved on its own and each yields its own drive, its own record, and its own units per [verdict-scale](../rules/verdict-scale.md)'s composition order. A comma-separated value is never resolved as a single persona whose name contains a comma.

The base run drives each flow as an operator who knows the system — who knows where things are, what the next step is, and what a healthy response looks like. This module re-drives the same flows in one named user's shoes and reports what *that* user encounters, under that user's constraints, through the access path that user actually arrives by. The operator's drive answers whether the flow can be completed by someone holding the whole model of it; that is a different question from whether it can be completed by the person it was built for.

## The delta

Re-drive each flow the run already framed, holding the persona's constraint for the entire drive rather than sampling it at the interesting steps — a constraint dropped halfway through produces a record of a user who does not exist. Where the persona is a user of assistive technology, the flow is exercised **through that access path**, and what is reported is what is perceivable and operable that way: what was presented or announced at each step, what was reachable, what could be operated with the input that user has, and where the flow stalled. This is not an audit of the markup or of a structural checklist — a surface can satisfy every structural rule and still leave this user unable to finish, and it can violate one and still be completable. The finding is what the drive encountered.

Record each step as three things: the persona constraint in play, the step, and what was observed through that access path. Findings stay **scoped to that persona's path** — a fact about how that user's route behaves, never a claim about every user — and two personas are two drives with two records, never averaged into a single "the user" result, because the whole reason to name a persona is that their path is not the general one.

**Deletion test:** without the flag, [exercise-the-flows](../phases/03-exercise-the-flows.md) drives each framed flow once from the operator's vantage and records the functional observation; the persona re-drive, the constraint it imposes on the access path, and the persona-scoped findings are the added behavior. Remove the module and no framed flow goes undriven — it is only driven by one kind of user.

## What a persona must supply before the pass can run

The persona domain is **open by design** — the value is the project's own vocabulary for its own users. What *is* pinned is what each name has to resolve to before a drive is possible — two things:

- **The constraints the persona operates under** — what they can perceive, what they can operate and with which input, what they already know about the system, and the access path they arrive by.
- **The goal they came to accomplish** — what completing the flow means *for them*, since a persona whose goal is unstated cannot be observed failing to reach it.

`(basis: derivation, not a choice about which users exist — a drive cannot be constrained by a persona whose constraints are unstated, and a failure to reach a goal cannot be observed when no goal was named; both are read out of the project's own material, which is what keeps the domain open while the input requirement stays fixed.)`

Resolve both from the project's own material — its spec, design notes, prior user research, whatever the codebase already says about its users — per named persona, and where several are named a persona that resolves is driven whether or not its neighbours do. **Error case:** if a named persona cannot be resolved to constraints and a goal from that material, do not invent them from a stereotype; that manufactures findings about a user who may not exist and dresses them as observations. Report that persona's pass as **requested and not performed**, name the persona given, and name what would resolve it (the material that would have to exist, or the constraints the caller can state directly). The framed flows are still driven by the base run, so the functional pass is unaffected — only the persona vantage is missing, and it is reported missing.

## The discipline that separates this from guesswork

Every line this pass writes down is either something the drive did and showed, or something you concluded from it. Before writing each line, apply the discriminator defined in [observation-over-inference](../rules/observation-over-inference.md) and label the line as the side of that discriminator it falls on — the two may both be reported and may never be conflated, and this module is where the temptation to conflate them is strongest.

The specific failure mode: a claim about a user whose path you did not exercise. *"A user relying on announced output would be lost at this step"*, written after looking at the surface rather than driving it through that access path, is an inference — a defensible one, sometimes, but it is not a persona finding and it does not go in the persona record. A persona finding requires all three of the recorded elements above: the constraint in play, the named step, and what was observed **through that access path**. A line missing any one of the three is an inference at best, is labelled one, and never counts as evidence about that user.

## What the pass yields

Sort each thing the persona hit into one of two kinds, because they travel differently:

- **A completion failure on that access path** — the persona could not complete a step, or could not complete the flow, through the path they use, while the operator's drive completed it. This is a behavioral observation about a real path, not a preference, so it returns into the observation record [exercise-the-flows](../phases/03-exercise-the-flows.md) hands onward and is classified there like any other malfunction — with the persona and access path attached, so the defect reads as scoped to that path rather than as a general break.
- **Friction on that access path** — the persona completed the step, but at a cost: the extra attempts, the state they could not interpret, the information they had to hold themselves. These are friction findings and clear the same bar every friction finding in the run answers to — anchored to a step that was driven, an expectation grounded in something outside the driver's own preference, an observed consequence, and no proposal attached — with the persona's stated constraint doing the grounding work, which is what makes a persona finding the easiest kind to ground and the easiest kind to fake.

`(routed to maintainer: the split above is this build's proposal, not a set house standard — the call at issue is whether "the persona cannot complete the flow through the path they use" is a functional defect or a usability finding. Proposed as a functional observation, on the reasoning that a change which works only for users who do not need that access path has not done what was claimed, which is the functional question and not a matter of preference; friction short of that stays a finding. Confirm, or set the narrower policy — for example, that a persona-path completion failure is a defect only where that path is one the project commits to supporting.)`

## Degraded case

The pass depends on being able to exercise the persona's access path. Where it cannot be exercised — the run has no way to drive the flow through that path, or no way to observe what is presented on it — the pass is **reported as not performed**, with the path named and the reason stated, and the run's scope is described as narrowed: the flows were observed from the operator's vantage only.

Do not substitute a reading. Inspecting the code, the markup, or the interface definition to say what that user *would* encounter produces an inference about an unexercised path, and reporting it in place of the pass is worse than reporting nothing, because it looks like evidence about that user and is not. Where the path can be exercised for some flows and not others, drive the ones it can and name the rest as unobserved on that path — an unexercised path yields no persona result, clean or otherwise. In every degraded shape, the functional verdicts the base run assigned stand untouched: the absence of a persona observation is a gap in what this run saw, never a downgrade of what it did see.
