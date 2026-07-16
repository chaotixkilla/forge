With service restored (or safely mitigated), the pressure is off enough to find *why* it broke — the real cause, not the nearest symptom. This phase forms falsifiable hypotheses, tests them against evidence, and narrows to a confirmed mechanism. It runs after stabilization by design: diagnosing while the incident is actively burning trades users' time for the responder's curiosity, which [mitigate-before-diagnose](../rules/mitigate-before-diagnose.md) forbids. (For a stood-down or purely mitigated-and-handed-off run, this phase may be light or deferred — but a durable fix needs a confirmed cause.)

## Weight the recent change, gather the evidence

Start where incidents actually come from: apply [suspect-recent-change-first](../rules/suspect-recent-change-first.md) — anchor on the signal's onset and correlate it against the deploy/config/flag timeline before chasing exotic causes. Gather the evidence around the failure:

- the **failing path and its state** — recruit the [code explorer](../../../agents/explorers/code.md) to trace the route from entry point to the symptom site;
- **what changed near the symptom** — the [repository explorer](../../../agents/explorers/repository.md) for recent commits, blame, and history in the suspect window;
- the **recorded signals** — telemetry, traces, and logs through the [telemetry](../../telemetry/SKILL.md) port (or a local log by direct read), plus any volatile state captured in [stabilize-first](02-stabilize-first.md);
- and where the failure has a known signature, prior occurrences via the [community-practices explorer](../../../agents/explorers/community-practices.md).

Without fan-out, walk each of these lanes yourself in sequence before proceeding — the delegation is optional, the evidence is not.

## Form hypotheses and test them — one variable at a time

Turn the evidence into falsifiable hypotheses, and test them under [change-one-thing-at-a-time](../rules/change-one-thing-at-a-time.md): vary a single factor per experiment, observe, and record before the next — batched changes destroy attribution. Distinguish a causal signal from residual jitter as you narrow ([real-signal-vs-flapping](../rules/real-signal-vs-flapping.md) applies here too: a metric still settling after mitigation is not necessarily part of the mechanism).

Before a leading hypothesis stands, attack it. Recruit the [adversary critic](../../../agents/critics/adversary.md) to construct the case the hypothesis does *not* explain — an input or state where the supposed cause is present but the failure doesn't follow, or the failure occurs without it — and the [assumption-hunter critic](../../../agents/critics/assumption-hunter.md) to surface the unstated premise the hypothesis rests on. Without fan-out, run both lenses yourself: state the strongest case that this is *not* the cause, and keep the hypothesis only if that case fails.

## Narrow to the confirmed cause — the loop and the done-state

Diagnosis is a loop, not a waterfall: gather → hypothesize → test → narrow, cycling until the mechanism is confirmed. A cause is **confirmed** when you can show the mechanism — the cause→symptom chain, demonstrated against evidence — not merely a correlated recent change or a plausible story. A correlation in the change timeline is where the search started; it is not a confirmed cause until the mechanism is shown.

Done-state: a confirmed root-cause mechanism (the cause, the chain to the symptom, and the evidence for it) ready for [remediate-and-verify](04-remediate-and-verify.md) to fix durably — or, if the cause cannot be confirmed, the leading hypothesis and the specific evidence that would confirm or kill it, carried forward honestly rather than a guess dressed as a finding.
