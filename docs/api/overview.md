# FundingWiki — Conceptual API

> Crowdfunding, crowdsourcing  and task management platform combining StackOverflow-style reputation, GitHub Issues, bounties, and crowdfunding. Sponsors sponsor Issues; Developers execute them and get paid; Advisors propose approaches; Communicators contribute media; Entrepreneurs create the Issues that start everything.

## User roles

| Role         | Description                                                                        |
|--------------|------------------------------------------------------------------------------------|
| Entrepreneur | Creates Issues (tasks, questions, ideas, concerns)                                 |
| Advisor      | Writes textual proposals (TechSolutions) on how an Issue could be addressed        |
| Communicator | Contributes media (graphics, video) as marketing strategies for Issues or projects |
| Developer    | Executes Issues in practice — not necessarily a programmer                         |
| Sponsor       | Makes financial contributions: task payments or open donations                     |

A single User can hold multiple roles simultaneously.

---

## Entities

| Entity               | Description                                                                           |
|----------------------|---------------------------------------------------------------------------------------|
| User                 | A person who participates in one or more roles                                        |
| Project              | An initiative grouping related Issues under a shared goal                             |
| Issue                | The central entity: any actionable, fundable task, idea, question or concern          |
| Wiki                 | Collaborative documentation attached to an Issue, Project or TechSolution *(pending)* |
| WikiRevision         | Historical snapshot of a Wiki page *(pending)*                                        |
| Offer                | A financial sponsorship pledge on an Issue, made by a Sponsor                         |
| Solution             | A Developer's commitment to execute an Issue                                          |
| Payment              | A money transfer from Sponsor to Developer(s)                                         |
| PaymentPart          | A portion of a Payment directed to a specific Developer                               |
| IssueComment         | A comment on an Issue                                                                 |
| OfferComment         | A comment on an Offer (Sponsor/Developer discussion)                                  |
| Media                | An image or video attached to an Issue, contributed by a Communicator                 |
| TechSolution         | A textual proposal by an Advisor on how to address an Issue                           |
| Watch                | A subscription to notifications about an Issue or Project                             |
| Tag                  | A simple text tag on a Project or Issue *(to be removed)*                             |
| MultilingualTag      | A Wikidata-backed semantic tag with translations, usable on Issues or Projects        |
| Rates                | Current currency exchange rates (USD, BRL, BTC)                                       |

---

## Value Objects

| Name           | Used by                    | Description                                          |
|----------------|----------------------------|------------------------------------------------------|
| IssueFilter    | issues.search              | Criteria for searching/filtering Issues              |
| VoteAction     | issues.vote, tech.vote     | A vote direction: up, down, or cancel                |
| Currency       | offers.create, payments.*  | Supported currency: USD, BRL, BTC                    |
| OfferTerms     | offers.create, offers.edit | Price, currency, acceptance criteria, expiration     |
| PaymentConfirm | payments.confirmWeb, …     | Confirmation details from PayPal or Bitcoin network  |

---

## Operations

### Issues

| Operation                | Input                                                   | Output    | Description                                                        |
|--------------------------|---------------------------------------------------------|-----------|--------------------------------------------------------------------|
| issues.create            | title, description, project[]?, trackerURL?, isPrivate? | Issue     | Create a new Issue (Entrepreneur role). Can belong to multiple Projects|
| issues.edit              | issueId, title?, description?, trackerURL?, isPrivate?  | Issue     | Modify an existing Issue (revision history in progress)            |
| issues.search            | filter?: IssueFilter                                    | Issue[]   | Search and list Issues with filters                                |
| issues.get               | issueId                                                 | Issue     | Get Issue details                                                  |
| issues.vote              | issueId, action: VoteAction                             | void      | Vote up/down on an Issue or cancel vote                            |
| issues.random            | —                                                       | Issue     | Get a random Issue                                                 |
| issues.togglePrivacy     | issueId                                                 | Issue     | Toggle public/private status (author only)                         |
| issues.addToProject      | issueId, projectId                                      | Issue     | Associate an existing Issue with an additional Project             |
| issues.removeFromProject | issueId, projectId                                      | Issue     | Remove an Issue from a Project                                     |

### Wiki *(pending implementation)*

| Operation       | Input                             | Output       | Description                                           |
|-----------------|-----------------------------------|--------------|-------------------------------------------------------|
| wiki.get        | entity: enum, entityId            | Wiki         | Get the Wiki for an Issue or Project                  |
| wiki.edit       | wikiId, content                   | Wiki         | Edit the Wiki body (creates a WikiRevision snapshot)  |
| wiki.history    | wikiId                            | WikiRevision[] | List all revisions of a Wiki page                   |
| wiki.restore    | revisionId                        | Wiki         | Restore a previous revision                           |

