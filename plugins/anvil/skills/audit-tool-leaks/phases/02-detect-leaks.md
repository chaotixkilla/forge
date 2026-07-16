A leak is a concrete tool wearing the costume of a capability. Detection is two passes, and the order is deliberate: first a wide, mechanical sweep that over-collects candidates, then an adversarial judgment pass that decides which candidates are real. The sweep alone is too blunt — it flags the word "publish" because some tool is named that — and judgment alone is too slow and too easy to fool, because a leak you never surfaced is a leak you never judged. Run both, in that order.

## Pass 1 — sweep for tool-name signals

Go through every file the collection phase handed you and surface anything that *could* name a concrete tool. You are casting a wide net here; precision comes in pass 2. The signals to match:

- **Vendor and product names** — a named SaaS, app, or service, and brandable shortenings of one.
- **CLI binaries** — the literal name of a command-line program a phase tells you to invoke.
- **SDK / library calls** — a package import, a client class, a method that only exists for one provider.
- **Tool / connector ids** — the machine identifier of a specific integration or connector, in whatever id shape the harness uses.
- **Tool-specific jargon** — a noun that only makes sense if you already know which backend is meant (a vendor's word for an issue, a board, a workspace, a channel).

Anchor every hit to file and line; later phases rank and rephrase against that anchor, and a finding a maintainer can't locate is a finding they can't fix. Resist the urge to adjudicate while you sweep — a borderline token belongs in the candidate pile, not in your head. The cost of a false candidate is one judgment call in pass 2; the cost of a missed candidate is a shipped leak. The inclusion bar, made operational: a token goes in the pile unless you can instantly place it as a known-clean form (a capability noun, the configured-X phrasing, one of the kit's own role names) — hesitation is itself the signal. *How* you sweep is deliberately open — pattern scan, straight read, either works, because the mechanism doesn't move the outcome; the output contract does: every collected file touched, every candidate anchored.

Do **not** treat the signal set as a fixed vendor list to memorize. The durable signal is the *shape* of the tell — "this word only resolves if you know the tool" — not a roster of today's products, which goes stale the moment a new one appears. (The craft of telling a tool token from a capability noun is [what-counts-as-a-tool-name](../rules/what-counts-as-a-tool-name.md); lean on it, don't re-derive it.)

## Pass 2 — challenge each candidate

Now flip from collecting to interrogating. Recruit the leak-hunter critic and hand it the candidate list. Its lens is adversarial by design: it *assumes* the skill layer is hiding a tool and tries to prove that each "capability" is a disguised tool reference. That posture matters — a sympathetic read passes leaks ("well, everyone knows what that means"); a hostile read is what catches the disguised ones. If recruiting isn't available in the current context, apply the same lens inline: assume each candidate hides a tool and make it prove otherwise.

The operative test for each candidate is the swap test: **could this token be replaced by a different tool of the same kind without changing the surrounding sentence's meaning?**

- If yes, it's a capability — the sentence is about *what* gets done, and the tool is incidental. Pass it.
- If no — if the sentence only makes sense for one specific tool, or names a step, a noun, or a parameter that only that tool has — it's a leak. Record it.

Watch for the leaks that hide *inside* capability-sounding phrasing, because those are the ones a sweep-only pass waves through:

- A capability verb chained to a concrete object: "open a change request" is clean; "open a change request in <the named tracker>" leaks the moment the object is the tool.
- A genuinely tool-specific *parameter* dressed as a setting — a flag, field, or option that exists only for one provider.
- Borrowed jargon — using a vendor's word for a generic concept so that the sentence silently assumes that vendor.

Anti-pattern: rubber-stamping a token because it *reads* fluently. Fluency is the disguise. The leak-hunter's whole value is that it doesn't grant the benefit of the doubt — and neither should you when you're adjudicating its findings.

## Classify each hit

Sort every candidate into exactly one bucket:

- **Leak** — names a concrete tool in the skill layer; fails the swap test. Carries forward to ranking and suggestion.
- **Legitimate capability term** — passes the swap test; a capability noun, a config-key reference, or the word "adapter" itself. Drop it.
- **Legitimate mention** — a tool name that is *allowed* in context: an explicitly-marked illustrative example, or (had it been in scope) an adapter's own detail. Judge intent, not just the token — see [legitimate-tool-mentions](../rules/legitimate-tool-mentions.md). Drop it, but only after confirming the marking is genuine and not a leak excusing itself.

The edge case worth slowing down for: an example that names a tool to illustrate a point. The question is never "does a tool name appear" but "is this text *instruction that depends on* the tool, or an illustration that happens to mention one." A clearly-fenced example ("for instance, a backend such as X") is a mention; the same name in a step a cold executor would *act on* is a leak. When the marking is ambiguous, treat it as a leak — the fix (make the example unmistakably illustrative, or rephrase to a capability) is cheap, and an "example" a reader might act on literally is exactly how leaks sneak in.

The output of this phase is the classified set: confirmed leaks with anchors, everything else dropped with the candidates cleared.
