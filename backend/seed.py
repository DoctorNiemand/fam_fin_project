from datetime import datetime

from database import Session

from models.user import User, Role
from models.account import Account, AccountType
from models.workspace import Workspace
from models.workspace_member import WorkspaceMember, Permission
from models.transaction import Transaction, TransactionType
from models.settlement import Settlement, SettlementItem

from shared.currency import Currency


session = Session()
now = datetime.now()


# ============================================================
# USERS
# ============================================================

sers = User(
    name="Sers",
    login="sers",
    password_hash="1234",
    created_at=now,
    role=Role.ADMIN
)

dad = User(
    name="Dad",
    login="dad",
    password_hash="1234",
    created_at=now,
    role=Role.USER
)

anya = User(
    name="Anya",
    login="anya",
    password_hash="1234",
    created_at=now,
    role=Role.USER
)

andrea = User(
    name="Andrea",
    login="andrea",
    password_hash="1234",
    created_at=now,
    role=Role.USER
)

mom = User(
    name="Mom",
    login="mom",
    password_hash="1234",
    created_at=now,
    role=Role.USER
)

session.add_all([
    sers,
    dad,
    anya,
    andrea,
    mom
])

session.flush()


# ============================================================
# ACCOUNTS
# ============================================================

sers_bank = Account(
    name="Sers Bank",
    acc_type=AccountType.BANK,
    currency=Currency.EUR,
    owner_id=sers.id,
    created_at=now,
    active=True
)

sers_cash = Account(
    name="Sers Cash",
    acc_type=AccountType.CASH,
    currency=Currency.USD,
    owner_id=sers.id,
    created_at=now,
    active=True
)

dad_bank = Account(
    name="Dad Bank",
    acc_type=AccountType.BANK,
    currency=Currency.EUR,
    owner_id=dad.id,
    created_at=now,
    active=True
)

anya_bank = Account(
    name="Anya Bank",
    acc_type=AccountType.BANK,
    currency=Currency.EUR,
    owner_id=anya.id,
    created_at=now,
    active=True
)

mom_bank = Account(
    name="Mom Bank",
    acc_type=AccountType.BANK,
    currency=Currency.EUR,
    owner_id=mom.id,
    created_at=now,
    active=True
)

session.add_all([
    sers_bank,
    sers_cash,
    dad_bank,
    anya_bank,
    mom_bank
])

session.flush()


# ============================================================
# WORKSPACES
# ============================================================

us_trip = Workspace(
    name="US Trip",
    description="Snowboard trip to the US in February 2027",
    created_at=now,
    active=True
)

italy_trip = Workspace(
    name="Italy Trip",
    description="Family trip to Italy in 2027",
    created_at=now,
    active=True
)

money_transfer = Workspace(
    name="Money Transfer",
    description="Money transfers between Sers and Dad",
    created_at=now,
    active=True
)

session.add_all([
    us_trip,
    italy_trip,
    money_transfer
])

session.flush()


# ============================================================
# WORKSPACE MEMBERS
# ============================================================

# ---------- US TRIP ----------

sers_us = WorkspaceMember(
    user_id=sers.id,
    workspace_id=us_trip.id,
    permission=Permission.ADMIN,
    active=True
)

anya_us = WorkspaceMember(
    user_id=anya.id,
    workspace_id=us_trip.id,
    permission=Permission.ADMIN,
    active=True
)

dad_us = WorkspaceMember(
    user_id=dad.id,
    workspace_id=us_trip.id,
    permission=Permission.READ,
    active=True
)


# ---------- ITALY TRIP ----------

sers_italy = WorkspaceMember(
    user_id=sers.id,
    workspace_id=italy_trip.id,
    permission=Permission.ADMIN,
    active=True
)

mom_italy = WorkspaceMember(
    user_id=mom.id,
    workspace_id=italy_trip.id,
    permission=Permission.READ,
    active=True
)

dad_italy = WorkspaceMember(
    user_id=dad.id,
    workspace_id=italy_trip.id,
    permission=Permission.READ,
    active=True
)

anya_italy = WorkspaceMember(
    user_id=anya.id,
    workspace_id=italy_trip.id,
    permission=Permission.READ,
    active=True
)


# ---------- MONEY TRANSFER ----------

sers_transfer = WorkspaceMember(
    user_id=sers.id,
    workspace_id=money_transfer.id,
    permission=Permission.ADMIN,
    active=True
)

