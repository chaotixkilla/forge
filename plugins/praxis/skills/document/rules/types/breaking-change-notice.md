# Breaking-change notice

The notice to whoever consumes an interface, schema, event or file format that this change breaks or alters: what breaks, from when, and what to change.

## Reader and question

A maintainer of code that calls or reads the contract, machine clients and integrations included, and support answering them: "Does this break my integration, by when, and what do I change?"

## Page

`own page`

## Membership

Each element of a contract consumed outside the change whose compatibility class is breaking or behavioural. A compatible change isn't listed. What people using the product are told is the [communications-plan](communications-plan.md)'s. Its subject is the task's changes to contracts others consume, so a task has one. It is filed again when an element is added, reclassified or redated.

## Items

**Breaking change `BRK`.** One changed element: a field, an endpoint, a default, a format, a value set, a header, an access rule. Its body shows the element before and after.

- `class`: enum `breaking`, `behavioural`. `breaking` when an existing caller that is correct today fails or misreads the result without changing its code; `behavioural` when the shape is the same but the effect differs in a way a caller may rely on.
- `breaks`: list of enum `source`, `wire`, `semantic`. (basis: Google AIP-180)
- `rule`: enum `removed or renamed`, `new required field`, `type changed`, `default changed`, `format changed`, `values added`, `limit changed`, `pagination added`, `newly refused`. The last is a caller an enforcement step starts refusing. (basis: Google AIP-180; `newly refused`, prototype sweep, 2026-11-11, machine clients refused by new enforcement)
- `who`: text. The consumers affected, machine clients and integrations named apart from people.
- `deprecated on`: when, and `sunset on`: date. `sunset on` may stay missing until a `removed at` gate is filed. The least notice between the two is the project's policy, or else the decider's call, recorded in the body. (basis: no standard pins a minimum notice, so it is open by design)
- `migration`: text. A link to the migration guide.
- `signals`: text. The machine-readable signals consumers receive, such as deprecation and sunset headers with a link to this notice. (basis: RFC 9745)
- `removed at`: id. The `contract` `GATE` that removes the old form, when a cutover plan is owed.

Live field: `old-form calls`, number, `telemetry: calls in the last day still using the element's old form`.

Agreement `needed`, change regime `baseline`. Its decide-by is its `deprecated on`.

Shows `GATE` (home: [cutover-plan](cutover-plan.md)).

## Sections

1. **What breaks, and for whom?** Always. The change table.
2. **By when?** Always. The deprecation timeline.
3. **What do I change?** Always. The migration cards.

## Checks

*Computed:*
- Every change has its class, breaks, rule, who, deprecated on, migration and signals, and its sunset on once a `removed at` gate is filed.
- Sunset is no earlier than deprecation. (basis: RFC 9745, after RFC 8594)
- A `breaking` change has a `removed at` gate with an opens-on date when a cutover plan is owed.

*Judgment:*
- An element left out as compatible that changes a default, a format or a value set. (basis: Google AIP-180)
- A semantic change, the same call meaning something else, filed as compatible.
- Machine clients and integrations not named, above all those a new enforcement step refuses.
- A prose notice with no machine-readable signal.
- A `contract` gate opening while old-form calls are above zero, with no go-when criterion on them.

## Views

- **Change table:** `table` of every `BRK`, sorted by class, breaking first: class, breaks, rule, who, sunset on, old-form calls.
- **Deprecation timeline:** `timeline` of every `BRK` from deprecated on to sunset on.
- **Migration cards:** `cards` of every `BRK`: its body (the before and after), migration, signals.

## Minimum form

Each section keeps its heading with one line: no element is classified yet, and who classifies them.
