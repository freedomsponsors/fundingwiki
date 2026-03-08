# FundingWiki — Conceptual API

> Crowdfunding management system where sponsors fund issues and programmers get paid for solving them.

## Entities

| Entity          | Description                                                  |
|-----------------|--------------------------------------------------------------|
| User            | A person who can sponsor issues, solve them, or both         |
| Project         | An open-source project that issues belong to                 |
| Issue           | A problem or feature request that can be sponsored           |
| Offer           | A financial sponsorship pledge on an issue                   |
| Solution        | A programmer's commitment to solve an issue                  |
| Payment         | A money transfer from sponsor to programmer(s)              |
| PaymentPart     | A portion of a payment directed to a specific programmer     |
| IssueComment    | A comment on an issue                                        |
| OfferComment    | A comment on an offer (sponsor/programmer discussion)        |
| Media           | An image or video attached to an issue                       |
| TechSolution    | A knowledge-base article proposing a technical approach      |
| Idea            | A brainstorm submission for future issues or features        |
| Watch           | A subscription to notifications about an issue or project    |
| MultilingualTag | A Wikidata-backed semantic tag with translations             |
| Rates           | Current currency exchange rates (USD, BRL, BTC)              |

## Value Objects

| Name              | Used by                   | Description                                          |
|-------------------|---------------------------|------------------------------------------------------|
| IssueFilter       | issues.search             | Criteria for searching/filtering issues              |
| VoteAction        | issues.vote, ideas.vote   | A vote direction: up, down, or cancel                |
| Currency          | offers.create, payments.* | Supported currency: USD, BRL, BTC                    |
| OfferTerms        | offers.create, offers.edit| Price, currency, acceptance criteria, expiration     |
| PaymentConfirm    | payments.confirmWeb, ...  | Confirmation details from PayPal or Bitcoin network  |

## Operations

### Issues

| Operation                  | Input                                              | Output      | Description                                    |
|----------------------------|----------------------------------------------------|-------------|------------------------------------------------|
| issues.create              | title, description, project?, trackerURL?          | Issue       | Create a new issue                             |
| issues.edit                | issueId, title?, description?, trackerURL?         | Issue       | Modify an existing issue                       |
| issues.search              | filter?: IssueFilter                               | Issue[]     | Search and list issues with filters            |
| issues.get                 | issueId                                            | Issue       | Get issue details                              |
| issues.vote                | issueId, action: VoteAction                        | void        | Vote up/down on an issue or cancel vote        |
| issues.random              | —                                                  | Issue       | Get a random issue                             |

### Offers (Sponsorship)

| Operation                  | Input                                              | Output      | Description                                    |
|----------------------------|----------------------------------------------------|-------------|------------------------------------------------|
| offers.sponsorNew          | title, description, terms: OfferTerms              | Offer+Issue | Create a new issue and immediately sponsor it with an offer |
| offers.kickstart           | title, description                                 | Issue       | Propose a new issue without funding, hoping others will sponsor it |
| offers.sponsorExisting     | issueId, terms: OfferTerms                         | Offer       | Add a sponsorship offer to an existing issue   |
| offers.edit                | offerId, terms: OfferTerms                         | Offer       | Modify offer terms                             |
| offers.revoke              | offerId                                            | Offer       | Cancel an offer (sponsor only)                 |

### Solutions

| Operation                  | Input                                              | Output      | Description                                    |
|----------------------------|----------------------------------------------------|-------------|------------------------------------------------|
| solutions.start            | issueId                                            | Solution    | Programmer begins working on an issue          |
| solutions.resolve          | solutionId                                         | Solution    | Mark solution as done, ready for payment       |
| solutions.abort            | solutionId                                         | Solution    | Abandon work on a solution                     |

### Payments

| Operation                  | Input                                              | Output      | Description                                    |
|----------------------------|----------------------------------------------------|-------------|------------------------------------------------|
| payments.create            | offerId, parts: PaymentPart[]                      | Payment     | Initiate payment from sponsor to programmer(s) |
| payments.confirmWeb        | paymentId                                          | Payment     | Confirm payment via web redirect (PayPal)      |
| payments.confirmIPN        | paymentId, confirm: PaymentConfirm                 | Payment     | Confirm payment via IPN callback               |
| payments.confirmBitcoin    | paymentId, confirm: PaymentConfirm                 | Payment     | Confirm payment via Bitcoin transaction         |
| payments.forget            | paymentId                                          | Payment     | Discard a pending payment                      |
| payments.payProgrammers    | paymentId                                          | Payment     | Distribute Bitcoin to programmer addresses     |

### Comments

