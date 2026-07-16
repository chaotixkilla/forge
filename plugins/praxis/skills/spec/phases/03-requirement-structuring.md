The hardened requirements from the previous phase arrive as a flat pile; this phase gives each a home, so nothing is forgotten and the reader can find every requirement of a kind in one place. The buckets are not bureaucracy — the discipline of filling each one is what surfaces the requirements a single-list spec drops. Non-functional requirements especially: no one forgets the feature, everyone forgets the latency budget and the authorization rule until they are expensive to retrofit.

## Choose the taxonomy

The house default is four buckets — **functional, non-functional, data, interface/contract** — but the taxonomy is a genuine fork (a pure user-story/Gherkin backlog and ADR-style decision records are defensible alternatives), so pick it by the routing chain rather than by habit: mirror the repo's existing spec convention if one exists, else take the house default, else propose one and route it ([match-existing-spec-conventions](../rules/match-existing-spec-conventions.md)). `(basis: functional / non-functional / data / interface is the praxis house taxonomy — the existing spec skill's buckets, propagated across sibling skills — and aligns with ISO/IEC/IEEE 29148's requirement categories.)`

## Functional — what it does

State each functional requirement as a user story: *As a [role], I want [action] so that [benefit]*. The discriminator for the bucket: **a functional requirement names a behavior an actor can invoke and observe.** The role ties it to an actor from [interrogating-prompts](01-interrogating-prompts.md); the "so that" ties it to the need it serves ([trace-each-requirement-to-a-need](../rules/trace-each-requirement-to-a-need.md)) — a story with no defensible "so that" is an orphan to resolve, not a requirement to keep.

## Non-functional — the qualities it must have

Sweep the quality dimensions the request implies but rarely states: performance, security, accessibility, scale, availability, compliance. These are easy to forget and costly to retrofit — a system built without them baked in rarely bolts them on cleanly later. The discriminator that makes each a *requirement* rather than an aspiration: it must be quantified ([testable-or-its-not-a-requirement](../rules/testable-or-its-not-a-requirement.md)). "The system must be secure" is not an NFR; "all data at rest is encrypted, and no endpoint returns another tenant's records" is two.

## Data — the logical model

Name the entities, their fields and types, validation rules, and relationships. The discriminator that keeps this in spec and out of plan: state the **logical** model (what data exists and how it relates), never the **physical** schema (tables, indexes, storage engine) — the schema is a design decision plan owns ([separate-problem-from-solution](../rules/separate-problem-from-solution.md)). "A share links one document to one team at a permission level" is a data requirement; "a `shares` table with a composite index on (doc_id, team_id)" is design leaking into the spec.

## Interface / contract — the boundary

For a service: the endpoints — inputs, outputs, status codes, and error shapes. For a UI: the screens and their states, including the empty, error, denied, and extreme states pinned in [pin-down-ambiguity](02-pin-down-ambiguity.md), rendered rather than assumed. Name the capability the interface depends on, never the product that provides it ([name-capabilities-not-tools](../rules/name-capabilities-not-tools.md)), so the contract stays portable across tool choices.

## Ground against standing conventions and invariants

Close with spec's strongest read: delegate to the `gather` skill ([gather](../../gather/SKILL.md)) to pull the standing conventions the spec must mirror and the behavioral invariants it must not violate — perf budgets, a11y and security baselines, tenancy and data-residency rules, the vocabulary the team already uses. These are constraints the spec inherits whether or not the prompt named them, and a requirement that contradicts a standing invariant is a defect — cheapest to catch here. `gather` owns the read and its degrade; without the delegation, read what standing context you can reach inline before finalizing the buckets.

The output is the structured requirement set — every requirement in a bucket, traced to a need, portable, and consistent with the system's standing constraints — ready to be made concrete and testable in [making-it-concrete](04-making-it-concrete.md).
