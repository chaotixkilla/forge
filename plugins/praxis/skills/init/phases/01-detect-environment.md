## Anchor on the template shape first

Before detecting anything, read the shipped `config.template.json` (at `${CLAUDE_PLUGIN_ROOT}/config.template.json`). It is the **canonical shape init fills** — the seven capability slots (vcs, ci, knowledge, artifacts, project-management, communication, telemetry), the `me` / `teams` / `team[]` roster keys, and the schema `version`. Fill this shape; invent no keys, drop none, and carry the version through unchanged. `(basis: maintainer, 2026-07-05)` The slot set you read here is the checklist detection maps signals onto.

## Scan the signals — statically, once

Sweep the signals already available, without probing live endpoints:

- **The working tree's version-control remote** — its configured host bears on the `vcs` slot: a recognized hosting host maps to exactly one provider ([capability-first-then-provider](../rules/capability-first-then-provider.md) governs how that maps without naming products in this prose). Reading the ambient remote needs no configured backend — it is like reading the local tree itself.
- **CI configuration present in the repository** — its presence signals the `ci` capability is in use; the specific provider follows from the configuration's form, matched against the template's `ci` option-strings (the candidate menu), not guessed here.
- **The harness's live backend connections** — connections the harness already holds can bear on `knowledge`, `artifacts`, `project-management`, or `communication`. A connection surfaces a *candidate* backend; which slot it fills — and whether the project wants it there — is not settled by its mere existence. Three rules make this convergent:
  - **Enumeration is best-effort and harness-specific.** Read whatever connections the harness exposes; the *mechanism* for listing them is the harness's, not named here. Where the executor cannot enumerate connections at all, treat live-connection signals as **absent** and let the walkthrough ask — never block detection on it.
  - **Presence is the signal, not authorization.** A connection counts whether or not it is currently authenticated: its presence makes the provider a *suggestive* candidate. The authorization state feeds only the credential decision ([route-secrets-to-userconfig](../rules/route-secrets-to-userconfig.md)), not the provider's tier.
  - **A connection may be a candidate for more than one slot, and is offered per-slot.** One backend can be proposed for `knowledge` *and* `artifacts` *and* `project-management` independently — the user confirms each slot separately. A connection that maps to **none** of the seven capabilities is not a signal — drop it, don't try to place it.

**Static, not probed.** Read configured state — the remote, repository files, the harness's held connections — but do not open a live handshake, ping an endpoint, or authenticate to confirm a backend is reachable. Detection only *proposes* values the user confirms, and reachability is verified lazily when a skill first uses the backend, so a probe's side effects and latency buy nothing here. `(basis: derived from the lazy-gate stance)`

## Grade each signal, then stage it — commit nothing

For every signal found, assign its strength tier — **derivable**, **suggestive**, or **absent** — by the test in [infer-before-asking](../rules/infer-before-asking.md): a remote host that resolves to a single provider is *derivable*; a live connection that could fill more than one slot is *suggestive*; a slot no signal touches (commonly telemetry, and always the team roster) is *absent* and named as such so the next phases know to ask. The grade travels with the proposal — it is what [resolve-tools](02-resolve-tools.md) and [resolve-team](03-resolve-team.md) read to decide, per the run's posture, whether to pre-fill, propose, ask, or skip ([confirm-dont-assume-defaults](../rules/confirm-dont-assume-defaults.md)).

The `transport` field is deliberately *not* scanned here — it has no environment signal of its own, so it is resolved downstream from the chosen provider's *reach* (a port adapter for a port-backed provider, or the explorer/backend nature for knowledge or a local root) in [resolve-tools](02-resolve-tools.md), not graded in this pass.

This phase **stages, it does not write**: it produces a set of graded per-field proposals and a list of the slots left untouched, and hands both forward. Nothing is committed to the config here — committing, and confirming, is the work of the phases that follow. (When the run is scoped to a single capability via `--phase`/`init:<cap>`, detection narrows to just that slot's signals — see [single-phase](../modules/single-phase.md).)
