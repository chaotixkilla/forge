# Suspect the recent change first

Most incidents are self-inflicted: something changed, and the change broke it. So diagnosis does not start from a blank hypothesis space — it starts weighted toward what changed most recently and closest to the symptom, and only widens to exotic causes (a slow resource leak, a traffic-shape shift, a dependency's silent regression) when the recent-change hypotheses are exhausted. This rule is the ordering discipline for [diagnose-root-cause](../phases/03-diagnose-root-cause.md); it makes the search converge instead of wandering.

## The method

- **Anchor on the onset.** Establish when the signal first crossed — the seam a regression crossed — not when it was noticed. The onset is the timestamp everything else lines up against.
- **Line the onset up against the change timeline.** Correlate it with recent deploys, config changes, feature-flag flips, infra changes, and dependency updates in the same window. Recruit the [repository explorer](../../../agents/explorers/repository.md) for the code/deploy history; a failure that appeared at a known time is most often a change at that time.
- **Test the nearest recent change first.** Order hypotheses by recency-and-proximity: the deploy that landed minutes before the onset, touching the failing path, is the first suspect — before a theory about a rarely-hit edge case.

## The guard

Recency is a **prior, not proof**. A change that correlates with the onset is a hypothesis to confirm against evidence ([change-one-thing-at-a-time](change-one-thing-at-a-time.md)), not the confirmed cause — correlation in time is where the search *starts*, and the mechanism still has to be shown. And when nothing recent correlates, that itself is a finding: widen to the slow-onset causes (leaks, saturation, data growth, an upstream change) rather than forcing a recent change to fit.

`(basis: SRE operational practice — the strong empirical prior that production incidents trace to a recent change, so correlating the failure window against the deploy/config timeline is the highest-yield first move; this is the operational twin of debug's suspect-recent-change instinct, applied to a live signal rather than a filed bug.)`
