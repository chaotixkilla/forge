# Match the existing conventions

A design's job is to be a good citizen of *this* system, not an exemplar of the designer's preferred one. The trap is measuring the design against an ideal architecture in the designer's head instead of the codebase it must live in — importing a foreign layering, a naming style, or an abstraction the project deliberately avoids. Even when the imported pattern is better in the abstract, a system with two ways of doing the same thing costs the next maintainer more than either way alone. This rule anchors the design to the patterns already present.

## The standard is the neighborhood

Before committing to a structure, read the local norm: how modules are bounded, how errors propagate, what abstractions the codebase reaches for, how much indirection it tolerates, its sync-vs-async idiom. Then design against *that*. The discriminator: **does the design diverge from a pattern the surrounding code actually establishes?** If the codebase does it this way and the design doesn't, that divergence needs a reason; if the codebase is simply silent on the question, it is open and you choose.

## The fork: conform vs import a superior foreign pattern

When a strong local convention exists but a foreign pattern would genuinely be better, there are two defensible positions — encode the fork, don't pretend there is one answer:

- **Conform to the local convention.** Cost: you forgo the better pattern. Benefit: one consistent way; no split-brain codebase; every future maintainer already knows the idiom.
- **Import the superior pattern.** Cost: inconsistency the next maintainer pays, a two-standard codebase, and the pressure to migrate the rest. Benefit: the better pattern, where the improvement is worth the seam it opens.

**Routing:** the surrounding convention wins by default → a declared house rule overrides it → the maintainer settles a genuine tie. Importing is justified only when the improvement is large *and* you name how the resulting inconsistency will be resolved (a migration direction), not on preference alone.

## Two overrides on "conform by default"

- **A convention that is itself a correctness bug is never excused by consistency.** If the local pattern is wrong (a shared missing guard, an unsafe idiom), don't propagate it — design the correct thing and note the divergence.
- **A convention the project is actively migrating away from** — with clear evidence (recent changes, a stated direction) — is not the standard to match; design to the *new* direction and say so. Absent that evidence, the existing convention wins; do not infer a migration from your own taste.

Cited by [mapping-to-system](../phases/01-mapping-to-system.md), [choosing-approach](../phases/02-choosing-approach.md), and [specify-interfaces](../phases/03-specify-interfaces.md). Related: [justify-every-moving-part](justify-every-moving-part.md) (a foreign pattern is a moving part that must earn the inconsistency it costs).
