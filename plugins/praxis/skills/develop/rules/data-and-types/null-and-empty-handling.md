# Null and empty handling

Every value that can be absent forces a decision the moment you return or accept it: how is "nothing here" represented, and who checks for it. Left to reflex, absence is handled ad hoc — one function returns null, another an empty collection, another throws, another a sentinel like `-1` — and each caller guesses which. The failure is a null that leaks across a boundary and lands as a crash three layers away from the code that produced it, or an "empty" quietly conflated with an "error." Two builders pick two representations for the same absence, and the callers can't tell them apart. This rule pins the discriminator so two builders converge on one explicit absence strategy per boundary.

## The discriminator

Decide, **at each boundary, how absence is represented — and convert to that representation at the edge, so interior code never defends against null.** The test is who is forced to check:

- **Choose the representation that fits the meaning, and keep the three meanings distinct.** *Empty* (a well-formed collection with zero elements — usually returned as an empty collection, never null, so callers iterate without a guard), *absent* (there legitimately is no value — an explicit `Optional`/`Maybe` or a null-object that answers safely), and *error* (something went wrong producing it — a failure result, not a null). Collapsing these is the bug: an empty list returned as null forces a guard on a case that needn't exist; an error returned as an empty list hides the failure.
- **Never return a bare null across a public API.** A nullable return pushes a defensive check onto *every* caller, forever, and the one caller who forgets ships the crash. Return an explicit absence type the signature advertises, so the caller is forced to handle the missing case at compile time rather than discovering it at runtime ([model-with-the-type-system](model-with-the-type-system.md)).
- **Convert at the boundary, once.** Absorb whatever an external source hands you — null, missing key, sentinel — and translate it to your chosen representation right where it enters ([parse-dont-validate](parse-dont-validate.md), [handle-errors-at-the-boundary](../errors/handle-errors-at-the-boundary.md)); the strongest form is a design where the absent case can't arise inside at all ([define-errors-out-of-existence](../errors/define-errors-out-of-existence.md)).

(basis: C.A.R. Hoare — the null reference as his "billion-dollar mistake," the class of failures caused by an unchecked absent value; Fowler's null-object pattern — a stand-in that responds safely so callers need no null guard; and established Optional/Maybe practice — an explicit absence type the signature declares, preferred over sentinel nulls that the type system can't police.)

## The anchors

- *Good:* a lookup returns `Optional<User>`; the signature announces the miss, the caller must open it to use the value, and there is no reachable path where a null user is dereferenced. A list-returning query returns `[]` for "no matches," so callers iterate unconditionally.
- *Bad:* the same lookup returns `User` or null; three of four callers guard, the fourth doesn't, and a missing user surfaces as a null-dereference in an unrelated module — or a "no rows" result comes back as null instead of an empty list, and every loop over it needs a null check first.
