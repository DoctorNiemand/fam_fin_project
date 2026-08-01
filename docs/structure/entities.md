# Entities

## User

Basically an app's user with given permissions.

Examples:
- Me
- Dad
- Sister
- Andrea

### Attributes

- id (int)
- Name (string)
- Login (string)
- Password (hashed) (string)
- Role (enum/set/whatever it must be: Admin / Member / ...) 
- Notifications (i guess this shall be another "notification" entity)
- Debt summary (merged from all accessible workspaces) (entity: debt)
<!-- - Permissions (idk how to realize them tbh)  seemed to be redundant. they are stored in every workspace_member for teh user-->


<!-- - Owned workspaces (entity: workspace)
- Joined workspaces (entity: workspace) -->

### Methods
- create(name, login, password) {id, role}
- calculate_debt(self) {}
- add_account(name, type, currency) = account->create(user, name, type, currency)
- change_name(new_name) {name}
- change_password(new_password) {password}


---


## Workspace

Basically any unit we wanna track finances for.

Examples:
- Family
- Dad
- Italy Trip
- August 2026
- Workshop

### Attributes

- id (int)
- Name (string)
- Description (string or whatever will fit there best, but i guess just string)
- Users included and their rights (entity: WorkspaceMember)
- Audit log (entity: auditlog)

### Methods

- create(name, description, users) {id, audit_log}
<!-- - add_transaction(source_acc, ben_acc, source_worksp_member, ben_worksp_member, amount_in, currency_in, amount_out, currency_out, description) is not rlly needed as the workspace doe not create transaction itself, but the transaction creates itself within the workspace -->
{transaction, audit_log}
- optimize_debts () <!-- splitwise-like stuff, slightly over the v1.0 -->
- add_member (user, permission) = workspacemember->create(user, permission, workspace)
- remove_member(workspace_member)
- change_permissions(workspace_member, new_permission)
- rename(new_name)
- change_description(new_descr)
---


## WorkspaceMember

Directly derived from both user entity and workspace entity. needed as neither of them fully depend on each other.

Examples:
- sis in Italy trip
- me in dad-me finances 

### Attributes
- User (enity: User)
- Workspace (enity: Worksapce)
- Debt (entity: debt, so yeah it looks like creating a class/entity debt totally makes sense)
- permissions (enum/set/whatever_the_right_wording: {"readonly", "can add", "can modify"})
- id (int)
<!-- - Probably: transactions_list (entity: transaction) -->

### Methods
- create(user, permission, workspace)
- change_permission(new_permission)

---


## Account

The place/object where the actual money is stored

Examples:
- Bybit
- C24

### Attributes
- Owner (enity: User)
- balance (float: just a number)
- name (string)
- Currency (enum/set/whatever: {"eur", "rub", "usd"})
- balance_planned (or anything like this, but this is surely beyond v0.1)
- Type (enum/set/whatever_the_right_wording: {"bank account", "crypto", "cash"})
- id (int)

### Methods

- create(user, name, currency, type, initial_balance) 
{id, balance}
- change_balance (signed_float: value) {balance}
- change_name (string: new_name) {name}
---


## Transaction

An event where money are deducted from some account or transferred between accounts.
Actually a challenge here is to decide what's relevant: the account the money's transfered from (e.g. relevant in case i buy crypto) or only the user wo paid (e.g. when sharing finances for the trip, it might be irrelevant where my sister paid from, AmExp or some other bank)

### Attributes

- Workspace (entity:workspace)
<!-- - Creator (entity: user) not needed as it has the log. same as for the workspace-->
- Source account (entity: account) 
- Beneficiary account (entity: account) 
- Source worksp memb (entity: WorkspaceMember) 
- Beneficiary worksp memb (entity: WorkspaceMember)
<!-- idk how to avoid redundancy here, as if we provide the acoounts, then users become redundant. but it is not always relevant to provide the exact accounts i'd say -->
- Amount (float)
- Currency (enum/set/whatever: {"eur", "rub", "usd"})
- multicurrency (bool -- just to ba eble to mae transactions like 500 eur -> 50k rub)
- Category (just a string i guess)
- Description (just a string i guess)
- Timestamp (date: some RTC value)
- Source (enum/set/whatever: Manual / CSV / API)
<!-- - Audit log (entity: auditlog) i'd say making transaction connected to an audit log is kinda wrong. better lets make audit log know over which transaction or over which workspace (2 types of audit logs here become needed) it works, and it will kinda dinamically access the relevant sources-->
- deleted_by (entity:user)
- deleted_at (date: some RTC value)
- Attachments (future) (idk yet)
- id (int)

### Methods
- Create (<!-- workspace is redundant as we can find out iether directly from source_worksp_member-->source_acc, ben_acc, source_worksp_member, ben_worksp_member, amount_in, currency_in, amount_out, currency_out, description) 
{id, timestamp, audit_log}
- Delete (workspace_member) {deleted_by, deleted_at, audit_log}
- Restore (workspace_member) {deleted_by, deleted_at, audit_log}
- modify(something)
- To be defined.

---




## Debt

Needed to provide the user the final info about who lends them/whom they owe

Examples:
- Dad's debt in Italy trip
- My overall debt in all of my workspaces

### Attributes
- Debtor (entity: user)
- Creditor (entity: user)
- Workspace(or workspaces as we wanna also tell the user how much he owes overall) (entity: workspace)
- Amount (float)
- Reason (optional tbh, as i think debt must be at least workspace-level for each user -> many transactions -> reasion is kinda irrelevant)
- id (int)

### Methods

- To be defined.

---


## AuditEntry

Log of some actions over another entity (-ies)

Examples:
- Audit of all transactions for a workspace
- Audit for one transaction

### Attributes
- user (entity: user)
- action (set/enum/whats the right name for it: {"add", "modify", "delete"})
- old_data (something: may be description/beneficiary/value)
- new_data (something: may be description/beneficiary/value)
- timestamp (date: some RTC value)
- target (entity: transaction/user/workspace)
- id (int)

### Methods

- create(user, action, target) 
{id, old_data, timestamp}
- 

---









## Notification

Notification of some event (add/change/delete)

Examples:
- Transaction added in Italy trip
- Price for a snowboard changed in system

### Attributes
- User (enity: User)
- Workspace (enity: Worksapce)
- text (string)
- seen (bool)
- id (int)
- ref_id (int)

### Methods
- create
- mark_seen()