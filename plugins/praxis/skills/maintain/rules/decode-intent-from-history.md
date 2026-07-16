# Decode intent from history

Living code accumulates decisions, and the ones that look most removable are often the ones that were added *on purpose* — the redundant-looking guard that handles a production incident, the magic constant that matches an external system's limit, the awkward branch that exists because a "cleaner" version broke something two years ago. This is Chesterton's fence: *don't remove a fence until you know why it was put there.* The failure this rule prevents is the confident cleanup that silently reintroduces a fixed bug, and it's a failure precisely because the code looked wrong and the maintainer was sure.

## The discriminator: when you must recover intent first

You do not need to archaeology every line you touch — that would make maintenance impossible. Recover intent *before* changing code when **either** trigger fires:

- **The code has no self-evident purpose from the code alone.** It reads as dead, redundant, or arbitrary: an unreferenced-looking branch, a guard that seems to duplicate one above it, a constant with no derivation, a workaround with no comment. "I can't see why this is here" is the trigger — the whole point is that the reason isn't in front of you.
- **The code is load-bearing.** It sits in a contract, an error/recovery path, a concurrency guard, a security check, or anything the [blast-radius map](../phases/02-understand-blast-radius.md) marked as reaching past this diff. Here the cost of being wrong is high enough that you confirm intent even when you think you understand it.

When **neither** fires — you're adding new code, or the code's purpose is self-evident and unchanged by your edit — skip the check and move on. Recovering intent for genuinely obvious code is the over-application that makes people abandon the rule entirely.

## How to recover it, and when you may proceed

Recover the *why* from the cheapest sources first: the surrounding comments, then the change history for the introducing commit and its message, then any linked work-item or discussion, then the tests that exercise the code (a test pins behavior someone cared about). Reading commit messages and change authorship/annotations is an **ambient** local version-control read, done directly; a linked work-item is read via the [project-mgmt](../../project-mgmt/SKILL.md) skill; deeper cross-lane prior-art is a [gather](../../gather/SKILL.md) step in [understand-blast-radius](../phases/02-understand-blast-radius.md).

You may proceed to change the code when **one** of these is true:

- **Intent recovered and consistent.** You found why it's there, and your change preserves that intent (or deliberately supersedes it with a migration path per [preserve-the-contract](preserve-the-contract.md)).
- **Established absence of intent.** You've done the search above and found no reason — no comment, no meaningful commit, no test, no consumer — so the code is genuinely dead and removing it changes nothing observable.

The fence stays up until you can state, in one sentence, why it was built. If the search is inconclusive — signs of intent but you can't pin it — treat it as load-bearing and route the uncertainty into the [blast-radius](../phases/02-understand-blast-radius.md) grade rather than guessing.

`(basis: Chesterton's fence — the principle that a reform should not remove a thing until it understands why the thing was put there (G.K. Chesterton, *The Thing*, 1929), a standard reference in refactoring practice; the two-trigger discriminator is derived craft that bounds the check so it fires on the puzzling-or-load-bearing cases and not on self-evident edits.)`