### Offers (Sponsorship)

| Operation              | Input                                    | Output      | Description                                                         |
|------------------------|------------------------------------------|-------------|---------------------------------------------------------------------|
| offers.sponsorNew      | title, description, terms: OfferTerms    | Offer+Issue | Create a new Issue and immediately sponsor it (Sponsor role)         |
| offers.sponsorExisting | issueId, terms: OfferTerms               | Offer       | Add a sponsorship Offer to an existing Issue                        |
| offers.edit            | offerId, terms: OfferTerms               | Offer       | Modify Offer terms                                                  |
| offers.revoke          | offerId                                  | Offer       | Cancel an Offer (Sponsor only)                                       |

> **Task payments vs Donations:** Offers tied to a specific resolution are task payments (refundable if unresolved by expiration date). Offers without resolution requirements are donations (different refund rules). Refund logic is not yet implemented — handled manually in case of conflict.

### Solutions

| Operation         | Input        | Output   | Description                                              |
|-------------------|--------------|----------|----------------------------------------------------------|
| solutions.start   | issueId      | Solution | Developer begins working on an Issue                     |
| solutions.resolve | solutionId   | Solution | Mark Solution as done, ready for payment                 |
| solutions.abort   | solutionId   | Solution | Developer abandons work on a Solution                    |

### Payments

| Operation                | Input                                   | Output   | Description                                            |
|--------------------------|-----------------------------------------|----------|--------------------------------------------------------|
| payments.create          | offerId, parts: PaymentPart[]           | Payment  | Initiate payment from Sponsor to Developer(s)          |
| payments.confirmWeb      | paymentId                               | Payment  | Confirm payment via web redirect (PayPal)              |
| payments.confirmIPN      | paymentId, confirm: PaymentConfirm      | Payment  | Confirm payment via IPN callback                       |
| payments.confirmBitcoin  | paymentId, confirm: PaymentConfirm      | Payment  | Confirm payment via Bitcoin transaction                |
| payments.forget          | paymentId                               | Payment  | Discard a pending payment                              |
| payments.payDevelopers   | paymentId                               | Payment  | Distribute Bitcoin to Developer addresses              |

### Comments

| Operation               | Input                | Output       | Description                                |
|-------------------------|----------------------|--------------|--------------------------------------------|
| comments.addToIssue     | issueId, content     | IssueComment | Add a comment to an Issue                  |
| comments.editOnIssue    | commentId, content   | IssueComment | Edit an Issue comment (author only)        |
| comments.addToOffer     | offerId, content     | OfferComment | Add a comment to an Offer                  |
| comments.editOnOffer    | commentId, content   | OfferComment | Edit an Offer comment (author only)        |

### Users

| Operation          | Input                                           | Output | Description                                                      |
|--------------------|-------------------------------------------------|--------|------------------------------------------------------------------|
| users.editProfile  | screenName?, realName?, paypalEmail?, about?, … | User   | Update user profile                                              |
| users.deactivate   | userId                                          | void   | Deactivate account (aborts Solutions, revokes Offers)            |
| users.verifyEmail  | token                                           | void   | Confirm email address change                                     |

### Reputation *(pending full implementation)*

| Operation               | Input              | Output   | Description                                     |
|-------------------------|--------------------|----------|-------------------------------------------------|
| reputation.getForUser   | userId             | integer  | Get current reputation score for a User         |
| reputation.getPrivileges| userId             | string[] | List privileges unlocked by current reputation  |
| reputation.getBadges    | userId             | Badge[]  | List badges earned by a User                    |

### Projects

| Operation      | Input                                        | Output    | Description                             |
|----------------|----------------------------------------------|-----------|-----------------------------------------|
| projects.list  | —                                            | Project[] | List all Projects                       |
| projects.get   | projectId                                    | Project   | Get Project details with stats          |
| projects.edit  | projectId, name?, description?, homeURL?, …  | Project   | Update Project information              |

### Watches

| Operation      | Input                   | Output  | Description                                      |
|----------------|-------------------------|---------|--------------------------------------------------|
| watches.toggle | entity: enum, entityId  | Watch?  | Subscribe/unsubscribe from notifications         |

### Tech Solutions (Advisor Knowledge Base)

| Operation            | Input                        | Output          | Description                                  |
|----------------------|------------------------------|-----------------|----------------------------------------------|
| techSolutions.create | issueId, title, content      | TechSolution    | Advisor proposes a textual approach for an Issue |
| techSolutions.list   | issueId                      | TechSolution[]  | List proposals for an Issue                  |
| techSolutions.vote   | solutionId, action: VoteAction | void          | Vote on a TechSolution                       |

### Media (Communicator Contributions)