dad_transfer = WorkspaceMember(
    user_id=dad.id,
    workspace_id=money_transfer.id,
    permission=Permission.READ,
    active=True
)


session.add_all([
    sers_us,
    anya_us,
    dad_us,

    sers_italy,
    mom_italy,
    dad_italy,
    anya_italy,

    sers_transfer,
    dad_transfer
])

session.flush()


# ============================================================
# TRANSACTIONS
# ============================================================

# ------------------------------------------------------------
# US TRIP
# ------------------------------------------------------------

# Sers pays 300 EUR for Dad and Anya.
# 150 EUR each.
#
# Debt state:
#   Dad  +150
#   Anya +150
#   Sers -300
#

us_1 = Transaction(
    amount=150,
    description="Snowboard equipment - Dad",
    transact_type=TransactionType.SHARED_PAYMENT,
    workspace_id=us_trip.id,
    currency=Currency.EUR,
    beneficiary_workspace_member=dad_us.id,
    source_workspace_member=sers_us.id,
    beneficiary_acc=None,
    source_acc=sers_bank.id,
    operation_id=None,
    data_source="seed",
    deleted_by=None,
    deleted_at=None,
    created_at=now
)

us_2 = Transaction(
    amount=150,
    description="Snowboard equipment - Anya",
    transact_type=TransactionType.SHARED_PAYMENT,
    workspace_id=us_trip.id,
    currency=Currency.EUR,
    beneficiary_workspace_member=anya_us.id,
    source_workspace_member=sers_us.id,
    beneficiary_acc=None,
    source_acc=sers_bank.id,
    operation_id=None,
    data_source="seed",
    deleted_by=None,
    deleted_at=None,
    created_at=now
)

# Anya pays 120 EUR to Dad.
#
# Final:
#   Dad  +270
#   Anya +30
#   Sers -300
#

us_3 = Transaction(
    amount=120,
    description="Hotel booking",
    transact_type=TransactionType.DIRECT_TRANSFER,
    workspace_id=us_trip.id,
    currency=Currency.EUR,
    beneficiary_workspace_member=dad_us.id,
    source_workspace_member=anya_us.id,
    beneficiary_acc=None,
    source_acc=anya_bank.id,
    operation_id=None,
    data_source="seed",
    deleted_by=None,
    deleted_at=None,
    created_at=now
)


# ------------------------------------------------------------
# ITALY TRIP
# ------------------------------------------------------------

# Sers pays 200 EUR:
#   Mom  = 100
#   Dad  = 50
#   Anya = 50
#
# Then Mom pays Dad 80 EUR.
#
# Final:
#   Dad  +130
#   Anya +50
#   Mom  +20
#   Sers -200
#

italy_1 = Transaction(
    amount=100,
    description="Dinner - Mom",
    transact_type=TransactionType.SHARED_PAYMENT,
    workspace_id=italy_trip.id,
    currency=Currency.EUR,
    beneficiary_workspace_member=mom_italy.id,
    source_workspace_member=sers_italy.id,
    beneficiary_acc=None,
    source_acc=sers_bank.id,
    operation_id=None,
    data_source="seed",
    deleted_by=None,
    deleted_at=None,
    created_at=now
)

italy_2 = Transaction(
    amount=50,
    description="Dinner - Dad",
    transact_type=TransactionType.SHARED_PAYMENT,
    workspace_id=italy_trip.id,
    currency=Currency.EUR,
    beneficiary_workspace_member=dad_italy.id,
    source_workspace_member=sers_italy.id,
    beneficiary_acc=None,
    source_acc=sers_bank.id,
    operation_id=None,
    data_source="seed",
    deleted_by=None,
    deleted_at=None,
    created_at=now
)

italy_3 = Transaction(
    amount=50,
    description="Dinner - Anya",
    transact_type=TransactionType.SHARED_PAYMENT,
    workspace_id=italy_trip.id,
    currency=Currency.EUR,
    beneficiary_workspace_member=anya_italy.id,
    source_workspace_member=sers_italy.id,
    beneficiary_acc=None,
    source_acc=sers_bank.id,
    operation_id=None,
    data_source="seed",
    deleted_by=None,
    deleted_at=None,
    created_at=now
)

