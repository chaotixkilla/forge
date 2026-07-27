# Choosing the right data structure

The moment this rule governs is the one where you declare the thing that will hold the change's data — a collection, a map, a record. The default failure is reaching for the *familiar* structure (the one already in scope, the one the language makes easiest to type) rather than the one the data's usage demands. The cost surfaces later and quietly: a list scanned for membership on a hot path, a nested map that lets two fields drift out of sync, an index rebuilt on every read. Two builders picking by habit land on two shapes with two different performance and correctness profiles.

## The discriminator

Pick the structure by two properties of the data, established in orient's "how does the data move" reading — its **access pattern** and the **invariant it must always hold** — not by what is familiar:

- **Enumerate how the data is read, written, and searched, then pick the structure that makes the *common* operation cheap.** Lookup by key → a map/dictionary. Ordered iteration or positional access → a list/array. Membership and uniqueness → a set. Repeatedly pulling the min/max or top-*k* → a heap/priority queue. Range queries on a sorted key → a sorted/ordered map. The operation you do most on the hot path decides; a structure whose cheap operation is one you never perform is the wrong pick.
- **Ask which invariant must hold at all times, and pick the structure that makes the invalid state impossible rather than merely unlikely.** "No duplicates" is a set, not a list you dedupe by hand. "Exactly one value per key" is a map, not paired parallel arrays that can fall out of step. Push the guarantee into the structure so no code has to re-establish it ([model-with-the-type-system](model-with-the-type-system.md)).
- **The classic wrong pick: a list scanned for membership on a hot path.** Linear search where a set or map would answer in one step — correct, and fine at ten elements, quietly quadratic at ten thousand. When lookup is the operation, the structure is a set or map.

(basis: McConnell, *Code Complete* 2nd ed. ch. 12 — choose the data structure from how the data is accessed and the operations performed on it, not convenience; and the widely-held craft maxim, folklore variously attributed to Brooks and Torvalds, that getting the data structures right makes the code that operates on them follow — the structure is the load-bearing decision, the algorithm often falls out of it.)

## The anchors

- *Good:* a membership check against a fixed roster of allowed keys is a set built once; the check is a single containment test and "these are unique" is guaranteed by the structure, not by discipline at each insert.
- *Bad:* the allowed keys live in a list, every request walks it with a linear scan, and a duplicate slips in because nothing forbids it — the access pattern (membership) and the invariant (uniqueness) both argued for a set, and familiarity picked the list.
