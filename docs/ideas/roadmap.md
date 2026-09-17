\# Finance Platform Roadmap

\## Vision

A simple family finance platform for synchronizing finances across users,

workspaces, accounts, and currencies.

The primary goal is to replace manual notes / Excel-based tracking with a

system that makes recording financial operations extremely fast and makes

debts and financial state easy to understand.

The application should be usable from a phone and should require only a few

steps to record a transaction.

\---

\# v0.1 — Working MVP

## Current MVP direction

The MVP is focused on replacing the current notes / Excel workflow:
managing workspaces and accounts, recording financial operations quickly,
and—most importantly—correctly calculating and presenting who owes whom.

Settings, automation, CSV import, bank synchronization, charts, notifications,
and other secondary functionality should not delay v0.1.

**\*\*Goal:\*\***

*> I can completely replace my current note-taking workflow for syncing*

*> finances with my family.*

\## Users & Authentication

\- [ ] Login

\- [ ] Proper session/token-based authentication

\- [ ] User creation / registration

\- [ ] Password handling

\- [ ] Current user derived from authentication rather than request parameters

\---

\## Workspaces

\- [x] Create workspace

\- [x] List workspace members

\- [x] Add members

\- [x] Remove members

\- [x] Workspace member permissions

\- [ ] Clean frontend permission handling

\- [ ] Workspace ownership handling

Workspaces provide the shared areas in which users can synchronize

finances while keeping other family members out of unrelated data.

\---

\## Accounts

Each user owns their own accounts.

Examples:

\- Bank account

\- Credit card

\- Cash

\- Crypto exchange account

\- Other personal financial accounts

\### MVP

\- [x] Create account

\- [x] List accounts

\- [x] Edit account

\- [x] View account transactions

\- [x] Attach accounts to transactions

\- [x] Backend account value calculation
- [ ] Show account balances in the frontend
- [ ] Clean account management UI
- [ ] Add account action directly from the sidebar

\---

\# Transactions

Transactions are the central entity of the application.

\## Transaction creation

\- [x] Expense

\- [x] Direct transfer

\- [x] Shared payment

\- [x] Workspace selection

\- [x] Workspace-member selection

\- [x] Optional source account

\- [x] Optional beneficiary account

\- [x] Shared-payment recipients

\- [x] Shared-payment shares

\- [ ] Expense / transfer UI terminology cleanup

\- [ ] Optimize creation flow for 3–5 clicks

\### Transaction participants

The transaction model should be able to represent:

\- who paid

\- who received / benefited

\- which account was involved

This means an expense paid by one user for another user's needs can already

be represented by the current transaction model.

The current \`expense\` / \`direct\_transfer\` terminology is temporary and will

be cleaned up later.

\---

\## Financial operation / transaction grouping

A real-world financial operation may produce multiple underlying financial
effects. The system should distinguish the logical operation from its
individual accounting effects.

Introduce a stable **operation / transaction-group identifier** above the
individual financial effects.

Example:

```text
Operation #123

Dad pays restaurant: €100

Dad's share:     €50
Sergei's share:  €50
```

The operation represents one real-world event; the underlying financial
effects are what account and debt calculations use.

### MVP

- [ ] Define the operation / transaction-group entity
- [ ] Define its identifier and relationship to transactions/effects
- [ ] Define which fields belong to the operation
- [ ] Define which fields belong to individual financial effects
- [ ] Keep historical operations understandable and stable

---

## Debt / Rebalancing

Debt calculation is one of the core reasons for the application.

## Workspace debt

- [ ] Workspace debt overview
- [ ] Show who owes whom
- [ ] Correctly account for expenses where one user pays for another
- [ ] Correctly account for shared-payment shares
- [ ] Correctly account for direct transfers
- [ ] Derive debt from explicit financial effects

## Debt rebalancing / netting

The system should combine opposing debts between the same users.

Example:

```text
Dad owes Sergei €120
Sergei owes Dad  €35

----------------------

