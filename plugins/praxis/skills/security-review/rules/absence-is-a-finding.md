# Absence is a finding

A code review reads what is written; a security review must also read what is *missing*. The most damaging vulnerabilities are often not a wrong line but an absent one — the authorization check that was never added, the validation that no one wrote, the rate limit that doesn't exist. A missing control has no line to point at, so a line-by-line read slides right past it: nothing looks wrong because nothing is there. This rule is the discipline of hunting the control that *should* exist against the surface's own requirements, not just judging the controls that do.

## Read for the owed control, not the written one

For each boundary and sink the surface exposes, name the defense the situation demands and check whether it is present:

- **Authorization** — an action on a resource: is there a check that *this* caller may act on *this* object, not merely that they are authenticated? A missing ownership check is invisible precisely because the happy-path caller owns their object.
- **Validation / encoding** — an input reaching a sink: is it constrained or escaped, or does it arrive raw?
- **Rate / resource limits** — an expensive or security-sensitive operation an attacker can repeat: is there anything bounding it (a limit, a lockout, a quota)?
- **The other half of a pair** — authentication without authorization, a check on read without one on write, encryption in transit without it at rest.

Anchor the finding at the site where the control *belongs* (the handler that skips the check), since there is no offending line to cite.

## The discriminator: an owed absence, not a wished-for one

The gilding trap is real — you can always name one more control that *could* exist, and demanding controls the situation never required is this rule's characteristic noise. So a missing control is a finding only when its absence is **reachably abusable**: name the adversary and the concrete abuse the absence permits ([confirm-reachability-before-flagging](confirm-reachability-before-flagging.md)), and hold it to the exploitable-vs-hardening line ([separate-finding-from-noise](separate-finding-from-noise.md)). The test: **is the control owed by this surface's own trust boundaries and the project's own posture ([match-the-projects-security-posture](match-the-projects-security-posture.md)), and does its absence let a reachable attacker do something?** Owed-and-abusable is a finding; merely-conceivable is defense-in-depth, kept out of the ranked list.

`(basis: missing-control analysis is core to threat modeling — the DFD-and-STRIDE method asks per element which controls are owed, not only which are present; the method, not a graded bar.)`
