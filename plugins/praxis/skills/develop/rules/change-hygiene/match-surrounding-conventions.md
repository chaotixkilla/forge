# Match surrounding conventions

Every file already has a dialect — how it names things, how it structures a module, how it handles errors, how it lays out whitespace. The judgment this rule governs is whose style wins when you add code: yours, or the file's. Left to taste it goes wrong quietly — a builder writes in their personal idiom, technically fine in isolation, and the module now reads in two voices, so the next maintainer can't tell house style from local exception and burns attention reconciling them on every read. Two builders with different personal styles produce a file that fights itself.

## The discriminator

The standard is **the neighborhood, not your preference**: for naming, structure, error handling, and formatting, infer the local idiom of the file/module you're in and match it — even where you'd personally choose otherwise. The test at each decision:

- **Is there a strong local convention for this?** Read what the surrounding code already does — the casing and vocabulary of its names ([name-for-the-reader](../naming/name-for-the-reader.md)), the get/fetch/load distinctions it draws, how it returns errors, how it orders a module. If a clear pattern exists, follow it. A change that breaks a strong local convention is a **real cost** — inconsistency the next maintainer pays — even when your alternative is defensible in the abstract; "mine is arguably better" does not clear the bar against an established house style.
- **One concept, one name — the file's name.** When the surrounding code already has a word for the thing, use that word rather than introducing a synonym ([one-name-per-concept](../naming/one-name-per-concept.md)); a second name for an existing concept is the most common convention break.
- **The exception:** you do *not* preserve a local pattern that is an actual bug, or one the project is **provably migrating away from** (a documented deprecation, a migration in visible progress). Match where the code is going, not a pattern being actively retired. Absent that proof, the incumbent convention wins.

(basis: Feathers, *Working Effectively with Legacy Code* — respect the surrounding style; the "be a good citizen of this codebase" principle: code you add should be indistinguishable from the code already there. Mirrors review's judge-against-the-surrounding-code stance — a change is measured against its neighbors, not an abstract ideal.)

## The anchors

- *Good:* the module returns errors as result values throughout, so your new function returns a result value too — even though you'd personally have thrown. The file reads as one hand wrote it.
- *Bad:* the surrounding code uses `fetchX`/`loadX` consistently and you add `getData` in a different casing that also throws where its siblings return — three convention breaks in one name, each a small tax the next reader pays, none of them the task's job.
