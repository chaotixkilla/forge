# --check: a preflight that leaves nothing behind

`--check` replaces the run. It answers one question about this repository: is praxis set up so it can read its config, find its state folders and commit, without stopping on any of them? It asks nothing, changes no setting and leaves nothing behind. It doesn't test the session's permission settings, whether a secret resolves or whether a backend is reachable. (basis: maintainer, 2026-10-20)

## The checks

Run each, in this order, and give each one result: `pass`, `fail`, or `warn` for one that won't stop a run but may degrade it.

1. **Config.** `.claude/praxis.json` exists where [write-and-validate](../phases/04-write-and-validate.md) reads it, parses, and passes that phase's Validate section apart from slot resolution, which check 3 reports. Unrecognized keys and older shapes are carried, as there. A missing, unparseable or invalid config fails, and so do checks 2 and 3, each naming check 1 as the reason.
2. **Version.** The config's `praxis_version` against the installed praxis's, from `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`. A difference, or no `praxis_version`, warns: init last ran under another version.
3. **Slots.** Each enabled capability slot is resolved as write-and-validate requires. An unresolved one fails. A slot written disabled is a resolved decision, and passes.
4. **Identity.** git has a user name and email for this repository. Missing either fails.
5. **Signing.** When git is set to sign commits here, sign a temporary file outside the repository with the configured format's signing program and key, in a mode that fails rather than prompts, then remove the file. A signature that fails fails. When it succeeds with a key that has a passphrase, ask the signing program's key agent whether it holds that passphrase: when it does, warn, since a later run may find the cache expired. A key with no passphrase passes. Signing off passes.
6. **State folders.** The main checkout's `.claude/praxis/`, the memory folder and the plugin's data folder can each be written. Each is tested by creating and removing one empty file, at the folder itself, or, when the folder doesn't exist yet, at its nearest existing parent. A folder that can't be written fails. The plugin's data folder is the exception: it warns, or, with no data folder set, warns too, unless the config uses a learned adapter or container commands, which keep their files there, and then it fails. The state result is the worst of the three, fail over warn over pass.
7. **Ignored.** `.claude/praxis.json` and `.claude/praxis/` are ignored by git, as write-and-validate's ignore check reads them. A tracked one, or an untracked one git doesn't ignore, warns: a commit could sweep it in.

## The report

One line per check, with its result and, for `fail` and `warn`, what fixes it, then the overall result: `fail` when any check failed, else `warn` when any warned, else `pass`.

`--check` takes no other flag. Combined with one, it runs alone, saying so in its first line.
