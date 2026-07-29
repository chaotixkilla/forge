# draft-only (`--draft`)

Activated by `--draft`, referenced from [deliver-and-route](../phases/07-deliver-and-route.md).

Base behavior: [deliver-and-route](../phases/07-deliver-and-route.md) routes the finished artifact to its resolved sink (returning it, and — under `--notify`/`--publish` — posting or publishing it). This module holds that: it stops before external routing and returns the content as an unsent draft for review. Deletion test: remove it and deliver-and-route routes normally; the flag adds a "hold before delivery" gate the base run doesn't have — so it is a module.

## The delta — hold delivery, return for review

Stop after [tighten-and-verify](../phases/06-tighten-and-verify.md), and return the finished content **marked as an unsent draft**, with a note of where it *would* have gone (the resolved form, channel, and any `--notify`/`--publish` targets). The point of `--draft` is "let me see it before anything happens," so it is authored to the same bar as a delivered artifact — clean-export applied, ask explicit, tier-pitched — it simply isn't sent. A draft returned half-finished ("I'll tighten it if you approve") defeats the purpose: the reviewer can't judge what they can't see finished.

## Precedence — `--draft` wins over delivery

`--draft` **overrides** the delivery flags: if `--notify` or `--publish` are also present, they are **held, not fired** — recorded as intended-but-suppressed so the user knows what would happen on approval, but nothing is posted or published. This is the one interaction that isn't additive: where `--notify` and `--publish` compose (publish then announce), `--draft` gates both off. Nothing this module governs reaches a port — [notify-targets](notify-targets.md) and [publish-output](publish-output.md) both check for `--draft` and stand down.

## Prerequisite and degrade

`--draft` reaches no backend — it is the one delivery-mode flag that is purely local — so it has no prerequisite and cannot fail on availability. There is nothing to degrade: returning the draft is ambient, exactly as the base return is.
