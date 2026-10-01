# Match the project's security posture

A generic checklist produces generic noise: it flags the absence of a control the project deliberately doesn't use, misses the deviation from a guarantee the project actually makes, and buries the one finding that matters under a dozen that don't. The change's job is to defend this system the way this system defends itself — to uphold the controls and conventions the codebase already establishes.

## The standard is how this codebase already defends itself

Before flagging a missing or weak control, read how the project handles the same concern elsewhere: how it authorizes actions, where and how it validates input, how it stores and passes secrets, how it scopes tenant data, what it pins and verifies in its supply chain. Then judge the change against *that* established bar. A change that upholds a strong local convention is sound even if you'd have built the defense differently; a change that breaks one the codebase consistently keeps is a real finding even if the gap is defensible in the abstract — inconsistency in a security control is itself an exploitable seam.

## The discriminator, and the two overrides

The test for a posture-based finding: **does this diverge from a control the surrounding code actually establishes?** If the neighbors guard this boundary and the change doesn't, that is the finding; if the project is uniformly silent on a control and the change simply doesn't add one you'd prefer, that is a hardening suggestion, not a deviation — hold it to [separate-finding-from-noise](separate-finding-from-noise.md). Two overrides, and only these, keep the anchoring honest:

- **A reachable, exploitable defect is never excused by convention.** If the whole module builds queries by concatenation and the change does too, the shared pattern is a shared vulnerability — flag it at the change's site and name the pattern. A convention can make a *hardening nit* moot; it cannot make a reachable breach acceptable.
- **A posture the project is actively moving toward** — where recent changes or a stated direction show the old pattern being replaced — is judged against the new direction, said so explicitly. Absent that evidence, the established convention wins; do not infer a migration from your own preference.

The project's posture is the **surrounding-convention tier** of the fork-routing rule the framework and taxonomy defaults use ([modeling-the-threats](../phases/02-modeling-the-threats.md), [hunting-vulnerabilities](../phases/03-hunting-vulnerabilities.md)): when the codebase's own practice settles a contested call, it wins over the house default.

`(basis: derived from [match-the-surrounding-code](../../../craft/engineering/match-the-surrounding-code.md)'s neighborhood standard)`
