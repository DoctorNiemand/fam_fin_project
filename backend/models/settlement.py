from sqlalchemy import ForeignKey, Enum, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from shared.currency import Currency
from sqlalchemy import DateTime
from datetime import datetime

from models.base import Base


class Settlement(Base):
	__tablename__ = "settlements"

	id: Mapped[int] = mapped_column(primary_key=True)
	workspace_id: Mapped[int] = mapped_column(
		ForeignKey("workspaces.id"),
		nullable=False
	)
	created_at: Mapped[datetime] = mapped_column(
		DateTime,
		nullable=False
	)

	items = relationship("SettlementItem", back_populates="settlement")

class SettlementItem(Base):
	__tablename__ = "settlement_items"

	id: Mapped[int] = mapped_column(primary_key=True)
	settlement_id: Mapped[int] = mapped_column(
		ForeignKey("settlements.id"),
		nullable=False
	)
	debtor_wsm_id: Mapped[int] = mapped_column(
		ForeignKey("workspace_members.id"),
		nullable=False
	)
	creditor_wsm_id: Mapped[int] = mapped_column(
		ForeignKey("workspace_members.id"),
		nullable=False
	)
	amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
	currency: Mapped[Currency] = mapped_column(Enum(Currency), nullable=False)
	transaction_id: Mapped[int | None] = mapped_column(
		ForeignKey("transactions.id"),
		nullable=True
	)

	settlement = relationship("Settlement", back_populates="items")
	debtor_wsm = relationship(
		"WorkspaceMember",
		foreign_keys=[debtor_wsm_id]
	)

	creditor_wsm = relationship(
		"WorkspaceMember",
		foreign_keys=[creditor_wsm_id]
	)
