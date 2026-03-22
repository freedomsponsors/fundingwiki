# FundingWiki — Entity Details

## User

A person who participates in the platform in one or more roles.

| Attribute         | Type    | Description                                                        |
|-------------------|---------|--------------------------------------------------------------------|
| screenName        | string  | Display name (unique, changeable once during onboarding)           |
| realName          | string? | Full legal name                                                    |
| email             | string  | Primary contact email (verified)                                   |
| paypalEmail       | string? | PayPal email for receiving payments                                |
| bitcoinAddress    | string? | Bitcoin address for receiving payments                             |
| website           | string? | Personal website URL                                               |
| about             | string? | Bio / description                                                  |
| preferredLanguage | string? | Language code for content                                          |
| reputation        | integer | Accumulated reputation points from community contributions         |
| status            | enum    | active, inactive                                                   |
| emailPreferences  | object  | Notification toggles (comments, work, offers, payments, announcements) |

**Roles a user can hold:** Entrepreneur, Advisor, Communicator, Developer, Sponsor

**Relationships:** has many Issue (proposed), has many Offer (funded), has many Solution (worked), has many TechSolution (advised), has many Media (campaigned), has many Watch

---

## Reputation

A StackOverflow-inspired karma system reflecting community trust. Reputation gates access to platform privileges.

| Event                                         | Points   |
|-----------------------------------------------|----------|
| Someone upvotes your Issue or TechSolution    | +10      |
| Your TechSolution is marked as best answer    | +15      |
| Someone downvotes your Issue or TechSolution  | −2       |
| You cast a downvote (discourages abuse)       | −1       |
| Offer you funded gets paid out                | +5       |
| Issue you proposed gets resolved              | +10      |

**Privilege thresholds (indicative, to be confirmed in implementation):**

| Reputation | Privilege unlocked                              |
|------------|-------------------------------------------------|
| 50         | Comment on other users' Issues                  |
| 150        | Create new Tags                                 |
| 1,000      | Edit other users' Issues without review         |
| 10,000     | Access moderation tools (view deleted content)  |

**Badges:** Gold, silver, and bronze badges reward specific achievements (excellent Issues, well-voted TechSolutions, correct platform usage). Badges are independent of reputation points.

> ⚠️ Full reputation and badge logic is **pending implementation**.

---

## Project

An initiative that groups related Issues under a shared goal. Projects can receive donations and have a formal organization behind them.

| Attribute   | Type    | Description                              |
|-------------|---------|------------------------------------------|
| name        | string  | Project name                             |
| description | string? | Brief description                        |
| homeURL     | string? | Project homepage                         |
| trackerURL  | string? | Issue tracker URL                        |
| image       | image?  | Project logo (3:1 ratio)                 |
| language    | string? | Primary language of the project          |
| createdBy   | User    | User who registered this project         |

**Relationships:** has many Issue (many-to-many), has many Tag, has many MultilingualTag

---

## Issue

The central entity of FundingWiki. An Issue is any text from which an actionable, potentially fundable task can be extracted. This includes problems, feature requests, questions, ideas, and concerns — all unified under this entity (previously split into "Issue" and "Idea").

| Attribute    | Type     | Description                                                      |
|--------------|----------|------------------------------------------------------------------|
| title        | string   | Issue title                                                      |
| description  | string?  | Detailed description (supports revision history — in progress)   |
| trackerURL   | string?  | Link to external issue tracker (deduplicated — no two Issues share the same URL) |
| status       | enum     | open, closed                                                     |
| isFeedback   | boolean  | Whether this is user feedback                                    |
| isSponsored  | boolean  | Whether this Issue has active Offers                             |
| language     | string?  | Content language code                                            |
| points       | integer  | Community vote score                                             |
| isPrivate    | boolean  | Whether the Issue is private (default: false; user can toggle)   |
| ideaFrom     | string?  | Source/origin if the Issue originated as an idea or external input |
| createdBy    | User     | The Entrepreneur who created this Issue                              |

**Projects:** An Issue can belong to **more than one Project** (many-to-many).

**Relationships:** belongs to many Project, has many Offer, has many Solution, has many IssueComment, has many Media, has many TechSolution, has many MultilingualTag, has many Watch

---

## Wiki

A collaborative knowledge base attached to an Issue, Project or TechSolution, allowing structured documentation to be built collectively by the community.

| Attribute   | Type    | Description                                      |
|-------------|---------|--------------------------------------------------|
| entity      | enum    | issue, project                                   |
| entityId    | ID      | The Issue or Project this Wiki belongs to        |
| content     | string  | Wiki body (supports revision history)            |
| createdBy   | User    | Author of the initial version                    |
| updatedBy   | User?   | Last editor                                      |
| language    | string? | Content language code                            |

