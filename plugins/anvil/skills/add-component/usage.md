# add-component — usage

Add one non-skill component — adapter, explorer, critic, rule, module, or hook — to a target plugin, in the one canonical place its kind belongs.

## When to use
- You have an existing skill and need to extend it with a part it consumes: an adapter to back a capability, a rule for craft it should reach for, a module for a flag-gated pass.
- You need a plugin-wide agent — an explorer to gather facts or a critic to challenge work — that skills will recruit.
- You need a lifecycle handler (hook) scoped to the plugin.
- The component slots into an established family and you want it to match the house style and land wired-up, not orphaned.

## Not for / use instead
- Creating a whole new skill's file skeleton (frontmatter + slots) → scaffold-skill. add-component adds a *part of* a skill; scaffold-skill births the skill shell itself.
- Filling a skill's procedure — turning a process into runnable phases → codify. add-component seeds a component's body; when that body is a real process (multiple decision points, sourced knowledge), it *hands off* to codify rather than free-handing it.
- Birthing a new plugin — its config posture, shell, and initial skill pool → new-plugin. add-component targets an existing plugin tree.
- Checking that flags↔modules, adapter coverage, and slot placement are wired correctly → audit-contract (add-component wires as it goes; audit-contract verifies after the fact).
- Checking a tool name didn't escape a skill into the layer that must name only capabilities → audit-tool-leaks.
- Checking that authoring-only files stay out of a shipping plugin → audit-packaging.
- Publishing the plugin / bumping its version / writing release notes → release.
- Proving the plugin's skills actually run end-to-end → dogfood.

## Examples
`--plugin=<plugin> --kind=adapter --skill=<skill> --tool=…` — add an adapter backing the target skill's capability for one provider; `--name` defaults to `--tool`, and the adapter is the *only* place a concrete tool is named. Wired via a dispatch line in the parent skill.
`--plugin=<plugin> --kind=rule --skill=<skill> --name=seam-discipline` — add a-la-carte craft under `<skill>/rules/`; nothing to wire — being cited by the phases that apply it *is* its registration.
`--plugin=<plugin> --kind=module --skill=<skill> --name=security` — add flag-gated behavior under `<skill>/modules/`; wiring is two steps — the file plus the activating flag declared in the parent skill's `metadata.flags`.
`--plugin=<plugin> --kind=explorer --name=convention-reader` — add a read-only gatherer under `agents/explorers/` (plugin-wide, no `--skill`); wired by adding it to a skill's recruit list where that skill gathers.
`--plugin=<plugin> --kind=critic --name=cold-executor` — add an adversarial lens under `agents/critics/`; wired into the recruit list where a skill challenges.
`--plugin=<plugin> --kind=hook --name=pre-publish-guard` — add a lifecycle handler under `hooks/` (plugin-wide, no `--skill`); wired by a hooks-manifest entry bound to the event.
`--plugin=<plugin> --kind=explorer --name=<existing> --extend` — change the body of a component that already exists, instead of creating one: revises it against its kind's bars and runs the three-lens gate on the merged result. This is the lane for a *method* edit to an adapter, agent, or hook — the component bodies codify cannot target.
`--plugin=<plugin> --kind=adapter --skill=<skill> --tool=… --dry-run` — resolve inputs, home, and sibling inventory and report the exact path the file *would* land at, writing nothing.

## Gotchas
- Always requires `--plugin`, `--kind`, and `--name`. Only an adapter defaults `--name` (to `--tool`); every other kind stops-and-asks on a missing name — it won't guess a filename the maintainer owns.
- `--skill` is mandatory for adapter, rule, and module (they nest under a skill); explorer, critic, and hook are plugin-wide and take no `--skill`.
- `--tool` is adapter-only and is the *single* input in this whole skill that legitimately names a concrete tool — everywhere else, a tool name is the leak audit-tool-leaks hunts for.
- It will not clobber: if a file by that name already exists and `--extend` was *not* given, it stops and surfaces the choice (re-run with `--extend`, rename, abort) rather than overwriting authored work. Intent is read from the flag, never inferred — this skill is dispatched programmatically as often as it is invoked by hand, and a caller with no one to answer a question still needs the lane.
- **`--extend` is the edit lane, and it is gated.** It holds the *merged* body to the same per-kind bars as a new one — a small edit that leaves the body short of its bar has not passed because it was small — preserves what already conforms rather than recomposing, and runs the cold-executor / standards-skeptic / economy-skeptic lenses on the result. Reach for it whenever an adapter, agent, or hook needs a method change; those bodies have no other owner, since agents and hooks are plugin-wide (no `--skill` for codify to take) and an adapter is the one file whose concrete tool names codify may not write. `--extend` with no file at that name stops rather than creating one.
- It mirrors the plugin's *existing* family for structure/headers/altitude — it does not import a convention from a different plugin or from the kit's own files. First-of-kind sets the convention, so it's built minimal, not padded with speculative sections.
- A component isn't done until it's registered: adapters get a dispatch line, agents a recruit reference, modules a flag, hooks a manifest entry. Rules are the exception — nothing to wire. An unwired component reads as dead code / an orphan to the next audit.
- **A family of same-kind agents whose recruiters are unbuilt** — author them in ONE pass against the ratified siblings, not `add-component` run N times: per invocation, phase 02 re-derives the family shape independently and the set drifts apart, when the whole point is that they read as identical siblings. Their wiring is legitimately *deferred* — an auto-discovering agent (explorer/critic) needs no registration until a skill recruits it, so when every recruiter is still unbuilt the wire-up is a genuine no-op, not a skipped step; each is added to its recruiter's recruit-list when that recruiter is built. And gate the family *against the siblings*: compare each member to the ratified pair, not in isolation, so a soft bar shared verbatim with them reads as house-wide convention, not a per-file open standard.
- **A bulk or regenerate grow follows the method, not N literal invocations.** When a lift adds several components at once — a regenerated skill growing its absent `rules/` and `modules/` — apply add-component's *method* per file (resolve the canonical home → mirror the sibling exemplar → write → wire) rather than issuing a separate `/anvil:add-component` call for each. Per-file invocation is optional; mirroring the exemplar and landing each in its canonical, wired place is the requirement.
- `--dry-run` is a faithful preview: it reports every file and registration that would be written and writes nothing — never a half-applied change.
