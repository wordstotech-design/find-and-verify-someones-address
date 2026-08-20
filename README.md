# Find and Verify Someone's Address

<p align="center">
  <a href="https://www.idenfy.com/">
    <img src="https://github.com/user-attachments/assets/42b041d7-709f-4195-8283-1fbbdc7311d0" alt="find-and-verify-someones-address" />
  </a>
</p>



A working reference on [how to verify someone's address](https://www.idenfy.com/identity-verification-service/) when your business has a lawful reason to: nine methods ranked by how strong the resulting evidence actually is, what each one fails to prove, and how to stack two of them into a check that holds up. The dataset lives in [methods.yaml](methods.yaml) and the table is computed by [render_table.py](render_table.py).

## Scope, stated plainly before anything else

This repo is written for businesses that have an obligation or a documented legitimate interest: a regulated entity running customer due diligence, a lender or insurer confirming residency, a merchant fighting card-not-present fraud, a marketplace onboarding sellers, a logistics operator that needs a deliverable address.

It is **not** a guide to locating a private individual who has not transacted with you. People-search aggregation, social media reconnaissance, and pretexting a former landlord are all things you can find written up elsewhere; they are excluded here on purpose. They produce weak evidence, they are unlawful in many jurisdictions without a basis, and the most common reason someone wants to trace a person who has not given them their address is not a reason any vendor should help with. If you are trying to locate someone who does not want to be found, the correct route is a court, a licensed process server, or the police, not an API.

Everything below assumes a subject who is transacting with you and a lawful basis you can name in writing. Nothing here is legal advice.

## Finding and verifying are two different jobs

The phrase gets used as one thing and the two halves have different success criteria.

**Finding** an address means obtaining a candidate string. In a business context this is nearly always trivial, because the subject supplies it during onboarding. The interesting cases are the ones where you have a partial record: a company with a registered office but no operating premises, a customer whose statement post is bouncing, a seller whose stated country conflicts with their payout account.

**Verifying** means establishing that the candidate string is genuinely connected to that person or company, to a standard you could defend to a regulator, a card scheme, or a court. That is an evidence problem, and evidence has grades.

The single most common failure in address programs is treating a completed lookup as a completed verification. An address that validates against a postal database is real. It is not therefore *theirs*.

## The evidence ladder

Nine methods, sorted by strength of proof rather than by ease of implementation. The two are close to inversely related, which is the uncomfortable part.

<!-- TABLE:START -->
| Method | Strength | What a pass proves | How it fails | Typical lawful basis |
| --- | --- | --- | --- | --- |
| Document plus identity binding | 5/5 | The person presenting the address document is the person named on it | Coerced or complicit third party; a genuine tenant fronting for someone else | Legal obligation under CDD |
| Physical delivery confirmation | 5/5 | Something reached a human at that address | Slow, expensive, and defeated by mail forwarding | Contract performance |
| Government or registry record | 4/5 | An authoritative body records this address against this person or company | Registry lag after a move; access limited or closed in many jurisdictions | Legal obligation, or public-register access rules |
| Proof-of-address document | 4/5 | A named third party sent this person post at this address recently | Edited PDFs and template forgeries; stale documents outside the date window | Legal obligation under CDD |
| Credit header or reference data match | 3/5 | A name and address pair appears together in bureau records | Thin-file and recently moved users; coverage drops sharply outside major markets | Legitimate interest, permissible purpose under local credit rules |
| AVS check at payment | 2/5 | The billing address matches what the card issuer holds | Stolen card used with the real billing address; partial-match codes | Fraud prevention, legitimate interest |
| Geolocation and IP consistency | 2/5 | The session is consistent, or inconsistent, with the claimed location | Proves the network path, never the residence; travel produces false alarms | Fraud prevention, legitimate interest |
| Postal format validation | 1/5 | The string is a deliverable address that exists | A real address the person has no connection to | Contract performance |
| Self-declared entry | 1/5 | Nothing beyond what the user typed | Any typo, any fabrication, no corroboration at all | Contract performance |
<!-- TABLE:END -->

```bash
python render_table.py --ladder     # same ranking with latency per method
python render_table.py --min 4      # only the methods that survive scrutiny
```

Read the "How it fails" column first. Every method on this list has a defeat condition, and the design question is never "which method is best" but "which two failure modes do not overlap."

## Stacking, and why one check is never enough

Pair one instant, high-coverage check with one documentary, high-strength check. The instant check clears the large majority of users at almost no cost and no friction. The documentary check carries the cases the first one flags, and carries your defensibility.

A worked pattern for a regulated onboarding flow:

1. **Validate the string.** Postal format API at the point of entry. Catches typos, normalizes formatting, and costs a fraction of a cent. Never treat a pass here as verification.
2. **Match against reference data.** A credit header or registry match, silent to the user. In mature markets this clears most genuine customers instantly.
3. **Route the remainder to documents.** Users who do not match get asked for a proof-of-address document. This is the group where the real risk sits, and it is small.
4. **Bind the document to the person.** An address document alone proves post arrived somewhere. Combined with identity verification on the same session, it proves the person holding it is the person named on it. That is the jump from 4 to 5 on the ladder.
5. **Escalate on conflict, not on volume.** A geolocation mismatch or a partial AVS code is a reason to look closer, never a reason to decline on its own.

The economics matter. Documentary checks cost real money per attempt and add friction that costs conversions, so a design that sends every user down that path is both expensive and worse: it trains your reviewers to rubber-stamp, because almost everything they see is genuine.

## Proof-of-address documents, and how they are actually forged

The commonly accepted set is narrow and consistent across most compliance programs: a utility bill, a bank or card statement, a tax bill, a tenancy agreement, an employment letter, or a government correspondence letter. Most programs require the document to be dated within the last three months and to show the full name and full address in the same view.

What makes a document trustworthy is not the category but four attributes:

- **Issuer independence.** Someone unconnected to the subject chose to send post there. A self-generated invoice proves nothing.
- **Recency.** People move. A six-month-old bill is evidence about a former address.
- **Consistency.** Name and address match the identity record exactly, including spelling and unit numbers.
- **Integrity.** The file has not been edited.

That last one is where the attacks land. The dominant forgery in 2026 is not a physical fake, it is a genuine PDF from a genuine provider with the name and address layer edited, or a template reproduction that renders convincingly at screen resolution. Both defeat a human reviewer glancing at a thumbnail. What catches them is machine inspection of the file itself: font substitution and kerning anomalies inside the text layer, object and metadata inconsistencies in the PDF structure, compression artifacts where a raster region was pasted, and cross-checks that the issuer, account format, and date are internally coherent.

Two practical rules follow. Accept the original file rather than a photograph of a screen wherever possible, because the original carries the metadata that makes tampering detectable. And treat a document that passes visual review but fails structural checks as the higher-risk signal, not the lower one, since a forger competent enough to look right is the one worth worrying about.

## Businesses that owe this to a regulator

For regulated entities, address verification is part of customer due diligence rather than a delivery nicety. Under AMLD in the EU, the BSA in the US, and equivalent regimes elsewhere, an obliged entity must identify and verify its customer, and residential address is a standard element of that identity record, particularly for risk scoring and for jurisdictional screening.

The framing that matters: the obligation sits with you as the operator. A verification vendor supplies the rail and the evidence trail; it does not assume your obligation, and no vendor can make you compliant. What a good provider gives you is a defensible record: what was checked, against what source, on what date, with what result, retained for the period your regime requires and no longer.

Sectors where this bites hardest are financial services and payments, crypto and digital assets, online gaming and gambling where residence determines licensing eligibility, lending and insurance, and any marketplace paying out money to sellers. If your business decides eligibility by jurisdiction, an unverified address is not a data-quality problem, it is a licensing exposure.

Two adjacent checks belong in the same design conversation. Sanctions and PEP screening depends on identity resolution that address data sharpens considerably, and [AML screening](https://www.idenfy.com/aml-compliance/) against a wrong or stale address produces both false negatives and expensive false positives. On the business side, confirming a company's operating premises against its registered office is a standard [KYB](https://www.idenfy.com/know-your-business-solution/) step, and a mismatch between the two is one of the more reliable shell-company indicators available.

## Where each check belongs in a product flow

- **At the payment step:** AVS, always. It is free, it rides inside the authorization, and it costs nothing in friction. Read the response codes properly: a partial match on street but not postcode is a different risk from a full mismatch, and treating them the same throws away the signal.
- **At signup:** postal validation inline, reference-data match in the background. Neither should be visible to a good customer.
- **At the money-out step:** the strongest check you have. Fraud concentrates on withdrawal and payout, not on registration, and a program that verifies hard at signup and loosely at payout has it backwards.
- **On change of address:** re-verify. An address change followed quickly by a payout request to a new destination is one of the highest-signal patterns in account takeover, and a flow that lets a user edit their address without any check has a hole in it regardless of how good the onboarding was.
- **Periodically, on risk:** regimes expect refresh on a risk-sensitive basis rather than on a fixed clock. Higher-risk customers get re-checked sooner.

## Data protection, kept short

An address is personal data everywhere and special-category-adjacent when combined with biometric identity checks, so three constraints apply regardless of jurisdiction.

Collect the minimum that answers the question. Store the verification result and its provenance rather than hoarding the raw document where your retention rules permit that. Set a retention period that matches the regime you are under and delete on schedule, because a warehouse of expired proof-of-address PDFs is a breach waiting for an attacker and serves no compliance purpose once the record is aged out. Where you are relying on legitimate interest rather than legal obligation, write the balancing test down before you launch, not after a complaint.

## FAQ

### How do I verify someone's address?

Ask the subject for a proof-of-address document issued within the last three months by an independent third party, such as a utility bill, bank statement, or tenancy agreement, then confirm the name and address match your identity record and that the file has not been altered. For stronger evidence, bind that document to the person in the same session with an identity check, so you prove the presenter is the named party rather than just that post arrived somewhere.

### How can I find someone's address legitimately?

In a business context you ask them, and the interesting work is confirming what they gave you. Where you hold only a partial record, the lawful routes are the ones tied to your relationship: registry and public-register lookups for companies, permissible-purpose reference data queries where local credit rules allow, and returned-mail handling. Tracing a private individual who has no relationship with you is a matter for a court, a licensed process server, or law enforcement.

### What counts as proof of address?

Most programs accept a utility bill, bank or credit card statement, tax bill, tenancy agreement, employment letter, or official government correspondence. The category matters less than four attributes: an independent issuer, a date inside your window (usually three months), an exact name and address match to the identity record, and an unedited file.

### Is address verification legally required?

For regulated entities it is part of the customer due diligence obligation under regimes such as the EU's AMLD and the US Bank Secrecy Act, and residence often also determines licensing eligibility in gambling and financial services. The obligation belongs to the operating business, not to its verification vendor. Confirm the specific requirement in each market you serve with counsel.

### What is AVS, and is it enough on its own?

The Address Verification Service compares the billing address entered at checkout with the one the card issuer holds, returning a match, partial match, or mismatch inside the authorization. It is free, instant, and worth always using, but it proves only that the entered address matches the issuer's record, so a stolen card presented with the correct billing address passes cleanly. Treat it as one signal in a fraud decision, never as identity verification.

### How do fraudsters defeat address checks?

Most commonly with a genuine document whose name and address layer has been edited, or a convincing template reproduction that survives a human glance. Others use a real address they have no connection to, mail forwarding services, or a complicit resident. The countermeasures are structural file inspection rather than visual review, recency limits, and binding the document to a verified identity rather than accepting it standalone.

### How long should proof-of-address documents be retained?

For exactly as long as the regime you operate under requires, and no longer. Store the verification outcome and its provenance in preference to the raw file where your rules allow it, and delete on a schedule you can evidence. An aged archive of address documents creates data-protection exposure without adding compliance value.

### Can an address be verified without asking the user for a document?

Often, yes. A credit header or reference-data match, or a government registry lookup where access exists, confirms a name and address pairing silently and clears most genuine customers with no friction. Coverage is the constraint: thin-file users, recent movers, and many markets outside the largest economies return no match, which is exactly the population that then needs the documentary path.

## Contributing and credits

To correct a strength rating, a failure mode, or a lawful-basis note, edit [methods.yaml](methods.yaml), run `python render_table.py --write`, and open a PR per [CONTRIBUTING.md](CONTRIBUTING.md). The topic outline was adapted from iDenfy's article on how to [find and verify someone's address](https://www.idenfy.com/blog/find-and-verify-someones-address/); iDenfy publishes that source. The evidence ladder, the failure modes, and the scope limits above are our own.

This repository is documentation, not legal advice. Address verification obligations, permissible-purpose rules, and public-register access differ by jurisdiction and change often. Confirm your own obligations with qualified counsel before building a flow on anything here.

## License

MIT. See [LICENSE](LICENSE).
