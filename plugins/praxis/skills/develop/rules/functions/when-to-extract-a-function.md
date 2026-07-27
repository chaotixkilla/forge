# When to extract a function

Mid-way through writing a block, the question arises: should this stretch of code become its own function, or stay inline? Pull too eagerly and the logic shatters into a dozen one-line functions you must reassemble in your head to read; pull too rarely and a single function grows into a slab that does five things. Left to taste, one builder extracts by a line-count rule of thumb and another by feel, and the same block lands inline in one codebase and as a named helper in the next.

## The discriminator

Extract when the block has **a nameable sub-responsibility** — a coherent *what* you can give an honest, intent-revealing name to. The name is the test: if a short verb phrase captures exactly what the block does (`normalizeAddress`, `isEligibleForRefund`), that name *is* the function, and the extraction makes the caller read as intent instead of mechanism. If no honest name fits the block short of restating its every line, it has no single responsibility to extract yet.

- **Extract to separate levels of abstraction** — when a low-level detail is cluttering a run of high-level steps, lifting it into a named call restores one altitude to the caller ([one-level-of-abstraction-per-function](one-level-of-abstraction-per-function.md)).
- **Extract to kill a "what" comment** — if a block needs a comment explaining *what* it does, that comment is usually the function's name waiting to happen; extract and let the name carry it.
- **Not by line count.** Length is not the trigger. A twelve-line block that does one nameable thing stays; a four-line block that does two unrelated things should split. Extracting purely to hit a size target manufactures shallow functions whose interface costs more to read than the body they hide.

(basis: Fowler, *Refactoring* — "Extract Function": extract by intent, and let the resulting name state the *what* while the body holds the *how*; Ousterhout, *A Philosophy of Software Design* — warns against shallow methods created only to satisfy a length target, where the interface earns less than it costs. Intent, not size, is the trigger.)

## The anchors

- *Good:* a 30-line request handler where a run of lines assembles and signs an auth token becomes `buildSignedToken(claims)` — the handler now reads as a sequence of named intents, and the token mechanics live in one honestly-named place.
- *Bad:* splitting `applyDiscount` into `getRate`, `multiply`, and `roundResult` — three shallow functions for one arithmetic thought, each called exactly once, so a reader must chase three definitions to reconstruct a line of math that read fine inline.

Once an extracted helper starts serving more than one caller or hiding a real seam, it stops being a mere extraction and becomes an abstraction whose altitude must be judged ([right-altitude-abstraction](../abstraction/right-altitude-abstraction.md)).
