A concrete spec is still a wall of requirements until it is carved into pieces that ship. This phase does the carving: it breaks the spec into independently shippable slices, sizes each so it is neither too big to ship nor too small to matter, prioritizes them so time pressure cuts the right scope, and orders them by dependency and risk. Its two graded outputs — a **priority** on every requirement and a **size verdict** on every slice — are load-bearing decisions, so each rates against a defined scale, not an invented one: without the scales, two specifiers rank and cut the same spec differently, which is the exact divergence a spec exists to prevent.

## Break into independently shippable slices

Find the thin vertical slice that delivers value on its own, then layer. A slice cuts **vertically** — through every layer needed to produce user-observable value — rather than horizontally (a "data layer" slice that is useless until three later slices land is not a slice, it is a task). The unit is the increment a team can ship and demonstrate by itself; sizing (below) is how you judge whether a candidate slice is that unit.

## The sizing scale

A slice is well-sized when it clears three properties, grounded in the INVEST criteria for a good increment:

- **Independently shippable** — delivers user-observable value on its own, cutting vertically through all layers (INVEST: *valuable / vertical*).
- **Independently verifiable** — its acceptance criteria can be checked without the rest of the spec built (INVEST: *testable*).
- **Fits one delivery cadence** — completable within the team's iteration unit (INVEST: *small — fits within an iteration*).

`(basis: the vertical-slice and independent-verifiability discriminators are pinned from INVEST (Bill Wake, 2003; corroborated by the Agile Alliance glossary tying "valuable" to vertical and "small" to fitting an iteration). The concrete cadence bound — one sprint, ≤ N days, ≤ N acceptance criteria — is ratified by the maintainer, 2026-07-04, to stay parameterized to team cadence rather than pinned to a fixed number: no universal number exists, and the qualitative bar plus the no-cadence degrade below carry the verdict without one.)`

Absent a known team cadence at runtime, do not stall or invent a number: size by the qualitative bar alone — one vertical increment, independently shippable and verifiable — and flag the missing cadence as an assumption to confirm ([make-the-unsaid-explicit](../rules/make-the-unsaid-explicit.md)). The cadence bound only sharpens the split call at the margin; the value-seam and independent-verifiability discriminators carry the verdict without it.

The three-state verdict, assigned by walking the properties:

- **right-sized** — one value increment; independently shippable and verifiable; fits one cadence.
  - *Anchor:* "an owner grants read access to a document and the grantee can open it" — ships and demos on its own, verifiable alone, one iteration.
- **too-big — split it** — fails any one of: cannot be completed in one cadence, **or** bundles more than one independently-releasable increment, **or** its criteria cannot all be verified together. Split along the *value* seam into vertical sub-slices, never into horizontal layers.
  - *Anchor (top of scale):* "all of sharing" — grant, revoke, notify, audit, and external recipients bundled; many increments across many cadences. Split.
- **too-small — merge it** — delivers no independently-observable value (a pure sub-task of another slice) **or** cannot be verified until another slice is built first. Merge into the slice whose value it completes.
  - *Anchor (bottom of scale):* "add the `permission_level` column" — no user-observable value alone, verifiable only once the grant flow exists. Merge into the grant slice.

Adjacent-state discriminators: **right-sized vs too-big** — can it ship *and* be verified as one increment within one cadence? All three → right-sized; fails any → too-big. **right-sized vs too-small** — does it deliver observable value on its own? Yes → right-sized; no (a pure sub-task) → too-small.

## The priority scale (MoSCoW)

Every requirement carries a priority, because when time runs short the priority is what tells everyone what gets cut — an unprioritized spec gets cut arbitrarily under pressure, and the wrong things go.

