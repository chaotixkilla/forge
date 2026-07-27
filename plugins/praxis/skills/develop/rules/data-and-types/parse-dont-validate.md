# Parse, don't validate

When untrusted or unstructured input enters — a request body, a config file, a string from an external system — the moment this rule governs is how you establish that it's well-formed. The reflex is to *validate*: run a check that returns true/false, then carry the same raw shape onward. The failure is that the raw shape still looks unchecked to everything downstream, so every site either re-validates (duplicated, drift-prone) or trusts blindly (a crash waiting for the one input that skipped the check). Two builders put their checks in different places and the interior can't tell validated data from raw.

## The discriminator

The test on any input check: **does it return a boolean and leave the data in its raw shape, or does it return a *new type* that can only exist if the input was valid?** Prefer the second — parse, don't validate:

- **Validation throws away what it learned.** A function that returns `bool` verifies the input then discards the evidence; the caller holds the same untyped string or loose map it had before, and the knowledge "this is valid" lives nowhere the type system can enforce. Every downstream function must re-check or assume — and assumptions rot.
- **Parsing preserves the proof in the type.** A function that takes the raw input and returns a richer type — `EmailAddress`, `NonEmptyList`, a fully-typed record — performs the check *once*, at the boundary, and hands back a value whose very existence means it passed. Downstream code accepts that type and cannot receive an unvalidated one; the check can't be forgotten because the type won't let the raw shape through ([model-with-the-type-system](model-with-the-type-system.md)).
- **Do it once, at the trust boundary, and let the interior carry the guarantee.** Parsing is where validation ([validate-at-the-trust-boundary](../errors/validate-at-the-trust-boundary.md)) and error handling ([handle-errors-at-the-boundary](../errors/handle-errors-at-the-boundary.md)) belong: reject the malformed input at the edge with a clear failure, and past that edge every function trusts its types instead of re-checking.

(basis: Alexis King, "Parse, don't validate" — a validation returning a boolean discards the evidence of its own success, forcing redundant checks or unsafe assumptions downstream, whereas parsing into a more precise type performs the check once and encodes the result so the invalid state is unrepresentable past the boundary; the boundary-parsing / make-illegal-states-unrepresentable lineage.)

## The anchors

- *Good:* an API edge parses the incoming body into a typed `CreateOrderRequest` — required fields present, quantities positive, currency known — or rejects it with a specific error; every function behind the edge takes `CreateOrderRequest` and never re-checks a field, because an instance can't exist unless it was valid.
- *Bad:* the edge calls `isValidOrder(body)` returning a boolean, then passes the raw map onward; three services deep, a function re-runs its own partial check, a fourth trusts blindly, and a body that slipped past one gap surfaces as a crash far from the boundary that should have owned it.
