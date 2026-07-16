---
name: develop
description: Implement work to a finished, integrated standard — ground it in the code, stand up the tightest per-slice verify loop, build in verified slices while applying the in-the-moment craft-rule library, wire it into the running system, self-review as a hostile reader, and land to a clean, committable local state. Drives from a plan or spec; hands off to review / integrate, not to production.
metadata:
  flags:
    --from-plan=<path>: consume an existing plan's buildable units and ordering as the build backbone (orient's preferred driving artifact)
    --from-spec=<path>: drive the build from a spec — derive the implementation order and flag the design decisions the spec left open as you hit them
    --until=<condition>: halt at a named milestone (a slice, a phase, first-green, first-red) and report state instead of carrying the change to landing
    --lens=<value>: bias the whole build toward a stated concern (e.g. performance, accessibility, security) so it shapes choices in every phase, not just review
    --checkpoint-commit: commit locally at each verified-slice boundary so progress is recoverable and history reads as the build's slices
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

develop owns no backend of its own, and needs none: committing (at landing / `--checkpoint-commit`) is **local, ambient git** — no configured backend, the same way develop reads the working tree — and develop pushes nothing to a host (it hands the hosted landing to `integrate`). So it touches no external capability at all and declares no `config_requires`. `--lens=<value>` reshapes every phase toward a stated concern: see [modules/lens.md](modules/lens.md). `--until=<condition>` halts at a named milestone and reports state instead of landing: see [modules/until-checkpoint.md](modules/until-checkpoint.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft-library where it applies, and phase 6 is gated on the definition of done.

1. Orient in the code: ground the driving plan/spec in the real codebase — locate the touch-points, read the surrounding code, and confirm the entry point before writing anything  — see [phases/01-orient-in-the-code.md](phases/01-orient-in-the-code.md)
2. Establish the feedback loop: stand up the tightest run/test loop available so every change is checkable in seconds, not at the end  — see [phases/02-establish-the-feedback-loop.md](phases/02-establish-the-feedback-loop.md)
3. Build in verified slices: implement one independently-runnable unit at a time, proving each green before the next, applying the craft-rule library as you write  — see [phases/03-build-in-verified-slices.md](phases/03-build-in-verified-slices.md)
4. Integrate and wire up: connect the new units to their callers, config, and boundaries so the change is actually reachable in the running system  — see [phases/04-integrate-and-wire-up.md](phases/04-integrate-and-wire-up.md)
5. Self-review the diff: read your own change as a hostile reviewer — scope creep, leftovers, dead code, missed edge cases — before handing off  — see [phases/05-self-review-the-diff.md](phases/05-self-review-the-diff.md)
6. Land the change: bring the working tree to a clean, committable state, run the full local check, and confirm the change meets the definition of done  — see [phases/06-land-the-change.md](phases/06-land-the-change.md)
