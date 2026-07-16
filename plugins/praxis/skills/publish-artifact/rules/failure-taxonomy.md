# The failure taxonomy

When a publish fails, the caller has to *react* — keep a local copy, retry later, prompt for access, reshape the content, choose a write mode. It can only react if it hears the failure in terms it understands. Hand back a raw provider error and every caller's degrade logic has to learn that provider's error codes, and a provider swap breaks every caller. So this port returns one of a fixed set of **capability-level outcomes**, never a backend's own error. This rule pins that vocabulary and the discriminators between the confusable pairs, so the same underlying failure maps to the same outcome whichever executor handles it and whichever adapter raised it.

`(basis: derived — mirrors the vcs port's capability-failure principle (the caller reacts to an outcome class, never a provider code); the five classes partition publish's distinct failure axes (reachability / permission / existence / representability / target-state), with the term set taken from the regenerate brief. Not a maintainer-ratified fork — a derivation proposed with the skill.)`

## The five outcomes

Each names the axis it fails on and the reaction it invites:

- **`unavailable`** — the backend can't be reached or has no usable credentials at all: transport/network failure, the service is down, rate-limited/transient, or the capability isn't configured. **This is the retryable/transient class** — the caller can back off and retry, or degrade to a local fallback. *(Assignment test: the request never reached an authenticated backend.)*
- **`unauthorized`** — the backend was reached and the identity is known, but that identity lacks permission for this target or operation (can read, not write here; no access to this container). Caller must escalate access, not retry. *(Assignment test: reached + authenticated, but forbidden for this target.)*
- **`target-not-found`** — the resolved destination (a parent page, container, path, or a `--to` target id) does not exist on the backend. Caller must fix the destination. *(Assignment test: the target the request named is absent.)*
- **`unsupported-content`** — the backend cannot faithfully represent something the publish requires: a content block that survives no faithful degradation ([degrade-unsupported-content](degrade-unsupported-content.md)), **or** a requested mode the backend lacks (a `--draft` state, a versioned copy, an idempotent match the backend can't offer). Caller must reshape the content or drop the unsupported mode. *(Assignment test: a capability gap in the backend, not a state or access problem.)*
- **`conflict`** — the target exists and is reachable, but the write can't proceed as asked without ambiguity or loss: creating where one already exists (no `--idempotent`/`--version`), an idempotent identity that resolves to none or to several ([stable-identity-and-precedence](stable-identity-and-precedence.md)), or a concurrent modification. Caller must choose a mode (update, version, rename). *(Assignment test: the target is there, but the requested write is blocked by its state.)*

## Confusable-pair discriminators

Walk these when two outcomes seem to fit:

- **`unavailable` vs `unauthorized`** — could not reach an authenticated backend (no creds, transport down) → `unavailable`; reached and authenticated but forbidden for *this* target → `unauthorized`. (reachability vs permission)
- **`unauthorized` vs `target-not-found`** — the target exists but access is refused → `unauthorized`; the target is absent → `target-not-found`. Absence counts as *confirmed* only when the backend returns an unambiguous not-found distinct from its forbidden response. When the backend masks absence as forbidden (one indistinguishable "not found / no access" for both), the default is `unauthorized` — never guess absence into a not-found. So each adapter maps an unambiguous not-found → `target-not-found` and an ambiguous-or-forbidden response → `unauthorized`. (permission vs existence)
- **`target-not-found` vs `conflict`** — the target isn't there → `target-not-found`; the target *is* there but its state blocks the write → `conflict`. (existence vs target-state)
- **`unsupported-content` vs `conflict`** — the backend *can't* do what's asked (represent a block, offer a mode) → `unsupported-content`; the backend *could*, but the target's state is in the way → `conflict`. (capability gap vs target-state)

## What this taxonomy does and does not cover

These five classify a **publish outcome** — a failure that arises from the backend or the target once the skill dispatches (or resolves the destination against it): reachability, permission, existence, representability, target-state. A **malformed invocation** — a caller error caught before any backend interaction, such as passing `--idempotent` with `--version` ([stable-identity-and-precedence](stable-identity-and-precedence.md)) — is **not** one of these classes; it is rejected up front and reported as the contradictory flags it is, so a caller never has to read a self-inflicted argument error as a backend outcome.

## Where it binds

Adapters do the mapping: each adapter's **Failure surface** section translates its provider's concrete errors into exactly these outcomes (a permission-denied error → `unauthorized`, a missing-target error → `target-not-found`, and so on), so the outcome vocabulary is honored below the seam, not merely asserted here. The concrete code→outcome mappings (whatever error shape a given backend raises) live in the adapter, never in this rule. Step 5 of [SKILL.md](../SKILL.md) returns the outcome to the caller unchanged; the caller's degrade logic reads the outcome, never the provider error beneath it.
