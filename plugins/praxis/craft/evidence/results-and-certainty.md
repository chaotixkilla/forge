# Results and certainty

A reader acts on two things a check reports: what it found, and how sure the finding is. When each piece of work names these in its own words, the same outcome reads as "works" in one report and "verified" in the next. A word that meant "nothing was exercised" in one place gets read as a pass in another, and two different strengths of evidence both arrive as "confirmed".

## What the vocabulary covers

It covers the words a reader sees for **what a check found** (a result) and **how sure a claim is**: certainty for a claim about the system, support for a claim about the outside world.

It does not cover:
- **severity**, which stays on each domain's own scale;
- **process states**, such as landed, merged, awaiting review, a delivery's disposition, or how a piece of work ended;
- **port error codes**, which are written for callers, not readers.

Report each word as it is written here. Don't substitute a synonym, a local alias, or a mapping from local words onto these. **`confirmed` is not a certainty word.** It has stood for a witnessed mechanism, a path read end to end, and a real incident, so say which of those you mean. Where a check has its own finer test for placing an outcome, that test still decides. What it decides between is these words, with these meanings. `(basis: maintainer, 2026-10-02)`

## Results: what a check found

Each result attaches to one thing checked: a flow, a requirement, an assumption, or a gate. It carries its scope, meaning what was checked and where: the environment, the inputs, the version. A result stripped of its scope overstates itself as soon as it leaves the check. `(basis: maintainer, 2026-10-02)`

- **holds**: checked, and what was claimed or required was met within the stated scope.
  - *Anchor:* the password-reset flow was driven end to end in staging, and every step behaved as claimed, each effect confirmed where it lands. **holds**, for that flow in staging.
- **fails**: checked and refuted, either by a reproducing failure or by a requirement shown unmet.
  - *Anchor:* signing in with the new credential fails on every re-run, while the build from before the change completes the same flow. **fails**, with the reproduction attached.
- **unsettled**: checked, at least in part, but what was seen doesn't settle it either way.
  - *Anchor:* the flow ran as far as the confirmation message, but the reset message never arrived through the environment's delivery path, so the last step was never reached. **unsettled**. Every step that ran looked healthy, and those steps grade only themselves.
- **not checked**: nothing about the claim was exercised. The reason is always given.
  - *Anchor:* the environment requires an access credential the run could not obtain, so no step was driven. **not checked**, because no credential was available for the environment.

**holds is provisional and fails is terminal.** One reproducing failure settles the question for that thing in that scope, and no number of later clean checks undoes it. No number of clean checks settles the other direction, because the next input, environment or part can still fail. The strongest thing `holds` can mean is "checked here and not refuted", so word it that way and read it that way. `(basis: maintainer, 2026-10-02; the asymmetry after Dijkstra, The Humble Programmer, 1972)`

**Parts that come out differently get one result each.** A requirement met in two of its three clauses gets a result for each clause, not a fifth word such as "partially satisfies". `unsettled` is for a single thing whose evidence doesn't decide it. The test is whether the thing divides into parts that each have their own outcome. If it does, split it and place each part. If it doesn't, it takes one result. `(basis: maintainer, 2026-10-02)`

### Placing a result

Ask these in order, and stop at the first that answers:

1. **Was anything about the claim exercised, meaning run, driven or examined against the claim?** No → **not checked**, with the reason: out of scope, unreachable, no access, or not run. Yes → question 2. This is the line between `not checked` and `unsettled`.
2. **Was a refutation established?** That means a failure that reproduces, or a requirement shown unmet. Yes → **fails**. A misbehaviour that didn't recur, or whose cause can't be told apart from the environment, is not a refutation, so it goes on to question 3. This is the line between `fails` and `unsettled`.
3. **Was every part of what was claimed shown to be met within the scope?** Yes → **holds**. Any part unreached, unseen or unresolved → **unsettled**. This is the line between `holds` and `unsettled`.

## Which scale a claim takes

A claim's certainty and its support grade different things, and each claim takes one of them. The choice follows from **what the claim is about**, not from where its evidence came from:

