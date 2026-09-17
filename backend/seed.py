from datetime import datetime

from database import Session
from models.user import User, Role
from models.workspace import Workspace
from models.workspace_member import WorkspaceMember, Permission

import services.transaction_services as serv_tr

session = Session()


# =========================
# USERS
# =========================

sers = User(
    name="Sers",
    login="sers",
    password_hash="1234",
    role=Role.ADMIN,
    created_at=datetime.now()
)

dad = User(
    name="Dad",
    login="dad",
    password_hash="1234",
    role=Role.USER,
    created_at=datetime.now()
)

anya = User(
    name="Anya",
    login="anya",
    password_hash="1234",
    role=Role.USER,
    created_at=datetime.now()
)

andrea = User(
    name="Andrea",
    login="andrea",
    password_hash="1234",
    role=Role.USER,
    created_at=datetime.now()
)

mom = User(
    name="Mom",
    login="mom",
    password_hash="1234",
    role=Role.USER,
    created_at=datetime.now()
)

session.add_all([sers, dad, anya, andrea, mom])
session.flush()


# =========================
# WORKSPACES
# =========================

us_trip = Workspace(
    name="US Trip",
    description="Snowboard trip to the US in February 2027",
    created_at=datetime.now()
)

italy_trip = Workspace(
    name="Italy Trip",
    description="Family trip to Italy in 2027",
    created_at=datetime.now()
)

money_transfer = Workspace(
    name="Money Transfer",
    description="Money transfers between Sers and Dad",
    created_at=datetime.now()
)

session.add_all([us_trip, italy_trip, money_transfer])
session.flush()


# =========================
# US TRIP
# Sers ADMIN
# Anya ADMIN
# Dad READ
# =========================

sers_us = WorkspaceMember(
    user_id=sers.id,
    workspace_id=us_trip.id,
    permission=Permission.ADMIN
)

anya_us = WorkspaceMember(
    user_id=anya.id,
    workspace_id=us_trip.id,
    permission=Permission.ADMIN
)

dad_us = WorkspaceMember(
    user_id=dad.id,
    workspace_id=us_trip.id,
    permission=Permission.READ
)

session.add_all([sers_us, anya_us, dad_us])
session.flush()


# =========================
# ITALY TRIP
# Sers ADMIN
# Mom READ
# Dad READ
# Anya READ
# =========================

sers_italy = WorkspaceMember(
    user_id=sers.id,
    workspace_id=italy_trip.id,
    permission=Permission.ADMIN
)

mom_italy = WorkspaceMember(
    user_id=mom.id,
    workspace_id=italy_trip.id,
    permission=Permission.READ
)

dad_italy = WorkspaceMember(
    user_id=dad.id,
    workspace_id=italy_trip.id,
    permission=Permission.READ
)

anya_italy = WorkspaceMember(
    user_id=anya.id,
    workspace_id=italy_trip.id,
    permission=Permission.READ
)

session.add_all([
    sers_italy,
    mom_italy,
    dad_italy,
    anya_italy
])
session.flush()


# =========================
# MONEY TRANSFER
# Sers ADMIN
# Dad READ
# =========================

sers_transfer = WorkspaceMember(
    user_id=sers.id,
    workspace_id=money_transfer.id,
    permission=Permission.ADMIN
)

dad_transfer = WorkspaceMember(
    user_id=dad.id,
    workspace_id=money_transfer.id,
    permission=Permission.READ
)

session.add_all([sers_transfer, dad_transfer])
session.flush()


# =========================
# TRANSACTIONS
# =========================

# ---------- US TRIP ----------

# Sers pays 300 EUR, shared equally between Sers and Dad
serv_tr.shared_payment(
    session=session,
    workspace_id=us_trip.id,
    payer_id=sers_us.id,
    value=300,
    currency="EUR",
    description="Snowboard equipment",
    recipients_list=[
        sers_us.id,
        dad_us.id
    ]
)

# Anya pays 120 EUR for Dad
serv_tr.direct_transfer(
    session=session,
    workspace_id=us_trip.id,
    payer_member_id=anya_us.id,
    recipient_member_id=dad_us.id,
    value=120,
    currency="EUR",
    description="Hotel booking"
)


# ---------- ITALY TRIP ----------

# Sers pays 200 EUR, shared equally between all four
serv_tr.shared_payment(
    session=session,
    workspace_id=italy_trip.id,
    payer_id=sers_italy.id,
    value=200,
    currency="EUR",
    description="Dinner",
    recipients_list=[
        sers_italy.id,
        mom_italy.id,
        dad_italy.id,
        anya_italy.id
    ]
)

# Mom pays 80 EUR for Dad
serv_tr.direct_transfer(
    session=session,
    workspace_id=italy_trip.id,
    payer_member_id=mom_italy.id,
    recipient_member_id=dad_italy.id,
    value=80,
    currency="EUR",
    description="Train tickets"
)


# ---------- MONEY TRANSFER ----------

# Dad sends 500 EUR to Sers
serv_tr.direct_transfer(
    session=session,
    workspace_id=money_transfer.id,
    payer_member_id=dad_transfer.id,
    recipient_member_id=sers_transfer.id,
    value=500,
    currency="EUR",
    description="Money transfer"
)

# Sers sends 150 EUR back
serv_tr.direct_transfer(
    session=session,
    workspace_id=money_transfer.id,
    payer_member_id=sers_transfer.id,
    recipient_member_id=dad_transfer.id,
    value=150,
    currency="EUR",
    description="Money transfer back"
)


session.commit()

print("Database seeded successfully.")