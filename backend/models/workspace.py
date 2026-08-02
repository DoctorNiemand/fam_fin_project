from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from models.base import Base

class Workspace(Base):
	__tablename__ = "workspaces"

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String(100))
	created_at: Mapped[str] = mapped_column(String(80))  # immutable
	description: Mapped[str] = mapped_column(String(255))

	members = relationship("WorkspaceMember",  back_populates = "workspace")
	transactions = relationship("Transaction",  back_populates = "workspace")