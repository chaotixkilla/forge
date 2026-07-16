The quality of a dogfood run is decided before it runs, by the scenarios. A smoke test — invoke the skill the obvious way, watch it succeed — proves only that the obvious way works, which the maintainer already knew and the static audits half-confirmed. The craft is choosing invocations that put the skill under the kind of stress a real run applies, so the run *finds* something. This rule is how to choose them; the pick-scenarios phase applies it.

## A scenario is a stress, not a demo

Frame each scenario by what it would *break*, not by what it would show. The question is never "how do I demonstrate this skill works?" but "what's the input that would expose it if it's wrong?" A scenario is **load-bearing** when it passes three tests, and a smoke test the moment it fails any one:

1. **Nameable defect.** You can state, before running, the specific plausible defect it would catch — not "something might be wrong" but "if the flag-gated module isn't actually wired to its flag, this invocation runs without it and never notices."
2. **Observable failure.** The defect, if present, produces a failure the log can point at — a stall, a wrong or missing file, a contradicted declaration — not a silent degradation no record would capture. A defect the run can't observe is a scenario wasted.
3. **Beyond the audits' reach.** No static audit would already have caught it. A scenario that proves "the frontmatter parses" or "a file gets written" re-proves what the contract audit certified; the run's budget belongs to what only running reveals — dispatch resolution, branch behavior, declared-versus-actual flag meaning.

Write the hunted defect into the scenario entry itself; a defect you can't write down means the scenario is a demo — drop it. One deliberate exception: the happy path earns a slot only when the common path itself is the suspect — the plugin's primary workflow has never once been walked end to end — and then the nameable defect is exactly that: "the primary chain is unexercised."

## Aim at the forks

A skill's decision forks are where its behavior is least uniform and therefore least exercised by habit. Every case-split in a phase — "if X do this, else that" — is two scenarios, and the maintainer has almost certainly hand-run the first branch far more than the second. Aim at the branch that's reached for least: the error path, the already-exists path, the empty-input path, the second provider. Forks are where skills rot, because the common branch gets all the manual testing and the rare branch gets none.

For example, dogfooding a component-adder: the common scenario adds a standalone rule (no wiring, just a file). The fork worth picking is adding a flag-activated module to a skill with no flags yet — because that branch must produce *two* coupled things, the module body and its activating flag, and the failure mode (writing one without the other) is exactly what a downstream contract check exists to catch. Picking the fork turns the dogfood into a real test of a relationship; picking the common branch tests a file write.

## Weight by surface area

When choosing which skills to dogfood at all, spend the budget on the ones with the most ways to be wrong:

- **Flag count.** Each flag is a behavior that can fail to fire, fire when it shouldn't, or contradict its declared meaning. More flags, more drift surface.
- **Slot spread.** A skill with phases *and* rules *and* a flag-gated module has more seams than one with phases alone — and seams are where wiring breaks.
- **External touches.** A skill that names a capability resolving to a configured backend can fail at the dispatch even when its prose is perfect. The run is the only thing that exercises that resolution; the audits can't.

A skill that is one linear phase chain with no flags and no external touch is the *least* worth a scenario — its static audit already told you nearly everything a run would, and the run adds little. Invert the instinct to start with the simple skill: start with the tangled one.

## Under `--self`, aim reflexively

When the kit dogfoods itself, prefer the skills whose subject is *skills* — the authoring and audit skills — because the entire self-hosting claim rests on them. If the kit's own skeleton-layer can't lay out a skill in the kit, or the kit's own audit can't audit the kit, self-hosting is a slogan. The reflexive scenarios that prove the most are the ones where the kit operates on its own kind.

## Sufficiency — what the set licenses the report to claim

A dogfood verdict is scoped by its scenarios; sufficiency is relative to the claim, never absolute. The floor, per claim:

- **To conclude anything at all:** every scenario in the set passed the load-bearing test above. A set of demos concludes nothing the audits didn't — however smoothly it ran.
- **To claim a *skill* runs cold:** the set covers each decision fork that skill's phases contain, or the report names the untaken forks as coverage gaps. "Runs cold," silently scoped to the one branch that happened to be walked, is exactly the lie dogfooding exists to catch.
- **To claim the *plugin* works end-to-end:** at least one scenario chains the plugin's primary workflow start to finish, plus one scenario at the highest-risk fork of each skill carrying two or more surface-area signals (flags, slot spread, external touches). Anything narrower, and the verdict must name the paths walked instead of claiming the plugin.

The scenario *count* is deliberately open — pinning one would be false precision, because plugin pools range from two skills to twenty and the floor above scales with the pool while a number wouldn't. Few and sharp still beats many and shallow: three scenarios that each hit a distinct fork outrank ten that re-walk one path, and past roughly six the challenge phase's full read of every log starts degrading to a skim.

## Keep the set closed

Close the set before running: it is the scenario list, fixed, and the run phases execute exactly it. Closing the set is what keeps a reflexive `--self` run from recursing without end — a scenario that would invoke the dogfood skill itself is recorded as a coverage note, never folded into the live set. A new scenario discovered mid-run is a finding for the report, not an addition to the current pass.

Anti-pattern: picking scenarios by setup cost. The easiest skill to invoke is usually the one least worth dogfooding, and the scenario you can stand up in one line is usually the happy path. Choose by likelihood of breakage, then pay the setup cost the strong scenario demands.
