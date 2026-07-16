# Infer before asking

The expensive failure of a setup skill is interrogation: a run that fires a dozen questions at the user when half the answers were sitting in the environment. Every question init asks that the project could have answered is a question that erodes the "let inference do the first draft" promise the skill is built on. This rule is the discipline of exhausting the cheap signals before reaching for the user — and, just as important, of grading how strong each signal is, because a signal that *determines* a value and a signal that merely *hints* at one must be treated differently downstream.

## Climb the cost ladder, cheapest rung first

Fill each field from the cheapest source that can answer it, and escalate a rung only when the current one comes up empty:

1. **Already in context** — facts about the project you already hold from the session (a provider the user just named, a path already established). Free.
2. **The environment, read statically** — the working tree's version-control remote, CI configuration present in the repository, and the harness's live backend connections. One pass over signals already on disk or already held by the harness; no live probe (the derivation is in [detect-environment](../phases/01-detect-environment.md)).
3. **The user** — the only rung that interrupts a human. Reached last, and only for what the first two genuinely could not resolve.

A field escalates to the user on exactly one trigger: the cheaper rungs returned nothing that bears on it, *or* what they returned only *narrows* the value without fixing it. Never ask what rung 1 or 2 already answered.

## Grade the signal's strength — the three-tier scale

Detection does not just find signals; it grades how much each one settles. The grade is read off the signal's determinism, never guessed — a model's hunch about the likely provider is not a signal, it is the anecdote the sourcing discipline forbids. Every detected field lands in exactly one tier:

`(basis: ratified by the maintainer, 2026-07-05. The three tiers and their boundary tests are init's derivation of "how strong is strong enough to fill" — there is no external authority for a config-detection confidence ladder the way there is for, say, severity, so the rung boundaries and anchors are the maintainer's ratified house standard. The scale drives the posture matrix in [confirm-dont-assume-defaults](confirm-dont-assume-defaults.md); the two were ratified together.)`

- **derivable** — a single environment signal *uniquely* determines the field's value, and reading the signal is deterministic (two cold runs read it the same). Exactly one value is consistent with the signal.
  - *Anchor (top of scale):* the working tree's version-control remote resolves to a recognized hosting provider — the remote's host maps to exactly one provider, so the `vcs.provider` is fixed by the environment, no human needed to know it.
- **suggestive** — a signal *narrows* the field but a human choice remains: the signal is consistent with more than one value, or it surfaces a resource without fixing which slot it fills or whether to use it at all.
  - *Anchor (middle):* the harness holds a live backend connection, but it could serve knowledge, artifacts, *or* project-management — which capability it fills, and whether the project wants it there, is the user's call; the connection's existence is real, its assignment is not.
- **absent** — no environment signal bears on the field; only the user holds the answer.
  - *Anchor (bottom of scale):* who owns which area of the codebase and who is a designated reviewer — a team decision no repository state encodes, and a secret value, which the environment must never surface into a config.

## The adjacent-tier discriminators

- **derivable vs suggestive** — does the signal admit *exactly one* value (derivable) or *more than one, or an unresolved slot assignment* (suggestive)? A recognized remote host → one provider is derivable; an unrecognized/self-hosted host, or a connection that could fill several slots, is suggestive. When you cannot name the single value the signal forces, it is not derivable — drop a tier.
- **suggestive vs absent** — does *any* signal bear on the field (suggestive) or *none* (absent)? If nothing on disk or in the connection registry constrains it, it is absent, and the user is the only source.

The tier is not the action — a derivable field is still surfaced for confirmation under the default posture, and a suggestive one is still skipped under `--degrade`. The tier feeds the posture matrix in [confirm-dont-assume-defaults](confirm-dont-assume-defaults.md), which is where a tier becomes an auto-fill, a proposal, a question, or a skip. Keep the two concerns separate: this rule decides *how strong the signal is*; that rule decides *what to do about it* given the run's posture.
