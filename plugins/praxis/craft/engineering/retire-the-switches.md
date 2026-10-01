# Retire the switches

A rollout that puts a change behind a switch (a feature flag or toggle) installs debt. Every switch left in place keeps a dead branch, a second path to test, and a config value nobody remembers the reason for, so the rollout that installs one owes its removal.

## When a switch is installed

The rollout records two things at the switch's declaration, in the code or in the description its flag service keeps, so whoever finds the switch finds them: who owns removing it (whoever installs it, unless the rollout names someone else), and the date or condition that ends it, such as fully rolled out or rolled back. A switch without both is incomplete. The condition is attached when the switch is born, as part of the change that adds it, never as a someday-ticket.

## Retiring one

Retiring a switch is a maintenance change:

1. Find the switches past their removal date or condition, from the records at their declarations and from the code's own flag reads. A switch with no record is reported as incomplete and left in place.
2. Confirm the rollout ended, from a record of the switch's values (the version history of the config that sets it, or the change log its flag service keeps): it has held one value across its whole exposure for the period its rollout named, with no rollback pending. With no such record to read, report the switch and leave it.
3. Remove the switch read and the branch it no longer takes, as one scoped change, verified like any other.
4. Leave the switch's config value for a follow-up, reported with the change: it can go once the code that reads it is gone everywhere it deploys.

A switch whose rollout hasn't ended stays, and its owner and date are reported.

(basis: after growthbook's flag lifecycle, which ends in cleanup; rollout planning that gives every toggle a removal owner and date)
