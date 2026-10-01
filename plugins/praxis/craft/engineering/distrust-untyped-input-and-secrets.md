# Distrust untyped input and secrets

This is an **always-on security baseline**: hygiene applied to every change regardless of flags, even a routine dependency bump or refactor, and distinct from a full security review.

Two disciplines, applied to whatever the change touches:

## Treat data crossing a trust boundary as tainted

Any value that entered from outside the trust boundary — a request, a file, an environment value, a response from another service, a dependency's output — is hostile until validated. When a change moves, reads, or newly exposes such a value:

- **Validate and encode at the boundary**, not deep inside. Check shape and range where the data enters; encode/escape where it exits into a sink (a query, a shell, a template, a path, a deserializer). A value that reaches a sink without passing a boundary check is the defect.
- **A dependency upgrade is a taint event.** New code from an upgraded dependency crosses into your trust boundary; a change in how it parses, escapes, or validates is a security-relevant change even when the API looks identical.

## Keep secrets out of code

- **Credentials, tokens, and keys never live in source or in a committed file** — they're referenced through the project's configured secret mechanism. A change that hard-codes a secret, logs one, or moves one into a committed config is a defect to stop, not a style nit.
- **Don't widen a secret's exposure incidentally** — a refactor that puts a credential into a log line, an error message, a cache, or a serialized payload has leaked it, even if the value was already configured correctly.

## The bound: hygiene, not a threat model

This rule is a uniform hygiene lens a cold executor applies the same way every run — spot the tainted-data path and the mishandled secret in the code the change touches. It is deliberately *not* a full threat model: enumerating adversaries, mapping attack surface, dependency-advisory and supply-chain analysis, and compliance mapping are a dedicated security review's work. When this baseline lens surfaces something beyond routine hygiene — a plausible injection, an authz gap — treat it as a signal that the change needs one, noted in the change, rather than trying to fully adjudicate it here.

`(basis: OWASP's input-validation and secrets-management guidance; the depth bound derived from the split between a code review's hygiene pass and a dedicated security review)`
