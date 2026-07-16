Picking scenarios decides *what* to run; this phase runs them and captures *what happened*. The whole value of dogfooding lives here, and it depends on one discipline: run each skill the way a stranger would, and record the run honestly — including the moments you were tempted to help. A run that quietly fills the skill's gaps with your own context proves the gaps don't exist, which is exactly the lie a dogfood is meant to expose.

## Run as a cold executor

Invoke each scenario as if you had no prior context — only the skill's own files and the flags from the scenario. This is the same fresh-agent stance the cold-executor critic takes, applied to yourself while you run. The skill must carry its own water: its frontmatter, its phases, its rules. If completing a step requires something the skill never says — a convention "everyone knows," a path the maintainer always uses, a default the skill assumes but doesn't state — that is precisely the friction to surface, not to supply.

Concretely: when a step is underspecified, do not reach into this conversation for the answer. Make the gap visible, then keep moving, by this rule: if the most literal reading of the words on the page still yields a runnable action, take it — even where it looks wrong — and record where it leads; the wrong destination is the evidence that the gap is real. If no literal reading yields an action at all (the step needs a value, path, or order it never supplies), record the stall, adopt the most defensible fill as a *declared* assumption, and continue — a stall ends the scenario only when no declared assumption can make the next step actionable. Continuing matters: a scenario abandoned at step 2 says nothing about steps 3 through 6, and the assumption is captured as a finding either way. The instinct to be helpful is the enemy here — every assumption you smooth over is a finding you've destroyed; an assumption you declare is a finding you've kept.

## When the skill under test mutates its subject

Most skills read and analyze; some — a skill that edits code, writes files, lands a change — *mutate the subject tree* when run for real, and dogfooding one raises a question the read/analysis stance never faces: what becomes of the change the run makes? Left unaddressed, a real run either pollutes the build's own diff with an unrelated edit, or gets reverted (erasing the very artifact the run existed to produce), or quietly isn't run at all. Decide the disposition *before* running, on two axes:

- **Pick a reversible, output-verifiable scenario.** Prefer a change whose correctness a machine can confirm — a refactor whose output is provably unchanged, a change with a clean single-step revert — over one whose effect you would have to eyeball. A verifiable mutation lets the run *prove* it did the right thing (regenerate and diff, run the guard test), which is the behavioral evidence the dogfood exists to produce; an unverifiable one leaves you trusting the skill you are testing.
- **Decide where the real artifact goes, and record it.** State it in the log: **kept** as its own attributable commit, separate from unrelated work, so the mutation is traceable and doesn't ride along with something else; **reverted** after you have observed and recorded the run, when keeping it would pollute the tree and the observation was the whole point; or made against a **throwaway subject** (`--subject=<copy>`) when the real tree must stay untouched. Never leave a real mutation stranded in the tree with no decision recorded — an un-dispositioned edit reads later as an accident, not a dogfood.

The cold-executor stance still governs *how* you drive the skill; this only adds what to do with what it writes.

## When the skill's real effect lands on an external system

The mirror case: some skills' real effect never touches the subject tree — it reaches an external system through a configured capability (a read from a live source, a post to an external channel, a directed action against a running environment), none of it reachable from the dogfood run. Un-runnable is not un-dogfoodable. The legitimate dogfood is a **cold walk with simulated capability returns**: drive the procedure end to end, and where a step calls the absent backend, feed it a plausible return as a declared assumption (per the cold-executor stance above) and keep going. What the walk actually tests is the skill's declared **degrade/block posture** — a backend unreachable from the run is the environment's condition, not a stall to bill against the skill, so the thing to observe is whether the skill degrades or blocks the way its frontmatter promised when the capability yields nothing. A **produce-then-deliver** skill splits here: its produce half is a genuine cold run against real output, and only the deliver half is degrade-exercised against the absent sink. Either way, record that the live external effect was never exercised — a clean walk proves the procedure and the posture, not that the effect lands.

## Record three things per scenario

For each scenario, capture a short, factual log of:

- **What it did** — the path the skill actually took: which phases fired, which branch of each fork it went down, what it produced. This is the ground truth later phases reason about; keep it concrete (files touched, decisions made), not a paraphrase of the skill's intent.
- **Where it stalled** — any point the skill couldn't proceed without more than it gave you: a missing input, an unstated default, a step that referenced a capability with nothing behind it, a fork with no rule to resolve it. Note the *file and step* where the stall happened, not just that it happened.
- **What it assumed** — every choice you had to make that the skill left open. Write these as explicit assumptions ("the step said publish the report but named no destination, so I assumed the configured artifacts backend"), because an assumption you record is a finding and an assumption you forget is a silent pass. Include every judgment call where the skill named the call but not the bar — a step that says grade, filter, or keep the best without saying against what. Record both the call you made and the bar you invented to make it: the challenge phase's standards critic reads exactly these to test whether a second run would have called it the same.

## Watch for contract drift

Beyond stalls and assumptions, watch for the run diverging from what the skill *declared*. Contract drift is behavior that contradicts the frontmatter or the slot structure — the gap a static audit can't catch because it shows up only when the skill runs:

- A flag the skill declares but the run never actually honors — e.g. a dry-run flag that still writes, or a report-format flag that's ignored.
- A capability the phase names but that resolves to nothing at run time — the dispatch has no backing for the configured provider, so the step describes an action the plugin can't perform.
- A step doing work that belongs in a different slot — a phase quietly applying reusable craft that should have been a cited rule, or a "rule" the run can only follow in one fixed order (a phase in disguise).
- Output that doesn't match the declared shape — a skill whose description promises one thing and whose run produces another.

Record each drift against the specific declaration it contradicts: *this* frontmatter flag, *this* phase line. That pointer is what makes the finding actionable in the report phase.

For example, dogfooding a release skill under `--dry-run`: the scenario is "release a plugin marked unpublished." A cold run reveals two things at once — a stall (the skill's preflight gate is meant to hard-block an unpublished target, so the run should refuse, and you record whether it actually does) and a contract check (under `--dry-run` it must report every intended write and touch nothing). If the run writes a version bump anyway, that's drift against the `--dry-run` flag's declared meaning, logged against that exact flag. Notice the dogfood found this by *running* the gate, not by reading that the gate exists.

Anti-pattern: a log that records only outcomes ("the skill ran"). An outcome with no path, no stalls, and no assumptions is unfalsifiable — it can't be challenged in the next phase and can't be traced to a file in the report. The log's job is to make the run *inspectable*, so capture the friction even when the scenario ultimately succeeded; a skill can reach the right answer by a route that only worked because you helped it.

Carry the per-scenario logs forward intact. The challenge phase interrogates them; the report phase mines them. Do not summarize them away yet.
