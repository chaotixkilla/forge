# dry-run (`--dry-run`)

Activated by `--dry-run`, referenced from [write-and-validate](../phases/04-write-and-validate.md).

The base run resolves the config and writes it. This module runs the whole resolution and validation but stops short of any side effect — it shows the config that *would* be written so the user can review it before committing. Deletion test: remove it and init writes its result; the compute-and-show-but-don't-persist behavior is what the flag turns on.

## The delta

- **Resolve and validate as normal**, at whatever posture the other flags set — `--dry-run` changes only the ending, not the resolution.
- **Render the would-be config** with its validity verdict from [write-and-validate](../phases/04-write-and-validate.md): the full file as it would land, which slots are configured, which disabled, and any defect that *would* block the real write.
- **Write nothing, and trigger no secret side effect** — do not touch `praxis.json`, and do not prompt the user to set a `secret_ref` value in userConfig ([route-secrets-to-userconfig](../rules/route-secrets-to-userconfig.md)); report that the ref *would* be recorded and where its value *would* go, then stop.

## Composition

`--dry-run` pairs with either posture to preview it: with `--guide` it shows what an interactive result would look like without running the interaction to a write; with `--degrade` it shows how much a headless run could fill and what it would disable. In every combination the invariant holds — the file on disk is unchanged when the run ends.
