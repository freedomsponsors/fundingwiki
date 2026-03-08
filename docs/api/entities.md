# FundingWiki — Entity Details

## User

A person who can sponsor issues, solve them, or both.

| Attribute              | Type    | Description                                  |
|------------------------|---------|----------------------------------------------|
| screenName             | string  | Display name (unique, changeable once)       |
| realName               | string? | Full legal name                              |
| email                  | string  | Primary contact email (verified)             |
| paypalEmail            | string? | PayPal email for receiving payments          |
| bitcoinAddress         | string? | Bitcoin address for receiving payments       |
| website                | string? | Personal website URL                         |
| about                  | string? | Bio / description                            |
| preferredLanguage      | string? | Language code for content                    |
| reputation             | integer | Accumulated reputation from contributions    |
| status                 | enum    | active, inactive                             |
| emailPreferences       | object  | Notification toggles (comments, work, offers, payments, announcements) |

**Relationships:** has many Issue (created), has many Offer (sponsored), has many Solution (worked), has many Watch

## Project

An open-source project that issues belong to.

| Attribute   | Type     | Description                              |
|-------------|----------|------------------------------------------|
| name        | string   | Project name                             |
| description | string?  | Brief description                        |
| homeURL     | string?  | Project homepage                         |
| trackerURL  | string?  | Issue tracker URL                        |
| image       | image?   | Project logo (3:1 ratio)                 |
| language    | string?  | Primary programming language             |
| createdBy   | User     | User who registered this project         |

**Relationships:** has many Issue, has many Tag

## Issue

A problem or feature request that can be sponsored.

| Attribute    | Type     | Description                                        |
|--------------|----------|----------------------------------------------------|
| project      | Project? | Associated project                                 |
| key          | string?  | External tracker key                               |
| title        | string   | Issue title                                        |
| description  | string?  | Detailed description (supports revision history)   |
| trackerURL   | string?  | Link to external issue tracker                     |
| status       | enum     | open, closed                                       |
| isFeedback   | boolean  | Whether this is user feedback                      |
| isSponsored  | boolean  | Whether this issue has active offers               |
| language     | string?  | Content language code                              |
| points       | integer  | Community vote score                               |

**Relationships:** belongs to Project, has many Offer, has many Solution, has many IssueComment, has many Media, has many TechSolution, has many MultilingualTag, has many Watch

## Offer

A financial sponsorship pledge on an issue.

| Attribute          | Type      | Description                                      |
|--------------------|-----------|--------------------------------------------------|
| issue              | Issue     | The sponsored issue                              |
| sponsor            | User      | The user making the offer                        |
| price              | decimal   | Pledge amount                                    |
| currency           | enum      | USD, BRL, BTC                                    |
| status             | enum      | open, revoked, paid                              |
| acceptanceCriteria | string?   | What the sponsor requires for payment            |
| expirationDate     | datetime? | When the offer expires                           |
| noForking          | boolean   | Sponsor prefers no forking                       |
| requireRelease     | boolean   | Sponsor requires inclusion in a release          |

**Relationships:** belongs to Issue, belongs to User (sponsor), has many Payment, has many OfferComment

## Solution

A programmer's commitment to solve an issue.

| Attribute        | Type    | Description                               |
|------------------|---------|-------------------------------------------|
| issue            | Issue   | The issue being worked on                 |
| programmer       | User    | The user doing the work                   |
| status           | enum    | in_progress, done, aborted               |
| acceptingPayments| boolean | Whether the programmer accepts payments   |

**Relationships:** belongs to Issue, belongs to User (programmer), has many PaymentPart

## Payment

A money transfer from sponsor to programmer(s).

| Attribute    | Type     | Description                                        |
|--------------|----------|----------------------------------------------------|
| offer        | Offer    | The offer being fulfilled                          |
| status       | enum     | created, canceled, confirmed_web, confirmed_ipn, confirmed_ipn_underpay, confirmed_trn, confirmed_trn_underpay, forgotten |
| currency     | enum     | USD, BRL, BTC                                      |
| total        | decimal  | Payment total                                      |
| fee          | decimal  | Processing fee                                     |
| bitcoinTxHash| string?  | Bitcoin transaction hash (for BTC payments)        |
| paypalPayKey | string?  | PayPal pay key (for PayPal payments)               |

**Relationships:** belongs to Offer, has many PaymentPart

## PaymentPart

A portion of a payment directed to a specific programmer.

| Attribute | Type     | Description                             |
|-----------|----------|-----------------------------------------|
| payment   | Payment  | Parent payment                          |
| solution  | Solution | The solution being rewarded             |
| price     | decimal  | Amount allocated to this programmer     |

**Relationships:** belongs to Payment, belongs to Solution

## IssueComment

A comment on an issue.

| Attribute | Type   | Description                              |
|-----------|--------|------------------------------------------|
| issue     | Issue  | The issue being commented on             |
| author    | User   | Who wrote it                             |
| content   | string | Comment text                             |
| language  | string?| Content language code                    |