| Operation     | Input                             | Output  | Description                                       |
|---------------|-----------------------------------|---------|---------------------------------------------------|
| media.add     | issueId, title, url, type, content? | Media | Communicator attaches an image or video to an Issue |
| media.vote    | mediaId, action: VoteAction       | void    | Vote on a Media item                              |
| media.delete  | mediaId                           | void    | Soft-delete a Media item (author only)            |

### Tags

| Operation                | Input                   | Output            | Description                                                         |
|--------------------------|-------------------------|-------------------|---------------------------------------------------------------------|
| tags.search              | query, language?        | MultilingualTag[] | Search Wikidata for tag suggestions (autocomplete)                  |
| tags.addToProject        | projectId, name         | Tag               | Add a simple text tag to a Project                                  |
| tags.removeFromProject   | projectId, name         | void              | Remove a simple text tag from a Project                             |
| tags.addToIssue          | issueId, qid: string    | MultilingualTag   | Add a Wikidata-backed tag to an Issue                               |
| tags.removeFromIssue     | issueId, qid: string    | void              | Remove a Wikidata-backed tag from an Issue                          |
| tags.addToProjectWikidata| projectId, qid: string  | MultilingualTag   | Add a Wikidata-backed tag to a Project                              |
| tags.removeFromProjectWikidata | projectId, qid: string | void        | Remove a Wikidata-backed tag from a Project                         |

### Currency

| Operation        | Input                          | Output  | Description                                        |
|------------------|--------------------------------|---------|----------------------------------------------------|
| currency.getRate | from: Currency, to: Currency   | decimal | Get current exchange rate (with payment fees)      |

---

## Invariants

- An Offer can only be revoked by its Sponsor
- A Solution can only be aborted by its Developer
- A comment can only be edited by its author
- Offer status transitions: OPEN → PAID or OPEN → REVOKED only
- Solution lifecycle: IN_PROGRESS → DONE or IN_PROGRESS → ABORTED (DONE can reopen to IN_PROGRESS)
- Expired Offers cannot be paid
- Username can only be changed once (during onboarding)
- Tracker URLs are deduplicated — no two Issues share the same tracker URL
- Every Payment must reference an existing open Offer
- Bitcoin payments require 3 confirmations before being considered confirmed
- An Issue can belong to more than one Project (many-to-many)
- A MultilingualTag can be applied to both Issues and Projects
- Private Issues are only visible to their author and invited collaborators

---

## Side Effects

| Trigger                      | Effect                                                            |
|------------------------------|-------------------------------------------------------------------|
| offers.sponsorNew            | Watchers notified; Issue Entrepreneur gains reputation                |
| offers.sponsorExisting       | Watchers notified of new Offer                                    |
| offers.edit                  | Watchers notified of Offer change                                 |
| offers.revoke                | Watchers notified of revocation                                   |
| solutions.start              | Watchers notified work has begun                                  |
| solutions.resolve            | Watchers notified work is done; Developer gains reputation        |
| solutions.abort              | Watchers notified work has stopped                                |
| payments.confirm*            | Sponsor and Developer notified; admin notified                     |
| payments.payDevelopers       | Developers notified of Bitcoin payment pending confirmation       |
| comments.addToIssue          | Issue Watchers notified                                           |
| comments.addToOffer          | Offer Watchers notified                                           |
| techSolutions.create         | Issue Watchers notified of new Advisor proposal                   |
| media.add                    | Issue Watchers notified of new Communicator media                   |
| issues.vote                  | Entrepreneur reputation updated                                       |
| techSolutions.vote           | Advisor reputation updated                                        |
| users.deactivate             | All in-progress Solutions aborted; open Offers revoked            |
| users.editProfile            | Verification email sent if email changed                          |
| wiki.edit *(pending)*        | Issue or Project Watchers notified of Wiki update                 |

---

## Implementation Status

| Feature                                           | Status         |
|---------------------------------------------------|----------------|
| Issues: create, edit, vote, comment               | ✅ Done         |
| Issues: generate from external tracker URLs       | ✅ Done         |
| Issues: payments (Offers)                         | ✅ Done         |
| Issues: group in Projects                         | ✅ Done         |
| Issues: belong to more than one Project           | ❌ Pending      |
| Issues: edit history                              | 🔄 In progress |
| Issues: private/public toggle                     | ❌ Pending      |
| Ideas merged into Issues                          | ❌ Pending      |
| Reputation system                                 | ✅ Done         |
| Badges system                                     | ❌ Pending      |
| Wiki (Issue & Project)                            | ❌ Pending      |
| MultilingualTag saved to DB after Wikidata lookup | ✅ Done         |
| MultilingualTag on Projects                       | ❌ Pending      |
| Media (Communicator): upload photos, embed video  | ✅ Done         |
| Refunds (task payments)                           | ❌ Pending      |
