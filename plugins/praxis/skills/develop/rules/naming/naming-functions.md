# Naming functions

The moment this rule governs is naming a routine you're about to define. A function *does* something, and its name is the promise the caller reads instead of the body. The failure when it's left to taste: one builder names a mutating routine `getConfig`, another names a pure lookup `updateCache`, and callers act on the promise the name made — refetch when nothing changed, or skip a save because the name hid the write. The reader trusts the name and is betrayed by the body. This rule pins the discriminator so two builders converge on a name a caller can act on.

## The discriminator

A function name is a **verb or verb-phrase stating the effect**, and the test is: **from the name alone, can a caller predict what it does, whether it changes anything, and what it returns?** Four things the name must get right:

- **State the effect with a verb.** `chargeCard`, `parseHeader`, `evictStale` say what happens. A bare noun (`data()`, `config()`) or a vague verb (`doIt`, `handle`, `process`) forces the caller into the body to learn the effect.
- **Reveal side effects — or their absence.** A name that reads as a pure query but mutates is a lie: a `getX` that writes to a cache, a `validate` that also persists. If it commands (changes state), the name should signal the command; if it queries (returns without changing observable state), it should read as a query. A caller routes control flow on this distinction.
- **Use symmetric pairs consistently.** Opposed operations take opposed names, the same pair everywhere: `open`/`close`, `get`/`set`, `add`/`remove`, `start`/`stop`. Don't pair `add` with `delete` or `open` with `dispose` — the asymmetry makes a reader wonder what the difference means.
- **Make a boolean-returning function read as a predicate.** `isReady`, `hasPending`, `canRetry` read at a branch as the yes/no question they answer; a boolean named `status` or `check` does not.

(basis: McConnell, *Code Complete* 2nd ed. ch. 7 — name a routine for what it does, describing its return value for a function and its effect for a procedure; and Meyer's command–query separation intuition — a name should signal whether a routine commands, i.e. changes state, or queries, i.e. returns a value without observable effect.)

## The anchors

- *Good:* `isExpired(token)` reads at an `if` as the question it answers and promises no mutation; `saveDraft(doc)` names its effect and its target; the pair `acquireLock`/`releaseLock` is symmetric, so a reader pattern-matches them instantly.
- *Bad:* `getUser(id)` that lazily inserts a row on miss — the caller reads a harmless lookup and ships a write ([avoid-misleading-names](avoid-misleading-names.md)); `handleData(x)` — neither effect nor return is predictable, so the name buys the caller nothing ([name-for-the-reader](name-for-the-reader.md)). A function whose honest name would need three verbs is doing three jobs — split it ([keep-functions-cohesive](../functions/keep-functions-cohesive.md)).
