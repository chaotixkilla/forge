# init — usage

Detect and write the per-project praxis config — the `tools` map and `team` roster every other praxis skill reads to know which backends to talk to and who owns what.

## When to use
- Bootstrapping praxis in a new project: no `.claude/praxis.json` exists yet and you need one before any config-bearing skill can run.
- Onboarding a repo whose tooling is discoverable from the environment (the version-control remote, live backend connections) — let inference do the first draft, confirm the rest.
- Adding or correcting a single section after the fact (a new team member, a switched knowledge backend) — target it with `--phase` instead of rewriting the whole file.
- Auditing what config *would* be written before committing to it (`--dry-run`).

## Not for / use instead
- Changing harness settings, permissions, hooks, or env vars → that is the CLI's own config, not praxis config; this skill only writes `praxis.json`.
- Producing or filing a document into `tools.artifacts` → publish-artifact. init only records *where* artifacts go; it never writes one.
- Reading knowledge or prior art out of `tools.knowledge` → understand / deep-research. init only records the connection; it does not fetch through it.
- Any downstream engineering step (spec, plan, develop, review, …) → those *consume* the config init produces; run init once first, then reach for them.

## Examples
`init` — full run: load the template shape, infer what it can, walk the user through the rest, write `.claude/praxis.json`.
`--phase=tools` — configure only the `tools` map (per-category provider + transport + connection), leave the roster untouched. Named-section form.
`--phase=vcs` — configure only the `tools.vcs` slot, merging over the existing file and leaving the other slots and the version untouched. Capability-name form; this is the target every sibling skill's `guide via init:vcs` (and `init:knowledge`, `init:artifacts`, …) resolves to.
`--phase=3` — run only the 3rd phase (resolve-team) in isolation. Ordinal form; the ordinal indexes the phases in SKILL.md run order (1 detect-environment, 2 resolve-tools, 3 resolve-team, 4 write-and-validate).
`--guide` — walk the user through every section even where inference would have answered; use when you want to review/override inferred defaults rather than accept them.
`--degrade` — fill only what is inferable and disable the rest (writing `provider: null`, which the downstream gate reads as deliberately-unconfigured); use in non-interactive/automated runs where prompting the user is impossible. Produces a valid but narrower config, never one full of placeholders.
`--dry-run` — compute the full config and show it, but write nothing; pair with `--guide` to preview an interactive result or with `--degrade` to see how much a headless run could fill.
`--phase=team --dry-run` — preview just the roster section without touching the file.

## Gotchas
- Secrets never land in the file. Any tool needing a token gets a `secret_ref` pointer; the actual value goes in the harness userConfig. If you find yourself pasting a token into `praxis.json`, stop.
- Output shape is fixed by the shipped template: `version`, `tools` (vcs, ci, knowledge, artifacts, project_mgmt, communication, telemetry), `me`, `teams`, `team[]`. init preserves that shape and version — it fills slots, it does not invent new keys.
- `--degrade` and `--guide` pull in opposite directions: `--degrade` avoids the user, `--guide` maximizes user involvement. Passing both is contradictory — pick the interaction posture you actually want.
- Inference is a proposal, not a commitment: the version-control remote suggests the `tools.vcs` provider and a live backend connection suggests a backend, but init still surfaces these for confirmation unless `--degrade` told it to run headless.
- This skill has no `config_requires` — it is the bootstrap that *creates* the config every other praxis skill gates on. Run it before you expect anything else to resolve its prerequisites.
- Re-running is safe for targeted edits via `--phase`: a scoped run merges over the existing file, resolving only the targeted section and leaving the other slots and the version untouched. A full `init` refills the whole file; use `--dry-run` first if you are unsure what an existing config would lose.
