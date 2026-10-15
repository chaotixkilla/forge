# forget (`--forget`)

Activated by `--forget`, referenced from [SKILL.md](../SKILL.md).

The base run learns a map. This module deletes one: the resolved transport's section, or the whole file when that is its only section, and says what it removed. Run with `--provider` and no `--port`, it lists every map for that provider and asks which to delete. Nothing else changes. The port's next call learns again. Deletion test: without it, a map the user no longer trusts can only be removed by hand.
