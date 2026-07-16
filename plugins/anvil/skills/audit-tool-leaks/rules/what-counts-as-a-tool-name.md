This is the craft at the center of the whole audit: telling a concrete tool reference apart from a legitimate capability noun. Every leak the skill catches and every false positive it avoids comes down to this one judgment, made over and over against individual tokens. It's craft and not a checklist because the line isn't a word list — the same word can be a leak in one sentence and clean in another. What's durable is the test, not a roster of banned terms.

## The test: would swapping the tool change the sentence?

The single question that resolves almost every case: **could you replace this token with a different tool of the same kind, and have the sentence still mean what it meant?**

- If **yes**, the sentence is about a *capability* — what gets done — and the specific tool is incidental. It's clean. "Publish the report" survives swapping any publishing backend underneath it.
- If **no** — if the sentence only makes sense for one specific tool, or names a step, object, or parameter that only that tool has — it's a *leak*. The sentence has welded itself to a vendor.

The test works because it operationalizes the rule's actual purpose: the skill layer must stay swappable across tools, with all tool-specific knowledge confined below it. A token that survives the swap doesn't threaten swappability; one that doesn't, does.

## What a leak looks like

A leak names something an adapter would wrap:

- **A vendor or product name** — a specific SaaS, app, or service, including its brandable shortenings. The sentence now assumes that company exists and is the one in use.
- **A CLI binary** — the literal name of a command-line program a step says to run. "Run the formatter" is a capability; the program's actual name is a leak.
- **An SDK or library call** — a package import, a client class, a method that exists only for one provider's library.
- **A tool or connector id** — the machine identifier of one specific integration, in whatever id form the harness uses.
- **Borrowed jargon** — a vendor's proprietary word for a generic concept (their name for an issue, a board, a workspace, a channel), used as if it were the generic term. This is the sneakiest leak: it reads like a normal noun but silently pins the vendor, because only that vendor calls the thing that.

## What is fine

A capability noun names *what* without committing to *which*:

- **Capability verbs and objects** — "publish", "open a change request", "fetch the artifact", "notify the channel-of-record." These are roles a tool fills, not the tool.
- **Role names in the kit's own vocabulary** — "explorer", "critic", "the matching adapter", "the dispatch." These describe the architecture, not a product.
- **The configured-X form** — "the configured artifacts backend", "the configured tracker", "whichever provider is configured." Naming the *slot* a tool plugs into is the canonical clean phrasing; it makes the swappability explicit.
- **Config-key references** — pointing at a capability key the config defines is naming a category, not a vendor.

## Edge cases the swap test sharpens

- **Capability verb, concrete object.** "Open a change request" passes; "open a change request in <the named tracker>" fails — the verb is clean, the object leaked. Test the *whole* noun phrase, not just the verb.
- **A tool-specific parameter dressed as a setting.** A flag, field, or option that exists only for one provider is a leak even when the verb around it is generic. The swap exposes it: change the tool and the parameter is meaningless.
- **A category that sounds like a brand (or vice versa).** Some generic capability words began as products; some products use generic-sounding names. Don't judge by how brand-y the word *sounds* — apply the swap. If any tool of that kind slots in cleanly, it's a category; if only one does, it's a brand.
- **The word "adapter" and dispatch language.** Saying a capability "dispatches to the matching adapter" is skill-layer text *about the seam* and is clean — it names no tool, only the mechanism by which a tool gets reached. Don't flag the architecture for describing itself.
- **An ambient substrate vs the pluggable tool on top of it.** A plugin may treat some substrate as *ambient* — assumed universally present, not a configured backend a project chooses (a foundational version-control substrate, the shell). Three tiers, one test: named at the level of its *concepts* — the operations it offers generically — it survives the swap and is clean; named as a literal *CLI command* it is a leak, because the command is mechanism an adapter or the harness owns, not a capability; and the *pluggable* layer built on that substrate (a hosted provider of it) is a different thing again — it stays behind a port and is named as the configured capability. The generic concept is clean, the concrete command leaks (mechanism), the hosted provider leaks (belongs behind the port).
- **A methodology or pattern name that embeds a brand.** A proper noun for a *generic* technique whose name carries a vendor brand is a soft leak: the technique swaps fine, but the brand rides in on its name. When a generic synonym names the same model, prefer it — the branded name is an avoidable pin even though the underlying concept is clean. (If no generic synonym exists and the named thing genuinely is that one vendor's, it's a plain vendor leak, not this case.)

## When you genuinely can't decide

If the swap test comes back ambiguous — you can half-imagine another tool fitting but the sentence leans hard on one — treat it as a leak and rephrase to the configured-X form. The rephrase is cheap and lossless when the term really was a capability, and corrective when it wasn't. Ambiguity should resolve toward the rule, not against it; the cost of over-correcting a borderline term is one slightly more explicit sentence, while the cost of under-correcting is a vendor quietly pinned into the skill layer.
