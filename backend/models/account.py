from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from models.base import Base

class Account(Base):
	__tablename__ = "accounts"

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String(100))
	created_at: Mapped[str] = mapped_column(String(80)) # immutable
	acc_type: Mapped[str] = mapped_column(String(50)) # here lets make some presets like bank account/crypto/cash
	currency: Mapped[str] = mapped_column(String(50)) # here lets make some presets like usd / eur/ rub
	owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

	owner = relationship("User", back_populates="accounts")

	as_beneficiary = relationship(
			"Transaction",
			foreign_keys="Transaction.beneficiary_acc",
			back_populates="benef_acc"
			)
	as_source = relationship(
			"Transaction",
			foreign_keys="Transaction.source_acc",
			back_populates="sou_acc"
			)