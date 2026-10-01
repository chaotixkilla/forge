# DRY vs. incidental duplication

You are looking at two blocks of code that look alike, and the pull is to collapse them into one — a shared function, a common base, a single config. But some sameness is real and some is a coincidence: two blocks can be byte-identical today yet answer to entirely different reasons-to-change tomorrow, so merging them couples things that were never meant to move together. The judgment this rule governs is *whether this repetition is one truth showing up twice, or two truths that momentarily rhyme* — and left to taste one engineer dedupes on sight while another leaves it, so the codebase collects both a wrong abstraction and a missed one.

## The discriminator

Ask what would make each copy change: **do the two copies change for the *same reason*, or for *different reasons* that happen to look the same right now?**

- **Same reason to change → it's shared *knowledge* → dedupe.** If a change to the rule (a tax formula, a validation policy, the wire format) would have to be made in both places to stay correct, they are one truth. Two copies of one truth is a bug waiting for the day someone updates only one. Give it a single authoritative home.
- **Different reasons to change → *incidental* duplication → leave it.** If the two blocks are alike by coincidence — two unrelated domains that today need the same three lines — merging them creates a coupling that fights you the moment one side needs to change and the other doesn't. The shared abstraction then grows a flag, then a second flag, until it serves no one.
- **The tell:** imagine the next realistic change to each site. If it lands on both, they share knowledge. If it lands on one and would *break* the other, they don't.

DAMP, the test-readability principle, is a separate call; don't conflate it with this one.

(basis: Hunt & Thomas, *The Pragmatic Programmer*, DRY)

## The fork: strict DRY, or tolerate duplication

The reason-to-change test settles most cases before this fork is reached. For the rest, *how eagerly to collapse repetition* is a genuine, contested fork — encode it, don't pick a house winner:

- **Strict DRY.** Any repetition of knowledge is debt; dedupe on sight, at the second occurrence. Cost: committing to an abstraction on two data points risks committing to the *wrong* one, and a wrong abstraction is costlier to unwind (re-inline, re-separate) than duplication is to remove later.
- **Tolerate duplication.** Wait until the shared shape has proven itself before extracting; a premature merge is worse than a little copying. Cost: you carry duplicates meanwhile, and a factoring deferred under deadline may never happen, so real shared knowledge drifts out of sync.

**Routing rule (non-gating): surrounding convention → house rule → maintainer.** The house rule, for a case the reason-to-change test leaves genuinely uncertain, is to keep the copies separate until the shape proves itself: an abstraction merged on an uncertain call is the wrong-abstraction risk this fork weighs. `(routed to maintainer: uncertain keeps the copies separate, as the design-time change-together test held; the exact count that triggers extracting once the test is decisive — the second occurrence or the third — no authority sets.)` Read what the module already does — if the codebase factors aggressively, match it; if it tolerates copies until a pattern is undeniable, match that. This is the **home** of the extract-early-vs-wait fork: [right-altitude-abstraction](right-altitude-abstraction.md) (which owns the abstraction's *shape*) and [avoid-premature-abstraction](avoid-premature-abstraction.md) (which owns *whether to abstract yet*) both defer here for *how much* duplication is enough. And never merge for a caller that doesn't yet exist ([avoid-premature-abstraction](avoid-premature-abstraction.md)).

(basis: Hunt & Thomas, DRY, against Fowler & Roberts's Rule of Three, *Refactoring* 2nd ed., Metz, "The Wrong Abstraction", and Dodds, "AHA Programming" — the last two practitioner sources weaker than DRY but pulling the other way)

## The anchors

- *Good (dedupe):* two endpoints both compute the same order-total including the same discount rule; a pricing change must hit both to be correct — one authoritative `orderTotal()`, both call it.
- *Bad (wrong merge to reject):* a `formatUserLabel` and a `formatInvoiceLabel` are three identical lines today, so you fuse them into `formatLabel(kind)`; the next sprint the invoice label needs a currency and the user label needs a badge, and the merged function sprouts branches for both — the copies never shared a reason to change ([reuse-before-writing](reuse-before-writing.md) flagged this near-match as incidental).
