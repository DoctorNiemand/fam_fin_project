from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from sqlalchemy import DateTime
from datetime import datetime
from shared.currency import Currency

from models.base import Base


class AccountType(PyEnum):
	BANK = "bank"
	CASH = "cash"
	CRYPTO = "crypto"

class Account(Base):
	__tablename__ = "accounts"

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String(100))
	created_at: Mapped[datetime] = mapped_column(DateTime)
	acc_type: Mapped[AccountType] = mapped_column(
						Enum(AccountType))
	currency: Mapped[Currency] = mapped_column(
                                        Enum(Currency))
	owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
	#active: Mapped[bool] = mapped_column(default=True, nullable=False)



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