Require `--plugin`; without a named target there is nothing to measure, and inferring one from the working directory is how an audit silently reports on the wrong plugin. Resolve it to a directory under the marketplace's `plugins/`, and fail loudly if it isn't there.

Measurement is the script's job, not yours. Run it over the resolved plugin directory:

```
python3 <anvil>/scripts/measure_context.py <plugin-dir> --json
```

Read the JSON. It carries four things this phase needs: `always_resident_tokens` with the per-file `resident_parts` breakdown, a `skills` array with each skill's spine / usage / phases / rules / modules weights and its `no_flag_ceiling`, a ranked `hotspots` array with each file's direct citation count and fan-out ratio, and the `breaches` list — the subset that exceeded a budget from [context-budget](../rules/context-budget.md). Pass `--budget=<k=v,…>` through as the script's matching `--max-*` flags where the caller overrode one.

Do not re-derive any of these by hand, and do not adjust them. If a figure looks wrong, that is a finding about the script, not a number to correct in the report — say so plainly and stop, rather than substituting a hand count that no one can reproduce.

## What the layers mean, and which of them a reader actually pays

The numbers are only interpretable against the harness load model, so hold it explicitly while reading them:

- **Always resident.** The `name` + `description` of every skill and every agent, paid on every request whether or not anything is invoked. This is the only layer with no opt-out, so a token here is worth far more than a token anywhere else — and it is the layer a growing skill pool inflates silently, one description at a time.
- **The spine.** One `SKILL.md`, loaded on trigger. Its *ratio* — corpus governed per token of spine — is a virtue, not a cost: a high ratio means a thin index is steering a large body. Read it as a disclosure score.
- **The phases.** Every phase the spine cites, loaded when the executor works the step. On a no-flag run, treat all of them as paid.
- **The rules and everything transitive.** Reachable, not resident. This is where a ceiling comes from, and where judgment starts.
- **The modules.** Flag-gated, so they cost nothing by default. The script excludes them from the ceiling deliberately; do not add them back.

Two boundaries end a load path rather than extending it, and the script honors both: a citation to a **sibling skill's** `SKILL.md` is an *invocation* — that skill runs its own procedure in its own window, so you pay to read the spine and nothing beyond it — and a **recruited agent** runs in a forked context, so its body costs the caller nothing. A measurement that expanded through either would report every well-connected file as reaching the whole plugin, which is the failure mode that makes this kind of metric useless.

## Sanity-check the output against the tree before you build on it

The script trusts the filesystem, so a structural surprise shows up as a strange number rather than an error. Two checks, both cheap, both worth doing before any finding rests on the figures:

- **Does the skill count match the tree?** Compare the `skills` array against `ls` of the plugin's `skills/`. A skill missing from the measurement has no `SKILL.md` — a contract defect that belongs to [audit-contract](../../audit-contract/SKILL.md), and one you should route there rather than absorb here.
- **Is any ceiling implausibly small?** A skill reporting phases at zero either genuinely has none (a thin port — correct, and its ceiling should be roughly spine + usage) or its spine cites its phases in a form the resolver could not follow. The second case is a dangling-citation defect; hand it to `audit-contract` and note that this skill's figures are unreliable until it is fixed.

## What this phase hands forward

The layer table, the ranked hotspot list, and the breach list — untouched. Under `--skill`, keep the whole plugin's resident total (a per-skill view of an always-resident layer is meaningless) but carry forward only the named skill's ceiling and only the hotspots inside it. Everything else is context for the read, not subject matter for it.

A breach is not yet a finding. The script measures; the next two phases decide what the measurements mean, and a report that promotes a breach straight to a finding without the read has skipped the only part of this audit that requires judgment.