`(basis: ratified by the maintainer, 2026-07-04. MoSCoW is the house priority default — named in the praxis spec design and defined by the DSDM standard (Agile Business Consortium). The four rungs' definitions and assignment tests are DSDM's; the anchors and the inflation guard are the maintainer's ratified house standard, since MoSCoW has no single external authority for exact rung boundaries the way CVSS has for severity. Alternatives — numeric 1–5, Kano — answer different questions (fineness, satisfaction-modeling) and were set aside for this cut-order use.)`

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

Adjacent-rung discriminators: **Must vs Should** — the *workaround test*: if any viable workaround exists (even a painful, manual one), it is not a Must — demote to Should; a Must has no workaround. **Should vs Could** — the *degree of pain* if unmet, measured in business value or people affected; both leave the solution viable, so they are separated by magnitude, not kind. **Could vs Won't** — is it in this cycle at all? A candidate you would do if time allowed → Could; one you have agreed not to do now → Won't.

*Inflation guard:* if more than roughly half the requirements land on Must, the ladder has collapsed — re-apply the workaround test to each, and any Must with a viable workaround becomes a Should. `(basis: DSDM's guideline of ≤ 60% Must-have effort, transferred here as a smell test against Must-inflation; the exact percentage presumes a timeboxed delivery, so treat a Must-heavy spec as a signal to recheck, not a hard cap.)`

The rungs are assigned to requirements; a **slice inherits the highest priority among the requirements it delivers** — a slice carrying any Must is a Must slice, even when a lower-priority requirement was merged into it (a too-small requirement folds into the slice whose value it completes). `(basis: the inherit-the-highest rule is total — every slice delivers at least one value-bearing requirement, and taking the maximum rung resolves the mixed-priority case a merge can create, so no slice is ever left without a defined priority.)` This is what lets the dependency check below reason about a "Must slice" from a scale defined on requirements.

## Flag dependencies and risks

Two final passes over the sized, prioritized slices. **Dependencies:** what must exist before a slice can be built — the order follows the dependency graph, thin vertical slice first, then the layers that build on it. Slices with **no** dependency between them carry no imposed order — being independently shippable is their definition, so their relative sequence is *deliberately left open* (pinning it would be false precision, and priority is the cut axis here, not a sequencing one). A Must slice that depends on a Could slice is a contradiction to resolve, not a sequence to ship — resolve it by re-running the workaround test (above) on the depended-on requirement: a genuine build-dependency of a Must has no workaround, so it is itself a Must and gets promoted, or the two slices merge along the value seam. Never ship the Must ahead of what it needs. **Risks:** what is uncertain enough to threaten the estimate or the approach — an unknown that could invalidate a slice — is flagged for a spike (a time-boxed investigation) *before* the slice is committed, rather than discovered mid-build.

## The assembled spec

The finished spec is the assembly of what the phases produced, and its *content* is fixed even though its *layout* is not. It carries: the requirements in their taxonomy buckets ([requirement-structuring](03-requirement-structuring.md)), each with its acceptance criteria (and the examples and counter-examples that pin them), its priority rung, and its trace to a need ([trace-each-requirement-to-a-need](../rules/trace-each-requirement-to-a-need.md)); the sized, prioritized slices ordered by dependency, with risks flagged for spikes; the surfaced assumptions, open questions, and explicit out-of-scope list ([make-the-unsaid-explicit](../rules/make-the-unsaid-explicit.md)); and, on the base (non-strict) path, any testability warnings on requirements still below the bar ([testable-or-its-not-a-requirement](../rules/testable-or-its-not-a-requirement.md)). That content is the deliverable in every run — the interrogation machinery that produced it is not part of it. The concrete document layout — section order, headings, whether a template is used — is *deliberately not pinned here*: it follows the repo's own convention via [match-existing-spec-conventions](../rules/match-existing-spec-conventions.md) (mirror repo → house → maintainer), because a spec that imports a foreign template gets reformatted or ignored.

When `--publish` is set, hand this finished spec to the artifacts capability as a clean, team-facing document ([publish-spec](../modules/publish-spec.md)).
