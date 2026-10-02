# Orient in the code

The failure this phase prevents is the change that is locally sensible and globally wrong — a new helper beside an existing one that already does the job, an error swallowed where the module propagates, a name in a style the file doesn't use.

## Consume the driving artifact

develop is artifact-driven by default: it expects a plan or a spec upstream. Which artifact you have decides how much is already decided for you:

- **A plan (`--from-plan=PATH`, the preferred entry).** A plan has already closed the solution space: it carries buildable units, their ordering, concrete interfaces, and a rollout. **Consume it as the build backbone** — take its units and sequence as phase 3's slices rather than re-deriving them, and trace each thing you build back to a plan decision. Do not silently re-litigate a decision the plan closed; if a plan decision proves unbuildable as written, surface that as a finding, don't quietly diverge.
- **A spec (`--from-spec=PATH`).** A spec fixes *what* must be true (requirements, acceptance criteria) but not *how*. **Derive the implementation order yourself**, and — the load-bearing difference from the plan branch — **flag each design decision the spec left open as you reach it**. Decide the *build-local* ones in-flight and record them; **route the plan-level ones out** (see the discriminator below) rather than smuggling a design in unremarked.
- **Neither (a direct request).** Frame the work inline: state the change in one sentence, its acceptance condition, and its touch-points. If framing surfaces an *unsettled plan-level decision* ([decide-or-route](../rules/decide-or-route.md)), do not absorb that work silently: recommend a `spec`/`plan` pass first and **end the run here, reporting the terminal outcome `blocked`** ([land-the-change](06-land-the-change.md)'s partition) with the next skill named — develop builds, it does not design the approach or set requirements, so a run that can't start without that work stops rather than building. A **trivial edit** — one with no unsettled design decision, where the approach is already determined — proceeds directly.

Sort every decision the change raises — at framing and during the build — by [decide-or-route](../rules/decide-or-route.md): decide it in-flight, route it to plan, or put it to the user.

## Locate the touch-points and read the neighborhood

Before you write, answer three questions about the code the change touches:

- **What is the local convention?** How this module names things, structures functions, handles errors, and how much indirection it tolerates — the standard the change must be a good citizen of ([match-the-surrounding-code](../../../craft/engineering/match-the-surrounding-code.md)).
- **What already exists?** The helper, pattern, or abstraction that already does part of this, so you extend rather than duplicate ([reuse-before-writing](../../../craft/engineering/reuse-before-writing.md)).
- **How does the data move?** The shape, validation, and mutation of the data across the boundaries the change touches, so the structure you reach for in phase 3 follows the data's realities, not the happy path (this reading feeds [choosing-the-right-data-structure](../../../craft/engineering/choosing-the-right-data-structure.md) and where the trust boundary sits for [parse-dont-validate](../../../craft/engineering/parse-dont-validate.md)).

**From a map.** When the caller hands you a map of the code the change touches — an understand run's result, its claims anchored and graded by certainty — start from it. What it establishes answers the questions above, and the entry point below, without a second read. Read only what it leaves open for this unit, the way a run without a map reads its neighborhood:

- a touch-point of this unit the map doesn't cover;
- a claim about code the unit will call, extend or rely on that the map carries only as *inferred* or *unverified* ([results-and-certainty](../../../craft/evidence/results-and-certainty.md)) — check it before building on it ([observation-over-inference](../../../craft/evidence/observation-over-inference.md));
- code an earlier unit of the same change has edited since the map was traced, which the map describes as it was;
- an external contract the unit leans on that the map doesn't establish — a library's, a framework's or a service's — read from its official documentation, as below.

**Without a map,** find where the change lives before reading whole files. Recruit the **code explorer** to locate the surfaces the change touches — by symbol, signature, and call-site — and the **repository explorer** for why they are the way they are (a prior attempt, a revert, a constraint in the history); recruit **official-documentation** when the change leans on an unfamiliar external contract. Without fan-out, do this reading yourself: locate by symbol and usage, read to the load-bearing detail, and trust what the code does over what names and comments claim. Recruit only as [fan-out-only-when-it-pays](../../gather/rules/fan-out-only-when-it-pays.md) allows. Read enough of the surrounding code to answer the three questions.

## Confirm the entry point and the seam

Name, concretely — from the map where it names one — the entry point through which the finished change becomes reachable — the caller, route, command, or event that will exercise it — and the seam where the new code attaches. This is what phase 4 will wire up and what "integrated / reachable" in the [definition of done](../rules/definition-of-done.md) is checked against; identifying it now keeps you from building a unit that is correct and orphaned. If no reachable entry point exists yet, that is itself the first thing to build, and it belongs in the slice plan.

**Grounded enough to start** is reached when you can state, in a sentence each: where the change lands, the convention it must match, what it reuses, and the entry point that makes it reachable. (Deliberately open: the *depth* of reading is left to executor judgment against the change's blast radius — a one-file fix needs the one file's neighborhood; a cross-cutting change needs the seam on every side. Pinning a fixed reading depth would be false precision.) The output of this phase is that grounding plus the slice plan phase 3 will build — carried forward, not re-derived.
