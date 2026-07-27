# Model with the type system

When you shape a record or the fields of an object, the moment this rule governs is whether to let a combination of fields be *representable-but-invalid* and guard it at runtime, or to shape the type so the invalid combination cannot be constructed at all. The default failure is the first: three loose fields — a `loading` flag, a `data` that may be null, an `error` that may be set — where the valid states are a fraction of the combinations the type permits, and every reader must remember which combinations are real. Two builders diverge on where the guard lives — one asserts at construction, another checks at each use, a third trusts and crashes.

## The discriminator

The test, applied when a type has more than one field whose combinations aren't all valid: **can the invalid combination be constructed?** If yes, and the language offers a shape that forbids it, use that shape instead of validating the combination everywhere at runtime:

- **When a set of fields is really "one of N mutually-exclusive cases," model it as a sum type / discriminated union, not as N optional fields.** The `loading | loaded(data) | failed(error)` example collapses to one tag with the right payload per case — `data` exists only in `loaded`, `error` only in `failed` — so "loaded but data is null" or "loading and errored at once" cannot be written. The reader reads three states, not eight combinations of which five are nonsense.
- **When a field must always be present, make it non-nullable; when a value has a constrained form, give it a type only a valid value inhabits.** Move the error from "runtime check that could be forgotten" to "compile-time or construction-time fact that can't be." A value that exists proves its own validity ([parse-dont-validate](parse-dont-validate.md)); absence gets a first-class type rather than a sentinel ([null-and-empty-handling](null-and-empty-handling.md)).
- **Where the language can't express the constraint, concentrate it in one constructor / factory and let the rest of the code hold the constructed type.** A single guarded gate beats a check scattered across every use site — the same move as defining the bad state out of existence downstream ([define-errors-out-of-existence](../errors/define-errors-out-of-existence.md)).

(basis: Yaron Minsky, "Effective ML" / *Real World OCaml* — "make illegal states unrepresentable": encode invariants in types so the compiler rejects the invalid combination rather than deferring it to a runtime check. Complements Ousterhout's define-errors-out-of-existence — the strongest form of eliminating an error case is a type in which it cannot occur.)

## The anchors

- *Good:* a request result is a union of `success(payload)` and `failure(reason)`; a caller must handle both to touch either, and there is no reachable state with both a payload and a reason, or neither.
- *Bad:* the result is a struct with a nullable `payload`, a nullable `error`, and an `ok` boolean; every reader re-checks `if ok && payload != null`, one reader forgets, and a "successful" result with a null payload flows downstream because the type never forbade it.
