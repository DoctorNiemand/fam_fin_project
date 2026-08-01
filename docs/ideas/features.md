# Features

## Must have

### 1. Being able to sync my and dad's finances

This is **THE** most challenging task to solve without some dedicated stuff.

#### Realization

- Adding areas with shared access, so that e.g. me and dad can both add transactions there and see them, but e.g. sister cannot.
- Crypto purchase shall be done as an event. Then I automatically get some debt to my dad for the given amount. I enter the sum in rubles and what I got as USDT / USDT price / EUR price / whatever else.
- Whenever adding some expense, I need to be able to choose that it was spent for dad's needs. Also if it's added via `.csv`, I need to be able to kinda "mark" it as an expense for dad.
- Add a eur/usdc price tracker? 
- Ownership: who owns money after operation / who benefits from it
- Currency:Original currency, Exchange rate, Converted value
---

### 2. Transactions / operations

Without this, making the syncing basically won't work.

#### Realization

- I see a first trouble here. E.g. I add a transaction manually at some point.
- Anyway, must have a minimal design, so that it kinda takes 5 sec to add a new transaction. Otherwise it won't be used at all after a while.
- Must be phone-friendly too.
- History of changes: who created, when. Who changed, when.
- Which workspace the transaction refers to?
- Source: API/CSV/Manual
- Categoies, better hierarchy. like Food -> restaurant and food -> grocery store
- Account it refers to: bybit/c24. i feel like each user shall add own accounts here, as this stuff is rlly personal


#### Bottleneck

- Then we add stuff through `.csv` export, but there will be my transactions too. How do I make sure nothing is included twice then? So doubled transactions.

#### Don't do's
- Making a lot of steps for selection of smth. No more than 5 actual clicks to add transaction
- Not 10 fields to fill in

---

### 3. Adding transactions from the phone must be extremely easy

#### Realization

- Website?
- App?
- Can we make a website, but "install it as an app", so kinda a shortcut for the website as an icon?

#### Bottleneck

- Never ever worked with mobile websites.
- Also an app would be cooler, but this sounds insane lol.

---

### 4. Authentification

Logging in and stuff

#### Realization

- Creating a profile
- Changing password
- Permissions: Workspace ownership, Workspace creation, transaction adding/deleting/modifying


### 4. Backups

Self explaining

#### Realization
- periodical auto saving of the current system's state

#### Bottleneck
- no idea how to and even where.

---

## Should have

### 1. Monthly financial planner / project financial planner

May be created as one entity, but month / some project shall be distinguishable ofc.

#### Realization

- Project name
- Budget
- Positions

Example:

- Name: `08/26`
- Budget: `1800`
- Positions:
  - Fun and friends
  - Saving
  - Food
  - Apartment costs

#### Bottleneck

- Making month just as a project sounds like a ghetto solution lol.
- But making two planners, one for month and one for project, is also expanding the app unnecessarily + making it less intuitive to navigate, so bullshit too.

---

### 2. Trip planner / organizer

So basically a Splitwise for family.

#### Realization

Literally like Splitwise:

- Project name
- What
- What's the price
- Who paid
- Who owes what share

---

### 3. Search in transactions

#### Realization

- Filter by category
- Filter by name
- ...

#### Bottleneck

- No idea how to implement search on a website tbh.
- Also what do we need to be able to search for?
- I do not want a user to be obliged to add keywords or whatever lol.

---

### 4. `.csv` upload from bank

#### Realization

- Bank allows to pull the info as a `.csv` file.
- We may extract info + reformat it to some my custom stuff.
- Be able to choose it was spent for someone else.

#### Bottleneck

- Is discussed already: how do we avoid doubling some manually added transactions with the ones from the `.csv`?

---

## Nice to have

### 1. Visualization of allat stuff in some nice way

#### Realization

- Idk tbh.
- I only worked with Grafana previously.
- But you needa log in there separately and it is like really a whole other site lol.

---

### 2. Family stonks

#### Realization

- Public portfolio on Intelinvest.

#### Bottleneck

- No idea how to pull any data from there.



### 3. Notifications

#### Realization

- like a bell/mailbox icon as it is on many websites. when a new transaction in some workspaces a user owns/is a part of is added/changed/deleted, the user gets a notification

#### Bottleneck

- how to mark them as read unread properly, and how to design it at all tbh

### 4. Recurring transactions

#### Realization

- Recognition from .csv and so on?
- 

#### Bottleneck

- how to mark them as read unread properly, and how to design it at all tbh


