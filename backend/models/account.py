from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[str] = mapped_column(String(80))
    acc_type: Mapped[str] = mapped_column(String(50)) # here lets make some presets like bank account/crypto/cash
    currency: Mapped[str] = mapped_column(String(50)) # here lets make some presets like usd / eur/ rub
    owner_id: Mapped[int] = mapped_column()