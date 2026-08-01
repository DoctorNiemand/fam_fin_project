# Database Schema

## Users

**One row represents one person using the app.**

| Column | Notes |
|--------|-------|
| id | immutable |
| created_at | immutable |
| name | |
| login | |
| password_hash | |
| role | |

---

## Workspaces

**One row represents one shared financial area.**

| Column | Notes |
|--------|-------|
| id | immutable |
| created_at | immutable |
| name | |
| description | |

---

## Workspace Members

**One row represents one user's participation in one workspace.**

| Column | Notes |
|--------|-------|
| id | immutable |
| workspace_id | immutable |
| user_id | immutable |
| permission | must somehow be synced with members table so than no interchange may happen when something gets deleted or whatever |

---

## Transactions

**One row represents one financial event.**

| Column | Notes |
|--------|-------|
| id | immutable |
| workspace_id | immutable |
| created_at | immutable |
| deleted_by | |
| deleted_at | |
| description | |
| amount | |
| currency | |
| benefeciary_acc | |
| source_acc | |
| beneficiary_workspace_member | |
| source_workspace_member | |
| source | api / csv / manual |

---

## Accounts

**One row represents one financial account.**

| Column | Notes |
|--------|-------|
| id | immutable |
| owner_id | immutable |
| name | |
| type | |
| currency | |

<!--
I have a little struggle to create a proper structure in terms of what shall be a database and what just a table, what just a table entry. So it seemed like "users" will be a database. One entry is user with tables: name, login, password, id, role. Then a user has accounts. And here I seem to struggle. So "accounts" sounds like another database tbh. But still a user has to know all accounts it has, so basically we also gonna have both: accounts table in user db (where we gonna store the ids of the accs the user has), and accounts database with all accounts and their details? But then e.g. we seem to have a redundancy: we wanna store all the accounts for the user, and we wanna store the account owner for an account entry in accounts database? It looks like then we dont wanna store the accounts in user db, but somehow access for the accounts like for "Account in Accounts with Account.owner == this_user.id do smth"?

Also a little struggle is how do we store some pure log info. So basically we shall never delete any transactions/account states and so on. From this information we can provide full log for each account and for all the transactions inside e.g. a workspace. It can be done in a uniform way, by just letting "sweep" over transaction details of transactions with some given properties (e.g. inside one workspace or with some beneficiary account or whatever). But how do we get some complete info about the e.g. workspace then? Like when created, by whom...

Also how do we handle the stuff which only has like 1 entry? Whole column for it? Or how's it normally done?

balance seemed redundant
-->