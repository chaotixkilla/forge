# Separate fact from inference — the certainty scale

The whole product of understand is a map, and a map that states an inference as a fact is worse than no map: it sends the reader forward confident about something you never verified. The load-bearing grade every claim carries is its **certainty** — how you came to believe it: did you watch it, trace it, reason it, or read it somewhere. Undefined, each investigator invents their own ladder — one calls a reasoned guess "confirmed," another "unsure," and the same claim gets two incompatible weights.

Certainty answers one question: **how did you come to believe this — did you witness it, trace it end to end, reason it from partial evidence, or take a description on faith?** It is orthogonal to the source-of-truth ordering ([find-the-source-of-truth](find-the-source-of-truth.md)): that rule says *which source to believe when they disagree*; this scale says *how well-established your belief is* once you've chosen.

## The four levels

`(basis: ratified by the maintainer, 2026-07-09. The four-level scale below — observed → traced → inferred → assumed-unverified, keyed to the evidence that earns each rung. Code-investigation certainty has no single external authority the way security severity has CVSS, so the rungs, anchors, and boundaries are the maintainer's ratified house standard. Derived from the evidence ladder review's confidence scale uses — confirmed/probable/speculative by how much of the cause→effect chain you read — split at the top into witnessed-vs-read and extended down one rung to name the claim taken purely on faith.)`

- **observed** — you witnessed the behavior: you ran the path and saw the output or state, or you watched a test exercise it and pass. The claim rests on behavior you saw happen, not on reading that says it should.
  - *Anchor (top of scale):* "I ran the migration runner against a scratch DB and watched it emit `ALTER TABLE users …` then exit 0 — migrate.py:210, observed output."
- **traced** — you read every line of the exact path end to end; the mechanism is proven by reading, but you did not execute it. No link in the chain is reasoned — each is read.
  - *Anchor:* "reading `login()` at auth.py:20 → `refresh()` at token.py:88, an expired token reaches `tokens[0]` with no guard between — I read every line on that path but did not run it."
- **inferred** — you reasoned the behavior from partial evidence: read the definition and some call sites but not the whole path, or generalized from a pattern the codebase repeats. At least one link is reasoned, not read.
  - *Anchor:* "this handler almost certainly receives null when the upstream optional field is unset — I read the handler and one caller, not every caller."
- **assumed-unverified** — the claim rests on a name, a comment, a doc, a commit message, or a human's word, not checked against what the code does. You are relaying a description, not a behavior you established.
  - *Anchor (bottom of scale):* "the function is named `validateAndSave`, so it presumably validates before persisting — I did not read its body."

**State vs. behavior at the top rung.** The rungs above grade a claim about what the system *does* (behavior). A claim about an artifact's current *state or contents* — what a config, data file, or manifest *currently holds*, or the current value of a constant read directly — is **observed**: the bytes are the fact, and there is nothing being-consumed to witness. (Reading the catalog's current entries directly is *observed*; claiming what the loader *does* with them is a behavior claim, graded by the rungs above — often only *traced* until you watch it run.) `(basis: ratified by the maintainer, 2026-07-09; dogfood-surfaced — a direct read of static state is the fact itself, distinct from witnessing behavior, so the behavior-centric rungs would otherwise understate it.)`

## The adjacent-level discriminators

Assign by finding the highest rung whose evidence you actually hold; the boundary tests stop a claim sliding up a rung it didn't earn:

- **observed vs traced** — did you *witness the behavior happen* (ran it, saw the output/state, watched a test go green), or only *read the path* that would produce it? Witnessed → observed; read-but-not-run → traced. (the execution line)
- **traced vs inferred** — is *every* link between cause and effect *read*, or is at least one *reasoned* (a caller you didn't open, a branch you assumed, a pattern you generalized)? All links read → traced; one reasoned → inferred. (the every-link line)
- **inferred vs assumed-unverified** — is the claim backed by *any* first-hand read of the code, or does it rest *entirely* on a name, comment, doc, or human claim you never checked against code? Some code read → inferred; nothing but description → assumed-unverified. (the any-code-read line)

When two rungs both seem to fit, the higher wins only if you can name the specific evidence that earns it — the run you did, the lines you read. Absent that, drop a rung: a claim graded above the evidence you can name is the exact defect this scale exists to prevent.

## When the system is declarative, not executable
Not every system understand maps is executable code — a config, a schema, an IaC manifest, or a skill like this one is declarative, and "run it" and "the path" need a referent. Generalize by one substitution: **the system's behavior is how its interpreter consumes the artifact** — the loader that reads the config, the validator that applies the schema, the harness that loads the skill. The rungs then read:
- **observed** — you saw the interpreter consume the artifact and produce the effect (ran the config through its loader, validated against the schema, loaded the skill and saw which files actually wired).
- **traced** — you read the artifact's operative text end to end *and* the consuming rules that apply hold as established ground: either you read the artifact-specific consuming logic, or the rule is a **platform-general** foundational semantic — one that governs every artifact of this kind, relied on the way the executable scale relies on a language's evaluation rules without re-deriving them (you read the skill files, and the harness's "load only referenced slots" rule is a platform general, not a claim about this one skill).
- **inferred** — you read the artifact but *reasoned* about how it is consumed, or took an **artifact-specific** consuming behavior from a doc you have not seen borne out — a claim about *this* system's consumption (not a platform general), so it is claimed, not established. The discriminator that stops these two sliding: is the consuming rule platform-general (governs every artifact of the kind → traced) or specific to this system (must be read or observed → inferred until then)?
- **assumed-unverified** — you took the artifact's own labels or comments at face value without establishing how the interpreter treats them.

The artifact's *operative* text is Tier-1 evidence for a declarative system — it *is* the source of truth, not a description of one ([find-the-source-of-truth](find-the-source-of-truth.md)); the comments and docs *about* the artifact stay Tier 2.

## How --read-only caps the top rung
`observed` requires execution. Under [read-only-boundary](../modules/read-only-boundary.md) (`--read-only`) execution is forbidden, so the highest a claim can reach is **traced** — state that cap in the map rather than grading a static read as observed. A claim sourced only from a Tier-2 description (a doc, a comment; [find-the-source-of-truth](find-the-source-of-truth.md)) can be no higher than *assumed-unverified* until you check it against the code.

## Where it is assigned and consumed
Cited from [frame-the-question](../phases/01-frame-the-question.md) (set the target rung), [trace-the-behavior](../phases/03-trace-the-behavior.md) (grade each claim as you establish it), [corroborate-against-reality](../phases/04-corroborate-against-reality.md) (grade the "why"), and [synthesize-the-answer](../phases/05-synthesize-the-answer.md) (every claim in the map carries its rung). It is also the scale understand grades the [assumption-hunter](../../../agents/critics/assumption-hunter.md) critic's surfaced premises on: the critic grades on understand's declared scale where it can, and where it hands a premise back in plain terms (load-bearing-ness and reachability), understand assigns it the rung its evidence earns — either way every folded-in premise reaches the map graded.
