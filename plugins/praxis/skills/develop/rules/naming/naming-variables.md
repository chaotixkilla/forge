# Naming variables

The moment this rule governs is choosing what to call a value you're binding — a local, a field, a parameter. The failure when it's left to taste is quiet: one builder writes `t` for a timeout and `d` for a payload, another writes `elapsedTimeoutInMillisecondsSinceStart` for a three-line local; a third writes `price` for a value the rest of the system carries in cents. At every later read someone has to reconstruct what's in the box — or worse, guesses the unit and is wrong.

## The discriminator

A variable holds a thing, so its name is a **noun or noun-phrase that answers "what is in here?" at every point it's read** — not how it's computed, not what loop it lives in. Judge a candidate name on three axes:

- **Does it name the contents?** A variable is a box; the name is the label on the box. `remainingRetries`, `activeUser`, `parsedConfig` say what's inside. `data`, `tmp`, `result`, `val` say only "a box exists" — the reader must open it to know. Prefer the noun that a reader could predict the type and role from.
- **Is the length scaled to the scope?** Scope sets the budget. A loop index that lives three lines and never escapes is fine as `i` — the whole context is on screen. A value that crosses functions, lives on a type, or persists across a long body earns a name that survives the distance from its definition. The two errors are symmetric: a wide-lived value with a terse cryptic name is as wrong as a one-line throwaway dressed in ceremony.
- **Are units or domain encoded where ambiguity bites?** When the bare noun leaves a reader able to guess wrong about unit, scale, or representation, fold the disambiguator into the name: `timeoutMs` not `timeout`, `priceCents` not `price`, `widthPx`, `ratioPct`. Do this exactly where a wrong guess would be acted on silently — not as blanket ceremony on every name.

(basis: McConnell, *Code Complete* 2nd ed. ch. 11 — name a variable for the entity it represents; scale name length to scope (short names for short-lived locals, fuller names for wider scope); encode units and qualifiers in the name where the type alone doesn't carry them.)

## The anchors

- *Good:* `retryDelayMs` at the point it's passed to a sleep tells you it's a duration and its unit; `i` as the index of a tight loop over an array needs nothing more; `pendingOrders` reads as a collection of a known domain thing.
- *Bad:* `timeout = 30` — thirty what? a reader has to chase the sleep call to learn the unit ([avoid-misleading-names](avoid-misleading-names.md) if the surrounding code is seconds and this is millis); `data2` for a wide-scope value threaded through five functions — the label says nothing, so every read is a lookup ([name-for-the-reader](name-for-the-reader.md)).
