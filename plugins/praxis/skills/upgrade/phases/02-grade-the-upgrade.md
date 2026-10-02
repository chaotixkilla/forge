Starting from the versions and consumers [phase 01](01-read-the-upgrade-path.md) located, map what the bump actually moves and grade it *before* anything is bumped. The miss this prevents is underestimated reach: a "patch" that changes how a shared copy behaves for a co-importer that deploys on its own schedule, or a minor whose changelog quietly changes a default your call sites lean on.

## Map what the bump moves

Trace outward from the dependency (**judgment** — depth follows the reach you keep finding):

- **Your call sites** — where a behavioral delta in the dependency would land, and which of the changes read in phase 01 touch them.
- **Co-importers** — anything else that resolves the same copy, and whether it deploys with this change or on its own schedule. Whether a co-importer counts as a consumer this bump moves turns on the resolution topology ([change-risk-scale](../../../craft/engineering/change-risk-scale.md)).
- **Contracts** — a surface you export, or persisted data, that the dependency's types or formats reach. A change to one is governed by [preserve-the-contract](../../../craft/engineering/preserve-the-contract.md).

## Pull prior gotchas

Has this dependency been bumped before, and what bit last time? Read the change history and prior reverts around its manifest entry directly (an ambient version-control-history read), and any linked discussion through the port that holds it: a tracked item through [project-mgmt](../../project-mgmt/SKILL.md)'s *fetch a work-item*, a review request through [vcs](../../vcs/SKILL.md)'s *read a review request*, a chat thread through [communication](../../communication/SKILL.md)'s *read a thread*. When a call site's purpose isn't self-evident, recover it before adapting it ([decode-intent-from-history](../../../craft/engineering/decode-intent-from-history.md)).

## Stress the map with future-self

Recruit the [future-self](../../../agents/critics/future-self.md) critic to ask the questions the author skips: *when this upgrade goes wrong six months from now, what breaks, and can it be backed out?* Hand it [change-risk-scale](../../../craft/engineering/change-risk-scale.md) with the recruit, so its answer comes back on the tiers' own reach-and-reversibility axes. Fold its findings into the reach map. **Without fan-out**, apply the lens yourself — walk the upgrade forward: if it fails in production, what's the blast radius, and is the rollback a clean revert or a data-stranding mess? Recruit only as [fan-out-only-when-it-pays](../../gather/rules/fan-out-only-when-it-pays.md) allows.

## Grade the upgrade

Assign the upgrade its risk tier (**contained / bounded / exposed**) on [change-risk-scale](../../../craft/engineering/change-risk-scale.md), by its dependency-upgrade grading: the *worse* of its reach (who the bump moves) and its delta (bounded by the increment, discharged by the safeguards in [dependency-upgrade-posture](../rules/dependency-upgrade-posture.md)). The grade is provisional on the intended bump until [prove-it-green](04-prove-it-green.md) confirms or escalates it.

## Output

The reach map (call sites, co-importers, contracts), the migration steps from phase 01 that the call sites need, and the **risk tier with the action it forces** — the input [bump-and-fix](03-bump-and-fix.md) acts on.