italy_4 = Transaction(
    amount=80,
    description="Train tickets",
    transact_type=TransactionType.DIRECT_TRANSFER,
    workspace_id=italy_trip.id,
    currency=Currency.EUR,
    beneficiary_workspace_member=dad_italy.id,
    source_workspace_member=mom_italy.id,
    beneficiary_acc=None,
    source_acc=mom_bank.id,
    operation_id=None,
    data_source="seed",
    deleted_by=None,
    deleted_at=None,
    created_at=now
)


# ------------------------------------------------------------
# MONEY TRANSFER
# ------------------------------------------------------------

# Dad -> Sers: 500 EUR
# Sers -> Dad: 150 EUR
#
# Final:
#   Sers +350
#   Dad  -350
#

transfer_1 = Transaction(
    amount=500,
    description="Money transfer",
    transact_type=TransactionType.DIRECT_TRANSFER,
    workspace_id=money_transfer.id,
    currency=Currency.EUR,
    beneficiary_workspace_member=sers_transfer.id,
    source_workspace_member=dad_transfer.id,
    beneficiary_acc=None,
    source_acc=dad_bank.id,
    operation_id=None,
    data_source="seed",
    deleted_by=None,
    deleted_at=None,
    created_at=now
)

transfer_2 = Transaction(
    amount=150,
    description="Money transfer back",
    transact_type=TransactionType.DIRECT_TRANSFER,
    workspace_id=money_transfer.id,
    currency=Currency.EUR,
    beneficiary_workspace_member=dad_transfer.id,
    source_workspace_member=sers_transfer.id,
    beneficiary_acc=None,
    source_acc=sers_bank.id,
    operation_id=None,
    data_source="seed",
    deleted_by=None,
    deleted_at=None,
    created_at=now
)

session.add_all([
    us_1,
    us_2,
    us_3,

    italy_1,
    italy_2,
    italy_3,
    italy_4,

    transfer_1,
    transfer_2
])

session.flush()


# ============================================================
# SETTLEMENT SNAPSHOTS
# ============================================================

# ------------------------------------------------------------
# US TRIP
# ------------------------------------------------------------

us_settlement = Settlement(
    workspace_id=us_trip.id,
    created_at=now
)

session.add(us_settlement)
session.flush()

us_settlement_items = [
    SettlementItem(
        settlement_id=us_settlement.id,
        debtor_wsm_id=dad_us.id,
        creditor_wsm_id=sers_us.id,
        amount=270,
        currency=Currency.EUR,
        transaction_id=None
    ),

    SettlementItem(
        settlement_id=us_settlement.id,
        debtor_wsm_id=anya_us.id,
        creditor_wsm_id=sers_us.id,
        amount=30,
        currency=Currency.EUR,
        transaction_id=None
    )
]


# ------------------------------------------------------------
# ITALY TRIP
# ------------------------------------------------------------

italy_settlement = Settlement(
    workspace_id=italy_trip.id,
    created_at=now
)

session.add(italy_settlement)
session.flush()

italy_settlement_items = [
    SettlementItem(
        settlement_id=italy_settlement.id,
        debtor_wsm_id=dad_italy.id,
        creditor_wsm_id=sers_italy.id,
        amount=130,
        currency=Currency.EUR,
        transaction_id=None
    ),

    SettlementItem(
        settlement_id=italy_settlement.id,
        debtor_wsm_id=anya_italy.id,
        creditor_wsm_id=sers_italy.id,
        amount=50,
        currency=Currency.EUR,
        transaction_id=None
    ),

    SettlementItem(
        settlement_id=italy_settlement.id,
        debtor_wsm_id=mom_italy.id,
        creditor_wsm_id=sers_italy.id,
        amount=20,
        currency=Currency.EUR,
        transaction_id=None
    )
]


# ------------------------------------------------------------
# MONEY TRANSFER
# ------------------------------------------------------------

transfer_settlement = Settlement(
    workspace_id=money_transfer.id,
    created_at=now
)

session.add(transfer_settlement)
session.flush()

transfer_settlement_items = [
    SettlementItem(
        settlement_id=transfer_settlement.id,
        debtor_wsm_id=sers_transfer.id,
        creditor_wsm_id=dad_transfer.id,
        amount=350,
        currency=Currency.EUR,
        transaction_id=None
    )
]


session.add_all(
    us_settlement_items
    + italy_settlement_items
    + transfer_settlement_items
)


# ============================================================
# COMMIT
# ============================================================

session.commit()
session.close()

print("Database seeded successfully.")