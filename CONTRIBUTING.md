# Contributing

This repo is a dataset with a README attached. The evidence table in `README.md` is generated from `methods.yaml`, so please do not hand edit it.

## To correct a fact

1. Edit the relevant entry in [methods.yaml](methods.yaml).
2. Run `python render_table.py --write` to regenerate the table between the `<!-- TABLE:START -->` and `<!-- TABLE:END -->` markers.
3. Open a pull request explaining what changed and where you verified it.

Requirements: Python 3.9+ and PyYAML (`pip install pyyaml`).

## How strength ratings are decided

Strength is about the quality of the evidence a pass produces, not about how easy the method is to run.

| Rating | Meaning |
|---|---|
| 5 | Independently issued evidence, bound to a verified identity or physically confirmed |
| 4 | Independently issued or authoritative evidence, not bound to the presenter |
| 3 | Corroborated against third party reference data, coverage limited |
| 2 | A consistency signal only, proving a relationship other than residence |
| 1 | Self asserted, or proves only that the address exists |

A method moves up a grade only if it adds independent corroboration. Faster, cheaper, or better marketed does not move a rating.

## Scope limits, enforced

Pull requests will be closed without merge if they add:

- Techniques for locating a private individual who has no transactional relationship with the operator: people search aggregation, social media reconnaissance, data broker scraping, or pretexting.
- Any method whose primary use is tracing someone who does not wish to be found.
- Links to people search or data broker products.
- Claims that a vendor or a method makes the operator compliant. The obligation belongs to the operating business. Tools supply evidence.

Additions should serve a business with a nameable lawful basis. If a method only makes sense for surveillance of an individual, it does not belong here.

## Style

No affiliate links. No vendor marketing copy. Every `proves` field should state the narrowest true claim, and every `fails` field should name a concrete defeat condition rather than a general caveat.
