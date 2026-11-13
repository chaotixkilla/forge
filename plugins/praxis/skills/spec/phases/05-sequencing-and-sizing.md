Carve the concrete spec into independently shippable slices, then give every slice a **size verdict** and every requirement a **priority**, and order the slices by dependency and risk.

## Break into independently shippable slices

Find the thin vertical slice that delivers value on its own, then layer. A slice cuts **vertically** — through every layer needed to produce user-observable value — rather than horizontally (a "data layer" slice that is useless until three later slices land is not a slice, it is a task). The unit is the increment a team can ship and demonstrate by itself; sizing (below) is how you judge whether a candidate slice is that unit.

## The sizing scale

A slice is well-sized when it clears three properties, grounded in the INVEST criteria for a good increment:

- **Independently shippable** — delivers user-observable value on its own, cutting vertically through all layers (INVEST: *valuable / vertical*).
- **Independently verifiable** — its acceptance criteria can be checked without the rest of the spec built (INVEST: *testable*).
- **Fits one delivery cadence** — completable within the team's iteration unit, in whatever bound the team uses (one sprint, ≤ N days, ≤ N acceptance criteria) rather than a fixed number (INVEST: *small — fits within an iteration*).

`(basis: Wake's INVEST, 2003; the Agile Alliance glossary; maintainer, 2026-07-04)`

Absent a known team cadence at runtime, do not stall or invent a number: size by the qualitative bar alone — one vertical increment, independently shippable and verifiable — and flag the missing cadence as an assumption to confirm ([make-the-unsaid-explicit](../rules/make-the-unsaid-explicit.md)). The cadence bound only sharpens the split call at the margin; the value-seam and independent-verifiability discriminators carry the verdict without it.

The three-state verdict, assigned by walking the properties:

- **right-sized** — one value increment; independently shippable and verifiable; fits one cadence.
  - *Anchor:* "an owner grants read access to a document and the grantee can open it" — ships and demos on its own, verifiable alone, one iteration.
- **too-big — split it** — fails any one of: cannot be completed in one cadence, **or** bundles more than one independently-releasable increment, **or** its criteria cannot all be verified together. Split along the *value* seam into vertical sub-slices, never into horizontal layers.
  - *Anchor (top of scale):* "all of sharing" — grant, revoke, notify, audit, and external recipients bundled; many increments across many cadences. Split.
- **too-small — merge it** — delivers no independently-observable value (a pure sub-task of another slice). Merge into the slice whose value it completes.
  - *Anchor (bottom of scale):* "add the `permission_level` column" — no user-observable value alone, verifiable only once the grant flow exists. Merge into the grant slice.

Adjacent-state discriminators: **right-sized vs too-big** — can it ship *and* be verified as one increment within one cadence? All three → right-sized; fails any → too-big. **right-sized vs too-small** — does it deliver observable value on its own? Yes → right-sized; no (a pure sub-task) → too-small. A slice with value of its own that can only be verified once another slice is built is right-sized, sequenced after that slice in the dependency graph below. `(basis: derived from value being the too-small test)`

## The priority scale (MoSCoW)

Every requirement carries a priority, because when time runs short the priority is what tells everyone what gets cut.

`(basis: maintainer, 2026-07-04; after DSDM's MoSCoW, Agile Business Consortium)`

Priority is release-scoped: a requirement's rung is stated relative to *this* cycle, and can change for a later one.

- **Must** — the release fails its core purpose without it; no viable solution omits it.
  - *Assignment test (DSDM):* ask "what happens if this is not met?" If the answer is "cancel the release — there is no point shipping without it," it is a Must.
  - *Anchor (top of scale):* for "add sharing," *an owner can grant another account access to a document* — without it the feature does not exist.
- **Should** — important and painful to omit, but the solution is still viable without it; a defensible temporary gap.
  - *Anchor:* *a shared user is notified by email* — the feature works without it (they find the share in-app), but omitting it hurts adoption.
