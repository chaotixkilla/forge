# Avoid misleading names

The moment this rule governs is catching a name that's not merely unclear but actively *wrong* about what it labels. The failure when it's left to taste: a name that lies passes review because it reads fluently — `userList` that's actually a set, `getPrice` that hits the database, `simpleLookup` that fans out three calls — and the next builder acts on the promise, indexing the "list," calling the "getter" in a tight loop, trusting the "simple" one on a hot path. A vague name costs a lookup; a lying name costs a wrong assumption acted on, and the bug lands far from the name.

## The discriminator

The test is not "is this name clear?" but **"does this name assert something false about the thing?"** A vague name (`data`, `tmp`) is a lookup tax; a *misleading* name plants a false belief the reader builds on. Reject a name that misrepresents any of:

- **Type or shape** — `list` for something that isn't ordered/indexable, `count` for a non-number, `userList` for a map. The reader will use the operations the named type implies, and they'll be wrong.
- **Mutation** — a query-shaped name (`get`, `find`, `is`) on something that writes, or a name that hides that it mutates its argument. The reader assumes it's safe to call freely or reorder ([naming-functions](naming-functions.md) — the name must reveal side effects).
- **Cost** — a name implying cheapness (`simple`, a plain accessor shape) on something that does I/O, network, or heavy compute. The reader puts it somewhere a cheap call belongs.
- **Contents / meaning** — noise words that hide what the thing actually is: `data`, `info`, `manager`, `object`, `helper`, `process`. They name the existence of a thing, not the thing, so they can quietly cover anything and mislead by vagueness that reads as specificity.

The rule: **a name that lies is worse than one that's merely vague** — fix the lie first. When in doubt, a name that under-promises beats one that over-promises.

(basis: Martin, *Clean Code* — avoid disinformation: don't use a name whose implied type, structure, or meaning is false, and drop noise words that carry no distinguishing information (the convergent, uncontested part); Ousterhout, *A Philosophy of Software Design* — a name that leads the reader to a wrong conclusion is worse than one that merely lacks information.)

## The anchors

- *Good:* `activeUserIds` is a collection of ids of active users and nothing else — type, contents, and scope all true; `fetchPriceFromApi` warns at the call site that it costs a round trip.
- *Bad:* `accountList` that's really a `Map` keyed by id — a reader writes `accountList[0]` expecting the first account and gets undefined ([name-for-the-reader](name-for-the-reader.md)); `getBalance()` that silently issues a network call, so it lands inside a render loop and melts the service — the name promised a field read, not I/O.
