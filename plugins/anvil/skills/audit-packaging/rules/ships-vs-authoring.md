This is the craft of putting a single, defensible verdict on a file: does it *ship* to consumers, or is it *authoring-only* and must stay outside every published source path? Every finding this skill produces rests on this call, and the cost of getting it wrong is asymmetric and real — a wrong "ships" leaks maintainer tooling or secrets onto a consumer's disk, a wrong "authoring-only" could strip something the running plugin needs. The classification is load-bearing because the install model is unforgiving: a published plugin's source directory copies whole, with no per-file exclude. There is no filter downstream to catch a mislabeled file. The label *is* the filter.

## The one test that decides every case

> Would a consumer who installed this plugin need this file to *use* it?

If yes, it ships. If no — if the file exists only to **build, audit, document-for-maintainers, or release** the plugin — it is authoring-only. Everything below is this test applied to the recurring shapes; when a new shape appears, return to the test rather than pattern-matching against the list. The distinction is *use* versus *make*: consumers use, maintainers make.

What separates a *defensible* verdict from a guess: you can name the moment the file gets used. For *ships*, point at the runtime moment a consumer's session reads it — the spine loads this phase, the adapter reads this table, the harness fires this hook. For *authoring-only*, point at the making activity it serves — this fixture feeds the authoring tests, this note records a design decision. One nameable moment and not the other → defensible. Both → genuinely dual-use, mark *uncertain*. Neither → you don't yet know what the file is; read it before it gets a verdict. A classification backed by nothing but a plausible filename is a guess wearing a verdict's clothes.

## Ships — the runtime surface

A consumer needs these to invoke and run the plugin, so they belong inside the published source path:

- The skill bodies and their frontmatter — the capability surface the consumer invokes.
- The agents the skills recruit — explorers that gather, critics that challenge.
- The adapters that resolve a named capability to a concrete tool — the running plugin dispatches through them.
- Lifecycle hooks the harness loads.
- The plugin manifest.
- The config *template/schema* the consumer fills in to wire the plugin to their own environment.
- Any data a component reads *at runtime* — an adapter's lookup table, a hook's payload. The plugin loads it while running, so the consumer needs it.
- An **executable a skill invokes during a run** — a checker or measurement script a phase shells out to. It is not maintainer tooling merely for being code: the consumer's own session executes it, so by the one test above it ships, exactly like the data an adapter reads. It must be reachable from the skill that invokes it and assume no install step of its own.

## Authoring-only — the apparatus that makes the plugin

None of these is needed to *use* the plugin; all exist to *make* it, so each lives in an authoring plane outside every source path:

- Design and decision notes, architecture write-ups, the reasoning behind the build.
- Maintainer scripts and generators — the tooling that *authors* content, renders a design record, or drives a release. This is the make side of the split, and it is distinct from an executable a skill invokes while running, which ships: both are code, and code is not the discriminator. Ask who runs it and when.
- Contributor docs aimed at the people building the plugin, not the people running it.
- Test suites and their fixtures — a consumer does not run the plugin's authoring tests.
- Scratch material, populated configs holding real backend choices or secrets, anything that captures *this maintainer's* state rather than *a consumer's* runtime.

This split is per-file and applies inside *every* plugin, including anvil itself. anvil is a published plugin: its skill bodies, agents, and adapters are the runtime surface a consumer installs and ships accordingly; only anvil's own design notes, maintainer tooling, and tests are authoring-only. "Authoring plugin" is anvil's role, not a blanket authoring-only verdict on its files.

## The calls that are genuinely hard

- **Documentation splits by audience, not by being documentation.** A usage README that shows a consumer how to invoke the plugin ships. A "how this is built / how to contribute" doc is authoring-only. Ask who needs to read it to use the thing.
- **Config splits by template-vs-populated.** The empty template/schema a consumer fills in ships; a config already populated with a maintainer's backends or secrets is authoring-only and a hard flag if it sits inside a source path.
- **Data splits by runtime-vs-fixture.** Data a component reads while the plugin runs ships; data that exists only to test the plugin authoring does not.
- **Executables split by who invokes them.** A script a *skill* shells out to mid-run ships — the consumer's session runs it, and the skill would be broken without it, so the nameable moment is a runtime one. A script a *maintainer* runs by hand to generate content or cut a release is authoring-only, however similar it looks. The give-away is the caller: if a phase names the script, it ships; if only a human or a repo workflow does, it does not. A shipped executable inherits a further obligation — it must depend on nothing that is not already present, because there is no install step between the copy and the run.
- **A plugin's authoring apparatus is authoring-only even when the plugin itself ships.** anvil is published, so its skills and adapters ship — but its design notes, generators, and tests are still authoring-only. The same design/notes and tooling planes that stay out of any plugin's source path stay out of anvil's too. Judge the material by the *use-vs-make* test, not by which plugin it belongs to.

## Anti-patterns

- **Classifying by file extension or name.** A `.md` is not automatically docs that ship; a file named "config" may be a maintainer fixture. Judge by audience and runtime need, never by surface form — a misleading name is exactly the trap.
- **Classifying by directory convenience.** "It was easiest to drop it next to the skill" is not a reason it ships. Location should *follow* the verdict, not produce it; if an authoring-only file ended up inside a source path, that is the finding, not a reclassification.
- **Forcing a verdict you cannot defend.** When *use* and *make* genuinely both apply, mark the file uncertain and let the boundary-keeper critic challenge it — guessing one way leaks tooling, guessing the other strips a needed file.
- **Treating "exclude it from the package" as a remedy.** There is no per-file exclude in this install model. The only fix for a misplaced authoring-only file is to move it physically outside the source path.
