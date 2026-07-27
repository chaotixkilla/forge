# security-pass (`--security`)

Activated by `--security`, referenced from [verify-and-guard](../phases/04-verify-and-guard.md).

Every maintain run applies the always-on security baseline ([distrust-untyped-input-and-secrets](../rules/distrust-untyped-input-and-secrets.md)) — taint and secret hygiene on the code the change touches. This module **escalates** that baseline to a full security/compliance pass and **gates completion on it** rather than treating it as advisory: with `--security` set, the change is not done until the pass clears its bar. **Deletion test:** remove it and maintain still applies the baseline hygiene and lands; the dedicated audit and the completion gate are the added, flag-gated behavior.

## The delta

- **Delegate the audit to [security-review](../../security-review/SKILL.md)**, scoped to the change (its diff and blast radius) — the dedicated threat audit that covers authn/authz, injection, secret handling, data exposure, and supply-chain/dependency-advisory checks. maintain does not re-implement the threat model; it recruits the skill that owns it and consumes its severity-ranked findings. The signals that audit reads are in turn delegated to the [telemetry](../../telemetry/SKILL.md) and [ci](../../ci/SKILL.md) skills.
- **Without fan-out, or where security-review isn't reachable,** apply the security-auditor lens inline: recruit the [security-auditor](../../../agents/critics/security-auditor.md) critic to hunt injection, broken authz, secret exposure, and tainted-data paths across the change, handing it [security-review's severity scale](../../security-review/rules/severity-scale.md) to grade on; without that agent either, apply its lens yourself — follow tainted input from each entry point to its sinks and confirm every secret is referenced, not embedded — and grade what you find on that same scale.

## The blocking bar — reuse, don't mint

`--security` gates completion, and a gate needs a blocking bar. **Reuse security-review's severity scale and its ratified gate floor** rather than minting a fresh one — the security lens is that skill's domain, and a second, subtly-different scale is exactly the divergence a shared scale prevents.

- **Grade findings on [security-review's severity scale](../../security-review/rules/severity-scale.md)** (CVSS-sourced: critical / high / medium / low).
- **Block completion on any finding at or above the floor.** The floor is `security-review`'s ratified default gate floor — **high** (the pass fails on high and critical findings; medium and below are advisory and surfaced, not blocking) — unless the caller sets a stricter minimum via a severity-min. State the floor in the output either way, so a blocked run says *what* bar it failed.
- **A blocked run resolves to `blocked-and-reported`** in [review-and-record](../phases/05-review-and-record.md)'s disposition — the change does not land until the blocking findings are resolved (fix the cause, then re-run the pass) or the maintainer explicitly lowers the bar.

`(basis: reuse security-review's severity scale (CVSS qualitative bands) and its maintainer-ratified default gate floor of high+critical — do not mint a fresh scale for maintain. The reuse is ratified by the maintainer, 2026-07-11.)`

## Degraded

If the security capability can't complete the audit (security-review unreachable and the inline lens can't run, or the signals it needs are unavailable), the pass is **inconclusive** — and because `--security` *gates*, an inconclusive pass must never read as a pass. Report can't-verify distinctly and do not land as if clean; defer to the owning skill's `if_missing` posture. "We couldn't check" is not "it's clean."