Net:
Dad owes Sergei €85
```

- [ ] Define debt direction semantics
- [ ] Calculate pairwise balances
- [ ] Net opposing debts
- [ ] Return a clean "who owes whom" representation
- [ ] Ensure rebalancing does not modify historical transactions
- [ ] Keep historical operations immutable while calculating current debt

Rebalancing is a calculated view of the underlying financial history, not a
destructive rewrite of transactions.

## Global debt

- [ ] Global debt overview across workspaces
- [ ] Aggregate debts between users
- [ ] Define how debts from multiple workspaces are combined
- [ ] Net opposing debts globally

---

# Frontend / UX

The application should be designed around extremely fast transaction entry.

\## MVP requirements

\- [ ] Responsive layout

\- [ ] Phone-friendly transaction creation

\- [ ] 3–5 clicks where realistically possible

\- [ ] No unnecessary fields

\- [ ] Clear transaction type selection

\- [ ] Clean member/account selection

\- [ ] Proper validation feedback

\- [ ] Date formatting

\- [ ] Consistent terminology

The application should ideally work as a mobile-friendly web app / PWA

rather than requiring a native mobile application.

\---

\# Reliability

\- [ ] SQLite database

\- [ ] Automatic periodic database backups

\- [ ] Basic error handling

\- [ ] Validation of all important inputs

\- [ ] Unique user login

\- [ ] Immutable fields where appropriate

\- [ ] Transactional database operations / rollback handling

\---

\## Explicitly NOT v0.1

The following should not delay the first usable version:

\- CSV import

\- Automatic bank synchronization

\- Notifications

\- Financial planner

\- Investment tracking

\- Charts / advanced visualization

\- Recurring transactions

\- Native mobile application

\- Advanced transaction categorization

\- Crypto-specific transaction events

\- Automatic exchange-rate retrieval
- Settings page

\---

\# v0.2 — Automation & Multi-Currency

**\*\*Goal:\*\***

*> Reduce the amount of manual work required to maintain the financial data.*

\## CSV

\- [ ] CSV upload

\- [ ] Bank-specific CSV parsing

\- [ ] Transaction normalization

\- [ ] Duplicate detection

\- [ ] Matching imported transactions with existing manual transactions

\- [ ] Mark imported transactions as belonging to / benefiting another user

\- [ ] Transaction source tracking

\---

\## Multi-currency

\- [ ] Base currency

\- [ ] Received currency

\- [ ] Exchange rate

\- [ ] Dynamic calculation between the three

\- [ ] Currency conversion handling

\- [ ] EUR / USDC or other relevant price tracking if still useful

\---

\## Crypto

\- [ ] Crypto purchase event

\- [ ] Record amount paid in original currency

\- [ ] Record crypto amount received

\- [ ] Record relevant exchange rate / price

\- [ ] Automatically derive resulting family debt where applicable

\---

\## Transactions

\- [ ] Search transactions

\- [ ] Filter by category

\- [ ] Filter by user

\- [ ] Filter by account

\- [ ] Filter by source

\- [ ] Better transaction editing

\- [ ] Better transaction categorization

\---

\# v0.3 — Collaboration & Planning

**\*\*Goal:\*\***

*> Expand the application from a finance-sync tool into a broader family*

*> finance platform.*

\## Notifications

\- [ ] New transaction notifications

\- [ ] Transaction changed notifications

\- [ ] Transaction deleted/restored notifications

\- [ ] Read/unread state

\---

\## Financial planner

\- [ ] Monthly financial planner

\- [ ] Project-based planner

\- [ ] Budget

\- [ ] Financial positions/categories

\- [ ] Distinguish months from projects without unnecessarily duplicating

  the underlying concept

\---

\## Recurring transactions

\- [ ] Recurring transaction definition

\- [ ] Automatic generation

\- [ ] CSV recognition where useful

\---

\## Permissions

\- [ ] More granular workspace permissions

\- [ ] More granular transaction permissions

\- [ ] Better administration UI

\---

\## Audit

\- [ ] User-facing transaction history

\- [ ] Detailed change history

\---

\# Later / Experimental

\## Trips / Group Expenses

Workspaces already provide much of the functionality required for trips.

If that proves insufficient:

\- [ ] Trip-specific UI

\- [ ] Expense grouping

\- [ ] Trip totals

\- [ ] Settlement functionality

\---

\## Investments

\- [ ] Family investment overview

\- [ ] Public portfolio integration

\- [ ] Investment value tracking

\- [ ] Historical performance

\---

\## Visualization

\- [ ] Financial dashboards

\- [ ] Spending breakdowns

\- [ ] Debt visualization

\- [ ] Currency exposure

\- [ ] Investment visualization

\---

\## External integrations

\- [ ] Bank APIs

\- [ ] Automatic transaction synchronization

\- [ ] Crypto exchange APIs

\- [ ] Automatic exchange-rate APIs

\---

\# Current Implementation Status

The following foundation is already working and should not be treated as
future work unless it needs cleanup:

- Global application shell and navigation
- Workspace switching and workspace/member pages
- Transaction pages and transaction lists
- Dashboard and recent transactions
- Basic workspace debt display
- Expense, direct-transfer, and shared-payment creation
- Soft deletion and restoration
- Account CRUD backend
- Account transaction retrieval
- Backend account value calculation

The next major focus is the **financial operation + debt model**, not further
visual polishing of the shell.

---

# Recommended v0.1 Implementation Order

## 1. Finish small shell/account items

- [ ] Remove Settings from the sidebar
- [ ] Add `+ Add workspace`
- [ ] Add `+ Add account`
- [ ] Add `+ New transaction` to the transaction navigation area
- [ ] Build/clean Accounts frontend
- [ ] Display account balances

## 2. Design the financial model

- [ ] Define operation / transaction-group semantics
- [ ] Define financial effects
- [ ] Define participant responsibilities
- [ ] Define expense behavior
- [ ] Define shared-payment behavior
- [ ] Define transfer / settlement behavior
- [ ] Define debt direction

## 3. Implement the backend debt engine

- [ ] Generate debt effects
- [ ] Calculate pairwise balances
- [ ] Rebalance/net opposing debts
- [ ] Workspace debt endpoint
- [ ] Global debt endpoint

## 4. Connect the frontend to the real debt model

- [ ] Workspace "who owes whom"
- [ ] Global debt view
- [ ] Dashboard position
- [ ] Correct positive/negative semantics
- [ ] Settlement/rebalancing presentation

## 5. Clean transaction UX

- [ ] Terminology
- [ ] Validation
- [ ] 3–5 click flow
- [ ] Better account/member selection
- [ ] Delete/restore presentation
- [ ] Editing

## 6. Reliability and authentication

- [ ] Database transactions / rollback
- [ ] Input validation
- [ ] Backups
- [ ] Immutable fields
- [ ] Authentication

Only after these are sufficiently stable should v0.1 be considered complete.

---

# Design Principles

1\. **\*\*Fast transaction entry comes first.\*\***

2\. **\*\*Do not force users to enter information they don't need.\*\***

3\. \*\*A transaction should remain understandable without knowing the

   implementation behind it.\*\*

4\. **\*\*Workspaces provide the boundary for shared financial information.\*\***

5\. **\*\*Accounts belong to individual users, not workspaces.\*\***

6\. **\*\*The system must distinguish who paid from who benefited.\*\***

7\. \*\*Currency conversion should preserve the original financial information

   rather than replacing it with a single converted value.\*\*

8\. **\*\*Automation should reduce manual work, not make manual entry harder.\*\***

9\. **\*\*Mobile usability is a requirement, not a separate feature.\*\***

10\. \*\*Do not build features merely because they are technically interesting;

    prioritize the workflow of actually managing family finances.\*\*

\---

\# MVP Success Criterion

The MVP is successful when:

*> I can use the application instead of my current notes / Excel workflow to*

*> record our family financial operations, see who owes whom, and maintain*

*> the underlying accounts and transactions without having to manually*

*> calculate everything.*