The plugin now exists and has a seeded pool, but it is deliberately *not done* — it is born, not published. This final phase makes the boundary explicit so no one mistakes a freshly-scaffolded plugin for a released one, and points at what comes next. new-plugin stops at birth on purpose: publication is `release`'s job, and conflating the two is how unfinished plugins leak into the catalog.

## Report the new tree as a whole

Report the complete change set, not a fragment: the manifest, the slot folders, the README, every skill scaffolded into the pool, and — if the plugin is config-bearing — the config schema and the config-setup skill. The maintainer reviews the birth as one unit, so a partial list is worse than none. Anchor the report to the created paths under `plugins/<name>/` so the maintainer can walk the tree directly.

## State plainly that it is NOT in the catalog

Say it without hedging: the plugin is **not** in `marketplace.json` and is not installable by consumers. new-plugin never touched the catalog — that's `release`'s sole responsibility — so the plugin sits unpublished until someone runs the publication path deliberately. Spelling this out is what prevents a half-built plugin from being assumed live; the gap between "scaffolded" and "released" is a feature, the window in which the plugin gets its skills filled, its tools pushed into adapters, and its three audits passed.

## Point at the path forward — and stop early for `--unpublished`

Point at `release` as the next step *when the plugin is ready* — that is, once its skills are codified, its capability surface is backed by adapters, and it passes the kit's quality gate (tool-leaks, contract, packaging). Don't imply it's ready to release now; a just-born plugin rarely is.

For an `--unpublished` plugin, this is the end of the road for now by design. It was marked in-development to stay out of the catalog until it's built and released — so do **not** point it at `release` yet; instead confirm its unpublished posture and that it loads via the direct plugin-directory path rather than the marketplace. Pointing an unpublished plugin at release would invite exactly the publication its marking exists to forbid until it's ready; `release`'s own gate would block it, but the handoff should never suggest it in the first place.
