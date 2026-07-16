A committed approach is still not buildable — it says *what* to build, not the exact shapes a developer types. This phase turns the approach into contracts precise enough that two developers, handed them, build the same thing: the data model down to the column, the interfaces down to the field, and a clear placement for every piece of logic. The bar is convergence — an interface specified so loosely that two builders make incompatible choices has not been specified.

## Design the implementation data model

Move from the logical entities to the actual storage: schema, keys, indexes, and the migrations that get from the current shape to the new one. Let the data's realities drive it — the shape, volume, access pattern, and lifecycle you characterized in mapping ([follow-the-data](../rules/follow-the-data.md)) decide what is normalized, what is denormalized for a hot read, and what is indexed. A data model that ignores the hottest query or the growth rate is where the design will later buckle.

## Define the interface contracts to the field

Specify each interface the change introduces or alters down to the field: request and response shapes, types, status codes, the error cases and what each returns, pagination and idempotency where they apply. For an **external** interface being integrated, recruit the `official-documentation` explorer **directly** — this is a single-lane read against a known source (the vendor's contract), not a multi-lane synthesis, so it does not go through `gather` — and pin the authoritative request/response contract rather than inferring it. If the external interface is **unnamed or its contract is not yet knowable**, do not block and do not silently infer one: record the dependency as a load-bearing assumption ([surface-assumptions](../rules/surface-assumptions.md)) and a spike to run before build ([slice-and-validate](06-slice-and-validate.md)), so the unknown is explicit rather than baked into the design as fact.

## Place the boundaries and the logic

Decide where each piece of logic lives — client versus server, which service, synchronous versus asynchronous — and draw the component boundaries. Put each seam where change and ownership actually diverge, so a future edit stays local ([seam-along-change-boundaries](../rules/seam-along-change-boundaries.md)); that rule places the boundary, while [justify-every-moving-part](../rules/justify-every-moving-part.md) governs whether a new component or abstraction between them has earned its place at all. Match the layering and idiom the surrounding code already establishes rather than importing a foreign structure ([match-existing-conventions](../rules/match-existing-conventions.md)). Then state the component-level plan: what changes where, and which new parts appear.

The output is field-level contracts plus a component-level plan of what changes where — the exact shapes [working-the-hard-parts](04-working-the-hard-parts.md) pressure-tests on the tricky flows.
