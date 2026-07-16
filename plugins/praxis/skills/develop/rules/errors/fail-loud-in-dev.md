# Fail loud in dev

When code discovers that an assumption it depends on is broken — a value that should never be null is null, a case the switch was supposed to cover isn't, a state the invariant forbids exists — the judgment is whether to stop dead or to paper over it and keep going. The reflex to be "robust" quietly absorbs the impossible: return a default, skip the case, log a warning. That reflex hides a *logic bug* behind a plausible-looking result, so it surfaces far from its cause, as corrupt data three layers on, long after the stack that would have named it is gone. Two builders split by temperament — one asserts, one defends — and the same broken assumption is a loud crash in one path and a silent wrong answer in the other. This rule pins the discriminator so two builders converge on which failures should crash.

## The discriminator

The property this turns on is **whose fault the failure is and where the input came from** — and this is the same boundary question that separates it from graceful handling, not a rival philosophy.

- **A violated *internal* invariant is a programmer error** — trusted interior code reached a state your own logic says is impossible. Fail fast and loud: assert, guard, or throw at the point of discovery, so the failure dies with its cause attached rather than propagating as bad state. In dev especially, a dead program tells no lies; a limping one lies convincingly.
- **An anticipated *external* condition is not a bug** — untrusted input, a service down, a missing file. That is handled gracefully at its boundary ([handle-errors-at-the-boundary](handle-errors-at-the-boundary.md), [validate-at-the-trust-boundary](validate-at-the-trust-boundary.md)), and often designed away entirely ([define-errors-out-of-existence](define-errors-out-of-existence.md)). Crashing on expected external failure is as wrong as swallowing an internal one.
- **The test:** *could correct code ever produce this?* If no — impossible-by-design — fail loud. If yes — the world can produce it — handle it. Fail-fast and the barricade are the same map read from two sides: loud in the trusted interior, deliberate at the untrusted edge.

## The fork: fail-fast vs. defensive

*How much to assert versus absorb* reads as a contested fork, but it resolves to the boundary above — encode both poles, don't crown one:

- **Fail-fast pole.** Surface the broken assumption immediately; an assertion is cheap and its absence is expensive. Cost: an assertion that fires in production on a *recoverable* condition turns a degraded experience into an outage.
- **Defensive pole.** Keep running through the unexpected; tolerate and continue. Cost: absorbing a genuine invariant violation converts a diagnosable crash into silent, spreading corruption.

**Routing rule (non-gating): surrounding convention → house rule → maintainer.** These are emphasis-by-boundary, not tribes: apply fail-fast to the trusted interior and defensive handling to the untrusted edge, following what the surrounding code already does; absent a signal, the house rule, then the maintainer sets how aggressively assertions ship to production.

(basis: Hunt & Thomas, *The Pragmatic Programmer*, Topic 24 "Dead Programs Tell No Lies" — crash early, a program that has detected the impossible should not continue; Jim Shore, "Fail Fast", *IEEE Software* 2004 — assertions as the mechanism, catching bugs at debugging time. This sits against McConnell's barricade and Ousterhout's "define errors out of existence" not as a flat contradiction but as emphasis by boundary — trusted interior vs. untrusted edge — which is why it routes rather than rules.)

## The anchors

- *Good:* an `assert`/guard on a state the code's own logic says is unreachable — a supposedly-exhaustive switch throwing on the default case — so a future change that breaks the assumption fails at the line that broke it.
- *Bad:* a `catch` that logs and returns a default around a call that "shouldn't fail," swallowing a real logic bug — the program limps on with wrong state and the failure resurfaces as garbage output nowhere near its cause.
