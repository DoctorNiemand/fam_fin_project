# Roadmap

## v0.1 - Working MVP

Goal:
A working application that replaces my notes/Excel for syncing finances with my dad.

Features:

- User login
- User registration (or manual user creation)
- Workspaces
- Workspace members
- Accounts
- Transactions
- Automatic debt calculation
- Audit log
- Responsive UI
- SQLite database

Implementation notes:

- Date format for created_at
- currencies/roles/permissions must be enumerations
- login unique
- immutability of e.g. created_at
- sender may not know where he sends the money, b

No:

- CSV import
- Notifications
- Investments
- Planner
- Attachments
- Charts

Success criterion

I can completely replace my current note-taking workflow.


## v0.2

- CSV import
- Duplicate detection
- Search
- Better transaction editing


## v0.3

- Notifications
- Planner
- Better permissions