**Relationships:** belongs to Issue, belongs to User

## OfferComment

A comment on an offer (sponsor/programmer discussion).

| Attribute | Type   | Description                              |
|-----------|--------|------------------------------------------|
| offer     | Offer  | The offer being discussed                |
| author    | User   | Who wrote it                             |
| content   | string | Comment text                             |

**Relationships:** belongs to Offer, belongs to User

## Media

An image or video attached to an issue.

| Attribute | Type   | Description                                |
|-----------|--------|--------------------------------------------|
| issue     | Issue  | The issue this media belongs to            |
| title     | string | Media title                                |
| content   | string?| Description                                |
| url       | string | Media URL                                  |
| type      | enum   | url (image), vid (video)                   |
| createdBy | User   | Who uploaded it                            |
| karma     | integer| Community score                            |
| deleted   | boolean| Soft-delete flag                           |

**Relationships:** belongs to Issue, belongs to User

## TechSolution

A knowledge-base article proposing a technical approach for an issue.

| Attribute | Type    | Description                              |
|-----------|---------|------------------------------------------|
| issue     | Issue   | The issue this solution addresses        |
| title     | string  | Solution title                           |
| content   | string  | Detailed technical proposal              |
| createdBy | User    | Author                                   |
| karma     | integer | Community vote score                     |
| language  | string? | Content language code                    |
| points    | integer | Reputation points                        |
| deleted   | boolean | Soft-delete flag                         |

**Relationships:** belongs to Issue, belongs to User, has many TechSolutionComment

## Idea

A brainstorm submission for future issues or features.

| Attribute | Type    | Description                              |
|-----------|---------|------------------------------------------|
| content   | string  | Idea description                         |
| point     | integer | Reputation score                         |
| createdBy | User    | Author                                   |
| ideaFrom  | string? | Source/origin of the idea                |

**Relationships:** belongs to User

## Watch

A subscription to notifications about an issue or project.

| Attribute | Type   | Description                              |
|-----------|--------|------------------------------------------|
| user      | User   | The subscriber                           |
| entity    | enum   | issue, project                           |
| entityId  | ID     | The watched entity's ID                  |
| reason    | string?| Why the user is watching                 |

**Relationships:** belongs to User

## Tag

A simple text tag on a project.

| Attribute | Type    | Description                              |
|-----------|---------|------------------------------------------|
| name      | string  | Tag text                                 |
| project   | Project | The tagged project                       |

**Relationships:** belongs to Project

## MultilingualTag

A Wikidata-backed semantic tag with translations.

| Attribute   | Type   | Description                              |
|-------------|--------|------------------------------------------|
| qid         | string | Wikidata Q-identifier (e.g., Q9143)      |
| slug        | string | URL-friendly identifier                  |
| title       | string | Default display title                    |
| description | string?| Tag description                          |

**Relationships:** has many Issue (many-to-many), has many translations

## Rates

Current currency exchange rates.

| Attribute      | Type   | Description                              |
|----------------|--------|------------------------------------------|
| blockchainData | object | Bitcoin exchange rates (BTC ↔ USD/BRL)   |
| oerData        | object | Fiat exchange rates (USD ↔ BRL)          |

---

## Value Objects

### IssueFilter

Criteria for searching/filtering issues.

| Attribute    | Type     | Description                              |
|--------------|----------|------------------------------------------|
| projectId    | ID?      | Filter by project                        |
| projectName  | string?  | Filter by project name                   |
| searchTerms  | string?  | Full-text search                         |
| isSponsored  | boolean? | Only sponsored issues                    |
| sortBy       | enum?    | Sorting field                            |
| ascending    | boolean? | Sort direction                           |
| tags         | string[]?| Filter by tags                           |
| language     | string?  | Filter by content language               |
| noProposals  | boolean? | Issues without solutions                 |
| hasSponsors  | boolean? | Issues with active offers                |

### OfferTerms

Terms for creating or editing an offer.

| Attribute          | Type      | Description                              |
|--------------------|-----------|------------------------------------------|
| price              | decimal   | Pledge amount                            |
| currency           | enum      | USD, BRL, BTC                            |
| acceptanceCriteria | string?   | What must be true for payment            |
| expirationDate     | datetime? | When the offer expires                   |
| noForking          | boolean?  | Prefer no forking                        |
| requireRelease     | boolean?  | Require inclusion in release             |

### VoteAction

A vote direction.

| Value  | Description           |
|--------|-----------------------|
| up     | Upvote                |
| down   | Downvote              |
| cancel | Cancel existing vote  |

### Currency

Supported currencies.

| Value | Description       |
|-------|-------------------|
| USD   | US Dollar         |
| BRL   | Brazilian Real    |
| BTC   | Bitcoin           |

### PaymentConfirm

Confirmation details from a payment provider.

| Attribute       | Type    | Description                              |
|-----------------|---------|------------------------------------------|
| payKey          | string? | PayPal payment key                       |
| transactionHash | string? | Bitcoin transaction hash                 |
| amountReceived  | decimal?| Actual amount received                   |
