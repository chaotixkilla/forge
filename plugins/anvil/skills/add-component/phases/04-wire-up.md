Creating the component file is the easy half. A component that exists but isn't *registered* is invisible: the parent skill never dispatches to the adapter, never recruits the agent, never activates the module. And it isn't a silent no-op — the next `audit-contract` run flags an unreferenced agent as orphaned and a flagless module as dead. Wiring is the half that makes the component live, and it differs by kind.

## Adapters — add the dispatch

The skill layer names a *capability* ("publish the artifact", "open a change request"); the adapter is the concrete implementation for one tool×transport. A dispatch line in the parent skill connects them: where a phase invokes the capability, it resolves to the matching adapter at call time, chosen by the configured provider.

If the skill already invokes this capability, you're adding a new provider under an existing dispatch — confirm the capability reference exists and that the dispatch can now resolve to your adapter. If the capability is new to the skill, add both the capability reference (in the phase that needs it) and the dispatch that routes it. Never name the adapter in a phase: the phase names the capability, the dispatch is the only thing that knows adapters exist.

In capability terms: a phase reads *"publish the report to the configured artifacts backend"*; the dispatch routes the `artifacts` capability to whichever provider is configured under `adapters/`, and that adapter holds the provider-specific calls. Swap the provider and the phase text doesn't change — that's the seam holding. The example deliberately stops at the capability: a literal backend name would be a tool-leak, and a fixed dispatch syntax would pin a mechanism the kit hasn't settled.

Anti-pattern: writing the adapter but leaving the phase still describing the tool inline. That's both a tool-leak and a dead adapter — `audit-tool-leaks` catches the first, `audit-contract` the second.

When the parent is a **port** whose body already carries a provider-agnostic dispatch (`adapters/<provider>`), adding an adapter is **zero parent-skill edits**: the dispatch already resolves to any adapter under it, and writing the concrete provider name into the skill would be a leak. Report the adapter file alone — that empty wire-up *is* the complete, correct outcome, not an under-wiring to flag (the same blessing the explorer/critic case gets below). You only touch the parent when its dispatch doesn't yet exist or doesn't yet resolve to your adapter.

## Explorers and critics — add to the recruit list

An agent runs only when a skill recruits it, so add the new explorer/critic to the parent skill's agent listing in the phase that uses it: an explorer where the skill *gathers* ("read the target plugin's conventions via the plugin explorer"), a critic where it *challenges* ("send the draft to the cold-executor critic"). An agent file no skill references is orphaned — it never runs, and it reads as cruft to the next maintainer. One exception makes an unwired agent legitimate: if the agent auto-discovers and *every* skill that would recruit it is still unbuilt, there is nothing to wire yet — registration is deferred until a recruiter exists, and an empty wire-up here is the correct outcome, not a skipped step to flag. This is the norm when seeding an agent family ahead of its consumers (see [usage.md](../usage.md)); where a recruiter already exists, wire it now.

## Modules — declare the activating flag (mandatory)

A module is behavior a flag turns on, so wiring it is two steps, not one: the file in `modules/`, **and** the flag in the parent skill's `metadata.flags` that activates it. Skip the flag and the module is unreachable dead code — exactly what `audit-contract`'s flags↔modules check exists to catch.

For example, a skill declares `--security: also run the security lens` under `metadata.flags`, and that lens's behavior lives in `modules/security.md`. The flag is the on-switch: declare the module without it and the lens can never fire. If the flag already exists (you're adding a module under an already-declared flag), just confirm the activation wiring; otherwise add the flag with a one-line meaning.

## Rules — nothing to wire

A rule is a-la-carte craft, not gated behavior. Living in `rules/` and being cited by the phases that apply it *is* its registration — no manifest entry, no flag. If a "rule" seems to need activation wiring, it's a module in disguise; reclassify it rather than inventing a flag for it.

## Hooks — add the manifest entry

A hook file is inert until the plugin's hooks manifest points at it, bound to a lifecycle event. Add that entry at the right event; without it the harness never loads the hook, and the file is just documentation.

## Under `--extend` — confirm the wiring, don't re-add it

A component that already existed is already registered, so this phase **verifies rather than adds**: confirm the dispatch, recruit reference, activating flag, or manifest entry the kind owes is still present and still correct. Adding a second one is the duplicate this phase exists to prevent.

One case does need a write: an extend that *changed what the component is* — an agent given a new lane, a module whose flag was renamed, an adapter that now serves an operation it did not before — can leave the existing wiring accurate about the old body and wrong about the new one. Re-read the registration against the body you just wrote, not against the body you found.

## Finish — report, and honor `--dry-run`

Report the full change set: the component file plus every parent-skill file you touched to wire it — dispatch line, recruit reference, flag declaration, manifest entry. The maintainer reviews the change as a whole, so a partial list is worse than none. Under `--dry-run`, produce that exact report — every file and registration that *would* be written — and write nothing. A dry run is a faithful preview, never a half-applied change.