| Operation                  | Input                                              | Output       | Description                                   |
|----------------------------|----------------------------------------------------|--------------|-----------------------------------------------|
| comments.addToIssue        | issueId, content                                   | IssueComment | Add a comment to an issue                     |
| comments.editOnIssue       | commentId, content                                 | IssueComment | Edit an issue comment (author only)           |
| comments.addToOffer        | offerId, content                                   | OfferComment | Add a comment to an offer                     |
| comments.editOnOffer       | commentId, content                                 | OfferComment | Edit an offer comment (author only)           |

### Users

| Operation                  | Input                                              | Output      | Description                                    |
|----------------------------|----------------------------------------------------|-------------|------------------------------------------------|
| users.editProfile          | screenName?, realName?, paypalEmail?, about?, ...   | User        | Update user profile                            |
| users.deactivate           | userId                                             | void        | Deactivate account (aborts solutions, revokes offers) |
| users.verifyEmail          | token                                              | void        | Confirm email address change                   |

### Projects

| Operation                  | Input                                              | Output      | Description                                    |
|----------------------------|----------------------------------------------------|-------------|------------------------------------------------|
| projects.list              | —                                                  | Project[]   | List all projects                              |
| projects.get               | projectId                                          | Project     | Get project details with stats                 |
| projects.edit              | projectId, name?, description?, homeURL?           | Project     | Update project information                     |

### Watches

| Operation                  | Input                                              | Output      | Description                                    |
|----------------------------|----------------------------------------------------|-------------|------------------------------------------------|
| watches.toggle             | entity: enum, entityId                             | Watch?      | Subscribe/unsubscribe from notifications       |

### Ideas (Brainstorming)

| Operation                  | Input                                              | Output      | Description                                    |
|----------------------------|----------------------------------------------------|-------------|------------------------------------------------|
| ideas.create               | content                                            | Idea        | Submit a new idea                              |
| ideas.list                 | —                                                  | Idea[]      | List all ideas                                 |
| ideas.listMine             | —                                                  | Idea[]      | List current user's ideas                      |
| ideas.findSimilar          | ideaId                                             | Idea[]      | Find semantically similar ideas (FAISS)        |
| ideas.vote                 | ideaId, action: VoteAction                         | void        | Vote on an idea                                |

### Tech Solutions (Knowledge Base)

| Operation                  | Input                                              | Output       | Description                                   |
|----------------------------|----------------------------------------------------|--------------|-----------------------------------------------|
| techSolutions.create       | issueId, title, content                            | TechSolution | Propose a technical approach for an issue      |
| techSolutions.list         | issueId                                            | TechSolution[] | List solutions for an issue                  |
| techSolutions.vote         | solutionId, action: VoteAction                     | void         | Vote on a tech solution                        |

### Tags

| Operation                  | Input                                              | Output          | Description                                |
|----------------------------|----------------------------------------------------|-----------------|---------------------------------------------|
| tags.add                   | entityType, entityId, name                         | Tag             | Add a simple tag                            |
| tags.addMultilingual       | issueId, qid: string                               | MultilingualTag | Add a Wikidata-backed tag to an issue       |
| tags.remove                | entityType, entityId, name                         | void            | Remove a tag                                |

### Currency

| Operation                  | Input                                              | Output      | Description                                    |
|----------------------------|----------------------------------------------------|-------------|------------------------------------------------|
| currency.getRate           | from: Currency, to: Currency                       | decimal     | Get current exchange rate (with payment fees)  |

## Invariants

- An offer can only be revoked by its sponsor
- A solution can only be aborted by its programmer
- A comment can only be edited by its author
- Account balance flows: offer status goes OPEN → PAID or OPEN → REVOKED (no other transitions)
- Solution lifecycle: IN_PROGRESS → DONE or IN_PROGRESS → ABORTED (DONE can reopen to IN_PROGRESS)
- Offer expiration: expired offers cannot be paid
- Username can only be changed once (during onboarding)
- Tracker URLs are deduplicated — no two issues share the same tracker URL
- Every payment must reference an existing open offer
- Bitcoin payments require 3 confirmations before being considered confirmed

## Side Effects

| Trigger                    | Effect                                                        |
|----------------------------|---------------------------------------------------------------|
| offers.sponsorNew          | Watchers notified, issue creator gains reputation             |
| offers.sponsorExisting     | Watchers notified of new offer                                |
| offers.edit                | Watchers notified of offer change                             |
| offers.revoke              | Watchers notified of revocation                               |
| solutions.start            | Watchers notified work has begun                              |
| solutions.resolve          | Watchers notified work is done                                |
| solutions.abort            | Watchers notified work has stopped                            |
| payments.confirm*          | Sponsor and programmer notified, admin notified               |
| payments.payProgrammers    | Programmers notified of Bitcoin payment pending confirmation   |
| comments.addToIssue        | Issue watchers notified                                       |
| comments.addToOffer        | Offer watchers notified                                       |
| users.deactivate           | All user's in-progress solutions aborted, open offers revoked |
| users.editProfile          | Verification email sent if email changed                      |
