`--inputs-only` restricts the gather to what can be audited from inside the project, for runs that must not depend on the open web.

1. Consult only the provided/seeded inputs and the project-internal lanes — `code`, `repository`, `knowledge-base`; forbid the open-web lanes (`official-documentation`, `authoritative-literature`, `community-practices`) entirely.
2. A question that can only be answered by a forbidden lane returns a documented gap — `unanswerable under --inputs-only: needs the <lane> lane` — never a quiet best-guess from a project-internal lane standing in for authority.
3. The sourcing model still governs what remains: within the project-internal tier, `code`/`repository` outrank `knowledge-base` on what-is-true-now (see [sourcing-model](../rules/sourcing-model.md)).
