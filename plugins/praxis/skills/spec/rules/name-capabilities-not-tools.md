# Name capabilities, not tools

A spec that names products dates the moment it's written and pre-empts the design it should leave open. "Store uploads in S3," "queue jobs in Redis," "send email via SendGrid" each smuggle a chosen solution into a document whose job is to state the need — and they read as decided when they were never argued. When the team later evaluates object stores or message queues, the spec is already lying: it says "S3" where it means "durable object storage," and a reader can't tell the immovable constraint from the incidental default. This rule keeps requirements at the level of the *capability* and the *property that matters*, so the spec stays portable across tool choices and the design phase stays free to make them.

## The discriminator: would it survive a vendor swap?

The test for any named product in a requirement: **is the name a chosen solution, or an immovable constraint of the environment?**

- **A chosen solution** — the team picked it, or could pick differently, and the requirement is really about what it *provides*. Drop the name; state the capability plus the property that mattered. "Store in S3" → "durable object storage, 99.9% availability, objects up to 5 GB." This is the common case, and leaving the name in is a leaked design decision ([separate-problem-from-solution](separate-problem-from-solution.md)).
- **An immovable constraint** — the environment forces it: "must integrate with the company's existing Salesforce instance," "must run on the on-prem Postgres the client already licenses." Here the product *is* the requirement, because the constraint is real and the design cannot route around it. Keep the name — but record it as a **constraint**, not a casual implementation choice, so its force is visible.

The swap test makes the call concrete: imagine the vendor is replaced next quarter. If the requirement should still hold unchanged (it was about the capability), the name was incidental — remove it. If the requirement becomes false or meaningless (the whole point was that specific integration), the name was a constraint — keep it and label it one.

## Method

For each requirement that names a product, ask what capability the team actually depends on and what measurable property of it matters, and rewrite to that: the capability (object storage, message queue, transactional email, full-text search) plus the properties that constrain the outcome (durability, latency, ordering guarantees, deliverability). The named product, if it survives the swap test, moves to a constraints section as an explicit environmental constraint — never left inline as though it were the requirement itself.

This is the spec-writing sibling of the kit-wide capability discipline: the skill layer names capabilities and adapters hold tools; a *spec* names capabilities and the design chooses tools. Same seam, one layer up.
