A run produces raw friction: stalls, assumptions, surprises, the critics' challenges. None of that is a finding yet. A finding is a defect stated so the maintainer can fix it — pinned to a file, attributable to the skill rather than the test, graded on a fixed ladder, and ranked by how much it matters. This rule is the craft of that conversion: how to read friction without over-reading it. The report phase applies it; get it wrong and the report is either noise (everything's a finding) or denial (nothing is).

## Separate the skill bug from the thin scenario

The first cut on every piece of friction: is this the *skill's* fault or the *scenario's*? Not every stall indicts the skill. A scenario built on a precondition the skill legitimately requires — and that the run simply failed to set up — produces a stall that's on the test, not the tool. Misattribute it and you'll send a clean skill back for a fix it doesn't need.

The discriminator is the skill's declared contract, with "declared" read against the loading model, not the tree. A precondition counts as declared only if a cold executor would have *loaded* it before hitting the stall: the frontmatter, `usage.md`, the SKILL.md body, an earlier-or-current phase, or a rule one of those cites. A precondition stated only in a later phase, or in a rule no phase cites, is undeclared for blame purposes — the executor never saw it, so the next cold run stalls exactly the same way. (In that case the finding may be mis-wiring rather than missing text: the statement exists but is stranded where nothing loads it.)

So: skill *states* the precondition somewhere the run had loaded, and the scenario ignored it — the friction is the scenario's; note it as a test gap and move on. Skill *assumes* a precondition it never states (or strands the statement) — the friction is the skill's, billed to the phase that relies on it. And one third party: a capability that fails to resolve is the *environment's* fault when the plugin ships wiring for the configured provider and the test setup simply isn't configured — record that as a run-environment note; it is the *plugin's* fault when the skill names a capability and no wiring the plugin ships could ever resolve it.

For example: a skill stalls because the subject tree wasn't in the shape it expected. If the skill's frontmatter or first phase declares that precondition, the dogfood scenario was thin — record "scenario didn't establish the declared starting state" and don't bill the skill. If the skill nowhere says it needs that shape, the finding is "skill assumes an unstated precondition." Read the contract — and check what would actually have loaded — before you assign blame.

## A reasonable guess is still a gap

Resist the pull to excuse an assumption because it was the *right* assumption. When a step left a choice open and the run filled it sensibly, the sensible fill is evidence of a gap, not its absence — the next executor might fill it differently, or worse. Demote every "I assumed the obvious default" back to "the skill doesn't state a default here." The same demotion applies to judgment calls: a grade or selection the run made confidently, under a bar the skill never pins, is a divergence waiting for the second run. The skill's correctness can't depend on the runner being reasonable; that's the whole premise of the cold-executor stance. A defensible guess is a finding wearing a disguise.

One exception, and only one: openness the skill *documents*. A step that leaves a call to executor judgment and records why on the page has made a decision, not left a gap. Undocumented openness is the defect; documented openness is a design.

## Grade on the pinned ladder

The report ranks, and ranking needs a scale two executors assign identically. Three grades, assigned by observable effect — never by feel (ladder from the kit's own dogfood record, with *blocker* added for the stalls a run can't declare its way past):

- **[blocker]** — a cold run cannot complete the step: no literal reading yields an action, and no declared assumption makes the next step actionable. The run provably halts.
- **[friction]** — the run completes, but only by guessing or diverging: a forced assumption, an open bar behind a judgment, a contract drift. Two cold runs finish with different-character results.
- **[nit]** — no behavioral effect: cosmetic, phrasing, layout. A cold run's output is identical with or without the fix.

The assignment test is the second cold run: ask what it does at this exact point. Halts → blocker. Proceeds, differently → friction. Proceeds, identically → nit.

## A finding is falsifiable, or it isn't finished

The bar that separates a clean finding from a vibe: a second reader, holding only the skill's files and the run log, could check the finding and agree or refute it. Operationally, a finding ships only when it carries all four parts:

1. **the defect** — one sentence stating what the skill fails to supply, or which declaration it contradicts;
2. **the pointer** — the owning file, plus the step, flag, or declaration within it;
3. **the evidence** — the log entry (stall, declared assumption, judgment divergence, drift) that shows the defect biting;
4. **the route** — the authoring skill that owns the repair.

Missing any part, it isn't a finding yet — keep reading the friction until all four exist or the item dissolves (some do: friction that can't produce a pointer and evidence is usually the scenario's or the environment's, not the skill's). "This was confusing to run" has zero of the four. "Phase 03 step 2 grades output as adequate with no bar — the log shows this run inventing one, so a second run invents another — route: the procedure-filling skill, to pin the bar or record why it stays open" has all four.

## Trace to the owning slot

Every finding resolves to a file, and the slot kind tells you which. This is the single mapping the report phase invokes rather than restating:

- Friction at an ordered step, or a stall/guess at a procedure step → a **phase** (cite the step and number).
- Friction at an unresolved decision, a fork the skill resolves by luck, or an open bar behind a judgment (a grade, threshold, or selection the skill demands but never pins) → the **rule** that should decide or carry it, or the phase step that demands the judgment, or the absence of one.
- Friction where behavior contradicts a declaration — a flag that doesn't behave as declared, a description that oversells the run → the **frontmatter** (the specific flag or the description).
- Friction where a named capability resolves to nothing → the **wiring** (dispatch/adapter), surfaced as a gap, never as a tool name.
- Friction where a flag-activated behavior never fired → the **flag↔module** seam.

If a finding doesn't resolve to a slot, it isn't finished — keep reading until it does. "The skill feels unreliable" hasn't been read yet; "phase 03 takes the success branch with no defined behavior for the empty-input branch" has.

## Rank by bite

Order findings by how often the friction would hit a real run, weighted by how badly it hurts when it does. Anchors for the scale's ends: rank *first* a blocker-or-friction defect on a path every invocation crosses that yields silently wrong output — silent wrong beats loud stall for damage, because a stall at least announces itself; rank *last* a nit inside a flag-gated module most invocations never load. Between the anchors, frequency times damage is deliberately a judgment call — real bite depends on how the plugin is actually invoked, which the page can't know — with one pinned tiebreak: the finding whose fix clears other findings (the open bar that several recorded guesses trace back to) outranks its own symptoms. Rank ruthlessly — an unranked list of twenty findings buries the three that matter under seventeen that don't.

Anti-pattern: reporting friction as a feeling instead of a defect. A feeling can't be fixed, traced, or re-checked. Convert it through the four-part bar — defect, pointer, evidence, route — or recognize that it never was the skill's defect at all. If you can't make the conversion, you haven't read the friction yet; you've only felt it.
