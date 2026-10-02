# The outcome taxonomy

A caller reads this port to learn what the org wrote down. What it does next turns entirely on *which kind of nothing* it got back: read the source another way, retry, escalate access, fix a reference, reshape the request, or record a genuine absence as evidence. So this port returns one of a fixed set of **capability-level outcomes**, never a backend's own error, and one of them is a *success*. The distinction the whole port exists to preserve is between **reached the space and it holds nothing** and **never reached the space** — a caller that conflates them reports an absence it never established, and a fabricated absence is indistinguishable from a real one downstream.

`(basis: derived from [artifacts/rules/failure-taxonomy.md](../../artifacts/rules/failure-taxonomy.md))`

## The seven outcomes

- **`unsupported`** — the source can't be read this way at all: its adapter doesn't support the read, or a search has no root to be confined to ([SKILL.md](../SKILL.md) step 3), so the read is never dispatched. It says nothing about what the space holds, and retrying never changes it. The caller reads the source another way, such as walking it from its entry references, or records it as not read. *(Assignment test: the read was not dispatched because this source can't perform it.)*
- **`ok`** — the read executed against the resolved space and the backend answered in full. **An empty answer is `ok`**: a search that matched nothing, or a document with no children, is a fact about the space, and the port reached the space to learn it. Every `ok` carries the source and resolved space it queried, so the caller can see *what* was read and not merely that something was. *(Assignment test: the request reached the backend, and the backend's answer is complete.)*
- **`unavailable`** — the request never reached an authenticated backend: the capability isn't configured, the service is down or rate-limited, the transport failed, **or the running context cannot dial the configured transport at all.** The retryable/degradable class. *(Assignment test: the request never reached an authenticated backend.)*
- **`unauthorized`** — the backend was reached and the identity is known, but that identity may not read this target or scope. The caller escalates access; retrying changes nothing. *(Assignment test: reached + authenticated, but forbidden for this target.)*
- **`target-not-found`** — the reference the request *named* does not exist on the backend. The caller fixes the reference. *(Assignment test: the request named a specific target and that target is absent.)*
- **`unreadable-content`** — reached and permitted, but what is there cannot be returned as document content: a reference that resolves to a container or schema rather than a document, or content the adapter cannot render as text at all. The caller reshapes the request. *(Assignment test: a representability gap in the backend, not an access or existence problem.)*
- **`partial`** — the read executed and returned **less than the whole answer**, and knows it: a truncated document, a result set cut short by a page limit, or a subtree the identity cannot see inside an otherwise readable space. Returned *with* whatever was read. The caller either narrows the request or records the answer as incomplete. *(Assignment test: reached and answered, but the answer is known-incomplete.)*

## The partition

Every run lands in exactly one, by this cascade — **the first "no" wins, and the order is the precedence**:

1. Can this source perform the read, by its adapter's **Supported reads**? **No → `unsupported`**. A provider with no adapter has no such section to answer from: its source goes to step 2 and lands `unavailable`, never `unsupported`. `(basis: derived — unsupported is what an adapter declares its backend can't do, and an absent adapter declares nothing)`
2. Did the request reach an authenticated backend? **No → `unavailable`**
3. Was the read permitted for this target or scope? **No → `unauthorized`**
4. If the request named a specific target, does it exist? **No → `target-not-found`**
5. Can what is there be returned as document content? **No → `unreadable-content`**
6. Was the whole answer returned? **No → `partial`**
7. Otherwise → **`ok`** (with the result, empty or not)

Exhaustive because every run answers all seven questions; mutually exclusive because the cascade stops at the first "no." A run that "found nothing" never falls out of the set — it reaches step 7 and returns `ok` with an empty result.

**A read across several sources is one run per source.** Each source's read lands in exactly one outcome by the cascade — one source `ok`-empty, another `unavailable`, a third `ok` with results — and there is no composite outcome. Rolling them into one would either report the whole read as failed when most sources answered, or report an absence across sources one of which was never reached.

## Confusable-pair discriminators

- **`ok`-empty vs `unsupported`** — a search the backend ran and that matched nothing is `ok`; a search it can't run is `unsupported`. Never answer a read the source can't perform with an empty `ok`: that asserts the space was searched.
- **`ok`-empty vs `unavailable`** — the space was queried and answered nothing → `ok`; the query never reached the space → `unavailable`. Never let an unreached read return an empty result: an empty `ok` asserts *the space does not hold this*, which is a claim about the org that only a completed read can make.
- **`ok`-empty vs `target-not-found`** — turns on what the request *named*. A **search** asks a question of the space; no match is `ok` with zero references. A **fetch** or **children** request names a specific target; its absence is `target-not-found`.
- **`ok`-empty vs `partial`** — `ok` asserts the answer is complete; `partial` asserts it is knowably not. An empty result the backend confirmed is `ok`; an empty-so-far result cut off by a limit is `partial`.
- **`unavailable` vs `unauthorized`** — reachability against permission: no credentials or no transport → `unavailable`; reached and authenticated but forbidden → `unauthorized`.
- **`unauthorized` vs `target-not-found`** — existence counts as *confirmed* only when the backend returns an unambiguous not-found distinct from its forbidden response. Where a backend masks absence as forbidden (one indistinguishable response for both), the default is **`unauthorized`** — never guess absence into a not-found, because a fabricated not-found sends the caller to fix a reference that was never wrong.
- **`unauthorized` vs `partial`** — a scope refused *outright* is `unauthorized`; a scope silently *skipped* inside a space that otherwise answered is `partial`. The second is the more dangerous, because the backend returns success.

## What this taxonomy does not cover

A **malformed invocation** — a read request naming no operation, a reference the port cannot parse before any backend interaction, a source name no resolved source carries, or a fetch or children request naming no source whose reference no resolved source's provider can claim — is not one of these seven. It is rejected up front as the caller error it is, so a caller never reads a self-inflicted argument error as a fact about the backend. Nor is there a `conflict` outcome: the port never writes, so no target state can block a request. And **listing the sources** reads the config, not a backend: it returns the list, never one of these outcomes.

## Where it binds

Adapters do the mapping: each adapter's **Supported reads** section names the reads its backend can perform, and its **Failure surface** section translates its backend's concrete conditions into exactly these outcomes. The concrete condition→outcome mappings live in the adapter, never in this rule. Step 4 of [SKILL.md](../SKILL.md) returns each source's outcome to the caller unchanged.
