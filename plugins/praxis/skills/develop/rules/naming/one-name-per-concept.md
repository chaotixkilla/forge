# One name per concept

The moment this rule governs is reaching for a word for something the codebase has already named — or reusing a word you've already spent on something else. The failure when it's left to taste: one builder calls it `fetchUser`, another `getUser`, a third `loadUser`, a fourth `retrieveUser`, all for the identical operation; or one word, `handler`, comes to mean three unrelated things. A reader can no longer tell whether two names mean one thing or one name means two, and has to carry a running translation table. This rule pins the discriminator so two builders converge on one word per meaning.

## The discriminator

Hold a strict bijection between words and concepts: **one concept gets exactly one word, and one word denotes exactly one concept**, across the change and the codebase it sits in. The test, applied whenever you pick a name:

- **Does this concept already have a word here?** If the operation, role, or entity is already named somewhere the reader will meet it, reuse that word — don't mint a synonym. Four verbs (`fetch`/`get`/`load`/`retrieve`) for one operation force the reader to prove they're the same thing every time; collapse to the one the codebase already uses ([match-surrounding-conventions](../change-hygiene/match-surrounding-conventions.md) — the codebase already picked the word).
- **Is this word already spent on another concept?** If the word you're reaching for already means something else nearby, picking it for a second meaning is the mirror failure — now the reader must disambiguate by context on every read. Pick a distinct word for the distinct concept.
- **The tell is the translation table.** If a reader would need to hold "X and Y are the same" or "this Z is not that Z" in their head to read the code, the vocabulary has drifted — one word per concept removes the table.

(basis: Ousterhout, *A Philosophy of Software Design* Ch. 14 §14.4 "Use names consistently" — a given name should always refer to the same thing, so a reader who has seen it elsewhere can reuse that knowledge without re-deriving it; the consistent-vocabulary principle, convergent with *Clean Code* on this uncontested point.)

## The anchors

- *Good:* the codebase uses `fetch*` for every network read, so your new network read is `fetchInvoice` — a reader who knows one `fetch` knows yours without checking; `user` means the authenticated principal everywhere, never also a DB row.
- *Bad:* a module with `getConfig`, `loadSettings`, and `readOptions` that all return the same config object — the reader has to open all three to learn they're synonyms; or `context` meaning the request context in one function and a rendering context two functions down, silently ([avoid-misleading-names](avoid-misleading-names.md)).
