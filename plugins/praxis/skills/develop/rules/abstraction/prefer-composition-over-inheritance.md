# Prefer composition over inheritance

The moment this rule governs is the one where you want to reuse or extend existing behavior and reach for a base class — subclassing to inherit the methods you need. Inheritance couples the subtype to the base's internals for the life of the hierarchy: a change to the base ripples into every descendant, and a subclass that overrides selectively can leave the object in a state the base never anticipated. Left to taste, one builder subclasses to grab three handy methods while another holds an instance as a field, and the codebase grows two different reuse idioms — one of them a hierarchy that models nothing real. This rule pins the discriminator so two builders converge on when inheritance is warranted.

## The discriminator

Reach for **composition by default**; use **inheritance only for a true is-a with a shared, stable contract.** The test:

- **Does the subtype genuinely substitute for the base?** Inheritance is right only when an instance of the subtype can stand in anywhere the base is expected without breaking the caller's expectations — the Liskov Substitution Principle holds: no strengthened preconditions, no weakened postconditions, no surprises. If substitutability holds *and* the types share a real behavioral contract, the is-a is genuine.
- **Are you subclassing only to reuse code?** If the pull is "the base already has the method I want," that is a *has-a* or *uses-a* relationship wearing an is-a costume — hold the collaborator as a field and delegate to it. Reuse is not a reason to inherit; shared behavior is delivered by composition without welding the lifecycles together.
- **Does the hierarchy model the domain, or just the implementation?** A tree that mirrors real subtype relationships in the problem earns inheritance; one that exists to share a helper or to avoid retyping fields is an implementation shortcut that will fight every future change.

(basis: Gang of Four, *Design Patterns* — "favor object composition over class inheritance," because inheritance exposes a subclass to its parent's implementation and composition keeps each class encapsulated and swappable. The Liskov Substitution Principle (Barbara Liskov) is the is-a test: a subtype must be substitutable for its base type.)

## The fork: composition-shaped vs inheritance-shaped codebases

Whether a codebase leans on inheritance is partly a contested convention, not a pure correctness call — encode it, don't crown a winner:

- **Composition-first.** Wire behavior from small collaborators; keep hierarchies shallow or absent. Cost: more explicit wiring and delegation boilerplate; a very natural is-a can feel over-engineered when forced through composition.
- **Framework/inheritance-shaped.** Some frameworks and established codebases *are* built around extending base classes — the idiomatic extension point is a subclass. Cost: deeper coupling to base internals, and fragility when the base evolves.

**Routing rule (non-gating): surrounding convention → house rule → maintainer.** If the module (or its framework) has an established extension idiom, match it ([match-surrounding-conventions](../change-hygiene/match-surrounding-conventions.md)) — a lone composition-purist seam in an inheritance-shaped framework is its own kind of debris. Absent a signal, default to composition per the GoF guidance above. (basis: authority-conflict fork — GoF's composition preference vs. framework-idiomatic inheritance; both are legitimate, so the local convention decides, not this rule.)

## The anchors

- *Composition (good):* a report needs formatting and delivery, so it *holds* a formatter and a sender as fields and delegates — either can be swapped without touching the report, and no lifecycle is welded to another.
- *Inheritance misused (reject):* a `PaymentJob` extends `HttpClient` so it can call `.post()` without holding one — it is not a kind of HTTP client, it *uses* one. The is-a is false; a caller handed a `PaymentJob` where an `HttpClient` was expected gets nonsense. Hold the client as a field instead. Keep inheritance for the genuine is-a where substitution actually holds ([right-altitude-abstraction](right-altitude-abstraction.md) — reach up the ladder only when the rung below can't carry the load).
