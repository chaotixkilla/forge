# Keep functions cohesive

Every function should do one job. The judgment this rule governs is what counts as "one job" — the line you draw when a function starts feeling too big and you decide whether to split it. The trap is treating *length* as the criterion: a builder who splits at a line count will carve a cohesive routine in half at an arbitrary seam, while another who never splits lets three concerns pile into one body. Both are judging the wrong property.

## The discriminator

A function is too big when it bundles **more than one *independent concern*** — not when it crosses some line count. The bar is **concern-distinctness**: are the sub-steps facets of one outcome, or separable jobs sharing a body? Length is a *smell* that invites the question, never the answer. Two tests, applied together, because either alone misfires:

- **The "and" test — a prompt, not the verdict.** Try to name everything the function does in one honest phrase. If the only honest phrase joins unrelated verbs with "and" ("validates the order *and* charges the card *and* emails the receipt"), that's a strong signal of multiple concerns. But a single covering verb can *hide* several — "synchronize the user," "handle the submit" — so a clean one-phrase name does **not** by itself prove one job. Do not stop here.
- **The co-occurrence test — the real bar.** Ask whether the sub-steps *always serve the one outcome together*, or whether a caller (or a test) could reasonably want one without the others. `syncUser` that fetches the remote record and updates the local one is **one job** — the two only mean anything as "sync," and no caller wants half of it. `handleSubmit` that validates input, mutates global state, and fires a network call is **three jobs** — each is an independently-meaningful concern something would want to reach alone, merely bundled under a convenient name. When a single verb covers the function, this is the test that decides: *facets of one outcome* → keep whole; *separable concerns under one name* → split.
- A long function that does one thing is fine; a short function that juggles three concerns is not. Length is only evidence; concern-distinctness is the verdict.

## The fork: how small is too small

*How aggressively to split cohesive-but-long functions* is a genuinely contested point on the record — encode it, don't pick a house winner:

- **Split aggressively (very short functions).** Prefer many tiny functions; "extract till you drop," so each does one obvious thing and reads like a paragraph of prose. Cost: pushed past cohesion, it fragments a single thought across many one-line helpers, and the reader reassembles the logic by chasing definitions — interface overhead exceeding the body it hides. (basis: Martin, *Clean Code* — functions should be very small, and you extract until you can extract no more.)
- **Stop at the cohesive unit (tolerate length).** Below a few dozen lines, further splitting a routine that already does one thing tends to *hurt* readability by scattering related logic and multiplying shallow interfaces. Cost: you carry longer function bodies, and a genuine second responsibility hiding inside one is easier to miss. (basis: Ousterhout, *A Philosophy of Software Design* — deep modules, cohesion over length; splitting for its own sake creates shallow methods that cost more than they save.)

That these two poles genuinely disagree is itself documented in the public Ousterhout↔Martin "aposd-vs-clean-code" debate, with Ousterhout as the standing counter to Clean Code's small-function guidance.

**Routing rule (non-gating): surrounding convention → house rule → maintainer.** Match the function size the surrounding module already keeps — a codebase of tiny functions and one of larger cohesive routines are each internally consistent, and consistency reads better than either dogma imposed. Either way the non-negotiable both poles share: **one nameable job** is the real bar; size only tells you where to look.

## The anchors

- *Good:* a 40-line parser that does exactly one thing — turn a token stream into an AST node — left whole, because every line serves that single job and no sub-part earns an honest name of its own.
- *Bad:* a 15-line `handleSubmit` that validates input, mutates global state, and fires a network call — short by any line count, yet three unrelated jobs that must be split before it can be named, tested, or reused honestly ([keep-functions-pure](keep-functions-pure.md) governs the effect it tangles in).
