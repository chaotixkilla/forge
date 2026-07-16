# Fix at the right altitude

Once the mechanism is known, there is still a choice: *where* to put the correction. The convenient answer — patch the call site where the failure surfaced — is usually the wrong one, because it guards one path while the invariant stays breakable everywhere else. The right answer is the layer that *owns* the violated invariant. Getting this wrong turns a root-cause fix back into a symptom patch, one layer up. This rule is the test for the layer a fix belongs at.

## Place the fix where the invariant lives

Find the layer that is *responsible* for the property the bug violated — the highest point at which the bad state first becomes representable, the boundary whose contract says "past here, this holds." That is where the fix belongs. A value that should never be null belongs guarded where it is produced or where it enters the system, not at the tenth reader that happened to dereference it first.

The tell of a **too-low patch** (wrong altitude): the change makes the *symptom* stop while the bad value still flows past the boundary that should have rejected it — so the same fault re-emerges at the next reader that isn't guarded. If your fix has to be repeated at each call site, it is at the wrong altitude; the invariant it protects lives one layer up.

## The fail-fast exception — raise louder, never swallow

There is a legitimate reason to add a check at an *outer* layer in addition to the cause-layer fix: to fail fast and loudly at a boundary, so a future violation surfaces at its source instead of three layers away. The discriminator that separates this from a band-aid:

- **Legitimate:** the outer check *raises a truer, louder error* — it names the real invariant and stops, making future occurrences easier to root-cause.
- **Band-aid:** the outer check *returns a plausible value and continues* — it swallows the bad state, and the real bug disappears into the layers below, harder to find next time.

Add the first; never the second. The cause-layer fix is still owed either way.

## Before removing an existing guard, learn why it's there

If the fix means removing an existing workaround — a sleep, a retry, a defensive clamp someone added before — find out what it was compensating for first. An unexplained guard is often load-bearing (a past incident's mitigation that was never replaced by a real fix); removing it blind reintroduces the original bug. Ask what would have to be true for it to make sense; if you can't answer, treat its removal as its own change to verify, not a free cleanup.

`(basis: the "put the corrective as close as possible to the cause" and "smallest change = smallest scope, not fewest lines" formulations are from practitioner craft — D. Hayes, WPShout 2018 — and the boundary-defense-vs-silent-swallow distinction from T. Hoffman, Memfault 2020 ("Defensive and Offensive Programming"). The invariant-ownership test ("the layer responsible for the violated property") is the durable principle beneath them; the removing-a-guard caution is Chesterton's Fence applied to fixes. No single authority sets this bar numerically — it is craft with a stated discriminator, not a threshold.)`
