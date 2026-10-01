# Define errors out of existence

When a case can go wrong, the reflex is to reach for handling — a check, a thrown error, a branch every caller must then remember. The judgment this rule governs comes one step earlier: before adding that handling, whether the *API itself* can be shaped so the error case simply isn't one. Left unasked, an error the design could have absorbed instead propagates as an obligation onto every caller — each must check for null, catch the exception, handle the out-of-range case — and the handling code outweighs the working code.

## The discriminator

The property this turns on is **whether the error case can be redefined into a normal case without lying to the caller** — reduce the *number of places* that must deal with the error, don't just relocate the handling.

- **Can the operation define the "error" as valid behavior?** Deleting a range that runs partly past the end can *clamp* to what exists instead of erroring; a lookup that misses can return empty rather than throwing; an operation on nothing can be a well-defined no-op. If the redefined semantics are honest and useful, every caller's guard disappears.
- **Can the return shape make the bad case unrepresentable?** Returning an empty collection instead of null means no caller can forget the null check — there is no null ([null-and-empty-handling](null-and-empty-handling.md)).
- **The line you must not cross:** this is design, not suppression. Absorbing a case only counts if the new behavior is genuinely correct for callers. Swallowing a *real* failure to make the signature tidy isn't defining the error out of existence — it's hiding it, and a violated internal invariant must still fail loud ([fail-loud-in-dev](fail-loud-in-dev.md)).

(basis: Ousterhout, *A Philosophy of Software Design*, ch. 10)

## The anchors

- *Good:* a `deleteRange(start, end)` that clamps to the collection's bounds and deletes what overlaps — a call that runs past the end is normal, not an error, so no caller writes a bounds check; the failure that would have been handled everywhere is handled nowhere because it no longer exists.
- *Bad:* the same operation throws `IndexOutOfRange` on any overshoot, so every one of its dozen callers wraps it in a try/catch that mostly just clamps anyway — the design pushed a decision it could have owned once onto twelve call sites.
