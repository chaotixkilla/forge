# localize-and-translate (`--lang=<code>`)

Activated by `--lang=<code>`, referenced from [draft-the-content](../phases/04-draft-the-content.md).

Base behavior: [draft-the-content](../phases/04-draft-the-content.md) writes the artifact in the work's default language. This module produces it in the target language instead. Deletion test: remove it and drafting still produces a complete artifact in the default language; the target-language rendering is additive — so it is a module.

## The delta — render in the target language, preserving meaning

Produce the artifact in the language named by `<code>`, as a faithful re-expression of the framed message — not a mechanical word swap of a default-language draft. What must survive the translation:

- **The takeaway and the ask** — the point and the requested action land with the same force in the target language.
- **The register and tier** — the tone calibrated in [calibrate-tone-to-context](../rules/calibrate-tone-to-context.md) and the depth of the assigned tier carry over; formality and directness norms differ by locale, so match the target locale's conventions for the same tier rather than transliterating the source's.
- **Locale-appropriate idiom and conventions** — dates, units, honorifics, and idiom follow the target locale, not the source.

This module does not change *what* the artifact says, *whom* it is for, or *how much* detail it carries — the frame, tier, and altitude are fixed upstream; it only changes the language the finished message is expressed in. Technical terms and internal names that [match-reader-vocabulary](../rules/match-reader-vocabulary.md) kept bare stay in their canonical form (a code identifier is not translated); prose around them is localized.

## Prerequisite and degrade

Translation is a drafting capability, not a backend call — it needs no configured tool and declares no `config_requires`. Degrade on *fidelity*, not availability: if the target language or locale can't be rendered faithfully (an unfamiliar locale, content whose meaning would be distorted), do **not** ship a low-confidence translation as if it were sound — produce the best faithful version, flag the specific passages whose translation is uncertain, and offer the default-language original alongside so a fluent reviewer can check it. A silently wrong translation is worse than an acknowledged uncertain one.
