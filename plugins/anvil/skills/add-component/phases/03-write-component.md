Now write the body, into the shape phase 2 mirrored. What "the body" means is entirely kind-dependent — an adapter's body is concrete tool calls, an agent's is a gather-or-challenge procedure, a rule's is durable craft, a module's is flag-gated behavior, a hook's is a scoped handler — so this phase is a case-split, one section per kind. Write only the section for the kind you resolved. The unifying discipline across all of them: every component except the adapter must obey the same capability-not-tool rule the kit enforces on its targets, because the kit's own components are subject to it too. The adapter is the single sanctioned exception, and that exception is precisely what keeps every other layer clean.

## Adapter — the concrete calls, and nothing above

The adapter is the *only* file in a plugin where a concrete tool, provider, transport, CLI, or vendor name may appear. That is its entire reason to exist: it absorbs the tool so the skill layer never has to. An adequate adapter body carries four things, each with a bar to clear:

- **The capability it implements, named up front** — one line, matching the capability vocabulary the parent skill uses, so the dispatch and the coverage audit can match file to need. Bar: a reader knows *which* abstract request this file answers before any provider detail appears.
- **The translation, per request** — for *every* request the parent skill's phases make of this capability, the provider's concrete counterpart: the operation, what it needs, what comes back. Bar: the **coverage test** — an executor given only this file and the capability request can complete the act without opening the skill or guessing intent. A request the skill makes with no counterpart here is a hole in the adapter's coverage.
- **The provider's failure surface** — its characteristic error shapes and quirks, and what the adapter reports upward when they hit, phrased in capability terms (the skill hears "the backend refused the publish," never a provider error code). Bar: the parent skill can react to failure without learning the provider's vocabulary.
- **Call-time discovery notes for the volatile surface** — name the calls and their shape, but instruct the executor to resolve exact parameter names and current options against the live tool, not from a frozen list (see [adapter-discipline](../rules/adapter-discipline.md) — methods over facts, even inside the one place tools are allowed).

The bottom of the scale, so you recognize it: a body that restates the capability's wording with a provider name attached ("publish the artifact using this provider") — that names the tool without carrying the translation, and is an adapter in filename only. Hold the line *upward* too: if you find yourself writing what *order* things happen in, or *whether* to do them, that's skill-layer logic leaking down — stop. The per-line test is the swap test in [adapter-discipline](../rules/adapter-discipline.md): anything that would survive a provider swap belongs upstairs. This translation only stays clean if the seam is drawn in the right place ([port-and-adapter-seam](../rules/port-and-adapter-seam.md)): write strictly below the seam — the concrete mechanism — and leave the capability's intent above it untouched, so that swapping providers later changes only this file and never the skill layer.

## Explorer or critic — a gather procedure or a challenge procedure

These are agents, and the two roles are strictly distinct ([explorer-vs-critic](../rules/explorer-vs-critic.md)). Write the body for the one you're adding, and do not let it drift into the other. For both, the convergence bar is the same: two agents running this body over the same subject must return findings that match — a body that leaves *where to look* or *what counts* to the runner's taste fails, however fluent it reads. And a shared agent's body must not **bake a factual claim about its sibling skills' current state** — which skills declare a graded scale today, which flags exist. Such a claim staleifies the moment a sibling changes, and no audit cross-references an agent against its recruiters; state the conditional generically ("grade on the recruiter's declared scale where it has one; where none does, …") so the body stays true under any sibling's evolution.

An **explorer** gathers. Its body must contain four parts, each with its bar:

- **The question it answers** — one line, phrased as a question of *fact* ("which capabilities have a backing adapter?"), never of quality. Bar: no judgment word survives in it.
- **The search space, enumerated** — the specific surfaces to read and the order to sweep them. Bar: it's a sweep, not a wander — "read each skill's frontmatter, then each adapters/ folder" passes; "investigate the plugin" fails, because two runners would visit different files.
- **The finding shape** — every finding is a claim plus its source anchor (file, line, location). Bar: a caller can verify each claim without re-running the explorer.
- **The done condition** — finished when the enumerated space is exhausted, never when "enough" was found. Bar: the body says what full coverage is.

For example: *"enumerate the target plugin's adapters and report, per skill, which capabilities have a backing adapter and which don't, anchored to each file."* Facts with provenance, no verdict.

A **critic** challenges. Its body must contain four parts, each with its bar:

- **The lens** — one line naming the failure class this critic owns, stated as what it assumes is wrong ("assumes the procedure can't be run cold"). Bar: the lens is narrow enough that a second critic knows which findings are out of scope.
- **The hunt** — the ordered checks it applies, each phrased as an attempted break ("construct the case where this step forces a guess"), never as virtues to admire ("check the steps are clear"). Bar: each check tells the runner what a *hit* looks like, not what goodness looks like.
- **The finding shape** — verdict + the reasoning that justifies it + an anchor into the work under challenge; graded on the parent plugin's declared scale if one exists, never on a scale the critic invents mid-run.
- **The clean verdict** — what it returns when the lens finds nothing: an explicit "no findings under this lens," never nits manufactured to look thorough.

