from sqlalchemy import create_engine
from models.base import Base
from sqlalchemy.orm import sessionmaker

from models.user import User
from models.account import Account
from models.workspace import Workspace
from models.workspace_member import WorkspaceMember
from models.transaction import Transaction
from models.settlement import Settlement, SettlementItem


engine = create_engine(
    "sqlite:///finance.db",
    connect_args={"check_same_thread": False}
)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
