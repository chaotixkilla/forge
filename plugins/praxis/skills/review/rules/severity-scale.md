# The severity scale

Severity answers one question: **how bad is the consequence, if the finding is real?** It is assigned in [triage-and-rank](../phases/05-triage-and-rank.md), consumed by [deliver-findings](../phases/06-deliver-findings.md) (the `--severity-min` floor and the ranking) and by [gate-mode](../modules/gate-mode.md) (the gate's floor). Severity is orthogonal to certainty ([calibrate-certainty-to-rigor](calibrate-certainty-to-rigor.md)): *how bad if real* versus *how sure it is real*. Keep them separate — a traced nit is low severity / traced certainty; an unverified data-loss bug is critical severity / unverified certainty. Reachability is a certainty input, never a severity one: an unestablished path lowers how sure the finding is, not how bad it would be. `(basis: derived from the orthogonality above)`

## The five levels

`(basis: maintainer, 2026-07-02)`

- **critical** — a correctness or security defect that causes an unrecoverable loss (data loss/corruption, a security breach such as auth bypass, injection, or secret exposure) or takes down a core flow, with no guard stopping it.
  - *Anchor (top of scale):* a query built by concatenating unsanitized request input, on the login path — an attacker bypasses auth and reads other users' data.
- **high** — a defect that produces a wrong result or a failure on a plausible input, but whose damage is bounded: one feature or flow, recoverable, no data loss or breach.
  - *Anchor:* an off-by-one that drops the last element for every non-empty list returned by an exported function.
- **medium** — misbehaves only on an edge or uncommon input, **or** is a craft problem very likely to *become* a bug as the code evolves (a footgun).
  - *Anchor:* a null-dereference that triggers only when an optional config field is absent.
- **low** — no correctness impact for any input; a craft cost a maintainer really pays: duplication, a misleading name, a missed convention, a minor inefficiency off the hot path.
  - *Anchor:* a helper reimplemented inline where an existing one in the same module would do.
- **info** — an observation worth surfacing that needs no action to land; a suggestion the author may reasonably decline.
  - *Anchor (bottom of scale):* "this shape recurs three times in the file; consider extracting it later."

## The scannable marker

Each level carries a **pinned visual marker**, so a reader scans severities at a glance rather than reading every word to find the worst one ([deliver-findings](../phases/06-deliver-findings.md) leads each finding, and the verdict tally, with it):

**🔴 critical · 🟠 high · 🟡 medium · 🔵 low · ⚪ info**

The marker is **always paired with the word** (`🔴 critical`), never emoji-only — so it degrades to the plain label in a text-only sink and stays legible to a reader who can't see the glyph. `(basis: maintainer, 2026-07-15)`

## The adjacent-level discriminators

Assign by walking down until a level fits; the boundary tests are what stop a finding sliding between two rungs:

- **critical vs high** — is the consequence *unrecoverable or a breach*? Critical. *Bounded and recoverable*? High. (blast radius + recoverability)
- **high vs medium** — does a *plausible real input* trigger it? High. Does it need an *edge* input? Medium. (input plausibility; reachability is certainty's)
- **medium vs low** — can it produce a *wrong result*, now or as the code plausibly evolves? Medium. Is behavior *correct for all inputs* and only the form worse? Low. (this is the correctness/craft line — [separate-correctness-from-taste](separate-correctness-from-taste.md))
- **low vs info** — does a maintainer pay a *real cost* (a likely future bug, a genuine inefficiency, a name that misleads)? Low. Is *declining it reasonable*? Info. (actionability)

When two levels both seem to fit, the higher wins only if you can name the input or path that justifies it; absent that evidence, drop a level. A severity you cannot anchor to a concrete consequence is a certainty problem masquerading as severity — re-check it against [anchor-every-claim](../../../craft/evidence/anchor-every-claim.md).

## What this scale does *not* grade

This scale grades **correctness defects** (by consequence) and **craft findings** (by maintainer cost) — the two piles [separate-correctness-from-taste](separate-correctness-from-taste.md) defines. It does **not** grade **scope findings** (a bundled, unrelated change flagged per [respect-author-intent](respect-author-intent.md)): a scope finding states something is *outside* the reviewed change, so it has no consequence-in-the-change to place on any rung. Scope findings carry no severity — they are boundary notes delivered in their own section ([deliver-findings](../phases/06-deliver-findings.md)), out of the verdict tally. Do not reach for this scale to grade one; if a bundled change is itself *wrong*, that is an ordinary correctness finding on that change, graded here like any other.