For example, a cold-executor lens: *"assume a fresh agent with zero context, walk the procedure step by step, and flag every point where running it would require a guess."* A verdict and the reasoning, no new fieldwork — if a check requires reading beyond the work handed to it, that's gathering: recruit an explorer for it instead.

If the agent you're describing seems to need to both gather facts *and* render judgment on them, you have two components, not one — split them.

## Rule or module — durable craft, or flag-gated behavior

A **rule** is a-la-carte craft: reusable judgment a phase reaches for when it applies, not bound to any sequence. A rule earns its file by *settling a judgment call*: its body must carry the **why** (what goes wrong without it), the **method** (how to actually make the call), and the **discriminator** — the test that decides the call it exists to settle, precisely enough that two executors reading it converge. That last part is the bar: a rule that only exhorts ("keep components minimal") is below it; the same rule carrying the test that separates minimal from missing is at it. Write at the altitude of craft (never naming a tool — a rule that names a tool is a leak). A rule needs no activation: living in `rules/` and being cited by the phases that use it *is* its registration. Phase 4 confirms there's nothing to wire.

A **module** is behavior a flag turns on — an optional lens or extra pass the maintainer opts into per-invocation. Write only the **delta**: what the run does differently when the flag is set, on top of a base procedure the body never restates. The bar is the deletion test: remove the module and the parent skill must still complete its job — if it can't, this isn't a module, it's a phase, and its "flag" is really a phase input (a flag that merely names a phase's default branch or window fails the same test). The module body is only half the component; its activating flag is the other half, declared in the parent skill, and phase 4 makes that mandatory. Don't write a module whose flag you can't name — if there's no flag, it's not a module (it might be a rule, or a phase).

For either kind, if the body encodes a real *process* — multiple decision points, sourced knowledge, a method that deserves codify's discipline — hand the body to the codify skill (a sibling) rather than free-handing prose. codify exists to turn a process into a runnable procedure; reach for it when the rule or module is process-heavy, and write the body inline when it's a short, self-evident piece of craft.

## Hook — a handler scoped to one lifecycle event

A hook fires on a harness lifecycle event. Write the handler for the concern this hook owns and keep it scoped to *this plugin* — a hook that reaches outside its plugin's business is a packaging risk and a surprise to consumers. The body says what to do when the event fires, and it must state its **failure posture** explicitly: when the hook's check fails, does it block the event or warn past it? That one line is the hook's most consequential decision — a blocking hook that should have warned halts a consumer's work; a warning hook that should have blocked lets the very thing it guards against through — so never leave it implicit for the harness's default to decide. Phase 4 binds the file to the event in the plugin's hooks manifest (the file is inert until then). Pick the event that matches the concern — a check that should run as work is authored binds to an authoring-time event; a guard that should run before an action binds to that action's pre-event — and write the handler to do one thing well at that moment.

## Under `--extend` — revise the body that is already there

The kind sections above say what an adequate body holds. Under `--extend` they are unchanged: **the merged file is held to exactly the same bars as a newly written one, and it is the merged file that is judged, never the delta.** A small edit that leaves the body short of its kind's bar has not passed because the edit was small.

Two disciplines are specific to editing:

- **Lift, don't rewrite.** Preserve every part of the existing body that already clears its bar, and raise only what falls short — the same discipline [codify](../../codify/SKILL.md) states for its regenerate lane, which governs here unchanged rather than being restated. Discarding conformant content to recompose from scratch is this lane's failure mode, and it is invisible in the result: a rewritten body reads well while quietly having dropped the one exception a previous maintainer put there on purpose.
- **Run the gate on the result.** An extend that writes prose and stops is hand-authoring with a procedure around it, which is the failure this lane exists to end. Recruit the **cold-executor**, **standards-skeptic**, and **economy-skeptic** critics on the merged body and close what they raise, looping until a pass over the current text raises nothing — the same three lenses codify's validation runs, reached by recruiting the critics directly because codify targets a skill and a component is not one. Without fan-out, apply each lens yourself in a deliberately amnesiac pass. `(basis: derived — the gap this lane closes was a component body edited with no gate at all; giving the lane a procedure but no verification would move the defect rather than fix it, and these three are the kit's existing answer for authored prose.)`

An extend that changes only a citation or a flag name is wiring, not a body edit — it does not need this lane.

## Across every kind

Keep the body minimal and earned — the scaffolding-skeptic lens applies to component bodies too: no speculative sections, no behavior the component wasn't asked for. Write into the mirrored shape from phase 2 so the file reads as family. Under `--dry-run`, compose nothing to disk: report the body you *would* write and the path it lands at, then stop. Then carry the finished file into phase 4, which makes it live by wiring it where it's consumed.
