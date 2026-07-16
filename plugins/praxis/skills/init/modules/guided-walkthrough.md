# guided-walkthrough (`--guide`)

Activated by `--guide`, referenced from [resolve-tools](../phases/02-resolve-tools.md).

The base run takes the default posture: propose inferred values for one-shot confirmation, ask only the gaps ([confirm-dont-assume-defaults](../rules/confirm-dont-assume-defaults.md)). This module raises the interaction to maximum — explain every slot and re-confirm even what the environment settled — for a first-time setup, or a user who wants to review and override every call rather than accept inferences. Deletion test: remove it and init still runs and configures every slot at the default posture; the added explanation and re-confirmation of derivable fills is what the flag turns on.

## The delta

- **Explain before asking.** For each slot, state what the capability is for and what its options mean (reading the menu from the template, never reciting products in prose — [capability-first-then-provider](../rules/capability-first-then-provider.md)) before resolving it, so a user new to the config model can choose deliberately.
- **Re-confirm even the derivable fills.** This is the `--guide` column of the posture matrix: a *derivable* field that the default posture would pre-fill for a glance is instead presented for explicit confirmation, so an inferred provider can be reviewed and overridden, not just accepted. *Suggestive* and *absent* fields are asked as they are at the default posture.
- **It never skips.** Unlike `--degrade`, a gap under `--guide` is asked, not disabled — the whole point is maximal user involvement.

`--guide` and `--degrade` pull in opposite directions (maximize vs. avoid user involvement); passing both is contradictory — the run should reject the combination and ask which posture the user meant rather than silently picking one.
