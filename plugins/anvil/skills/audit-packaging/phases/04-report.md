An audit's value is realized only when its findings reach the maintainer in a form they can act on. The boundary work is done; this phase delivers it. A packaging leak is high-stakes — it ships maintainer tooling or secrets to consumers — so the report must be precise enough to fix from directly: not "boundary issues found," but *this file, on the wrong side, belongs there*.

## Shape the report by `--report`

Default to **inline** prose returned to the caller: a short verdict line, then the findings most-dangerous-first. When `--report=artifact`, render the same content as a structured page (or a local file) instead of prose — use the artifact form when the finding set is large enough that a scannable, navigable layout beats a wall of inline text, or when the maintainer wants something to keep alongside a release. The findings are identical across formats; only the presentation changes. Never let the format choice alter which findings you surface or their order.

## What each finding must carry

Make every finding self-contained and fixable without re-running the audit:

- **The file** — its path, and which published source path it falls under (the thing that puts it in shipping scope).
- **The violation class** — authoring-only inside a shipping tree, the authoring plane nested in a source path, an unpublished plugin present in the catalog, or a catalog-integrity defect (a dangling entry, overlapping or widened source paths, a publishable plugin wrongly absent).
- **Why it is a leak** — tie it to the install mechanic: this file copies to every consumer on install because the source directory ships whole, with no per-file exclude. The "why" is what stops a maintainer from dismissing it.
- **Where it belongs** — the concrete destination across the boundary: the authoring/notes plane, the tooling area, or (for a catalog leak) removal of the manifest entry. A finding without a destination is a complaint, not a fix.

Assign severity by one rubric — what the next install does with the defect — then order most severe first, never by walk order:

- **Critical** — the install delivers what must never reach a consumer: a populated or secret-bearing config inside a source path, or an unpublished plugin present in the catalog (unreleased work made installable). Exposure or premature release, not recoverable once shipped.
- **High** — the install ships the making-of apparatus, or the frontier itself is mis-drawn: maintainer tooling or the design plane inside a source path; a widened, overlapping, or dangling source path (the wrong *set* of files ships regardless of per-file verdicts).
- **Low** — inert spillover and gaps: a stray contributor doc or fixture that exposes nothing sensitive and misleads no run; a publishable plugin wrongly absent from the catalog (nothing wrong ships — it just isn't shipping yet).

Ties inside a tier break by how much crosses the line: a mis-drawn path that drags a whole plane outranks a single stray file.

Emit each finding in one shape, so two runs of this audit read identically:

```
<severity> · <violation class> · <path> (under <source path>) → belongs: <destination>
```

## Report a clean boundary as a real result

If both invariants held and the catalog is integral, say so plainly — "boundary clean: every published plugin ships only consumer-facing files; the design plane stays outside all source paths, and every unpublished plugin stays out of the catalog." A clean audit is a finding too, and the maintainer needs the affirmative signal before a release. Do not invent borderline nits to look thorough; a clean report that names exactly what was checked is more trustworthy than a padded one.

## With `--fix` — propose, scoped to relocation

`--fix` proposes corrections rather than only reporting them. The correction for a packaging leak is almost always a **relocation across the boundary**: move the authoring-only file out of the source path to where it belongs, or remove the offending catalog entry for an unpublished plugin. Propose the exact move per finding — from-path to to-path. Crucially, the fix is never "exclude the file from the package": the install model has no per-file exclude, so the only real remedy is to get the file physically outside the shipping tree. Proposing an exclude would teach a mechanism that does not exist.

Treat `--fix` as a proposal the maintainer approves, not a silent rewrite — a misjudged relocation can move a file a consumer actually needed, and moving files reshapes the repo. Present the moves, let the maintainer confirm. If a finding was *uncertain* and only cleared by the critic into a real violation, say so in its fix proposal, so the maintainer can sanity-check the borderline call before any file moves.
