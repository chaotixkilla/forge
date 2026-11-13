# Reference

The facts a reader looks up: formats, endpoints, configuration keys, error codes, each stated exactly.

**Reader and question.** New engineer and maintainer, in the middle of using the part: "what exactly is this setting, field or code?"

**Page.** `own page`

## Membership

A result that pins exact facts about the touched part — a schema, a request and response shape, a setting and its default. Its subject is the part, held in `part` on its entries, so a task has one per part.

System documentation, bounded as [shape-the-document](../../phases/02-shape-the-document.md) says.

## Items

**Entry `REF`.**
- Fields: `part` text, the part it belongs to; `of` enum `endpoint`, `field`, `setting`, `error`, `format`, `other`; `shape` text, its type, format or signature, exactly; `default` text, when it has one.
- Granularity: one thing a reader looks up by name. Its parts stay in its body, such as an endpoint's request and response fields.
- Change regime: `living`.
- Agreement: `none`.

## Sections

1. **What does it cover?** Always. One line: the part, and what kinds of entry the page lists.
2. One section per `of` value present, in this order: **Which endpoints does it serve?**, **What fields does it hold?**, **Which settings does it read?**, **Which errors can it return?**, **What formats does it use?**, **What else is there to look up?** Each holds its entry table, below.

## Checks

- *Computed:*
  - every `REF` whose `part` is the page subject has `shape`;
  - every `REF` whose `part` is the page subject has an evidence link to the code or contract it was read from;
  - no two `REF` whose `part` is the page subject share a title within one `of`.
- *Judgment:*
  - an entry that explains why or tells the reader what to do;
  - a shape paraphrased rather than stated as the code states it;
  - a default given that the code doesn't set.

## Views

One entry table per section 2 heading, each a `table` of `REF` whose `part` is `page subject` and whose `of` is the value named, sorted by title: shape, default (empty marker `none`).

- **Endpoints** (Which endpoints does it serve?): `of` is `endpoint`.
- **Fields** (What fields does it hold?): `of` is `field`.
- **Settings** (Which settings does it read?): `of` is `setting`.
- **Errors** (Which errors can it return?): `of` is `error`.
- **Formats** (What formats does it use?): `of` is `format`.
- **Other entries** (What else is there to look up?): `of` is `other`.

## Minimum form

The coverage line, and "no entries established yet".
