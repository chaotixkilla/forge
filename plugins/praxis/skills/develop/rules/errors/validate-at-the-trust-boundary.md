# Validate at the trust boundary

Untrusted data — a request body, a form field, a file's contents, a response from another service — arrives somewhere and then flows inward through many functions. The judgment this rule governs is *where* to check it: at the one edge where it enters, or wherever a downstream function happens to depend on it being well-formed. Left to reflex it scatters — each interior function re-checks the parts it uses, defensively and partially, so the same field is validated five times in five ways and still no layer is sure it's clean. Two builders put the checks in two different sets of places, and the codebase can't say where its data became trustworthy. This rule pins the discriminator so two builders converge on the barricade.

## The discriminator

The property this turns on is **whether the data has crossed from outside your control into your trust zone yet** — validate at that crossing, completely, and let everything inward assume validity.

- **Where does this data come from?** If it originates outside your control — network, user, file, another service, a queue — it is untrusted and the boundary it crosses is *the* place to validate it. If it came from interior code you already trust, re-validating it is noise (a violated interior assumption is a different failure — fail loud, [fail-loud-in-dev](fail-loud-in-dev.md), don't quietly re-check).
- **Validate completely at the edge, then trust inward.** The barricade is only a barricade if the check is total: everything the interior assumes must be established *here*, so interior functions can take their inputs as given and carry no defensive checks. A half-check that leaves interior code guessing is worse than none — it looks safe and isn't.
- **Validate is *where*; parsing is *how*.** This rule places the check at the entering edge. Converting the raw input into a trusted type at that edge — so downstream code holds a value that *cannot* be malformed rather than a raw one it must trust — is [parse-dont-validate](../data-and-types/parse-dont-validate.md)'s move; the two compose: parse at the boundary this rule identifies.

(basis: McConnell, *Code Complete* 2nd ed. ch. 8 — the "barricade": isolate dirty data at the boundary, convert it to clean data crossing in, and let internal routines assume validity; the secure-input practice that untrusted input is validated at the edge, once, rather than defended against everywhere downstream.)

## The anchors

- *Good:* an entry handler validates and parses the incoming payload into a typed value at the surface; the service and data layers it calls take that value as valid and contain no re-checks — the boundary is the single place data becomes trustworthy, and where an invalid payload is rejected ([handle-errors-at-the-boundary](handle-errors-at-the-boundary.md)).
- *Bad:* no validation at the edge, and instead every interior function guards the two fields it touches, so a malformed request gets three layers deep before a missing field surfaces as a crash — the check is everywhere and the barricade is nowhere.