- **About the system under work** → **certainty**. That means its code, configuration, running behaviour, data and history, including how a dependency behaves inside it. A claim about the system that rests only on documentation, the system's own or a dependency's, is still graded for certainty, and it grades `unverified` until it is checked against the system.
- **About the world outside it** → **support**. That means what a standard specifies, what a vendor documents for its own product, what a field has found, or what a practice is.
- **About what one of the organization's own records states**, where the record isn't about the system, such as a policy, a decision's rationale, product intent or a process → **certainty**, as a state claim: **observed** when the record was read directly, and the claim names the record. It never grades on support, because the record isn't a source on the outside world. A claim that the system is as a record says is about the system, above. `(basis: derived — the record's contents are the fact, as the state-claim rule holds)`

*Anchor:* "our call to the parser returns null on empty input" is about the system. "the parser's next major version drops that behaviour" is about the outside world, and its evidence is the vendor's changelog.

The scales stay separate because on the certainty scale every sourced claim would grade at the bottom. A research finding would then read as no better than a guess, and the line between corroborated and contested, which is what research exists to report, would be lost. `(basis: maintainer, 2026-10-02; the anchor and the dependency case derived from that ruling)`

## Certainty: how a claim about the system was established

This scale grades a finding, a cause, a map entry or an assumption about the system. `(basis: maintainer, 2026-10-02)`

- **observed**: seen happening. The behaviour ran and its output or state was watched, or a test exercised it.
  - *Anchor (top):* "I ran the migration against a scratch database and watched it emit `ALTER TABLE users …` and exit 0 (migrate.py:210, observed output)."
- **traced**: every link from cause to effect was read, but the path wasn't run.
  - *Anchor:* "`login()` at auth.py:20 calls `refresh()` at token.py:88, and an expired token reaches `tokens[0]` with no guard in between. I read every line on that path but didn't run it."
- **inferred**: at least one link is reasoned rather than read. That could be a caller left unopened, a branch assumed, or a pattern generalized from what was read.
  - *Anchor:* "this handler receives null when the upstream optional field is unset. I read the handler and one of its callers, not every caller."
- **unverified**: the claim rests on a pattern, a name, a description or someone's word, with nothing of the system worked through.
  - *Anchor (bottom):* "the function is named `validateAndSave`, so it presumably validates before persisting. I didn't read its body."

**State claims.** A claim about an artifact's current contents is **observed** when those contents were read directly, for example what a config file holds or the value of a constant. The contents are the fact, and there's nothing to watch run. A claim about what the system *does* with those contents is a behaviour claim, and the scale above grades it. Reading a manifest's entries is observed. Saying what its loader does with them is often only traced until the loader has been run.

