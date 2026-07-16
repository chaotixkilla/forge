# Separate problem from solution

spec's job stops at *what must be true*; choosing *how to make it true* is the next skill's (plan's). The failure this rule prevents is the spec that quietly decides the design: it says "add a Redis cache" when the requirement was "product pages load in under 300 ms," or "use a state machine" when the requirement was "an order can't ship before it's paid." A solution smuggled in as a requirement does two kinds of damage — it pre-empts the design phase's freedom to find a better mechanism, and it hides the *actual* requirement behind a chosen one, so no one can tell whether a different design would also satisfy the need. This rule pins the seam between spec and plan so two specifiers keep the same statements on the spec side of it.

## The discriminator: outcome, or mechanism?

The one test: **could two genuinely different designs both satisfy this statement?**

- **Yes → it's a requirement.** It constrains the *outcome* — what must be observably true when the work is done — and leaves the mechanism open. "Search returns matches in under 200 ms." "A deleted account's data is unrecoverable after 30 days." Many designs could meet each; the statement judges the result, not the route. Keep it in the spec.
- **No — it names the one design → it's a solution.** It fixes a *mechanism*, and a mechanism is plan's to choose. "Use an inverted index." "Run a nightly purge job." Defer it; the spec should state the outcome that mechanism was meant to achieve, and let plan pick the mechanism.

The WHAT/HOW line drawn concretely: for "add sharing," spec resolves the **what-ambiguity** — who can share, what can be shared, which permission levels exist, whether access is revocable, what a revoked user sees. spec does **not** resolve the **how-decision** — whether sharing is implemented with ACLs, capability tokens, or per-resource grants. The first set is requirements (outcomes, each testable); the second is design (mechanisms, plan's call).

## The boundary case: a constraint that names a mechanism

Some statements name a mechanism and are still requirements — because the mechanism is *imposed*, not chosen. "Data must remain in the EU region" (regulatory), "must authenticate through the existing corporate SSO" (environmental) both constrain the outcome even though they sound like design. The discriminator holds: could two different designs satisfy it? For a real constraint, no design may violate it, but many designs can *honor* it — so it constrains outcome and belongs in the spec, recorded as a constraint ([name-capabilities-not-tools](name-capabilities-not-tools.md) governs how to phrase it). The tell that separates a constraint from a smuggled solution: a constraint says what the design may **not** do; a smuggled solution says what the design **must** do at the mechanism level. Fence the space, don't pick the point.

When a statement is genuinely a solution but encodes a real requirement, don't just delete it — extract the requirement it was standing in for ("nightly purge job" → "data unrecoverable after 30 days") and hand the mechanism to plan. Throwing away the solution loses the need hiding inside it.
