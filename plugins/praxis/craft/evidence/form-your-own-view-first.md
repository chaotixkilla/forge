# Form your own view first

Someone's conclusion shapes what you look for: read an author's reasons first, and you go looking for evidence that fits them and stop seeing the alternatives. So form your own view of the work against what it must achieve, and read anyone's argument for how it was done only after that, against your view.

- **Intent** says what should be true when the work is done: a ticket, a spec, an RFC, a requirement. It is read first, always.
- **Rationale** says why someone did it their way: a change's description, its commit messages, the author's notes, linked discussion threads, an alert's claimed cause, a teammate's "this part is done". Where the work starts from someone else's rationale, it is read only once your own view is formed.

The discriminator: does the text state what must be true when the work is done (intent), or argue for the way it was done (rationale)? A ticket that also proposes a solution is intent for its requirement and rationale for its proposal. (basis: maintainer, 2026-09-30, from reviewing a teammate's change and taking over a teammate's branch.)
