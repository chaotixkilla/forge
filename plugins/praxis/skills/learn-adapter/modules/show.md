# show (`--show`)

Activated by `--show`, referenced from [SKILL.md](../SKILL.md).

The base run learns a map. This module only reads one: for the port and provider resolved by [resolve-the-target](../phases/01-resolve-the-target.md), show each transport's section as a table, one row per operation, with these columns:

- its status;
- the calls it maps to;
- whether it is tested;
- each guarantee's verdict;
- what is unsupported and why.

Then show the extras, and say whether the tool's current signature still matches. With no map, say so and give the command that learns one. Nothing is read from the tool but its signature, and nothing is written. Deletion test: without it, the only way to see what praxis learned is to open the file.
