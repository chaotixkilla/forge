# Backup and restore plan

How state that a change moves into a service another organisation runs is copied and restored, how much a restore loses and how long it takes, and whether anyone has done one.

**Reader and question.** On-call: "if this data is lost or its provider fails, how do we get it back, what do we lose, and has a restore ever worked?"

**Page.** `on the vendor-review page`

## Membership

The plan the outside-service concern owes for state that moves, during the build. It holds a restore path for each set of data at risk. Data that can't be restored is a path whose `copy` is `none`, with why in its body, and the agreement on it records who accepted the loss. Undoing a deploy is the [cutover plan](cutover-plan.md)'s. A one-way gate's restore there is one of the paths here, and the gate `rests-on` it. The commands an operator runs belong to a [runbook](runbook.md) procedure when a runbook is owed. Otherwise they are in the restore path's body.

The type is operational: restore paths stay in use after the task closes.

A task has one. It is filed again when a path is added, its copy, frequency or targets change, or a restore is tested.

(basis: maintainer, 2026-11-11, from the prototype sweep: state moving into a vendor had no backup or recovery plan, and one-way gates demanded a tested restore. The research read no source on restore targets, so the loss and time fields are the common recovery-point and recovery-time terms, unsourced.)

## Items

**Restore path `RST`.**
- Fields:
  - `restores` id, the vendor, or the data-store element, log stores included, that holds the state;
  - `data` text, which data, and which copy is the source of truth;
  - `against` list of enum `deletion`, `corruption`, `provider outage`, `provider loss`, what it recovers from. Provider loss is losing the account or the provider for good;
  - `copy` text, where the copy is kept and who can start a restore from it, or `none` when the data can't be restored;
  - `frequency` text, how often a copy is taken, as a period;
  - `loss target` and `loss achieved` text, the most recent data a restore may lose, and did lose, each as a period;
  - `time target` and `time achieved` text, how long a restore end to end may take, and did take, each as a period;
  - `kept` text, how long copies are kept, as a period;
  - `tested` date, the latest restore that succeeded. Set, with `loss achieved` and `time achieved`, only from a restore verification in its evidence, which records the environment, how much data and how long it took;
  - `procedure` id, the runbook procedure that holds its steps, when there is one.
- Granularity: one set of data restored from one copy. The same data restorable from two copies, ours and the provider's, is two paths.
- Change regime: `baseline`.
- Agreement: `needed`. Its decide-by is the gate that `rests-on` it, when one does; otherwise the plan's fallback for this type's due point ([items-and-agreements](../items-and-agreements.md)).
- Live fields: `last copy`, date — telemetry: when the newest copy completed.

## Sections

1. **What would we lose, and how long would it take?** Always. The restore view.
2. **What can't we get back?** When a path's `copy` is `none`. Each, with why, and the agreement that accepted losing it.
3. **How do we restore it?** Always. For each path, its steps or its procedure, and its latest restore test: when, where, how much data, and how long it took.

## Checks

- *Computed.* `frequency`, the targets and `kept` may be `unknown`, which a judgment check catches at the gate that rests on the path, or else at `build start`:
  - every vendor whose `holds state` is `source of truth` has a path that `restores` it, one whose `copy` is `none` when it can't be restored;
  - `restores` names a vendor or an element that is a data store or a log store;
  - `frequency`, `loss target`, `loss achieved`, `time target`, `time achieved` and `kept` are periods, as the [privacy screening](privacy-screening.md) defines one.
- *Judgment:*
  - the provider's own backup counted as ours, when we can't start a restore from it;
  - a copy kept with the same provider or account, so losing the provider loses both;
  - a restore that needs the provider that just failed;
  - a restore tested on far less data than production holds, so `time achieved` is a guess;
  - loss and time targets nobody agreed;
  - copies kept longer than the data's retention in the privacy screening;
  - a field still `unknown` at the gate that rests on the path, or at `build start` when no gate does.

## Views

- Restore: `RST` as a `table`, sorted by `tested`, ascending, empty first: untested paths, then the oldest test first: title, data, against, copy, loss target, loss achieved, time target, time achieved, tested, `last copy`, owner.

## Minimum form

Each set of data at risk named with `restores` and `data`, its targets `unknown`, `tested` empty, "nothing known to be unrecoverable yet", and "no restore steps yet".
