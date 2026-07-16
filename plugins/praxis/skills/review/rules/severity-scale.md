# The severity scale

Every finding review keeps carries a severity, and severity is what lets the author triage: fix this before landing, fix it soon, or note it and move on. If the scale is undefined, each reviewer invents their own ladder — one calls a null-deref "critical," another "medium," and the same change gets two incompatible verdicts. A rated output with no defined scale is not a lighter-weight review; it is a review whose most load-bearing judgment is left to chance. This rule pins the scale so two cold reviewers land a borderline finding on the same rung.

Severity answers one question: **how bad is the consequence, and how reachable is it?** It is assigned in [triage-and-rank](../phases/05-triage-and-rank.md), consumed by [deliver-findings](../phases/06-deliver-findings.md) (the `--severity-min` floor and the ranking) and by [gate-mode](../modules/gate-mode.md) (the pass/fail floor). Severity is orthogonal to confidence ([calibrate-confidence-to-effort](calibrate-confidence-to-effort.md)): *how bad if real* versus *how sure it is real*. Keep them separate — a confirmed nit is low severity/high confidence; a speculative data-loss bug is critical severity/low confidence.

## The five levels

`(basis: ratified by the maintainer, 2026-07-02. The five-level scale below — derived from blast-radius → reachability → correctness → actionability; code-review severity has no single external authority the way security vulnerabilities have CVSS, so the rung boundaries and anchors are the maintainer's ratified house standard.)`

- **critical** — a correctness or security defect that, on a reachable path, causes an unrecoverable loss (data loss/corruption, a security breach such as auth bypass, injection, or secret exposure) or takes down a core flow, with no guard stopping it.
  - *Anchor (top of scale):* a query built by concatenating unsanitized request input, on the login path — an attacker bypasses auth and reads other users' data.
- **high** — a defect that produces a wrong result or a failure on a plausible, reachable input, but whose damage is bounded: one feature or flow, recoverable, no data loss or breach.
  - *Anchor:* an off-by-one that drops the last element for every non-empty list returned by an exported function.
- **medium** — misbehaves only on an edge or uncommon input, **or** is a real correctness risk whose reachability you could not confirm, **or** is a craft problem very likely to *become* a bug as the code evolves (a footgun).
  - *Anchor:* a null-dereference that triggers only when an optional config field is absent.
- **low** — no correctness impact for any input; a craft cost a maintainer really pays: duplication, a misleading name, a missed convention, a minor inefficiency off the hot path.
  - *Anchor:* a helper reimplemented inline where an existing one in the same module would do.
- **info** — an observation worth surfacing that needs no action to land; a suggestion the author may reasonably decline.
  - *Anchor (bottom of scale):* "this shape recurs three times in the file; consider extracting it later."

## The scannable marker

Each level carries a **pinned visual marker**, so a reader scans severities at a glance rather than reading every word to find the worst one ([deliver-findings](../phases/06-deliver-findings.md) leads each finding, and the verdict tally, with it):

**🔴 critical · 🟠 high · 🟡 medium · 🔵 low · ⚪ info**

The marker is **always paired with the word** (`🔴 critical`), never emoji-only — so it degrades to the plain label in a text-only sink and stays legible to a reader who can't see the glyph. `(basis: ratified marker set, 2026-07-15 — the maintainer asked for at-a-glance colour-coding of severity; the red→blue→white ramp mirrors the scale's own high→low order, and pairing glyph-with-word keeps it accessible and sink-portable.)`

## The adjacent-level discriminators

Assign by walking down until a level fits; the boundary tests are what stop a finding sliding between two rungs:

- **critical vs high** — is the consequence *unrecoverable or a breach* on a reachable path? Critical. *Bounded and recoverable*? High. (blast radius + recoverability)
- **high vs medium** — does a *plausible real input* trigger it and did you *confirm the path is reachable*? High. Does it need an *edge* input, or is reachability *unconfirmed*? Medium. (input plausibility + reachability)
- **medium vs low** — can it produce a *wrong result*, now or as the code plausibly evolves? Medium. Is behavior *correct for all inputs* and only the form worse? Low. (this is the correctness/craft line — [separate-correctness-from-taste](separate-correctness-from-taste.md))
- **low vs info** — does a maintainer pay a *real cost* (a likely future bug, a genuine inefficiency, a name that misleads)? Low. Is *declining it reasonable*? Info. (actionability)

When two levels both seem to fit, the higher wins only if you can name the input or path that justifies it; absent that evidence, drop a level. A severity you cannot anchor to a concrete consequence is a confidence problem masquerading as severity — re-check it against [anchor-every-finding-to-evidence](anchor-every-finding-to-evidence.md).

## What this scale does *not* grade

This scale grades **correctness defects** (by consequence) and **craft findings** (by maintainer cost) — the two piles [separate-correctness-from-taste](separate-correctness-from-taste.md) defines. It does **not** grade **scope findings** (a bundled, unrelated change flagged per [respect-author-intent](respect-author-intent.md)): a scope finding states something is *outside* the reviewed change, so it has no consequence-in-the-change to place on any rung. Scope findings carry no severity — they are boundary notes delivered in their own section ([deliver-findings](../phases/06-deliver-findings.md)), out of the verdict tally. Do not reach for this scale to grade one; if a bundled change is itself *wrong*, that is an ordinary correctness finding on that change, graded here like any other.
