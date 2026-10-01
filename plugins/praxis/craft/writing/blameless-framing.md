# Blameless framing

The retrospective's job is to make the next incident less likely, and that depends entirely on people telling the truth about what happened. The moment a postmortem names and shames, the reporting dries up — responders hide the near-misses and the "I ran the wrong command" moments that are exactly the signal prevention needs.

## The method

- **Rewrite every "X did Y" as "the system let Y happen with no guard."** "An engineer deployed to prod on a Friday and took it down" becomes "a deploy with a known-bad config reached prod because no gate caught the config, and the rollback took 40 minutes because it was manual." The human action stays in the timeline as fact; the *analysis* targets the missing guard.
- **Turn each missing guard into a follow-up.** The guard that would have caught it — the gate, the validation, the alert, the faster rollback — is the concrete prevention item (the retrospective names it).
- **Treat human error as a signal, not a cause.** If a person could take the action that caused the incident, the system permitted it; "be more careful" is not a fix, a guardrail that makes the mistake impossible or cheap to undo is.

## The discriminator — blameless is not accountability-free

Blameless does not mean the action is erased or that nobody owns the follow-up. The action is recorded honestly in the timeline (you cannot fix what you won't name), and follow-ups have owners. What blameless forbids is making a *person* the root cause and stopping there — because that ends the investigation exactly where the systemic fix begins. The test: does the analysis end at "human made a mistake," or does it continue to "the system allowed the mistake"? Only the second is done.

`(basis: Google SRE, postmortem culture)`
