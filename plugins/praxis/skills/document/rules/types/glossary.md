# Glossary

The words the work coins, or uses in a sense particular to this project, each with the one meaning every page holds it to.

## Reader and question

A new engineer, reading any of the work's pages: "What does this word mean here?"

## Page

`on the design-document page`.

## Membership

One per task. A term belongs when the work coins it or uses it in a sense particular to this project ([documentation-plan](../../../../craft/writing/documentation-plan.md)); a word with its ordinary meaning in the field does not. It is filed again when a term is added or its meaning changes.

## Items

**Term `TERM`.** One word or phrase in one sense.
- Fields:
  - `meaning`: text, in one or two sentences;
  - `origin`: enum `ours`, `vendor`, `both`: the project coined it, an outside product did, or the project uses a vendor's term in a narrower or wider sense;
  - `avoid`: list of text, the synonyms the pages don't use for it.
- Granularity: one sense. A word with two senses here is two terms with distinct titles, or a renamed one. (basis: arc42 §12, no synonyms or homonyms)
- Agreement: `none`.

## Sections

1. **What do these words mean here?** — always. The terms view.

## Checks

*Computed:*
- No two terms share a title. (basis: arc42 §12)
- No word in a term's `avoid` list is another term's title, or appears on a page of the current round other than the glossary and the plumbing pages: matched as a whole word, in any case, outside quote and code blocks. (basis: arc42 §12; NASA SE Handbook App. C, consistency with the glossary)
- Every term appears somewhere in the task's documentation outside the glossary, matched the same way. (basis: arc42 §12)

*Judgment:*
- A definition that uses the term it defines.
- A term whose use on some page drifts from its definition.
- An ordinary word of the field defined as if it were the project's.

## Views

- **Terms:** `table` of every `TERM`: title, meaning, origin and `avoid`, sorted by title.

## Minimum form

The glossary joins with its first term, so it is never empty.
