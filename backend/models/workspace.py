from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from datetime import datetime

from models.base import Base

class Workspace(Base):
	__tablename__ = "workspaces"

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String(100))
	created_at: Mapped[datetime] = mapped_column(DateTime)  # immutable
	description: Mapped[str] = mapped_column(String(255))
	active: Mapped[bool] = mapped_column(default=True, nullable=False)

###
	members = relationship("WorkspaceMember",  back_populates = "workspace")
	transactions = relationship("Transaction",  back_populates = "workspace")