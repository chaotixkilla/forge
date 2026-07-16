# Distrust untyped input and secrets

This is maintain's **always-on security baseline** — the hygiene applied on every run regardless of flags, distinct from the deeper, flag-gated audit in [security-pass](../modules/security-pass.md). It resolves a design question the skill was born with: security in maintenance is not opt-in. Baseline secret and taint hygiene lives here as a rule that fires on every change; `--security` *escalates* to the full delegated audit and gates completion. So even a routine dependency bump or refactor gets this lens; only the depth changes with the flag.

Two disciplines, applied to whatever the change touches:

## Treat data crossing a trust boundary as tainted

Any value that entered from outside the trust boundary — a request, a file, an environment value, a response from another service, a dependency's output — is hostile until validated. When a change moves, reads, or newly exposes such a value:

- **Validate and encode at the boundary**, not deep inside. Check shape and range where the data enters; encode/escape where it exits into a sink (a query, a shell, a template, a path, a deserializer). A value that reaches a sink without passing a boundary check is the defect.
- **A dependency upgrade is a taint event.** New code from an upgraded dependency crosses into your trust boundary; a change in how it parses, escapes, or validates is a security-relevant change even when the API looks identical ([dependency-upgrade-posture](dependency-upgrade-posture.md)).

## Keep secrets out of code

- **Credentials, tokens, and keys never live in source or in a committed file** — they're referenced through the project's configured secret mechanism. A change that hard-codes a secret, logs one, or moves one into a committed config is a defect to stop, not a style nit.
- **Don't widen a secret's exposure incidentally** — a refactor that puts a credential into a log line, an error message, a cache, or a serialized payload has leaked it, even if the value was already configured correctly.

## The bound: hygiene, not a threat model

This rule is a uniform hygiene lens a cold executor applies the same way every run — spot the tainted-data path and the mishandled secret in the code the change touches. It is deliberately *not* a full threat model: enumerating adversaries, mapping attack surface, dependency-advisory and supply-chain analysis, and compliance mapping are the [security-review](../../security-review/SKILL.md) skill's work, reached through [security-pass](../modules/security-pass.md) when `--security` is set. When this baseline lens surfaces something beyond routine hygiene — a plausible injection, an authz gap — treat it as a hand-off signal to that skill, noted in the change, rather than trying to fully adjudicate it here.

`(basis: the taint-tracking and secrets-management baseline is the common core of application-security guidance — validate/encode untrusted input at trust boundaries, keep credentials out of code — e.g. OWASP's input-validation and secrets-management guidance; the *depth* boundary between this always-on hygiene and the flag-gated audit is maintain's design decision, mirroring how review carries a code-review-depth security lens while security-review owns the full threat model.)`