- **Could** — desirable, with less impact if omitted than a Should; the first pool cut when time runs short.
  - *Anchor:* *the share dialog remembers the last team you shared with* — a convenience whose absence is minor friction.
- **Won't (this time)** — a real candidate the team has consciously agreed not to deliver in this cycle; recorded, not deleted, to fix the scope boundary.
  - *Anchor (bottom of scale):* *sharing to external, non-account recipients* — explicitly deferred and recorded, so it is neither silently rebuilt nor re-argued.

Adjacent-rung discriminators: **Must vs Should** — the *workaround test*: if any viable workaround exists (even a painful, manual one), it is not a Must — demote to Should; a Must has no workaround. **Should vs Could** — the *degree of pain* if unmet, measured in business value or people affected; both leave the solution viable, so they are separated by magnitude, not kind: **Should** when its absence reaches every user of the feature or adds recurring support load, **Could** when it reaches some users occasionally. (routed to maintainer: every-user-or-recurring-support as the Should line, where DSDM leaves it relative.) **Could vs Won't** — is it in this cycle at all? A candidate you would do if time allowed → Could; one you have agreed not to do now → Won't.

**A criterion the intent states as acceptance** — a ticket's acceptance criteria, a requirement the request marks as required — enters as a Must, because the requester set it. When the workaround test would demote it, keep it a Must and surface the divergence as an open question for the requester, who owns the call: never demote a stated acceptance quietly. `(basis: derived — reconcile the intent, don't silently overrule it)`

*Inflation guard:* if more than half of this cycle's requirements — Won't (this time) excluded — land on Must, the ladder has collapsed — re-apply the workaround test to each, and any Must with a viable workaround becomes a Should. A Must-heavy spec is a signal to recheck, not a hard cap. `(basis: DSDM's ≤ 60% Must-have effort guideline, adapted here to a requirement-count smell test)`

The rungs are assigned to requirements; a **slice inherits the highest priority among the requirements it delivers** — a slice carrying any Must is a Must slice, even when a lower-priority requirement was merged into it (a too-small requirement folds into the slice whose value it completes). `(basis: derived from every slice delivering at least one prioritized requirement)` This is what lets the dependency check below reason about a "Must slice" from a scale defined on requirements.

## Flag dependencies and risks

Two final passes over the sized, prioritized slices. **Dependencies:** what must exist before a slice can be built — the order follows the dependency graph, thin vertical slice first, then the layers that build on it. Slices with **no** dependency between them carry no imposed order — being independently shippable is their definition, so their relative sequence is *deliberately left open* (pinning it would be false precision, and priority is the cut axis here, not a sequencing one). A Must slice that depends on a Could slice is a contradiction to resolve, not a sequence to ship — resolve it by re-running the workaround test (above) on the depended-on requirement: a genuine build-dependency of a Must has no workaround, so it is itself a Must and gets promoted, or the two slices merge along the value seam. Never ship the Must ahead of what it needs. **Risks:** what is uncertain enough to threaten the estimate or the approach — an unknown that could invalidate a slice — is flagged for a spike (a time-boxed investigation) *before* the slice is committed, rather than discovered mid-build.

## The assembled spec

The finished spec is the assembly of what the phases produced, and its *content* is fixed even though its *layout* is not. It carries: the requirements in their taxonomy buckets ([requirement-structuring](03-requirement-structuring.md)), each with its acceptance criteria (and the examples and counter-examples that pin them), its priority rung, and its trace to a need ([trace-each-requirement-to-a-need](../rules/trace-each-requirement-to-a-need.md)); the sized, prioritized slices ordered by dependency, with risks flagged for spikes; the surfaced assumptions, open questions, and explicit out-of-scope list ([make-the-unsaid-explicit](../rules/make-the-unsaid-explicit.md)); and, on the base (non-strict) path, any testability warnings on requirements still below the bar ([testable-or-its-not-a-requirement](../rules/testable-or-its-not-a-requirement.md)). That content is the deliverable in every run — the interrogation machinery that produced it is not part of it. The concrete document layout — section order, headings, whether a template is used — is *deliberately not pinned here*: it follows the repo's own convention via [match-existing-spec-conventions](../rules/match-existing-spec-conventions.md) (mirror repo → house → maintainer).

## Its content as items

The spec's result carries that content as the pieces its documentation type declares ([spec](../../document/rules/types/spec.md)). Each piece is new under a handle, or keeps the id it carried in an earlier spec the run was handed ([items-and-agreements](../../document/rules/items-and-agreements.md)).

- **North-star clauses `NS`.** The intent's goal as the type splits it, each clause in the intent's own words, verbatim, since later briefs quote them.
- **Requirements `REQ`.** One per obligation:
  - `priority` is its rung: `must`, `should` or `could`. `obligation` is the keyword its own statement uses, how binding it is once built, never its rung, since a rung is set per release and can change while the requirement doesn't. A Won't (this time) requirement is filed `deferred` with no priority, its reason the agreement not to deliver it now and what brings it back the next release's prioritization, unless the run names another trigger, and never `agreed`. (basis: maintainer, 2026-07-04, priority is release-scoped)
  - `type` from its bucket: functional and data are `functional`, and a data requirement that limits the solution is `constraint`; non-functional is `quality` when it measures a behaviour, with a `TBR` while its number is unsettled, and `constraint` when it limits the solution; interface/contract is `interface`. A repo's own buckets map by the type file's definitions.
  - `verification`, the strongest method its criteria use, test before demonstration before analysis before inspection, else the one the requirement names; `rationale`, the "so that".
  - It `serves` the clause or the outside need it traces to, and `rests-on` each assumption it holds.
- **Acceptance criteria `AC`.** Each criterion, its examples and counter-examples in its body. Each is a pass/fail check of its own, so the result says it is verified separately and it is its own item.
- **Slices `SLC`.** Each slice, with the rung it inherits as `priority` and its spike when one is flagged, linked as the type says.
- **Assumptions `ASM`.** Each surfaced assumption, with what breaks if it is false and how it will be checked, `status` `open`.
- **Questions `Q`.** Each open question, its `reversibility`, `reach` and `tier` set by the [decision register](../../document/rules/types/decision-register.md)'s tests from what its answer would settle. A requirement's `TBR` names the question by its handle. On the base path, a requirement still below the testability bar is `blocked-by` a question naming what it lacks.

Every piece is `proposed`, with two exceptions: a question is `open`, or `lean` when the run leans, and a Won't requirement is `deferred`. A piece the run carries an agreement on takes that agreement. Criteria and requirements the intent states, such as a ticket's acceptance criteria, stay `proposed`: the spec restates them, and only an agreement on the spec settles them.

- **Owner.** Of every clause, requirement, criterion, slice and assumption, the task's owner when the run names one, such as the ticket's assignee, even when that is the person running the spec: it is a fact the run holds, not a default. Of a question, and its decider, the one person the run names for it. A team named instead leaves both missing and goes in the question's `consulted`.
- **Decide-by.** The date or gate the run gives, else left missing for documenting it to fill with the type's due point.

## Before it goes out, read it as its reader

Put the finished spec through [deliver-at-the-readers-register](../../../craft/writing/deliver-at-the-readers-register.md) before delivering it, applying its honesty floor item by item from the rule, not from memory. This deliverable sits on the **reference** side of that rule's fork; classify it there rather than taking the guidance default. What it binds is wording and how much detail each part carries — **not** the document's section order or which sections exist, which stay with the repo's own convention ([match-existing-spec-conventions](../rules/match-existing-spec-conventions.md)).

**And a visual where prose would carry it worse:** a state set, the logical data model and the slices' dependencies are relations; show it rather than describe it, per `output.diagrams` ([report-style-settings](../../../craft/writing/report-style-settings.md)) and [when-a-visual-is-owed](../../../craft/writing/when-a-visual-is-owed.md), which decides whether one is owed, drawn from the requirements, never from an implementation. `(basis: maintainer, 2026-10-07)`


