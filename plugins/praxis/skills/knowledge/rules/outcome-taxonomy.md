# The outcome taxonomy

A caller reads this port to learn what the org wrote down. What it does next turns entirely on *which kind of nothing* it got back: retry, escalate access, fix a reference, reshape the request, or record a genuine absence as evidence. So this port returns one of a fixed set of **capability-level outcomes**, never a backend's own error, and one of them is a *success*. The distinction the whole port exists to preserve is between **reached the space and it holds nothing** and **never reached the space** — a caller that conflates them reports an absence it never established, and a fabricated absence is indistinguishable from a real one downstream.

`(basis: derived — the five failure axes and the confusable-pair method are the sibling artifacts port's ([publish-artifact/rules/failure-taxonomy.md](../../publish-artifact/rules/failure-taxonomy.md)), reused rather than re-derived; this set drops its write-only `conflict` (no write can be blocked by target state here) and adds two values a failure-only vocabulary has no rung for — `ok`, which must carry the empty result, and `partial`, the known-incomplete read. Named outcome- rather than failure-taxonomy because it classifies successes too. Not a maintainer-ratified fork — a derivation proposed with the skill.)`

## The six outcomes

- **`ok`** — the read executed against the resolved space and the backend answered in full. **An empty answer is `ok`**: a search that matched nothing, or a document with no children, is a fact about the space, and the port reached the space to learn it. Every `ok` carries the resolved space it queried, so the caller can see *what* was read and not merely that something was. *(Assignment test: the request reached the backend, and the backend's answer is complete.)*
- **`unavailable`** — the request never reached an authenticated backend: the capability isn't configured, the service is down or rate-limited, the transport failed, **or the running context cannot dial the configured transport at all.** The retryable/degradable class. *(Assignment test: the request never reached an authenticated backend.)*
- **`unauthorized`** — the backend was reached and the identity is known, but that identity may not read this target or scope. The caller escalates access; retrying changes nothing. *(Assignment test: reached + authenticated, but forbidden for this target.)*
- **`target-not-found`** — the reference the request *named* does not exist on the backend. The caller fixes the reference. *(Assignment test: the request named a specific target and that target is absent.)*
- **`unreadable-content`** — reached and permitted, but what is there cannot be returned as document content: a reference that resolves to a container or schema rather than a document, or content the adapter cannot render as text at all. The caller reshapes the request. *(Assignment test: a representability gap in the backend, not an access or existence problem.)*
- **`partial`** — the read executed and returned **less than the whole answer**, and knows it: a truncated document, a result set cut short by a page limit, or a subtree the identity cannot see inside an otherwise readable space. Returned *with* whatever was read. The caller either narrows the request or records the answer as incomplete. *(Assignment test: reached and answered, but the answer is known-incomplete.)*

## The partition

Every run lands in exactly one, by this cascade — **the first "no" wins, and the order is the precedence**:

1. Did the request reach an authenticated backend? **No → `unavailable`**
2. Was the read permitted for this target or scope? **No → `unauthorized`**
3. If the request named a specific target, does it exist? **No → `target-not-found`**
4. Can what is there be returned as document content? **No → `unreadable-content`**
5. Was the whole answer returned? **No → `partial`**
6. Otherwise → **`ok`** (with the result, empty or not)

Exhaustive because every run answers all six questions; mutually exclusive because the cascade stops at the first "no." A run that "found nothing" never falls out of the set — it reaches step 6 and returns `ok` with an empty result.

## Confusable-pair discriminators

- **`ok`-empty vs `unavailable`** — the distinction this port exists for. The space was queried and answered nothing → `ok`; the query never reached the space → `unavailable`. Never let an unreached read return an empty result: an empty `ok` asserts *the space does not hold this*, which is a claim about the org that only a completed read can make.
- **`ok`-empty vs `target-not-found`** — turns on what the request *named*. A **search** asks a question of the space; no match is `ok` with zero references. A **fetch** or **children** request names a specific target; its absence is `target-not-found`. So a search finding nothing and a fetch of a nonexistent page are different answers, not two spellings of one.
- **`ok`-empty vs `partial`** — `ok` asserts the answer is complete; `partial` asserts it is knowably not. An empty result the backend confirmed is `ok`; an empty-so-far result cut off by a limit is `partial`.
- **`unavailable` vs `unauthorized`** — reachability against permission: no credentials or no transport → `unavailable`; reached and authenticated but forbidden → `unauthorized`.
- **`unauthorized` vs `target-not-found`** — existence counts as *confirmed* only when the backend returns an unambiguous not-found distinct from its forbidden response. Where a backend masks absence as forbidden (one indistinguishable response for both), the default is **`unauthorized`** — never guess absence into a not-found, because a fabricated not-found sends the caller to fix a reference that was never wrong.
- **`unauthorized` vs `partial`** — a scope refused *outright* is `unauthorized`; a scope silently *skipped* inside a space that otherwise answered is `partial`. The second is the more dangerous, because the backend returns success.

## What this taxonomy does not cover

A **malformed invocation** — a read request naming no operation, or a reference the port cannot parse before any backend interaction — is not one of these six. It is rejected up front as the caller error it is, so a caller never reads a self-inflicted argument error as a fact about the backend.

## Where it binds

Adapters do the mapping: each adapter's **Failure surface** section translates its backend's concrete conditions into exactly these outcomes, so the vocabulary is honored below the seam rather than merely asserted here. The concrete condition→outcome mappings live in the adapter, never in this rule. Step 4 of [SKILL.md](../SKILL.md) returns the outcome to the caller unchanged.
