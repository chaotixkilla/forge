# Vendor review

What a change takes on by relying on a service another organisation runs, or a dependency it adds: what each receives and keeps, the limits of its plan, what may change under us, and how we would leave.

**Reader and question.** Decider (whether to take the dependency on), and maintainer: "what are we committing to by relying on this, and can we live with it?"

**Page.** `own page`

## Membership

The review the plan's outside-service concern owes, before the build. It covers each service the change starts relying on or moves state into, and the direct dependencies the change adds or upgrades. No per-change template exists for this review, so its fields and checks are derived from the sources marked and from what the field prototype missed, which the checks carry. (basis: research, 2026-11-11; maintainer, 2026-11-11)

Threats on the flows to a provider belong to the [threat model](threat-model.md), where its service is an element. What a recipient of personal data changes in the record of processing belongs to the [privacy screening](privacy-screening.md). Restoring what a provider holds belongs to the [backup and restore plan](backup-restore-plan.md), which fills this page's section on it.

A task has one. It is filed again when a vendor is added or dropped, or its plan, limits, terms, regions or the data it receives change.

A vendor's entry names which secrets it holds, or we hold for it, and who rotates them. Names of secrets and of who rotates them, and categories of data received, are `team`; storage locations and values never appear.

## Items

**Vendor or dependency `VEN`.**
- Fields:
  - `kind` enum `service`, `library`;
  - `provider` text, who runs or maintains it;
  - `version` text, a library's pinned version, or the API version of a service;
  - `licence` text, a library's licence;
  - `provenance` text, a library's build provenance level as its publisher states it, or "none stated" (basis: SLSA; what v1.2 changed since v1.0 wasn't verified);
  - `plan` text, a service's plan or tier, and a link to its terms;
  - `limits` list of text, each cap of the plan, such as requests, seats, storage or jobs, with its value and the use expected at peak;
  - `early access` list of text, each feature in use that is in preview, beta or early access, with its terms;
  - `commitment` text, the availability it commits to and where, or "none";
  - `receives` list of text, the data it receives, with personal data named as such;
  - `region` text, where it processes and stores that data;
  - `retention` text, how long it keeps the data, as a period;
  - `holds state` enum `source of truth`, `copy`, `none`;
  - `exit` text, how we would leave: how our data comes out, and what notice either side owes;
  - `secrets` list of text, the secrets it holds or we hold for it;
  - `rotated by` text, who rotates them.
- Granularity: one thing relied on that is versioned or contracted on its own. A service and its SDK are two items when the SDK is pinned separately.
- Change regime: `baseline`.
- Agreement: `needed`. No field is a `when`, so its decide-by is the plan's fallback for this type's due point ([items-and-agreements](../items-and-agreements.md)).
- Live fields: `usage`, list of number — telemetry: the latest observed use against each of `limits`, in order.

## Sections

1. **What are we taking on?** Always. The vendor view, each with the agreement that accepted it.
2. **Where are we near a limit?** When a vendor has `limits`. The limits view.
3. **What do they receive and keep?** Always. The data view.
4. **What could change under us?** When a vendor has `early access` features, or its `commitment` is "none". Each feature or vendor, with its terms and what we would do if it changed or went away.
5. **How would we leave?** When a vendor is a service. Each service's `exit`, a source of truth first.
6. **Can we get our data back?** When the backup and restore plan is owed and shares this page. Its sections.
7. **Which libraries does it add?** When a vendor is a library. The library view.

## Checks

- *Computed.* Any field below may be `unknown`, which a judgment check catches at the build:
  - every service has `provider`, `plan`, `limits` (or "none stated"), `commitment`, `receives`, `region`, `retention`, `holds state` and `exit` (derived);
  - every library has `provider`, `licence`, `provenance` and a `version` that is one exact version, never a range (derived from SLSA and the NIST SSDF, whose 1.2 draft's status wasn't checked);
  - every `limits` entry has its value and its expected peak;
  - every `retention` is a period, as the [privacy screening](privacy-screening.md) defines one.
- *Judgment:*
  - an expected peak near a cap, with no plan for reaching it;
  - an early-access feature on a path users depend on, with no fallback;
  - a vendor that became the source of truth without anyone deciding it should;
  - a secret held by an outside service with nobody named to rotate it;
  - terms, regions or subprocessors taken on trust rather than linked;
  - no way out: data that can't be exported, or no exit stated;
  - part of the change rebuilding what the vendor already provides (basis: maintainer, 2026-11-11);
  - a field still `unknown` when the build starts.

## Views

- Vendors: `VEN` as a `table`, sorted by `holds state`, descending: title, kind, provider, holds state, receives, state, owner, and the covering agreement's decider, date and link.
- Limits: `VEN` with `kind` `service`, as a `table`: title, plan, limits, `usage`.
- Data: `VEN` as a `table`: title, receives, region, retention.
- Libraries: `VEN` with `kind` `library`, as a `table`: title, version, licence, provenance, provider.

## Minimum form

Each vendor named with its `kind` and `provider`, and every other field `unknown`.
