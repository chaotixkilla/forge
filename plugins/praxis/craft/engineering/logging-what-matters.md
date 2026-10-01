# Logging what matters

As you write code that will run where you can't watch it, the judgment this standard governs is which log lines to leave behind and at what level. It is easy to under-do (ship a path that fails silently in production with nothing to go on) and just as easy to over-do (narrate every step until the real signal drowns, or quietly write a secret into the log).

## The discriminator

A log line earns its place if it would help someone answer **"why did this fail in production?"** without a rerun — otherwise it is noise. Apply the test as you write:

- **Log the decision points, not the narration.** Key state transitions, boundary crossings (a call out to another system, a request entering or leaving), and error context with the *why* — the values that would let a debugger reconstruct what happened, structured as the surrounding logs are, so a search can find them — earn a line. A line that narrates the happy path step by step ("entered function", "got value", "returning") is noise; it costs signal-to-noise and buys nothing.
- **Match the level to the audience and severity.** *Debug* for detail useful only when actively diagnosing; *info* for milestones an operator watches in normal running; *warn* for a recovered-from anomaly; *error* for a failure that needs attention. The level is a routing decision — wrong levels make the important invisible and the trivial alarming.
- **Never log secrets.** Credentials, tokens, keys, personal data, and full request/response payloads must never reach the log — a log is long-lived, widely readable, and often shipped off-box. Log an identifier or a redacted shape, never the sensitive value itself. This is the one non-negotiable.

Pair logging with the error's home: the line that explains a failure belongs where the failure is *handled* ([handle-errors-at-the-boundary](handle-errors-at-the-boundary.md)), not re-logged at every layer it passes through. Reach the logging facility the surrounding code already uses; match its level conventions and structure.

(basis: operability and observability practice)

## The anchors

- *Good:* on a payment call, one line at the boundary — "charge submitted, order=<id>, amount, gateway" at info; on failure, "charge rejected, order=<id>, reason=<code>" at error. A debugger reads exactly what was attempted and why it failed, with no card number in sight.
- *Bad (reject):* debug lines on every internal step of the happy path so the one failure is buried in a thousand routine lines — *and* one of them logs the full request body, tokens and all. Noise that hides the signal, plus a secret leaked to anyone who can read the log.