**Relationships:** belongs to Issue , Project or TechSolution, has many WikiRevision

> ⚠️ Wiki is **pending implementation**.

---

## WikiRevision

A historical snapshot of a Wiki page, enabling full edit history.

| Attribute  | Type    | Description                              |
|------------|---------|------------------------------------------|
| wiki       | Wiki    | The Wiki this revision belongs to        |
| content    | string  | Content at this point in time            |
| editedBy   | User    | Who made this edit                       |
| editedAt   | datetime| When this revision was created           |

> ⚠️ WikiRevision is **pending implementation**.

---

## Offer

A financial sponsorship pledge on an Issue, made by a Sponsor.

| Attribute          | Type      | Description                             |
|--------------------|-----------|-----------------------------------------|
| issue              | Issue     | The sponsored Issue                     |
| sponsor            | User      | The User making the offer               |
| price              | decimal   | Pledge amount                           |
| currency           | enum      | USD, BRL, BTC                           |
| status             | enum      | open, revoked, paid                     |
| acceptanceCriteria | string?   | What the Sponsor requires for payment   |
| expirationDate     | datetime? | When the offer expires                  |
| noForking          | boolean   | Sponsor prefers no forking              |
| requireRelease     | boolean   | Sponsor requires inclusion in a release |

> **Payments vs Donations:** Offers tied to a specific resolution are *task payments* (refundable if unresolved). Offers without resolution requirements are *donations* (different refund rules). Refund logic is **not yet implemented** — handled manually in case of conflict.

**Relationships:** belongs to Issue, belongs to User (Sponsor), has many Payment, has many OfferComment

---

## Solution

A Developer's commitment to execute an Issue in practice.

| Attribute         | Type    | Description                               |
|-------------------|---------|-------------------------------------------|
| issue             | Issue   | The Issue being worked on                 |
| developer         | User    | The Developer doing the work              |
| status            | enum    | in_progress, done, aborted                |
| acceptingPayments | boolean | Whether the Developer accepts payments    |

**Relationships:** belongs to Issue, belongs to User (Developer), has many PaymentPart

---

## Payment

A money transfer from a Sponsor to one or more Developers.

| Attribute     | Type    | Description                                                             |
|---------------|---------|-------------------------------------------------------------------------|
| offer         | Offer   | The Offer being fulfilled                                               |
| status        | enum    | created, canceled, confirmed_web, confirmed_ipn, confirmed_ipn_underpay, confirmed_trn, confirmed_trn_underpay, forgotten |
| currency      | enum    | USD, BRL, BTC                                                           |
| total         | decimal | Payment total                                                           |
| fee           | decimal | Processing fee                                                          |
| bitcoinTxHash | string? | Bitcoin transaction hash (for BTC payments)                             |
| paypalPayKey  | string? | PayPal pay key (for PayPal payments)                                    |

**Relationships:** belongs to Offer, has many PaymentPart

---

## PaymentPart

A portion of a Payment directed to a specific Developer.

| Attribute | Type     | Description                             |
|-----------|----------|-----------------------------------------|
| payment   | Payment  | Parent Payment                          |
| solution  | Solution | The Solution being rewarded             |
| price     | decimal  | Amount allocated to this Developer      |

**Relationships:** belongs to Payment, belongs to Solution

---

## IssueComment

A comment on an Issue.

| Attribute | Type    | Description                              |
|-----------|---------|------------------------------------------|
| issue     | Issue   | The Issue being commented on             |
| author    | User    | Who wrote it                             |
| content   | string  | Comment text                             |
| language  | string? | Content language code                    |

**Relationships:** belongs to Issue, belongs to User

---

## OfferComment

A comment on an Offer (discussion between Sponsor and Developer).

| Attribute | Type   | Description                              |
|-----------|--------|------------------------------------------|
| offer     | Offer  | The Offer being discussed                |
| author    | User   | Who wrote it                             |
| content   | string | Comment text                             |

**Relationships:** belongs to Offer, belongs to User

---

## Media

An image or video attached to an Issue, typically contributed by a Communicator as a marketing or communication strategy.

| Attribute | Type    | Description                                |
|-----------|---------|--------------------------------------------|
| issue     | Issue   | The Issue this media belongs to            |
| title     | string  | Media title                                |
| content   | string? | Description                                |
| url       | string  | Media URL                                  |
| type      | enum    | url (image), vid (video)                   |
| createdBy | User    | The Communicator who uploaded it             |
| karma     | integer | Community score                            |
| deleted   | boolean | Soft-delete flag                           |

