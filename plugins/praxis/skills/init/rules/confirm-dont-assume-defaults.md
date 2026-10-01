# Confirm, don't assume defaults

A wrong value written silently is worse than a question asked: the question costs a moment, the wrong value costs a debugging session downstream when a skill talks to the wrong backend and no one remembers init chose it.

## The default posture: propose every inference, ask every gap

With neither `--guide` nor `--degrade` set — the common path — init takes the middle posture: **it proposes every inferred value pre-filled for one-shot confirmation, and asks openly for every field the environment left as a gap.** It does not silently commit an inference, and it does not re-interrogate what the environment already answered (that is the failure [infer-before-asking](infer-before-asking.md) prevents). "Confirm this: `vcs.provider` = the provider your remote host points to — press through to accept" is the shape; a wrong inference is caught in the one glance it takes to reject, and a right one costs nothing.

`(basis: maintainer, 2026-07-05, for this default and the posture matrix below)`

## The posture matrix — signal strength × interaction mode

The action init takes on a field is the cross-product of the field's signal tier ([infer-before-asking](infer-before-asking.md)) and the run's interaction mode. This is the whole decision, pinned as a table:

| signal tier | default | `--guide` | `--degrade` |
|---|---|---|---|
| **derivable** | propose the value pre-filled, confirm in one glance | explain the options, then re-confirm even this | auto-fill silently |
| **suggestive** | propose as a question (the narrowed candidates) | explain the options, then ask | skip → write disabled |
| **absent** | ask openly | ask openly | skip → write disabled |

Read the columns as the three modes:

- **default** — propose-and-confirm, as above. Every field is seen by the user once; none is committed unseen, none is re-asked when the environment settled it.
- **`--guide`** ([guided-walkthrough](../modules/guided-walkthrough.md)) — the maximally-interactive mode: explain each slot's purpose and options and re-confirm *even the derivable inferences*, for a first-time setup or a user who wants to review every call. It never *skips* — a gap is asked, not disabled.
- **`--degrade`** ([degrade-gracefully](../modules/degrade-gracefully.md)) — the no-user mode: take the derivable fills silently and *skip* everything that would need the user, writing each skipped slot as deliberately-disabled (`"provider": null`) so it stays legible to the downstream gate. A degrade run never prompts; it produces a valid but narrower config.

A "skip" is never a silent omission — it is an explicit disabled marker the [write-and-validate](../phases/04-write-and-validate.md) step treats as a resolved (valid) slot, distinct from an unresolved placeholder.
