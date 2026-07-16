A version number is a promise about compatibility, and the catalog is the public record of that promise. This rule is the craft for keeping both honest: choosing the right semver bump from what actually changed, and keeping the plugin's own manifest and its catalog entry from ever disagreeing about what version it is. Get the bump from the change itself — never from how big the diff *looks* or how much effort went in. A one-line fix to a function consumers call can be a major bump; a thousand-line internal refactor nobody can observe is a patch.

## Choosing the bump

Classify the change set by its effect on the plugin's **consumer surface** — never by its size. The surface is everything a consumer can invoke or observe: the skill set (names, descriptions, triggers), each skill's declared flags and their meanings, its default behavior when no flag is passed, its config keys and their `if_missing` postures, the output shapes skills promise, and the capability set the adapters back. In a plugin, prose *is* code — a phase edit can change behavior as surely as a signature change — so the question for every item is what an existing invocation would feel, not which kind of file moved.

The derivation method: walk the change set item by item, tag each item with the surface element it touches, and classify:

- **Major** — some existing invocation now fails or does a different kind of thing. In plugin terms: a skill, flag, or config key removed or renamed; a flag or skill whose meaning changed; a default flipped (the no-flag behavior differs from before); an output shape consumers parse changed; a config key newly required (`if_missing` hardened to block). Major is the bump that says "you must read the notes before upgrading."
- **Minor** — new invocations become possible and every old one behaves as before: a new skill, a new optional flag or module, a new capability or adapter, a new config key that guides or degrades rather than blocks.
- **Patch** — every previously-valid invocation keeps its contract; only its correctness or clarity improved: a bug fix, a phase clarified without changing declared behavior, a corrected adapter, an internal restructure touching no surface element.

When the change set mixes levels, the **highest** level wins — one breaking change in an otherwise-additive release still makes it major. For the ambiguous item — the prose edit or restructure that might or might not be observable — the tie-breaker test: *would a consumer who scripted yesterday's invocation notice anything besides improvement?* If you can't answer confidently, round **up**: under-bumping a breaking change silently breaks installs, while over-bumping merely asks for an unnecessary read of the notes. The conservative error is the cheap one.

### Pre-1.0 plugins

Below `1.0.0` the compatibility promise is explicitly weak — the leading zero says "still stabilizing." The convention shifts down a notch: breaking changes ride the minor position (`0.4.0 → 0.5.0`) rather than forcing a `1.x`, and additive/fix changes ride patch. Don't auto-promote a plugin to `1.0.0` as a side effect of a bump; reaching `1.0.0` is a deliberate "this is now stable" decision the maintainer makes, not something a breaking change triggers mechanically.

### Derived vs declared

When the maintainer passes `--bump`, that's a declaration — apply it, but if the change set plainly contradicts it (a `patch` over a removed skill), say so rather than silently obeying; the point of the rule is to keep the promise honest. When `--bump` is absent and the level is derived, the derivation is always a *proposal*: state the level and the evidence behind it so a misjudgment can be corrected before it's written.

## Keeping manifest and catalog consistent

The plugin's `plugin.json` is the single source of truth for its version; the catalog entry **mirrors** it. They move together in one release — never bump one without the other, because a manifest and catalog that disagree about a plugin's version are a defect the next packaging audit will flag, and worse, they make "what version is installed" unanswerable.

Two invariants hold across every release:

- **The catalog source path always points at the plugin's own subdirectory** under `plugins/`. That's what install copies; it never points above the plugin root (which would drag in authoring-only siblings) or beside it.
- **The catalog name matches the manifest name exactly.** The two identify the same plugin; a mismatch breaks resolution.

When in doubt about whether a field belongs in the manifest or the catalog: durable identity and version originate in the manifest and are mirrored to the catalog; the catalog adds only what the *index* needs (the source path that tells the harness where to load the plugin from). Keep the duplication minimal and always in that direction — manifest leads, catalog follows.
