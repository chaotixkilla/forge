# --lens=<value> — build through a concern

`--lens=<value>` names a concern the whole build should be shaped by — `performance`, `accessibility`, `security`, `reliability`, `observability`, and the rest — so it drives choices *while the code is written*, not only when it is reviewed afterward. The point is placement in time: catching a performance or accessibility problem as the slice is built is cheap; catching it at review is a rework. Without the lens, these concerns are handled by whatever the change happens to need; with it, one concern is elevated to shape every phase.

## The lens values

The value is a concern drawn from the shared analytical-lens vocabulary the flag axis defines (`performance`, `security`, `correctness`, `concurrency`, `reliability`, `cost`, `privacy`, `accessibility`, `observability`, `testability`, `compatibility`, `data-integrity`, `scalability`, … and the free-form escape hatch for one the list doesn't name). develop does not re-define that vocabulary — it consumes it. `(basis: routed to maintainer, ratified 2026-07-10 — the lens vocabulary is a cross-skill concern; --lens stays develop-local for now, sourcing its values from the shared analytical-lens taxonomy rather than re-authoring them, and a shared cross-skill lens module/skill is recorded as a future extraction to be maintainer-directed when a second consumer makes the sharing concrete — the same way `gather` and the `vcs` port were extracted only once sharing was real. Until then, re-authoring a lens vocabulary per skill is the risk this note guards against.)`

## How a lens reshapes each phase

A lens is not "bias toward it" — it attaches a concrete obligation to each phase. The mechanism, phase by phase:

| Phase | What the lens changes |
|---|---|
| **1 · orient** | Additionally locate the lens's *touchpoints* in the code — the surfaces where this concern lives or breaks (perf → hot paths, allocations, query sites; security → trust boundaries and sinks; accessibility → the interaction/markup surfaces). |
| **2 · feedback-loop** | Add the lens's own fast check to the loop, so the concern is *verified per slice*, not deferred (perf → a benchmark/profile; a11y → contrast/keyboard/label check; security → the relevant guard test). This is the load-bearing change: the lens becomes part of "green." |
| **3 · build-in-slices** | Apply the lens's craft as you write each slice (perf → avoid the N+1 / the per-item allocation now; security → validate-and-escape at the boundary now; a11y → semantic markup and labels as the component is built). |
| **4 · integrate-and-wire-up** | Check the lens holds across the wiring, not just within a unit (perf → no per-call round-trip introduced by the integration; reliability → the new external call has a timeout/retry story; security → the guard is on the actually-reachable path). |
| **5 · self-review** | Run a dedicated hostile pass *in the lens* — this is where `--lens` most sharpens self-review: read the whole diff once asking only "how does this fail on the lens's terms?" |
| **6 · land** | The lens's check is part of the full-green landing bar and of the [definition of done](../rules/definition-of-done.md)'s *verified-green* criterion — a change that isn't green on its declared lens is not done. |

The reshaping *method* above is pinned; the specific concern is the open parameter (any value from the taxonomy). A lens raises a concern to first-class in every phase — it does not license scope creep: the change still does only what the task needs ([keep-the-diff-focused](../rules/change-hygiene/keep-the-diff-focused.md)), now done well on the named axis. Multiple concerns at once are review's `--lenses` territory; `--lens` here elevates *one* to shape the build. Deep, comprehensive treatment of a concern (a full security audit, a full performance investigation) is still the specialist skill's job — `--lens=security` builds security-consciously; it is not `security-review`.
