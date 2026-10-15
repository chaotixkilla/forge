# relearn (`--relearn`)

Activated by `--relearn`, referenced from [SKILL.md](../SKILL.md), and run by [dispatch-through-a-learned-map](../rules/dispatch-through-a-learned-map.md) when the tool's signature changed.

The base run writes a map where none exists. This module maps again over an existing one. It runs phases 2 to 5 as usual, then carries one thing over from the old map: an operation's `write succeeded` mark, but only when every one of its calls keeps the digest it had. A call whose digest changed is a new write and asks again. Deletion test: without it, a changed tool keeps a stale map until the user forgets it by hand.
