# benchmark — usage

Run a change to a plugin's skills against the version before it, over the same scenarios several times each, grade both arms, and return a verdict: net improvement, hidden regression, or within noise — regressions first.

## When to use
- You've landed a revise batch large enough that regression risk is real — a change that repairs one scenario can quietly break another, and neither the static audits nor a single dogfood pass will see it. Reach for benchmark when you need *proof* the diff is a net improvement, not a plausible-looking trade you didn't notice.
- You're about to release and want the change vindicated against the version consumers already have, not just confirmed to run.
- This is the heavyweight tier you *opt into*, one rung above dogfood's cheaper single-pass "does it run?" proof — pay its cost when the stakes justify an A/B-with-repeats comparison, not as an always-on gate.

## Examples
`--plugin=<plugin>` — evaluate the working-tree change to the plugin against its pre-change baseline over freshly picked scenarios; the default, full comparison.
`--plugin=<plugin> --skill=<skill> --repeats=5` — narrow to the one skill you changed and run five times per arm for a tighter variance read when the delta looks close to the noise floor.
`--plugin=<plugin> --baseline=<ref>` — compare against an explicit baseline (a release point, an earlier revision) instead of the default pre-change tree.
`--plugin=<plugin> --scenarios=<ref>` — reuse a curated scenario set rather than picking fresh ones — the honest, repeatable path when you're comparing across successive iterations of the same change.
`--plugin=<plugin> --dry-run` — frame the comparison and print the run plan (resolved baseline, target skills, scenarios, repeats per arm); execute nothing.
`--plugin=<plugin> --report=artifact` — render the per-scenario comparison and verdict as a durable, scannable page instead of inline prose; delivery only, the verdict is identical either way.

## Gotchas
- It is the heavyweight, opt-in tier — directly invocable, the escalation revise can hand a large batch to, and a check to run by hand before a release when there is a prior version to beat. It is not a standing gate, and release does not auto-invoke it (a first release has no baseline to compare against); running it on every small edit spends far more than the change is worth.
- It needs a resolvable baseline or it stops. With no pre-change tree to fetch via the configured version-control capability and no `--baseline` override, there is nothing to compare against and the skill asks rather than inventing one.
- Both arms must see **identical** scenarios, or the delta is meaningless — a difference you can't attribute to the change is not evidence. If the scenario set can't be held fixed across the baseline and the changed arm, the comparison is void.
- Regressions are the headline. A net-positive average can hide a single scenario that got *worse*; the report surfaces regressions first and never lets a cheerful aggregate bury one. That per-scenario A/B catch is the whole reason the skill costs what it does.
- It reuses the kit rather than reinventing it: execution is delegated to dogfood (run once per arm over the same scenarios), and grading to the kit's own critics as the assertion library — benchmark itself owns only the decision method (how many repeats, how large a delta counts as real signal). It does not re-implement running skills or judging them.