**Declarative systems.** For a declarative artifact, such as a configuration, a schema or a manifest, its behaviour is how its interpreter consumes it. "Ran" means the interpreter was seen consuming it, and "the path" means the artifact's operative text together with the consuming rules. `(basis: derived — the scale needs a referent for running when the system doesn't execute)`

**Absence claims.** A claim that something doesn't happen, such as "nothing calls X" or "no retry on this path", is graded by how the search for it was done, and it is anchored to that search. It is **traced** when the search covered every place the thing could be, such as every caller by the code's own references or every path. It is **inferred** when the search couldn't be exhaustive, for example because of dynamic dispatch, reflection or generated code. An absence is never observed, because there is nothing to watch happen. `(basis: derived from the tests below)`

### The adjacent-level discriminators

Assign the highest level whose evidence you actually hold:

- **observed vs traced**: was the behaviour seen happening, or was only the path read? Seen → observed. Read but not run → traced. This is the execution line. Where the check may not execute anything, the highest level a behaviour claim can reach is traced. State that cap, and don't grade a read as observed.
- **traced vs inferred**: is *every* link between cause and effect read, or is at least one reasoned? All read → traced. Any reasoned → inferred. This is the every-link line.
- **inferred vs unverified**: is the claim backed by *any* first-hand reading of the system, or does it rest entirely on a pattern, name, comment, document or person's word that was never checked against the system? Some first-hand reading → inferred. Nothing first-hand → unverified. This is the any-first-hand-read line.

When two levels both seem to fit, the higher one wins only if you can name the evidence that earns it: the run you did, or the lines you read. Otherwise, drop a level.

## Support: how well sources back a claim about the outside world

This scale grades a claim that rests on sources. Two terms define the levels:

- An **origin** is a source that doesn't draw on another source already counted, as [triangulate-before-trusting](triangulate-before-trusting.md) counts them.
- A source is **credible** when it has an accountable author with standing on the topic. From strongest down, that is the claim's definitive origin, a vetted synthesis (peer-reviewed or editorially overseen), or an identified expert's unvetted first-hand analysis. Unvetted community voice is not credible in this sense, however much of it agrees. One source is **clearly stronger** than another when it sits higher on that order.

`(basis: maintainer, 2026-10-02)`

- **established**: two or more independent origins, each a vetted synthesis or stronger, converge on the claim, and no credible contradiction stands. A single source also establishes a claim when it is the claim's definitive origin, by [prefer-primary-sources](prefer-primary-sources.md)'s test.
  - *Anchor (top):* the language specification defines the default, two independent reference texts that trace to it agree, and a deliberate search for dissent found none.
- **corroborated**: at least two independent origins agree, at least one of them credible, but a gap keeps the claim short of established. The gap is that the strongest agreeing source is one expert's unvetted word, a tension in detail the claim doesn't assert is left unresolved and noted, or the support is slightly indirect: it bears on this specific claim without stating it outright. Support attaches to the specific claim, and a source that backs only an adjacent claim doesn't count.
  - *Anchor:* two named practitioners' write-ups, each independent of the other, report the same rate limit, and nothing from the vendor states it.
- **contested**: credible sources genuinely disagree, and the evidence doesn't resolve the disagreement to one side. The claim is delivered as the dispute, per [surface-disagreement](surface-disagreement.md).
  - *Anchor:* the vendor's documentation says the limit applies per key, while an expert's published benchmark measures it per account, and neither one accounts for the other.
- **single-source**: the claim rests on one independent origin. That covers one source, several sources that trace back to one, a citation chain that dead-ends before reaching its origin, and agreement only among sources that aren't credible. It also covers a claim that was never checked beyond the source it arrived from.
  - *Anchor (bottom):* one forum answer asserts it, the link it cites is dead, and no independent origin turned up.

`(basis: derived for the last two cases of single-source — weak agreement and an unchecked claim each rest on no more than one origin)`

### The adjacent-level discriminators

- **established vs corroborated**: are there two or more independent origins at vetted synthesis or stronger converging, or one definitive origin, with no credible contradiction standing? Yes → established. Agreement whose strongest source is one expert's unvetted word, an unresolved tension in detail the claim doesn't assert, or slightly indirect support → corroborated.
- **corroborated vs contested**: do the independent origins agree, or does a credible contradiction stand? The sign of contested is a credible contradiction still standing, not the absence of every doubt. When one side's best source is clearly stronger than the other side's best, the conflict resolves to that side and doesn't stand. A disagreement reaches contested only when it reaches what the claim asserts: values, or a conclusion, the reader would use differently. A tension in detail the claim doesn't assert leaves it corroborated, with the tension noted. `(basis: derived — a grade reports the claim as asserted, so only a disagreement about that changes what the reader does)`
- **contested vs single-source**: is there credible evidence on more than one side, or too little evidence for there to be sides at all? Sides → contested. One origin, a broken chain, or claims that were never checked → single-source.

When two levels both seem to fit, the lower one wins unless you can name the independent corroboration or the definitive origin that earns the higher.

The grades that judge one source on its own, such as its strength or its standing as anecdote, are inputs to support. They stay inside the work that gathers sources and never reach the reader as a claim's grade. `(basis: maintainer, 2026-10-02)`
