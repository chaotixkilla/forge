# Handle errors at the boundary

When something can fail, the reflex is to catch it right where it happens — wrap the call, swallow the exception, return a default, log and continue. That reflex, applied everywhere, produces a codebase where every layer half-handles every failure: errors are caught too early to be handled meaningfully, swallowed where the caller needed to know, or scattered so no layer owns the decision. The judgment this rule governs is *where* each failure is caught, surfaced, or propagated — and left to reflex, two builders put the handler in two different places, so the same failure is fatal in one path and silent in another. This rule pins which boundary owns it.

## The discriminator

Handle a failure at the boundary where **the code first has enough context to decide what to do about it** — and propagate it, untouched, through every layer that doesn't. The test for a given `try`/catch or error check:

- **Can this layer actually *do* something correct with the failure** — recover, retry, substitute, or translate it into a meaningful result for its caller? If yes, this is the boundary; handle it here. If no, it does not belong here — let it propagate.
- **A "boundary" is where responsibility changes**, and the recurring ones are: the **trust boundary** (untrusted input enters — validate it here and only here, [validate-at-the-trust-boundary](validate-at-the-trust-boundary.md)); the **system boundary** (a call to an external service, DB, filesystem — where the failure is expected and a retry/timeout/fallback story lives); and the **top of a request/operation** (where an unrecoverable failure is turned into a user-facing result, a status code, a logged incident). Between boundaries, code should assume its inputs are already valid and let unexpected failures fly.
- **Catching without handling is the anti-pattern**: a `catch` that logs and swallows, or returns a default that masks the failure, moves the error's boundary to *nowhere* — the caller proceeds on bad state. Either handle it (do something correct) or propagate it (preserve its context — don't drop the stack or the original cause). A bare catch that does neither is the bug.

(basis: McConnell, *Code Complete* — the "barricade": validate at the boundary, trust inside it; Ousterhout, *A Philosophy of Software Design* — pull error handling to where it can be dealt with, and prefer designs that reduce the number of places that must handle it ([define-errors-out-of-existence](define-errors-out-of-existence.md)). The "handle where you have context to decide" test is the shared principle.)

## How it sits with the fail-fast / graceful poles

*Which* boundary interacts with *how loudly* to fail there, and the two poles are governed by their own rules — this rule places the handler; those decide its posture:

- Inside the barricade, a violated invariant is a *programmer error* — fail loud and early so bad state can't flow ([fail-loud-in-dev](fail-loud-in-dev.md)).
- At a system/trust boundary, an *expected* failure (bad input, a service down) is not a crash — handle it deliberately with the chosen strategy ([choose-an-error-strategy](choose-an-error-strategy.md)) and clean up on the failing path ([clean-up-on-the-failing-path](clean-up-on-the-failing-path.md)).

The discriminator between "assert and crash" and "handle gracefully" is *whose fault the failure is*: a broken internal assumption fails fast; an anticipated external condition is handled at its boundary.

## The anchors

- *Good:* a parse function at the API edge validates and rejects malformed input with a clear error; the inner functions it feeds assume valid data and don't re-check; a DB call three layers down that times out propagates up to the request handler, which owns the retry-or-fail decision.
- *Bad:* every function in the chain wraps its DB call in a `try/catch` that logs and returns `null`, so a timeout surfaces as a mysterious null three layers up with the original error long since swallowed — no layer owns the failure, and the caller runs on bad state.
