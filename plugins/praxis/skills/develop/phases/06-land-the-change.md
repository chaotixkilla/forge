# Land the change

## Run the full local check

Run the repo's **full local check** — the set the repo itself gates on (its CI / pre-commit / documented "run everything" target); where the repo defines no single gate, that is the build + the test suite it runs + any lint/type gate it *enforces* (not optional style checks a reader can ignore) — over the complete change, not just the last slice's scope. A change whose slices were each green but whose whole fails is not landed; the full check is what catches the cross-slice interaction the per-slice loop couldn't see. If `--lens` was set, its check is part of this full green too. A whole-change failure here whose cause **is** in the change's own diff is more work to do before landing; one whose cause **isn't** localizable to the change in hand (a cross-slice or pre-existing interaction you can't pin to your lines) is a **blocked** outcome — a `debug` hand-off, not a signal to keep reworking inside develop ([verified-slice](../rules/verified-slice.md)'s fault-localization discriminator applies to the whole-change check too).

## Confirm the definition of done

Landing is gated on the [definition of done](../rules/definition-of-done.md): walk its five criteria, each against its own test; a change that fails any one is not done. Any leftover debris found now is a *coherent* failure to close before landing ([leave-no-debris](../../../craft/engineering/leave-no-debris.md)).

## Commit locally to a clean state

Bringing the tree to a **clean, committable state** — no half-staged work, no stray files (a local backend's task documentation isn't one: it stays out of the change), the change coherent — and then **recording the commit** are both **local, ambient git**: they need no configured backend, exactly as develop reads the working tree, and they always happen. They are not delegated to the vcs port, which is host-only, so nothing here degrades. Commit the change, its message by [commits-tell-the-why](../../../craft/engineering/commits-tell-the-why.md) and the commit by the repo's policy ([honor-commit-policy](../../../craft/engineering/honor-commit-policy.md)) (and, with `--checkpoint-commit`, the per-slice commits already recorded — see [checkpoint-commit](../modules/checkpoint-commit.md), which carries the commit-granularity fork: per-slice checkpoints vs a squashed single commit). Pushing, opening a PR, merging and shipping are hosted work, deliberately outside develop: they belong to whoever delivers the change. `(basis: maintainer, 2026-07-11)`

## Report the terminal outcome

Every develop run ends in exactly one of three outcomes — state which, so a reader can tell a paused run (resume it) from a blocked one (re-plan, or route to debug):

- **landed** — the definition of done is met and the change is committed to a clean local state. The normal terminal state.
- **checkpointed** — the run stopped short of done *by request* (a `--until` condition — a slice, a phase, first-green — deliberately reached) to report state. Not a failure; a requested pause. (see [until-checkpoint](../modules/until-checkpoint.md))
- **blocked** — the run **cannot proceed to done within develop**. That rationale defines the outcome, not a list of triggers, so a can't-proceed state named nowhere here still lands in it. The known causes: a red state whose cause is not localizable to the change in hand and needs `debug` (a per-slice red — [verified-slice](../rules/verified-slice.md) — *or* a whole-change full-check failure at landing that isn't in the diff); an upstream plan/spec decision that proved unbuildable as written; or work that isn't develop's to start yet (the [orient](01-orient-in-the-code.md) direct-request bailout that recommends a `spec`/`plan` pass first). The run stops and hands off with the blocker and its next-owner named. `--until=red` is the requested-stop form of reaching a red state, and it lands here, not in checkpointed: a stop that is both requested and an inability takes the inability's label.

`(basis: maintainer, 2026-07-10)`

A landed change is ready for an independent review and for landing.

Alongside the outcome, a **landed** run owes three things the outcome word does not carry, because the reader is deciding whether to review it, ship it, or work near it:

- **What a user of the software will notice**, or plainly that nothing will. A change with no observable surface is the common case and the none-case is stated, not omitted.
- **What another developer must know** — a contract, signature, error mode, default, config key, invariant, or process step that moved, such that correct code or a correct assumption elsewhere is now wrong. This is the outward face of the caller reading [integrate-and-wire-up](04-integrate-and-wire-up.md) already did; report it rather than re-deriving it.
- **Where to start reading**, capped at the files that carry the change's meaning. Every touched file is not a reading order, and paths resolve in the tree the reader has — the linked worktree's own root when the run is inside one.

A **checkpointed** or **blocked** run owes the first two only where it changed something observable before stopping, and owes the third always — a reader picking up a paused build needs the entry point more than a finished one does. `(basis: derived from review's brief)`

## Before it goes out, read it as its reader

Put the finished report through [deliver-at-the-readers-register](../../../craft/writing/deliver-at-the-readers-register.md) before delivering it, applying its honesty floor item by item from the rule, not from memory.

**And a visual where prose would carry it worse:** where the report describes a *structure* — a shape, a flow, a set of relationships — show it rather than describe it, per `output.diagrams` ([report-style-settings](../../init/rules/report-style-settings.md)) and [when-a-visual-is-owed](../../../craft/writing/when-a-visual-is-owed.md), which decides whether one is owed.
