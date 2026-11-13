# Explanation

How a part of the system works and why it works that way, with a diagram where structure or flow carries the point better than prose.

**Reader and question.** New engineer and maintainer: "how does this work, and why is it built this way?"

**Page.** `own page`

## Membership

A result that says how the touched part behaves and why: a map of its flow, its states, the reasons behind its design. A page that starts telling the reader what to do is a [how-to](how-to.md); one that starts listing formats or settings is a [reference](reference.md).

System documentation, bounded as [shape-the-document](../../phases/02-shape-the-document.md) says.

## Items

**Explanation `EXP`.** One per page, the whole explanation in its body.
- Change regime: `living`.
- Agreement: `none`.

## Sections

1. **What is it for?** Always. What the part does for the system, in a paragraph.
2. **How does it work?** Always. Its flow, states and structure, drawn where [when-a-visual-is-owed](../../../../craft/writing/when-a-visual-is-owed.md) owes it, each visual with its caption.
3. **Why is it built this way?** Always. The reasons behind its design and the constraints that hold it there, linking a decision record where one exists.
4. **Where does it meet the rest?** When the part has callers or dependencies outside it. Its boundaries, and the pages on the other side.

## Checks

- *Computed:*
  - exactly one `EXP`;
  - every visual has a caption and a provenance.
- *Judgment:*
  - steps to follow, which belong on a how-to;
  - tables of settings or formats, which belong on a reference;
  - a "why" that restates the "how";
  - a design reason with no source, reconstructed from the code's shape.

## Minimum form

What the part is for, and each of the other always-present sections "not yet established".