**Relationships:** belongs to Issue, belongs to User (Communicator)

---

## TechSolution

A textual proposal written by an Advisor explaining how an Issue could be addressed. Functions as a knowledge-base article and can be voted on by the community.

| Attribute | Type    | Description                              |
|-----------|---------|------------------------------------------|
| issue     | Issue   | The Issue this proposal addresses        |
| title     | string  | Proposal title                           |
| content   | string  | Detailed proposal                        |
| createdBy | User    | The Advisor who wrote it                 |
| karma     | integer | Community vote score                     |
| language  | string? | Content language code                    |
| points    | integer | Reputation points                        |
| deleted   | boolean | Soft-delete flag                         |

**Relationships:** belongs to Issue, belongs to User (Advisor), has many TechSolutionComment

---

## Watch

A subscription to notifications about an Issue or Project.

| Attribute | Type   | Description                              |
|-----------|--------|------------------------------------------|
| user      | User   | The subscriber                           |
| entity    | enum   | issue, project                           |
| entityId  | ID     | The watched entity's ID                  |
| reason    | string?| Why the user is watching                 |

**Relationships:** belongs to User

---

## Tag

A simple text tag on a Project.

| Attribute | Type    | Description                              |
|-----------|---------|------------------------------------------|
| name      | string  | Tag text                                 |
| objtype   | string  | Object type being tagged (project, issue, …) |
| objid     | ID      | ID of the tagged object                  |

**Relationships:** belongs to Project (or other taggable entity)
> ⚠️ Tag will be removed in order to use just MultilingualTag instead

---

## MultilingualTag

A Wikidata-backed semantic tag with automatic multilingual translations. Can be applied to both Issues and Projects.

| Attribute   | Type    | Description                              |
|-------------|---------|------------------------------------------|
| qid         | string  | Wikidata Q-identifier (e.g., Q9143)      |
| slug        | string  | URL-friendly identifier                  |
| title       | string  | Default display title                    |
| description | string? | Tag description                          |

**Relationships:** has many Issue (many-to-many), has many Project (many-to-many), has many MultilingualTagTranslated

---

## MultilingualTagTranslated

A translation of a MultilingualTag in a specific language.

| Attribute | Type   | Description                              |
|-----------|--------|------------------------------------------|
| tag       | MultilingualTag | Parent tag                      |
| language  | string | Language code                            |
| label     | string | Translated label                         |
| description | string? | Translated description               |

---

## Rates

Current currency exchange rates used for payment calculations.

| Attribute      | Type   | Description                              |
|----------------|--------|------------------------------------------|
| blockchainData | object | Bitcoin exchange rates (BTC ↔ USD/BRL)   |
| oerData        | object | Fiat exchange rates (USD ↔ BRL)          |

---

## Value Objects

### IssueFilter

Criteria for searching/filtering Issues.

| Attribute   | Type      | Description                              |
|-------------|-----------|------------------------------------------|
| projectId   | ID?       | Filter by Project                        |
| projectName | string?   | Filter by Project name                   |
| searchTerms | string?   | Full-text search                         |
| isSponsored | boolean?  | Only sponsored Issues                    |
| sortBy      | enum?     | Sorting field                            |
| ascending   | boolean?  | Sort direction                           |
| tags        | string[]? | Filter by tags                           |
| language    | string?   | Filter by content language               |
| noProposals | boolean?  | Issues without TechSolutions             |
| hasSponsors | boolean?  | Issues with active Offers                |
| isPrivate   | boolean?  | Filter by privacy status                 |

### OfferTerms

Terms for creating or editing an Offer.

| Attribute          | Type      | Description                              |
|--------------------|-----------|------------------------------------------|
| price              | decimal   | Pledge amount                            |
| currency           | enum      | USD, BRL, BTC                            |
| acceptanceCriteria | string?   | What must be true for payment            |
| expirationDate     | datetime? | When the offer expires                   |
| noForking          | boolean?  | Prefer no forking                        |
| requireRelease     | boolean?  | Require inclusion in release             |

### VoteAction

| Value  | Description           |
|--------|-----------------------|
| up     | Upvote                |
| down   | Downvote              |
| cancel | Cancel existing vote  |

### Currency

| Value | Description       |
|-------|-------------------|
| USD   | US Dollar         |
| BRL   | Brazilian Real    |
| BTC   | Bitcoin           |

### PaymentConfirm

| Attribute       | Type     | Description                              |
|-----------------|----------|------------------------------------------|
| payKey          | string?  | PayPal payment key                       |
| transactionHash | string?  | Bitcoin transaction hash                 |
| amountReceived  | decimal? | Actual amount received                   |
