from sqlalchemy import String, ForeignKey, Enum, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from sqlalchemy import DateTime
from datetime import datetime
from shared.currency import Currency

from models.base import Base


class TransactionType(PyEnum):
	SHARED_PAYMENT = "shared_payment"
	DIRECT_TRANSFER = "direct_transfer"
	EXPENSE = "expense"


class Transaction(Base):
	__tablename__ = "transactions"
	id: Mapped[int] = mapped_column(primary_key=True)
	operation_id: Mapped[int | None] = mapped_column(nullable=True) # "layer above" the transaction id, e.g. for proper handling of shared
	created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
	description: Mapped[str | None] = mapped_column(String(255),nullable=True)
	transact_type: Mapped[TransactionType] = mapped_column(Enum(TransactionType),nullable=False)
	workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"),nullable=False)
	amount: Mapped[float] = mapped_column(Numeric(12, 2),nullable=False)
	currency: Mapped[Currency] = mapped_column(Enum(Currency),nullable=False)
	deleted_by: Mapped[int | None] = mapped_column(ForeignKey("workspace_members.id"),nullable=True)
	deleted_at: Mapped[datetime | None] = mapped_column(DateTime,nullable=True)
	beneficiary_acc: Mapped[int | None] = mapped_column(ForeignKey("accounts.id"),nullable=True)
	source_acc: Mapped[int | None] = mapped_column(ForeignKey("accounts.id"),nullable=True)
	data_source: Mapped[str | None] = mapped_column(String(50),nullable=True)
	beneficiary_workspace_member: Mapped[int] = mapped_column(ForeignKey("workspace_members.id"),nullable=False)
	source_workspace_member: Mapped[int] = mapped_column(ForeignKey("workspace_members.id"),nullable=False)


###
	benef_acc = relationship("Account", foreign_keys=[beneficiary_acc], back_populates = "as_beneficiary")
	sou_acc = relationship("Account", foreign_keys=[source_acc], back_populates ="as_source")

	benef_worksp_memb = relationship("WorkspaceMember", 
									foreign_keys=[beneficiary_workspace_member],
									back_populates = "as_beneficiary")
	sou_worksp_memb= relationship("WorkspaceMember", 
									foreign_keys=[source_workspace_member],
									back_populates = "as_source") # how does the mapping work here with severla foreignkeys from same table lol

	workspace = relationship("Workspace", back_populates = "transactions")

	#deleter = relationship() # 2-level stuff again, as must go up to the user