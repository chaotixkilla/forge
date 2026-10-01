# Fix the cause, not the symptom

The commonest way a diagnosis ends wrong is stopping one level too early: fixing the place the failure *surfaced* instead of the place it was *caused*. The symptom fix passes the reproduction — that's what makes it seductive — but the mechanism is untouched, so the fault returns through another path, now masked by the patch that "fixed" it, and the next fix is harder because a guard now obscures where the real defect is. The instinct to patch the nearest surface — wrap the crashing call in a try, clamp the bad value where it's read — is strong because it's fast and it works *for the case in front of you*; it fails every other case the cause still reaches.

## Find the cause: a mechanism, not another effect

Keep asking *why does that happen?* one level deeper, and read each answer against a single test: **does it bottom out in a mechanism, or does it point at a further effect?**

- A **mechanism** is a self-contained "this produces that" — a specific line, state or interaction that, given its inputs, necessarily yields the next state. When the answer is a mechanism, asking "why" again would only ask why the *code is written that way* (a design question), not why the *failure occurs* (the fault question). That is the floor: stop there.
- An **effect** is another symptom wearing a cause's clothes: "the request fails because the cache is stale" — but *why* is the cache stale? If the answer names a further state that itself needs explaining, you're still on an effect, not the cause. Keep going.

The tell that you've stopped too early: the "cause" you name is itself something you'd have to debug. The tell that you've arrived: you can state the fix in terms of the mechanism, and you can explain every prior symptom as a consequence of it.

The cause is the earliest point where the code first does the wrong thing, not the point where the wrong thing becomes visible: a null that crashes three frames down originates where it was allowed to be null, not where it was dereferenced. Trace back along the data and control flow to the first frame that violated an invariant.

**Don't force a single linear chain.** Asking "why" repeatedly biases toward one line of causation and one root cause, but real failures often have a *branching* chain (two conditions that had to co-occur) or more than one contributing cause. Follow every branch the evidence supports, not just the first; a chain that felt too clean is often one where a co-cause was dropped. The depth is set by reaching a mechanism, not by a count of questions — the "five" in five-whys is illustrative, and stopping at an arbitrary depth is exactly how the method names a symptom as the root.

`(basis: Ohno 1988; Card, BMJ Quality & Safety 26(8), 2017; the stop test is the maintainer's, after Zeller, Why Programs Fail)`

## Place the fix where the invariant lives

Once the mechanism is known there is still a choice of *where* to put the correction, and the convenient answer — the call site where the failure surfaced — usually guards one path while the invariant stays breakable everywhere else. Find the layer *responsible* for the property the fault violated: the highest point at which the bad state first becomes representable, the boundary whose contract says "past here, this holds". The fix belongs there. A value that should never be null is guarded where it's produced or where it enters the system, not at the tenth reader that happened to dereference it first.

The test of a placement: *if I fix it here, does every downstream symptom disappear?* A fix that makes the symptom stop while the bad value still flows past the boundary that should have rejected it is **too low**, and the same fault re-emerges at the next reader that isn't guarded. A fix that has to be repeated at each call site is at the wrong altitude; the invariant it protects lives a layer up.

**A louder check at an outer layer is legitimate; a quieter one is a band-aid.** Adding a check at an outer layer *as well as* the cause-layer fix, to fail fast at a boundary so a future violation surfaces at its source instead of three layers away, is right when the check *raises a truer, louder error*: it names the real invariant and stops. It's a band-aid when it *returns a plausible value and continues*, swallowing the bad state so the real fault disappears into the layers below. Add the first, never the second; the cause-layer fix is owed either way.

**Before removing an existing guard, learn why it's there.** If the fix removes a workaround — a sleep, a retry, a defensive clamp someone added before — find out what it was compensating for first. An unexplained guard is often load-bearing, a past incident's mitigation that was never replaced by a real fix, and removing it blind reintroduces the original fault. Ask what would have to be true for it to make sense; if you can't answer, its removal is its own change to verify, not a free cleanup.

`(basis: Hayes, WPShout, 2018; Hoffman, Memfault, 2020; Chesterton's fence for removing a guard)`

## When a stopgap is acceptable

A knowingly-labeled stopgap — a symptom-level guard placed *deliberately*, as a holding action — is legitimate; pretending otherwise produces heroic cause-fixes nobody asked for. A stopgap is acceptable when **all** of these hold:

- **It's labeled and tracked.** The code says it's a stopgap (a comment naming what the real cause is) and a follow-up is recorded with the change, so it can't masquerade as the fix.
- **It doesn't deepen the debt.** The guard adds no new coupling to the symptom and doesn't make the eventual cause-fix harder — it holds the line, it doesn't build on the wrong foundation.
- **The cause is genuinely out of reach now.** The cause sits outside the change's scope or its risk tier ([change-risk-scale](../engineering/change-risk-scale.md)), or fixing it now is materially riskier than the stopgap — the cause is in a contract consumers outside the team depend on, say, which needs a migration path this change can't carry.

The **cause-fix is required** — a stopgap is *not* acceptable — when any of these hold, regardless of convenience:

- The symptom **recurs across sites**: the same guard is being, or would be, copied to several call sites — the signature of a systemic cause that a per-site patch will never contain.
- The stopgap would **mask data corruption or a security defect**: here a guard that hides the symptom is actively dangerous, because it removes the signal that the corruption or breach is happening.
- The cause is **inside the change's scope already**: you're touching the causing code anyway, so "out of reach" doesn't apply and patching around it is pure avoidance.

When a stopgap is acceptable, make it *visibly* one: name the real cause in a comment, keep the guard minimal, and record the follow-up. The honest stopgap is often the *more* reversible move ([smallest-reversible-change](../engineering/smallest-reversible-change.md)), and that's a point in its favor — as long as it's labeled.

`(basis: maintainer, 2026-07-11; after the debugging and refactoring literature)`
