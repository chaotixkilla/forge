# Incident retrospective

A retrospective that recounts what happened and stops there prevents nothing: the same gap lets the next incident through. This rule holds what a retrospective owes, at every severity; the *effort and detail* scale with severity, the parts don't. It applies to any incident that was real; a signal that was stood down gets at most a note that its alert needs tuning.

## Reconstruct the timeline and the contributing factors

Assemble what happened from the evidence, not memory: the onset, the detection, the mitigation, the diagnosis and the resolution, with timestamps. The evidence captured before mitigation and the confirmed mechanism are the spine of the record. Capture the *contributing factors*, plural, since incidents rarely have a single cause: the trigger, the gaps that let it reach production, and the reasons detection or recovery was slow are each a factor worth a follow-up.

## Frame it blamelessly

Write the analysis per [blameless-framing](../../../craft/writing/blameless-framing.md): describe what the *system* allowed to happen, not who erred. Every "X did Y" becomes "the system let Y happen with no guard", and each missing guard becomes a candidate follow-up. Keep the human actions in the timeline as fact; aim the fix at the system that permitted them.

## Name concrete follow-ups

Turn the analysis into work someone will do, not aspirations. A follow-up earns its place only if it is **concrete** (a specific change, not "improve monitoring"), **owned** (a person or team accountable) and **trackable** (fit to be filed where the team tracks work). The set usually includes the owed durable fix — or, when a rollback that removed the offending change resolved the incident, the forward re-fix and any dead-code cleanup as their own items — new or tuned alerts and guardrails, and runbook updates. Mark each one **gating** (a guardrail whose absence would let this exact incident recur, so it blocks "done") or **advisory** (an improvement worth doing). Filing them is the delivering act's job; the retrospective names them.

Where the project's runbook has its own retrospective template or severity vocabulary, use it ([match-the-runbook-conventions](../../triage/rules/match-the-runbook-conventions.md)) rather than inventing a format.

`(basis: Google SRE, "Postmortem Culture: Learning from Failure")`
