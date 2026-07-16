A procedure is only as good as the knowledge inside it, and that knowledge has a cost gradient. The expensive failure mode of codification isn't a missing step — it's *interrogation*: a run that fires fifteen questions at the maintainer when twelve of the answers were already in context, in the repo, or one explorer call away. So this phase has a strict order — cheapest source first, the human last — and a discipline that governs *what* you keep: the durable method and the why behind each step, never a brittle fact that goes stale (the rule in [methods-over-facts](../rules/methods-over-facts.md)). The cost ladder has four rungs, climbed in order: your own domain knowledge (free, §1), supplied artifacts (one read, §2), explorer fan-out (a delegated pass, §3), the maintainer (the only rung that interrupts a human, §5). Escalate exactly one rung, and only on one of two triggers: the current rung returns nothing on the question, or it can answer only at a signal tier too weak for what's being decided — and for a *standard's bar*, anything below an accountable source is too weak (the flip, below).

## 1. Draw from your own domain knowledge first

For processes with a known canonical shape — a retro, an intake triage, a release checklist, an onboarding runbook — you already hold the standard form. Lay it down from your own knowledge before reaching for anything external. This is free and instant, and it gives every later source something to confirm or contradict rather than a blank page. Encode the *method* ("a release gates on the audits passing before any version bump"), not a fact that will drift ("the catalog currently lists two plugins").

## 2. Mine the artifacts the requester already supplied

Existing docs, a sample input paired with its ideal output, a runbook, a half-written checklist — these are the highest-signal cheap source, because they're *this team's actual process* rather than the generic shape. Mine them for steps and for rules: an example input/output pair silently encodes the transformation the procedure must perform, and a worked example often pins an edge case no prose mentioned. Read what's in hand before asking for more.

## 3. Fan out to explorers for the real shape (retrieve)

When in-context knowledge and supplied artifacts leave the shape underspecified, recruit explorers — read-only gatherers that return findings anchored to a source:

- The **authoritative-sources** and **community-practices** explorers source a process's canonical form — what the standard, the reference, or the established practice says good looks like.
- The **plugin explorer** sources the *de-facto* shape: how the target plugin's own existing skills already do analogous things (so the new procedure reads like its siblings, not a transplant), plus prior art from external plugins solving the same problem.

Explorers gather; they do not decide. Treat their findings as input to weighting, not as settled answers.

## 4. Weight what comes back

Sourced knowledge is not all equal, and silently averaging it corrupts the procedure (the full craft is [source-weighting](../rules/source-weighting.md)). Authority outranks anecdote — a standard or reference beats a single forum post. Corroboration across *independent* sources boosts signal: several unrelated sources agreeing is strong evidence something real is there. And a conflict — anecdote says X, authority says not-X — is an attrition point, not a coin flip: favor the authoritative source, and surface the conflict to the maintainer rather than resolving it silently. A buried conflict becomes a latent bug in the procedure; a surfaced one is a decision the maintainer gets to make.

When two *authorities* disagree — both accountable, both defensible — that's not a conflict to win but a fork to encode: name each position and its tradeoff in one line, give the routing rule — the established convention of the surrounding context if one exists, else a declared house rule, else the maintainer — and mark it non-gating, so the run proceeds whichever way it routes. Collapsing a genuine fork to one side is the same defect as burying a conflict: a contested call written in as settled fact.

## The flip for standards: your own default is the anecdote

One class of knowledge inverts the ladder's first rung. When what you're sourcing is a **standard's bar** — a threshold the procedure will enforce, a grade boundary, a selection criterion, what its output must count as "good" — your own default answer is not free knowledge; it's the anecdote tier. A model's default for a bar is the average of common practice, and a bar that restates average practice encodes nothing — average is precisely what a stated bar exists to improve on. So a bar is never default-filled. The move is **derive and propose**, and it lands as an inline marker written onto the pinned bar: pull a candidate from an accountable source — the target plugin's design record, its established conventions, an official reference, craft you can defend in a clause — and write the bar carrying **(basis: <the source or derivation>)**. Where no accountable source reaches the call — a genuinely house-specific bar — you still pin your best defensible candidate, but write it carrying **(routed to maintainer: <the candidate + why>)** so the maintainer ratifies rather than excavates. A pinned bar written with neither marker *is* the default-fill this flip forbids — a fiat assertion phase 04 rejects and phase 06's gate fails.

## 5. Elicit only the forks the first four can't resolve

Now, and only now, ask the human — and ask narrowly. A question earns its place only if it meets both bars: the cheaper sources genuinely couldn't resolve it, *and* the answer changes the output. A fork that doesn't change what the procedure produces isn't worth a question; pick a sane default and note it. Batch the questions that survive both bars into one pass rather than dribbling them out — a codify run that interrogates is bad UX, and most of what feels like a needed question is actually an inference you haven't surfaced yet.

## 6. Infer aggressively, then surface every inference as an assumption

Prefer a visible assumption over a question almost every time. The line between the two: take it as a labeled assumption when one accountable source answers unopposed, or when independent cheaper sources agree with nothing against; keep it as a question when sources conflict, when the call is house-specific (nothing external could know it), or when it's a standard's bar with no authority found — the flip forbids default-filling those. Where the assumption side wins, take it — and write it down as an explicit assumption the maintainer can see and override, rather than stopping to ask. *"Assuming the spec seeds from the tracked work item; say so if it starts from a freeform brief instead"* moves the run forward while leaving the decision reversible. Phase 06 collects these surfaced assumptions for the final handoff; your job here is to make the inference and label it, never to make it invisibly.

## Source from a transcript when handed one

Under `--from-transcript`, the prior session, notes, or discussion *is* your primary artifact — it stands in for steps 1–2, replacing live interrogation with mining. Treat it exactly as a supplied artifact: extract the method and the why, and discard the situational facts. A transcript captures a process *as performed once*, so it's thick with one-time specifics ("we skipped the lint step because CI was down that day"). Keep the durable shape; let the incidental fall away — otherwise the run ossifies one session's accidents into the permanent procedure.
