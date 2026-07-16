# scaffold-skill — usage

Generate the file skeleton for a new skill in a target plugin — frontmatter and slots stubbed, procedure deliberately left empty.

## When to use
- You've decided a target plugin needs a *new capability* and want the SKILL.md, its slot directories, and stub files laid down so the structure is locked before any method is written.
- You want the skeleton built breadth-first: interrogate the single capability, shape the frontmatter contract (name, description, flags, and — for config-bearing plugins — `config_requires`), and seed one phase per ordered step, only the rules/modules that are earned.
- You want the intent pinned *before* files exist — is this really a skill, or a flag/module/rule on one that already exists — so you don't scaffold a near-duplicate the contract audit can't catch.
- You want the skill's standard-points — every place it will grade, select, or default — surfaced at interrogation and carried as explicit stubs, so the content pass closes each bar from an authority or the maintainer instead of filling it from priors.
- You want the skeleton handed straight to codify (`--with-codify`) so the same run produces slots then method.
- You want to preview the whole tree — every directory and stub with its one-line intent — before it touches disk (`--dry-run`).

## Not for / use instead
- Filling the procedure — writing the actual method inside the stubbed phases, sourced and cold-executor-validated → **codify**. scaffold-skill owns *structure*, codify owns *method*; the seam between them is a hard line this skill will not cross.
- Growing an *existing* skill with a non-skill part — an adapter, explorer, critic, rule, module, or hook → **add-component**. If the "new capability" turns out to be a lens or reusable judgment on a skill that already exists, it's a component, not a skill.
- Birthing the *plugin itself* — its `plugin.json`, config posture, slot folders, and the initial pool of skills → **new-plugin**. scaffold-skill adds one skill *into* an existing plugin's `skills/` tree; it does not create the tree.
- Checking that a scaffolded skill's contract is well-shaped — frontmatter fields, slot placement, flags↔modules wiring, config keys → **audit-contract**. scaffold *declares* the contract; the audit *verifies* it.
- Scanning the skill layer for leaked tool/vendor names → **audit-tool-leaks**. scaffold avoids leaks by phrasing capabilities cleanly at authoring time; the audit confirms none escaped.

## Examples
`--plugin=<plugin> --name=<skill>` — scaffold a new skill into the target plugin: interrogate the capability, shape frontmatter, seed `phases/` (rules/modules only if earned), report every path created.
`--plugin=<plugin> --name=<skill> --dry-run` — produce the exact tree that *would* be created — every directory and stub with its one-line intent — and write nothing; the maintainer reviews the shape before it lands.
`--plugin=<plugin> --name=<skill> --slots=phases,rules` — override the default need-derivation and seed exactly `phases/` and `rules/`, e.g. when you already know the skill carries reusable craft.
`--plugin=<plugin> --name=<skill> --slots=phases,modules` — seed `phases/` and `modules/`; each module owes a matching declared flag in frontmatter, or it's unreachable.
`--plugin=<plugin> --name=<skill> --with-codify` — lay the skeleton, then hand the fixed shape (known phases, known slots, per-slot intent) to codify to fill the procedure in the same run.
`--plugin=<plugin> --name=<skill> --with-codify --dry-run` — preview the skeleton *and* state that codify would be handed it, but write nothing and invoke nothing.

## Gotchas
- `--plugin` and `--name` are both required — this skill mutates a specific plugin's `skills/` tree. If either is missing it stops and asks; it never infers the target from cwd, the last plugin touched, or the only plugin that exists. A wrong guess writes into the wrong tree.
- `--name` becomes *both* the directory (`skills/<name>/`) and the frontmatter `name` field, so it must read as a capability verb-phrase, not a tool or noun.
- It deliberately writes **no procedure**. Every seeded file is a *stub* — what the slot will hold, plus any standard-point demands (a bar the content pass must close: a scale, a threshold, an acceptance test, a default) — never a first draft of the method. A fake-finished phase repels the filling pass that should follow; an honestly empty stub invites it.
- Empty is a valid, often correct answer: a clean linear procedure is `phases/` alone. Do not expect `rules/`/`modules/` "for symmetry" — speculative slots read as a missing-content promise. Slots are earned by content that exists, not anticipated.
- Flags↔modules is a closed loop: if you seed a module, the activating flag must already be declared in frontmatter, and vice versa. A module with no flag is dead code; a flag with no behavior is dead declaration.
- `config_requires` is declared *only* for config-bearing plugins. The kit's own authoring plugins are config-less — adding a spurious prerequisite makes a skill demand configuration it never uses, and the contract audit will flag a key with no backing template entry.
- Doer-owns-prerequisites: declare only what *this* skill needs to run — never a prerequisite belonging to a skill it hands off to (`--with-codify` does not pull codify's obligations up into this contract).
- The spine and the phase files move in lockstep: every seeded `phases/NN-name.md` earns exactly one numbered line in SKILL.md that links to it by relative path. A phase with no spine reference is loaded by nothing at runtime; rules and modules get *no* spine line — a module is referenced from its activating phase (or a non-spine body line when the flag changes the whole run), and rule citations are laid by codify against the wiring plan each rule stub records.
- Mirror the target plugin's existing conventions (phase-naming, numbering, stub density) rather than stamping a generic template; where the plugin is brand-new with no siblings, fall back to the kit's defaults. Mirroring governs voice/naming/density only — *which slots exist* comes from the skill's own seed and the documented contract, which beat sibling precedent when siblings are known-incomplete.
