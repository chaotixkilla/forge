# upgrade — usage

Move a dependency to a new version: read what its publisher says changes across the span, capture how the project's checks stand now, grade the bump's reach, bump it the way the project pins, fix what breaks at its cause, and prove the checks green again.

## When to use
- A dependency needs a new version — a security fix, a feature you need, or keeping current — and you want the bump sized to what it actually moves.
- A major version is due and you want it taken from its migration guide, one major at a time, not by trial and error.

## Not for / use instead
- Restructuring code without moving a dependency → **refactor**.
- Replacing a dependency with a different one → **develop**.
- Finding why something broke → **debug**.
- Carrying an upgrade through review, records and delivery → the maintaining act in **work**, which runs upgrade as its change step.

## Examples
`upgrade` — read the path, baseline, grade, bump and fix, prove it green, and commit.
`--checkpoint-commit` — commit after each major taken in sequence.
`--changelog` — add a changelog entry in the project's own format.
`--dry-run` — report the versions, upgrade path, risk tier and intended bump without changing anything.

## Gotchas
- **The publisher's record comes first.** Changelogs and migration guides are read through gather before anything is bumped; memory of the library isn't a source.
- **Majors go one at a time.** A jump across several majors is taken in sequence, each green before the next.
- **Unknown reach grades high.** A bump that moves a co-importer deploying on its own schedule, with no in-scope way to migrate it, is blocked and reported.
- **It commits locally and stops.** upgrade never pushes, opens a review request or records anything outside the repository.
- **In a project set up for praxis, it changes code only inside an act.** Invoked on its own there, its edits are blocked until an act starts; the work skill routes the change to the act that runs it.
