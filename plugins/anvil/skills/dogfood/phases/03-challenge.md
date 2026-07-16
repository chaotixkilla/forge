The run phase captures friction you *hit*. But the most dangerous gaps are the ones a single run glides past — a step you happened to have the context to fill, a fork you happened to take the easy branch of, a judgment you happened to make one way when the skill's text would have licensed another. A run proves a path works; it can't prove the path works *for someone who isn't you*, or that a second someone would have produced output of the same character. This phase closes both gaps by handing the run to two skeptics whose whole job is to assume you got lucky.

## Two critics, two failure classes

Recruit the cold-executor critic and the standards-skeptic critic, and give each the same two halves: the skill's files (what the skill *says*) and the per-scenario run logs (what actually *happened*). Both work the seam between the halves, but they hunt different defects there:

- The **cold-executor critic** hunts *stalls and guesses*. Its lens: could an agent with zero context have run this end-to-end without inventing a value, an order, or a fact? It flags every step the log shows completing that the skill's text doesn't actually license, and assumes by default that every smooth-looking step hides an unstated assumption until the text proves otherwise.
- The **standards-skeptic critic** hunts *open standards*. Its lens: everywhere the skill demands a judgment — a bar for "good", a threshold, a grade, a selection criterion — would two independent cold runs converge on the same call? It flags every judgment the run made that the skill's text couldn't force a second run to make identically.

The discriminator between their territories: a cold-executor finding is a step that *cannot complete* without a guess — the run stalls or invents. A standards finding is a step that *completes either way* — both runs finish, and their outputs differ in character. A run that never stalls can still fail the standards critic at every point it graded, ranked, or filtered; surfacing those is why this pass recruits two lenses, not one.

Where both critics flag the same step — a guess was forced *because* a bar was open — merge them into one finding and keep the open-standard framing: the unpinned bar is the root cause, the guess its symptom, and one repair (pin the bar, or record why it stays open) clears both. The critics also share one adjudication rule: deliberate open-endedness is a defect only when it is *undocumented*. A judgment the skill leaves open with the reason recorded on the page is a decision; the same openness with no recorded reason is a finding, whichever critic caught it.

## Surface what the happy path concealed

The critics are hunting the gaps a successful run masks. Direct them at the failure modes a single pass under-tests:

- **Untaken branches.** The run went down one side of a fork; the other side may have no rule, no checkpoint, no defined behavior at all. The critic flags forks the skill resolves only by luck of which branch the run happened to need.
- **Borrowed context.** A step that "just worked" because the runner knew the missing piece. The critic challenges every step that completed without the skill stating how — these read as success but are latent stalls for the next executor.
- **Unstated preconditions.** State the run happened to start in that the skill never establishes. If a scenario only worked because the subject was already in a particular shape, the skill has a precondition it doesn't declare.
- **Silent guesses logged as decisions.** An assumption the run recorded as if it were a defined default. The critic's job is to demote these back to gaps: a default the skill doesn't state is a guess, however reasonable.
- **Unpinned bars behind smooth judgments.** The log reads clean at a step that graded, ranked, or filtered something — but the skill names the judgment without carrying its bar. The standards critic asks the counterfactual: would a second run, given only these files, have made the same call? Wherever the text can't force a yes, the bar is open, and the smoothness of *this* run is precisely what concealed it.

For example, a scenario ran a skill's first fork — the "capability is new to the skill" branch — and it completed cleanly. The cold-executor critic challenges the *other* branch: when the capability already exists, the skill says to "confirm the wiring resolves," but a fresh agent has no way to tell a resolved wiring from an unresolved one — the skill never says what confirmation looks like. The standards critic's parallel catch, same skill: its report step says to keep only the "significant" findings — this run kept four and the log reads clean, but nothing on the page separates significant from not, so a second run keeps nine. Neither finding could have come from the run alone.

## Keep the reflexive run bounded

Challenging is where a self-run is most tempted to recurse: the critics' findings invite re-running, the re-run produces new outputs, those want challenging in turn. Resist it. The scenario set was closed in the pick phase; challenge *those* runs and stop. New scenarios the critics suggest are findings for the report — "this fork was never exercised" — not new runs to fold into this pass. The kit challenging the kit must terminate at the boundary the first phase drew, or the self-hosting proof never returns an answer.

Anti-pattern: treating a critic as a second runner — re-executing scenarios to "check" its findings until the run loops. The critics read the existing logs against the existing skill; they do not generate new runs. One challenge pass over the closed set, then forward to the report.

Carry the critics' findings alongside the run logs into the report phase. The run supplies the friction you hit; the cold-executor supplies the friction you'd have hit cold; the standards-skeptic supplies the divergence a second executor would have produced — the report phase fuses all three and points each back at the file that owns it.
