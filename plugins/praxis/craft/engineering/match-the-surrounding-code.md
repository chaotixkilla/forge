# Match the surrounding code

Every codebase already has a dialect — how it names things, bounds its modules, handles errors, structures control flow, lays out its tests — and the judgment this standard governs is whose style wins when you add to it, design for it or judge a change in it: yours, or the code's. Left to taste it goes wrong quietly. Code written in a personal idiom is technically fine in isolation, and the module now reads in two voices, so the next maintainer can't tell house style from local exception and pays to reconcile them on every read. A design measured against an ideal architecture in its author's head imports a foreign layering or an abstraction the project deliberately avoids. A review measured against the reviewer's picture of good code flags a pattern the whole module uses. Even where the imported way is better in the abstract, a codebase with two ways of doing the same thing costs the next maintainer more than either way alone: the change should read as though whoever wrote the module wrote it.

## The standard is the neighborhood

Read the local norm before you write, design or judge: the casing and vocabulary of its names and the get/fetch/load distinctions it draws, how modules are bounded, how errors propagate, what abstractions it reaches for, how much indirection it tolerates, its sync-versus-async idiom, and, for tests, the framework, naming, fixture style, assertion idiom and directory layout already in use. A convention you guessed at is one you'll violate.

The discriminator: **does this diverge from a pattern the surrounding code actually establishes?** If the code does it one way and the change or design does it another, the divergence needs a reason — and in a review, the divergence is the finding. If the code is silent on the question, it's open: choose, and in a review it's taste, not a finding.

- **The nearest consistent pattern governs:** the file first, then the module, then the package. When the file is itself inconsistent — two error-handling styles already present — match the one that dominates the module around it, and don't add a third.
- **One concept, one name — the code's name.** When the surrounding code already has a word for the thing, use it rather than introducing a synonym ([one-name-per-concept](one-name-per-concept.md)); a second name for an existing concept is the commonest convention break.
- **Where genuinely no convention exists** (a greenfield surface), fall back to the language's mainstream idiom and say so. The moment prior art exists in the repository, prior art wins.

## Where the local pattern stops winning

Matching the surroundings is a style-and-structure standard, not a correctness one. It stops at these edges:

- **A local pattern that is a bug** is not a convention to preserve. If the whole module dereferences without a null check, the shared pattern is a shared bug: don't propagate it. Write or design the correct thing and note the divergence; in a review, flag it at the change's site with the pattern named. It's a [cause to fix](../evidence/fix-the-cause-not-the-symptom.md), not a style to mirror.
- **A pattern the project is provably migrating away from** — a documented deprecation, a migration in visible progress, a direction stated in recent changes — is not the standard: match where the code is going, and say so. Absent that evidence, the incumbent convention wins; never infer a migration from your own taste.
- **A security or contract requirement** overrides local style: you don't match a convention of interpolating input into queries because the file does it ([distrust-untyped-input-and-secrets](distrust-untyped-input-and-secrets.md), [preserve-the-contract](preserve-the-contract.md)).
- **A pattern you're deliberately improving** is a [campsite-cleaner](leave-the-campsite-cleaner.md) call — allowed within that standard's bound, and then improved *consistently* within the touched scope, not halfway.
- **Comment density is not a convention.** A file thick with comments that restate their own lines is not a house style to honor; it's the rot [comment-the-why-not-the-what](comment-the-why-not-the-what.md) exists to stop, and reproducing it because the neighbors do multiplies it under cover of good citizenship, since nothing ever forces an empty comment to be corrected. Decide every comment by the why-not-the-what test at whatever the local density, and the carve-out cuts **both** ways: a heavily-commented file doesn't license narration, and a comment-free one doesn't forbid the single comment that carries a genuinely non-obvious *why*. A project that wants local density followed says so explicitly in its settings (praxis's `output.comments`), and that is the one thing that overrides this. `(basis: maintainer, 2026-09-01)`

Outside those edges, the local pattern wins even when your own taste disagrees.

## The fork: conform, or import a better foreign pattern

When a strong local convention exists and a foreign pattern would genuinely be better, there are two defensible positions — encode the fork, don't pretend there's one answer:

- **Conform to the local convention.** Cost: you forgo the better pattern. Benefit: one consistent way, no split-brain codebase, an idiom every future maintainer already knows.
- **Import the better pattern.** Cost: the inconsistency the next maintainer pays, a two-standard codebase, and the pressure to migrate the rest. Benefit: the better pattern, where the improvement is worth the seam it opens.

**Routing:** the surrounding convention wins by default → a declared house rule overrides it → the maintainer settles a genuine tie. Importing is justified only when the improvement is large *and* you name how the inconsistency it opens will be resolved — a migration direction — never on preference alone. A foreign pattern is a moving part like any other, and must earn the inconsistency it costs ([justify-every-moving-part](justify-every-moving-part.md)).

(basis: Feathers, *Working Effectively with Legacy Code*)

## Anchors

- *Good:* the module returns errors as result values throughout, so your new function returns a result value too, even though you'd personally have thrown. The file reads as one hand wrote it.
- *Bad:* the surrounding code uses `fetchX`/`loadX` consistently, and you add `getData` in a different casing that also throws where its siblings return — three convention breaks in one name, each a small tax the next reader pays, none of them the task's job.
