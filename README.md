# Family Finance

A personal family finance management application for tracking shared finances,
transactions, accounts, workspaces, and debts between family members.

The project is currently under active development.

## Features

### Workspaces
- Create and manage family/group workspaces
- Add and manage workspace members
- Separate financial activity by workspace

### Accounts
- Bank accounts
- Cash accounts
- Crypto accounts
- Multiple currencies

### Transactions
- Expenses
- Direct transfers
- Shared payments
- Operation-based transaction grouping
- Soft deletion and restoration
- Transaction history

### Debts
- Overall personal debt position
- Debt breakdown by person
- Debt breakdown by workspace
- Multi-currency debt tracking
- Debt compensation through direct transfers
- Simplified debt settlements
- Settlement snapshots

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

### Frontend
- HTML
- CSS
- Vanilla JavaScript

No frontend framework is currently used.

## Project Structure

```text
fam_fin_project/
│
├── backend/
│   ├── api/
│   │   └── routes/
│   │       ├── accounts.py
│   │       ├── transactions.py
│   │       ├── users.py
│   │       └── workspaces.py
│   │
│   ├── models/
│   │   ├── account.py
│   │   ├── base.py
│   │   ├── notification.py
│   │   ├── settlement.py
│   │   ├── transaction.py
│   │   ├── user.py
│   │   ├── workspace.py
│   │   └── workspace_member.py
│   │
│   ├── services/
│   │   ├── account_services.py
│   │   ├── db_services.py
│   │   ├── transaction_services.py
│   │   ├── user_services.py
│   │   ├── workspace_member_services.py
│   │   └── workspace_services.py
│   │
│   ├── shared/
│   │   ├── currency.py
│   │   └── helpers.py
│   │
│   ├── database.py
│   ├── main.py
│   ├── seed.py
│   └── test.py
│
├── frontend/
│   ├── css/
│   │   └── style.css
│   │
│   ├── html/
│   │   ├── account.html
│   │   ├── debts.html
│   │   ├── index.html
│   │   ├── members.html
│   │   ├── settings.html
│   │   ├── transactions.html
│   │   └── workspace.html
│   │
│   └── js/
│       ├── account.js
│       ├── accounts.js
│       ├── app-shell.js
│       ├── config.js
│       ├── debt.js
│       ├── index.js
│       ├── members.js
│       ├── transaction-api.js
│       ├── transaction-form.js
│       ├── transaction-render.js
│       ├── transaction-state.js
│       ├── transaction.js
│       └── workspace.js
│
├── docs/
│   ├── ideas/
│   │   ├── features.md
│   │   ├── roadmap.md
│   │   └── vision.md
│   │
│   └── structure/
│       ├── databases.md
│       └── entities.md
│
├── docker/
│
├── .vscode/
├── .gitignore
└── README.md