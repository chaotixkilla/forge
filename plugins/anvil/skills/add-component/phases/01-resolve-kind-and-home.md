Every component kind has exactly one canonical home in a plugin, and putting a file anywhere else breaks the contract silently: an adapter outside `adapters/` is read by the skill layer as a tool-leak, an agent outside `agents/` is never recruited, a module that lands in `rules/` reads as ungated craft. Before writing a byte, this phase pins down *what* you're adding and *where the one right place for it is* — because the rest of the skill (mirroring siblings, wiring up) is parameterized entirely by that decision. Get the home wrong here and every later phase compounds the error.

## Require the inputs that name the component

Three inputs are non-negotiable: `--plugin` (which target tree), `--kind` (which sort of component), and `--name` (the component's filename). The file lands as `<name>.md`. If `--name` is absent for an adapter, default it to `--tool` — the provider an adapter wraps *is* its natural name, so an adapter for a given provider's calls is named after that provider. For every other kind, a missing `--name` is a stop-and-ask: don't guess a filename from the kind, because the name is a design choice the maintainer owns (a critic's lens, a rule's craft-noun, a module's flag).

If any required input is missing, stop and ask rather than inventing one. A scaffold built on a guessed target is worse than no scaffold — the maintainer has to find and undo it.

## Map the kind to its canonical home

Each kind resolves to a fixed directory; this mapping is the whole point of the phase:

- **adapter** → `skills/<skill>/adapters/` — adapters belong to the skill whose capability they implement, never to the plugin at large. This is why an adapter additionally requires `--skill`.
- **explorer** → `agents/explorers/` — agents are plugin-wide, recruited by whichever skill needs them, so they live at the plugin root, not under a skill.
- **critic** → `agents/critics/` — same altitude as explorers, separate folder by role (see [explorer-vs-critic](../rules/explorer-vs-critic.md)).
- **rule** → `skills/<skill>/rules/` — a-la-carte craft attached to one skill.
- **module** → `skills/<skill>/modules/` — flag-activated behavior attached to one skill.
- **hook** → `hooks/` — lifecycle handlers are plugin-wide, like agents.

The split is altitude: adapters, rules, and modules are *parts of a skill* and nest under it; explorers, critics, and hooks are *plugin-wide* and sit at the root. Memorize that division and the home falls out of the kind.

## Require the kind-specific inputs

Three kinds attach to a specific skill and so demand `--skill`: **adapter**, **rule**, and **module**. Without it there is no `<skill>/` segment to resolve the home into — stop and ask. Adapters need one input more: `--tool`, the provider/transport the adapter wraps. `--tool` is the *only* input in this whole skill that legitimately names a concrete tool, because it names the thing the adapter exists to encapsulate; everywhere else, naming a tool is the leak the kit audits for.

Explorers, critics, and hooks take no `--skill` — they're plugin-wide and bind to skills later, at wire-up, by being recruited rather than by living under a skill.

## Confirm it doesn't already exist

Send the plugin explorer to read the resolved home, then branch on **whether the collision was intended** — which the executor does not infer from context, it reads from the invocation:

- **`--extend` given** — the maintainer means to change the component that is already there. This is the edit lane, not a collision: proceed, and phase 3 revises the existing body instead of composing a new one. If `--extend` is given and *no* file exists at that name, stop and say so rather than silently creating one — an extend that finds nothing is a wrong `--name` or a wrong home, and creating the file would hide the mistake behind a plausible result.
- **`--extend` absent** — treat an existing file as a genuine collision. Do not clobber it: stop and surface the choice — re-run with `--extend` to change it, pick a different name, or abort. Silently overwriting is the worst outcome, because the maintainer loses authored work with no diff to recover it from.

Intent is read from the flag rather than asked, because this skill is dispatched programmatically as often as it is invoked by hand — a lane that resolves the ambiguity by asking cannot be reached by a caller that has no one to answer. `(basis: derived — the collision guard already named extending as a legitimate outcome while offering no lane that performs it, so the gap was a missing branch, not a missing question; a flag is the only discriminator a dispatching caller can supply.)`

Reading the home now also feeds the next phase, which mirrors whatever siblings already live there.

Anti-pattern: resolving the home from `--kind` but skipping the existence check, then having phase 3 overwrite a sibling. The check costs one read and prevents the one truly destructive failure this skill can cause.

For an **adapter** specifically, the existence check runs one level up too: before adding a skill-local adapter for a capability, confirm the plugin doesn't *already own that capability as a shared port*. If it does, a local adapter is the wrong component — the consumer should delegate to the port and declare no adapter of its own. Verify against the tree, not against a seed's "first consumer / no port yet" claim, which goes stale as the plugin grows; the full guard (and why a duplicate breaks the single-owner seam) is [port-and-adapter-seam](../rules/port-and-adapter-seam.md).

## Under `--dry-run`

Resolve everything — inputs, home, sibling inventory — and report the exact path the file *would* land at, but write nothing and proceed no further into the writing phases. The maintainer is asking "where would this go?"; answer precisely and stop.
