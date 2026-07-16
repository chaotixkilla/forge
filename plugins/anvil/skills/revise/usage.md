# revise — usage

Turn a batch of findings or maintainer feedback into the smallest, verified set of changes to an existing plugin: triage and dedup the batch, size each item to the least-invasive mechanism that resolves it, dispatch it to the engine that owns that fix, and re-verify the diff.

## When to use
- You have a **batch** of change-requests against a plugin — a dogfood report's ranked findings, a review/audit report, or plain maintainer feedback ("this is bloated," "the severity isn't scannable") — and you want them applied as a minimal, proportional diff rather than a pile of edits.
- The batch **spans more than one skill or more than one kind of fix** (some are one-word method pins, some need a new rule, some are just a missing citation). revise's value is sizing each to its own mechanism so a small finding gets a small change.
- You want the result **verified against what it touched** — the concern-matched critics and audits re-run on the diff — and reported as one auditable change set (applied / deferred / won't-do / dropped).

## Not for — use instead
- **Diagnosing or producing findings** → **dogfood**. revise is the *repair* plane; it consumes findings, it never generates them. Run dogfood first, then hand its report to revise.
- **Authoring or lifting the method of a single skill** → **codify** directly. For a batch that reduces to *one method lift into one skill*, revise degenerates to a direct codify call and adds nothing but ceremony — call codify. revise earns its keep only on a multi-skill, multi-mechanism batch.
- **Creating one known new component** (a rule, module, adapter, agent) → **add-component** directly.
- **Building a new skill or plugin, or splitting one** → **scaffold-skill** / **new-plugin**. revise *routes these out* as a recommendation (its heaviest tier); it never births structure itself.
- **Publishing a finished plugin** → **release**.

## Examples
`--plugin=praxis` — apply the pending batch of findings/feedback to praxis; interrogate for the batch if no source is given.
`--plugin=praxis --from=design/anvil/REVIEW-DOGFOOD-FINDINGS.md` — seed the batch from a findings report, then triage/size/dispatch it.
`--plugin=praxis --dry-run` — triage and size the whole batch and show the change set (each item's disposition, tier, and target engine) **without** writing anything or invoking any engine; the preview is explicitly unverified.

## Gotchas
- **It sizes down, never up.** Every item gets the *lowest* mechanism-tier that resolves it (wire it / dispatch to codify / dispatch to add-component / route structure out); climbing a tier needs a recorded reason. A one-word method pin never balloons into a new rule.
- **It authors nothing itself except wiring.** All method (defaults, scales, thin bodies, leaked-tool rephrasings) dispatches to **codify**; all new files to **add-component**; all structure routes out. revise's only direct edits are a missing citation link or an activating-flag declaration — and its own report.
- **`--dry-run` stops before any change.** It reports the sized plan and mutates nothing; because no diff exists, the preview is **unverified** — it does not run the verify pass.
- **It won't re-grade a finding's severity.** A dogfood grade is honored for ranking; intervention *size* is a separate axis. And it won't action coverage notes, demoted not-findings, "what worked" items, or preference-only findings — those are dropped or deferred in triage, with the reason recorded.
- **Single-skill single-plane batch? Don't reach for revise.** See "Not for" — call codify directly. revise assumes breadth; on a narrow batch it is pure overhead.
