# Concept

How an outside standard or framework maps onto this system's implementation.

**Reader and question.** Maintainer and auditor: "where does our implementation follow it, and where does it depart?"

**Page.** `own page`

## Membership

A result that relates something defined outside the project — a standard, a protocol, a framework's model — to how this system implements it, naming where they match and where the system departs, each with its source on both sides. Its subject is one standard at one version, as the touched part implements it, held in `standard` on its mappings: one standard per page.

System documentation, bounded as [shape-the-document](../../phases/02-shape-the-document.md) says.

## Items

**Mapping `MAP`.**
- Fields: `standard` text, the standard and its version, as the page names them; `outside` text, the standard's term or clause; `outside version` text, the standard's version; `outside source` text, the link to the standard's text; `inside` text, where the system implements it; `inside source` text, the link to the code or documentation it maps to; `certainty` enum `observed`, `traced`, `inferred`, `unverified` ([results-and-certainty](../../../../craft/evidence/results-and-certainty.md)), for the inside side; `fit` enum `departs`, `absent`, `matches`.
- Granularity: one term or clause of the standard and its counterpart here. A clause the system follows in part is one mapping per part, each with its own fit. Why a departure was made goes in its body.
- Change regime: `living`.
- Agreement: `none`.

## Sections

1. **What is the standard, and which version?** Always. What it defines, in a paragraph, and the version mapped.
2. **Where do we depart from it?** Always. The departure table, each mapping with why in its body.
3. **How does it map?** Always. The mapping table.

## Checks

- *Computed:*
  - every `MAP` whose `standard` is the page subject has `outside source` and `inside source` filled, each a link that resolves;
  - every `MAP` whose `standard` is the page subject has `outside version` filled.
- *Judgment:*
  - a match claimed from names alone, with behaviour unread;
  - a departure with no why;
  - the standard paraphrased from memory rather than read at its source.

## Views

- **Departure table** (section 2): `table` of `MAP` whose `standard` is `page subject` and whose `fit` is in `departs`, `absent`, sorted by `fit` descending: outside, inside, fit, certainty.
- **Mapping table** (section 3): `table` of `MAP` whose `standard` is `page subject`, sorted by `fit` descending: outside, outside version, inside, fit, certainty.

## Minimum form

The standard and version, "no departures found yet", and "no mappings established yet".
