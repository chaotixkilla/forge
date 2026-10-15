Map the whole port at once, so the user meets one exploration, not one per operation. `(basis: maintainer, 2026-10-13 — whole port at first contact)`

## Match each operation

For each operation the port lists, find the call, or the ordered calls, that perform it. A sequence of calls can match: for example, a request read with one call and its comments with another. It matches when the calls' inputs can carry every input the operation names. Choose among matches by this ladder; the first rung that separates them decides:

1. the one whose outputs carry every field the operation returns;
2. the one needing no required input that neither the operation, the slot nor an earlier call supplies;
3. the one with fewer calls;
4. the one that changes less: a call that updates in place over one that recreates;
5. the first by name.

**Local operations.** Some operations run on the local repository rather than on the provider: vcs's *push a branch* and *fetch a change's head*. They map to the local version control's own commands, read from its help as a `cli` surface is, with the provider supplying only the ref names. They are judged as any other call.

Record, per operation:

- **the calls**, in order, each with its digest and how its inputs are filled:
  - from the operation's input;
  - from a slot or entry field, `slot <key>`;
  - from an earlier call's result, `<from call n>`;
  - or a fixed value.

  A call repeated per item is prefixed `for each <item>:`, and calls after such a loop `after all:`. A call that runs only when an earlier one finds nothing sits under `if <call n> returns none:`, with `else: return <call n>` for the found result; one that runs only when an input is given sits under `when <input> given:`. A guarantee that needs a branch these forms can't hold is not shown.
- **the outputs** — how each field the operation returns is read from the calls' results, and which it can't return.
- **the failures** — the tool's errors mapped onto the port's own outcomes, named in its words. Where the surface states no error, use the generic mapping:
  - no transport or authentication → the port's reach-failure outcome (`unavailable`);
  - forbidden → its permission outcome;
  - an unknown reference, where absence and no access look alike → its masking default;
  - a throttle or timeout → its transient outcome;
  - a refusal with a stated reason → `refused` in vcs, `conflict` in artifacts;
  - anything else → the outcome that tells the caller to change its request.
- **its status**:
  - `mapped`;
  - `partial`, when some returned fields can't be read; the port returns them as not exposed, and a field a guarantee depends on makes the operation `unmapped` instead;
  - `unmapped`, when no call can perform it; the port answers `unsupported`.

## Reads are tried, writes never

An operation whose calls are all reads is tried once. Its input comes only from the slot or entry fields, the repository the session is in, or a reference the user gave in this request, never from another call's result. Where an operation has a variant that holds data back, such as a change fetched without its description, the try uses that variant. Record the outcome:

- `read on <date>`;
- `read failed on <date> (<outcome>)`;
- a result whose shape the mapping doesn't fit is remapped, or the operation is marked `unmapped`.

An operation with no such input stays `untested`, which doesn't stop it being used. An operation that uses any write is never performed here: it is marked `untested write` until its first use succeeds ([dispatch-through-a-learned-map](../rules/dispatch-through-a-learned-map.md)). `(basis: maintainer, 2026-10-13 — never probe a write by performing it)`

## Extras

A call no operation uses is listed by name as an extra. Nothing uses it, however useful it looks. `(basis: maintainer, 2026-10-13)`

The output is each operation's mapping and status, the tried reads' results, and the extras, for [judge-the-guarantees](04-judge-the-guarantees.md).
