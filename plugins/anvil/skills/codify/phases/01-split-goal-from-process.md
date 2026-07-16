Every codify request arrives as a destination — *"turn prompts into specs"*, *"run our incident retro"*, *"triage inbound bugs"*. The destination is real, but it is not yet a procedure: it names where the maintainer wants to end up, not the route. This phase does two things at once — it pries the *route* out of the stated *goal*, and it splits the goal itself into the part that is invariant (what good looks like for anyone doing this) from the part that is this team's contingent way of getting there. Get this wrong and everything downstream inherits the error: a skill that hard-codes one team's house style as if it were the law, or a skill whose steps are just the goal said three times.

## Require the target before anything else

Codify writes the procedure *into a specific skill*, so it needs to know which one. Require `--plugin` and `--skill`; if either is missing, stop and ask — don't guess a target from context, because writing a procedure into the wrong skill is a silent, expensive mistake. With both in hand, you know your write destination: the named skill's `phases/` (and `rules/` for any reusable craft you extract).

**If this is a regenerate** — the named skill already carries phase bodies (thin, below the bar), not empty stubs — the goal and its invariant/contingent split are already encoded in those files. Read them off the existing skill and *confirm* the split rather than re-deriving it from scratch; re-open it only where the existing skill got the split wrong (a contingent house habit hardened as if invariant, or the reverse). The sections below author the split fresh; in a regenerate they become a read-and-check pass, and the real work waits in phases 04–06.

## Identify the stated goal, then separate invariant from contingent

State the goal back in one line — the outcome the requester actually wants. Then split it (this is the craft in [goal-vs-process](../rules/goal-vs-process.md)): the **invariant goal** is what good looks like for *anyone* doing this well; the **contingent process** is how *this* team reaches it. Harden the goal into the skill's reason for existing; parameterize the process so a different team can swap their own way in without rewriting the skill.

The test that does the separating: *would another team, also doing this well, do this step differently?* If yes, it's process — parameterize it (a flag, a config value, a documented assumption). If no, it's the invariant goal — harden it into the procedure's spine. A spec skill's goal *"a spec a cold implementer can build from with no further questions"* is invariant; *"we always start specs from the item in our work tracker"* is contingent — encode the first as the skill's purpose, the second as a swappable input, named at the capability level (*"seed from the tracked work item"*) so it isn't pinned to one team's tracker.

## Expand the goal into an actual procedure

Now produce the route: the ordered steps that reach the invariant goal. This is the move from noun to verb — from *"specs"* to *gather the source material → draft the interface → enumerate the cases → check it against a cold reader*. The steps don't need to be polished or complete here; that's what phases 02–05 are for. What they need to be is *steps* — actions with an order — not a restatement of where you're going.

## Check: steps, not a paraphrase

Before leaving this phase, read your steps against the goal. If each "step" is the goal wearing a different verb — goal *"produce a good spec"*, step 1 *"write the spec well"* — phase 1 hasn't actually started; you've renamed the destination, not charted the route. A real procedure has steps the goal does not mention: the gathering, the decomposition, the edge-case sweep, the validation. If those aren't surfacing, the process knowledge isn't in hand yet — which is exactly what phase 02 goes to source.

## Honor --first-pass

Under `--first-pass`, the goal/process split plus the bare skeleton *is* the deliverable: return it and pause for the maintainer to steer before you invest in filling detail. The split is the highest-leverage thing to get right and the cheapest to correct early, so a steering checkpoint here is well spent — a wrong split caught now saves rewriting every phase below it.
